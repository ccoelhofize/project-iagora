# SPDX-License-Identifier: EUPL-1.2

import json
import tempfile
import unittest
from pathlib import Path

from iagora.pilot import build, build_passport, render_html
from iagora.presentation import (
    dashboard_metrics,
    render_dashboard_html,
    render_education_html,
)


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
        self.assertEqual(22, len(self.passport["evidence"]))
        school_evidence = [
            item
            for item in self.passport["evidence"]
            if item["evidence_id"].startswith("evidence-063")
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
        self.assertEqual(
            "candidate_evidence_found",
            self.passport["campaign_commitment"]["mapping_evidence_state"],
        )
        self.assertEqual(
            "evidenced_at_programme_level",
            self.passport["administrative_chain"]["executed_expenditure"],
        )
        self.assertEqual("not_located", self.passport["administrative_chain"]["procurement"])
        self.assertIn(
            "procurement_and_competent_completion_evidence_missing",
            self.passport["publication"]["blockers"],
        )

    def test_mapping_is_explicit_ai_assisted_and_review_pending(self) -> None:
        mapping = self.passport["commitment_mapping"]
        self.assertEqual("proposed_review_pending", mapping["lifecycle_state"])
        self.assertEqual("ai_assisted", mapping["proposal_origin"])
        self.assertEqual(
            "pending_independent_methodological_review", mapping["review_state"]
        )
        self.assertEqual("implements", mapping["relationship_role"])
        self.assertEqual("essential", mapping["component"]["essentiality"])
        self.assertEqual("action", mapping["component"]["component_type"])
        self.assertEqual("not_stated", mapping["component"]["quantity"]["state"])
        self.assertEqual("not_stated", mapping["component"]["deadline"]["state"])
        self.assertEqual("unknown", mapping["component"]["implementation_state"])
        self.assertEqual(7, len(mapping["scope_comparison"]))
        self.assertEqual("not_verifiable", mapping["fulfillment_conclusion"])

    def test_administrative_evidence_is_linked_without_scope_conflation(self) -> None:
        self.assertEqual(1, len(self.cases["Nestor-Perret"]["administrative_evidence_ids"]))
        self.assertEqual(
            2, len(self.cases["Pierre-et-Marie-Curie"]["administrative_evidence_ids"])
        )
        self.assertEqual(3, len(self.cases["Jean-Zay"]["administrative_evidence_ids"]))
        self.assertTrue(
            all(
                search["interpretation"] == "not_evidence_of_absence"
                for search in self.passport["administrative_chain"]["procurement_searches"]
            )
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
            self.assertEqual(
                (Path(first) / "education/index.html").read_bytes(),
                (Path(second) / "education/index.html").read_bytes(),
            )
            self.assertEqual(
                (Path(first) / "programmes/respire-a-la-recre/index.html").read_bytes(),
                (Path(second) / "programmes/respire-a-la-recre/index.html").read_bytes(),
            )
            parsed = json.loads(first_passport.read_text(encoding="utf-8"))
            self.assertEqual("iagora.knowledge-passport", parsed["contract_id"])

    def test_dashboard_metrics_keep_financial_stages_separate(self) -> None:
        metrics = dashboard_metrics(self.passport)
        self.assertEqual(6, metrics["school_units"])
        self.assertEqual(3, metrics["case_studies"])
        self.assertEqual(3, metrics["state_counts"]["reported_complete"])
        self.assertEqual(2, metrics["state_counts"]["reported_in_progress"])
        self.assertEqual(1, metrics["state_counts"]["reported_not_complete"])
        self.assertEqual(3237, metrics["reported_surface_m2"])
        self.assertEqual(41, metrics["reported_trees"])
        self.assertEqual(4_070_000, metrics["finance"]["programme_authorization"])
        self.assertEqual(1_090_000, metrics["finance"]["executed_2022"])

    def test_city_dashboard_exposes_coverage_without_inventing_macro_kpis(self) -> None:
        rendered = render_dashboard_html(self.passport)
        self.assertIn("Trajectoire de Clermont-Ferrand", rendered)
        self.assertIn("Données insuffisantes pour une comparaison macro", rendered)
        self.assertIn("1/4", rendered)
        self.assertIn("Éducation", rendered)
        self.assertIn("Finances", rendered)
        self.assertIn("Culture", rendered)
        self.assertIn("Sécurité", rendered)
        self.assertIn("Les pointillés signalent une série à définir", rendered)

    def test_education_dashboard_uses_bounded_kpis_and_accessible_chart(self) -> None:
        rendered = render_education_html(self.passport)
        self.assertIn("Tableau de bord thématique", rendered)
        self.assertIn("3\u202f237", rendered)
        self.assertIn(">41<", rendered)
        self.assertIn(
            'aria-label="3 unités déclarées achevées, 2 en cours et 1 non achevée"',
            rendered,
        )
        self.assertIn("Filiation actuellement indéterminable", rendered)
        self.assertIn("4,07 M€", rendered)
        self.assertIn("1\u202f939\u202f810,63 €", rendered)
        self.assertIn("Ces chiffres ne décrivent pas l’ensemble des écoles", rendered)

    def test_html_has_accessible_structure_and_explicit_warning(self) -> None:
        rendered = render_html(self.passport)
        self.assertIn('<html lang="fr">', rendered)
        self.assertIn('<main id="contenu" class="report-shell">', rendered)
        self.assertEqual(5, rendered.count("<caption>"))
        self.assertIn("Prototype local — publication bloquée", rendered)
        self.assertIn("Synthèse multidimensionnelle", rendered)
        self.assertIn("Filiation de la politique publique", rendered)
        self.assertIn("Imprimer le dossier", rendered)
        self.assertIn("Engagement de campagne retrouvé", rendered)
        self.assertIn("Pourquoi le rapprochement avec", rendered)
        self.assertIn("proposition assistée par IA", rendered)
        self.assertIn("Comparaison explicite des périmètres", rendered)
        self.assertIn("Aucune échéance indiquée", rendered)
        self.assertIn("Les lignes par unité scolaire restent distinctes", rendered)
        self.assertIn("La revue méthodologique globale du POC reste incomplète", rendered)
        self.assertNotIn("School-unit rows remain distinct", rendered)
        self.assertNotIn("commitment_mapping_and_methodological_review_incomplete", rendered)
        self.assertIn("authentifié avec limites", rendered)
        self.assertIn("ni à un impact sur la ville", rendered)
        self.assertIn("Croisement avec les décisions et les finances municipales", rendered)
        self.assertIn("1 939 810,63 € cumulés avant 2023", rendered)


if __name__ == "__main__":
    unittest.main()
