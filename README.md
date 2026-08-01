# Project IAgora

> **Transforming Data into Knowledge.**  
> **Transforming Knowledge into Empowerment.**

Project IAgora is an open-source civic intelligence platform for turning fragmented public information into reliable, understandable, and verifiable knowledge.

Public budgets, council decisions, procurement notices, official reports, statistics, and open datasets are technically accessible, yet often difficult to find, connect, and interpret. IAgora preserves their origin, structures their content, links related facts, and makes the resulting knowledge easier to explore without hiding uncertainty or contradictory evidence.

The first implementation will focus on Clermont-Ferrand, France. The platform itself is designed to support other municipalities and public bodies without coupling the core model to one territory.

## Why IAgora exists

Publication alone does not guarantee meaningful transparency. A public record can remain practically inaccessible when it is buried in a long PDF, split across incompatible portals, published without context, or disconnected from later decisions and outcomes.

IAgora aims to help people answer questions such as:

- What was promised, decided, funded, and delivered?
- Which institution or public official was responsible?
- How much was announced, budgeted, committed, and spent?
- Which source is authoritative, and what other evidence supports the claim?
- How did a value travel from its original publication to an API, visualization, or AI-assisted explanation?
- Where do sources disagree, and what remains uncertain?

The project serves citizens, journalists, researchers, civil-society organizations, public administrations, students, and developers.

## What makes the project different

IAgora is not merely an open-data portal, dashboard, document search engine, or chatbot. It is designed as a **verifiable knowledge platform** in which every significant claim can be traced back to public evidence.

The planned public experience is an interactive territory dashboard rather than a report-only product. A macro territory view and thematic blocks lead to indicator, programme, commitment, evidence, and Knowledge Passport detail. Printable reports remain available as reproducible exports of the same governed records. A local static prototype now demonstrates the territory-home, education-theme, and programme-dossier path; it is not a deployed SaaS product.

Its governance model is built around complementary concepts:

- **Source of Truth** identifies the source with the strongest authority for a given fact.
- **Source of Evidence** records the materials that support, contextualize, or contradict an assertion.
- **Data Contracts** define what valid data must look like at system boundaries.
- **Data Lineage** records how information moves and changes through IAgora.
- **Data Provenance** records who published or supplied information and how it was acquired.
- **Data Quality** measures whether an asset is fit for its intended use.
- **Knowledge Passport** presents these elements as a human- and machine-readable identity card for a knowledge asset.

Artificial intelligence may assist with extraction, classification, retrieval, summarization, and explanation. It is never a source of truth, never silently resolves a material contradiction, and must cite the evidence used for a factual answer.

## Core principles

1. **Evidence before conclusion.** Claims must follow the available evidence, not the reverse.
2. **Traceability by design.** Every published fact must retain a path to its sources and transformations.
3. **Raw data is immutable.** Corrections and interpretations create new records; they do not overwrite collected evidence.
4. **Uncertainty remains visible.** Missing, disputed, estimated, and superseded values must be distinguishable.
5. **Methods are reproducible.** Validation, transformation, scoring, and analytical rules are documented and versioned.
6. **AI assists human understanding.** Generated content is labeled, sourced, and reviewable.
7. **Methodological neutrality.** IAgora documents public action; it does not campaign, rank politicians, or prescribe political choices.
8. **Accessibility is part of correctness.** Civic knowledge is useful only when non-specialists can understand it.
9. **Open and maintainable by design.** Prefer open standards, clear boundaries, simple solutions, and documented decisions.

## Platform model

```text
Public sources
      |
      v
Connectors and immutable raw storage
      |
      v
Parsing, validation, and canonical transformation
      |
      v
Canonical data + documents + provenance + lineage
      |
      v
Knowledge, evidence, search, and analytics services
      |
      v
Versioned API
      |
      v
Editorial web experience, visualizations, and AI-assisted exploration
```

The architecture is specified in terms of responsibilities before technologies. Concrete implementation choices belong in Architecture Decision Records (ADRs).

## Documentation map

The repository is documentation-first. The files below are present, but most specifications remain drafts and do not prove that the described capabilities are implemented.

```text
README.md
AGENTS.md
docs/
├── 00_PROJECT_INTENT.md
├── 01_ARCHITECT_PLAYBOOK.md
├── vision/
│   ├── 00_VISION.md
│   ├── 01_MANIFESTO.md
│   ├── 02_PRODUCT_SCOPE.md
│   └── 03_ROADMAP.md
├── architecture/
│   ├── 04_ARCHITECTURE.md
│   ├── 05_ARCHITECTURAL_PRINCIPLES.md
│   ├── 06_DATA_MODEL.md
│   ├── 07_CANONICAL_DATA_DICTIONARY.md
│   ├── 08_DATA_PIPELINE.md
│   ├── 09_BACKEND.md
│   ├── 10_API.md
│   ├── 11_FRONTEND.md
│   ├── 12_AI_ENGINE.md
│   ├── 13_SEARCH_ENGINE.md
│   ├── 14_SECURITY.md
│   └── 15_OBSERVABILITY.md
├── governance/
│   ├── 16_SOURCE_OF_TRUTH.md
│   ├── 17_SOURCE_OF_EVIDENCE.md
│   ├── 18_DATA_CONTRACTS.md
│   ├── 19_DATA_LINEAGE.md
│   ├── 20_DATA_QUALITY.md
│   ├── 21_DATA_PROVENANCE.md
│   ├── 22_GLOSSARY.md
│   ├── 23_KNOWLEDGE_PASSPORT.md
│   └── 24_PILOT_SOURCE_INVENTORY.md
├── adr/
│   ├── README.md
│   ├── ADR-INDEX.md
│   ├── ADR-TEMPLATE.md
│   ├── ADR-0001-project-vision-and-pilot-boundary.md
│   ├── ADR-0002-canonical-assertion-and-evidence-model.md
│   ├── ADR-0003-fact-specific-source-of-truth-rules.md
│   ├── ADR-0004-campaign-commitment-fulfillment.md
│   ├── ADR-0005-outcome-measurement-and-causal-impact.md
│   ├── ADR-0006-minimum-knowledge-passport-contract.md
│   ├── ADR-0007-raw-evidence-retention-redaction-and-legal-removal.md
│   ├── ADR-0008-public-source-acquisition-privacy-and-security-boundaries.md
│   ├── ADR-0009-project-licensing-policy.md
│   └── ADR-0010-multidimensional-accountability-and-policy-lineage.md
├── development/
│   ├── CONTRIBUTING.md
│   ├── CODING_STANDARDS.md
│   ├── TESTING.md
│   ├── RELEASES.md
│   └── LICENSE.md
└── 99_ARCHITECTURE_INDEX.md
contracts/
├── README.md
└── v1/
data/
├── sources/
└── pilot/
src/iagora/
tests/
```

The architecture index is the detailed navigation hub. The ADR index records accepted, proposed, superseded, and rejected architectural decisions.

## Recommended reading paths

### First-time reader

1. This `README.md`
2. `docs/00_PROJECT_INTENT.md`
3. `docs/vision/01_MANIFESTO.md`
4. `docs/vision/00_VISION.md`
5. `docs/vision/02_PRODUCT_SCOPE.md`
6. `docs/99_ARCHITECTURE_INDEX.md`

### Contributor

1. This `README.md`
2. `AGENTS.md` when using an AI coding agent
3. `docs/01_ARCHITECT_PLAYBOOK.md`
4. `docs/development/CONTRIBUTING.md`
5. The specification and ADRs relevant to the proposed change

### Architect or technical reviewer

1. `docs/01_ARCHITECT_PLAYBOOK.md`
2. `docs/architecture/04_ARCHITECTURE.md`
3. `docs/architecture/05_ARCHITECTURAL_PRINCIPLES.md`
4. `docs/architecture/06_DATA_MODEL.md`
5. `docs/governance/16_SOURCE_OF_TRUTH.md` through `23_KNOWLEDGE_PASSPORT.md`
6. `docs/adr/ADR-INDEX.md`

## Current phase

IAgora has completed its initial documentation foundation and now has a **bounded local proof of concept**. The immediate goals are to:

- consolidate the vision and product scope;
- complete and cross-reference the architecture specifications;
- stabilize the canonical data model and governance vocabulary;
- document significant decisions as ADRs;
- complete methodological review of the candidate campaign-to-programme mapping and locate the missing attributable works-procurement and competent-completion records for the accepted Clermont-Ferrand pilot;
- evolve the pre-stable executable contracts without weakening the accepted evidence, authority, lineage, rights, and publication invariants;
- validate the local vertical slice with methodological, privacy, security, legal, and accessibility reviewers before any public release.

The current implementation authenticates a short, unquantified schoolyard-regreening commitment from a 2019 archived campaign page, preserves two exact bounded City API responses, and validates their school and procurement projections. The school subset covers Nestor-Perret, Pierre-et-Marie-Curie, and Jean-Zay. Ten metadata-only municipal documents establish adopted policy, programme-level budget authorization and expenditure, reported site delivery, and funding forecasts without conflating those stages. A separate procurement bundle documents candidate evidence for a 2020 study and 2025 design and user-assistance services while preventing holder-level amount duplication. The source records do not directly name the Respire programme and do not establish attributable works, payment, or competent completion. BOAMP raw bytes remain excluded pending rights review. An explicit AI-assisted proposal maps one essential campaign component to the later programme through a visible scope comparison; it remains pending independent methodological and authority review. The Knowledge Passport and a deterministic three-level static interface expose the same bounded records through a Clermont-Ferrand home, an education dashboard, and a detailed printable dossier. The home keeps the macro city chart as an explicit missing-data state and keeps unsupported themes as placeholders; it does not invent a generalized city KPI. No generalized indicator explorer, production report service, account system, public frontend, or SaaS deployment exists. Publication remains blocked because the mapping is not accepted, attributable works procurement and competent-completion records remain missing, administrative-document and BOAMP dataset rights remain pending, and no reviewed outcome or causal-impact evidence exists. The roadmap describes strategic milestones rather than guaranteed dates.

## Run the local proof of concept

The prototype uses Python 3.11 or later and has no third-party runtime dependency.

```sh
PYTHONPATH=src python3 -m iagora validate
PYTHONPATH=src python3 -m iagora build
python3 -m http.server --directory build/pilot 8000
```

The generated territory home is available at `http://localhost:8000`, the first thematic dashboard at `http://localhost:8000/education/`, and the detailed printable dossier at `http://localhost:8000/programmes/respire-a-la-recre/`. They are local review artifacts, not an authorized civic publication. Run the test suite with:

```sh
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

## Working with the project

Before proposing a change:

1. Identify the user problem and the affected knowledge assets.
2. Read the relevant specification, glossary entries, and accepted ADRs.
3. Separate established facts from proposals and assumptions.
4. Evaluate impacts on evidence, provenance, lineage, quality, security, accessibility, and operations.
5. Use an ADR for a significant architectural decision and an RFC for a substantial proposal that needs discussion.
6. Keep documentation, contracts, tests, and implementation aligned.

AI agents must also follow [`AGENTS.md`](AGENTS.md).

## Project boundaries

IAgora may collect and explain legally accessible public information. It does not:

- monitor private citizens;
- generate political endorsements or campaign material;
- predict elections;
- treat media coverage or AI output as authoritative when primary records exist;
- conceal material source conflicts;
- publish a confidence or quality score without an inspectable method.

## Contributing

Contributions from software engineering, data engineering, design, journalism, public policy, law, accessibility, research, and civic communities are welcome.

Follow the accepted [contribution guide](docs/development/CONTRIBUTING.md). Before a large change, open a discussion or issue explaining the problem, affected users, evidence requirements, architectural impact, alternatives, and validation approach. The contribution attestation process and qualified licensing review remain incomplete.

## License

[ADR-0009](docs/adr/ADR-0009-project-licensing-policy.md) accepts the project licensing policy: EUPL-1.2 for original software, CC BY 4.0 for original reusable documentation, and dataset-specific Licence Ouverte 2.0 publication after rights review. The exact EUPL-1.2 text is in [`LICENSE`](LICENSE), and [`NOTICE.md`](NOTICE.md) explains artifact classes and exclusions. Third-party evidence and data retain their original rights; consult their manifests and the [licensing guide](docs/development/LICENSE.md). Qualified ownership, compatibility, and dataset-publication reviews remain necessary.

## Status

Project IAgora is under active design. Interfaces, schemas, terminology, and document locations may change before the first stable release. Public visibility does not imply production readiness or that every planned document has been accepted.

---

**Project IAgora**  
**Transforming Data into Knowledge.**  
**Transforming Knowledge into Empowerment.**
