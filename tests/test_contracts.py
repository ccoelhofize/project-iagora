# SPDX-License-Identifier: EUPL-1.2

import copy
import hashlib
import unittest

from iagora.contracts import ContractViolation, load_json, validate
from iagora.pilot import (
    ADMINISTRATIVE_EVIDENCE,
    CANONICAL_ASSERTIONS,
    COMMITMENT_MAPPING,
    COMMITMENT_MAPPING_REVIEW,
    CONTRACTS,
    PROCUREMENT_EVIDENCE,
    SOURCE_PROFILES,
    SNAPSHOT,
    validate_inputs,
)


class ContractTests(unittest.TestCase):
    def test_repository_inputs_validate(self) -> None:
        (
            profiles,
            snapshot,
            dataset,
            campaign_artifact,
            acquisition_event,
            raw_dataset,
            administrative_evidence,
            canonical_assertions,
            commitment_mapping,
            commitment_mapping_review,
            procurement_evidence,
            procurement_acquisition_event,
            procurement_raw,
        ) = validate_inputs()
        self.assertEqual(19, len(profiles["sources"]))
        self.assertEqual("2025-12-31", snapshot["observation_cutoff"])
        self.assertEqual(6, len(dataset["records"]))
        self.assertEqual(
            "authenticated_with_limitations", campaign_artifact["authenticity"]["outcome"]
        )
        campaign_profile = next(
            item for item in profiles["sources"] if item["source_id"] == "src-campaign-2020-primary"
        )
        self.assertEqual(
            campaign_artifact["rights"]["state"], campaign_profile["rights"]["state"]
        )
        self.assertEqual(6, raw_dataset["total_count"])
        self.assertEqual(3189, acquisition_event["response"]["byte_size"])
        self.assertTrue(snapshot["source_dataset"]["raw_bytes_preserved"])
        self.assertEqual(10, len(administrative_evidence["documents"]))
        self.assertFalse(administrative_evidence["raw_bytes_preserved"])
        self.assertEqual(1, len(canonical_assertions["assertions"]))
        self.assertEqual(
            commitment_mapping["target_programme"]["target_assertion_id"],
            canonical_assertions["assertions"][0]["assertion_id"],
        )
        self.assertEqual("proposed_review_pending", commitment_mapping["lifecycle_state"])
        self.assertEqual(1, len(commitment_mapping["components"]))
        self.assertEqual(
            "ready_for_maintainer_review",
            commitment_mapping_review["lifecycle_state"],
        )
        self.assertEqual(2, len(commitment_mapping_review["ai_advisory_roles"]))
        self.assertEqual(5, len(commitment_mapping_review["ai_advisory_runs"]))
        self.assertIsNone(commitment_mapping_review["maintainer_review"])
        self.assertEqual([], commitment_mapping_review["independent_human_reviews"])
        self.assertIsNone(commitment_mapping_review["independent_final_decision"])
        self.assertEqual(
            "partial_candidate_services_evidence",
            procurement_evidence["chain_summary"]["procurement"],
        )
        self.assertEqual(8, procurement_acquisition_event["response"]["record_count"])
        self.assertEqual(8, len(procurement_raw["results"]))

    def test_acquisition_event_and_raw_artifact_validate(self) -> None:
        event_path = (
            SNAPSHOT.parents[1]
            / "raw/respire-a-la-recre/2026-07-29/acquisition-event.json"
        )
        event = load_json(event_path)
        schema = load_json(CONTRACTS / "acquisition-event.schema.json")
        validate(event, schema)
        raw_path = (
            SNAPSHOT.parents[1]
            / "raw/respire-a-la-recre/2026-07-29/records-selected.json"
        )
        self.assertEqual(
            event["raw_artifact"]["sha256"],
            hashlib.sha256(raw_path.read_bytes()).hexdigest(),
        )
        raw = load_json(raw_path)
        selected_fields = set(event["request"]["selected_fields"])
        self.assertTrue(all(set(row) == selected_fields for row in raw["results"]))
        self.assertTrue(all("position" not in row for row in raw["results"]))
        self.assertTrue(
            all(
                not key.startswith("fichier_")
                for row in raw["results"]
                for key in row
            )
        )

    def test_historical_snapshot_remains_valid(self) -> None:
        historical = load_json(SNAPSHOT.with_name("pilot-snapshot-0.1.json"))
        schema = load_json(CONTRACTS / "pilot-snapshot.schema.json")
        validate(historical, schema)

    def test_campaign_artifact_is_metadata_only(self) -> None:
        campaign = load_json(SNAPSHOT.with_name("campaign-artifact.json"))
        schema = load_json(CONTRACTS / "campaign-artifact.schema.json")
        validate(campaign, schema)
        self.assertFalse(campaign["raw_bytes_preserved"])
        self.assertEqual("blocked", campaign["rights"]["redistribution"])
        self.assertEqual(
            "evidence-campaign-schoolyards-2020",
            campaign["evidence_fragment"]["evidence_id"],
        )
        self.assertRegex(campaign["content_fingerprint_sha256"], r"^[a-f0-9]{64}$")

    def test_canonical_target_assertion_resolves_to_precise_evidence(self) -> None:
        bundle = load_json(CANONICAL_ASSERTIONS)
        schema = load_json(CONTRACTS / "canonical-assertions.schema.json")
        validate(bundle, schema)
        assertion = bundle["assertions"][0]
        self.assertEqual(
            "assertion-respire-schoolyard-transformation-policy-2023",
            assertion["assertion_id"],
        )
        self.assertEqual(
            set(assertion["derivation"]["evidence_ids"]),
            {item["evidence_id"] for item in bundle["evidence_relationships"]},
        )
        self.assertEqual("source_claim", assertion["epistemic_kind"])

    def test_administrative_evidence_preserves_financial_stages(self) -> None:
        bundle = load_json(ADMINISTRATIVE_EVIDENCE)
        schema = load_json(CONTRACTS / "administrative-evidence.schema.json")
        validate(bundle, schema)
        amounts = [
            fragment["amount"]
            for document in bundle["documents"]
            for fragment in document["evidence_fragments"]
            if "amount" in fragment
        ]
        stages = {amount["financial_stage"] for amount in amounts}
        self.assertIn("authorized_programme", stages)
        self.assertIn("authorized_annual", stages)
        self.assertIn("executed_annual", stages)
        self.assertIn("executed_cumulative", stages)
        self.assertIn("forecast_site_cost", stages)
        self.assertTrue(
            all(
                search["interpretation"] == "not_evidence_of_absence"
                for search in bundle["procurement_searches"]
            )
        )
        self.assertTrue(
            all(
                not document["acquisition"]["raw_bytes_preserved"]
                for document in bundle["documents"]
            )
        )
        expected_cases = {"case-nestor-perret", "case-pierre-marie-curie", "case-jean-zay"}
        actual_cases = {
            scope_id
            for document in bundle["documents"]
            if document["scope"]["level"] == "school_case"
            for scope_id in document["scope"]["ids"]
        }
        self.assertEqual(expected_cases, actual_cases)

    def test_procurement_evidence_prevents_double_counting_and_scope_conflation(self) -> None:
        bundle = load_json(PROCUREMENT_EVIDENCE)
        schema = load_json(CONTRACTS / "procurement-evidence.schema.json")
        validate(bundle, schema)
        raw_path = SNAPSHOT.parents[1] / bundle["city_dataset_acquisition"]["raw_local_path"].removeprefix("data/")
        raw = load_json(raw_path)
        rows = raw["results"]
        self.assertEqual(602_150, sum(row["montant"] for row in rows))
        unique_values = {
            row["marche_id"]: row["montant"]
            for row in rows
        }
        self.assertEqual(204_050, sum(unique_values.values()))
        self.assertEqual(
            "post_cutoff_publication_historical_event",
            next(record for record in bundle["records"] if record["role"] == "award_notice")["observation_state"],
        )
        self.assertFalse(bundle["boamp_acquisition"]["raw_bytes_preserved"])
        self.assertEqual("not_located", bundle["chain_summary"]["attributable_works_procurement"])
        self.assertEqual("not_verifiable", bundle["chain_summary"]["fulfillment_conclusion"])
        self.assertTrue(
            all(
                record["scope"]["relationship_to_programme"]
                == "candidate_relevant_object_not_directly_named"
                for record in bundle["records"]
            )
        )

    def test_commitment_mapping_preserves_primary_scope_and_review_gate(self) -> None:
        mapping = load_json(COMMITMENT_MAPPING)
        schema = load_json(CONTRACTS / "commitment-mapping.schema.json")
        validate(mapping, schema)
        component = mapping["components"][0]
        self.assertEqual("Végétalisation des cours d’école", component["original_span"])
        self.assertEqual("essential", component["essentiality"])
        self.assertEqual("action", component["component_type"])
        self.assertEqual({"state": "not_stated", "value": None, "unit": None}, component["quantity"])
        self.assertEqual({"state": "not_stated", "value": None}, component["deadline"])
        self.assertEqual("unknown", component["implementation_state"])
        self.assertEqual("ai_assisted", mapping["method"]["proposal_origin"])
        self.assertEqual([], mapping["review"]["completed_reviews"])
        self.assertIsNone(mapping["review"]["final_decision"])
        self.assertEqual("not_verifiable", mapping["output_constraints"]["fulfillment_conclusion"])
        self.assertFalse(mapping["output_constraints"]["publication_eligible"])

    def test_generated_mapping_cannot_claim_completed_review(self) -> None:
        mapping = load_json(COMMITMENT_MAPPING)
        schema = load_json(CONTRACTS / "commitment-mapping.schema.json")
        invalid = copy.deepcopy(mapping)
        invalid["review"]["state"] = "accepted"
        with self.assertRaisesRegex(ContractViolation, "expected constant"):
            validate(invalid, schema)

    def test_review_packet_supports_interim_maintainer_path_and_stays_fail_closed(self) -> None:
        packet = load_json(COMMITMENT_MAPPING_REVIEW)
        schema = load_json(CONTRACTS / "commitment-mapping-review.schema.json")
        validate(packet, schema)
        self.assertEqual(
            {"methodological_reviewer", "evidence_authority_reviewer"},
            set(packet["human_review_requirements"]["independent_publication_roles"]),
        )
        self.assertTrue(
            packet["human_review_requirements"]["independent_reviewer_separation_required"]
        )
        self.assertEqual(
            "maintainer_reviewer",
            packet["human_review_requirements"]["interim_poc_reviewer_role"],
        )
        self.assertTrue(
            packet["human_review_requirements"][
                "ai_advisory_required_before_maintainer_review"
            ]
        )
        self.assertFalse(packet["preparation"]["counts_as_independent_review"])
        self.assertEqual(
            {"ai_methodology_auditor", "ai_evidence_authority_auditor"},
            {item["role_id"] for item in packet["ai_advisory_roles"]},
        )
        self.assertTrue(
            all(item["status"] == "completed" for item in packet["ai_advisory_roles"])
        )
        self.assertTrue(
            all(
                item["execution_mode"] == "manually_invoked_non_autonomous"
                and item["role_configuration_version"] == "0.3.0"
                for item in packet["ai_advisory_roles"]
            )
        )
        self.assertEqual(
            {"accept", "request_changes"},
            {
                item["recommendation"]
                for item in packet["ai_advisory_runs"]
                if item["reviewed_mapping_version"] == "0.2.0"
            },
        )
        current_runs = [
            item
            for item in packet["ai_advisory_runs"]
            if item["reviewed_mapping_version"] == "0.3.0"
            and item["applicability_state"] == "current"
        ]
        self.assertEqual(2, len(current_runs))
        self.assertEqual(
            {"ai_methodology_auditor", "ai_evidence_authority_auditor"},
            {item["role_id"] for item in current_runs},
        )
        self.assertEqual(
            {"accept"},
            {item["recommendation"] for item in current_runs},
        )
        self.assertTrue(
            all(not item["counts_as_human_review"] for item in packet["ai_advisory_runs"])
        )
        self.assertIsNone(packet["maintainer_review"])
        self.assertEqual(4, len(packet["evidence_basis"]))
        self.assertEqual(
            "indeterminate_with_predecessors",
            next(
                finding["finding_state"]
                for finding in packet["findings"]
                if finding["dimension"] == "policy_lineage"
            ),
        )
        self.assertEqual("not_verifiable", packet["output_constraints"]["fulfillment_conclusion"])
        self.assertFalse(packet["output_constraints"]["publication_eligible"])
        self.assertFalse(packet["output_constraints"]["implementation_percentage_allowed"])

    def test_missing_required_source_field_is_rejected(self) -> None:
        profiles = load_json(SOURCE_PROFILES)
        invalid = copy.deepcopy(profiles)
        del invalid["sources"][0]["purpose"]
        schema = load_json(CONTRACTS / "source-profiles.schema.json")
        with self.assertRaisesRegex(ContractViolation, "missing required fields"):
            validate(invalid, schema)

    def test_publication_gate_cannot_be_enabled_in_prototype_contract(self) -> None:
        snapshot = load_json(SNAPSHOT)
        invalid = copy.deepcopy(snapshot)
        invalid["publication_gate"]["eligible"] = True
        schema = load_json(CONTRACTS / "pilot-snapshot.schema.json")
        with self.assertRaisesRegex(ContractViolation, "expected constant False"):
            validate(invalid, schema)


if __name__ == "__main__":
    unittest.main()
