# Canonical Data Dictionary

**Status:** Draft  
**Owner:** Maintainers  
**Last reviewed:** 2026-07-28

## Purpose

This dictionary maps canonical record names to their responsibility. Detailed semantics belong in the [glossary](../governance/22_GLOSSARY.md), accepted ADRs, and future field-level schemas.

| Record | Responsibility | Must not be confused with |
| --- | --- | --- |
| `Source` | Origin, publisher, custodian, or system identity | A claim or authority decision |
| `SourceArtifactVersion` | Exact acquired state of an artifact | A corrected canonical interpretation |
| `EvidenceFragment` | Precisely located evidence material | An assertion that the material is true |
| `ClaimRecord` | Attributable original statement and context | IAgora endorsement |
| `Assertion` | Atomic proposition under evaluation | Evidence or universal truth |
| `CampaignCommitment` | Campaign-era future undertaking | Later programme or delivery record |
| `EvidenceRelationship` | Support, contradiction, or context evaluation | Source authority |
| `AuthorityAssessment` | Fact- and scope-specific authority result | Evidence quality or popularity |
| `ConflictRecord` | Material incompatibility and review history | Any difference in values |
| `CommitmentMapping` | Reviewed link from promise to later public action | Text similarity |
| `FinancialObservation` | Amount at a defined accounting stage and scope | Generic “cost” |
| `FulfillmentAssessment` | Versioned method result at a cut-off | Political score or impact |
| `IndicatorDefinition` | Complete semantics of a measure | A display label |
| `OutcomeObservation` | Measured condition or change | Causal attribution |
| `ImpactAssessment` | Bounded causal or contribution conclusion | Chronological association |
| `KnowledgePassport` | Public projection of governance records | Independent truth store |

## Shared value-state rules

Contracts MUST distinguish `known`, `unknown`, `absent`, `not_applicable`, `restricted`, `conflicted`, and `not_verifiable`. They MUST distinguish event time, validity time, publication time, acquisition time, processing time, and observation cut-off.

## Extension rules

A source-specific field MAY map to a canonical record as an explicitly named extension. It MUST NOT redefine the canonical concept. New shared entities or meanings require specification review and, when long-lived or migration-heavy, an ADR.

## Current state

This is a logical dictionary. Field names, datatypes, identifiers, controlled vocabularies, and schemas remain to be implemented as versioned contracts.
