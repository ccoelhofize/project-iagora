# SPDX-License-Identifier: EUPL-1.2

"""Deterministic Increment 0 contracts and historical acquisition fixtures.

This module performs no network or repository write. It validates the first
bounded plan and projects the three existing acquisition events into the new
generalized contracts without changing their historical records.
"""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from .contracts import ContractViolation, load_json, validate, validate_files


FIRST_PLAN_PATH = Path("data/acquisition/plans/plan-city-schools-pilot-cases.json")
PENDING_REVIEW_FIXTURE_PATH = Path(
    "data/acquisition/fixtures/admission-review-pending.synthetic.json"
)
HISTORICAL_ACQUISITION_PATHS = (
    Path("data/raw/respire-a-la-recre/2026-07-29/acquisition-event.json"),
    Path("data/raw/procurement/city-contracts/2026-07-30/acquisition-event.json"),
    Path("data/raw/procurement/city-contracts/2026-08-01/acquisition-event.json"),
)

FIRST_PLAN_UAIS = (
    "0630258N",
    "0630268Z",
    "0630303M",
    "0630307S",
    "0630992L",
    "0631845N",
)
FIRST_PLAN_FIELDS = (
    "uai",
    "denomination_ecole",
    "nature",
    "nombre_d_enfants_concernes",
    "annee_vegetalisation",
    "vegetalisation_terminee",
    "cour_commune",
    "nombre_de_cours_concernees",
    "surface_de_la_cour_existante",
    "surface_de_la_cour_apres_vegetalisation",
    "nombre_d_arbres_existant",
    "nb_arbres_plantes",
    "surface_demineralisee_en_m2_surface_nette",
    "pourcentage_de_surface_totale_de_la_cour_rendue_permeable",
)


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()


def _source_index(profiles: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {source["source_id"]: source for source in profiles["sources"]}


def validate_plan_against_source(
    plan: dict[str, Any], source_profile: dict[str, Any]
) -> None:
    """Validate cross-contract gates that JSON Schema alone cannot express."""

    reference = plan["source_profile_reference"]
    if reference != {
        "source_id": source_profile["source_id"],
        "source_profile_version": source_profile["version"],
    }:
        raise ContractViolation("Acquisition plan does not bind the exact source profile version")
    if source_profile["status"] != "approved_prototype":
        raise ContractViolation("Acquisition plan source is not approved for prototype use")
    if source_profile["acquisition"] != {
        "mode": "bounded_api_query",
        "frequency": "one_off",
        "prototype_authorized": True,
    }:
        raise ContractViolation("Source profile does not authorize this bounded prototype mode")

    canonical_host = urlparse(source_profile["canonical_url"]).hostname
    if canonical_host != plan["transport_policy"]["allowed_host"]:
        raise ContractViolation("Acquisition plan host differs from the registered source host")
    if plan["connector"]["dataset_id"] not in plan["transport_policy"]["endpoint_path"]:
        raise ContractViolation("Acquisition endpoint path does not contain the reviewed dataset")

    rights_gate = plan["policy_gates"]["rights"]
    if rights_gate["required_state"] != source_profile["rights"]["state"]:
        raise ContractViolation("Acquisition rights state differs from the source profile")
    if rights_gate["license_id"] != source_profile["rights"]["license_id"]:
        raise ContractViolation("Acquisition licence differs from the source profile")
    if rights_gate["redistribution"] != source_profile["rights"]["redistribution"]:
        raise ContractViolation("Acquisition redistribution gate differs from the source profile")

    privacy_gate = plan["policy_gates"]["privacy"]
    if privacy_gate["classification"] != source_profile["privacy"]["classification"]:
        raise ContractViolation("Acquisition privacy class differs from the source profile")
    if privacy_gate["personal_data_expected"] != source_profile["privacy"]["personal_data_expected"]:
        raise ContractViolation("Acquisition personal-data expectation differs from the source profile")
    if privacy_gate["child_data_allowed"] or source_profile["privacy"]["child_data_allowed"]:
        raise ContractViolation("Child-level data must remain prohibited")

    security_gate = plan["policy_gates"]["security"]
    if security_gate["risk_tier"] != source_profile["security"]["risk_tier"]:
        raise ContractViolation("Acquisition security tier differs from the source profile")
    if security_gate["arbitrary_url_allowed"]:
        raise ContractViolation("Acquisition plans must never enable arbitrary URLs")
    if plan["admission_policy"] != {
        "human_review_required": True,
        "direct_main_write_allowed": False,
        "automatic_merge_allowed": False,
        "publication_authorized": False,
    }:
        raise ContractViolation("Acquisition admission policy must remain fail-closed")


def validate_first_plan_boundary(plan: dict[str, Any]) -> None:
    """Keep the initial plan exactly within the RFC-reviewed six-school scope."""

    if plan["plan_id"] != "plan-city-schools-pilot-cases" or plan["plan_version"] != "0.1.0":
        raise ContractViolation("Unexpected first acquisition plan identity")
    if plan["lifecycle_state"] != "approved_prototype":
        raise ContractViolation("First acquisition plan is not approved for bounded prototype use")
    if tuple(plan["observation_scope"]["identity_values"]) != FIRST_PLAN_UAIS:
        raise ContractViolation("First acquisition plan must remain bounded to the six reviewed UAIs")
    if tuple(plan["query"]["selected_fields"]) != FIRST_PLAN_FIELDS:
        raise ContractViolation("First acquisition plan fields differ from the reviewed field set")
    if plan["query"]["result_limit"] != 10:
        raise ContractViolation("First acquisition plan result limit must remain 10")
    policy = plan["transport_policy"]
    if policy["maximum_accepted_records"] != len(FIRST_PLAN_UAIS):
        raise ContractViolation("First acquisition plan may accept only six records")
    if policy["maximum_response_bytes"] != 65536:
        raise ContractViolation("First acquisition plan response limit must remain 64 KiB")
    if policy["timeout_seconds"] != 20 or policy["maximum_redirects"] != 2:
        raise ContractViolation("First acquisition timeout or redirect bound changed")
    if plan["review"]["review_state"] != "approved_for_bounded_prototype":
        raise ContractViolation("First acquisition plan review gate is not approved")


def validate_attempt_semantics(attempt: dict[str, Any]) -> None:
    """Enforce attempt invariants that depend on more than one field."""

    successful_outcomes = {"unchanged", "candidate_new_version"}
    if attempt["outcome"] in successful_outcomes:
        if attempt["safe_failure_code"] is not None:
            raise ContractViolation("Successful acquisition outcome cannot carry a failure code")
        if attempt["artifact_version_id"] is None:
            raise ContractViolation("Successful acquisition outcome must reference an artifact version")
    elif attempt["safe_failure_code"] is None:
        raise ContractViolation("Unsuccessful acquisition outcome must carry a safe failure code")

    if attempt["record_origin"] == "live_execution":
        if attempt["plan_reference"] is None:
            raise ContractViolation("Live acquisition attempt must bind an exact plan version")
        if attempt["source_profile_reference"]["source_profile_version"] is None:
            raise ContractViolation("Live acquisition attempt must bind a source-profile version")
        if attempt["connector_reference"]["connector_rule_version"] is None:
            raise ContractViolation("Live acquisition attempt must bind a connector-rule version")
        if attempt["completed_at"] is None:
            raise ContractViolation("Persisted live acquisition attempt must have a completion time")
    elif attempt["execution_environment"] != "compatibility_fixture":
        raise ContractViolation("Retrospective attempt must use the compatibility environment")


def validate_artifact_semantics(artifact: dict[str, Any]) -> None:
    """Keep byte preservation, storage, and non-retention states consistent."""

    storage = artifact["storage"]
    if artifact["raw_bytes_preserved"]:
        if storage["storage_state"] == "not_retained" or storage["storage_reference"] is None:
            raise ContractViolation("Preserved raw bytes require a storage reference")
        if artifact["non_retention_reason"] is not None:
            raise ContractViolation("Preserved raw bytes cannot carry a non-retention reason")
    else:
        if storage["storage_state"] != "not_retained" or storage["storage_reference"] is not None:
            raise ContractViolation("Unpreserved bytes must use the not-retained storage state")
        if not artifact["non_retention_reason"]:
            raise ContractViolation("Unpreserved bytes require a governed non-retention reason")

    if artifact["record_origin"] == "live_execution":
        if storage["storage_state"] != "not_retained" and not storage["content_addressed"]:
            raise ContractViolation("Retained live artifacts must use content-addressed storage")


def validate_receipt_semantics(receipt: dict[str, Any]) -> None:
    """Enforce the safe package and expiry lifecycle without inspecting raw bytes."""

    if receipt["sha256"] is None:
        if receipt["byte_size"] is not None or receipt["media_type"] is not None:
            raise ContractViolation("Receipt without a fingerprint cannot claim byte metadata")
        if receipt["bytes_available"]:
            raise ContractViolation("Receipt without a fingerprint cannot claim available bytes")

    terminal_without_bytes = {"rejected", "expired_without_admission"}
    if receipt["review_state"] in terminal_without_bytes and receipt["bytes_available"]:
        raise ContractViolation("Rejected or expired receipt cannot retain available package bytes")

    if receipt["record_origin"] == "live_execution":
        if receipt["plan_reference"] is None:
            raise ContractViolation("Live receipt must bind an exact plan version")
        if receipt["source_profile_reference"]["source_profile_version"] is None:
            raise ContractViolation("Live receipt must bind a source-profile version")
        if receipt["review_state"] in {"admission_pending", "extended"}:
            required_package_fields = (
                "package_id",
                "package_created_at",
                "reminder_due_at",
                "package_expires_at",
            )
            if any(receipt[field] is None for field in required_package_fields):
                raise ContractViolation("Reviewable live receipt requires package deadline metadata")
            if not receipt["bytes_available"]:
                raise ContractViolation("Pending or extended package bytes must remain available")
        if receipt["review_state"] in {"admitted", "rejected", "extended"}:
            if receipt["decision_at"] is None or not receipt["decision_rationale"]:
                raise ContractViolation("Recorded live decision requires time and rationale")
        if receipt["review_state"] == "expired_without_admission" and receipt["decision_at"] is None:
            raise ContractViolation("Expired live receipt requires its recorded expiry transition time")


def validate_admission_review_semantics(review: dict[str, Any]) -> None:
    """Keep pending examples undecided and real decisions attributable to a human role."""

    if review["review_state"] == "admission_pending":
        if any(
            value is not None
            for value in (review["reviewer_role"], review["decided_at"], review["rationale"])
        ):
            raise ContractViolation("Pending admission review cannot contain a decision")
        if review["targets"] or review["pull_request_url"] is not None:
            raise ContractViolation("Pending admission review cannot contain admission targets")
    else:
        if review["reviewer_role"] is None or review["decided_at"] is None or not review["rationale"]:
            raise ContractViolation("Admission decision requires reviewer role, time, and rationale")
    if review["review_state"] == "admitted":
        if not review["targets"] or review["pull_request_url"] is None:
            raise ContractViolation("Admitted review requires target paths and a pull request")
    if review["publication_authorized"] or review["automatic_merge_allowed"]:
        raise ContractViolation("Admission review cannot authorize publication or automatic merge")


def project_historical_acquisition(
    event: dict[str, Any], raw_path: Path, root: Path
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    """Project one exact historical event as transparent compatibility fixtures."""

    expected_relative_path = event["raw_artifact"]["local_path"]
    relative_path = Path(expected_relative_path)
    if relative_path.is_absolute() or ".." in relative_path.parts:
        raise ContractViolation("Historical raw artifact path must be repository-relative")
    if raw_path.resolve() != (root / relative_path).resolve():
        raise ContractViolation("Historical raw artifact path differs from its event")
    if not raw_path.is_file():
        raise ContractViolation("Historical raw artifact is missing")
    if _file_sha256(raw_path) != event["raw_artifact"]["sha256"]:
        raise ContractViolation("Historical raw artifact fingerprint mismatch")
    if raw_path.stat().st_size != event["response"]["byte_size"]:
        raise ContractViolation("Historical raw artifact byte-size mismatch")

    event_suffix = event["event_id"].removeprefix("acquisition-")
    attempt_id = f"attempt-compat-{event_suffix}"
    source_reference = {
        "source_id": event["source_id"],
        "source_profile_version": None,
    }
    policy_states = {
        "validation": "passed",
        "rights": "passed",
        "privacy": "passed",
        "security": "passed",
        "retention": "passed",
    }
    attempt = {
        "contract_id": "iagora.acquisition-attempt",
        "contract_version": "1.0.0",
        "attempt_id": attempt_id,
        "record_origin": "retrospective_compatibility_fixture",
        "plan_reference": None,
        "source_profile_reference": source_reference,
        "connector_reference": {
            "connector_type": "opendatasoft_explore_v2_json",
            "connector_rule_version": None,
        },
        "started_at": event["acquired_at"],
        "completed_at": event["acquired_at"],
        "execution_environment": "compatibility_fixture",
        "requested_endpoint": event["requested_endpoint"],
        "resolved_url": event["resolved_url"],
        "outcome": "candidate_new_version",
        "safe_failure_code": None,
        "response": {
            "http_status": event["response"]["http_status"],
            "media_type": event["response"]["media_type"],
            "byte_size": event["response"]["byte_size"],
            "record_count": event["response"]["record_count"],
            "duration_milliseconds": None,
        },
        "policy_decisions": {
            "contract_validation": "passed",
            "rights": "passed",
            "privacy": "passed",
            "security": "passed",
            "retention": "passed",
        },
        "artifact_version_id": event["artifact_version_id"],
        "retry_of": None,
        "correlation_id": f"correlation-compat-{event_suffix}",
        "software": event["software"],
        "limitations": [
            "Retrospective compatibility projection from a pre-RFC acquisition event; no versioned acquisition plan, source-profile version, connector-rule version, duration, or correlation identifier was recorded at acquisition time.",
            *event["limitations"],
        ],
    }
    artifact = {
        "contract_id": "iagora.source-artifact-version",
        "contract_version": "1.0.0",
        "artifact_id": f"artifact-{event['artifact_version_id']}",
        "artifact_version_id": event["artifact_version_id"],
        "record_origin": "retrospective_compatibility_fixture",
        "source_id": event["source_id"],
        "sha256": event["raw_artifact"]["sha256"],
        "byte_size": event["response"]["byte_size"],
        "media_type": event["response"]["media_type"],
        "acquisition_attempt_ids": [attempt_id],
        "storage": {
            "storage_state": "retained_repository",
            "storage_reference": expected_relative_path,
            "content_addressed": False,
        },
        "source_modified_at": None,
        "published_at": None,
        "rights": {
            "license_id": event["rights"]["license_id"],
            "redistribution": event["rights"]["redistribution"],
        },
        "access": event["authentication_class"],
        "retention": {
            "retention_class": event["raw_artifact"]["retention_class"],
            "retention_state": "active",
        },
        "lifecycle_state": "admitted",
        "supersedes": None,
        "possible_supersession_of": None,
        "raw_bytes_preserved": True,
        "non_retention_reason": None,
        "limitations": [
            "Retrospective compatibility projection; the repository path is not a content-addressed quarantine reference.",
            "Source publication and modification times were not recorded in the historical acquisition event."
        ],
    }
    receipt = {
        "contract_id": "iagora.acquisition-receipt",
        "contract_version": "1.0.0",
        "receipt_id": f"receipt-compat-{event_suffix}",
        "record_origin": "retrospective_compatibility_fixture",
        "attempt_id": attempt_id,
        "package_id": None,
        "workflow_run_id": None,
        "plan_reference": None,
        "source_profile_reference": source_reference,
        "attempted_at": event["acquired_at"],
        "safe_outcome": "candidate_new_version",
        "media_type": event["response"]["media_type"],
        "byte_size": event["response"]["byte_size"],
        "sha256": event["raw_artifact"]["sha256"],
        "policy_states": policy_states,
        "package_created_at": None,
        "reminder_due_at": None,
        "package_expires_at": None,
        "extension_count": 0,
        "review_state": "admitted",
        "decision_at": None,
        "decision_rationale": "The exact bytes are already present in the repository; this is a retrospective compatibility representation, not a contemporaneous admission decision.",
        "admission_review_id": None,
        "pull_request_url": None,
        "bytes_available": True,
        "limitations": [
            "No temporary package, workflow run, deadline, reminder, or admission-review record existed for this pre-RFC acquisition.",
            "This receipt projection is validation evidence only and must not be presented as a historical operational receipt."
        ],
    }
    return attempt, artifact, receipt


def validate_acquisition_increment(root: Path) -> dict[str, Any]:
    """Validate the Increment 0 contracts, plan, and compatibility projections."""

    contracts = root / "contracts" / "v1"
    profiles = validate_files(
        root / "data/sources/source-profiles.json",
        contracts / "source-profiles.schema.json",
    )
    plan = validate_files(root / FIRST_PLAN_PATH, contracts / "acquisition-plan.schema.json")
    source = _source_index(profiles).get(plan["source_profile_reference"]["source_id"])
    if source is None:
        raise ContractViolation("Acquisition plan references an unknown source profile")
    validate_plan_against_source(plan, source)
    validate_first_plan_boundary(plan)

    pending_review = validate_files(
        root / PENDING_REVIEW_FIXTURE_PATH,
        contracts / "admission-review.schema.json",
    )
    if pending_review["record_origin"] != "synthetic_non_civic_fixture":
        raise ContractViolation("Pending admission review example must remain explicitly synthetic")
    validate_admission_review_semantics(pending_review)

    historical_schema = load_json(contracts / "acquisition-event.schema.json")
    generalized_schemas = (
        load_json(contracts / "acquisition-attempt.schema.json"),
        load_json(contracts / "source-artifact-version.schema.json"),
        load_json(contracts / "acquisition-receipt.schema.json"),
    )
    projections = []
    source_ids = set(_source_index(profiles))
    for event_relative_path in HISTORICAL_ACQUISITION_PATHS:
        event = load_json(root / event_relative_path)
        validate(event, historical_schema)
        if event["source_id"] not in source_ids:
            raise ContractViolation("Historical acquisition references an unknown source profile")
        raw_path = root / event["raw_artifact"]["local_path"]
        projection = project_historical_acquisition(event, raw_path, root)
        for instance, schema in zip(projection, generalized_schemas, strict=True):
            validate(instance, schema)
        validate_attempt_semantics(projection[0])
        validate_artifact_semantics(projection[1])
        validate_receipt_semantics(projection[2])
        projections.append(projection)

    return {
        "plan": plan,
        "pending_review_fixture": pending_review,
        "historical_projections": projections,
    }
