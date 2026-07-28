# ADR-0006: Minimum Knowledge Passport Contract

**Status:** Accepted  
**Owner:** Maintainers  
**Proposed:** 2026-07-28  
**Accepted:** 2026-07-28  
**Deciders:** Project maintainer  
**Supersedes:** None  
**Superseded by:** None

## Context

[ADR-0001](ADR-0001-project-vision-and-pilot-boundary.md) requires a versioned Knowledge Passport for the pilot. [ADR-0002](ADR-0002-canonical-assertion-and-evidence-model.md) establishes separate assertions, evidence relationships, provenance, lineage, conflicts, and assessments. [ADR-0003](ADR-0003-fact-specific-source-of-truth-rules.md) makes authority fact-specific. [ADR-0004](ADR-0004-campaign-commitment-fulfillment.md) and [ADR-0005](ADR-0005-outcome-measurement-and-causal-impact.md) require public explanations for fulfillment, outcomes, and causal claims.

The repository defines a Knowledge Passport in the glossary but does not yet establish its minimum contract. Without one, interfaces could expose different metadata, omit material limitations, or duplicate governance records into an inconsistent second truth store.

The passport must be useful to citizens while remaining precise enough for machines and independent reviewers. Not every field applies to every asset, so the contract also needs explicit conditional requirements rather than meaningless empty values.

## Decision drivers

- Let a reader inspect what an asset says, where it came from, how it was produced, and what remains uncertain.
- Preserve one canonical governance record while supporting multiple presentations.
- Require precise evidence, authority, lineage, conflict, temporal, review, and rights information.
- Support assertions, commitments, indicators, datasets, assessments, and generated explanations without one oversized entity.
- Prevent opaque trust or confidence scores from replacing inspectable dimensions.
- Provide stable identity, versioning, accessibility, and deterministic validation.
- Permit lawful restriction without concealing that material information is unavailable.

## Decision

IAgora will define the Knowledge Passport as a **versioned projection of canonical governance records**, not as a separate source of truth. Each public knowledge asset must expose a machine-readable passport and an equivalent accessible human-readable view.

### Passport identity and version

Every passport must include:

- a stable passport identifier;
- the knowledge-asset identifier, type, and version represented;
- the passport contract version;
- creation and last-review timestamps;
- current lifecycle state;
- links to prior, superseding, or corrected versions;
- a content fingerprint or equivalent integrity reference where lawful and useful;
- the responsible owner role and review state.

A passport is a snapshot. Later evidence, corrections, or method changes create a new version and do not rewrite the earlier public state.

### Core profile

Every public passport must expose, directly or through stable references:

1. **Identity and definition:** canonical name, plain-language description, asset type, applicable definition, and semantic version.
2. **Scope:** subject, territory, institution, population, unit, period, temporal validity, publication time, and observation cut-off when applicable.
3. **Assertion content:** the atomic statement or analytical result represented, its attributable speaker or publisher when it is a claim, and its classification as observed fact, official claim, calculation, inference, editorial explanation, or generated content.
4. **Authority:** the fact type, applicable Source of Truth rule, selected authoritative source or unresolved authority state, scope match, and rationale.
5. **Evidence:** precise supporting, contradictory, and contextual evidence relationships, including source versions and locations.
6. **Provenance:** publisher or supplier, source location, acquisition event, acquisition method and time, and relevant licence or access information.
7. **Lineage:** raw inputs, transformations, validation results, rule or software versions, material parameters, and output links.
8. **Quality and fitness:** applicable quality dimensions, validation failures, intended and excluded uses, and known limitations.
9. **Conflicts and uncertainty:** unresolved conflicts, missing evidence, ambiguity, measurement or method limitations, and a plain-language effect on interpretation.
10. **Rights and safeguards:** licence status, reuse restrictions, access class, retention class, privacy classification, and any public redaction or withdrawal state.
11. **Review and correction:** method version, reviewer role, decision and time, correction channel, and challenge or appeal state when applicable.
12. **Accessibility:** a plain-language summary and non-visual equivalents for material graphical information.

Fields that do not apply must be explicitly marked `not applicable` with a contract-defined reason. Unknown, absent, restricted, and not applicable are distinct states.

### Assessment extension

A fulfillment, outcome, or impact passport must additionally expose:

- the original commitment and decomposition version when relevant;
- component implementation states and fulfillment rule version;
- indicator, baseline, target, formula, unit, population, territory, and time horizon;
- observed value or effect estimate with uncertainty;
- causal-claim class, evaluation design, counterfactual strategy, assumptions, and robustness limits;
- the relationship among commitment, decisions, resources, delivery, outcome, and claimed impact;
- generalization limits and material adverse, null, or inconclusive results.

These fields reference the records governed by ADR-0004 and ADR-0005; they do not reproduce editorial reasoning as unstructured text only.

### Generated-content extension

When the asset contains persisted AI-generated material, the passport must identify:

- that generated content is not evidence;
- the generation purpose and output type;
- model and instruction or prompt versions;
- input asset versions and cited evidence fragments;
- deterministic validations and human review state;
- known generation limitations and the correction path.

Private model reasoning must not be exposed or treated as proof.

### Disclosure profiles

The same canonical passport may have internal and public disclosure profiles. A public profile may omit or generalize information only for a documented legal, privacy, safety, security, or contractual reason.

The public passport must disclose that a field is restricted and give a non-sensitive reason code when doing so is lawful. Redaction must not silently change the meaning of the represented assertion. If safe publication would be materially misleading, the asset must not be published.

### Validation and transport

The normative Knowledge Passport specification must define:

- a machine-readable, versioned schema;
- deterministic required-field and cross-reference validation;
- controlled vocabularies and extension rules;
- compatibility and deprecation policy;
- JSON as the initial interchange representation unless implementation evidence supports another choice;
- an accessible HTML representation with equivalent material content;
- citation precision and resolvability checks;
- validation behavior for restricted, missing, unknown, and not-applicable fields.

No single composite trust, confidence, quality, fulfillment, or impact score is part of the minimum contract.

## Required invariants

1. A passport projects canonical records and cannot become a competing truth store.
2. Every public knowledge asset has a stable, versioned passport.
3. Asset time, validity, publication time, acquisition time, and observation cut-off remain distinguishable.
4. Source authority remains separate from supporting evidence and data quality.
5. Supporting, contradictory, and contextual evidence remain separately inspectable.
6. Raw inputs and every material transformation remain reachable through lineage, subject to governed restrictions.
7. Unknown, absent, restricted, and not applicable never collapse into one value.
8. Corrections create versions and preserve historical state unless lawful removal requires otherwise.
9. Generated content is labeled and never presented as evidence.
10. Public and machine-readable views convey equivalent material meaning.
11. Opaque composite scores cannot replace the required dimensions.

## Scope

### Included

- The logical minimum contract and conditional extensions.
- Identity, versioning, disclosure profiles, validation, and accessible representation.
- Passports for public knowledge assets and analytical assessments.

### Excluded

- Field-level JSON Schema, API routes, storage technology, or user-interface design.
- A universal scoring method.
- Final retention, redaction, security, privacy, or licence rules, which are addressed by ADR-0007 through ADR-0009.
- A requirement to publish an asset that cannot lawfully or safely be disclosed.

## Consequences

### Benefits

- Citizens and reviewers receive a consistent explanation of provenance, evidence, method, and limits.
- Interfaces can evolve without duplicating canonical governance state.
- Conditional extensions keep simple assets understandable while preserving analytical rigor.
- Deterministic validation makes omissions visible before publication.

### Drawbacks and risks

- Complete passports add ingestion, review, and interface work.
- Cross-record projections may be slow or incomplete until canonical contracts stabilize.
- A broad minimum can become bureaucratic if conditionality and plain-language design are poor.
- Public restriction reasons may themselves require security or privacy review.

### Follow-up work

- Create the normative Knowledge Passport specification and schema.
- Define controlled vocabularies, conformance examples, and compatibility rules.
- Prototype the core and assessment profiles on the “Respire à la récré” pilot.
- Test completeness, citation resolution, accessibility, correction, and restricted-field behavior.

## Alternatives considered

### Alternative A: Narrative passport pages without a contract

This would be quick and flexible but could not guarantee equivalent content across pages, APIs, and versions. Omissions would be hard to detect.

### Alternative B: Store a complete independent passport document

This could make retrieval simple but would duplicate canonical evidence and governance state. Synchronization errors could make the passport contradict the records it summarizes.

### Alternative C: Use one universal trust score

A headline score would be compact but would collapse authority, evidence, quality, uncertainty, method, and rights into an opaque judgment. It is incompatible with accepted principles.

### Alternative D: Versioned projection with core and conditional extensions

This is the selected approach. It preserves one canonical record, supports different asset types, and keeps public explanations inspectable at the cost of stronger contract and validation work.

## Migration and rollback

No implementation exists. Before public release, prototype schemas may change with explicit version increments. Once a passport contract is public, incompatible changes require a new major version and a documented migration window. A failed projection can be rebuilt from canonical records; it must never modify raw evidence.

## Validation

The decision is correctly implemented when:

- every published pilot asset references a schema-valid passport;
- every passport resolves to the exact asset and versions it describes;
- required authority, evidence, provenance, lineage, conflict, uncertainty, rights, and review states are present or carry valid explicit absence states;
- public and machine-readable views pass semantic equivalence and accessibility review;
- correction and supersession tests preserve historical versions;
- generated-content tests prevent AI output from being classified as evidence;
- no composite score can satisfy or bypass component requirements.

## Governance and evidence impact

The passport becomes the public inspection surface for accepted governance records. It does not change source authority, evidence, or assessment methods. Retention, restriction, removal, privacy, security, and licence states remain governed by their dedicated decisions and specifications.

## Related records

- Specifications: [`../governance/22_GLOSSARY.md`](../governance/22_GLOSSARY.md), [`../governance/23_KNOWLEDGE_PASSPORT.md`](../governance/23_KNOWLEDGE_PASSPORT.md)
- Contracts: Planned Knowledge Passport schema
- Related ADRs: [ADR-0001](ADR-0001-project-vision-and-pilot-boundary.md), [ADR-0002](ADR-0002-canonical-assertion-and-evidence-model.md), [ADR-0003](ADR-0003-fact-specific-source-of-truth-rules.md), [ADR-0004](ADR-0004-campaign-commitment-fulfillment.md), [ADR-0005](ADR-0005-outcome-measurement-and-causal-impact.md), [ADR-0007](ADR-0007-raw-evidence-retention-redaction-and-legal-removal.md), [ADR-0008](ADR-0008-public-source-acquisition-privacy-and-security-boundaries.md), [ADR-0009](ADR-0009-project-licensing-policy.md)
- RFCs or issues: None

## Decision record

- Outcome: Accepted
- Decision date: 2026-07-28
- Deciders: Project maintainer
- Rationale for outcome: The versioned projection preserves a single canonical governance record while giving citizens and machines a consistent, inspectable explanation of evidence, authority, lineage, uncertainty, rights, and review.

## Revision notes

- 2026-07-28: Linked the newly created draft Knowledge Passport specification. No decision semantics changed.
