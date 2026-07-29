# SPDX-License-Identifier: EUPL-1.2

import json
import tempfile
import unittest
from pathlib import Path

from iagora.pilot import build, build_passport, render_html


class PilotSliceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.passport = build_passport()
        self.cases = {case["school_name"]: case for case in self.passport["case_studies"]}

    def test_three_cases_preserve_school_unit_scope(self) -> None:
        self.assertEqual({"Nestor-Perret", "Pierre-et-Marie-Curie", "Jean-Zay"}, set(self.cases))
        self.assertEqual("reported_complete", self.cases["Nestor-Perret"]["reported_summary"])
        self.assertEqual("reported_in_progress", self.cases["Jean-Zay"]["reported_summary"])
        self.assertEqual("mixed_by_school_unit", self.cases["Pierre-et-Marie-Curie"]["reported_summary"])

    def test_every_source_row_has_precise_evidence(self) -> None:
        self.assertEqual(7, len(self.passport["evidence"]))
        school_evidence = [
            item
            for item in self.passport["evidence"]
            if item["evidence_id"] != "evidence-campaign-schoolyards-2020"
        ]
        self.assertEqual(6, len(school_evidence))
        self.assertTrue(all("records[uai=" in item["locator"] for item in school_evidence))
        self.assertEqual(
            "Végétalisation des cours d’école",
            self.passport["campaign_commitment"]["wording"],
        )

    def test_unsupported_conclusions_are_blocked(self) -> None:
        self.assertFalse(self.passport["publication"]["eligible"])
        self.assertEqual("not_verifiable", self.passport["assertion"]["fulfillment_conclusion"])
        self.assertEqual("causal_status_not_verifiable", self.passport["assertion"]["causal_claim_class"])
        self.assertNotIn("primary_campaign_artifact_missing", self.passport["publication"]["blockers"])
        self.assertIn(
            "commitment_mapping_and_methodological_review_incomplete",
            self.passport["publication"]["blockers"],
        )
        self.assertEqual(
            "primary_source_authenticated_with_limitations",
            self.passport["campaign_commitment"]["verification_state"],
        )

    def test_reported_permeable_share_matches_reported_surfaces(self) -> None:
        checked = 0
        for case in self.passport["case_studies"]:
            for record in case["records"]:
                surface = record["existing_surface_m2"]
                deimpermeabilized = record["deimpermeabilized_surface_m2"]
                reported_share = record["permeable_share_percent"]
                if surface is None or deimpermeabilized is None or reported_share is None:
                    continue
                checked += 1
                self.assertAlmostEqual(100 * deimpermeabilized / surface, reported_share)
        self.assertEqual(4, checked)

    def test_build_is_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            first_passport, first_html = build(Path(first))
            second_passport, second_html = build(Path(second))
            self.assertEqual(first_passport.read_bytes(), second_passport.read_bytes())
            self.assertEqual(first_html.read_bytes(), second_html.read_bytes())
            parsed = json.loads(first_passport.read_text(encoding="utf-8"))
            self.assertEqual("iagora.knowledge-passport", parsed["contract_id"])

    def test_html_has_accessible_structure_and_explicit_warning(self) -> None:
        rendered = render_html(self.passport)
        self.assertIn('<html lang="fr">', rendered)
        self.assertIn("<main>", rendered)
        self.assertEqual(3, rendered.count("<caption>"))
        self.assertIn("Prototype local — publication bloquée", rendered)
        self.assertIn("Engagement de campagne retrouvé", rendered)
        self.assertIn("authentifié avec limites", rendered)
        self.assertIn("ni à un impact sur la ville", rendered)


if __name__ == "__main__":
    unittest.main()
