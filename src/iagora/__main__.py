# SPDX-License-Identifier: EUPL-1.2

from __future__ import annotations

import argparse
import base64
import binascii
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from .acquisition_engine import (
    AcquisitionEngine,
    LocalQuarantineStore,
    load_reviewed_plan,
)
from .acquisition_transport import (
    AcquisitionFailure,
    ConstrainedHttpsTransport,
    ReplayTransport,
)
from .contracts import ContractViolation, load_json, validate
from .github_receipts import (
    GitHubAdapterFailure,
    GitHubIssueClient,
    apply_receipt_monitor,
    create_receipt_issue,
)
from .pilot import ROOT, build, build_passport, validate_inputs
from .remote_acquisition import (
    build_remote_package,
    extract_receipt_issue,
    plan_issue_updates,
)
from .acquisition import validate_receipt_semantics


def main() -> int:
    parser = argparse.ArgumentParser(description="Project IAgora bounded POC tools")
    subcommands = parser.add_subparsers(dest="command", required=True)
    subcommands.add_parser("validate", help="Validate contracts and deterministic invariants")
    build_parser = subcommands.add_parser(
        "build", help="Build the local passport and accessible product prototype"
    )
    build_parser.add_argument("--output", type=Path, default=ROOT / "build" / "pilot")
    acquire_parser = subcommands.add_parser(
        "acquire",
        help="Manually run one reviewed acquisition plan through constrained HTTPS",
    )
    acquire_parser.add_argument("--plan", required=True)
    acquire_parser.add_argument("--quarantine-dir", type=Path, required=True)
    replay_parser = subcommands.add_parser(
        "replay",
        help="Replay one local response through the same governed acquisition core",
    )
    replay_parser.add_argument("--plan", required=True)
    replay_parser.add_argument("--input", type=Path, required=True)
    replay_parser.add_argument("--quarantine-dir", type=Path, required=True)
    replay_parser.add_argument(
        "--media-type",
        default="application/json; charset=utf-8",
    )
    remote_parser = subcommands.add_parser(
        "remote-acquire",
        help="Run one reviewed plan and build a temporary GitHub review package",
    )
    remote_parser.add_argument(
        "--plan",
        required=True,
        choices=("plan-city-schools-pilot-cases",),
    )
    remote_parser.add_argument("--quarantine-dir", type=Path, required=True)
    remote_parser.add_argument("--package-dir", type=Path, required=True)
    remote_parser.add_argument("--adapter-output", type=Path, required=True)
    monitor_parser = subcommands.add_parser(
        "plan-receipt-updates",
        help="Plan metadata-only GitHub receipt reminder and expiry updates",
    )
    monitor_parser.add_argument("--input", type=Path, required=True)
    monitor_parser.add_argument("--output", type=Path, required=True)
    monitor_parser.add_argument("--repository", required=True)
    monitor_parser.add_argument("--now")
    issue_parser = subcommands.add_parser(
        "create-receipt-issue",
        help="Create one validated metadata-only GitHub receipt issue",
    )
    issue_parser.add_argument("--payload-base64", required=True)
    issue_parser.add_argument("--repository", required=True)
    remote_monitor_parser = subcommands.add_parser(
        "monitor-receipt-issues",
        help="Apply metadata-only receipt reminders and expiry transitions",
    )
    remote_monitor_parser.add_argument("--repository", required=True)
    remote_monitor_parser.add_argument("--now")
    args = parser.parse_args()

    if args.command == "validate":
        validate_inputs()
        build_passport()
        print(
            "Validated acquisition contracts, bounded plan, compatibility fixtures, source "
            "profiles, campaign artifact metadata, canonical assertions, "
            "commitment mapping, review packet, pilot snapshot, administrative evidence, procurement "
            "evidence, bounded raw artifacts, open-data subset, and Knowledge Passport."
        )
        return 0

    if args.command == "build":
        passport_path, dashboard_path = build(args.output)
        print(f"Built {passport_path}")
        print(f"Built {dashboard_path}")
        print(f"Built {args.output / 'education' / 'index.html'}")
        print(f"Built {args.output / 'programmes' / 'respire-a-la-recre' / 'index.html'}")
        return 0

    if args.command == "plan-receipt-updates":
        try:
            issues = json.loads(args.input.read_text(encoding="utf-8"))
            if not isinstance(issues, list):
                raise ContractViolation("GitHub issue input must be a JSON array")
            now = (
                datetime.fromisoformat(args.now.replace("Z", "+00:00"))
                if args.now
                else datetime.now(timezone.utc)
            )
            updates = plan_issue_updates(issues, args.repository, now)
            args.output.write_text(
                json.dumps(updates, ensure_ascii=False, indent=2, sort_keys=True)
                + "\n",
                encoding="utf-8",
            )
        except (ContractViolation, OSError, ValueError, json.JSONDecodeError) as exc:
            print(
                json.dumps(
                    {
                        "outcome": "failed",
                        "safe_failure_code": "receipt_monitor_invalid",
                        "message": str(exc),
                    },
                    ensure_ascii=False,
                    sort_keys=True,
                ),
                file=sys.stderr,
            )
            return 2
        print(json.dumps({"updates_planned": len(updates)}, sort_keys=True))
        return 0

    if args.command in {"create-receipt-issue", "monitor-receipt-issues"}:
        try:
            if os.environ.get("GITHUB_ACTIONS") != "true":
                raise ContractViolation(
                    "GitHub receipt writes are restricted to GitHub Actions"
                )
            if args.repository != os.environ.get("GITHUB_REPOSITORY"):
                raise ContractViolation(
                    "Receipt repository differs from the GitHub Actions context"
                )
            token = os.environ.get("GITHUB_TOKEN")
            if not token:
                raise ContractViolation("GitHub receipt token is unavailable")
            client = GitHubIssueClient(args.repository, token)
            if args.command == "create-receipt-issue":
                decoded = base64.b64decode(args.payload_base64, validate=True)
                payload = json.loads(decoded.decode("utf-8"))
                if not isinstance(payload, dict):
                    raise ContractViolation("Receipt issue payload must be an object")
                receipt = extract_receipt_issue(payload.get("body", ""))
                receipt_schema = load_json(
                    ROOT / "contracts/v1/acquisition-receipt.schema.json"
                )
                validate(receipt, receipt_schema)
                validate_receipt_semantics(receipt)
                issue_number = create_receipt_issue(
                    client, payload, receipt["review_state"]
                )
                output = {"issue_number": issue_number, "created": True}
            else:
                now = (
                    datetime.fromisoformat(args.now.replace("Z", "+00:00"))
                    if args.now
                    else datetime.now(timezone.utc)
                )
                updates = apply_receipt_monitor(client, now)
                output = {"updates_applied": len(updates)}
        except (
            ContractViolation,
            GitHubAdapterFailure,
            UnicodeDecodeError,
            json.JSONDecodeError,
            binascii.Error,
            ValueError,
        ) as exc:
            print(
                json.dumps(
                    {
                        "outcome": "failed",
                        "safe_failure_code": "github_receipt_failure",
                        "message": str(exc),
                    },
                    ensure_ascii=False,
                    sort_keys=True,
                ),
                file=sys.stderr,
            )
            return 2
        print(json.dumps(output, sort_keys=True))
        return 0

    try:
        store = LocalQuarantineStore(args.quarantine_dir, ROOT)
        execution_environment = (
            "github_actions" if args.command == "remote-acquire" else "local"
        )
        engine = AcquisitionEngine(
            ROOT,
            store,
            execution_environment=execution_environment,
        )
        if args.command == "acquire":
            transport = ConstrainedHttpsTransport()
        elif args.command == "replay":
            plan, _source = load_reviewed_plan(ROOT, args.plan)
            maximum = plan["transport_policy"]["maximum_response_bytes"]
            with args.input.open("rb") as handle:
                body = handle.read(maximum + 1)
            transport = ReplayTransport(body, media_type=args.media_type)
        else:
            if os.environ.get("GITHUB_ACTIONS") != "true":
                raise ContractViolation(
                    "Remote acquisition packaging is restricted to GitHub Actions"
                )
            workflow_run_id = os.environ.get("GITHUB_RUN_ID")
            repository = os.environ.get("GITHUB_REPOSITORY")
            if not workflow_run_id or not repository:
                raise ContractViolation(
                    "GitHub Actions run and repository identifiers are required"
                )
            transport = ConstrainedHttpsTransport()
        result = engine.run(args.plan, transport)
        if args.command == "remote-acquire":
            package = build_remote_package(
                root=ROOT,
                quarantine=store,
                package_directory=args.package_dir,
                result=result,
                workflow_run_id=workflow_run_id,
                repository=repository,
                now=datetime.now(timezone.utc),
            )
            adapter_output = {
                "package_id": package.manifest["package_id"],
                "receipt_payload_base64": package.issue_payload_base64,
                "review_state": package.receipt["review_state"],
                "outcome": package.safe_summary["outcome"],
            }
            args.adapter_output.write_text(
                json.dumps(adapter_output, ensure_ascii=False, sort_keys=True) + "\n",
                encoding="utf-8",
            )
    except (AcquisitionFailure, ContractViolation, OSError) as exc:
        if isinstance(exc, AcquisitionFailure):
            safe_code = exc.safe_code
            safe_message = exc.safe_message
        elif isinstance(exc, ContractViolation):
            safe_code = "contract_invalid"
            safe_message = str(exc)
        else:
            safe_code = "local_io_error"
            safe_message = "The local acquisition operation could not access its configured file."
        print(
            json.dumps(
                {"outcome": "failed", "safe_failure_code": safe_code, "message": safe_message},
                ensure_ascii=False,
                sort_keys=True,
            ),
            file=sys.stderr,
        )
        return 2
    print(json.dumps(result.safe_summary(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
