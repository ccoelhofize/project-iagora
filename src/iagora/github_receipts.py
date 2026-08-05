# SPDX-License-Identifier: EUPL-1.2

"""Least-privilege GitHub issue adapter for safe acquisition receipts."""

from __future__ import annotations

import json
from typing import Any, Callable
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from .contracts import ContractViolation
from .remote_acquisition import REPOSITORY_PATTERN, plan_issue_updates


API_ROOT = "https://api.github.com"
API_VERSION = "2022-11-28"
MAXIMUM_RESPONSE_BYTES = 2 * 1024 * 1024
MAXIMUM_ISSUE_PAGES = 20


class GitHubAdapterFailure(RuntimeError):
    """Safe GitHub adapter failure without response-body disclosure."""


class GitHubIssueClient:
    """Bounded client that can operate only on issues in one repository."""

    def __init__(
        self,
        repository: str,
        token: str,
        *,
        opener: Callable[..., Any] = urlopen,
    ) -> None:
        if not REPOSITORY_PATTERN.fullmatch(repository):
            raise ContractViolation("GitHub repository identifier is invalid")
        if not token or any(character.isspace() for character in token):
            raise ContractViolation("GitHub workflow token is missing or malformed")
        self.repository = repository
        self._token = token
        self._opener = opener

    def _request(
        self,
        method: str,
        suffix: str,
        payload: dict[str, Any] | None = None,
    ) -> Any:
        if not suffix.startswith("/issues"):
            raise ContractViolation("GitHub adapter path is outside the issue boundary")
        body = None if payload is None else json.dumps(payload).encode("utf-8")
        request = Request(
            f"{API_ROOT}/repos/{self.repository}{suffix}",
            data=body,
            method=method,
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {self._token}",
                "Content-Type": "application/json",
                "User-Agent": "Project-IAgora/0.1 receipt-adapter",
                "X-GitHub-Api-Version": API_VERSION,
            },
        )
        try:
            with self._opener(request, timeout=20) as response:
                content = response.read(MAXIMUM_RESPONSE_BYTES + 1)
        except (HTTPError, URLError, OSError, TimeoutError) as exc:
            raise GitHubAdapterFailure(
                "The GitHub receipt operation could not be completed."
            ) from exc
        if len(content) > MAXIMUM_RESPONSE_BYTES:
            raise GitHubAdapterFailure(
                "The GitHub receipt response exceeded its safe size limit."
            )
        if not content:
            return None
        try:
            return json.loads(content.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise GitHubAdapterFailure(
                "The GitHub receipt response was not valid JSON."
            ) from exc

    def create_issue(self, payload: dict[str, Any]) -> int:
        if set(payload) != {"title", "body"}:
            raise ContractViolation("Receipt issue payload contains unexpected fields")
        if not all(isinstance(payload[field], str) for field in ("title", "body")):
            raise ContractViolation("Receipt issue title and body must be strings")
        response = self._request("POST", "/issues", payload)
        number = response.get("number") if isinstance(response, dict) else None
        if not isinstance(number, int):
            raise GitHubAdapterFailure(
                "GitHub did not return a receipt issue identifier."
            )
        return number

    def update_issue_body(self, issue_number: int, body: str) -> None:
        self._issue_number(issue_number)
        self._request("PATCH", f"/issues/{issue_number}", {"body": body})

    def comment(self, issue_number: int, body: str) -> None:
        self._issue_number(issue_number)
        self._request("POST", f"/issues/{issue_number}/comments", {"body": body})

    def close_issue(self, issue_number: int) -> None:
        self._issue_number(issue_number)
        self._request("PATCH", f"/issues/{issue_number}", {"state": "closed"})

    def list_issues(self) -> list[dict[str, Any]]:
        issues: list[dict[str, Any]] = []
        for page in range(1, MAXIMUM_ISSUE_PAGES + 1):
            response = self._request(
                "GET", f"/issues?state=all&per_page=100&page={page}"
            )
            if not isinstance(response, list):
                raise GitHubAdapterFailure("GitHub returned an invalid issue list.")
            issues.extend(item for item in response if isinstance(item, dict))
            if len(response) < 100:
                return issues
        raise GitHubAdapterFailure("GitHub issue pagination exceeded its safe limit.")

    @staticmethod
    def _issue_number(value: int) -> None:
        if not isinstance(value, int) or value < 1:
            raise ContractViolation("GitHub issue number is invalid")


def create_receipt_issue(
    client: GitHubIssueClient,
    payload: dict[str, Any],
    review_state: str,
) -> int:
    """Create a durable receipt and close terminal non-reviewable states."""

    issue_number = client.create_issue(payload)
    if review_state != "admission_pending":
        client.close_issue(issue_number)
    return issue_number


def apply_receipt_monitor(
    client: GitHubIssueClient,
    now,
) -> list[dict[str, Any]]:
    """Apply deterministic metadata-only reminder and expiry updates."""

    updates = plan_issue_updates(client.list_issues(), client.repository, now)
    for update in updates:
        issue_number = update["issue_number"]
        client.update_issue_body(issue_number, update["body"])
        client.comment(issue_number, update["comment"])
        if update["close_issue"]:
            client.close_issue(issue_number)
    return updates
