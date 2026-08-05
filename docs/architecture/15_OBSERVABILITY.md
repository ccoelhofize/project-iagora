# Observability

**Status:** Draft  
**Owner:** Maintainers  
**Last reviewed:** 2026-08-05

## Purpose

Observability must reveal whether evidence moves safely and reproducibly through the system without leaking source content, personal data, or secrets.

## Signals

### Acquisition and processing

Track attempts, outcomes, latency, source freshness, fingerprints, quarantine reasons, parser failures, contract failures, retries, duplicate prevention, and lineage completeness.

### Governance and publication

Track authority-review backlog, unresolved conflicts, missing citations, passport validation, review state, restriction propagation, index invalidation, and publication-gate failures.

### Service health

Track availability, error rates, latency, saturation, dependency health, backup success, restore tests, security events, and access anomalies.

## Logging rules

Logs use stable event names, correlation identifiers, environment, component, safe object identifiers, outcome, and rule version. They MUST NOT contain raw document bodies, secrets, hidden model reasoning, unnecessary personal data, or access tokens.

## Alerts and objectives

Alerts should correspond to actionable user or evidence harm. Service objectives require measured operating needs and are not yet defined. Initial critical conditions include unauthorized publication, failed removal propagation, evidence-integrity mismatch, repeated acquisition failure, and restore failure.

## Audit versus telemetry

Security and governance audit records are durable, access-controlled evidence of decisions. Operational telemetry is minimized and retained for a defined period. One MUST NOT silently substitute for the other.

## Current state

Local acquisition and replay attempts emit append-only safe records containing
stable identifiers, outcome, timing, fingerprints when available, rule
versions, validation state, and bounded failure codes. They exclude response
bodies, request URLs, local paths, and secrets. These records are local
prototype metadata, not a durable audit or telemetry service. The remote
adapter can add a 14-day package manifest and a durable
metadata-only issue receipt with one reminder timestamp and an explicit expiry
transition. The workflow code is present but has not yet emitted an operational
receipt. No telemetry stack, service objectives, dashboards, alerts, on-call
process, generalized audit store, or production environment exists.
