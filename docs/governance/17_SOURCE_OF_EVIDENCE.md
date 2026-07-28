# Source of Evidence

**Status:** Accepted  
**Owner:** Maintainers  
**Accepted:** 2026-07-28  
**Deciders:** Project maintainer  
**Last reviewed:** 2026-07-28

## Purpose

Evidence supports, contradicts, or contextualizes an assertion. It does not become authoritative merely by being numerous, official-looking, or semantically similar.

## Evidence unit

An `EvidenceFragment` MUST identify one acquired artifact version and the smallest practical inspectable location: page, paragraph, table cell or row, timestamp, region, or equivalent. It retains extraction method, language, structural context, review state, rights, and access constraints.

## Relationship contract

An `EvidenceRelationship` records fragment and assertion versions, relationship type, scope comparison, material rationale, method or rule version, reviewer or deterministic process, review time, uncertainty, and limitations.

Initial types are:

- `supports`: materially strengthens the exact assertion;
- `contradicts`: is materially incompatible after comparability checks;
- `contextualizes`: assists interpretation without directly supporting or contradicting.

## Comparison procedure

Before declaring contradiction, compare identity, territory, institution, time, record status, unit, denominator, granularity, accounting stage, and method. A resolved scope difference remains recorded but is not mislabeled as conflict.

## Citation requirements

A citation MUST resolve to the source, exact version, precise fragment, publication and acquisition context, and lawful access state. A document homepage is insufficient when a precise locator exists.

## Generated material

AI extraction or summary is a generated artifact and never evidence. It MAY point reviewers to candidate fragments; accepted evidence relationships require deterministic validation and applicable review.
