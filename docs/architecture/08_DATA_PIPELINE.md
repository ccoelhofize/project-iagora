# Data Pipeline

**Status:** Draft  
**Owner:** Maintainers  
**Last reviewed:** 2026-08-03

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

The local vertical slice implements bounded source registration, three manually captured constrained City API responses, exact preservation of their selected-field bytes, acquisition-event validation, deterministic raw-to-normalized comparison, canonical scope-preserving transformation, row-level evidence location, passport projection, and a fail-closed publication check. Increment 0 of [RFC-0001](../rfc/RFC-0001-portable-governed-source-acquisition.md) is now partially implemented: five generalized acquisition and admission contracts, one bounded six-school plan, one explicitly synthetic admission-review fixture, and deterministic compatibility projections for the three historical acquisitions are executable. The projections expose missing historical plan, rule-version, timing, package, and review metadata rather than inventing it. The repository still does not implement reusable network acquisition, a connector, quarantine, sandboxed parsing, managed persistence, GitHub acquisition or admission workflows, scheduling, retry, restriction propagation, or production publication. RFC-0001 remains a draft proposal.

## Related records

- [Security](14_SECURITY.md)
- [Observability](15_OBSERVABILITY.md)
- [ADR-0007](../adr/ADR-0007-raw-evidence-retention-redaction-and-legal-removal.md)
- [ADR-0008](../adr/ADR-0008-public-source-acquisition-privacy-and-security-boundaries.md)
- [RFC-0001](../rfc/RFC-0001-portable-governed-source-acquisition.md)
