# Architecture Decision Record Policy

**Status:** Draft  
**Owner:** Maintainers  
**Last reviewed:** 2026-07-27

## Purpose

Architecture Decision Records preserve significant Project IAgora decisions, their context, trade-offs, and consequences. They allow contributors to determine what was decided, by whom, under which assumptions, and what later replaced it.

An ADR records a decision. A specification defines the resulting rules or contract. Neither should silently substitute for the other.

## When an ADR is required

Create or propose an ADR when a choice:

- changes a system boundary or canonical entity;
- establishes or changes a governance or public methodology rule;
- creates or changes a public contract or schema with compatibility consequences;
- selects a major dependency or infrastructure direction;
- establishes a security, privacy, retention, or identity model;
- has long-lived consequences or material migration cost;
- resolves disagreement between credible architectural alternatives;
- supersedes an accepted ADR.

Routine implementation details that are local, reversible, and contract-preserving do not require an ADR.

## ADR versus RFC

Use an RFC before a decision when the problem is broad, cross-cutting, still requires community exploration, or cannot yet be reduced to a concrete choice. An ADR may close an RFC by recording the accepted decision.

The repository does not yet define an RFC workflow. Until it does, substantial unresolved proposals must remain explicitly marked as drafts and must not be presented as accepted decisions.

## Status lifecycle

Every ADR uses one of these statuses:

- **Proposed:** complete enough for review but not yet authoritative;
- **Accepted:** explicitly approved by the recorded deciders;
- **Rejected:** considered but not selected;
- **Superseded:** replaced by a later accepted ADR, with reciprocal links;
- **Deprecated:** still part of history but no longer recommended, without a complete replacement.

An ADR must not be marked `Accepted` merely because its implementation exists or because no reviewer objected.

## Decision authority

Until project governance assigns more specific roles, maintainers are the decision authority. Acceptance must record the deciding role or named deciders and an acceptance date.

An ADR cannot grant itself authority to accept its own decision. Decisions that materially change public methodology, legal posture, privacy, licensing, cost, or external publication require explicit maintainer approval before acceptance or implementation.

## Workflow

1. Confirm that the decision is not already covered by an accepted ADR.
2. Identify affected users, knowledge assets, specifications, contracts, and prior decisions.
3. Create the next available ADR number from `ADR-INDEX.md` using the template.
4. Set the status to `Proposed` and describe viable alternatives fairly.
5. Review evidence, risks, migration impact, governance impact, and validation criteria.
6. Record the explicit decision outcome and update `ADR-INDEX.md`.
7. Update affected specifications and `docs/99_ARCHITECTURE_INDEX.md`.
8. Validate that implementation, tests, contracts, and documentation agree with the accepted decision.

## File rules

- File names use `ADR-NNNN-short-kebab-case-title.md`.
- Numbers are four digits, allocated sequentially, and never reused.
- Accepted ADR history must not be rewritten to make a later choice appear original.
- Clarifications that do not change the decision may be appended with a dated note.
- A material change requires a new ADR that supersedes the earlier record.
- Superseded ADRs remain in the repository.
- Every lifecycle change updates `ADR-INDEX.md` and reciprocal supersession links.

## Required content

Every ADR contains at least:

- identifier and title;
- status, owner, dates, and deciders;
- context and decision drivers;
- decision and its scope;
- consequences, including drawbacks;
- alternatives considered;
- migration or rollback impact when applicable;
- validation approach;
- governance and evidence implications;
- related specifications, ADRs, and supersession links.

Use [`ADR-TEMPLATE.md`](ADR-TEMPLATE.md) for new records and register every ADR in [`ADR-INDEX.md`](ADR-INDEX.md).
