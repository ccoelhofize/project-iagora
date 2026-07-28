# Architect Playbook

**Status:** Accepted  
**Owner:** Maintainers  
**Accepted:** 2026-07-28  
**Deciders:** Project maintainer  
**Last reviewed:** 2026-07-28

## Purpose

This playbook describes how to turn an IAgora need into a reviewable change without bypassing evidence governance or prematurely selecting infrastructure.

## Working sequence

1. State the user question, public value, affected territory, period, and observation cut-off.
2. Identify the knowledge assets and canonical concepts involved.
3. Inventory primary sources, supporting evidence, contradictions, rights, and acquisition risks.
4. Apply accepted ADRs and identify unresolved material choices.
5. Define or update contracts at every changed boundary.
6. Model provenance, lineage, versioning, temporal validity, conflicts, and removal behavior.
7. Choose the simplest component boundary and technology that meets measured needs.
8. Define deterministic publication gates and proportional tests.
9. Review accessibility, privacy, security, licensing, and operating impact.
10. Update specifications and indexes before calling the change complete.

## Decision filter

Use an ADR for a long-lived change to a boundary, canonical entity, public method, security model, licence, or major dependency. Use an RFC when viable alternatives still need broad discussion. Keep reversible implementation details in the relevant specification.

## Required questions

Every design must answer:

- What is the exact assertion or decision the feature supports?
- Which source can establish each fact, and which evidence merely supports it?
- What raw object and fragment can another reviewer inspect?
- Which transformations, rules, models, and reviewers produced the output?
- How are time, territory, institution, unit, and granularity represented?
- What happens when sources disagree, disappear, or must be removed?
- What personal data, licence, security, accessibility, and retention constraints apply?
- What fails closed, and how can the change be rolled back?

## Architecture guardrails

- Prefer a modular monolith with explicit modules and typed contracts.
- Keep collectors source-specific and the canonical model source-agnostic.
- Treat remote content and generated output as untrusted.
- Preserve raw inputs; create new versions for corrections and interpretations.
- Keep deterministic validation responsible for enforceable rules.
- Do not add queues, distributed services, graph databases, vector stores, or AI providers without demonstrated need and documented trade-offs.

## Handoff checklist

Report what changed, the governing decision, validation performed, affected contracts, unresolved risks, and the next safe step. Clearly distinguish implemented behavior from draft design and planned work.

## Related records

- [Architecture](architecture/04_ARCHITECTURE.md)
- [Architectural principles](architecture/05_ARCHITECTURAL_PRINCIPLES.md)
- [ADR policy](adr/README.md)
- [Repository agent policy](../AGENTS.md)
