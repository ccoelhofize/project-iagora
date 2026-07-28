# ADR-0002: Canonical Assertion and Evidence Model

**Status:** Accepted  
**Owner:** Maintainers  
**Proposed:** 2026-07-28  
**Accepted:** 2026-07-28  
**Deciders:** Project maintainer  
**Supersedes:** None  
**Superseded by:** None

## Context

[ADR-0001](ADR-0001-project-vision-and-pilot-boundary.md) establishes that IAgora must connect campaign commitments to public decisions, resources, delivery, outcomes, and defensible impact evidence. It also requires every material assertion and assessment to remain inspectable through its sources, evidence relationships, provenance, lineage, scope, method, and uncertainty.

The repository does not yet define the canonical structures needed to preserve those distinctions. A source document may state a commitment, a later deliberation may authorize an action, an open dataset may report delivery, and an analysis may calculate an outcome. These records may refer to the same subject without having the same authority, scope, meaning, or evidential role.

A model that stores only normalized “facts” would lose who stated them and why they are believed. A model that stores only documents would preserve origin but make cross-source comparison and commitment assessment difficult. A model that attaches a single truth or confidence score would conceal conflicts and mix authority, evidence quality, completeness, and interpretation.

The project needs a technology-neutral logical model before selecting a database schema, graph engine, search index, or API representation.

## Decision drivers

- Preserve source attribution and immutable raw evidence.
- Express atomic, comparable assertions without presenting them as self-proving facts.
- Keep source authority separate from evidential support.
- Connect campaign commitments to later public action without silently equating them.
- Preserve contradictory and differently scoped values.
- Distinguish source claims, observations, calculations, inferences, and generated explanations.
- Support temporal validity, supersession, and historical observation cut-offs.
- Make public assertions and assessments reproducible and precisely citable.
- Keep canonical concepts independent from source portals and implementation technology.
- Permit deterministic contract validation and manual methodological review.

## Decision

IAgora will use a typed logical knowledge graph composed of separate, versioned records. “Graph” describes the domain relationships; it does not select a graph database.

The canonical model will distinguish at least the following record types.

### Source identity

A `Source` identifies an origin of information, such as a public body, campaign organization, register, dataset, document collection, or information system.

It must preserve:

- stable canonical identifier;
- source type;
- publisher or responsible organization when known;
- territorial and institutional scope when applicable;
- canonical and observed source locations;
- applicable access and licensing metadata;
- version and supersession information.

A portal, publisher, and competent authority may be different entities and must not be silently merged.

### Source artifact and version

A `SourceArtifact` identifies a document, dataset, page, recording, image, or other published item. A `SourceArtifactVersion` represents the exact acquired state of that item.

Each acquired version must preserve:

- source and artifact identifiers;
- original location and retrieval result;
- publisher and publication date when known;
- acquisition event and acquisition time;
- media type, language, and content fingerprint;
- applicable licence, access, retention, and restriction information;
- relationship to earlier or later versions;
- raw bytes or a governed record explaining why they cannot be retained.

A correction or re-acquisition creates a new version. It must not overwrite the earlier acquired version.

### Evidence fragment

An `EvidenceFragment` identifies the smallest practical, inspectable portion of a source artifact version used in an evaluation. Depending on the medium, it may reference pages, paragraphs, table cells, rows, timestamps, regions, or byte ranges.

An evidence fragment must retain:

- its source artifact version;
- a stable fragment identifier within IAgora;
- precise source locator information;
- extracted content or representation when lawful;
- extraction method and version;
- language and relevant structural context;
- review state.

The fragment is evidence material, not an assertion of truth by IAgora.

### Claim record

A `ClaimRecord` preserves that an identified actor or source made a statement. It binds the original wording or representation to its speaker, publisher, artifact, fragment, publication context, and date.

A claim record may be decomposed into one or more canonical assertions. The original claim remains intact so decomposition does not erase wording, conditions, emphasis, or ambiguity.

### Canonical assertion

An `Assertion` is an atomic, versioned proposition expressed using canonical concepts. At minimum, it must identify:

- assertion identifier and version;
- subject;
- predicate or property;
- object, value, or referenced entity;
- datatype and unit when applicable;
- material qualifiers and conditions;
- territorial scope;
- temporal validity or relevant event time;
- epistemic kind;
- derivation or claim-record relationship;
- supersession state.

Initial epistemic kinds are:

- **source claim:** attributed content stated by a source;
- **reported observation:** a measurement or event reported by a source;
- **derived calculation:** a value produced from recorded inputs and a versioned formula;
- **methodological inference:** a reviewable conclusion produced under an explicit method;
- **editorial explanation:** explanatory wording that introduces no new factual assertion.

An assertion records what is being evaluated. Its existence does not establish that it is true, authoritative, current, or fit for use.

### Campaign commitment

A `CampaignCommitment` is a specialized, attributable claim record representing a future action or outcome proposed during a campaign. It must preserve:

- candidate, list, or authorized campaign actor;
- election and territory;
- primary campaign artifact and original wording;
- publication date and campaign context;
- conditions, deadline, target population, and quantified target when stated;
- decomposition into atomic commitment assertions;
- ambiguity, specificity, and primary-source verification state.

A later municipal programme, budget line, decision, or delivery record must not retroactively become the source of the campaign commitment.

### Evidence relationship

An `EvidenceRelationship` is a versioned evaluation connecting an evidence fragment to an assertion. Initial relationship types are:

- `supports`;
- `contradicts`;
- `contextualizes`.

It must preserve:

- evidence fragment and assertion versions;
- relationship type;
- scope comparison and material rationale;
- evaluation method or rule version;
- reviewer role or deterministic process;
- review time and state;
- uncertainty and limitations.

Evidence relationships are reviewable interpretations. They do not modify the evidence fragment or silently resolve conflicts.

### Authority assessment

An `AuthorityAssessment` records whether and why a source is competent to establish a particular fact type under a defined institutional, territorial, temporal, and publication scope.

It is separate from an evidence relationship. A source may be authoritative for an approved budget forecast but not for executed expenditure, programme impact, or the original wording of a campaign commitment.

The assessment must retain its governing rule, fact type, applicable scope, rationale, review state, and version. No source receives a universal authority rank.

### Commitment mapping

A `CommitmentMapping` connects an atomic campaign commitment assertion to later assertions concerning decisions, resources, outputs, outcomes, or impacts.

Initial mapping roles may include:

- `implements`;
- `partially_implements`;
- `changes_scope`;
- `replaces`;
- `contributes_to`;
- `reports_outcome_for`;
- `claims_impact_for`.

The exact role vocabulary remains subject to the fulfillment methodology ADR. Every mapping must preserve evidence, scope comparison, rationale, method version, review state, and uncertainty. Similar wording or a shared topic is insufficient by itself to establish implementation.

### Conflict record

A `ConflictRecord` groups assertions or evidence relationships that appear materially incompatible after unit, identity, territorial, temporal, and publication-scope checks.

It must preserve:

- participating record versions;
- the dimension of conflict;
- comparability checks performed;
- current resolution state;
- evidence and rationale for any later resolution;
- review history.

Resolved conflicts remain historically inspectable. A difference explained by scope should be recorded as such rather than mislabeled as a contradiction.

### Assessment

An `Assessment` is a derived, versioned knowledge asset produced under an explicit methodology, such as a future fulfillment assessment or impact assessment.

It must preserve:

- assessment type and subject;
- observation cut-off;
- method and rule version;
- input assertion, evidence, mapping, and conflict versions;
- result and component states;
- limitations and counterevidence;
- reviewer role and review record;
- supersession relationship.

An assessment must not overwrite its input assertions or replace them with a summary label.

### Provenance and lineage records

Acquisition, extraction, transformation, validation, and review events will be first-class lineage records. They must connect each derived or published object to its exact input versions and processing rules.

AI-generated extraction, classification, or explanation must be recorded as generated processing output. It must not create evidence or bypass deterministic validation and required review.

## Required invariants

The canonical model must enforce the following invariants at applicable publication boundaries:

1. Every source-derived published assertion cites at least one precise evidence fragment.
2. Every evidence fragment belongs to one immutable or governed source artifact version.
3. Claim wording and attribution remain available after canonical decomposition.
4. Authority assessments and evidence relationships remain separate records.
5. Assertions, evidence relationships, mappings, conflicts, and assessments are versioned rather than overwritten.
6. A later source does not silently rewrite an earlier observation cut-off.
7. Conflicting credible values remain accessible until and after governed resolution.
8. Scope differences are evaluated before a contradiction is asserted.
9. A campaign commitment is anchored to campaign evidence, not inferred solely from later public action.
10. A commitment mapping is explicit and reviewable; thematic similarity alone is insufficient.
11. A fulfillment or impact label retains its method, inputs, component states, counterevidence, and limitations.
12. Generated artifacts are labeled and never serve as evidence.
13. No global `truth`, `trust`, or opaque completion score replaces the model's separate dimensions.
14. Exceptional restriction, redaction, or deletion of raw evidence leaves an auditable governed record to the extent lawfully possible.

## Scope

### Included

- Logical identities, record responsibilities, and relationships required for the pilot.
- Assertion atomicity and epistemic-kind separation.
- Source artifact versioning and precise evidence fragments.
- Evidence relationships, authority assessments, commitment mappings, conflicts, and derived assessments.
- Provenance, lineage, temporal validity, and supersession invariants.
- Publication-boundary requirements.

### Excluded

- Physical database, graph, search, or storage technology.
- Identifier encoding such as UUID, ULID, or URI format.
- Complete field-level schemas and API payloads.
- Exact fulfillment-status thresholds and aggregation rules.
- Exact impact-evaluation design and causal method.
- Source-authority rules for each civic fact type.
- French public-accounting contract details.
- User-interface design.
- Retention periods and legal-removal procedure.

These excluded decisions require specifications or later ADRs.

## Consequences

### Benefits

- Source statements and IAgora interpretations cannot be silently conflated.
- Multiple sources can support or contradict the same canonical proposition while retaining attribution.
- Campaign commitments remain linked to their original wording and can be compared with later public action.
- Historical versions, observation cut-offs, and conflicts remain inspectable.
- Fulfillment and impact assessments can expose their components instead of publishing opaque scores.
- The logical model can be implemented in a relational, document, graph, or hybrid architecture.
- Deterministic contracts can validate high-risk publication invariants.

### Drawbacks and risks

- The model contains more record types and relationships than a conventional fact table.
- Atomic decomposition and mapping require methodological judgment and review effort.
- Source fragments need medium-specific locators and version handling.
- Canonical identity resolution may produce false merges or duplicates if rules are weak.
- Excessive granularity could make ingestion and public explanation expensive.
- A technology-neutral logical graph still requires careful mapping to a physical store.
- Review workflows and permissions are not yet defined.

### Follow-up work

- Create the canonical data model specification and field-level dictionary.
- Define machine-validatable contracts for the pilot record types.
- Propose the campaign commitment decomposition and fulfillment methodology.
- Propose Source of Truth authority rules by fact type.
- Specify conflict detection, comparison, and resolution behavior.
- Specify outcome indicators and causal impact requirements.
- Define stable identifier and entity-resolution rules.
- Define review roles, permissions, corrections, and appeals.
- Define Knowledge Passport projection from the canonical records.
- Test the model against the pilot campaign artifact and three school-level evidence chains.

## Alternatives considered

### Alternative A: Document-centric annotations only

Store source documents and attach annotations without a canonical assertion layer. This minimizes normalization and preserves context well, but makes cross-source comparison, conflict detection, and commitment-to-action mapping difficult. Repeated concepts would be rediscovered independently in each document.

This alternative is not proposed because the product requires comparison and traceability across heterogeneous sources.

### Alternative B: Single canonical fact table with truth status

Store normalized subject-predicate-value facts with source identifiers and a status or confidence score. This is simple to query and explain technically, but it collapses attribution, authority, evidential role, conflict, and interpretation into one record or score.

This alternative is rejected because it violates the accepted separation of evidence, authority, uncertainty, and generated interpretation.

### Alternative C: Select a property-graph database now

Implement every source, claim, assertion, and evidence relationship as graph nodes and edges in a dedicated graph database. This is expressive for traversal but prematurely selects infrastructure before query patterns, scale, contracts, and operating constraints are measured.

This alternative is deferred. A graph database may later implement part of the logical model if evidence justifies it.

### Alternative D: Typed logical graph with separate versioned records

Define domain responsibilities and invariants independently from physical storage. This adds conceptual structure now while preserving implementation choice and the ability to validate contracts deterministically.

This is the proposed alternative.

## Migration and rollback

No production schema or stored pilot corpus currently exists, so accepting this ADR would require no data migration.

A change that merges record responsibilities, removes required provenance, changes assertion identity, or weakens an invariant requires a superseding ADR and a migration plan.

If pilot modeling shows that a record type is unnecessary, a later ADR may simplify the model while documenting how existing identifiers, lineage, and public contracts migrate.

## Validation

Before this decision is considered implemented:

- a field-level draft model represents every required record type and relationship;
- a campaign artifact can be preserved, cited, decomposed, and mapped without losing original wording;
- the same canonical assertion can receive evidence from multiple attributed sources;
- differing units, dates, territories, and publication scopes can be detected before declaring conflict;
- an authority assessment can change without altering raw evidence or its evidence relationships;
- a corrected source creates a new artifact version and preserves the earlier state;
- a historical assessment can be reproduced using its original observation cut-off and input versions;
- a generated extraction remains distinguishable from evidence and reviewed canonical data;
- contracts reject a published source-derived assertion without a precise evidence fragment;
- contracts reject a fulfillment or impact assessment without a method version and input lineage;
- representative pilot examples pass manual review for traceability and plain-language explainability;
- no test requires a physical database choice not established by a later decision.

## Governance and evidence impact

- The glossary remains the vocabulary source; a later normative data-model specification will define exact fields and constraints.
- Source authority is modeled explicitly but its fact-type rules remain a separate decision.
- Evidence relationships and commitment mappings require inspectable rationale and review state.
- Conflicts are first-class records and cannot be resolved by deletion.
- Fulfillment and impact assessments remain derived knowledge assets rather than evidence.
- Raw evidence and original campaign wording remain immutable in normal operation.
- AI may propose extraction or mappings but cannot supply their evidence or final methodological authority.
- Knowledge Passports will project, not duplicate or replace, the canonical records.

## Related records

- Accepted vision and pilot decision: [`ADR-0001`](ADR-0001-project-vision-and-pilot-boundary.md)
- Product scope: [`../vision/02_PRODUCT_SCOPE.md`](../vision/02_PRODUCT_SCOPE.md)
- Glossary: [`../governance/22_GLOSSARY.md`](../governance/22_GLOSSARY.md)
- Data model specification: Planned
- Data contracts: Planned
- Related ADRs: ADR-0001
- RFCs or issues: None

## Decision record

- Outcome: Accepted
- Decision date: 2026-07-28
- Deciders: Project maintainer
- Rationale for outcome: Preserve source attribution, canonical assertion comparability, evidence relationships, authority assessments, commitment mappings, conflicts, and derived assessments as separate versioned records without selecting physical storage technology.

## Revision notes

- 2026-07-28: Accepted by the project maintainer.
