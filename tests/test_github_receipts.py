# SPDX-License-Identifier: EUPL-1.2

from __future__ import annotations

import json
import unittest
from datetime import datetime, timezone
from urllib.error import URLError

from iagora.contracts import ContractViolation
from iagora.github_receipts import (
    GitHubAdapterFailure,
    GitHubIssueClient,
    apply_receipt_monitor,
    create_receipt_issue,
)
from iagora.remote_acquisition import render_receipt_issue


NOW = datetime(2026, 8, 15, 9, 0, tzinfo=timezone.utc)


class FakeResponse:
    def __init__(self, payload) -> None:
        self.content = json.dumps(payload).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, _exception_type, _exception, _traceback) -> None:
        return None

    def read(self, maximum: int) -> bytes:
        return self.content[:maximum]


class RecordingOpener:
    def __init__(self, responses) -> None:
        self.responses = iter(responses)
        self.requests = []

    def __call__(self, request, timeout: int):
        self.requests.append((request, timeout))
        response = next(self.responses)
        if isinstance(response, Exception):
            raise response
        return FakeResponse(response)


class RecordingClient:
    repository = "ccoelhofize/project-iagora"

    def __init__(self, issues=None) -> None:
        self.issues = issues or []
        self.calls = []

    def create_issue(self, payload):
        self.calls.append(("create", payload))
        return 42

    def close_issue(self, issue_number):
        self.calls.append(("close", issue_number))

    def list_issues(self):
        self.calls.append(("list",))
        return self.issues

    def update_issue_body(self, issue_number, body):
        self.calls.append(("update", issue_number, body))

    def comment(self, issue_number, body):
        self.calls.append(("comment", issue_number, body))


def pending_receipt() -> dict:
    return {
        "contract_id": "iagora.acquisition-receipt",
        "contract_version": "1.1.0",
        "receipt_id": "receipt-remote-0001",
        "record_origin": "live_execution",
        "attempt_id": "attempt-remote-0001",
        "package_id": "package-remote-0001",
        "workflow_run_id": "30839222985",
        "plan_reference": {
            "plan_id": "plan-city-schools-pilot-cases",
            "plan_version": "0.1.0",
        },
        "source_profile_reference": {
            "source_id": "src-city-schools-pilot-cases",
            "source_profile_version": "0.1.0",
        },
        "attempted_at": "2026-08-05T09:00:00Z",
        "safe_outcome": "candidate_new_version",
        "media_type": "application/json; charset=utf-8",
        "byte_size": 1200,
        "sha256": "a" * 64,
        "policy_states": {
            "validation": "passed",
            "rights": "passed",
            "privacy": "passed",
            "security": "passed",
            "retention": "passed",
        },
        "package_created_at": "2026-08-05T09:00:00Z",
        "reminder_due_at": "2026-08-15T09:00:00Z",
        "reminder_sent_at": None,
        "package_expires_at": "2026-08-19T09:00:00Z",
        "extension_count": 0,
        "review_state": "admission_pending",
        "decision_at": None,
        "decision_rationale": None,
        "admission_review_id": None,
        "pull_request_url": None,
        "bytes_available": True,
        "limitations": [
            "Operational metadata only; human admission remains mandatory."
        ],
    }


class GitHubReceiptAdapterTests(unittest.TestCase):
    def test_terminal_receipt_issue_is_created_then_closed(self) -> None:
        client = RecordingClient()
        issue_number = create_receipt_issue(
            client,
            {"title": "Receipt", "body": "metadata"},
            "no_admission_required",
        )
        self.assertEqual(42, issue_number)
        self.assertEqual(
            [
                ("create", {"title": "Receipt", "body": "metadata"}),
                ("close", 42),
            ],
            client.calls,
        )

    def test_pending_receipt_issue_remains_open(self) -> None:
        client = RecordingClient()
        create_receipt_issue(
            client,
            {"title": "Receipt", "body": "metadata"},
            "admission_pending",
        )
        self.assertEqual(1, len(client.calls))

    def test_monitor_updates_body_and_comments_without_closing_at_day_ten(self) -> None:
        issue = render_receipt_issue(
            pending_receipt(), "ccoelhofize/project-iagora"
        )
        client = RecordingClient([{"number": 42, **issue}])
        updates = apply_receipt_monitor(client, NOW)
        self.assertEqual("remind", updates[0]["action"])
        self.assertEqual(["list", "update", "comment"], [call[0] for call in client.calls])

    def test_monitor_closes_expired_receipt(self) -> None:
        issue = render_receipt_issue(
            pending_receipt(), "ccoelhofize/project-iagora"
        )
        client = RecordingClient([{"number": 42, **issue}])
        updates = apply_receipt_monitor(
            client, datetime(2026, 8, 19, 9, 0, tzinfo=timezone.utc)
        )
        self.assertEqual("expire", updates[0]["action"])
        self.assertEqual(
            ["list", "update", "comment", "close"],
            [call[0] for call in client.calls],
        )

    def test_monitor_fails_visibly_without_mutating_a_tampered_receipt(self) -> None:
        issue = render_receipt_issue(
            pending_receipt(), "ccoelhofize/project-iagora"
        )
        issue["body"] = issue["body"].replace(
            '"contract_version": "1.1.0"',
            '"contract_version": "9.9.9"',
        )
        client = RecordingClient([{"number": 42, **issue}])
        with self.assertRaises(ContractViolation):
            apply_receipt_monitor(client, NOW)
        self.assertEqual([("list",)], client.calls)

    def test_http_client_is_fixed_to_repository_issues_and_safe_headers(self) -> None:
        opener = RecordingOpener([[{"number": 7}]])
        client = GitHubIssueClient(
            "ccoelhofize/project-iagora", "test-token", opener=opener
        )
        issues = client.list_issues()
        self.assertEqual([{"number": 7}], issues)
        request, timeout = opener.requests[0]
        self.assertEqual(20, timeout)
        self.assertTrue(
            request.full_url.startswith(
                "https://api.github.com/repos/ccoelhofize/project-iagora/issues?"
            )
        )
        self.assertEqual("Bearer test-token", request.get_header("Authorization"))

    def test_client_rejects_invalid_repository_and_out_of_scope_path(self) -> None:
        with self.assertRaises(ContractViolation):
            GitHubIssueClient("https://example.invalid/repository", "test-token")
        client = GitHubIssueClient("owner/repository", "test-token")
        with self.assertRaises(ContractViolation):
            client._request("GET", "/actions/runs")

    def test_network_failure_does_not_expose_token_or_response(self) -> None:
        opener = RecordingOpener([URLError("private response detail")])
        client = GitHubIssueClient(
            "owner/repository", "secret-token", opener=opener
        )
        with self.assertRaises(GitHubAdapterFailure) as context:
            client.list_issues()
        message = str(context.exception)
        self.assertNotIn("secret-token", message)
        self.assertNotIn("private response detail", message)


if __name__ == "__main__":
    unittest.main()
