# SPDX-License-Identifier: EUPL-1.2

import hashlib
import re
import unittest
from pathlib import Path
from urllib.parse import unquote

from iagora.pilot import ROOT


class RepositoryIntegrityTests(unittest.TestCase):
    def test_license_matches_verified_official_text(self) -> None:
        digest = hashlib.sha256((ROOT / "LICENSE").read_bytes()).hexdigest()
        self.assertEqual("6fc9e709ccbfe0d77fbffa2427a983282be2eb88e47b1cdb49f21a83b4d1e665", digest)

    def test_markdown_files_have_one_h1(self) -> None:
        for path in ROOT.rglob("*.md"):
            if ".git" in path.parts or "build" in path.parts:
                continue
            headings = [line for line in path.read_text(encoding="utf-8").splitlines() if line.startswith("# ")]
            self.assertEqual(1, len(headings), f"{path.relative_to(ROOT)} must contain exactly one H1")

    def test_relative_markdown_links_resolve(self) -> None:
        link_pattern = re.compile(r"(?<!!)\[[^]]*\]\(([^)]+)\)")
        failures = []
        for path in ROOT.rglob("*.md"):
            if ".git" in path.parts or "build" in path.parts:
                continue
            for raw_target in link_pattern.findall(path.read_text(encoding="utf-8")):
                target = raw_target.strip().strip("<>").split("#", 1)[0]
                if not target or target.startswith(("http://", "https://", "mailto:")):
                    continue
                resolved = (path.parent / unquote(target)).resolve()
                if not resolved.exists():
                    failures.append(f"{path.relative_to(ROOT)} -> {raw_target}")
        self.assertEqual([], failures)


if __name__ == "__main__":
    unittest.main()
