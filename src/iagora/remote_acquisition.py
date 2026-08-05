# SPDX-License-Identifier: EUPL-1.2

"""GitHub-runner package and metadata-only receipt adapters.

This module never contacts a civic source or the GitHub API. It converts the
result of the portable acquisition core into a bounded temporary review package
and plans deterministic receipt-issue transitions for thin workflow adapters.
"""

from __future__ import annotations

import base64
import copy
import hashlib
import json
import re
import shutil
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from .acquisition import validate_receipt_semantics
from .acquisition_engine import (
    AcquisitionResult,
    LocalQuarantineStore,
    load_reviewed_plan,
)
from .contracts import ContractViolation, load_json, validate


ISSUE_TITLE_PREFIX = "IAgora acquisition receipt — "
RECEIPT_START = "<!-- iagora-receipt-json:start -->"
RECEIPT_END = "<!-- iagora-receipt-json:end -->"
REPOSITORY_PATTERN = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
RECEIPT_SCHEMA_PATH = (
    Path(__file__).resolve().parents[2]
    / "contracts/v1/acquisition-receipt.schema.json"
)


@dataclass(frozen=True)
class RemotePackage:
    """Safe outputs created for the remote workflow adapters."""

    package_directory: Path
    manifest: dict[str, Any]
    receipt: dict[str, Any]
    issue_payload_base64: str
    safe_summary: dict[str, Any]


def _utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def _iso(value: datetime) -> str:
    return _utc(value).isoformat().replace("+00:00", "Z")


def _parse_datetime(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ContractViolation("Receipt timestamps must include a timezone")
    return parsed.astimezone(timezone.utc)


def _json_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")


def _write_new(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as handle:
        handle.write(content)


def _component(path: Path, package_directory: Path, role: str) -> dict[str, Any]:
    relative = path.relative_to(package_directory).as_posix()
    content = path.read_bytes()
    return {
        "path": relative,
        "sha256": hashlib.sha256(content).hexdigest(),
        "byte_size": len(content),
        "content_role": role,
    }


def _review_state(outcome: str) -> str:
    if outcome == "candidate_new_version":
        return "admission_pending"
    if outcome == "unchanged":
        return "no_admission_required"
    return "not_reviewable"


def _receipt(
    *,
    result: AcquisitionResult,
    plan: dict[str, Any],
    source: dict[str, Any],
    workflow_run_id: str,
    package_id: str,
    created_at: datetime,
) -> dict[str, Any]:
    outcome = result.attempt["outcome"]
    review_state = _review_state(outcome)
    sha256 = result.safe_summary()["sha256"]
    has_fingerprinted_bytes = sha256 is not None
    reminder_due = created_at + timedelta(
        days=plan["policy_gates"]["retention"]["reminder_day"]
    )
    expires_at = created_at + timedelta(
        days=plan["policy_gates"]["retention"]["temporary_package_days"]
    )
    response = result.attempt["response"]
    receipt = {
        "contract_id": "iagora.acquisition-receipt",
        "contract_version": "1.1.0",
        "receipt_id": f"receipt-{result.attempt['attempt_id'].removeprefix('attempt-')}",
        "record_origin": "live_execution",
        "attempt_id": result.attempt["attempt_id"],
        "package_id": package_id,
        "workflow_run_id": workflow_run_id,
        "plan_reference": {
            "plan_id": plan["plan_id"],
            "plan_version": plan["plan_version"],
        },
        "source_profile_reference": {
            "source_id": source["source_id"],
            "source_profile_version": source["version"],
        },
        "attempted_at": result.attempt["started_at"],
        "safe_outcome": outcome,
        "media_type": response["media_type"] if has_fingerprinted_bytes else None,
        "byte_size": response["byte_size"] if has_fingerprinted_bytes else None,
        "sha256": sha256,
        "policy_states": {
            "validation": result.attempt["policy_decisions"]["contract_validation"],
            "rights": result.attempt["policy_decisions"]["rights"],
            "privacy": result.attempt["policy_decisions"]["privacy"],
            "security": result.attempt["policy_decisions"]["security"],
            "retention": result.attempt["policy_decisions"]["retention"],
        },
        "package_created_at": _iso(created_at),
        "reminder_due_at": (
            _iso(reminder_due) if review_state == "admission_pending" else None
        ),
        "reminder_sent_at": None,
        "package_expires_at": _iso(expires_at),
        "extension_count": 0,
        "review_state": review_state,
        "decision_at": None,
        "decision_rationale": None,
        "admission_review_id": None,
        "pull_request_url": None,
        "bytes_available": outcome in {"unchanged", "candidate_new_version"},
        "limitations": [
            "Operational metadata receipt only; it is not civic evidence, a source-of-truth decision, an admission review, or publication authorization.",
            "A candidate remains quarantined and cannot enter canonical, search, AI-retrieval, assessment, or public stores without a later human admission decision.",
        ],
    }
    if outcome == "unchanged":
        receipt["limitations"].append(
            "The exact bytes already exist in the governed prototype evidence tree and are not duplicated in the temporary package."
        )
    if review_state == "not_reviewable":
        receipt["limitations"].append(
            "The attempt produced no remotely reviewable raw object; only safe failure and package metadata are retained."
        )
    return receipt


def render_receipt_issue(receipt: dict[str, Any], repository: str) -> dict[str, str]:
    """Render a safe, machine-updatable GitHub issue payload."""

    if not REPOSITORY_PATTERN.fullmatch(repository):
        raise ContractViolation("GitHub repository identifier is invalid")
    run_url = (
        f"https://github.com/{repository}/actions/runs/{receipt['workflow_run_id']}"
    )
    body = "\n".join(
        (
            "# IAgora acquisition receipt",
            "",
            "This issue is an operational, metadata-only receipt. It contains no response body, request query, secret, personal path, admission decision, or civic conclusion.",
            "",
            f"- Workflow run: {run_url}",
            f"- Review state: `{receipt['review_state']}`",
            f"- Temporary package expiry: `{receipt['package_expires_at']}`",
            "",
            RECEIPT_START,
            json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True),
            RECEIPT_END,
            "",
            "The issue lifecycle is operational only. Closing it does not admit or publish evidence.",
        )
    )
    return {
        "title": f"{ISSUE_TITLE_PREFIX}{receipt['attempt_id']}",
        "body": body,
    }


def extract_receipt_issue(body: str) -> dict[str, Any]:
    """Extract the exact receipt JSON from an issue body."""

    start = body.find(RECEIPT_START)
    end = body.find(RECEIPT_END)
    if start < 0 or end < 0 or end <= start:
        raise ContractViolation("Issue does not contain an IAgora receipt envelope")
    raw = body[start + len(RECEIPT_START) : end].strip()
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ContractViolation("Issue receipt JSON is malformed") from exc
    if not isinstance(value, dict):
        raise ContractViolation("Issue receipt must be a JSON object")
    return value


def transition_receipt(
    receipt: dict[str, Any], now: datetime
) -> tuple[str, dict[str, Any]]:
    """Return the deterministic reminder or expiry transition due at ``now``."""

    current = copy.deepcopy(receipt)
    validate_receipt_semantics(current)
    if current["record_origin"] != "live_execution":
        return "none", current
    if current["review_state"] not in {"admission_pending", "extended"}:
        return "none", current
    current_time = _utc(now)
    expires_at = _parse_datetime(current["package_expires_at"])
    if current_time >= expires_at:
        current["review_state"] = "expired_without_admission"
        current["decision_at"] = _iso(current_time)
        current["decision_rationale"] = (
            "The temporary GitHub Actions package expired without a recorded human admission decision."
        )
        current["bytes_available"] = False
        validate_receipt_semantics(current)
        return "expire", current
    reminder_due = _parse_datetime(current["reminder_due_at"])
    if current_time >= reminder_due and current["reminder_sent_at"] is None:
        current["reminder_sent_at"] = _iso(current_time)
        validate_receipt_semantics(current)
        return "remind", current
    return "none", current


def plan_issue_updates(
    issues: list[dict[str, Any]], repository: str, now: datetime
) -> list[dict[str, Any]]:
    """Plan safe issue-body updates without contacting GitHub."""

    updates = []
    receipt_schema = load_json(RECEIPT_SCHEMA_PATH)
    for issue in issues:
        if "pull_request" in issue:
            continue
        title = issue.get("title")
        body = issue.get("body")
        number = issue.get("number")
        if not isinstance(title, str) or not title.startswith(ISSUE_TITLE_PREFIX):
            continue
        if not isinstance(body, str) or not isinstance(number, int):
            continue
        receipt = extract_receipt_issue(body)
        validate(receipt, receipt_schema)
        validate_receipt_semantics(receipt)
        action, transitioned = transition_receipt(receipt, now)
        if action == "none":
            continue
        payload = render_receipt_issue(transitioned, repository)
        comment = (
            "Reminder: this temporary acquisition package is due for a human admission decision before its 14-day expiry. No civic source was contacted by this reminder."
            if action == "remind"
            else "The temporary package expired without a recorded admission decision. The receipt remains as safe operational metadata; a later retrieval would be a new acquisition."
        )
        updates.append(
            {
                "issue_number": number,
                "action": action,
                "body": payload["body"],
                "comment": comment,
                "close_issue": action == "expire",
            }
        )
    return updates


def validate_remote_package_semantics(manifest: dict[str, Any]) -> None:
    """Enforce package relationships that JSON Schema cannot express alone."""

    components = manifest["component_files"]
    paths = [component["path"] for component in components]
    if len(paths) != len(set(paths)):
        raise ContractViolation("Remote package component paths must be unique")

    role_counts: dict[str, int] = {}
    for component in components:
        role = component["content_role"]
        role_counts[role] = role_counts.get(role, 0) + 1
    if role_counts.get("attempt_metadata") != 1:
        raise ContractViolation("Remote package requires one attempt metadata file")
    if role_counts.get("receipt") != 1:
        raise ContractViolation("Remote package requires one receipt file")
    if role_counts.get("safe_summary") != 2:
        raise ContractViolation("Remote package requires JSON and Markdown safe summaries")

    expected_review_states = {
        "candidate_new_version": "admission_pending",
        "unchanged": "no_admission_required",
        "quarantined_validation_failure": "not_reviewable",
        "blocked_by_policy": "not_reviewable",
        "transport_failure": "not_reviewable",
    }
    if manifest["review_state"] != expected_review_states[manifest["outcome"]]:
        raise ContractViolation("Remote package outcome and review state disagree")

    raw_count = role_counts.get("candidate_raw_bytes", 0)
    candidate = manifest["outcome"] == "candidate_new_version"
    if manifest["raw_bytes_included"] != candidate or raw_count != int(candidate):
        raise ContractViolation("Remote package raw-byte eligibility is inconsistent")
    if candidate:
        if manifest["artifact_version_id"] is None:
            raise ContractViolation("Candidate package requires an artifact version")
        if role_counts.get("artifact_metadata") != 1:
            raise ContractViolation("Candidate package requires artifact metadata")
        if role_counts.get("change_report") != 1:
            raise ContractViolation("Candidate package requires one change report")
    elif manifest["outcome"] == "unchanged":
        if manifest["artifact_version_id"] is None:
            raise ContractViolation("Unchanged package requires its governed artifact version")
        if role_counts.get("change_report") != 1:
            raise ContractViolation("Unchanged package requires one comparison report")

    created_at = _parse_datetime(manifest["created_at"])
    expires_at = _parse_datetime(manifest["expires_at"])
    if expires_at - created_at != timedelta(days=14):
        raise ContractViolation("Remote package must use the reviewed 14-day lifetime")


def build_remote_package(
    *,
    root: Path,
    quarantine: LocalQuarantineStore,
    package_directory: Path,
    result: AcquisitionResult,
    workflow_run_id: str,
    repository: str,
    now: datetime,
) -> RemotePackage:
    """Build one validated, bounded, temporary GitHub review package."""

    package_directory = package_directory.expanduser().resolve()
    repository_root = root.resolve()
    if package_directory == repository_root or repository_root in package_directory.parents:
        raise ContractViolation("Remote package directory must remain outside the repository")
    if (
        package_directory == quarantine.root
        or quarantine.root in package_directory.parents
        or package_directory in quarantine.root.parents
    ):
        raise ContractViolation("Remote package and quarantine directories must not overlap")
    package_directory.mkdir(parents=True, exist_ok=False)

    plan_id = result.attempt["plan_reference"]["plan_id"]
    plan, source = load_reviewed_plan(root, plan_id)
    created_at = _utc(now)
    package_id = f"package-{result.attempt['attempt_id'].removeprefix('attempt-')}"
    receipt = _receipt(
        result=result,
        plan=plan,
        source=source,
        workflow_run_id=workflow_run_id,
        package_id=package_id,
        created_at=created_at,
    )
    receipt_schema = load_json(root / "contracts/v1/acquisition-receipt.schema.json")
    validate(receipt, receipt_schema)
    validate_receipt_semantics(receipt)

    components: list[dict[str, Any]] = []
    attempt_path = package_directory / "metadata/attempt.json"
    _write_new(attempt_path, _json_bytes(result.attempt))
    components.append(_component(attempt_path, package_directory, "attempt_metadata"))

    if result.artifact is not None:
        artifact_path = package_directory / "metadata/artifact.json"
        _write_new(artifact_path, _json_bytes(result.artifact))
        components.append(
            _component(artifact_path, package_directory, "artifact_metadata")
        )
    if result.change_report is not None:
        report_path = package_directory / "metadata/change-report.json"
        _write_new(report_path, _json_bytes(result.change_report))
        components.append(_component(report_path, package_directory, "change_report"))

    raw_bytes_included = result.attempt["outcome"] == "candidate_new_version"
    if raw_bytes_included:
        if result.artifact is None:
            raise ContractViolation("Candidate package requires artifact metadata")
        stored = quarantine.existing_object(result.artifact)
        source_path = quarantine.root / stored.storage_reference
        raw_path = package_directory / f"candidate/{stored.sha256}.json"
        raw_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_path, raw_path)
        components.append(
            _component(raw_path, package_directory, "candidate_raw_bytes")
        )

    safe_summary = result.safe_summary()
    summary_path = package_directory / "safe-summary.json"
    _write_new(summary_path, _json_bytes(safe_summary))
    components.append(_component(summary_path, package_directory, "safe_summary"))

    receipt_path = package_directory / "receipt.json"
    _write_new(receipt_path, _json_bytes(receipt))
    components.append(_component(receipt_path, package_directory, "receipt"))

    summary_markdown = "\n".join(
        (
            "## IAgora bounded acquisition",
            "",
            f"- Plan: `{safe_summary['plan_id']}` version `{safe_summary['plan_version']}`",
            f"- Attempt: `{safe_summary['attempt_id']}`",
            f"- Outcome: `{safe_summary['outcome']}`",
            f"- Review state: `{receipt['review_state']}`",
            f"- Package expires: `{receipt['package_expires_at']}`",
            "- Admission: `not_admitted`",
            "- Publication authorized: `false`",
            "",
            "This is an operational result, not evidence of civic truth, delivery, outcome, impact, or campaign fulfillment.",
            "",
        )
    ).encode("utf-8")
    summary_markdown_path = package_directory / "summary.md"
    _write_new(summary_markdown_path, summary_markdown)
    components.append(
        _component(summary_markdown_path, package_directory, "safe_summary")
    )

    manifest = {
        "contract_id": "iagora.remote-acquisition-package",
        "contract_version": "1.0.0",
        "package_id": package_id,
        "workflow_run_id": workflow_run_id,
        "created_at": receipt["package_created_at"],
        "expires_at": receipt["package_expires_at"],
        "plan_reference": {
            "plan_id": plan["plan_id"],
            "plan_version": plan["plan_version"],
            "plan_sha256": result.plan_sha256,
        },
        "source_profile_reference": receipt["source_profile_reference"],
        "attempt_id": result.attempt["attempt_id"],
        "outcome": result.attempt["outcome"],
        "review_state": receipt["review_state"],
        "artifact_version_id": result.attempt["artifact_version_id"],
        "component_files": sorted(components, key=lambda item: item["path"]),
        "raw_bytes_included": raw_bytes_included,
        "admission_state": "not_admitted",
        "publication_authorized": False,
        "limitations": [
            "Temporary 14-day GitHub Actions review package; it is not the governed evidence store.",
            "Only a structurally valid candidate new version may include raw bytes; validation failures export safe metadata only.",
            "Package creation does not admit, canonicalize, assess, publish, commit, merge, or deploy any civic information.",
        ],
    }
    manifest_schema = load_json(
        root / "contracts/v1/remote-acquisition-package.schema.json"
    )
    validate(manifest, manifest_schema)
    validate_remote_package_semantics(manifest)
    manifest_path = package_directory / "manifest.json"
    _write_new(manifest_path, _json_bytes(manifest))

    issue_payload = render_receipt_issue(receipt, repository)
    issue_payload_base64 = base64.b64encode(_json_bytes(issue_payload)).decode("ascii")
    return RemotePackage(
        package_directory=package_directory,
        manifest=manifest,
        receipt=receipt,
        issue_payload_base64=issue_payload_base64,
        safe_summary=safe_summary,
    )
