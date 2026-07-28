# Contributing

**Status:** Accepted  
**Owner:** Maintainers  
**Accepted:** 2026-07-28  
**Deciders:** Project maintainer  
**Last reviewed:** 2026-07-28

## Before contributing

Read the root [README](../../README.md), applicable [agent policy](../../AGENTS.md), [project intent](../00_PROJECT_INTENT.md), relevant specifications, and accepted [ADRs](../adr/ADR-INDEX.md). Repository documents and evidence take precedence over conversation history.

## Choose the right change

- Use a focused patch for local, reversible, contract-preserving work.
- Propose an ADR for a long-lived boundary, canonical entity, public method, security model, licence, or major dependency.
- Use an RFC when a cross-cutting proposal still needs alternatives and community discussion; the RFC workflow is not yet implemented.

## Contribution description

Explain the user problem, affected knowledge assets, sources or evidence, scope and observation time, contracts, architecture impact, privacy and security implications, licence and retention state, alternatives, validation, migration, and remaining uncertainty.

## Working rules

Preserve unrelated changes. Do not include secrets, unnecessary personal data, invented civic facts, or third-party material without rights metadata. Examples must be labeled real, illustrative, synthetic, or provisional. Update relevant documentation and indexes with the implementation.

## Review expectations

Review checks correctness, evidence and authority separation, canonical semantics, provenance and lineage, conflicts and time, accessibility, privacy, security, rights, retention, tests, migration, and operational impact.

High-impact public methodology, causal claims, licensing, privacy, security, production acquisition, publication, and destructive migration require the approval defined by accepted decisions.

## Contribution licensing

ADR-0009 accepts inbound-equals-outbound licensing for the target artifact. Exact repository licence notices and the contribution attestation process are not yet implemented. Do not submit work whose ownership or third-party rights are unclear.

## Git and release

Prefer focused commits that tell the architectural story. Do not rewrite shared history. A merged change is not automatically published, deployed, or released.
