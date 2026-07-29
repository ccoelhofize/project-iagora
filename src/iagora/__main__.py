# SPDX-License-Identifier: EUPL-1.2

from __future__ import annotations

import argparse
from pathlib import Path

from .pilot import ROOT, build, build_passport, validate_inputs


def main() -> int:
    parser = argparse.ArgumentParser(description="Project IAgora bounded POC tools")
    subcommands = parser.add_subparsers(dest="command", required=True)
    subcommands.add_parser("validate", help="Validate contracts and deterministic invariants")
    build_parser = subcommands.add_parser("build", help="Build the local passport and accessible HTML")
    build_parser.add_argument("--output", type=Path, default=ROOT / "build" / "pilot")
    args = parser.parse_args()

    if args.command == "validate":
        validate_inputs()
        build_passport()
        print(
            "Validated source profiles, campaign artifact metadata, commitment mapping, "
            "pilot snapshot, administrative evidence, open-data subset, and Knowledge Passport."
        )
        return 0

    passport_path, html_path = build(args.output)
    print(f"Built {passport_path}")
    print(f"Built {html_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
