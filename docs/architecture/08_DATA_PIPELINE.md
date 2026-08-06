# Data Pipeline

**Status:** Draft  
**Owner:** Maintainers  
**Last reviewed:** 2026-08-05

## Pipeline stages

1. **Register:** approve source purpose, scope, authority candidates, rights, retention, and risk profile.
2. **Acquire:** retrieve through constrained networking and record the acquisition event.
3. **Quarantine:** isolate untrusted bytes pending type, malware, size, archive, and parser checks.
4. **Preserve:** store the governed raw version read-only with fingerprint and lifecycle state.
5. **Parse:** create structural representations in an isolated, resource-limited environment.
6. **Extract:** produce fragments and candidate claims; AI output remains generated candidate data.
7. **Validate:** apply contracts, units, identifiers, scope, temporal, rights, privacy, and quality rules.
8. **Canonicalize:** map validated candidates to versioned source-agnostic entities and assertions.
9. **Relate:** evaluate authority, evidence, commitment mappings, and conflicts.
10. **Assess:** run accepted fulfillment or impact methods with explicit input versions.
11. **Review:** record required human and deterministic decisions.
12. **Publish:** create a schema-valid Knowledge Passport and promote only eligible assets.

## Processing rules

Every stage MUST be idempotent for the same input and rule version, record lineage, fail without silent coercion, and support replay from preserved inputs. Reprocessing creates a new derived version when rules or inputs change.

## Failure behavior

Network, parser, schema, authority, privacy, rights, security, and publication failures have distinct states. Failed or quarantined objects MUST NOT enter canonical, search, AI-retrieval, or public stores. Operators need actionable errors without sensitive payload leakage.

## Removal propagation

Restriction or removal events invalidate or rebuild affected fragments, assertions, indexes, caches, assessments, exports, and passports according to ADR-0007. Backups must not restore a removed object into active service.

## Current state

The local vertical slice implements bounded source registration, three manually captured constrained City API responses, exact preservation of their selected-field bytes, acquisition-event validation, deterministic raw-to-normalized comparison, canonical scope-preserving transformation, row-level evidence location, passport projection, and a fail-closed publication check. Increments 0–3 of [RFC-0001](../rfc/RFC-0001-portable-governed-source-acquisition.md) are implemented for one six-school plan: eight reusable acquisition contracts, deterministic historical compatibility projections, a registered Opendatasoft connector, constrained HTTPS transport, exact structural validation, append-only content-addressed local quarantine, offline replay, deduplication, safe attempt metadata, field-level change reports, a manually triggered read-only GitHub adapter, 14-day manifest-validated packages, metadata-only durable issue receipts, deterministic reminder and expiry transitions, and a separately protected admission workflow. Admission revalidates one exact non-expired candidate in a read-only job and, after environment approval, can only reject it or create a dedicated branch and draft pull request containing fixed evidence targets and an admission review. It cannot write directly to `main`, merge, canonicalize, publish, schedule acquisition, or contact a civic source. The acquisition and receipt path completed one [controlled remote exercise](../development/ACQUISITION.md#first-controlled-remote-exercise) with an exact-byte `unchanged` result; the pending-candidate monitor and admission path remain unexercised, and the required external admission environment is not configured. Tests continue to use retained or injected responses. The repository still does not implement sandboxed general parsing, managed shared persistence, civic-source scheduling, automated retry, restriction propagation, or production publication. RFC-0001 remains a draft proposal.

## Related records

- [Security](14_SECURITY.md)
- [Observability](15_OBSERVABILITY.md)
- [ADR-0007](../adr/ADR-0007-raw-evidence-retention-redaction-and-legal-removal.md)
- [ADR-0008](../adr/ADR-0008-public-source-acquisition-privacy-and-security-boundaries.md)
- [RFC-0001](../rfc/RFC-0001-portable-governed-source-acquisition.md)
