# SPDX-License-Identifier: EUPL-1.2

"""Portable local acquisition core and content-addressed quarantine adapter."""

from __future__ import annotations

import hashlib
import json
import os
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from .acquisition import (
    FIRST_PLAN_PATH,
    HISTORICAL_ACQUISITION_PATHS,
    validate_artifact_semantics,
    validate_attempt_semantics,
    validate_first_plan_boundary,
    validate_plan_against_source,
)
from .acquisition_transport import (
    AcquisitionFailure,
    OpendatasoftConnector,
    Transport,
    canonical_json_sha256,
)
from .contracts import ContractViolation, load_json, validate, validate_files


ENGINE_VERSION = "0.1.0"
CHANGE_RULE_VERSION = "0.1.0"
PLAN_REGISTRY = {"plan-city-schools-pilot-cases": FIRST_PLAN_PATH}


@dataclass(frozen=True)
class BaselineArtifact:
    artifact_version_id: str
    sha256: str
    raw_path: Path
    records: dict[str, dict[str, Any]]


@dataclass(frozen=True)
class StoredObject:
    sha256: str
    byte_size: int
    storage_reference: str
    created: bool


@dataclass(frozen=True)
class AcquisitionResult:
    plan_sha256: str
    attempt: dict[str, Any]
    artifact: dict[str, Any] | None
    change_report: dict[str, Any] | None
    object_created: bool

    def safe_summary(self) -> dict[str, Any]:
        """Return a body-free, URL-free, personal-path-free operator summary."""

        response = self.attempt["response"]
        sha256 = self.artifact["sha256"] if self.artifact else (
            self.change_report["candidate"]["sha256"] if self.change_report else None
        )
        return {
            "plan_id": self.attempt["plan_reference"]["plan_id"],
            "plan_version": self.attempt["plan_reference"]["plan_version"],
            "plan_sha256": self.plan_sha256,
            "attempt_id": self.attempt["attempt_id"],
            "outcome": self.attempt["outcome"],
            "safe_failure_code": self.attempt["safe_failure_code"],
            "artifact_version_id": self.attempt["artifact_version_id"],
            "sha256": sha256,
            "byte_size": response["byte_size"],
            "record_count": response["record_count"],
            "object_created": self.object_created,
            "change_summary": (
                self.change_report["summary"] if self.change_report else None
            ),
            "admission_state": "not_admitted",
            "publication_authorized": False,
        }


class LocalQuarantineStore:
    """Append-only local CAS that must remain outside the repository."""

    def __init__(self, root: Path, repository_root: Path) -> None:
        self.root = root.expanduser().resolve()
        repository = repository_root.resolve()
        if self.root == repository or repository in self.root.parents:
            raise ContractViolation(
                "The quarantine directory must remain outside the repository"
            )
        self.root.mkdir(parents=True, exist_ok=True)

    def _absolute(self, relative: Path) -> Path:
        if relative.is_absolute() or ".." in relative.parts:
            raise ContractViolation("Quarantine references must remain store-relative")
        target = (self.root / relative).resolve()
        if target != self.root and self.root not in target.parents:
            raise ContractViolation("Quarantine reference escapes the configured store")
        return target

    def _atomic_create(self, relative: Path, content: bytes) -> bool:
        target = self._absolute(relative)
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            if target.read_bytes() != content:
                raise ContractViolation(
                    "Append-only quarantine metadata conflicts with existing content"
                )
            return False

        temporary = target.parent / f".iagora-{uuid.uuid4().hex}.tmp"
        try:
            with temporary.open("xb") as handle:
                handle.write(content)
                handle.flush()
                os.fsync(handle.fileno())
            try:
                os.link(temporary, target)
                return True
            except FileExistsError:
                if target.read_bytes() != content:
                    raise ContractViolation(
                        "Concurrent quarantine write produced conflicting content"
                    )
                return False
        finally:
            if temporary.exists():
                temporary.unlink()

    @staticmethod
    def _json_bytes(value: dict[str, Any]) -> bytes:
        return (
            json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
        ).encode("utf-8")

    def put_object(self, body: bytes) -> StoredObject:
        sha256 = hashlib.sha256(body).hexdigest()
        relative = Path("objects") / "sha256" / sha256[:2] / f"{sha256}.bin"
        created = self._atomic_create(relative, body)
        return StoredObject(
            sha256=sha256,
            byte_size=len(body),
            storage_reference=relative.as_posix(),
            created=created,
        )

    def existing_object(self, artifact: dict[str, Any]) -> StoredObject:
        reference = Path(artifact["storage"]["storage_reference"])
        path = self._absolute(reference)
        if not path.is_file():
            raise ContractViolation(
                "Quarantine metadata exists but its bytes are unavailable; automatic restoration is prohibited"
            )
        body = path.read_bytes()
        sha256 = hashlib.sha256(body).hexdigest()
        if sha256 != artifact["sha256"] or len(body) != artifact["byte_size"]:
            raise ContractViolation("Quarantine object differs from its artifact metadata")
        return StoredObject(
            sha256=sha256,
            byte_size=len(body),
            storage_reference=reference.as_posix(),
            created=False,
        )

    def write_attempt(self, attempt: dict[str, Any]) -> None:
        self._atomic_create(
            Path("attempts") / f"{attempt['attempt_id']}.json",
            self._json_bytes(attempt),
        )

    def artifact_path(self, artifact_version_id: str) -> Path:
        return self._absolute(Path("artifacts") / f"{artifact_version_id}.json")

    def load_artifact(self, artifact_version_id: str) -> dict[str, Any] | None:
        path = self.artifact_path(artifact_version_id)
        return load_json(path) if path.is_file() else None

    def write_artifact(self, artifact: dict[str, Any]) -> None:
        self._atomic_create(
            Path("artifacts") / f"{artifact['artifact_version_id']}.json",
            self._json_bytes(artifact),
        )

    def write_change_report(self, report: dict[str, Any]) -> None:
        self._atomic_create(
            Path("change-reports") / f"{report['report_id']}.json",
            self._json_bytes(report),
        )


def load_reviewed_plan(root: Path, plan_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
    """Load one allowlisted plan and its exact registered source profile."""

    relative_path = PLAN_REGISTRY.get(plan_id)
    if relative_path is None:
        raise AcquisitionFailure(
            "plan_invalid",
            "The requested acquisition plan is not registered.",
            outcome="blocked_by_policy",
        )
    contracts = root / "contracts" / "v1"
    plan = validate_files(root / relative_path, contracts / "acquisition-plan.schema.json")
    profiles = validate_files(
        root / "data/sources/source-profiles.json",
        contracts / "source-profiles.schema.json",
    )
    source = next(
        (
            item
            for item in profiles["sources"]
            if item["source_id"] == plan["source_profile_reference"]["source_id"]
        ),
        None,
    )
    if source is None:
        raise AcquisitionFailure(
            "plan_invalid",
            "The acquisition plan references an unknown source profile.",
            outcome="blocked_by_policy",
        )
    try:
        validate_plan_against_source(plan, source)
        validate_first_plan_boundary(plan)
    except ContractViolation as exc:
        raise AcquisitionFailure(
            "plan_invalid",
            "The acquisition plan failed its deterministic policy gates.",
            outcome="blocked_by_policy",
        ) from exc
    return plan, source


def _load_baseline(root: Path, plan: dict[str, Any]) -> BaselineArtifact:
    if plan["plan_id"] != "plan-city-schools-pilot-cases":
        raise ContractViolation("No reviewed baseline is configured for this plan")
    event = load_json(root / HISTORICAL_ACQUISITION_PATHS[0])
    raw_path = root / event["raw_artifact"]["local_path"]
    body = raw_path.read_bytes()
    if hashlib.sha256(body).hexdigest() != event["raw_artifact"]["sha256"]:
        raise ContractViolation("The reviewed baseline fingerprint no longer matches")
    payload = json.loads(body.decode("utf-8"))
    records = {record["uai"]: record for record in payload["results"]}
    return BaselineArtifact(
        artifact_version_id=event["artifact_version_id"],
        sha256=event["raw_artifact"]["sha256"],
        raw_path=raw_path,
        records=records,
    )


def _validate_payload(payload: Any, plan: dict[str, Any]) -> dict[str, dict[str, Any]]:
    if not isinstance(payload, dict) or set(payload) != {"total_count", "results"}:
        raise AcquisitionFailure(
            "malformed_response",
            "The response does not match the reviewed Opendatasoft envelope.",
            outcome="quarantined_validation_failure",
        )
    results = payload["results"]
    if not isinstance(payload["total_count"], int) or not isinstance(results, list):
        raise AcquisitionFailure(
            "malformed_response",
            "The response count or record collection has an invalid type.",
            outcome="quarantined_validation_failure",
        )
    maximum = plan["transport_policy"]["maximum_accepted_records"]
    if len(results) > maximum or payload["total_count"] > maximum:
        raise AcquisitionFailure(
            "record_limit_exceeded",
            "The response exceeds the reviewed record limit.",
            outcome="quarantined_validation_failure",
        )
    if payload["total_count"] != len(results):
        raise AcquisitionFailure(
            "malformed_response",
            "The response count differs from the returned record collection.",
            outcome="quarantined_validation_failure",
        )

    expected_fields = set(plan["query"]["selected_fields"])
    identity_field = plan["observation_scope"]["identity_field"]
    expected_identities = set(plan["observation_scope"]["identity_values"])
    records: dict[str, dict[str, Any]] = {}
    for record in results:
        if not isinstance(record, dict) or set(record) != expected_fields:
            raise AcquisitionFailure(
                "contract_invalid",
                "A response record differs from the reviewed selected-field contract.",
                outcome="quarantined_validation_failure",
            )
        identity = record.get(identity_field)
        if not isinstance(identity, str) or identity not in expected_identities:
            raise AcquisitionFailure(
                "unexpected_identity",
                "A response record contains an unexpected or malformed identity.",
                outcome="quarantined_validation_failure",
            )
        if identity in records:
            raise AcquisitionFailure(
                "duplicate_identity",
                "The response contains a duplicate reviewed identity.",
                outcome="quarantined_validation_failure",
            )
        records[identity] = record
    if set(records) != expected_identities:
        raise AcquisitionFailure(
            "missing_expected_record",
            "The response omits one or more reviewed identities.",
            outcome="quarantined_validation_failure",
        )
    return records


def _decode_and_validate(
    body: bytes, plan: dict[str, Any]
) -> dict[str, dict[str, Any]]:
    try:
        payload = json.loads(body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise AcquisitionFailure(
            "malformed_response",
            "The response is not valid UTF-8 JSON.",
            outcome="quarantined_validation_failure",
        ) from exc
    return _validate_payload(payload, plan)


def _build_change_report(
    *,
    plan: dict[str, Any],
    plan_sha256: str,
    baseline: BaselineArtifact,
    candidate_artifact_version_id: str,
    candidate_sha256: str,
    candidate_records: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    changes: list[dict[str, Any]] = []
    changed_identities: set[str] = set()
    baseline_ids = set(baseline.records)
    candidate_ids = set(candidate_records)

    for identity in sorted(candidate_ids - baseline_ids):
        changed_identities.add(identity)
        changes.append(
            {
                "identity": identity,
                "change_type": "record_added",
                "field": None,
                "before": None,
                "after": candidate_records[identity],
            }
        )
    for identity in sorted(baseline_ids - candidate_ids):
        changed_identities.add(identity)
        changes.append(
            {
                "identity": identity,
                "change_type": "record_removed",
                "field": None,
                "before": baseline.records[identity],
                "after": None,
            }
        )
    for identity in sorted(baseline_ids & candidate_ids):
        before = baseline.records[identity]
        after = candidate_records[identity]
        for field in sorted(set(before) | set(after)):
            if before.get(field) != after.get(field):
                changed_identities.add(identity)
                changes.append(
                    {
                        "identity": identity,
                        "change_type": "field_changed",
                        "field": field,
                        "before": before.get(field),
                        "after": after.get(field),
                    }
                )

    unchanged_records = len((baseline_ids & candidate_ids) - changed_identities)
    comparison_state = "unchanged" if not changes else "candidate_changed"
    report = {
        "contract_id": "iagora.source-change-report",
        "contract_version": "1.0.0",
        "report_id": f"change-report-{plan['plan_id'].removeprefix('plan-')}-{candidate_sha256[:16]}",
        "plan_reference": {
            "plan_id": plan["plan_id"],
            "plan_version": plan["plan_version"],
            "plan_sha256": plan_sha256,
        },
        "baseline": {
            "artifact_version_id": baseline.artifact_version_id,
            "sha256": baseline.sha256,
        },
        "candidate": {
            "artifact_version_id": candidate_artifact_version_id,
            "sha256": candidate_sha256,
        },
        "comparison_state": comparison_state,
        "identity_field": plan["observation_scope"]["identity_field"],
        "summary": {
            "records_added": len(candidate_ids - baseline_ids),
            "records_removed": len(baseline_ids - candidate_ids),
            "records_changed": len(changed_identities & baseline_ids & candidate_ids),
            "records_unchanged": unchanged_records,
            "fields_changed": sum(
                item["change_type"] == "field_changed" for item in changes
            ),
        },
        "changes": changes,
        "generated_by": {
            "rule_id": "opendatasoft-record-diff",
            "rule_version": CHANGE_RULE_VERSION,
        },
        "limitations": [
            "This deterministic report describes source-record differences only; it does not establish truth, correction, temporal validity, delivery, outcome, impact, or campaign fulfillment.",
            "A changed value remains a quarantined candidate until human admission and later evidence review."
        ],
    }
    return report


def _utc_iso(value: datetime) -> str:
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _default_identifier(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex}"


def _safe_endpoint(url: str | None) -> str | None:
    if url is None:
        return None
    from urllib.parse import urlsplit, urlunsplit

    parsed = urlsplit(url)
    return urlunsplit((parsed.scheme, parsed.netloc, parsed.path, "", ""))


def _attempt(
    *,
    plan: dict[str, Any],
    source: dict[str, Any],
    record_origin: str,
    execution_environment: str,
    attempt_id: str,
    correlation_id: str,
    started_at: str,
    completed_at: str,
    endpoint_url: str,
    outcome: str,
    safe_failure_code: str | None,
    resolved_url: str | None,
    http_status: int | None,
    media_type: str | None,
    byte_size: int | None,
    record_count: int | None,
    duration_milliseconds: int | None,
    artifact_version_id: str | None,
) -> dict[str, Any]:
    contract_state = "failed" if outcome == "quarantined_validation_failure" else (
        "not_run" if outcome == "transport_failure" else "passed"
    )
    security_state = "not_run" if record_origin == "offline_replay" else (
        "blocked"
        if safe_failure_code in {
            "redirect_blocked",
            "response_too_large",
            "unauthorized_endpoint",
            "unexpected_media_type",
            "unsupported_content_encoding",
        }
        else "passed"
    )
    return {
        "contract_id": "iagora.acquisition-attempt",
        "contract_version": "1.0.0",
        "attempt_id": attempt_id,
        "record_origin": record_origin,
        "plan_reference": {
            "plan_id": plan["plan_id"],
            "plan_version": plan["plan_version"],
        },
        "source_profile_reference": {
            "source_id": source["source_id"],
            "source_profile_version": source["version"],
        },
        "connector_reference": {
            "connector_type": plan["connector"]["connector_type"],
            "connector_rule_version": plan["connector"]["connector_rule_version"],
        },
        "started_at": started_at,
        "completed_at": completed_at,
        "execution_environment": execution_environment,
        "requested_endpoint": endpoint_url,
        "resolved_url": _safe_endpoint(resolved_url),
        "outcome": outcome,
        "safe_failure_code": safe_failure_code,
        "response": {
            "http_status": http_status,
            "media_type": media_type,
            "byte_size": byte_size,
            "record_count": record_count,
            "duration_milliseconds": duration_milliseconds,
        },
        "policy_decisions": {
            "contract_validation": contract_state,
            "rights": "passed",
            "privacy": "passed",
            "security": security_state,
            "retention": "passed",
        },
        "artifact_version_id": artifact_version_id,
        "retry_of": None,
        "correlation_id": correlation_id,
        "software": f"project-iagora-acquisition/{ENGINE_VERSION}",
        "limitations": [
            "This attempt records technical acquisition processing, not source authority, civic truth, temporal validity, delivery, outcome, impact, or campaign fulfillment.",
            "Local quarantine content is unadmitted and cannot enter canonical, search, AI-retrieval, assessment, or public stores."
        ],
    }


def _candidate_artifact(
    *,
    plan: dict[str, Any],
    source: dict[str, Any],
    record_origin: str,
    attempt_id: str,
    stored: StoredObject,
    media_type: str,
    baseline: BaselineArtifact,
) -> dict[str, Any]:
    source_slug = source["source_id"].removeprefix("src-")
    artifact_version_id = f"dataset-{source_slug}-candidate-{stored.sha256[:16]}"
    return {
        "contract_id": "iagora.source-artifact-version",
        "contract_version": "1.0.0",
        "artifact_id": f"artifact-{source_slug}",
        "artifact_version_id": artifact_version_id,
        "record_origin": record_origin,
        "source_id": source["source_id"],
        "sha256": stored.sha256,
        "byte_size": stored.byte_size,
        "media_type": media_type,
        "acquisition_attempt_ids": [attempt_id],
        "storage": {
            "storage_state": "temporary_package",
            "storage_reference": stored.storage_reference,
            "content_addressed": True,
        },
        "source_modified_at": None,
        "published_at": None,
        "rights": {
            "license_id": source["rights"]["license_id"],
            "redistribution": source["rights"]["redistribution"],
        },
        "access": "public_unauthenticated",
        "retention": {
            "retention_class": plan["policy_gates"]["retention"]["retention_class"],
            "retention_state": "temporary",
        },
        "lifecycle_state": "quarantined",
        "supersedes": None,
        "possible_supersession_of": baseline.artifact_version_id,
        "raw_bytes_preserved": True,
        "non_retention_reason": None,
        "limitations": [
            "Unadmitted local quarantine artifact; storage outside the repository is not a governed evidence store or public source.",
            "Possible supersession is a byte and field comparison only and does not establish that the newer source value is authoritative or temporally applicable."
        ],
    }


class AcquisitionEngine:
    """Environment-independent orchestration for one manually invoked plan."""

    def __init__(
        self,
        root: Path,
        store: LocalQuarantineStore,
        *,
        now: Callable[[], datetime] = lambda: datetime.now(timezone.utc),
        identifier: Callable[[str], str] = _default_identifier,
        execution_environment: str = "local",
    ) -> None:
        self.root = root.resolve()
        self.store = store
        self._now = now
        self._identifier = identifier
        if execution_environment not in {"local", "github_actions"}:
            raise ContractViolation("Acquisition execution environment is not supported")
        self.execution_environment = execution_environment

    def run(self, plan_id: str, transport: Transport) -> AcquisitionResult:
        plan, source = load_reviewed_plan(self.root, plan_id)
        connector = OpendatasoftConnector()
        request = connector.build_request(plan)
        baseline = _load_baseline(self.root, plan)
        plan_sha256 = canonical_json_sha256(plan)
        attempt_id = self._identifier("attempt")
        correlation_id = self._identifier("correlation")
        started_at = _utc_iso(self._now())
        attempt_schema = load_json(
            self.root / "contracts/v1/acquisition-attempt.schema.json"
        )
        artifact_schema = load_json(
            self.root / "contracts/v1/source-artifact-version.schema.json"
        )
        report_schema = load_json(
            self.root / "contracts/v1/source-change-report.schema.json"
        )
        record_origin = transport.record_origin
        if record_origin not in {"live_execution", "offline_replay"}:
            raise ContractViolation("Transport record origin is not supported")

        try:
            response = transport.fetch(request)
        except AcquisitionFailure as failure:
            completed_at = _utc_iso(self._now())
            attempt = _attempt(
                plan=plan,
                source=source,
                record_origin=record_origin,
                execution_environment=self.execution_environment,
                attempt_id=attempt_id,
                correlation_id=correlation_id,
                started_at=started_at,
                completed_at=completed_at,
                endpoint_url=request.endpoint_url,
                outcome=failure.outcome,
                safe_failure_code=failure.safe_code,
                resolved_url=failure.resolved_url,
                http_status=failure.http_status,
                media_type=failure.media_type,
                byte_size=failure.byte_size,
                record_count=None,
                duration_milliseconds=failure.duration_milliseconds,
                artifact_version_id=None,
            )
            validate(attempt, attempt_schema)
            validate_attempt_semantics(attempt)
            self.store.write_attempt(attempt)
            return AcquisitionResult(plan_sha256, attempt, None, None, False)

        sha256 = hashlib.sha256(response.body).hexdigest()
        if sha256 == baseline.sha256:
            records = _decode_and_validate(response.body, plan)
            report = _build_change_report(
                plan=plan,
                plan_sha256=plan_sha256,
                baseline=baseline,
                candidate_artifact_version_id=baseline.artifact_version_id,
                candidate_sha256=sha256,
                candidate_records=records,
            )
            attempt = _attempt(
                plan=plan,
                source=source,
                record_origin=record_origin,
                execution_environment=self.execution_environment,
                attempt_id=attempt_id,
                correlation_id=correlation_id,
                started_at=started_at,
                completed_at=_utc_iso(self._now()),
                endpoint_url=request.endpoint_url,
                outcome="unchanged",
                safe_failure_code=None,
                resolved_url=response.resolved_url,
                http_status=response.http_status,
                media_type=response.media_type,
                byte_size=len(response.body),
                record_count=len(records),
                duration_milliseconds=response.duration_milliseconds,
                artifact_version_id=baseline.artifact_version_id,
            )
            validate(attempt, attempt_schema)
            validate_attempt_semantics(attempt)
            validate(report, report_schema)
            self.store.write_change_report(report)
            self.store.write_attempt(attempt)
            return AcquisitionResult(plan_sha256, attempt, None, report, False)

        artifact_version_id = (
            f"dataset-{source['source_id'].removeprefix('src-')}-candidate-{sha256[:16]}"
        )
        existing_artifact = self.store.load_artifact(artifact_version_id)
        if existing_artifact is None:
            stored = self.store.put_object(response.body)
            artifact = _candidate_artifact(
                plan=plan,
                source=source,
                record_origin=record_origin,
                attempt_id=attempt_id,
                stored=stored,
                media_type=response.media_type,
                baseline=baseline,
            )
            validate(artifact, artifact_schema)
            validate_artifact_semantics(artifact)
            self.store.write_artifact(artifact)
        else:
            artifact = existing_artifact
            validate(artifact, artifact_schema)
            validate_artifact_semantics(artifact)
            if artifact["sha256"] != sha256:
                raise ContractViolation("Quarantine artifact identifier collision")
            stored = self.store.existing_object(artifact)

        try:
            records = _decode_and_validate(response.body, plan)
        except AcquisitionFailure as failure:
            attempt = _attempt(
                plan=plan,
                source=source,
                record_origin=record_origin,
                execution_environment=self.execution_environment,
                attempt_id=attempt_id,
                correlation_id=correlation_id,
                started_at=started_at,
                completed_at=_utc_iso(self._now()),
                endpoint_url=request.endpoint_url,
                outcome=failure.outcome,
                safe_failure_code=failure.safe_code,
                resolved_url=response.resolved_url,
                http_status=response.http_status,
                media_type=response.media_type,
                byte_size=len(response.body),
                record_count=None,
                duration_milliseconds=response.duration_milliseconds,
                artifact_version_id=artifact["artifact_version_id"],
            )
            validate(attempt, attempt_schema)
            validate_attempt_semantics(attempt)
            self.store.write_attempt(attempt)
            return AcquisitionResult(
                plan_sha256,
                attempt,
                artifact,
                None,
                stored.created,
            )

        report = _build_change_report(
            plan=plan,
            plan_sha256=plan_sha256,
            baseline=baseline,
            candidate_artifact_version_id=artifact["artifact_version_id"],
            candidate_sha256=sha256,
            candidate_records=records,
        )
        attempt = _attempt(
            plan=plan,
            source=source,
            record_origin=record_origin,
            execution_environment=self.execution_environment,
            attempt_id=attempt_id,
            correlation_id=correlation_id,
            started_at=started_at,
            completed_at=_utc_iso(self._now()),
            endpoint_url=request.endpoint_url,
            outcome="candidate_new_version",
            safe_failure_code=None,
            resolved_url=response.resolved_url,
            http_status=response.http_status,
            media_type=response.media_type,
            byte_size=len(response.body),
            record_count=len(records),
            duration_milliseconds=response.duration_milliseconds,
            artifact_version_id=artifact["artifact_version_id"],
        )
        validate(attempt, attempt_schema)
        validate_attempt_semantics(attempt)
        validate(report, report_schema)
        self.store.write_change_report(report)
        self.store.write_attempt(attempt)
        return AcquisitionResult(
            plan_sha256,
            attempt,
            artifact,
            report,
            stored.created,
        )
