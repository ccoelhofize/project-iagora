# SPDX-License-Identifier: EUPL-1.2

from __future__ import annotations

import argparse
import json
import sys
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
from .contracts import ContractViolation
from .pilot import ROOT, build, build_passport, validate_inputs


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

    try:
        store = LocalQuarantineStore(args.quarantine_dir, ROOT)
        engine = AcquisitionEngine(ROOT, store)
        if args.command == "acquire":
            transport = ConstrainedHttpsTransport()
        else:
            plan, _source = load_reviewed_plan(ROOT, args.plan)
            maximum = plan["transport_policy"]["maximum_response_bytes"]
            with args.input.open("rb") as handle:
                body = handle.read(maximum + 1)
            transport = ReplayTransport(body, media_type=args.media_type)
        result = engine.run(args.plan, transport)
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
