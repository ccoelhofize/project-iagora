# SPDX-License-Identifier: EUPL-1.2

from __future__ import annotations

import json
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from iagora.acquisition_engine import AcquisitionEngine, LocalQuarantineStore
from iagora.acquisition_transport import FetchResponse
from iagora.admission import (
    prepare_admission_proposal,
    receipt_resolution,
    validate_proposal_directory,
)
from iagora.contracts import ContractViolation
from iagora.github_admission import apply_admission_proposal
from iagora.pilot import ROOT
from iagora.remote_acquisition import build_remote_package, render_receipt_issue


PLAN_ID = "plan-city-schools-pilot-cases"
REPOSITORY = "ccoelhofize/project-iagora"
NOW = datetime(2026, 8, 5, 9, 0, tzinfo=timezone.utc)
MAIN_SHA = "1" * 40
TREE_SHA = "2" * 40


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


class RecordingIssueClient:
    repository = REPOSITORY

    def __init__(self, issue: dict) -> None:
        self.issue = issue
        self.calls: list[tuple] = []

    def get_issue(self, number: int) -> dict:
        self.calls.append(("get", number))
        return self.issue

    def update_issue_body(self, number: int, body: str) -> None:
        self.calls.append(("update", number, body))

    def comment(self, number: int, body: str) -> None:
        self.calls.append(("comment", number, body))

    def close_issue(self, number: int) -> None:
        self.calls.append(("close", number))


class RecordingAdmissionClient:
    repository = REPOSITORY

    def __init__(self) -> None:
        self.calls: list[tuple] = []
        self._counter = 3

    def _sha(self) -> str:
        value = format(self._counter, "x") * 40
        self._counter += 1
        return value[:40]

    def main_commit(self):
        self.calls.append(("main",))
        return MAIN_SHA, TREE_SHA

    def create_blob(self, content: bytes):
        self.calls.append(("blob", content))
        return self._sha()

    def create_tree(self, base: str, entries: list[dict]):
        self.calls.append(("tree", base, entries))
        return self._sha()

    def create_commit(self, message: str, tree: str, parent: str):
        self.calls.append(("commit", message, tree, parent))
        return self._sha()

    def create_branch(self, branch: str, commit: str):
        self.calls.append(("branch", branch, commit))

    def create_pull_request(self, branch: str, title: str, body: str):
        self.calls.append(("pr", branch, title, body))
        return f"https://github.com/{REPOSITORY}/pull/99"

    def update_branch(self, branch: str, commit: str):
        self.calls.append(("update_branch", branch, commit))


class AdmissionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        baseline = json.loads(
            (
                ROOT
                / "data/raw/respire-a-la-recre/2026-07-29/records-selected.json"
            ).read_text(encoding="utf-8")
        )
        baseline["results"][0]["nb_arbres_plantes"] = (
            baseline["results"][0]["nb_arbres_plantes"] or 0
        ) + 1
        cls.changed_body = json.dumps(baseline, ensure_ascii=False).encode("utf-8")

    @staticmethod
    def _build_package(outer: Path):
        identifiers = iter(("attempt-admission-0001", "correlation-admission-0001"))
        store = LocalQuarantineStore(outer / "quarantine", ROOT)
        engine = AcquisitionEngine(
            ROOT,
            store,
            now=lambda: NOW,
            identifier=lambda _prefix: next(identifiers),
            execution_environment="github_actions",
        )
        result = engine.run(PLAN_ID, LiveFixtureTransport(AdmissionTests.changed_body))
        return build_remote_package(
            root=ROOT,
            quarantine=store,
            package_directory=outer / "package",
            result=result,
            workflow_run_id="31009987688",
            repository=REPOSITORY,
            now=NOW,
        )

    @staticmethod
    def _issue(package) -> dict:
        return {
            "number": 42,
            "state": "open",
            **render_receipt_issue(package.receipt, REPOSITORY),
        }

    def _prepare(self, outer: Path, decision: str = "admit"):
        package = self._build_package(outer)
        issue = self._issue(package)
        proposal = prepare_admission_proposal(
            root=ROOT,
            package_directory=package.package_directory,
            proposal_directory=outer / "proposal",
            issue=issue,
            repository=REPOSITORY,
            decision=decision,
            rationale="Reviewed exact package and bounded evidence scope.",
            now=NOW + timedelta(hours=1),
        )
        return package, issue, proposal

    def test_admit_proposal_preserves_exact_candidate_and_three_targets(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            outer = Path(temporary)
            package, _issue, prepared = self._prepare(outer)
            proposal = validate_proposal_directory(ROOT, prepared.directory)
            self.assertEqual("admit", proposal["decision"])
            self.assertEqual(3, len(proposal["target_files"]))
            self.assertFalse(proposal["publication_authorized"])
            self.assertFalse(proposal["automatic_merge_allowed"])
            raw = next(
                target
                for target in proposal["target_files"]
                if target["content_role"] == "candidate_raw_bytes"
            )
            self.assertEqual(
                self.changed_body,
                (prepared.directory / "files" / raw["path"]).read_bytes(),
            )
            self.assertEqual(package.receipt["sha256"], raw["sha256"])

    def test_reject_proposal_contains_no_repository_targets(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            _package, _issue, prepared = self._prepare(Path(temporary), "reject")
            self.assertEqual([], prepared.manifest["target_files"])
            self.assertEqual(
                {"proposal.json"},
                {
                    path.relative_to(prepared.directory).as_posix()
                    for path in prepared.directory.rglob("*")
                    if path.is_file()
                },
            )

    def test_resolution_rejects_expired_or_unchanged_receipts(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            package = self._build_package(Path(temporary))
            issue = self._issue(package)
            with self.assertRaisesRegex(ContractViolation, "expired"):
                receipt_resolution(issue, REPOSITORY, NOW + timedelta(days=14))
            issue["body"] = issue["body"].replace(
                '"safe_outcome": "candidate_new_version"',
                '"safe_outcome": "unchanged"',
            ).replace(
                '"review_state": "admission_pending"',
                '"review_state": "no_admission_required"',
            )
            with self.assertRaises(ContractViolation):
                receipt_resolution(issue, REPOSITORY, NOW + timedelta(hours=1))

    def test_prepare_rejects_tampered_package_component(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            outer = Path(temporary)
            package = self._build_package(outer)
            candidate = next(
                component
                for component in package.manifest["component_files"]
                if component["content_role"] == "candidate_raw_bytes"
            )
            (package.package_directory / candidate["path"]).write_bytes(b"{}")
            with self.assertRaisesRegex(ContractViolation, "fingerprint"):
                prepare_admission_proposal(
                    root=ROOT,
                    package_directory=package.package_directory,
                    proposal_directory=outer / "proposal",
                    issue=self._issue(package),
                    repository=REPOSITORY,
                    decision="admit",
                    rationale="Reviewed exact package and bounded evidence scope.",
                    now=NOW + timedelta(hours=1),
                )

    def test_apply_admit_creates_only_branch_draft_pr_review_and_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            outer = Path(temporary)
            _package, issue, prepared = self._prepare(outer)
            issue_client = RecordingIssueClient(issue)
            admission_client = RecordingAdmissionClient()
            result = apply_admission_proposal(
                root=ROOT,
                proposal_directory=prepared.directory,
                issue_client=issue_client,
                admission_client=admission_client,
                expected_main_sha=MAIN_SHA,
                now=NOW + timedelta(hours=2),
            )
            call_names = [call[0] for call in admission_client.calls]
            self.assertEqual("admitted", result["review_state"])
            self.assertEqual(1, call_names.count("branch"))
            self.assertEqual(1, call_names.count("pr"))
            self.assertEqual(1, call_names.count("update_branch"))
            self.assertNotIn("merge", call_names)
            self.assertEqual(["get", "update", "comment", "close"], [c[0] for c in issue_client.calls])
            review_blob = json.loads(
                [call[1] for call in admission_client.calls if call[0] == "blob"][-1]
            )
            self.assertEqual("iagora.admission-review", review_blob["contract_id"])
            self.assertFalse(review_blob["publication_authorized"])

    def test_apply_reject_writes_only_the_receipt_decision(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            outer = Path(temporary)
            _package, issue, prepared = self._prepare(outer, "reject")
            issue_client = RecordingIssueClient(issue)
            admission_client = RecordingAdmissionClient()
            result = apply_admission_proposal(
                root=ROOT,
                proposal_directory=prepared.directory,
                issue_client=issue_client,
                admission_client=admission_client,
                expected_main_sha=MAIN_SHA,
                now=NOW + timedelta(hours=2),
            )
            self.assertEqual("rejected", result["review_state"])
            self.assertEqual([], admission_client.calls)
            self.assertEqual(["get", "update", "comment", "close"], [c[0] for c in issue_client.calls])

    def test_changed_receipt_blocks_all_repository_writes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            outer = Path(temporary)
            _package, issue, prepared = self._prepare(outer)
            issue["body"] = issue["body"].replace(
                '"reminder_sent_at": null',
                '"reminder_sent_at": "2026-08-05T10:30:00Z"',
            )
            issue_client = RecordingIssueClient(issue)
            admission_client = RecordingAdmissionClient()
            with self.assertRaisesRegex(ContractViolation, "changed"):
                apply_admission_proposal(
                    root=ROOT,
                    proposal_directory=prepared.directory,
                    issue_client=issue_client,
                    admission_client=admission_client,
                    expected_main_sha=MAIN_SHA,
                    now=NOW + timedelta(hours=2),
                )
            self.assertEqual([], admission_client.calls)
            self.assertEqual([("get", 42)], issue_client.calls)

    def test_expiry_during_human_wait_blocks_all_writes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            outer = Path(temporary)
            _package, issue, prepared = self._prepare(outer)
            issue_client = RecordingIssueClient(issue)
            admission_client = RecordingAdmissionClient()
            with self.assertRaisesRegex(ContractViolation, "expired"):
                apply_admission_proposal(
                    root=ROOT,
                    proposal_directory=prepared.directory,
                    issue_client=issue_client,
                    admission_client=admission_client,
                    expected_main_sha=MAIN_SHA,
                    now=NOW + timedelta(days=14),
                )
            self.assertEqual([], admission_client.calls)
            self.assertEqual([("get", 42)], issue_client.calls)

    def test_main_change_blocks_candidate_blob_creation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            outer = Path(temporary)
            _package, issue, prepared = self._prepare(outer)
            issue_client = RecordingIssueClient(issue)
            admission_client = RecordingAdmissionClient()
            with self.assertRaisesRegex(ContractViolation, "main commit changed"):
                apply_admission_proposal(
                    root=ROOT,
                    proposal_directory=prepared.directory,
                    issue_client=issue_client,
                    admission_client=admission_client,
                    expected_main_sha="9" * 40,
                    now=NOW + timedelta(hours=2),
                )
            self.assertEqual([("main",)], admission_client.calls)
            self.assertEqual([("get", 42)], issue_client.calls)

    def test_workflow_separates_read_only_validation_and_protected_writes(self) -> None:
        workflow = (ROOT / ".github/workflows/governed-admission.yml").read_text(
            encoding="utf-8"
        )
        validation, apply = workflow.split("  apply:\n", 1)
        self.assertIn("environment: governed-admission", apply)
        self.assertIn("IAGORA_ADMISSION_ENVIRONMENT_READY", workflow)
        self.assertIn("actions: read", validation)
        self.assertIn("issues: read", validation)
        self.assertNotIn("contents: write", validation)
        self.assertNotIn("issues: write", validation)
        self.assertIn("contents: write", apply)
        self.assertIn("issues: write", apply)
        self.assertIn("pull-requests: write", apply)
        self.assertIn("persist-credentials: false", workflow)
        self.assertIn(
            "actions/download-artifact@3e5f45b2cfb9172054b4087a40e8e0b5a5461e7c",
            workflow,
        )
        self.assertNotIn("remote-acquire", workflow)
        self.assertNotIn("opendata.clermont-ferrand.fr", workflow)
        self.assertNotIn("merge", apply.lower())


if __name__ == "__main__":
    unittest.main()
