# Architecture

**Status:** Draft  
**Owner:** Maintainers  
**Last reviewed:** 2026-07-28

## Purpose

This document defines logical responsibilities and dependency direction. It does not select frameworks, databases, hosting, or vendors.

## Architectural style

IAgora begins as a modular monolith. Modules share one deployable boundary initially but MUST communicate through explicit typed contracts. A module may later be extracted only when measured scaling, isolation, ownership, or reliability needs justify the migration.

## Logical modules

1. **Source registry:** source identity, authority scope, rights, risk, and acquisition policy.
2. **Acquisition:** constrained retrieval and immutable source-artifact versions.
3. **Document processing:** safe parsing, fragment location, extraction candidates, and validation.
4. **Canonical knowledge:** entities, claims, assertions, evidence relationships, authority assessments, mappings, conflicts, and temporal versions.
5. **Methodology:** fulfillment, indicators, outcomes, and causal assessments.
6. **Governance:** contracts, provenance, lineage, quality, review, retention, redaction, and rights decisions.
7. **Publication:** Knowledge Passport projection and publication eligibility.
8. **Discovery:** lexical, structured, and optional semantic retrieval over publishable assets.
9. **Experience:** accessible editorial pages, exploration, visualization, and evidence-linked explanations.
10. **Operations:** identity, authorization, audit, monitoring, recovery, and incident response.

## Dependency direction

Source-specific connectors map inward to canonical contracts; canonical concepts never depend on portal-specific fields. Publication and AI features depend on governed knowledge records. They MUST NOT bypass canonical validation or write raw evidence as truth.

```text
sources -> acquisition -> processing -> canonical knowledge -> publication -> experiences
                 |             |              |                  |
                 +-------------+-- governance -+------------------+
```

## Data planes

- **Evidence plane:** immutable or governed raw versions and precise fragments.
- **Knowledge plane:** canonical, versioned assertions and relationships.
- **Assessment plane:** reproducible fulfillment, outcome, and impact evaluations.
- **Publication plane:** policy-filtered projections and accessible explanations.

## Current state

These boundaries are specified but not implemented. Physical deployment, persistence, messaging, caching, and model providers remain open.

## Related records

- [Architectural principles](05_ARCHITECTURAL_PRINCIPLES.md)
- [Data model](06_DATA_MODEL.md)
- [Data pipeline](08_DATA_PIPELINE.md)
- [ADR-0002](../adr/ADR-0002-canonical-assertion-and-evidence-model.md)
