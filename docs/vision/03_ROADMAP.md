# Strategic Roadmap

**Status:** Draft  
**Owner:** Maintainers  
**Last reviewed:** 2026-07-30

## How to read this roadmap

This roadmap is a proposed sequence of outcomes and decision gates. It is not a delivery schedule, release commitment, or evidence of implementation. Dates should be added only when ownership, capacity, dependencies, and acceptance criteria are known.

## Current phase: bounded vertical-slice prototype

The initial decision foundation is merged. A local, non-public vertical slice now validates source profiles and a six-record open-data subset, projects a Knowledge Passport, and renders the three accepted school cases. The immediate objective is to replace prototype gaps with reviewable evidence and production-grade controls without widening the pilot.

### Current repository evidence

- ADR-0001 through ADR-0010 are accepted; ADR-0010 now has a bounded local product projection, while its generalized field-level contracts remain incomplete.
- Every document in the target documentation map is present.
- Project Intent and the Architect Playbook are accepted.
- The Manifesto and contribution guide are accepted.
- The Source of Truth and Source of Evidence specifications are accepted.
- All architecture specifications, the remaining development guides, and the remaining governance specifications remain drafts.
- The product scope is accepted and the three case studies are confirmed through an active source inventory.
- The exact EUPL-1.2 text, artifact-class notice, and third-party notice are present.
- Eight pre-stable executable schemas cover source profiles, campaign artifacts, commitment mappings, acquisition events, administrative evidence, procurement evidence, pilot snapshots, and Knowledge Passports, with a standard-library validator.
- A deterministic local transformation, three-level static HTML product projection, and initial contract, methodology, and presentation guardrail tests exist.
- Three exact bounded City API responses and acquisition events exist; no production connector, general immutable raw store, database, network service, public API, deployment, or public service exists.
- Ten metadata-only municipal document versions establish a partial administrative chain without conflating adopted policy, programme finance, reported delivery, and funding forecasts.
- A minimal read-only CI workflow runs deterministic validation, tests, and the local build on Python 3.11.
- A primary campaign fragment is authenticated with limitations and retained as rights-aware metadata. Its one-component mapping to the later programme is now an explicit AI-assisted proposal. A separate executable bundle documents candidate procurement evidence for a 2020 study, a 2021 citywide schoolyard works framework, a separate 2022 works-framework competition, and 2025 design services, with explicit relationship, amount-stage, scope, cut-off, and rights limits; none directly names Respire or identifies a purchase order for a pilot school. Independent methodological and authority review, school-attributable works procurement, competent-completion evidence, retention schedule, privacy assessment, threat model, incident plan, qualified reviews, and production security controls remain incomplete.
- A local Clermont-Ferrand home, bounded Education dashboard, evidence-linked timeline, and printable programme dossier now demonstrate the target navigation. The macro view remains an explicit missing-data placeholder, and no real city-wide macro series, generalized indicator explorer, production report service, or SaaS deployment exists.

### Exit criteria

- vision and initial product boundaries are accepted;
- the Clermont-Ferrand pilot question is accepted;
- document status and ownership rules are operational;
- an ADR index and decision process exist;
- project licensing has been decided or is recorded as a blocker;
- unresolved legal, privacy, accessibility, and security questions have owners.

## Phase 1: pilot methodology

Define the minimum governance and domain model needed for the “Respire à la récré” pilot.

### Proposed outcomes

- canonical glossary;
- campaign commitment, implementation, fulfillment, and impact-assessment methodology;
- multidimensional public-accountability and policy-lineage methodology;
- Source of Truth and Source of Evidence rules;
- assertion, evidence, conflict, and temporal model;
- provenance and lineage requirements;
- financial-observation semantics;
- minimum Knowledge Passport contract;
- acquisition, retention, redaction, and licensing rules;
- accepted ADRs for long-lived decisions.

### Exit criteria

- representative examples can be expressed without losing source scope or uncertainty;
- authority is determined per fact type rather than by a global source ranking;
- campaign commitments can be linked to public actions without treating later municipal communication as the original promise;
- fulfillment summaries can be reproduced from visible atomic states and rules;
- financial stages and policy-lineage claims remain inspectable and cannot substitute for fulfillment or impact;
- outputs, outcomes, and attributed impacts remain distinguishable;
- material conflicts remain representable;
- enforceable rules have deterministic validation criteria;
- legal and security risks are either mitigated or explicitly block implementation.

## Phase 2: thin vertical slice — in progress

Implement one end-to-end path for the programme and three selected school case studies.

### Current prototype evidence

- bounded source profiles and rights states;
- fingerprinted metadata and a precise short fragment from an authenticated archived campaign page, while restricted raw HTML remains excluded;
- one exact six-UAI API response, acquisition event, and deterministic raw-to-normalized equality check;
- normalized six-record open-data subset for the three accepted cases;
- ten metadata-only municipal document versions forming a partial administrative chain;
- three bounded City API responses and an executable candidate-evidence bundle for study, design services, and citywide works frameworks, with BOAMP metadata retained without raw bytes pending rights review;
- one explicit, review-pending candidate-correspondence proposal with a seven-dimension scope comparison, documented 2015 and 2018 policy predecessors, a stable campaign-fragment identifier, a separately resolvable canonical target assertion, complete advisory history, two current non-binding `accept` recommendations for corrected version `0.3.0`, an interim single-maintainer POC decision still pending, retained publication-grade independent reviews, and fail-closed output constraints;
- deterministic validation and transformation;
- row-level evidence locators and source attribution;
- versioned Knowledge Passport JSON;
- static Clermont-Ferrand home, Education dashboard, and detailed printable review dossier generated from the same passport;
- publication gate that fails closed on known blockers;
- initial automated tests for contracts, scope separation, evidence coverage, determinism, and unsupported conclusions;
- minimal CI execution of validation, tests, and deterministic build on Python 3.11.

### Remaining outcomes

- idempotent acquisition from the approved official corpus;
- immutable raw evidence with recovery and governed redaction behavior;
- parsing, validation, and canonical transformation;
- source-fragment citations and transformation lineage;
- generalized immutable raw source versions and governed acquisition events beyond the three bounded City prototype artifacts;
- independent review of the proposed commitment-to-action mapping and action-to-impact pathways backed by the remaining authoritative records;
- browser, responsive-layout, print, and assistive-technology review of the product-shaped navigation prototype;
- generalized field-level implementation of the ADR-0010 assessment and policy-lineage model beyond the bounded dossier;
- reviewed accessible plain-language exploration;
- contract, lineage, accessibility, and security tests;
- observability for acquisition and publication failures.

### Exit criteria

- every displayed fact is traceable to evidence;
- reprocessing the same inputs is reproducible;
- source changes and contradictions are surfaced;
- non-specialist users can complete the defined journey;
- no unsupported political or impact conclusion is generated.

## Phase 3: pilot evaluation

Evaluate usefulness, methodological integrity, and operating cost before expanding scope.

### Proposed outcomes

- structured review by citizens, journalists, domain specialists, and accessibility testers;
- usability review of territory, theme, indicator, evidence, and print navigation without requiring users to understand the underlying data model;
- analysis of missing evidence and false certainty risks;
- measurement of acquisition reliability and review effort;
- corrections to the canonical model through specifications and, when necessary, superseding ADRs;
- a documented decision to stop, iterate, or expand.

## Phase 4: controlled expansion

Expand only when pilot evidence supports it.

Possible directions include additional municipal programmes, additional public-record classes, or another territory. Each expansion requires explicit scope, source, governance, legal, accessibility, and operating-cost assessment.

Thematic expansion may add education, finance, culture, public safety, or other policy domains only when each domain has a governed question, source inventory, indicator definitions, privacy and rights posture, and responsible reviewer. A navigation placeholder is not evidence that a theme is ready for publication.

## Deferred decisions

The roadmap does not yet select:

- application framework, database, search engine, or hosting platform;
- production service-level objectives;
- automated AI model or provider;
- public launch date;
- multi-territory deployment plan;
- the macro Clermont-Ferrand visualization and primary indicator set for each theme;
- SaaS tenancy, authentication, billing, and public-versus-maintainer workspace boundaries.

These choices would be premature before the pilot contracts and workload are understood.
