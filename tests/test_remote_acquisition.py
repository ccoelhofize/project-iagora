# SPDX-License-Identifier: EUPL-1.2

from __future__ import annotations

import base64
import hashlib
import io
import json
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch

from iagora.__main__ import main
from iagora.acquisition_engine import AcquisitionEngine, LocalQuarantineStore
from iagora.acquisition_transport import FetchResponse, ReplayTransport
from iagora.contracts import ContractViolation, load_json, validate
from iagora.pilot import ROOT
from iagora.remote_acquisition import (
    build_remote_package,
    extract_receipt_issue,
    plan_issue_updates,
    render_receipt_issue,
    transition_receipt,
    validate_remote_package_semantics,
)


PLAN_ID = "plan-city-schools-pilot-cases"
NOW = datetime(2026, 8, 5, 9, 0, tzinfo=timezone.utc)


class LiveFixtureTransport:
    record_origin = "live_execution"

    def __init__(self, body: bytes) -> None:
        self.body = body

    def fetch(self, request):
        return FetchResponse(
            requested_url=request.request_url,
            resolved_url=request.request_url,
            http_status=200,
            media_type="application/json; charset=utf-8",
            body=self.body,
            duration_milliseconds=12,
            redirect_count=0,
        )


class RemoteAcquisitionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.baseline_path = (
            ROOT / "data/raw/respire-a-la-recre/2026-07-29/records-selected.json"
        )
        cls.baseline_body = cls.baseline_path.read_bytes()
        cls.receipt_schema = load_json(
            ROOT / "contracts/v1/acquisition-receipt.schema.json"
        )
        cls.package_schema = load_json(
            ROOT / "contracts/v1/remote-acquisition-package.schema.json"
        )

    @staticmethod
    def _engine(store: LocalQuarantineStore) -> AcquisitionEngine:
        identifiers = iter(("attempt-remote-0001", "correlation-remote-0001"))
        return AcquisitionEngine(
            ROOT,
            store,
            now=lambda: NOW,
            identifier=lambda _prefix: next(identifiers),
            execution_environment="github_actions",
        )

    def _build(self, body: bytes, temporary: str):
        outer = Path(temporary)
        store = LocalQuarantineStore(outer / "quarantine", ROOT)
        result = self._engine(store).run(PLAN_ID, LiveFixtureTransport(body))
        package = build_remote_package(
            root=ROOT,
            quarantine=store,
            package_directory=outer / "package",
            result=result,
            workflow_run_id="30839222985",
            repository="ccoelhofize/project-iagora",
            now=NOW,
        )
        return result, package

    def test_unchanged_remote_result_reuses_governed_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            result, package = self._build(self.baseline_body, temporary)
            self.assertEqual("github_actions", result.attempt["execution_environment"])
            self.assertEqual("unchanged", result.attempt["outcome"])
            self.assertEqual("no_admission_required", package.receipt["review_state"])
            self.assertTrue(package.receipt["bytes_available"])
            self.assertFalse(package.manifest["raw_bytes_included"])
            self.assertFalse((package.package_directory / "candidate").exists())
            validate(package.receipt, self.receipt_schema)
            validate(package.manifest, self.package_schema)

    def test_local_and_github_fixture_execution_are_equivalent(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            outer = Path(temporary)
            local_store = LocalQuarantineStore(outer / "local", ROOT)
            remote_store = LocalQuarantineStore(outer / "remote", ROOT)

            def engine(store, environment):
                identifiers = iter(
                    ("attempt-equivalence-0001", "correlation-equivalence-0001")
                )
                return AcquisitionEngine(
                    ROOT,
                    store,
                    now=lambda: NOW,
                    identifier=lambda _prefix: next(identifiers),
                    execution_environment=environment,
                )

            local = engine(local_store, "local").run(
                PLAN_ID, ReplayTransport(self.baseline_body)
            )
            remote = engine(remote_store, "github_actions").run(
                PLAN_ID, ReplayTransport(self.baseline_body)
            )
            self.assertEqual(local.plan_sha256, remote.plan_sha256)
            self.assertEqual(local.attempt["outcome"], remote.attempt["outcome"])
            self.assertEqual(local.attempt["response"], remote.attempt["response"])
            self.assertEqual(local.attempt["artifact_version_id"], remote.attempt["artifact_version_id"])
            self.assertEqual(local.change_report, remote.change_report)
            self.assertEqual("local", local.attempt["execution_environment"])
            self.assertEqual("github_actions", remote.attempt["execution_environment"])

    def test_changed_remote_result_builds_reviewable_bounded_package(self) -> None:
        payload = json.loads(self.baseline_body)
        payload["results"][0]["nb_arbres_plantes"] = (
            payload["results"][0]["nb_arbres_plantes"] or 0
        ) + 1
        changed_body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        with tempfile.TemporaryDirectory() as temporary:
            _result, package = self._build(changed_body, temporary)
            receipt = package.receipt
            self.assertEqual("admission_pending", receipt["review_state"])
            self.assertEqual(_iso(NOW + timedelta(days=10)), receipt["reminder_due_at"])
            self.assertEqual(_iso(NOW + timedelta(days=14)), receipt["package_expires_at"])
            self.assertTrue(receipt["bytes_available"])
            self.assertTrue(package.manifest["raw_bytes_included"])
            raw_components = [
                item
                for item in package.manifest["component_files"]
                if item["content_role"] == "candidate_raw_bytes"
            ]
            self.assertEqual(1, len(raw_components))
            raw_path = package.package_directory / raw_components[0]["path"]
            self.assertEqual(changed_body, raw_path.read_bytes())
            for component in package.manifest["component_files"]:
                content = (package.package_directory / component["path"]).read_bytes()
                self.assertEqual(component["byte_size"], len(content))
                self.assertEqual(
                    component["sha256"],
                    hashlib.sha256(content).hexdigest(),
                )

            issue_payload = json.loads(
                base64.b64decode(package.issue_payload_base64).decode("utf-8")
            )
            self.assertEqual(receipt, extract_receipt_issue(issue_payload["body"]))
            serialized = json.dumps(
                {
                    "manifest": package.manifest,
                    "receipt": receipt,
                    "issue": issue_payload,
                }
            )
            self.assertNotIn(temporary, serialized)
            self.assertNotIn("select=", serialized)
            self.assertNotIn("results", serialized)

    def test_invalid_response_exports_metadata_without_raw_bytes(self) -> None:
        payload = json.loads(self.baseline_body)
        payload["results"][-1]["uai"] = payload["results"][0]["uai"]
        invalid_body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        with tempfile.TemporaryDirectory() as temporary:
            result, package = self._build(invalid_body, temporary)
            self.assertEqual("quarantined_validation_failure", result.attempt["outcome"])
            self.assertEqual("not_reviewable", package.receipt["review_state"])
            self.assertFalse(package.receipt["bytes_available"])
            self.assertFalse(package.manifest["raw_bytes_included"])
            roles = {
                item["content_role"] for item in package.manifest["component_files"]
            }
            self.assertNotIn("candidate_raw_bytes", roles)

    def test_package_semantics_reject_contradictory_raw_byte_claims(self) -> None:
        payload = json.loads(self.baseline_body)
        payload["results"][0]["nb_arbres_plantes"] = (
            payload["results"][0]["nb_arbres_plantes"] or 0
        ) + 1
        changed_body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        with tempfile.TemporaryDirectory() as temporary:
            _result, package = self._build(changed_body, temporary)
            contradictory = dict(package.manifest)
            contradictory["raw_bytes_included"] = False
            with self.assertRaisesRegex(
                ContractViolation, "raw-byte eligibility is inconsistent"
            ):
                validate_remote_package_semantics(contradictory)

    def test_receipt_is_reminded_once_then_expires_fail_closed(self) -> None:
        payload = json.loads(self.baseline_body)
        payload["results"][0]["nb_arbres_plantes"] = (
            payload["results"][0]["nb_arbres_plantes"] or 0
        ) + 1
        changed_body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        with tempfile.TemporaryDirectory() as temporary:
            _result, package = self._build(changed_body, temporary)
            receipt = package.receipt
            action, untouched = transition_receipt(receipt, NOW + timedelta(days=9))
            self.assertEqual("none", action)
            self.assertEqual(receipt, untouched)

            action, reminded = transition_receipt(receipt, NOW + timedelta(days=10))
            self.assertEqual("remind", action)
            self.assertIsNotNone(reminded["reminder_sent_at"])
            self.assertEqual(
                "none",
                transition_receipt(reminded, NOW + timedelta(days=11))[0],
            )

            action, expired = transition_receipt(reminded, NOW + timedelta(days=14))
            self.assertEqual("expire", action)
            self.assertEqual("expired_without_admission", expired["review_state"])
            self.assertFalse(expired["bytes_available"])
            self.assertIsNotNone(expired["decision_at"])
            validate(expired, self.receipt_schema)

            issue = render_receipt_issue(receipt, "ccoelhofize/project-iagora")
            updates = plan_issue_updates(
                [{"number": 42, **issue}],
                "ccoelhofize/project-iagora",
                NOW + timedelta(days=10),
            )
            self.assertEqual(1, len(updates))
            self.assertEqual("remind", updates[0]["action"])
            updated_receipt = extract_receipt_issue(updates[0]["body"])
            self.assertIsNotNone(updated_receipt["reminder_sent_at"])

    def test_remote_cli_refuses_non_actions_execution(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            arguments = [
                "iagora",
                "remote-acquire",
                "--plan",
                PLAN_ID,
                "--quarantine-dir",
                str(Path(temporary) / "quarantine"),
                "--package-dir",
                str(Path(temporary) / "package"),
                "--adapter-output",
                str(Path(temporary) / "adapter.json"),
            ]
            error = io.StringIO()
            environment = dict(os.environ)
            environment.pop("GITHUB_ACTIONS", None)
            with (
                patch.object(sys, "argv", arguments),
                patch.dict(os.environ, environment, clear=True),
                redirect_stderr(error),
            ):
                self.assertEqual(2, main())
            failure = json.loads(error.getvalue())
            self.assertEqual("contract_invalid", failure["safe_failure_code"])

    def test_remote_cli_builds_package_from_actions_context(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            outer = Path(temporary)
            adapter = outer / "adapter.json"
            arguments = [
                "iagora",
                "remote-acquire",
                "--plan",
                PLAN_ID,
                "--quarantine-dir",
                str(outer / "quarantine"),
                "--package-dir",
                str(outer / "package"),
                "--adapter-output",
                str(adapter),
            ]
            output = io.StringIO()
            environment = {
                "GITHUB_ACTIONS": "true",
                "GITHUB_RUN_ID": "30839222985",
                "GITHUB_REPOSITORY": "ccoelhofize/project-iagora",
            }
            with (
                patch.object(sys, "argv", arguments),
                patch.dict(os.environ, environment, clear=False),
                patch(
                    "iagora.__main__.ConstrainedHttpsTransport",
                    return_value=LiveFixtureTransport(self.baseline_body),
                ),
                redirect_stdout(output),
            ):
                self.assertEqual(0, main())
            self.assertEqual("unchanged", json.loads(output.getvalue())["outcome"])
            adapter_data = json.loads(adapter.read_text(encoding="utf-8"))
            self.assertEqual("no_admission_required", adapter_data["review_state"])
            self.assertTrue((outer / "package/manifest.json").is_file())

    def test_workflows_enforce_the_validated_boundary(self) -> None:
        acquisition = (
            ROOT / ".github/workflows/governed-acquisition.yml"
        ).read_text(encoding="utf-8")
        monitor = (
            ROOT / ".github/workflows/acquisition-receipt-monitor.yml"
        ).read_text(encoding="utf-8")
        acquire_job, receipt_job = acquisition.split("  receipt:\n", 1)
        self.assertIn("workflow_dispatch:", acquisition)
        self.assertIn("type: choice", acquisition)
        self.assertIn(PLAN_ID, acquisition)
        self.assertNotIn("url:", acquisition.lower())
        self.assertIn("contents: read", acquire_job)
        self.assertNotIn("issues: write", acquire_job)
        self.assertIn("issues: write", receipt_job)
        self.assertNotIn("contents: write", acquisition)
        self.assertNotIn("pull-requests: write", acquisition)
        self.assertNotIn("git push", acquisition)
        self.assertIn("persist-credentials: false", acquisition)
        self.assertIn("retention-days: 14", acquisition)
        self.assertIn(
            "actions/upload-artifact@043fb46d1a93c77aae656e7c1c64a875d1fc6a0a",
            acquisition,
        )
        self.assertIn("schedule:", monitor)
        self.assertIn("issues: write", monitor)
        self.assertNotIn("remote-acquire", monitor)
        self.assertNotIn("opendata.clermont-ferrand.fr", monitor)


def _iso(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":
    unittest.main()
