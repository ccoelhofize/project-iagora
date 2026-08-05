# SPDX-License-Identifier: EUPL-1.2

"""Fail-closed preparation of one protected remote admission decision."""

from __future__ import annotations

import copy
import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .acquisition import (
    validate_admission_review_semantics,
    validate_artifact_semantics,
    validate_attempt_semantics,
    validate_receipt_semantics,
)
from .acquisition_engine import _decode_and_validate, load_reviewed_plan
from .acquisition_transport import (
    AcquisitionFailure,
    OpendatasoftConnector,
    canonical_json_sha256,
)
from .contracts import ContractViolation, load_json, validate
from .remote_acquisition import (
    ISSUE_TITLE_PREFIX,
    REPOSITORY_PATTERN,
    extract_receipt_issue,
    render_receipt_issue,
    validate_remote_package_semantics,
)


SUPPORTED_PLAN_ID = "plan-city-schools-pilot-cases"
MAXIMUM_RATIONALE_LENGTH = 500


@dataclass(frozen=True)
class AdmissionProposal:
    directory: Path
    manifest: dict[str, Any]


def _utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def _iso(value: datetime) -> str:
    return _utc(value).isoformat().replace("+00:00", "Z")


def _parse(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ContractViolation("Admission timestamps must include a timezone")
    return parsed.astimezone(timezone.utc)


def _json_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")


def _sha256(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def _write_new(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as handle:
        handle.write(content)


def _safe_relative(value: str) -> Path:
    relative = Path(value)
    if relative.is_absolute() or ".." in relative.parts or not relative.parts:
        raise ContractViolation("Admission path must remain repository-relative")
    return relative


def validate_receipt_issue(
    issue: dict[str, Any], repository: str
) -> dict[str, Any]:
    """Validate one exact metadata-only receipt issue for admission use."""

    if not REPOSITORY_PATTERN.fullmatch(repository):
        raise ContractViolation("GitHub repository identifier is invalid")
    number = issue.get("number")
    title = issue.get("title")
    body = issue.get("body")
    if not isinstance(number, int) or number < 1:
        raise ContractViolation("Admission receipt issue number is invalid")
    if not isinstance(title, str) or not title.startswith(ISSUE_TITLE_PREFIX):
        raise ContractViolation("Admission input is not an IAgora receipt issue")
    if not isinstance(body, str):
        raise ContractViolation("Admission receipt issue body is unavailable")
    if issue.get("state") != "open" or "pull_request" in issue:
        raise ContractViolation("Admission requires one open receipt issue")
    receipt = extract_receipt_issue(body)
    root = Path(__file__).resolve().parents[2]
    validate(
        receipt,
        load_json(root / "contracts/v1/acquisition-receipt.schema.json"),
    )
    validate_receipt_semantics(receipt)
    if title != f"{ISSUE_TITLE_PREFIX}{receipt['attempt_id']}":
        raise ContractViolation("Admission receipt title and attempt disagree")
    return receipt


def receipt_resolution(
    issue: dict[str, Any], repository: str, now: datetime
) -> dict[str, Any]:
    """Return the bounded artifact coordinates from a still-pending receipt."""

    receipt = validate_receipt_issue(issue, repository)
    if receipt["record_origin"] != "live_execution":
        raise ContractViolation("Only a live receipt can enter remote admission")
    if receipt["review_state"] != "admission_pending":
        raise ContractViolation("Receipt is not pending human admission")
    if receipt["safe_outcome"] != "candidate_new_version":
        raise ContractViolation("Only a candidate new version can be admitted")
    if receipt["plan_reference"]["plan_id"] != SUPPORTED_PLAN_ID:
        raise ContractViolation("Admission receipt uses an unsupported plan")
    if not receipt["bytes_available"]:
        raise ContractViolation("Admission receipt no longer has available bytes")
    if _utc(now) >= _parse(receipt["package_expires_at"]):
        raise ContractViolation("Admission package has expired")
    return {
        "issue_number": issue["number"],
        "workflow_run_id": receipt["workflow_run_id"],
        "package_id": receipt["package_id"],
        "receipt": receipt,
    }


def _package_files(package_directory: Path) -> set[str]:
    files: set[str] = set()
    for path in package_directory.rglob("*"):
        if path.is_symlink():
            raise ContractViolation("Admission package cannot contain symbolic links")
        if path.is_file():
            files.add(path.relative_to(package_directory).as_posix())
    return files


def _target(
    proposal_directory: Path,
    target_path: str,
    content: bytes,
    role: str,
) -> dict[str, Any]:
    relative = _safe_relative(target_path)
    _write_new(proposal_directory / "files" / relative, content)
    return {
        "path": relative.as_posix(),
        "sha256": _sha256(content),
        "byte_size": len(content),
        "content_role": role,
    }


def _acquisition_event(
    plan: dict[str, Any],
    source: dict[str, Any],
    attempt: dict[str, Any],
    artifact: dict[str, Any],
    raw_target: str,
    request_url: str,
) -> dict[str, Any]:
    response = attempt["response"]
    suffix = artifact["sha256"][:12]
    acquired_date = _parse(attempt["started_at"]).strftime("%Y%m%d")
    return {
        "contract_id": "iagora.acquisition-event",
        "contract_version": "1.1.0",
        "event_id": f"acquisition-respire-selected-{acquired_date}-{suffix}",
        "source_id": source["source_id"],
        "artifact_version_id": artifact["artifact_version_id"],
        "requested_endpoint": attempt["requested_endpoint"],
        "resolved_url": request_url,
        "request": {
            "selected_fields": plan["query"]["selected_fields"],
            "uai": plan["observation_scope"]["identity_values"],
            "order_by": plan["query"]["order_by"],
            "limit": plan["query"]["result_limit"],
        },
        "acquired_at": attempt["started_at"],
        "method": "https_get",
        "response": {
            "http_status": response["http_status"],
            "media_type": response["media_type"],
            "byte_size": response["byte_size"],
            "record_count": response["record_count"],
        },
        "raw_artifact": {
            "local_path": raw_target,
            "sha256": artifact["sha256"],
            "immutable": True,
            "retention_class": "open_data_prototype",
        },
        "software": attempt["software"],
        "authentication_class": "public_unauthenticated",
        "rights": {
            "license_id": source["rights"]["license_id"],
            "attribution": source["publisher"],
            "redistribution": source["rights"]["redistribution"],
        },
        "privacy": {
            "classification": "public_school_level_aggregate",
            "coordinates_excluded": True,
            "image_metadata_excluded": True,
        },
        "security": {
            "risk_tier": source["security"]["risk_tier"],
            "content_treated_as_untrusted": True,
            "result": "accepted_after_contract_validation",
        },
        "limitations": [
            "Admission preserves the exact bounded selected-field response, not the full dataset.",
            "Source-reported values do not establish payment, competent completion, outcomes, impact, or campaign fulfillment.",
            "Repository admission does not authorize canonical interpretation or public product publication.",
        ],
    }


def validate_admission_proposal_semantics(proposal: dict[str, Any]) -> None:
    """Keep the decision and exact proposed target files consistent."""

    rationale = proposal["rationale"]
    if (
        len(rationale.strip()) < 10
        or len(rationale) > MAXIMUM_RATIONALE_LENGTH
        or "\n" in rationale
        or "\r" in rationale
    ):
        raise ContractViolation("Admission rationale must be one line of 10 to 500 characters")
    targets = proposal["target_files"]
    paths = [target["path"] for target in targets]
    if len(paths) != len(set(paths)):
        raise ContractViolation("Admission target paths must be unique")
    roles = [target["content_role"] for target in targets]
    attempt_suffix = proposal["attempt_id"].removeprefix("attempt-")
    if proposal["proposal_id"] != f"admission-proposal-{attempt_suffix}":
        raise ContractViolation("Admission proposal and attempt identifiers disagree")
    if proposal["admission_review_id"] != f"admission-review-{attempt_suffix}":
        raise ContractViolation("Admission review and attempt identifiers disagree")
    if proposal["decision"] == "admit":
        if sorted(roles) != sorted(
            ["candidate_raw_bytes", "acquisition_event", "source_change_report"]
        ):
            raise ContractViolation("Admission proposal requires exactly three governed targets")
        suffix = proposal["candidate"]["sha256"][:12]
        role_paths = {target["content_role"]: target["path"] for target in targets}
        raw_path = role_paths["candidate_raw_bytes"]
        event_path = role_paths["acquisition_event"]
        report_path = role_paths["source_change_report"]
        raw_prefix = "data/raw/respire-a-la-recre/"
        report_prefix = "data/acquisition/admissions/"
        if not raw_path.startswith(raw_prefix) or not raw_path.endswith(
            f"/records-selected-{suffix}.json"
        ):
            raise ContractViolation("Admission raw target is not deterministic")
        raw_date = raw_path.removeprefix(raw_prefix).split("/", 1)[0]
        if event_path != (
            f"{raw_prefix}{raw_date}/acquisition-event-{suffix}.json"
        ):
            raise ContractViolation("Admission event target is not deterministic")
        if report_path != (
            f"{report_prefix}{raw_date}/source-change-report-{suffix}.json"
        ):
            raise ContractViolation("Admission report target is not deterministic")
    elif targets:
        raise ContractViolation("Rejected proposal cannot contain admission targets")
    if proposal["publication_authorized"] or proposal["automatic_merge_allowed"]:
        raise ContractViolation("Admission proposal cannot publish or merge automatically")


def prepare_admission_proposal(
    *,
    root: Path,
    package_directory: Path,
    proposal_directory: Path,
    issue: dict[str, Any],
    repository: str,
    decision: str,
    rationale: str,
    now: datetime,
) -> AdmissionProposal:
    """Revalidate one exact candidate package and build a bounded proposal."""

    if decision not in {"admit", "reject"}:
        raise ContractViolation("Admission decision must be admit or reject")
    if (
        len(rationale.strip()) < 10
        or len(rationale) > MAXIMUM_RATIONALE_LENGTH
        or "\n" in rationale
        or "\r" in rationale
    ):
        raise ContractViolation("Admission rationale must be one line of 10 to 500 characters")
    resolution = receipt_resolution(issue, repository, now)
    receipt = resolution["receipt"]
    package_directory = package_directory.resolve()
    proposal_directory = proposal_directory.resolve()
    if root.resolve() in proposal_directory.parents or proposal_directory == root.resolve():
        raise ContractViolation("Admission proposal directory must remain outside the repository")
    proposal_directory.mkdir(parents=True, exist_ok=False)

    manifest_path = package_directory / "manifest.json"
    manifest = load_json(manifest_path)
    validate(
        manifest,
        load_json(root / "contracts/v1/remote-acquisition-package.schema.json"),
    )
    validate_remote_package_semantics(manifest)
    if manifest["package_id"] != resolution["package_id"]:
        raise ContractViolation("Receipt and package identifiers disagree")
    if manifest["workflow_run_id"] != resolution["workflow_run_id"]:
        raise ContractViolation("Receipt and package workflow runs disagree")
    if _utc(now) >= _parse(manifest["expires_at"]):
        raise ContractViolation("Admission package has expired")

    expected_files = {"manifest.json"}
    for component in manifest["component_files"]:
        relative = _safe_relative(component["path"])
        path = package_directory / relative
        if not path.is_file() or path.is_symlink():
            raise ContractViolation("Admission package component is missing or unsafe")
        content = path.read_bytes()
        if len(content) != component["byte_size"] or _sha256(content) != component["sha256"]:
            raise ContractViolation("Admission package component fingerprint mismatch")
        expected_files.add(relative.as_posix())
    if _package_files(package_directory) != expected_files:
        raise ContractViolation("Admission package contains unmanifested files")

    by_role = {
        component["content_role"]: package_directory / component["path"]
        for component in manifest["component_files"]
        if component["content_role"] not in {"safe_summary"}
    }
    package_receipt = load_json(by_role["receipt"])
    if package_receipt != receipt:
        raise ContractViolation("Issue receipt and packaged receipt differ")
    attempt = load_json(by_role["attempt_metadata"])
    artifact = load_json(by_role["artifact_metadata"])
    change_report = load_json(by_role["change_report"])
    raw_bytes = by_role["candidate_raw_bytes"].read_bytes()

    validate(attempt, load_json(root / "contracts/v1/acquisition-attempt.schema.json"))
    validate_attempt_semantics(attempt)
    validate(artifact, load_json(root / "contracts/v1/source-artifact-version.schema.json"))
    validate_artifact_semantics(artifact)
    validate(change_report, load_json(root / "contracts/v1/source-change-report.schema.json"))
    if attempt["outcome"] != "candidate_new_version":
        raise ContractViolation("Admission package does not contain a candidate")
    if attempt["execution_environment"] != "github_actions":
        raise ContractViolation("Admission candidate was not acquired by GitHub Actions")
    if any(state != "passed" for state in attempt["policy_decisions"].values()):
        raise ContractViolation("Admission candidate has an incomplete policy gate")
    if _sha256(raw_bytes) != artifact["sha256"] or len(raw_bytes) != artifact["byte_size"]:
        raise ContractViolation("Candidate bytes differ from artifact metadata")
    if not (
        manifest["attempt_id"]
        == receipt["attempt_id"]
        == attempt["attempt_id"]
        and manifest["outcome"]
        == receipt["safe_outcome"]
        == attempt["outcome"]
    ):
        raise ContractViolation("Admission package attempt relationships disagree")
    if not (
        manifest["artifact_version_id"]
        == attempt["artifact_version_id"]
        == artifact["artifact_version_id"]
        == change_report["candidate"]["artifact_version_id"]
    ):
        raise ContractViolation("Admission package artifact identifiers disagree")
    if not (
        receipt["sha256"]
        == artifact["sha256"]
        == change_report["candidate"]["sha256"]
        and receipt["byte_size"] == artifact["byte_size"]
        and receipt["media_type"] == artifact["media_type"]
    ):
        raise ContractViolation("Admission package candidate fingerprints disagree")
    if artifact["acquisition_attempt_ids"] != [attempt["attempt_id"]]:
        raise ContractViolation("Admission artifact and attempt linkage disagree")

    plan, source = load_reviewed_plan(root, SUPPORTED_PLAN_ID)
    compact_plan_reference = {
        "plan_id": plan["plan_id"],
        "plan_version": plan["plan_version"],
    }
    exact_plan_reference = {
        **compact_plan_reference,
        "plan_sha256": canonical_json_sha256(plan),
    }
    if manifest["plan_reference"] != exact_plan_reference:
        raise ContractViolation("Admission package plan reference is stale")
    if not (
        receipt["plan_reference"]
        == attempt["plan_reference"]
        == compact_plan_reference
    ):
        raise ContractViolation("Admission package plan version is stale")
    exact_source_reference = {
        "source_id": source["source_id"],
        "source_profile_version": source["version"],
    }
    if not (
        manifest["source_profile_reference"]
        == receipt["source_profile_reference"]
        == attempt["source_profile_reference"]
        == exact_source_reference
    ):
        raise ContractViolation("Admission package source profile is stale")
    if not (
        manifest["created_at"] == receipt["package_created_at"]
        and manifest["expires_at"] == receipt["package_expires_at"]
    ):
        raise ContractViolation("Admission package and receipt lifetimes disagree")
    expected_policy_states = {
        "validation": attempt["policy_decisions"]["contract_validation"],
        "rights": attempt["policy_decisions"]["rights"],
        "privacy": attempt["policy_decisions"]["privacy"],
        "security": attempt["policy_decisions"]["security"],
        "retention": attempt["policy_decisions"]["retention"],
    }
    if receipt["policy_states"] != expected_policy_states:
        raise ContractViolation("Admission receipt and policy decisions disagree")
    if not (
        artifact["storage"]["storage_state"] == "temporary_package"
        and artifact["lifecycle_state"] == "quarantined"
        and artifact["retention"]["retention_state"] == "temporary"
        and artifact["rights"]["license_id"]
        == plan["policy_gates"]["rights"]["license_id"]
        and artifact["rights"]["redistribution"]
        == plan["policy_gates"]["rights"]["redistribution"]
    ):
        raise ContractViolation("Admission artifact is not an eligible quarantined version")
    try:
        records = _decode_and_validate(raw_bytes, plan)
    except AcquisitionFailure as exc:
        raise ContractViolation("Candidate bytes no longer satisfy the reviewed plan") from exc
    request = OpendatasoftConnector().build_request(plan)
    if len(records) != attempt["response"]["record_count"]:
        raise ContractViolation("Admission candidate record counts disagree")
    if change_report["plan_reference"] != exact_plan_reference:
        raise ContractViolation("Admission change report plan reference is stale")
    if change_report["comparison_state"] != "candidate_changed":
        raise ContractViolation("Admission change report is not a changed candidate")
    if artifact["source_id"] != source["source_id"]:
        raise ContractViolation("Admission artifact source profile disagrees")
    if attempt["requested_endpoint"] != request.endpoint_url:
        raise ContractViolation("Admission attempt endpoint differs from the reviewed plan")
    if attempt["resolved_url"] != request.endpoint_url:
        raise ContractViolation("Admission attempt followed an unsupported final endpoint")

    acquired_date = _parse(attempt["started_at"]).date().isoformat()
    suffix = artifact["sha256"][:12]
    raw_target = (
        f"data/raw/respire-a-la-recre/{acquired_date}/"
        f"records-selected-{suffix}.json"
    )
    event_target = (
        f"data/raw/respire-a-la-recre/{acquired_date}/"
        f"acquisition-event-{suffix}.json"
    )
    report_target = (
        f"data/acquisition/admissions/{acquired_date}/"
        f"source-change-report-{suffix}.json"
    )
    review_id = f"admission-review-{attempt['attempt_id'].removeprefix('attempt-')}"
    targets: list[dict[str, Any]] = []
    if decision == "admit":
        event = _acquisition_event(
            plan, source, attempt, artifact, raw_target, request.request_url
        )
        validate(event, load_json(root / "contracts/v1/acquisition-event.schema.json"))
        targets.extend(
            (
                _target(proposal_directory, raw_target, raw_bytes, "candidate_raw_bytes"),
                _target(proposal_directory, event_target, _json_bytes(event), "acquisition_event"),
                _target(
                    proposal_directory,
                    report_target,
                    _json_bytes(change_report),
                    "source_change_report",
                ),
            )
        )

    proposal = {
        "contract_id": "iagora.admission-proposal",
        "contract_version": "1.0.0",
        "proposal_id": f"admission-proposal-{attempt['attempt_id'].removeprefix('attempt-')}",
        "record_origin": "live_execution",
        "repository": repository,
        "receipt_issue_number": issue["number"],
        "receipt_sha256": canonical_json_sha256(receipt),
        "prepared_at": _iso(now),
        "decision": decision,
        "rationale": rationale.strip(),
        "reviewer_role": "maintainer",
        "package_reference": {
            "package_id": manifest["package_id"],
            "workflow_run_id": manifest["workflow_run_id"],
            "created_at": manifest["created_at"],
            "expires_at": manifest["expires_at"],
        },
        "package_manifest_sha256": _sha256(manifest_path.read_bytes()),
        "attempt_id": attempt["attempt_id"],
        "artifact_version_id": artifact["artifact_version_id"],
        "plan_reference": manifest["plan_reference"],
        "source_profile_reference": manifest["source_profile_reference"],
        "candidate": {
            "sha256": artifact["sha256"],
            "byte_size": artifact["byte_size"],
            "media_type": artifact["media_type"],
            "record_count": len(records),
        },
        "target_files": sorted(targets, key=lambda item: item["path"]),
        "admission_review_id": review_id,
        "publication_authorized": False,
        "automatic_merge_allowed": False,
        "limitations": [
            "Protected prototype admission proposal; it is not a civic conclusion or publication authorization.",
            "Applying an admit decision may create only a dedicated branch and pull request; main and merge remain human-controlled.",
        ],
    }
    validate(
        proposal,
        load_json(root / "contracts/v1/admission-proposal.schema.json"),
    )
    validate_admission_proposal_semantics(proposal)
    _write_new(proposal_directory / "proposal.json", _json_bytes(proposal))
    return AdmissionProposal(proposal_directory, proposal)


def validate_proposal_directory(root: Path, directory: Path) -> dict[str, Any]:
    """Revalidate the protected handoff before the write-capable job acts."""

    proposal = load_json(directory / "proposal.json")
    validate(
        proposal,
        load_json(root / "contracts/v1/admission-proposal.schema.json"),
    )
    validate_admission_proposal_semantics(proposal)
    expected = {"proposal.json"}
    for target in proposal["target_files"]:
        relative = _safe_relative(target["path"])
        path = directory / "files" / relative
        if not path.is_file() or path.is_symlink():
            raise ContractViolation("Admission proposal target is missing or unsafe")
        content = path.read_bytes()
        if len(content) != target["byte_size"] or _sha256(content) != target["sha256"]:
            raise ContractViolation("Admission proposal target fingerprint mismatch")
        expected.add(f"files/{relative.as_posix()}")
    if _package_files(directory) != expected:
        raise ContractViolation("Admission proposal contains unmanifested files")
    return proposal


def build_admission_review(
    proposal: dict[str, Any], decided_at: datetime, pull_request_url: str | None
) -> dict[str, Any]:
    """Build the final human decision record after the protected action."""

    admitted = proposal["decision"] == "admit"
    if admitted and pull_request_url is None:
        raise ContractViolation("Admitted review requires its pull request URL")
    review = {
        "contract_id": "iagora.admission-review",
        "contract_version": "1.0.0",
        "review_id": proposal["admission_review_id"],
        "record_origin": proposal["record_origin"],
        "package_id": proposal["package_reference"]["package_id"],
        "artifact_version_id": proposal["artifact_version_id"],
        "attempt_id": proposal["attempt_id"],
        "plan_reference": {
            "plan_id": proposal["plan_reference"]["plan_id"],
            "plan_version": proposal["plan_reference"]["plan_version"],
        },
        "source_profile_reference": proposal["source_profile_reference"],
        "rule_versions": {
            "connector": "0.1.0",
            "contract_validation": "1.0.0",
            "policy_validation": "0.1.0",
        },
        "deterministic_checks": [
            {"check_id": "package-fingerprint", "result": "passed"},
            {"check_id": "component-fingerprints", "result": "passed"},
            {"check_id": "plan-boundary", "result": "passed"},
            {"check_id": "rights-privacy-security-retention", "result": "passed"},
            {"check_id": "candidate-contract", "result": "passed"},
            {"check_id": "human-evidence-review", "result": "passed"},
        ],
        "review_state": "admitted" if admitted else "rejected",
        "reviewer_role": proposal["reviewer_role"],
        "decided_at": _iso(decided_at),
        "rationale": proposal["rationale"],
        "targets": [target["path"] for target in proposal["target_files"]],
        "pull_request_url": pull_request_url,
        "publication_authorized": False,
        "automatic_merge_allowed": False,
        "limitations": [
            "Maintainer prototype admission is not independent public-release review.",
            "Admission preserves evidence and lineage but does not establish civic truth, fulfillment, outcome, or impact.",
        ],
        "required_follow_up": [
            "Review and merge remain separate human actions.",
            "Canonical interpretation and public product publication remain separately governed.",
        ],
    }
    root = Path(__file__).resolve().parents[2]
    validate(review, load_json(root / "contracts/v1/admission-review.schema.json"))
    validate_admission_review_semantics(review)
    return review


def decided_receipt(
    receipt: dict[str, Any],
    proposal: dict[str, Any],
    decided_at: datetime,
    pull_request_url: str | None,
) -> dict[str, Any]:
    """Return the final durable operational receipt state."""

    updated = copy.deepcopy(receipt)
    if canonical_json_sha256(updated) != proposal["receipt_sha256"]:
        raise ContractViolation("Receipt changed after admission preparation")
    admitted = proposal["decision"] == "admit"
    updated["review_state"] = "admitted" if admitted else "rejected"
    updated["decision_at"] = _iso(decided_at)
    updated["decision_rationale"] = proposal["rationale"]
    updated["admission_review_id"] = proposal["admission_review_id"]
    updated["pull_request_url"] = pull_request_url
    if not admitted:
        updated["bytes_available"] = False
    validate_receipt_semantics(updated)
    return updated


def rendered_decided_issue(
    receipt: dict[str, Any], repository: str
) -> dict[str, str]:
    """Render the decided receipt without adding civic interpretation."""

    return render_receipt_issue(receipt, repository)
