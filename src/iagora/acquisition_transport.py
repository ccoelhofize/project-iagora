# SPDX-License-Identifier: EUPL-1.2

"""Constrained Opendatasoft request construction and HTTPS transport.

The connector accepts a reviewed plan, never an arbitrary URL. The live
transport resolves and validates every destination, connects to a pinned public
IP address, preserves TLS hostname verification, disables compression, and
revalidates every redirect.
"""

from __future__ import annotations

import hashlib
import http.client
import ipaddress
import json
import socket
import ssl
import time
from dataclasses import dataclass
from typing import Any, Callable, Iterable, Protocol
from urllib.parse import urlencode, urljoin, urlsplit, urlunsplit


CONNECTOR_TYPE = "opendatasoft_explore_v2_json"
CONNECTOR_RULE_VERSION = "0.1.0"
USER_AGENT = "Project-IAgora/0.1 governed-acquisition-prototype"
REDIRECT_STATUSES = {301, 302, 303, 307, 308}


class AcquisitionFailure(RuntimeError):
    """Safe acquisition failure with a stable public code and outcome."""

    def __init__(
        self,
        safe_code: str,
        safe_message: str,
        *,
        outcome: str,
        resolved_url: str | None = None,
        http_status: int | None = None,
        media_type: str | None = None,
        byte_size: int | None = None,
        duration_milliseconds: int | None = None,
    ) -> None:
        super().__init__(safe_message)
        self.safe_code = safe_code
        self.safe_message = safe_message
        self.outcome = outcome
        self.resolved_url = resolved_url
        self.http_status = http_status
        self.media_type = media_type
        self.byte_size = byte_size
        self.duration_milliseconds = duration_milliseconds


@dataclass(frozen=True)
class RequestSpec:
    """Normalized request produced only from a reviewed acquisition plan."""

    endpoint_url: str
    request_url: str
    allowed_host: str
    allowed_path: str
    expected_media_types: tuple[str, ...]
    timeout_seconds: int
    maximum_response_bytes: int
    maximum_redirects: int


@dataclass(frozen=True)
class FetchResponse:
    """Bounded exact response returned by a transport adapter."""

    requested_url: str
    resolved_url: str
    http_status: int
    media_type: str
    body: bytes
    duration_milliseconds: int
    redirect_count: int


class Transport(Protocol):
    """Environment-independent acquisition transport port."""

    record_origin: str

    def fetch(self, request: RequestSpec) -> FetchResponse:
        """Return one bounded response or raise an AcquisitionFailure."""


def canonical_json_sha256(value: Any) -> str:
    """Fingerprint a JSON-compatible value with deterministic serialization."""

    encoded = json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


class OpendatasoftConnector:
    """Build the first reviewed Explore API request from governed components."""

    connector_type = CONNECTOR_TYPE
    rule_version = CONNECTOR_RULE_VERSION

    def build_request(self, plan: dict[str, Any]) -> RequestSpec:
        connector = plan["connector"]
        if connector["connector_type"] != self.connector_type:
            raise AcquisitionFailure(
                "plan_invalid",
                "The acquisition plan selects an unsupported connector.",
                outcome="blocked_by_policy",
            )
        if connector["connector_rule_version"] != self.rule_version:
            raise AcquisitionFailure(
                "plan_invalid",
                "The acquisition plan selects an unsupported connector-rule version.",
                outcome="blocked_by_policy",
            )

        transport = plan["transport_policy"]
        endpoint_url = urlunsplit(
            (
                transport["scheme"],
                transport["allowed_host"],
                transport["endpoint_path"],
                "",
                "",
            )
        )
        scope = plan["observation_scope"]
        quoted_values = ",".join(
            json.dumps(value, ensure_ascii=True)
            for value in scope["identity_values"]
        )
        query = urlencode(
            (
                ("select", ",".join(plan["query"]["selected_fields"])),
                (
                    "where",
                    f"{scope['identity_field']} in ({quoted_values})",
                ),
                ("order_by", plan["query"]["order_by"]),
                ("limit", str(plan["query"]["result_limit"])),
            )
        )
        return RequestSpec(
            endpoint_url=endpoint_url,
            request_url=f"{endpoint_url}?{query}",
            allowed_host=transport["allowed_host"],
            allowed_path=transport["endpoint_path"],
            expected_media_types=tuple(transport["expected_media_types"]),
            timeout_seconds=transport["timeout_seconds"],
            maximum_response_bytes=transport["maximum_response_bytes"],
            maximum_redirects=transport["maximum_redirects"],
        )


def _default_resolver(host: str, port: int) -> tuple[str, ...]:
    addresses = {
        item[4][0]
        for item in socket.getaddrinfo(
            host,
            port,
            family=socket.AF_UNSPEC,
            type=socket.SOCK_STREAM,
        )
    }
    return tuple(sorted(addresses))


def _is_public_address(address: str) -> bool:
    parsed = ipaddress.ip_address(address)
    return not any(
        (
            parsed.is_private,
            parsed.is_loopback,
            parsed.is_link_local,
            parsed.is_multicast,
            parsed.is_reserved,
            parsed.is_unspecified,
        )
    )


def validate_destination(
    url: str,
    request: RequestSpec,
    resolver: Callable[[str, int], Iterable[str]],
) -> tuple[str, ...]:
    """Validate URL shape and return only resolved public addresses."""

    parsed = urlsplit(url)
    if parsed.scheme != "https":
        raise AcquisitionFailure(
            "unauthorized_endpoint",
            "Only HTTPS acquisition destinations are allowed.",
            outcome="blocked_by_policy",
        )
    if parsed.username is not None or parsed.password is not None or parsed.fragment:
        raise AcquisitionFailure(
            "unauthorized_endpoint",
            "Credentials and fragments are prohibited in acquisition URLs.",
            outcome="blocked_by_policy",
        )
    if parsed.hostname != request.allowed_host or parsed.port not in (None, 443):
        raise AcquisitionFailure(
            "unauthorized_endpoint",
            "The acquisition destination is outside the reviewed host boundary.",
            outcome="blocked_by_policy",
        )
    if parsed.path != request.allowed_path:
        raise AcquisitionFailure(
            "unauthorized_endpoint",
            "The acquisition destination is outside the reviewed endpoint path.",
            outcome="blocked_by_policy",
        )
    if parsed.query != urlsplit(request.request_url).query:
        raise AcquisitionFailure(
            "unauthorized_endpoint",
            "The acquisition destination changed the reviewed query.",
            outcome="blocked_by_policy",
        )
    try:
        addresses = tuple(resolver(parsed.hostname, 443))
    except (OSError, socket.gaierror) as exc:
        raise AcquisitionFailure(
            "network_error",
            "The reviewed acquisition host could not be resolved.",
            outcome="transport_failure",
        ) from exc
    if not addresses:
        raise AcquisitionFailure(
            "network_error",
            "The reviewed acquisition host resolved to no address.",
            outcome="transport_failure",
        )
    try:
        unsafe = [address for address in addresses if not _is_public_address(address)]
    except ValueError as exc:
        raise AcquisitionFailure(
            "unauthorized_endpoint",
            "The acquisition host resolved to an invalid address.",
            outcome="blocked_by_policy",
        ) from exc
    if unsafe:
        raise AcquisitionFailure(
            "unauthorized_endpoint",
            "The acquisition host resolved to a prohibited network destination.",
            outcome="blocked_by_policy",
        )
    return tuple(sorted(set(addresses)))


class _PinnedHTTPSConnection(http.client.HTTPSConnection):
    """HTTPS connection that does not perform a second, unvalidated DNS lookup."""

    def __init__(
        self,
        host: str,
        address: str,
        *,
        timeout: float,
        context: ssl.SSLContext,
    ) -> None:
        super().__init__(host, port=443, timeout=timeout, context=context)
        self._validated_address = address

    def connect(self) -> None:
        if self._tunnel_host:
            raise OSError("HTTP tunnels are not supported by the acquisition transport")
        raw_socket = socket.create_connection(
            (self._validated_address, self.port),
            self.timeout,
            self.source_address,
        )
        self.sock = self._context.wrap_socket(raw_socket, server_hostname=self.host)


def _default_connection_factory(
    host: str,
    address: str,
    timeout: float,
) -> _PinnedHTTPSConnection:
    return _PinnedHTTPSConnection(
        host,
        address,
        timeout=timeout,
        context=ssl.create_default_context(),
    )


def _normalized_media_type(value: str | None) -> str:
    if value is None:
        return ""
    parts = [part.strip().lower() for part in value.split(";")]
    base = parts[0]
    parameters = {}
    for part in parts[1:]:
        if "=" in part:
            key, raw_value = part.split("=", 1)
            parameters[key.strip()] = raw_value.strip().strip('"')
    if "charset" in parameters:
        return f"{base}; charset={parameters['charset']}"
    return base


def _read_bounded_body(response: Any, maximum_bytes: int) -> bytes:
    content_length = response.getheader("Content-Length")
    declared_size = None
    if content_length is not None:
        try:
            declared_size = int(content_length)
        except ValueError as exc:
            raise AcquisitionFailure(
                "malformed_response",
                "The response contains an invalid Content-Length header.",
                outcome="transport_failure",
            ) from exc
        if declared_size < 0:
            raise AcquisitionFailure(
                "malformed_response",
                "The response contains a negative Content-Length header.",
                outcome="transport_failure",
            )
        if declared_size > maximum_bytes:
            raise AcquisitionFailure(
                "response_too_large",
                "The response exceeds the reviewed byte limit.",
                outcome="transport_failure",
                byte_size=declared_size,
            )

    body = bytearray()
    while True:
        remaining_with_probe = maximum_bytes - len(body) + 1
        chunk = response.read(min(65536, remaining_with_probe))
        if not chunk:
            break
        body.extend(chunk)
        if len(body) > maximum_bytes:
            raise AcquisitionFailure(
                "response_too_large",
                "The response exceeds the reviewed byte limit.",
                outcome="transport_failure",
                byte_size=len(body),
            )
    if not body:
        raise AcquisitionFailure(
            "malformed_response",
            "The response body is empty.",
            outcome="transport_failure",
            byte_size=0,
        )
    if declared_size is not None and len(body) != declared_size:
        raise AcquisitionFailure(
            "malformed_response",
            "The response body size differs from Content-Length.",
            outcome="transport_failure",
            byte_size=len(body),
        )
    return bytes(body)


class ConstrainedHttpsTransport:
    """Live transport with SSRF, redirect, compression, size, and timeout gates."""

    record_origin = "live_execution"

    def __init__(
        self,
        *,
        resolver: Callable[[str, int], Iterable[str]] = _default_resolver,
        connection_factory: Callable[[str, str, float], Any] = _default_connection_factory,
        monotonic: Callable[[], float] = time.monotonic,
    ) -> None:
        self._resolver = resolver
        self._connection_factory = connection_factory
        self._monotonic = monotonic

    def fetch(self, request: RequestSpec) -> FetchResponse:
        started = self._monotonic()
        current_url = request.request_url
        redirect_count = 0

        while True:
            try:
                addresses = validate_destination(current_url, request, self._resolver)
            except AcquisitionFailure as failure:
                if redirect_count:
                    raise AcquisitionFailure(
                        "redirect_blocked",
                        "The redirect target violates the reviewed destination policy.",
                        outcome="transport_failure",
                        resolved_url=current_url,
                    ) from failure
                raise
            parsed = urlsplit(current_url)
            response = None
            connection = None
            last_error: BaseException | None = None
            for address in addresses:
                remaining = request.timeout_seconds - (self._monotonic() - started)
                if remaining <= 0:
                    last_error = TimeoutError("acquisition deadline reached")
                    break
                candidate = self._connection_factory(
                    parsed.hostname or request.allowed_host,
                    address,
                    float(remaining),
                )
                try:
                    target = urlunsplit(("", "", parsed.path, parsed.query, ""))
                    candidate.request(
                        "GET",
                        target,
                        headers={
                            "Accept": "application/json",
                            "Accept-Encoding": "identity",
                            "User-Agent": USER_AGENT,
                        },
                    )
                    response = candidate.getresponse()
                    connection = candidate
                    break
                except (OSError, TimeoutError, ssl.SSLError, http.client.HTTPException) as exc:
                    last_error = exc
                    candidate.close()
            if response is None or connection is None:
                code = "timeout" if isinstance(last_error, (TimeoutError, socket.timeout)) else "network_error"
                elapsed = int((self._monotonic() - started) * 1000)
                raise AcquisitionFailure(
                    code,
                    "The reviewed acquisition request could not be completed.",
                    outcome="transport_failure",
                    resolved_url=current_url,
                    duration_milliseconds=elapsed,
                ) from last_error

            try:
                if response.status in REDIRECT_STATUSES:
                    location = response.getheader("Location")
                    if not location or redirect_count >= request.maximum_redirects:
                        raise AcquisitionFailure(
                            "redirect_blocked",
                            "The response redirect is missing or exceeds the reviewed limit.",
                            outcome="transport_failure",
                            resolved_url=current_url,
                            http_status=response.status,
                        )
                    current_url = urljoin(current_url, location)
                    redirect_count += 1
                    continue

                if response.status != 200:
                    raise AcquisitionFailure(
                        "network_error",
                        "The reviewed source returned a non-success HTTP status.",
                        outcome="transport_failure",
                        resolved_url=current_url,
                        http_status=response.status,
                    )

                content_encoding = (response.getheader("Content-Encoding") or "identity").lower()
                if content_encoding not in {"", "identity"}:
                    raise AcquisitionFailure(
                        "unsupported_content_encoding",
                        "Compressed or encoded responses are disabled for this prototype.",
                        outcome="transport_failure",
                        resolved_url=current_url,
                        http_status=response.status,
                    )
                media_type = _normalized_media_type(response.getheader("Content-Type"))
                if media_type not in request.expected_media_types:
                    raise AcquisitionFailure(
                        "unexpected_media_type",
                        "The response media type is outside the reviewed plan.",
                        outcome="transport_failure",
                        resolved_url=current_url,
                        http_status=response.status,
                        media_type=media_type or None,
                    )
                remaining = request.timeout_seconds - (self._monotonic() - started)
                if remaining <= 0:
                    raise AcquisitionFailure(
                        "timeout",
                        "The reviewed acquisition request exceeded its time limit.",
                        outcome="transport_failure",
                        resolved_url=current_url,
                        http_status=response.status,
                    )
                connection_socket = getattr(connection, "sock", None)
                if connection_socket is not None:
                    connection_socket.settimeout(remaining)
                try:
                    body = _read_bounded_body(response, request.maximum_response_bytes)
                except AcquisitionFailure:
                    raise
                except (OSError, TimeoutError, http.client.HTTPException) as exc:
                    code = "timeout" if isinstance(exc, (TimeoutError, socket.timeout)) else "network_error"
                    raise AcquisitionFailure(
                        code,
                        "The response body could not be read safely.",
                        outcome="transport_failure",
                        resolved_url=current_url,
                        http_status=response.status,
                    ) from exc
            finally:
                response.close()
                connection.close()

            elapsed = int((self._monotonic() - started) * 1000)
            return FetchResponse(
                requested_url=request.request_url,
                resolved_url=current_url,
                http_status=200,
                media_type=media_type,
                body=body,
                duration_milliseconds=elapsed,
                redirect_count=redirect_count,
            )


class ReplayTransport:
    """Offline adapter that applies the same byte and media bounds to fixtures."""

    record_origin = "offline_replay"

    def __init__(
        self,
        body: bytes,
        *,
        media_type: str = "application/json; charset=utf-8",
        http_status: int = 200,
    ) -> None:
        self._body = body
        self._media_type = _normalized_media_type(media_type)
        self._http_status = http_status

    def fetch(self, request: RequestSpec) -> FetchResponse:
        if self._http_status != 200:
            raise AcquisitionFailure(
                "network_error",
                "The replay fixture represents a non-success HTTP status.",
                outcome="transport_failure",
                resolved_url=request.request_url,
                http_status=self._http_status,
                duration_milliseconds=0,
            )
        if self._media_type not in request.expected_media_types:
            raise AcquisitionFailure(
                "unexpected_media_type",
                "The replay fixture media type is outside the reviewed plan.",
                outcome="transport_failure",
                resolved_url=request.request_url,
                http_status=200,
                media_type=self._media_type,
                duration_milliseconds=0,
            )
        if len(self._body) > request.maximum_response_bytes:
            raise AcquisitionFailure(
                "response_too_large",
                "The replay fixture exceeds the reviewed byte limit.",
                outcome="transport_failure",
                resolved_url=request.request_url,
                http_status=200,
                media_type=self._media_type,
                byte_size=len(self._body),
                duration_milliseconds=0,
            )
        if not self._body:
            raise AcquisitionFailure(
                "malformed_response",
                "The replay fixture body is empty.",
                outcome="transport_failure",
                resolved_url=request.request_url,
                http_status=200,
                media_type=self._media_type,
                byte_size=0,
                duration_milliseconds=0,
            )
        return FetchResponse(
            requested_url=request.request_url,
            resolved_url=request.request_url,
            http_status=200,
            media_type=self._media_type,
            body=self._body,
            duration_milliseconds=0,
            redirect_count=0,
        )
