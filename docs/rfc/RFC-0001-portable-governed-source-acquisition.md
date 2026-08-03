# RFC-0001: Portable Governed Source Acquisition

**Status:** Draft

**Owner:** Maintainers

**Proposed:** 2026-08-03

**Last reviewed:** 2026-08-03

**Implementation status:** Increment 0 partially implemented; network connector and workflows absent

**Decision dependency:** A later ADR is required before adopting material persistence, source scheduling, or external-storage choices

## Summary

IAgora should introduce a small, portable acquisition engine that runs from a maintainer computer or a standard GitHub-hosted runner. The first remote workflow is triggered manually. Acquisition and repository admission remain separate operations, and a human maintainer must approve every admission. GitHub Actions artifacts are temporary 14-day review packages, not the governed evidence store. Every package receives a safe durable receipt, a pre-expiry reminder, and an explicit admitted, rejected, extended, or expired state so temporary bytes never disappear silently. Cloudflare R2 is deferred until measured volume, retention, or collaboration needs justify a separate storage service and a later decision approves it.

The first connector is limited to reviewed Opendatasoft JSON API sources. This RFC does not authorize production acquisition, recurring collection, automatic publication, rights-uncertain raw retention, a database, or a public IAgora API.

## Status of this proposal

The project maintainer validated the drafting direction on 3 August 2026. This document remains a draft. Its five Increment 0 contracts, bounded first plan, synthetic pending-review example, and historical compatibility projections are now present and executable. Their presence does not prove that the engine, network connector, workflows, quarantine storage, or production controls exist.

## Problem

The bounded pilot contains three exact City API responses, acquisition-event metadata, fingerprints, deterministic validation, and replay tests. Those responses were captured manually. The repository can verify them but cannot perform the acquisition itself.

This creates four practical problems:

1. acquisition steps are not reusable across datasets;
2. failures, retries, unchanged responses, and source changes are not recorded consistently;
3. work depends on a maintainer computer unless another operator reconstructs the manual process;
4. the successful-only pilot contract cannot represent the full governed acquisition lifecycle.

The project needs faster source work without weakening purpose limitation, source registration, rights, privacy, security, immutability, provenance, lineage, or human publication control.

## Important API distinction

This RFC concerns **upstream source APIs** used to retrieve public data. It does not define the future **IAgora public API** used by the SaaS product. The two boundaries MUST remain separate.

## Current repository reality

### Present and executable

- twenty bounded source profiles for the Clermont-Ferrand pilot;
- three exact, small, open-data City API responses stored under `data/raw/`;
- three validated acquisition events for successful HTTP 200 JSON responses;
- deterministic fingerprint, byte-size, selected-field, scope, and projection checks;
- a fail-closed Knowledge Passport and static local product projection;
- read-only CI for validation, tests, and deterministic build.
- five generalized acquisition and admission contracts, one reviewed six-school plan, one explicitly synthetic pending-review fixture, and deterministic compatibility projections for the three historical acquisitions.

### Present but too narrow for a reusable collector

- the source-profile contract is fixed to one territory and prototype acquisition modes;
- the acquisition-event contract describes successful, retained, Licence Ouverte responses only;
- acquisition invariants are embedded in the bounded pilot validator;
- the repository raw directory is a curated prototype evidence set, not a general evidence store.

### Planned but absent

- reusable network acquisition;
- connector interfaces and executable network transport;
- quarantine and atomic promotion;
- failed-attempt and retry records;
- content-addressed deduplication;
- portable local and GitHub Actions execution;
- a remote human-admission workflow;
- durable external evidence storage;
- source scheduling, production monitoring, and incident operations.

## Goals

The first increment SHOULD:

1. run the same acquisition rules locally and on GitHub Actions;
2. support manually triggered, bounded Opendatasoft JSON requests for approved sources;
3. reject unregistered, unauthorized, rights-unknown, or retention-unassigned acquisition before network access;
4. preserve exact response bytes when their approved retention class permits it;
5. record every attempt and distinguish failure, rejection, unchanged content, and new content;
6. deduplicate identical bytes without erasing attempt history;
7. keep acquisition separate from canonicalization, assessment, admission, and publication;
8. allow a maintainer to review and admit eligible evidence through a pull request without depending on one computer;
9. use safe, minimal operational logs and deterministic validation;
10. remain small enough to replace or extend after pilot measurements.
11. prevent temporary-package expiry from erasing the fact, result, or review state of an acquisition attempt.

## Non-goals

The first increment MUST NOT introduce:

- continuous or scheduled source collection; a metadata-only expiry monitor MAY check review deadlines without contacting civic sources;
- general web scraping, browser automation, PDF parsing, archives, or active documents;
- acquisition of BOAMP response bytes while their reuse and retention basis remains unresolved;
- a database, queue, distributed workflow engine, data lake, or graph store;
- Cloudflare R2 or another external object store;
- AI extraction or interpretation;
- a public ingestion or product API;
- automatic canonical promotion, political assessment, publication, merge, or deployment;
- production availability, recovery, compliance, or security claims.

## Governing constraints

The design MUST preserve the accepted decisions in ADR-0002, ADR-0003, ADR-0006, ADR-0007, ADR-0008, and ADR-0009.

In particular:

- source-specific fields stay outside canonical domain definitions;
- remote content is untrusted regardless of publisher;
- public accessibility does not establish lawful retention or redistribution;
- ordinary re-acquisition never overwrites an earlier artifact version;
- restriction and removal remain governed exceptions to normal immutability;
- AI output is neither evidence nor publication authority;
- admission and publication fail closed;
- the implementation remains a modular monolith until measured needs justify more infrastructure.

## Proposed architecture

### Portable acquisition core

One environment-independent Python application layer should coordinate:

- source-profile and acquisition-plan validation;
- request normalization and idempotency keys;
- connector selection;
- pre-network policy checks;
- constrained retrieval through a transport port;
- streaming fingerprint and size calculation;
- quarantine validation;
- artifact-version and attempt-event creation;
- safe result summaries;
- admission-package creation.

The core MUST NOT depend on GitHub Actions, a maintainer home directory, or a cloud vendor. Local commands and GitHub workflows are adapters around the same core.

### First connector

The first connector supports only reviewed Opendatasoft Explore JSON endpoints. It receives a versioned plan containing the registered source identifier, dataset identifier, selected fields, bounded filters, stable order, and limit.

The connector MUST NOT accept an arbitrary URL as its primary interface. The source profile supplies the allowed host and endpoint family; the plan supplies only permitted bounded query components.

### First live demonstration plan

The first remote demonstration uses the already approved school dataset rather than procurement data:

- plan identifier: `plan-city-schools-pilot-cases`;
- proposed plan version: `0.1.0`;
- source profile: `src-city-open-data-schools` version `1.1.0`;
- publisher: Ville de Clermont-Ferrand, Direction Enfance Jeunesse;
- connector: Opendatasoft Explore API v2.1 JSON records;
- dataset: `respire-a-la-recre-et-les-enfants-d-abord-vcf`;
- authentication: public and unauthenticated;
- rights: Licence Ouverte 2.0 with attribution;
- privacy class: public, non-personal school-unit aggregate; child-level data remains prohibited;
- order: `uai`;
- proposed result limit: 10;
- maximum accepted records: 6;
- proposed response-size limit: 64 KiB;
- proposed redirect limit: 2;
- proposed request timeout: 20 seconds.

The plan is bounded to these six reviewed national school identifiers:

| School group | Unit | UAI |
| --- | --- | --- |
| Pierre-et-Marie-Curie | Elementary | `0630258N` |
| Nestor-Perret | Elementary | `0630268Z` |
| Nestor-Perret | Nursery | `0630303M` |
| Jean-Zay | Nursery | `0630307S` |
| Pierre-et-Marie-Curie | Nursery | `0630992L` |
| Jean-Zay | Elementary | `0631845N` |

The selected fields remain the fourteen fields admitted by the historical acquisition:

```text
uai
denomination_ecole
nature
nombre_d_enfants_concernes
annee_vegetalisation
vegetalisation_terminee
cour_commune
nombre_de_cours_concernees
surface_de_la_cour_existante
surface_de_la_cour_apres_vegetalisation
nombre_d_arbres_existant
nb_arbres_plantes
surface_demineralisee_en_m2_surface_nette
pourcentage_de_surface_totale_de_la_cour_rendue_permeable
```

Coordinates, images, free text, contact data, and all non-required dataset fields remain excluded. The response must contain each selected UAI at most once. A missing, duplicated, unexpected, malformed, or seventh record is quarantined for review rather than silently coerced.

The 29 July 2026 response fingerprint is a historical comparison point, not a permanent expected value. Matching bytes produce `unchanged`; different bytes produce a candidate new version and a field-level change report. Neither outcome proves that a reported school state was true at the 31 December 2025 observation cut-off. Source-modification, acquisition, observation, and reported programme times remain distinct.

### Acquisition and admission remain separate

```text
reviewed source profile
        |
versioned acquisition plan
        |
portable acquisition core
        |
quarantined acquisition package
        |
deterministic validation
        |
human review
        |
admission pull request
        |
governed pilot evidence
```

No arrow in this flow implies automatic canonicalization, assessment, publication, or merge.

## Execution environments

### Local execution

A maintainer can run the engine from a checkout for development, offline replay, and controlled acquisition. Temporary and unadmitted bytes stay in a configurable local store outside the tracked evidence tree. No personal absolute path may enter contracts, logs, or committed metadata.

### GitHub Actions execution

A manually triggered `workflow_dispatch` workflow runs the same engine on a standard GitHub-hosted runner.

The acquisition job should:

- keep repository contents read-only and grant no pull-request or merge permission;
- accept only a reviewed plan identifier, not a free-form URL or shell fragment;
- use no long-lived source credential for the initial public APIs;
- produce a concise job summary and a fingerprinted acquisition package;
- upload the package with an explicit 14-day retention period;
- create a safe durable attempt receipt outside the expiring package;
- perform no repository write, pull-request creation, publication, or merge.

GitHub Actions artifacts are temporary transport for review. They are not the system of record and MUST NOT be the only retained copy after an artifact is admitted.

### Attempt receipt and expiry

The temporary package and the durable receipt have different purposes. The package may contain eligible raw bytes and review material. The receipt contains only safe metadata needed to prove that the attempt occurred and to explain what happened to its package.

The receipt MUST include:

- receipt, attempt, workflow-run, plan, source-profile, and package identifiers;
- attempt time, safe outcome, media type, byte size, and SHA-256 fingerprint when available;
- rights, privacy, retention, security, and validation states without raw content;
- package creation and expiry times;
- current review state and decision reference;
- no response body, secret, personal path, unnecessary personal data, or unsafe query value.

For the initial remote prototype, a metadata-only GitHub issue or an equivalently durable GitHub record MAY implement the receipt adapter. It is an operational receipt, not civic evidence, canonical knowledge, or the future production audit store. The exact adapter requires implementation review and least-privilege permissions.

The review lifecycle is:

1. on day 0, create the package and its durable receipt;
2. on or before day 10, a metadata-only monitor reminds the maintainer that the package will expire;
3. before day 14, the maintainer chooses `admit`, `reject`, or `extend`;
4. admission revalidates the package and proposes eligible content through a pull request;
5. rejection removes or allows expiry of the bytes and preserves the decision and rationale in the receipt;
6. one extension MAY create a new protected review package from the exact verified bytes, with a new expiry and extension event; it MUST NOT silently re-acquire potentially changed source bytes;
7. if no decision is recorded before deletion, the receipt becomes `expired_without_admission` and states that the original bytes are no longer available.

An expired package cannot be reconstructed by claiming that a later API response is the same evidence. A later retrieval is a new acquisition attempt and may create a different artifact version.

### Remote human admission

A separate manually triggered admission workflow should allow the maintainer to identify a completed acquisition run and approve a reviewed package without using the original computer.

The admission job MUST:

- require a protected maintainer approval step;
- retrieve the exact package by run and artifact identifiers;
- verify its fingerprint, plan version, source-profile version, validation state, rights, retention, privacy, and security decisions again;
- reject expired, changed, incomplete, or rights-blocked packages;
- update the durable receipt with the admission, rejection, extension, or expiry decision;
- create a dedicated branch and pull request rather than write directly to `main`;
- grant write permission only to the admission job and only for the required repository operations;
- leave merge as a separate human action.

An implementation may deliver local acquisition before remote admission, but the portable increment is not resilient to loss of the maintainer computer until both paths work.

## Proposed contract boundaries

The historical bounded contracts remain valid and MUST NOT be silently redefined. The reusable engine should introduce new pre-stable contracts or a new major version for:

### Acquisition plan

- stable plan identifier and semantic version;
- source-profile identifier and exact version;
- connector type and connector-rule version;
- allowed dataset and normalized bounded query;
- purpose, territory, observation scope, and expected media type;
- byte, record, redirect, timeout, and retry limits;
- expected rights, privacy, security, access, and retention gates;
- output and admission policy;
- owner, review state, and suspension condition.

### Acquisition attempt

- unique attempt identifier and time;
- plan, source-profile, connector, and software versions;
- requested and resolved locations without secrets;
- outcome and safe failure code;
- response status, headers required for provenance, media type, byte size, and timing when available;
- security, rights, privacy, and retention decisions;
- artifact-version reference when bytes are admitted to quarantine;
- retry and correlation relationships.

### Source artifact version

- stable artifact and version identifiers;
- exact SHA-256 fingerprint and byte size;
- acquisition-attempt references;
- content-addressed storage reference that exposes no personal path;
- publication and source-modification times when known;
- rights, access, retention, lifecycle, and supersession states;
- governed non-retention reason when bytes cannot be kept.

### Admission review

- exact package, artifact, attempt, plan, source-profile, and rule versions;
- deterministic validation results;
- reviewer role, decision, time, and rationale;
- rejected or admitted targets;
- limitations and required follow-up;
- pull-request reference when admission is proposed.

### Attempt receipt

- exact attempt, package, workflow-run, plan, and source-profile references;
- safe result, fingerprint, size, validation, rights, privacy, security, and retention states;
- package creation, reminder, expiry, extension, and decision times;
- review state: `admission_pending`, `admitted`, `rejected`, `extended`, or `expired_without_admission`;
- decision rationale and related admission-review or pull-request reference;
- an explicit `bytes_available` state that becomes false after rejection or expiry.

## Idempotency and version behavior

Each normalized plan has a deterministic plan fingerprint. Every network attempt receives a distinct event identifier because it represents a real observation.

- If the returned bytes match an existing lawful artifact fingerprint, the attempt records `unchanged` and references the existing artifact version. The bytes are not duplicated.
- If the bytes differ, the engine creates a candidate new artifact version and an explicit possible-supersession relationship. Newer content is not automatically authoritative.
- A retry never erases or rewrites its failed parent attempt.
- Reprocessing the same artifact with the same deterministic rule version reproduces the same validation output.
- A changed plan or rule version creates new lineage even if the source bytes are unchanged.

## Storage model

### Initial stage

The engine uses storage and receipt ports with three initial adapters:

1. a configurable local content-addressed store for developer execution;
2. a temporary GitHub Actions package for remote review.
3. a durable metadata-only receipt adapter that remains inspectable after package expiry.

The tracked `data/raw/` tree remains a curated, human-admitted set of small evidence objects with reviewed redistribution rights. It is not the default destination for every acquisition.

Rights-unknown, retention-unassigned, restricted, or unsafe bytes MUST NOT be exported into the public repository. The engine must stop before retrieval when the profile does not authorize even temporary acquisition.

### Deferred R2 stage

Cloudflare R2 is the preferred candidate for later evaluation, not an accepted dependency. A separate ADR and qualified rights, privacy, retention, security, recovery, and cost review are required before integration.

The R2 decision gate is reached when evidence shows at least one of the following:

- lawful raw evidence volume makes Git history operationally unsuitable;
- temporary GitHub retention is shorter than the accepted evidence-retention need;
- contributors or workflows require durable shared access to uncommitted governed artifacts;
- repeated downloads create avoidable source load or reproducibility risk;
- backup, restriction, removal, or recovery requirements cannot be met by the initial adapters.

Free-tier availability alone is not a sufficient architecture reason, and the project MUST NOT claim that an external service will remain free.

## Security and privacy controls

Before network access, the engine MUST verify the registered purpose, profile status, rights state, retention class, privacy class, risk tier, connector, host, dataset, query bounds, and reviewer authorization.

The retrieval boundary MUST include:

- HTTPS-only allowlists;
- rejection of loopback, local, private, link-local, metadata-service, and unsafe destinations;
- destination revalidation after name resolution and every redirect;
- strict redirect, timeout, response-size, record-count, and decompression limits;
- media-type and structural checks before parsing;
- atomic temporary files and content-addressed promotion;
- no active-content execution;
- safe filenames independent of source-controlled names;
- minimal logs without bodies, secrets, tokens, personal paths, or unnecessary personal data;
- pinned workflow dependencies and least-privilege GitHub permissions;
- structural handling of workflow inputs to prevent shell injection.

Public-source authority never bypasses these controls.

## Failure model

The reusable attempt contract should distinguish at least:

- `rejected_policy`;
- `failed_network`;
- `failed_redirect_policy`;
- `failed_size_limit`;
- `failed_media_type`;
- `failed_security_validation`;
- `failed_contract_validation`;
- `quarantined`;
- `unchanged`;
- `candidate_new_version`;
- `admission_rejected`;
- `admission_pending`;
- `admitted`.

These states describe processing, not civic evidence quality or truth. Failed and quarantined content cannot enter canonical, search, AI-retrieval, assessment, or public stores.

## Observability

Each run should emit safe structured events for attempt start, policy rejection, retrieval result, fingerprint result, validation result, deduplication, package creation, admission decision, and pull-request creation.

Initial operational measures are diagnostic:

- attempts by source and outcome;
- unchanged versus changed responses;
- bytes and duration;
- retries and repeated failures;
- validation and policy-gate failures;
- package expiry before review;
- reminders delivered and receipts closed with an explicit decision;
- admission review time;
- lineage completeness.

No metric should reward collecting more data or suppressing difficult failures.

## Validation strategy

CI MUST use controlled fixtures or a local test server, never depend on a live civic endpoint for correctness.

Tests should cover:

- source and plan contract validation;
- deterministic request normalization and plan fingerprints;
- allowlist and unsafe-destination rejection;
- redirect revalidation;
- timeout, size, media-type, malformed JSON, and unexpected-field failures;
- atomic quarantine and cleanup after failure;
- identical-byte deduplication;
- changed-byte version creation and supersession candidates;
- retry lineage;
- rights, privacy, retention, and suspension gates;
- safe logs and absence of secret or personal-path leakage;
- equivalence of local and GitHub-runner results for the same fixture;
- inability of the acquisition job to write to the repository;
- revalidation before an admission pull request;
- inability of admission to publish or merge automatically.
- preservation of a safe receipt and `expired_without_admission` state after temporary bytes are deleted.

Live-source smoke tests, if later approved, are operational diagnostics and must not replace deterministic tests.

## Rollout

### Increment 0: contracts and fixtures

**Current state:** Partially implemented. The five reusable boundary contracts,
the bounded first plan, one synthetic pending-admission example, safe failure
vocabulary, and deterministic projections of all three historical acquisitions
are present. No live attempt, quarantine package, or human admission has been
created through the proposed pipeline.

- define acquisition-plan, generalized attempt, artifact-version, and admission-review contracts;
- encode `plan-city-schools-pilot-cases` as the first bounded plan after its field and limit review;
- preserve the three current acquisitions as compatibility fixtures;
- record safe failure vocabularies and policy gates.

### Increment 1: portable local core

- implement the Opendatasoft connector and constrained transport boundary;
- implement quarantine, fingerprints, deduplication, events, and local replay;
- keep all acquisition manually triggered.

### Increment 2: remote acquisition

- run the same plan through a read-only manual GitHub Actions workflow;
- publish only a 14-day review package and safe summary;
- create a durable metadata-only attempt receipt;
- add a metadata-only deadline monitor that sends the day-10 reminder and never contacts a civic source;
- verify local and remote equivalence.

### Increment 3: remote human admission

- add protected manual approval;
- revalidate the selected package;
- create an admission pull request with no direct write to `main` and no automatic merge.

### Deferred increments

- scheduling only after reliability, source-load, review-capacity, and notification behavior are measured;
- additional connectors only after source-specific rights and risk review;
- R2 only after the explicit decision gate and later ADR;
- production operation only after retention schedules, threat model, privacy assessment, incident plan, recovery tests, and qualified reviews exist.

## Alternatives considered

### Source-specific scripts

Small scripts would produce results quickly but duplicate policy, provenance, retry, storage, and failure logic. They would make evidence handling depend on operator discipline and are rejected as the primary architecture.

### Portable core with adapters

This is the proposed option. It centralizes governance while keeping local and remote execution replaceable. It adds contract work but remains proportionate to the pilot.

### Workflow orchestrator, database, and object storage now

A managed scheduler, database, queue, and durable object store could support production operations but would add cost, credentials, migrations, security boundaries, and recovery duties before workload evidence exists. This option is deferred.

### Git as the universal raw-evidence store

Git provides review and history for small open artifacts but is unsuitable as the universal raw store because large files, rights restrictions, governed removal, access separation, and operational retention do not map safely to immutable public history. This option is rejected.

### GitHub Actions artifacts as durable storage

Actions artifacts are convenient for remote review but expire and have storage limits. Treating them as the evidence store would break durable provenance and recovery expectations. This option is rejected.

## Risks and mitigations

- **False automation confidence:** a successful download does not establish authority, quality, fulfillment, or impact. Admission and publication remain separate.
- **Public-repository leakage:** pre-network and pre-upload rights, privacy, and retention gates block ineligible bytes.
- **Supply-chain compromise:** pin workflow dependencies, minimize third-party actions, and keep permissions read-only by default.
- **Remote-provider dependence:** keep the core environment-independent and preserve exportable contracts and packages.
- **Temporary-artifact loss:** make expiry visible and require admission or deliberate discard before the deadline.
- **Unreviewed expiry:** retain a safe receipt, send a day-10 reminder, and record `expired_without_admission` without implying that later retrieval reproduces the deleted bytes.
- **Single human reviewer:** keep every automated recommendation non-binding and record the maintainer decision; this does not satisfy later independent publication review.
- **Free-tier change:** monitor provider terms and keep R2 deferred and replaceable behind a storage port.
- **Source changes:** version plans, connectors, bytes, and transformations; never silently coerce changed fields.

## Acceptance criteria for the first portable increment

The increment is complete only when:

1. one reviewed plan can acquire an approved Opendatasoft fixture locally and through a manually triggered GitHub workflow;
2. both executions produce equivalent normalized requests, fingerprints, validation results, and lineage;
3. unchanged bytes are not duplicated and changed bytes create a candidate new version;
4. network, security, contract, rights, privacy, and retention failures remain distinct and fail closed;
5. the acquisition workflow cannot write to the repository;
6. a separate human-approved admission flow can create a pull request without publishing or merging;
7. the three historical acquisitions remain validateable;
8. no database, source scheduler, workflow orchestrator, R2 dependency, public API, AI processing, or production claim is introduced;
9. documentation, indexes, contracts, tests, and current-state statements clearly distinguish present, proposed, and deferred capabilities.
10. every remote package has a 14-day expiry, a durable safe receipt, a reminder by day 10, and an explicit final state even if the bytes expire unreviewed.

## Open questions for review

1. Which Python HTTP transport best satisfies streaming, redirect, DNS, timeout, and testability requirements with the smallest justified dependency surface?
2. Which GitHub environment and approval settings should protect the admission workflow?
3. Should the first admission increment export only metadata or also the reviewed small open raw response?
4. Which exact operational evidence will trigger a later source-scheduling proposal?
5. Should the initial durable receipt adapter use a metadata-only GitHub issue or another inspectable GitHub record?

## Consequences

### Benefits

- acquisition no longer depends on one computer;
- one governed core serves local and remote execution;
- source changes, failures, and retries become inspectable;
- human admission remains explicit;
- the project gains useful automation without prematurely selecting production infrastructure.

### Costs and limitations

- the new contracts and security tests require more work than a one-off script;
- remote review packages are temporary until admitted;
- GitHub remains an operational dependency for the remote path;
- the first connector will not solve document, PDF, BOAMP-rights, or non-API evidence gaps;
- the engine still requires qualified review before production use.

## Related records

- [Architecture](../architecture/04_ARCHITECTURE.md)
- [Data pipeline](../architecture/08_DATA_PIPELINE.md)
- [Security architecture](../architecture/14_SECURITY.md)
- [Observability](../architecture/15_OBSERVABILITY.md)
- [Data contracts](../governance/18_DATA_CONTRACTS.md)
- [Data lineage](../governance/19_DATA_LINEAGE.md)
- [Data provenance](../governance/21_DATA_PROVENANCE.md)
- [ADR-0002](../adr/ADR-0002-canonical-assertion-and-evidence-model.md)
- [ADR-0007](../adr/ADR-0007-raw-evidence-retention-redaction-and-legal-removal.md)
- [ADR-0008](../adr/ADR-0008-public-source-acquisition-privacy-and-security-boundaries.md)
- [ADR-0009](../adr/ADR-0009-project-licensing-policy.md)
- [RFC index](RFC-INDEX.md)

## External operational references

Provider terms and limits are informative operational inputs, not accepted project decisions. They MUST be rechecked before implementation.

- [GitHub Actions billing](https://docs.github.com/en/billing/concepts/product-billing/github-actions)
- [GitHub workflow triggers](https://docs.github.com/en/actions/concepts/workflows-and-actions/workflows)
- [GitHub Actions artifact retention](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/remove-workflow-artifacts)
- [GitHub Actions secure-use reference](https://docs.github.com/en/actions/reference/security/secure-use)
- [Cloudflare R2 pricing](https://developers.cloudflare.com/r2/pricing/)
