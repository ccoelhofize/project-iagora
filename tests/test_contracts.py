# SPDX-License-Identifier: EUPL-1.2

import copy
import hashlib
import unittest

from iagora.contracts import ContractViolation, load_json, validate
from iagora.pilot import CONTRACTS, SOURCE_PROFILES, SNAPSHOT, validate_inputs


class ContractTests(unittest.TestCase):
    def test_repository_inputs_validate(self) -> None:
        (
            profiles,
            snapshot,
            dataset,
            campaign_artifact,
            acquisition_event,
            raw_dataset,
        ) = validate_inputs()
        self.assertEqual(11, len(profiles["sources"]))
        self.assertEqual("2025-12-31", snapshot["observation_cutoff"])
        self.assertEqual(6, len(dataset["records"]))
        self.assertEqual(
            "authenticated_with_limitations", campaign_artifact["authenticity"]["outcome"]
        )
        self.assertEqual(6, raw_dataset["total_count"])
        self.assertEqual(3189, acquisition_event["response"]["byte_size"])
        self.assertTrue(snapshot["source_dataset"]["raw_bytes_preserved"])

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
