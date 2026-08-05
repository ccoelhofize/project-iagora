# SPDX-License-Identifier: EUPL-1.2

"""Protected GitHub write adapter for one reviewed admission proposal."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .admission import (
    build_admission_review,
    decided_receipt,
    rendered_decided_issue,
    receipt_resolution,
    validate_proposal_directory,
)
from .acquisition_transport import canonical_json_sha256
from .contracts import ContractViolation
from .github_receipts import GitHubAdmissionClient, GitHubIssueClient


def _json_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")


def apply_admission_proposal(
    *,
    root: Path,
    proposal_directory: Path,
    issue_client: GitHubIssueClient,
    admission_client: GitHubAdmissionClient,
    expected_main_sha: str,
    now: datetime,
) -> dict[str, Any]:
    """Apply one already protected decision without touching ``main``."""

    proposal = validate_proposal_directory(root, proposal_directory)
    if issue_client.repository != proposal["repository"]:
        raise ContractViolation("Admission proposal and issue repository disagree")
    if admission_client.repository != proposal["repository"]:
        raise ContractViolation("Admission proposal and write repository disagree")
    issue = issue_client.get_issue(proposal["receipt_issue_number"])
    receipt = receipt_resolution(issue, proposal["repository"], now)["receipt"]
    if canonical_json_sha256(receipt) != proposal["receipt_sha256"]:
        raise ContractViolation("Receipt changed after admission preparation")

    pull_request_url = None
    branch = None
    decided_at = now.astimezone(timezone.utc)
    if proposal["decision"] == "admit":
        for target in proposal["target_files"]:
            if (root / target["path"]).exists():
                raise ContractViolation("Admission target already exists on checked-out main")
        main_sha, main_tree_sha = admission_client.main_commit()
        if main_sha != expected_main_sha:
            raise ContractViolation("Protected admission main commit changed after checkout")
        target_entries = []
        for target in proposal["target_files"]:
            content = (proposal_directory / "files" / target["path"]).read_bytes()
            target_entries.append(
                {"path": target["path"], "sha": admission_client.create_blob(content)}
            )
        target_tree_sha = admission_client.create_tree(main_tree_sha, target_entries)
        target_commit_sha = admission_client.create_commit(
            f"Admit {proposal['artifact_version_id']}",
            target_tree_sha,
            main_sha,
        )
        suffix = proposal["attempt_id"].removeprefix("attempt-")
        branch = f"admission/{suffix}"
        admission_client.create_branch(branch, target_commit_sha)
        pull_request_url = admission_client.create_pull_request(
            branch,
            f"Admit reviewed acquisition {proposal['artifact_version_id']}",
            "\n".join(
                (
                    "## Governed evidence admission",
                    "",
                    f"- Receipt issue: #{proposal['receipt_issue_number']}",
                    f"- Package: `{proposal['package_reference']['package_id']}`",
                    f"- Artifact: `{proposal['artifact_version_id']}`",
                    f"- Decision rationale: {proposal['rationale']}",
                    "",
                    "This pull request preserves reviewed evidence and lineage. It does not authorize publication, merge, canonical interpretation, campaign fulfillment, outcome, or impact conclusions.",
                )
            ),
        )
        review = build_admission_review(proposal, decided_at, pull_request_url)
        review_date = decided_at.date().isoformat()
        review_path = (
            f"data/acquisition/admissions/{review_date}/"
            f"{proposal['admission_review_id']}.json"
        )
        review_blob_sha = admission_client.create_blob(_json_bytes(review))
        review_tree_sha = admission_client.create_tree(
            target_tree_sha, [{"path": review_path, "sha": review_blob_sha}]
        )
        review_commit_sha = admission_client.create_commit(
            f"Record {proposal['admission_review_id']}",
            review_tree_sha,
            target_commit_sha,
        )
        admission_client.update_branch(branch, review_commit_sha)
        comment = (
            f"Maintainer admission recorded in {pull_request_url}. The pull request remains draft and unmerged; publication is not authorized."
        )
    else:
        review = build_admission_review(proposal, decided_at, None)
        comment = "\n".join(
            (
                "Maintainer rejection recorded. No branch, pull request, admission target, canonical change, or publication was created.",
                "",
                "```json",
                json.dumps(review, ensure_ascii=False, indent=2, sort_keys=True),
                "```",
            )
        )

    updated_receipt = decided_receipt(
        receipt, proposal, decided_at, pull_request_url
    )
    rendered = rendered_decided_issue(updated_receipt, proposal["repository"])
    issue_client.update_issue_body(proposal["receipt_issue_number"], rendered["body"])
    issue_client.comment(proposal["receipt_issue_number"], comment)
    issue_client.close_issue(proposal["receipt_issue_number"])
    return {
        "decision": proposal["decision"],
        "branch": branch,
        "pull_request_url": pull_request_url,
        "receipt_issue_number": proposal["receipt_issue_number"],
        "review_state": updated_receipt["review_state"],
        "publication_authorized": False,
        "automatic_merge_allowed": False,
    }
