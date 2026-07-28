# Architecture and Governance Index

**Status:** Draft  
**Owner:** Maintainers  
**Last reviewed:** 2026-07-28

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
| [`vision/02_PRODUCT_SCOPE.md`](vision/02_PRODUCT_SCOPE.md) | Draft | “Respire à la récré” pilot scope |
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

## Planned capabilities and absent artifacts

No application, executable schema, data contract, source connector, pipeline, backend, API, frontend, AI service, search index, security control set, telemetry stack, test suite, CI workflow, release, dataset, or deployment exists yet.

The exact root `LICENSE` text, documentation licence notice, dataset manifest contract, third-party notice, dependency inventory, retention schedule, privacy assessment, threat model, incident plan, and production source inventory are also absent.

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
