# Architectural Principles

**Status:** Draft  
**Owner:** Maintainers  
**Last reviewed:** 2026-07-28

## Normative principles

1. **Evidence is addressable.** Every source-derived public assertion MUST cite an inspectable evidence fragment.
2. **Authority is fact-specific.** Publisher prestige MUST NOT become a universal source ranking.
3. **Raw and derived records are separate.** Corrections and interpretations create new versions.
4. **Lineage is part of the output.** A derived value without inputs and transformation version is incomplete.
5. **Conflicts remain modeled.** Differences are checked for scope before contradiction and never silently discarded.
6. **Time is explicit.** Event, validity, publication, acquisition, processing, and observation-cut-off times remain distinct.
7. **Canon is source-agnostic.** Connectors adapt to shared concepts, not the reverse.
8. **Publication fails closed.** Missing contracts, rights, privacy, security, evidence, or review states block promotion.
9. **AI is constrained processing.** It MAY propose; deterministic rules and required review decide publication.
10. **Accessibility is correctness.** Human-readable views MUST preserve the material meaning of machine-readable records.
11. **Privacy and security start at acquisition.** Public content remains untrusted and purpose limitation applies.
12. **Simplicity precedes scale.** Use the smallest reversible architecture that satisfies measured requirements.

## Design implications

- Prefer explicit schemas, stable identifiers, idempotent operations, and append-only history.
- Keep public summaries linked to atomic records and methodology versions.
- Separate storage concerns from domain semantics.
- Make exceptional deletion visible through lawful minimal tombstones and downstream invalidation.
- Measure operational needs before adding distributed infrastructure.

## Change policy

A change that alters one of these invariants requires an ADR. Implementations MAY vary behind stable contracts, provided evidence, lineage, temporal, security, rights, and accessibility behavior remains equivalent.

## Related records

- [Architecture](04_ARCHITECTURE.md)
- [Architect playbook](../01_ARCHITECT_PLAYBOOK.md)
- [ADR index](../adr/ADR-INDEX.md)
