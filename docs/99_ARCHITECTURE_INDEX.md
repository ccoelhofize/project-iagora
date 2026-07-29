# Architecture and Governance Index

**Status:** Draft  
**Owner:** Maintainers  
**Last reviewed:** 2026-07-29

## Purpose

This index distinguishes documents and accepted decisions from executable capabilities. Every target document is now present, but draft specifications are not accepted decisions and no described service should be treated as implemented without code, contracts, tests, and operating evidence.

## Status legend

- **Draft:** present and under review; not authoritative by itself.
- **Accepted:** explicitly approved through the applicable governance process.
- **Planned capability:** described but not implemented.
- **Superseded:** retained for history but replaced by another accepted record.

## Project and vision

| Document | State | Role |
| --- | --- | --- |
| [`../README.md`](../README.md) | Present, acceptance not recorded | Repository entry point |
| [`../AGENTS.md`](../AGENTS.md) | Present, acceptance not recorded | AI-agent working policy |
| [`00_PROJECT_INTENT.md`](00_PROJECT_INTENT.md) | Accepted | Concise product intent and current reality |
| [`01_ARCHITECT_PLAYBOOK.md`](01_ARCHITECT_PLAYBOOK.md) | Accepted | Design and decision workflow |
| [`vision/00_VISION.md`](vision/00_VISION.md) | Draft | Mission, users, outcomes, and boundaries |
| [`vision/01_MANIFESTO.md`](vision/01_MANIFESTO.md) | Accepted | Public-interest commitments and values |
| [`vision/02_PRODUCT_SCOPE.md`](vision/02_PRODUCT_SCOPE.md) | Accepted | “Respire à la récré” POC scope and confirmed case studies |
| [`vision/03_ROADMAP.md`](vision/03_ROADMAP.md) | Draft | Outcome-based strategic sequence |

## Architecture specifications

| Document | State | Role |
| --- | --- | --- |
| [`architecture/04_ARCHITECTURE.md`](architecture/04_ARCHITECTURE.md) | Draft | Logical modules, boundaries, and dependency direction |
| [`architecture/05_ARCHITECTURAL_PRINCIPLES.md`](architecture/05_ARCHITECTURAL_PRINCIPLES.md) | Draft | Cross-cutting design invariants |
| [`architecture/06_DATA_MODEL.md`](architecture/06_DATA_MODEL.md) | Draft | Logical canonical records and relationships |
| [`architecture/07_CANONICAL_DATA_DICTIONARY.md`](architecture/07_CANONICAL_DATA_DICTIONARY.md) | Draft | Record responsibilities and semantic distinctions |
| [`architecture/08_DATA_PIPELINE.md`](architecture/08_DATA_PIPELINE.md) | Draft | Acquisition-to-publication stages and failure behavior |
| [`architecture/09_BACKEND.md`](architecture/09_BACKEND.md) | Draft | Backend module and service boundaries |
| [`architecture/10_API.md`](architecture/10_API.md) | Draft | Public and internal API contract principles |
| [`architecture/11_FRONTEND.md`](architecture/11_FRONTEND.md) | Draft | Accessible public information architecture |
| [`architecture/12_AI_ENGINE.md`](architecture/12_AI_ENGINE.md) | Draft | Evidence-constrained AI responsibilities |
| [`architecture/13_SEARCH_ENGINE.md`](architecture/13_SEARCH_ENGINE.md) | Draft | Governed discovery and index lifecycle |
| [`architecture/14_SECURITY.md`](architecture/14_SECURITY.md) | Draft | Trust boundaries and required controls |
| [`architecture/15_OBSERVABILITY.md`](architecture/15_OBSERVABILITY.md) | Draft | Operational, governance, and audit signals |

## Governance specifications

| Document | State | Role |
| --- | --- | --- |
| [`governance/16_SOURCE_OF_TRUTH.md`](governance/16_SOURCE_OF_TRUTH.md) | Accepted | Fact-specific authority rules and assessment |
| [`governance/17_SOURCE_OF_EVIDENCE.md`](governance/17_SOURCE_OF_EVIDENCE.md) | Accepted | Evidence fragments, relationships, and citation |
| [`governance/18_DATA_CONTRACTS.md`](governance/18_DATA_CONTRACTS.md) | Draft | Shared contract and compatibility requirements |
| [`governance/19_DATA_LINEAGE.md`](governance/19_DATA_LINEAGE.md) | Draft | Transformation history, replay, and invalidation |
| [`governance/20_DATA_QUALITY.md`](governance/20_DATA_QUALITY.md) | Draft | Fitness-for-use dimensions and assessment |
| [`governance/21_DATA_PROVENANCE.md`](governance/21_DATA_PROVENANCE.md) | Draft | Origin, acquisition, rights, and custody |
| [`governance/22_GLOSSARY.md`](governance/22_GLOSSARY.md) | Draft | Canonical working vocabulary |
| [`governance/23_KNOWLEDGE_PASSPORT.md`](governance/23_KNOWLEDGE_PASSPORT.md) | Draft | Public governance projection contract |
| [`governance/24_PILOT_SOURCE_INVENTORY.md`](governance/24_PILOT_SOURCE_INVENTORY.md) | Active inventory | Verified, missing, limited, and approved POC sources |

## Decision records

The [ADR policy](adr/README.md), [index](adr/ADR-INDEX.md), and [template](adr/ADR-TEMPLATE.md) are present as drafts. The following decisions are accepted:

| ADR | Decision |
| --- | --- |
| [ADR-0001](adr/ADR-0001-project-vision-and-pilot-boundary.md) | Project vision and initial pilot boundary |
| [ADR-0002](adr/ADR-0002-canonical-assertion-and-evidence-model.md) | Canonical assertion and evidence model |
| [ADR-0003](adr/ADR-0003-fact-specific-source-of-truth-rules.md) | Fact-specific Source of Truth rules |
| [ADR-0004](adr/ADR-0004-campaign-commitment-fulfillment.md) | Campaign commitment decomposition and fulfillment |
| [ADR-0005](adr/ADR-0005-outcome-measurement-and-causal-impact.md) | Outcome measurement and causal impact attribution |
| [ADR-0006](adr/ADR-0006-minimum-knowledge-passport-contract.md) | Minimum Knowledge Passport contract |
| [ADR-0007](adr/ADR-0007-raw-evidence-retention-redaction-and-legal-removal.md) | Raw-evidence retention, redaction, and legal removal |
| [ADR-0008](adr/ADR-0008-public-source-acquisition-privacy-and-security-boundaries.md) | Public-source privacy and security boundaries |
| [ADR-0009](adr/ADR-0009-project-licensing-policy.md) | Project licensing policy |

Detailed evidence-conflict comparison and resolution behavior still requires a normative field-level specification. A new ADR is necessary only if that work changes an accepted invariant or selects a material architectural alternative.

## Development guides

| Document | State | Role |
| --- | --- | --- |
| [`development/CONTRIBUTING.md`](development/CONTRIBUTING.md) | Accepted | Contribution scope, review, and licensing expectations |
| [`development/CODING_STANDARDS.md`](development/CODING_STANDARDS.md) | Draft | Implementation-neutral coding standards |
| [`development/TESTING.md`](development/TESTING.md) | Draft | Risk-based test strategy |
| [`development/RELEASES.md`](development/RELEASES.md) | Draft | Versioning and release gates |
| [`development/LICENSE.md`](development/LICENSE.md) | Draft | Artifact-class licensing guide and incomplete implementation state |

## Executable prototype artifacts

| Artifact | State | Role |
| --- | --- | --- |
| [`../LICENSE`](../LICENSE) | Present | Exact official English EUPL-1.2 text for original software |
| [`../NOTICE.md`](../NOTICE.md) | Present | Artifact-class rights notice and third-party exclusions |
| [`../THIRD_PARTY_NOTICES.md`](../THIRD_PARTY_NOTICES.md) | Active | Runtime dependency and third-party boundary inventory |
| [`../contracts/README.md`](../contracts/README.md) | Pre-stable implementation | Contract lifecycle and local validation instructions |
| [`../contracts/v1/source-profiles.schema.json`](../contracts/v1/source-profiles.schema.json) | Executable prototype | Source-registration contract |
| [`../contracts/v1/campaign-artifact.schema.json`](../contracts/v1/campaign-artifact.schema.json) | Executable prototype | Rights-aware archived campaign evidence metadata |
| [`../contracts/v1/acquisition-event.schema.json`](../contracts/v1/acquisition-event.schema.json) | Executable prototype | Bounded exact-response acquisition metadata and invariants |
| [`../contracts/v1/pilot-snapshot.schema.json`](../contracts/v1/pilot-snapshot.schema.json) | Executable prototype | Bounded POC configuration and publication gate |
| [`../contracts/v1/knowledge-passport.schema.json`](../contracts/v1/knowledge-passport.schema.json) | Executable prototype | Minimum POC passport projection |
| [`../data/sources/source-profiles.json`](../data/sources/source-profiles.json) | Active prototype data | Machine-readable source inventory |
| [`../data/pilot/campaign-artifact.json`](../data/pilot/campaign-artifact.json) | Authenticated with limitations | Fingerprint, citation, authenticity basis, rights, and non-retention reason for the archived campaign page |
| [`../data/pilot/pilot-snapshot-0.1.json`](../data/pilot/pilot-snapshot-0.1.json) | Historical prototype input | Preserved state before the primary campaign fragment was located |
| [`../data/pilot/pilot-snapshot.json`](../data/pilot/pilot-snapshot.json) | Versioned prototype input | Accepted case set, cut-off, fingerprint, and blockers |
| [`../data/pilot/open-data-subset.json`](../data/pilot/open-data-subset.json) | Third-party normalized prototype data | Six licensed City open-data records for the selected cases |
| [`../data/raw/respire-a-la-recre/2026-07-29/records-selected.json`](../data/raw/respire-a-la-recre/2026-07-29/records-selected.json) | Immutable prototype evidence | Exact 3,189-byte bounded API response under Licence Ouverte 2.0 |
| [`../data/raw/respire-a-la-recre/2026-07-29/acquisition-event.json`](../data/raw/respire-a-la-recre/2026-07-29/acquisition-event.json) | Validated prototype metadata | Request, fingerprint, rights, privacy minimization, security result, and limitations |
| [`../src/iagora/`](../src/iagora/) | Local prototype | Deterministic validation, transformation, passport, and HTML projection |
| [`../tests/`](../tests/) | Executable tests | Contract, evidence, scope, replay, publication, and accessibility guardrails |

## Planned capabilities and absent artifacts

The repository now contains a bounded local prototype, five executable contract schemas, an active source inventory, authenticated campaign-artifact metadata, one exact bounded API response with acquisition metadata, a validated six-record normalization, and an initial test suite. It does not contain a production source connector, general raw-evidence store, quarantine or parser sandbox, database, backend service, public API, approved frontend, AI service, search index, production security control set, telemetry stack, CI workflow, release, or deployment.

The primary 2020 campaign fragment is authenticated with limitations, but its full raw HTML remains absent for rights reasons and its mapping has not completed methodological review. The general dataset manifest contract, retention schedule, privacy assessment, threat model, incident plan, qualified legal and security reviews, adopted-record chain, executed financial evidence, outcome indicators, and production source inventory remain absent or incomplete.

## Recommended reading path

1. [`../README.md`](../README.md)
2. [`00_PROJECT_INTENT.md`](00_PROJECT_INTENT.md)
3. [`vision/01_MANIFESTO.md`](vision/01_MANIFESTO.md)
4. [`vision/00_VISION.md`](vision/00_VISION.md)
5. [`vision/02_PRODUCT_SCOPE.md`](vision/02_PRODUCT_SCOPE.md)
6. [`adr/ADR-INDEX.md`](adr/ADR-INDEX.md)
7. [`architecture/04_ARCHITECTURE.md`](architecture/04_ARCHITECTURE.md)
8. [`architecture/06_DATA_MODEL.md`](architecture/06_DATA_MODEL.md)
9. [`governance/22_GLOSSARY.md`](governance/22_GLOSSARY.md)
10. the specification relevant to the intended change
