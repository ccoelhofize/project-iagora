# Canonical Glossary

**Status:** Draft  
**Owner:** Maintainers  
**Last reviewed:** 2026-07-29

## Purpose

This glossary provides the canonical working vocabulary for Project IAgora. Other documents should link here instead of creating competing definitions. Because this document is a draft, every definition remains subject to explicit review and acceptance.

Terms describe distinct concerns. In particular, authority, evidence, quality, provenance, lineage, and confidence must not be collapsed into a single trust concept or score.

## Core knowledge terms

### Assertion

An atomic, reviewable statement about one subject, property, value, scope, and relevant time. An assertion records what is stated; it is not evidence that the statement is true.

An assertion should be narrow enough that evidence can support, contradict, or contextualize it without implicitly deciding a broader political or editorial conclusion.

### Claim

A statement made by a source, institution, person acting in a public role, or generated artifact. IAgora may represent a claim as one or more atomic assertions. A claim remains attributable to its speaker or publisher.

### Campaign artifact

A dated item published or formally distributed by a candidate, campaign list, or authorized campaign organization, such as a programme, manifesto, profession of faith, website page, leaflet, speech transcript, or audiovisual statement. Its provenance and publication context must remain explicit.

Media reporting may provide evidence about a campaign statement but is not the original campaign artifact.

### Campaign commitment

An attributable campaign statement that promises, undertakes, or clearly proposes a future public action or outcome if the relevant candidate or list obtains office. A commitment must preserve its original wording, author, campaign, election, date, territorial scope, conditions, and degree of specificity.

A campaign commitment is not automatically equivalent to a later programme, budget line, administrative act, or observed result. Those relationships require explicit evidence-backed mappings.

### Commitment mapping

A versioned, reviewable relationship between an atomic campaign commitment component and a later assertion about a public decision, resource, output, outcome, or impact. A mapping preserves the compared scopes, evidence, rationale, method version, uncertainty, counterevidence, lineage, and review state.

Compatible wording or chronology may support a proposed mapping but cannot establish it alone. A proposed or AI-assisted mapping is not an accepted relationship, implementation state, fulfillment conclusion, or impact claim.

### Fulfillment assessment

A versioned evaluation of how the evidenced public action compares with a campaign commitment under an accepted method and observation cut-off. A fulfillment assessment must expose the commitment decomposition, required conditions, atomic implementation states, evidence, uncertainty, and review record.

The accepted summary labels are fulfilled, partially fulfilled, not fulfilled, changed, not yet assessable, and not verifiable. Their semantics and required evidence are governed by [`ADR-0004`](../adr/ADR-0004-campaign-commitment-fulfillment.md). A summary label must never replace its evidence and reasoning record.

### Knowledge asset

A versioned IAgora object intended to communicate or support knowledge, such as an assertion, indicator, timeline, dataset, document interpretation, or analytical output. A knowledge asset retains links to its evidence, provenance, lineage, validity, and applicable governance decisions.

### Knowledge Passport

A human- and machine-readable summary of a knowledge asset's identity, definition, scope, sources, evidence relationships, provenance, lineage, quality information, temporal validity, conflicts, uncertainty, licence, and review state.

A Knowledge Passport exposes existing governance information. It is not itself proof and must not replace the underlying records.

### Uncertainty

Known limits on what can be concluded from the available evidence, method, scope, or timing. Uncertainty may arise from missing evidence, measurement limitations, ambiguous scope, conflicting sources, or incomplete transformations. It should be expressed in inspectable components and plain language.

## Source and evidence terms

### Source

An identifiable origin from which information or evidence is obtained. A source may be an institution, information system, dataset, document, register, API, or other published record. The relevant level must be explicit: a portal hosting a document is not necessarily the document's publisher or competent authority.

### Publisher

The organization or public body that issues or makes a source available. Publisher identity contributes to provenance but does not automatically establish authority for every fact contained in the source.

### Source authority

The competence of a source to establish a particular fact within a defined legal, administrative, territorial, and temporal scope. Authority is evaluated per fact type and cannot be inferred from a single global ranking of sources.

### Source of Truth

The source or governed set of sources with the strongest applicable authority for a specific fact and scope. Source of Truth is a selection rule for authority, not a declaration that a source is complete, current, or infallible.

Different fact types may have different Sources of Truth. An initial budget (`budget primitif`) may establish an approved forecast while a financial account establishes executed expenditure.

### Source of Evidence

A source that provides material supporting, contradicting, or contextualizing an assertion. A Source of Evidence need not be authoritative for the fact and must retain its attribution, scope, and relationship to the assertion.

### Evidence item

A versioned source fragment or record used to evaluate an assertion. It should be addressable precisely enough for another person to inspect it, subject to lawful access and retention restrictions.

### Evidence relationship

A qualified, reviewable link between an evidence item and an assertion. Initial relationship types are:

- **supports:** the evidence is consistent with and materially strengthens the assertion;
- **contradicts:** the evidence is materially inconsistent with the assertion under the same interpreted scope;
- **contextualizes:** the evidence helps interpret the assertion but does not directly support or contradict it.

The relationship records an evaluation. It does not alter the immutable evidence item.

### Conflict

A situation in which credible evidence or authoritative sources cannot be reconciled under the currently documented scope, definitions, and temporal rules. A difference is not automatically a conflict: units, dates, institutional scope, or publication status may explain it.

Material conflicts must remain visible until they are resolved through additional evidence or a versioned governance decision.

### Citation

A reference from an assertion or output to the exact evidence used, including enough source, version, location, and access information for inspection. A link to a document homepage alone is insufficient when a more precise fragment can be identified.

### Raw evidence

The bytes and acquisition metadata captured from a source before interpretive transformation. Raw evidence is immutable in normal operation. Corrections, annotations, redactions, and later acquisitions create separate governed records.

Immutability does not override legal deletion, privacy, security, or safety obligations. Any exceptional restriction or removal requires an auditable record that reveals as much of the event as lawfully possible without retaining prohibited content.

## Provenance and processing terms

### Acquisition event

The recorded act of obtaining material from a source. It includes the source location, acquisition time, method, result, content fingerprint, applicable licence or access information, and relevant software version.

### Data provenance

Information about where an asset originated, who published or supplied it, and how and when IAgora acquired it. Provenance describes origin and custody; it does not describe every subsequent transformation.

### Data lineage

The ordered, reproducible record of how inputs, transformations, validations, and versions produced an output. Lineage connects a published asset to both raw inputs and processing steps.

### Transformation

A versioned operation that derives a new representation or value from recorded inputs. It includes the rule or software version, parameters, execution time, outputs, validation results, and material assumptions.

### Generated artifact

Content produced or materially rewritten by an AI model, including extraction, classification, summary, or explanation. A generated artifact is never evidence. If persisted, it retains model, prompt or instruction, input, output, and review-version information appropriate to its use.

### Idempotent ingestion

Ingestion behavior in which processing the same source version with the same rules does not create unintended duplicates or divergent canonical results.

## Canonical model and contract terms

### Canonical concept

A source-agnostic domain definition used consistently across IAgora. A source-specific field may map to a canonical concept but must not redefine it.

### Canonical entity

A versioned representation of a domain object, such as a public body, territory, programme, school, document, or assertion, identified independently of any one source system.

### Data contract

An explicit, versioned agreement governing data at a system boundary. It defines structure, semantics, required metadata, validation rules, compatibility expectations, and failure behavior.

### Deterministic validation

A repeatable rule whose outcome is determined by explicit inputs and logic rather than model judgment. Enforceable publication and contract rules should use deterministic validation wherever practicable.

### Version

An identifiable state of a document, source, entity, rule, contract, or output. A version must be distinguishable from later corrections and superseding states.

## Time and scope terms

### Territorial scope

The geographic or administrative area to which an assertion, source, rule, or measurement applies.

### Temporal validity

The period during which a fact, definition, relationship, or rule applies. Temporal validity is distinct from publication time, acquisition time, and processing time.

### Observation cut-off

The latest point in time included in a defined historical analysis. Evidence published later may change a later version of the analysis but must not be presented as if it had been available at the original cut-off.

### Supersession

A versioned relationship in which a later record or decision replaces an earlier one for future use while preserving the earlier record and its historical validity.

### Public body

An institution or legally recognized public entity acting within a documented competence. City, metropolitan, departmental, regional, national, and affiliated bodies retain distinct identities even when they collaborate.

### Programme

A governed grouping of public objectives, activities, resources, and expected outcomes. A programme is not equivalent to a political promise, budget line, project, contract, or individual realization unless an accepted mapping explicitly says so.

### Milestone

A dated or date-bounded event used to describe progress, such as an announcement, authorization, funding decision, start of work, reported completion, or measurement. A milestone records the event evidenced; it does not by itself establish overall programme completion.

### Policy lineage assessment

A versioned derived assessment describing an evidence-backed relationship between a public action and earlier or concurrent decisions, programmes, resources, outputs, or commitments. Possible relationships include a new initiative, continuation, extension, acceleration, reorientation, renaming or reframing, replacement, and indeterminate lineage.

A lineage assessment preserves the compared scopes, dated events, evidence, counterevidence, search boundary, method, uncertainty, and review state. Chronology, shared terminology, political identity, or an election boundary cannot establish novelty, continuity, causation, ownership, or political credit by itself. The rules are governed by [`ADR-0010`](../adr/ADR-0010-multidimensional-accountability-and-policy-lineage.md).

## Outcome and impact terms

### Baseline

The documented reference state against which a later outcome or change is compared. A baseline preserves the indicator definition, measurement method, population, territory, period, source, and known limitations.

### Indicator

A defined quantitative or qualitative measure used to describe an input, activity, output, outcome, or impact. An indicator retains its formula or assessment rule, unit, population, territorial scope, period, source, transformation version, and fitness-for-use limitations.

### Output

A directly produced deliverable or service attributable to an activity, such as a completed schoolyard transformation or a number of trees planted. Delivery of an output may support a fulfillment assessment but does not by itself establish an outcome or impact.

### Outcome

An observed change in conditions, behavior, experience, or performance following an intervention. An outcome may be temporally associated with an action without being proven to have been caused by it.

### Impact

A material longer-term effect on people, institutions, public services, the environment, or the territory. IAgora must distinguish an observed impact indicator from a claim that the intervention caused that impact.

### Causal attribution

A conclusion that an intervention caused some or all of an observed change. Causal attribution requires an accepted evaluation design, explicit assumptions, suitable baseline or comparison, and documented uncertainty. Chronological sequence or political credit alone is insufficient.

IAgora distinguishes observed change, association, contribution supported, causally attributed, and causal status not verifiable. Their semantics and evidence requirements are governed by [`ADR-0005`](../adr/ADR-0005-outcome-measurement-and-causal-impact.md).

## Quality and review terms

### Data quality

The degree to which an asset is fit for a stated use under documented dimensions, methods, and limitations. Relevant dimensions may include completeness, validity, timeliness, consistency, uniqueness, and accessibility. Quality is not a substitute for authority or truth.

### Fitness for use

A contextual assessment of whether an asset can safely support a specified task. The same asset may be fit for one use and unfit for another.

### Confidence

A documented assessment of the strength and limitations of a conclusion under an explicit method. Confidence must expose its inputs and rules. It must not be inferred solely from model output or compressed into an unexplained number.

### Methodological review

A recorded human or deterministic evaluation of an assertion, evidence relationship, transformation, or output. It includes reviewer role, decision, timestamp, rationale, and the version reviewed while avoiding unnecessary personal data.

## Acquisition, lifecycle, and publication terms

### Source profile

A versioned registration describing why and how IAgora may acquire from a source. It records purpose, scope, endpoint, expected content, authority candidates, rights, privacy and security risk, frequency, retention class, responsible role, and suspension conditions.

### Quarantine

An isolated lifecycle state for content that must not enter canonical, search, AI-retrieval, or public stores while security, legality, rights, format, or quality concerns are reviewed.

### Retention class

A governed rule defining why an asset may be retained, for how long or under which review condition, with which access controls, and how expiry, restriction, backup, and removal behave. Public availability does not establish a retention class.

### Removal tombstone

A minimal lawful record that explains that governed content was removed and which downstream assets were affected without retaining the prohibited content or unnecessary personal data.

### Publication gate

A deterministic and reviewable boundary that prevents an asset from becoming public until applicable evidence, authority, lineage, contract, conflict, privacy, security, licence, retention, review, and Knowledge Passport requirements pass.

### Disclosure profile

A versioned view defining which canonical passport fields an audience may access. A restricted field retains a lawful, non-sensitive reason state; the profile must not change the substantive meaning of the represented assertion.

### Rights state

The recorded licence, public-domain, permission, restriction, or unknown status governing an artifact or dataset. `Rights unknown` blocks redistribution but does not by itself erase the artifact's evidentiary relevance.

## Financial terms for the pilot

### Financial observation

An amount reported for a defined entity, purpose, accounting stage, period, territorial scope, and source. Amounts at different stages must remain distinguishable.

Initial stages include:

- **estimate:** an indicative amount without an approved budgetary effect;
- **multi-year programme:** planned resources across more than one financial year;
- **budget authorization:** authority to commit or spend within defined limits;
- **budget appropriation:** an amount entered in an approved budget for an exercise;
- **grant requested:** external funding applied for but not yet awarded;
- **grant awarded:** external funding formally allocated under stated conditions;
- **commitment:** an amount legally committed to a third party;
- **mandate or expenditure order:** an amount ordered for payment under the applicable accounting process, which is not automatically proof of disbursement;
- **payment:** an amount actually disbursed;
- **final cost:** a closed or formally reported total under the applicable accounting method.

These terms do not establish a complete French public-accounting model. The data model must map them to accepted legal and accounting definitions before implementation. A public label such as “spent” must identify which reviewed stage the source actually supports.
