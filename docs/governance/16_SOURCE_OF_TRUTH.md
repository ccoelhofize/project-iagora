# Source of Truth

**Status:** Accepted  
**Owner:** Maintainers  
**Accepted:** 2026-07-28  
**Deciders:** Project maintainer  
**Last reviewed:** 2026-07-28

## Purpose

This specification operationalizes [ADR-0003](../adr/ADR-0003-fact-specific-source-of-truth-rules.md). Source of Truth means the strongest applicable authority for one fact and scope; it is not a universal publisher rank or guarantee of correctness.

## Authority rule contract

Each versioned rule MUST define fact type, required competence, territory, institution, temporal scope, record status, finality, granularity, identifiers, admissible source classes, co-authority, fallback, conflict escalation, validation, and review.

## Assessment procedure

1. Define the exact fact, scope, time, unit, and granularity.
2. Identify candidate sources and artifact versions.
3. Check competence, authenticity, status, territory, institution, time, semantics, granularity, version, and method accessibility.
4. Apply the governing rule and record the rationale.
5. Produce `authoritative`, `co_authoritative`, `authoritative_with_limitation`, `not_authoritative`, or `undetermined`.
6. Preserve contrary evidence and escalate material unresolved conflicts.

## Pilot patterns

The original authenticated campaign artifact governs original campaign wording. A competent adopted act governs what was legally decided. Budget authorization and executed expenditure require records authoritative for their respective accounting stages. Delivery may require competent completion records and corroborating site-level evidence. No publisher is authoritative for causal impact by status alone.

## Fallback behavior

If the expected authoritative record is unavailable, IAgora MAY use attributed evidence to describe what another source reports but MUST mark authority `undetermined` or limited. It MUST NOT silently promote media, press releases, or AI output to Source of Truth.

## Publication requirements

Every material public assertion identifies its fact type, authority-rule version, assessment outcome, selected source versions, limitations, reviewer state, and unresolved authority conflicts in its Knowledge Passport.
