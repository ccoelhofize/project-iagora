# SPDX-License-Identifier: EUPL-1.2

import copy
import hashlib
import unittest

from iagora.contracts import ContractViolation, load_json, validate
from iagora.pilot import (
    ADMINISTRATIVE_EVIDENCE,
    COMMITMENT_MAPPING,
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
            commitment_mapping,
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
        self.assertEqual(6, raw_dataset["total_count"])
        self.assertEqual(3189, acquisition_event["response"]["byte_size"])
        self.assertTrue(snapshot["source_dataset"]["raw_bytes_preserved"])
        self.assertEqual(10, len(administrative_evidence["documents"]))
        self.assertFalse(administrative_evidence["raw_bytes_preserved"])
        self.assertEqual("proposed_review_pending", commitment_mapping["lifecycle_state"])
        self.assertEqual(1, len(commitment_mapping["components"]))
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
        self.assertRegex(campaign["content_fingerprint_sha256"], r"^[a-f0-9]{64}$")

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
