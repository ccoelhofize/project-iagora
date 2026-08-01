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
        self.assertEqual(26, len(self.passport["evidence"]))
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
        self.assertEqual(
            "Olivier Bianchi",
            self.passport["campaign_commitment"]["attribution"]["actor"],
        )
        self.assertEqual(
            "Naturellement Clermont",
            self.passport["campaign_commitment"]["attribution"]["campaign_list"],
        )
        self.assertEqual(
            {
                "quantity_state": "not_stated",
                "deadline_state": "not_stated",
                "budget_state": "not_stated",
                "broader_geographic_claim_state": "absent_from_primary_fragment",
            },
            self.passport["campaign_commitment"]["specificity"],
        )
        context_sources = self.passport["provenance"]["supporting_context_sources"]
        self.assertEqual(["src-campaign-2020-interview"], [item["source_id"] for item in context_sources])
        self.assertEqual("not_authoritative", context_sources[0]["authority_state"])

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
        self.assertEqual(
            "partial_candidate_services_evidence",
            self.passport["administrative_chain"]["procurement"],
        )
        self.assertIn(
            "attributable_works_procurement_and_competent_completion_evidence_missing",
            self.passport["publication"]["blockers"],
        )

    def test_procurement_evidence_stays_at_service_and_multi_school_scope(self) -> None:
        records = self.passport["administrative_chain"]["procurement_records"]
        award = next(record for record in records if record["role"] == "award_notice")
        self.assertEqual(158_300, award["amount"]["value"])
        self.assertEqual(
            "post_cutoff_publication_historical_event", award["observation_state"]
        )
        pierre_lot = next(
            lot for lot in award["lots"] if "Pierre-et-Marie-Curie" in lot["school_groups"]
        )
        self.assertEqual(
            {"Alphonse-Daudet", "Pierre-et-Marie-Curie"},
            set(pierre_lot["school_groups"]),
        )
        self.assertEqual(5, len(self.passport["quality"]["procurement_findings"]))

    def test_mapping_is_explicit_ai_assisted_and_review_pending(self) -> None:
        mapping = self.passport["commitment_mapping"]
        self.assertEqual("proposed_review_pending", mapping["lifecycle_state"])
        self.assertEqual("ai_assisted", mapping["proposal_origin"])
        self.assertEqual(
            "pending_independent_methodological_review", mapping["review_state"]
        )
        self.assertEqual("candidate_correspondence", mapping["relationship_role"])
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
        self.assertIn("Nous n’avons pas encore assez de données", rendered)
        self.assertIn("1/4", rendered)
        self.assertIn("Éducation", rendered)
        self.assertIn("Finances", rendered)
        self.assertIn("Culture", rendered)
        self.assertIn("Sécurité", rendered)
        self.assertIn("Les pointillés signifient « donnée manquante », pas zéro", rendered)

    def test_education_dashboard_uses_bounded_kpis_and_accessible_chart(self) -> None:
        rendered = render_education_html(self.passport)
        self.assertIn("Tableau de bord thématique", rendered)
        self.assertIn("L’essentiel en un regard", rendered)
        self.assertIn("Végétalisation des cours d’école", rendered)
        self.assertIn("La promesse a-t-elle été tenue ?", rendered)
        self.assertIn("Non vérifiable", rendered)
        self.assertIn("Les six unités scolaires que nous avons pu vérifier", rendered)
        self.assertIn("Données publiées par la mairie", rendered)
        self.assertIn('3 unités</strong><span class="state-card__label">terminées', rendered)
        self.assertIn('2 unités</strong><span class="state-card__label">en cours', rendered)
        self.assertIn('1 unité</strong><span class="state-card__label">non terminée', rendered)
        self.assertIn("Thèmes proposés", rendered)
        self.assertIn("Cadre de vie et transition écologique", rendered)
        self.assertIn("Voir ce qui a changé entre la promesse et le programme", rendered)
        self.assertIn("ne permettent pas de dire que toute la promesse", rendered)
        self.assertIn("3\u202f237", rendered)
        self.assertIn(">41<", rendered)
        self.assertIn(
            'aria-label="Selon les données publiées par la mairie : 3 unités indiquées comme terminées, 2 en cours et 1 non terminée, sur les six unités scolaires étudiées"',
            rendered,
        )
        self.assertIn("Le lien semble possible, mais il doit encore être vérifié", rendered)
        self.assertIn("4,07 M€", rendered)
        self.assertIn("1\u202f939\u202f810,63 €", rendered)
        self.assertIn("Elles ne décrivent pas toutes les écoles", rendered)
        self.assertIn("Olivier Bianchi", rendered)
        self.assertIn("Naturellement Clermont", rendered)
        self.assertIn("Nombre d’écoles non indiqué", rendered)
        self.assertIn("Pour calculer un pourcentage", rendered)
        self.assertIn("Ce que nous pouvons suivre, de la promesse aux travaux", rendered)
        self.assertIn('href="#etat-realise"', rendered)
        self.assertIn('id="etat-en-cours"', rendered)
        self.assertIn("Le budget a-t-il été respecté ?", rendered)
        self.assertIn("Économies ou coûts évités", rendered)
        self.assertIn("ils ne veulent pas tous dire la même chose", rendered)
        self.assertIn("Presse et autres déclarations", rendered)
        self.assertIn("Cette recherche reste à faire", rendered)
        self.assertIn("Nous n’en avons trouvé aucune dans les documents étudiés", rendered)
        self.assertNotIn("corpus borné", rendered)
        self.assertNotIn("Crédits rephasés", rendered)
        self.assertNotIn("Mandats cumulés", rendered)

    def test_html_has_accessible_structure_and_explicit_warning(self) -> None:
        rendered = render_html(self.passport)
        self.assertIn('<html lang="fr">', rendered)
        self.assertIn('<main id="contenu" class="report-shell">', rendered)
        self.assertEqual(5, rendered.count("<caption>"))
        self.assertIn("Prototype local — publication bloquée", rendered)
        self.assertIn("L’essentiel en six réponses", rendered)
        self.assertIn("La promesse a-t-elle été tenue ?", rendered)
        self.assertIn("Nous n’avons pas assez de preuves pour répondre", rendered)
        self.assertIn("Le programme vient-il de la promesse ?", rendered)
        self.assertIn("Imprimer le dossier", rendered)
        self.assertIn("Qu’avait promis le candidat ?", rendered)
        self.assertIn("Pourquoi relions-nous cette promesse", rendered)
        self.assertIn("proposition assistée par intelligence artificielle", rendered)
        self.assertIn("Comparaison explicite des périmètres", rendered)
        self.assertIn("Aucune échéance indiquée", rendered)
        self.assertIn("Les lignes par unité scolaire restent distinctes", rendered)
        self.assertIn("La revue méthodologique globale du POC reste incomplète", rendered)
        self.assertNotIn("School-unit rows remain distinct", rendered)
        self.assertNotIn("commitment_mapping_and_methodological_review_incomplete", rendered)
        self.assertIn("authentifiée avec limites", rendered)
        self.assertIn("mesurer ses effets sur la ville", rendered)
        self.assertIn("Quelles décisions et quels montants avons-nous retrouvés ?", rendered)
        self.assertIn("1 939 810,63 € d’ordres de paiement enregistrés avant 2023", rendered)
        self.assertIn("Identifiant national de l’école (UAI)", rendered)
        self.assertNotIn(">AP de 4,07 M€<", rendered)
        self.assertNotIn(">810 000 € de CP 2023<", rendered)


if __name__ == "__main__":
    unittest.main()
