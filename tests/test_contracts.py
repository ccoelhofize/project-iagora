# SPDX-License-Identifier: EUPL-1.2

import copy
import unittest

from iagora.contracts import ContractViolation, load_json, validate
from iagora.pilot import CONTRACTS, SOURCE_PROFILES, SNAPSHOT, validate_inputs


class ContractTests(unittest.TestCase):
    def test_repository_inputs_validate(self) -> None:
        profiles, snapshot, dataset = validate_inputs()
        self.assertEqual(11, len(profiles["sources"]))
        self.assertEqual("2025-12-31", snapshot["observation_cutoff"])
        self.assertEqual(6, len(dataset["records"]))

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
