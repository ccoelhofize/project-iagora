# Canonical Data Model

**Status:** Draft  
**Owner:** Maintainers  
**Last reviewed:** 2026-07-28

## Purpose

This specification organizes the logical records accepted in ADR-0002. It does not select a database or freeze field-level schemas.

## Record groups

### Sources and evidence

- `Source` identifies an origin, publisher, or responsible system.
- `SourceArtifact` identifies a document, page, dataset, recording, or image.
- `SourceArtifactVersion` identifies one acquired state with fingerprint and rights metadata.
- `EvidenceFragment` identifies a precise page, paragraph, cell, row, timestamp, or region.
- `AcquisitionEvent` records how and when a version was obtained.

### Claims and knowledge

- `ClaimRecord` preserves attributable original wording and context.
- `Assertion` represents one atomic subject–predicate–value proposition with scope and epistemic kind.
- `CampaignCommitment` specializes an attributable future campaign statement.
- `EvidenceRelationship` qualifies a fragment as supporting, contradicting, or contextualizing an assertion.
- `AuthorityRule` and `AuthorityAssessment` determine fact-specific authority.
- `ConflictRecord` preserves unresolved or explained incompatibilities.

### Public-action chain

- `CommitmentComponent` represents an independently assessable part of a commitment.
- `CommitmentMapping` links it to decisions, resources, delivery, outcomes, or impact claims.
- `FinancialObservation` preserves amount, stage, period, institution, scope, and source.
- `Milestone` records evidenced progress without implying completion.
- `FulfillmentAssessment` preserves component states and the accepted summary method.

### Outcomes and impact

- `IndicatorDefinition` defines concept, formula, unit, population, territory, period, baseline, target provenance, and fitness.
- `MeasurementPlan` records the theory of change and evaluation design.
- `OutcomeObservation` records a measured value or change.
- `ImpactAssessment` records causal class, design, assumptions, estimate, uncertainty, robustness, and limits.

### Governance

- `TransformationEvent`, `ValidationEvent`, and `ReviewRecord` form lineage.
- `RetentionDecision`, `RestrictionDecision`, `RedactionRecord`, and `RemovalTombstone` govern evidence lifecycle.
- `KnowledgePassport` is a versioned projection, not a second truth store.

## Cross-cutting fields

Every applicable record requires stable identity, version, lifecycle state, creation and review time, temporal validity, territorial and institutional scope, provenance, lineage links, rights state, access class, and supersession relationships.

## Invariants

Original claims survive decomposition. Assertions do not prove themselves. Authority and evidence remain separate. Versions are appended, not overwritten. Assessment summaries retain atomic inputs. Generated artifacts are labeled and cannot serve as evidence.

## Open implementation choices

Identifier encoding, physical schemas, indexing, persistence, graph traversal, event storage, and partitioning require later contracts or ADRs if materially consequential.

## Related records

- [Canonical dictionary](07_CANONICAL_DATA_DICTIONARY.md)
- [Glossary](../governance/22_GLOSSARY.md)
- [ADR-0002](../adr/ADR-0002-canonical-assertion-and-evidence-model.md)
