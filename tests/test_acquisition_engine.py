# SPDX-License-Identifier: EUPL-1.2

from __future__ import annotations

import copy
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import parse_qs, urlsplit
from unittest.mock import patch

from iagora.acquisition_engine import (
    AcquisitionEngine,
    LocalQuarantineStore,
    load_reviewed_plan,
)
from iagora.acquisition_transport import (
    AcquisitionFailure,
    ConstrainedHttpsTransport,
    OpendatasoftConnector,
    ReplayTransport,
    validate_destination,
)
from iagora.contracts import ContractViolation
from iagora.__main__ import main
from iagora.pilot import ROOT


PLAN_ID = "plan-city-schools-pilot-cases"
PUBLIC_ADDRESS = "93.184.216.34"


class FakeResponse:
    def __init__(
        self,
        status: int,
        body: bytes = b"",
        headers: dict[str, str] | None = None,
    ) -> None:
        self.status = status
        self._body = body
        self._offset = 0
        self._headers = headers or {}
        self.closed = False

    def getheader(self, name: str) -> str | None:
        return self._headers.get(name)

    def read(self, size: int) -> bytes:
        chunk = self._body[self._offset : self._offset + size]
        self._offset += len(chunk)
        return chunk

    def close(self) -> None:
        self.closed = True


class FakeConnection:
    def __init__(self, response: FakeResponse) -> None:
        self.response = response
        self.requests: list[tuple[str, str, dict[str, str]]] = []
        self.closed = False

    def request(self, method: str, target: str, headers: dict[str, str]) -> None:
        self.requests.append((method, target, headers))

    def getresponse(self) -> FakeResponse:
        return self.response

    def close(self) -> None:
        self.closed = True


class SequenceConnectionFactory:
    def __init__(self, responses: list[FakeResponse]) -> None:
        self.responses = iter(responses)
        self.connections: list[tuple[str, str, float, FakeConnection]] = []

    def __call__(self, host: str, address: str, timeout: float) -> FakeConnection:
        connection = FakeConnection(next(self.responses))
        self.connections.append((host, address, timeout, connection))
        return connection


class IncrementOneTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.plan, _source = load_reviewed_plan(ROOT, PLAN_ID)
        cls.request = OpendatasoftConnector().build_request(cls.plan)
        cls.baseline_path = (
            ROOT
            / "data/raw/respire-a-la-recre/2026-07-29/records-selected.json"
        )
        cls.baseline_body = cls.baseline_path.read_bytes()

    def _engine(self, store: LocalQuarantineStore) -> AcquisitionEngine:
        identifiers = iter(
            [
                "attempt-test-0001",
                "correlation-test-0001",
                "attempt-test-0002",
                "correlation-test-0002",
                "attempt-test-0003",
                "correlation-test-0003",
            ]
        )
        return AcquisitionEngine(
            ROOT,
            store,
            now=lambda: datetime(2026, 8, 3, 18, 0, tzinfo=timezone.utc),
            identifier=lambda _prefix: next(identifiers),
        )

    def test_connector_builds_one_deterministic_reviewed_request(self) -> None:
        second = OpendatasoftConnector().build_request(copy.deepcopy(self.plan))
        self.assertEqual(self.request, second)
        parsed = urlsplit(self.request.request_url)
        query = parse_qs(parsed.query)
        self.assertEqual("https", parsed.scheme)
        self.assertEqual("opendata.clermont-ferrand.fr", parsed.hostname)
        self.assertEqual(self.plan["query"]["selected_fields"], query["select"][0].split(","))
        self.assertEqual(["uai"], query["order_by"])
        self.assertEqual(["10"], query["limit"])
        self.assertNotIn("url", self.plan)

    def test_unregistered_plan_is_rejected_before_transport(self) -> None:
        with self.assertRaisesRegex(AcquisitionFailure, "not registered") as raised:
            load_reviewed_plan(ROOT, "../../arbitrary")
        self.assertEqual("plan_invalid", raised.exception.safe_code)
        self.assertEqual("blocked_by_policy", raised.exception.outcome)

    def test_destination_rejects_loopback_and_mixed_dns_answers(self) -> None:
        for addresses in (("127.0.0.1",), (PUBLIC_ADDRESS, "169.254.169.254")):
            with self.subTest(addresses=addresses):
                with self.assertRaisesRegex(AcquisitionFailure, "prohibited network") as raised:
                    validate_destination(
                        self.request.request_url,
                        self.request,
                        lambda _host, _port: addresses,
                    )
                self.assertEqual("unauthorized_endpoint", raised.exception.safe_code)

    def test_redirect_is_revalidated_and_cross_host_redirect_is_blocked(self) -> None:
        same_host = SequenceConnectionFactory(
            [
                FakeResponse(
                    302,
                    headers={"Location": self.request.request_url},
                ),
                FakeResponse(
                    200,
                    self.baseline_body,
                    {
                        "Content-Type": "application/json; charset=utf-8",
                        "Content-Length": str(len(self.baseline_body)),
                    },
                ),
            ]
        )
        resolutions: list[str] = []

        def resolver(host: str, _port: int) -> tuple[str, ...]:
            resolutions.append(host)
            return (PUBLIC_ADDRESS,)

        response = ConstrainedHttpsTransport(
            resolver=resolver,
            connection_factory=same_host,
        ).fetch(self.request)
        self.assertEqual(1, response.redirect_count)
        self.assertEqual(2, len(resolutions))

        cross_host = SequenceConnectionFactory(
            [
                FakeResponse(
                    302,
                    headers={
                        "Location": "https://example.com/api/explore/v2.1/catalog/datasets/respire-a-la-recre-et-les-enfants-d-abord-vcf/records"
                    },
                )
            ]
        )
        with self.assertRaisesRegex(AcquisitionFailure, "redirect target") as raised:
            ConstrainedHttpsTransport(
                resolver=lambda _host, _port: (PUBLIC_ADDRESS,),
                connection_factory=cross_host,
            ).fetch(self.request)
        self.assertEqual("redirect_blocked", raised.exception.safe_code)

        changed_query = SequenceConnectionFactory(
            [
                FakeResponse(
                    302,
                    headers={"Location": f"{self.request.endpoint_url}?limit=1"},
                )
            ]
        )
        with self.assertRaises(AcquisitionFailure) as changed_query_failure:
            ConstrainedHttpsTransport(
                resolver=lambda _host, _port: (PUBLIC_ADDRESS,),
                connection_factory=changed_query,
            ).fetch(self.request)
        self.assertEqual("redirect_blocked", changed_query_failure.exception.safe_code)

    def test_transport_blocks_size_media_type_and_compression(self) -> None:
        cases = (
            (
                FakeResponse(
                    200,
                    b"{}",
                    {
                        "Content-Type": "application/json",
                        "Content-Length": str(self.request.maximum_response_bytes + 1),
                    },
                ),
                "response_too_large",
            ),
            (
                FakeResponse(200, b"{}", {"Content-Type": "text/html"}),
                "unexpected_media_type",
            ),
            (
                FakeResponse(
                    200,
                    b"{}",
                    {"Content-Type": "application/json", "Content-Encoding": "gzip"},
                ),
                "unsupported_content_encoding",
            ),
        )
        for response, expected_code in cases:
            with self.subTest(expected_code=expected_code):
                factory = SequenceConnectionFactory([response])
                with self.assertRaises(AcquisitionFailure) as raised:
                    ConstrainedHttpsTransport(
                        resolver=lambda _host, _port: (PUBLIC_ADDRESS,),
                        connection_factory=factory,
                    ).fetch(self.request)
                self.assertEqual(expected_code, raised.exception.safe_code)

    def test_historical_replay_is_unchanged_and_not_duplicated(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            store = LocalQuarantineStore(Path(temporary), ROOT)
            result = self._engine(store).run(
                PLAN_ID,
                ReplayTransport(self.baseline_body),
            )
            self.assertEqual("unchanged", result.attempt["outcome"])
            self.assertEqual("offline_replay", result.attempt["record_origin"])
            self.assertEqual("not_run", result.attempt["policy_decisions"]["security"])
            self.assertIsNone(result.artifact)
            self.assertFalse(result.object_created)
            self.assertEqual("unchanged", result.change_report["comparison_state"])
            self.assertEqual(0, result.change_report["summary"]["fields_changed"])
            self.assertFalse((Path(temporary) / "objects").exists())
            self.assertEqual(
                result.change_report["candidate"]["sha256"],
                result.safe_summary()["sha256"],
            )

    def test_changed_valid_response_creates_one_candidate_and_field_report(self) -> None:
        payload = json.loads(self.baseline_body)
        payload["results"][0]["nb_arbres_plantes"] = (
            payload["results"][0]["nb_arbres_plantes"] or 0
        ) + 1
        synthetic_body = (
            json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n"
        ).encode("utf-8")

        with tempfile.TemporaryDirectory() as temporary:
            store = LocalQuarantineStore(Path(temporary), ROOT)
            engine = self._engine(store)
            first = engine.run(PLAN_ID, ReplayTransport(synthetic_body))
            second = engine.run(PLAN_ID, ReplayTransport(synthetic_body))
            self.assertEqual("candidate_new_version", first.attempt["outcome"])
            self.assertTrue(first.object_created)
            self.assertFalse(second.object_created)
            self.assertEqual(
                first.artifact["artifact_version_id"],
                second.artifact["artifact_version_id"],
            )
            self.assertEqual("quarantined", first.artifact["lifecycle_state"])
            self.assertEqual("offline_replay", first.artifact["record_origin"])
            self.assertEqual(1, first.change_report["summary"]["fields_changed"])
            self.assertEqual("candidate_changed", first.change_report["comparison_state"])
            objects = list((Path(temporary) / "objects").rglob("*.bin"))
            self.assertEqual(1, len(objects))
            serialized = json.dumps(
                {
                    "attempt": first.attempt,
                    "artifact": first.artifact,
                    "report": first.change_report,
                    "summary": first.safe_summary(),
                }
            )
            self.assertNotIn(str(Path(temporary)), serialized)
            self.assertNotIn(str(self.baseline_path), serialized)

    def test_duplicate_identity_is_quarantined_without_civic_promotion(self) -> None:
        payload = json.loads(self.baseline_body)
        payload["results"][-1]["uai"] = payload["results"][0]["uai"]
        synthetic_body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        with tempfile.TemporaryDirectory() as temporary:
            store = LocalQuarantineStore(Path(temporary), ROOT)
            result = self._engine(store).run(
                PLAN_ID,
                ReplayTransport(synthetic_body),
            )
            self.assertEqual("quarantined_validation_failure", result.attempt["outcome"])
            self.assertEqual("duplicate_identity", result.attempt["safe_failure_code"])
            self.assertIsNotNone(result.artifact)
            self.assertIsNone(result.change_report)
            self.assertEqual("not_admitted", result.safe_summary()["admission_state"])
            self.assertFalse(result.safe_summary()["publication_authorized"])

    def test_transport_failure_is_recorded_without_raw_content(self) -> None:
        class FailedTransport:
            record_origin = "live_execution"

            def fetch(self, _request):
                raise AcquisitionFailure(
                    "timeout",
                    "The reviewed acquisition request timed out.",
                    outcome="transport_failure",
                    duration_milliseconds=20000,
                )

        with tempfile.TemporaryDirectory() as temporary:
            store = LocalQuarantineStore(Path(temporary), ROOT)
            result = self._engine(store).run(PLAN_ID, FailedTransport())
            self.assertEqual("transport_failure", result.attempt["outcome"])
            self.assertEqual("timeout", result.attempt["safe_failure_code"])
            self.assertIsNone(result.artifact)
            attempts = list((Path(temporary) / "attempts").glob("*.json"))
            self.assertEqual(1, len(attempts))
            self.assertNotIn("results", attempts[0].read_text(encoding="utf-8"))

    def test_missing_quarantine_bytes_are_not_silently_restored(self) -> None:
        payload = json.loads(self.baseline_body)
        payload["results"][0]["nb_arbres_plantes"] = 99
        synthetic_body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        with tempfile.TemporaryDirectory() as temporary:
            store = LocalQuarantineStore(Path(temporary), ROOT)
            engine = self._engine(store)
            first = engine.run(PLAN_ID, ReplayTransport(synthetic_body))
            object_path = Path(temporary) / first.artifact["storage"]["storage_reference"]
            object_path.unlink()
            with self.assertRaisesRegex(ContractViolation, "restoration is prohibited"):
                engine.run(PLAN_ID, ReplayTransport(synthetic_body))
            self.assertFalse(object_path.exists())

    def test_replay_cli_emits_only_safe_summary(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = io.StringIO()
            arguments = [
                "iagora",
                "replay",
                "--plan",
                PLAN_ID,
                "--input",
                str(self.baseline_path),
                "--quarantine-dir",
                temporary,
            ]
            with patch.object(sys, "argv", arguments), redirect_stdout(output):
                self.assertEqual(0, main())
            summary = json.loads(output.getvalue())
            self.assertEqual("unchanged", summary["outcome"])
            self.assertEqual("not_admitted", summary["admission_state"])
            self.assertNotIn(temporary, output.getvalue())
            self.assertNotIn(str(self.baseline_path), output.getvalue())

    def test_quarantine_store_refuses_repository_paths(self) -> None:
        with self.assertRaisesRegex(ContractViolation, "outside the repository"):
            LocalQuarantineStore(ROOT / "build" / "quarantine", ROOT)


if __name__ == "__main__":
    unittest.main()
