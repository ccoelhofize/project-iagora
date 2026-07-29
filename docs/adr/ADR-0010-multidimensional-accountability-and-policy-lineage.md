# ADR-0010: Multidimensional Accountability Views and Policy Lineage

**Status:** Accepted
**Owner:** Maintainers
**Proposed:** 2026-07-29
**Accepted:** 2026-07-29
**Deciders:** Project maintainer
**Supersedes:** None
**Superseded by:** None

## Context

[ADR-0004](ADR-0004-campaign-commitment-fulfillment.md) separates component implementation states from commitment-level fulfillment conclusions. [ADR-0005](ADR-0005-outcome-measurement-and-causal-impact.md) separates inputs, activities, outputs, outcomes, and causal impact. The accepted model therefore already prevents spending, delivery, observed change, and impact from becoming interchangeable.

The public product still needs a consistent way to present these dimensions together. A citizen may reasonably want to know whether a commitment was fulfilled, what was implemented, how much was authorized or spent, what was delivered, what changed, and whether an initiative was new or continued earlier public action. A single label, percentage, or financial number cannot answer all of those questions safely.

The current local pilot is a detailed evidence report for one bounded commitment. The intended product experience is broader: a territory dashboard with thematic summaries, indicator drill-down, evidence-linked programme and commitment views, and printable reports. The same governed records must support each view without changing meaning between the dashboard and the report.

Policy chronology creates a separate attribution risk. An action announced after an election may have been designed, authorized, or funded earlier. A later administration may continue, extend, accelerate, rename, reorient, or replace earlier work. Dates and political identity alone do not establish institutional lineage or political credit.

## Decision drivers

- Give non-specialists a concise overview without hiding evidence or uncertainty.
- Preserve the accepted fulfillment taxonomy and causal-claim classes.
- Distinguish financial stages, periods, scopes, and institutions.
- Avoid treating expenditure as delivery, fulfillment, outcome, or impact.
- Make continuity and novelty reviewable without assigning political merit.
- Support territory, theme, indicator, programme, commitment, and report views from the same governed records.
- Keep missing, conflicting, differently scoped, and incomparable values visible.
- Prevent a citywide or administration-wide opaque composite score.
- Require accessible non-visual alternatives for every chart.
- Keep the initial implementation simple and compatible with a modular monolith.

## Decision

IAgora will use a multidimensional public-accountability projection. Public summaries MUST keep the following dimensions distinct and linked to their underlying records:

1. **fulfillment:** the commitment-level conclusion governed by ADR-0004;
2. **implementation:** the evidenced component states and milestones governed by ADR-0004;
3. **financial execution:** stage-qualified financial observations;
4. **outputs:** directly delivered goods, works, or services;
5. **outcomes and impact:** indicator observations and causal-claim classes governed by ADR-0005;
6. **policy lineage:** a versioned assessment of relationships to earlier or concurrent public action;
7. **evidence and review:** authority, support, conflict, uncertainty, cut-off, and review state.

These dimensions MAY appear together in a dashboard card, detail page, timeline, or report. They MUST NOT be collapsed into a single completion, trust, performance, or political-credit score.

### Fulfillment and verification semantics

The fulfillment conclusions accepted by ADR-0004 remain unchanged: `fulfilled`, `partially fulfilled`, `not fulfilled`, `changed`, `not yet assessable`, and `not verifiable`.

A public view MUST NOT describe a commitment as “fulfilled but not verifiable.” When evidence supports actions but not a global conclusion, the view SHOULD say, in plain language, “actions documented; overall fulfillment not verifiable” or an equivalent formulation. When an official source claims completion without sufficient independent support, IAgora records an attributable official claim or reported milestone; it does not silently promote that claim to `fulfilled`.

`Partially fulfilled` requires the defensible basis established by ADR-0004. Missing evidence, an editorial impression, expenditure alone, or arbitrary equal weighting cannot produce partial fulfillment.

### Financial execution

Every displayed amount MUST retain:

- amount, currency, and price basis when relevant;
- exact financial or accounting stage;
- institution and programme, project, site, or contract scope;
- covered period and observation date;
- source authority, precise evidence, and known limitations;
- relationship to other amounts, including overlap or incompatibility;
- calculation and rounding lineage for any derived value.

Relevant stages MAY include an announced estimate, multi-year programme, budget authorization, annual appropriation or payment credit, grant requested, grant awarded, legal commitment, mandate or expenditure order, payment, and final cost. A source-specific term MUST be preserved and mapped to a canonical stage only under a reviewed accounting definition.

A generic “spent” label MUST NOT hide whether the source proves a commitment, mandate, payment, or closed final cost. A mandate or expenditure order is not automatically proof of disbursement by the public accountant.

IAgora MAY calculate a financial execution ratio only when numerator and denominator use compatible stages, definitions, periods, institutions, and scopes. Overlapping or differently scoped amounts MUST NOT be summed. Programme-level expenditure MUST NOT be allocated to a site without evidence supporting that allocation.

### Indicator presentation

A territory or thematic summary MAY feature one or two primary indicators when each indicator has the versioned definition required by ADR-0005. Selection MUST be documented before interpretation and consider relevance, actionability, comparability, resistance to gaming, accessibility, and data fitness.

Primary indicators MUST NOT suppress adverse, conflicting, or inconclusive results. A dashboard MAY expose additional indicators through drill-down, but progressive disclosure MUST NOT hide material limitations or counterevidence.

A macro territory view SHOULD use separate series, small multiples, or another form that preserves units and definitions. It MUST NOT average incomparable domains such as education, finance, culture, and public safety into an unexplained city score.

### Policy lineage

A `PolicyLineageAssessment` is a versioned derived assessment relating a programme, decision, resource, output, or commitment to earlier or concurrent public action. It may express one or more of these reviewed relationships:

- **new initiative:** no qualifying predecessor is established after a proportionate search and the evidence supports a materially new public action;
- **continuation:** the competent records preserve substantially the same objective, scope, and delivery chain;
- **extension:** an earlier action is expanded to additional scope, population, territory, resources, or outputs;
- **acceleration:** an earlier action continues with an evidenced change in delivery pace or timetable;
- **reorientation:** the objective, method, target population, or delivery model changes materially while a lineage remains evidenced;
- **renaming or reframing:** terminology or public presentation changes without sufficient evidence of a materially new action;
- **replacement:** a competent later action supersedes an earlier one;
- **indeterminate:** available evidence cannot establish the lineage safely.

More than one relationship may apply to different components or periods. A public summary MUST expose the underlying dated events, compared scopes, evidence, counterevidence, search boundary, method version, and review state.

Chronology, shared vocabulary, political identity, or implementation after an election is insufficient by itself. An election boundary MAY be shown as context but MUST NOT be represented as proof of causation, ownership, novelty, or political credit.

### Policy-lineage visualization

The preferred public visualization is an evidence-linked timeline with distinct lanes for:

- earlier decisions and programmes;
- campaign commitments;
- later competent decisions and financial stages;
- implementation and delivered outputs;
- outcome and impact observations.

Confirmed relationships and proposed relationships MUST use distinguishable non-color cues. Missing periods remain gaps rather than zeros. Every visual mark supporting a material conclusion links to its source or Knowledge Passport entry, and every chart has an equivalent structured table or narrative.

### Consistent product projections

Territory dashboards, thematic dashboards, indicator pages, programme or commitment detail pages, and printable reports are projections of the same canonical and governance records. They MUST preserve equivalent material meaning, observation cut-off, filter state, method version, evidence links, uncertainty, conflicts, and correction state.

A printable report is an export view, not a separate assessment or truth store. It records its generation time, selected territory and period, filters, data and method versions, and material limitations.

## Scope

### Included

- Coordinated public presentation of fulfillment, implementation, finance, outputs, outcomes, impact, policy lineage, and evidence state.
- Financial-stage separation and compatibility rules for derived ratios.
- Policy-lineage relationship classes and evidence requirements.
- Dashboard-to-detail and dashboard-to-report semantic consistency.
- Accessible and evidence-linked timeline and chart requirements.
- Anti-gaming rules for primary indicators and macro views.

### Excluded

- Changes to the fulfillment taxonomy accepted in ADR-0004.
- Changes to causal-claim classes accepted in ADR-0005.
- Final field-level schemas, API payloads, or visualization components.
- Selection of final Clermont-Ferrand macro or thematic indicators.
- A city, administration, party, or candidate composite score or ranking.
- Political-credit attribution.
- Cost-benefit or cost-effectiveness methodology.
- SaaS hosting, tenancy, billing, identity, framework, or analytics-provider choices.
- Approval to publish the current local pilot.

## Consequences

### Benefits

- Citizens can distinguish promise fulfillment from activity, expenditure, delivery, observed change, and impact.
- Financial figures retain their accounting meaning and comparable scope.
- Continuity and novelty become inspectable rather than editorial assertions.
- One governed record can support overview, exploration, evidence review, and print without semantic drift.
- Missing evidence remains visible without being converted to zero or failure.

### Drawbacks and risks

- The model requires more records, review effort, accounting expertise, and explanation than a single dashboard score.
- Policy lineage can remain contestable even with a documented method.
- Some themes will lack one or two sufficiently mature primary indicators.
- Dense evidence and caveats can overwhelm users unless information hierarchy is tested carefully.
- Cross-period and cross-territory comparability may remain limited after normalization.
- Printable exports require separate accessibility and pagination testing while preserving the interactive view's meaning.

### Follow-up work

- Define field-level `PolicyLineageAssessment` and dashboard-projection contracts.
- Extend the financial vocabulary through qualified French public-accounting review.
- Select pilot indicators only after ADR-0005 readiness checks.
- Prototype the policy-lineage timeline with a structured-table equivalent.
- Test that dashboard, detail, passport, and report projections remain semantically consistent.
- Conduct citizen, journalistic, accounting, policy-history, accessibility, privacy, and security review.

## Alternatives considered

### Alternative A: One composite city or political-performance score

This offers a simple headline but requires hidden or contestable normalization and weighting across unrelated domains. It encourages ranking, hides missing evidence, and conflicts with the accepted anti-gaming principles.

This alternative is not proposed.

### Alternative B: Report-only publication

Publish only long evidence reports. This preserves nuance and simplifies navigation, but it does not support rapid territory-level orientation or thematic monitoring and does not match the intended public product.

This alternative is not proposed as the primary experience. Reports remain an export and review format.

### Alternative C: Dashboard summaries without mandatory evidence drill-down

This reduces interface complexity but permits semantic drift, unsupported graphics, and inaccessible or unexplained KPI selection.

This alternative is not proposed.

### Alternative D: Multidimensional dashboard with evidence-linked drill-down

Present a small number of distinct dimensions and primary indicators, then allow users to inspect definitions, lineage, sources, methods, and reports. This adds governance and design cost but best matches IAgora's mission.

This is the proposed alternative.

## Migration and rollback

No production dashboard, public API, or published assessment exists. The current local report prototype remains a bounded review artifact and requires no destructive migration.

If this proposal is accepted, future schemas and views will be versioned. Existing pilot snapshots remain reproducible under their original contracts. A later reversal can retire the new projection while preserving policy-lineage and financial assessment history; published records would require explicit supersession rather than silent reinterpretation.

## Validation

Before this decision is considered implemented:

- a summary cannot produce “fulfilled but not verifiable” or treat a reported milestone as reviewed fulfillment;
- financial observations at incompatible stages, periods, or scopes cannot be summed or divided;
- programme expenditure cannot become a site-level amount without supporting evidence;
- a policy-lineage assessment can return `indeterminate` without implying novelty;
- chronology or an election boundary alone cannot produce a lineage or political-credit conclusion;
- every primary indicator resolves to a complete versioned definition and visible selection rationale;
- missing values remain distinguishable from zero in data, charts, tables, and reports;
- a dashboard item links to the same evidence and method versions as its detail and printable report;
- every visualization has an understandable non-visual equivalent and passes keyboard, screen-reader, contrast, zoom, and print checks;
- security and privacy review confirms that thematic views, especially public-safety views, do not expose unnecessary personal or small-cell information;
- representative users can distinguish financial authorization, expenditure, delivery, fulfillment, outcome, impact, and policy lineage.

## Governance and evidence impact

- Public summaries remain derived projections and never become evidence.
- Financial source terms and canonical mappings retain provenance and review.
- Policy lineage becomes an evidence-backed, versioned, correctable assessment rather than an editorial label.
- Dashboard and report exports extend the Knowledge Passport projection model rather than create another truth store.
- Material conflicts, missing evidence, cut-offs, and method versions remain visible at every navigation level.
- AI may propose classifications, timelines, indicator mappings, or explanations but cannot supply evidence or final review authority.
- Public-safety indicators require aggregation, minimization, small-cell protection, and anti-stigmatization review.

## Related records

- Specifications: [`../vision/00_VISION.md`](../vision/00_VISION.md), [`../architecture/11_FRONTEND.md`](../architecture/11_FRONTEND.md), [`../architecture/06_DATA_MODEL.md`](../architecture/06_DATA_MODEL.md), [`../governance/22_GLOSSARY.md`](../governance/22_GLOSSARY.md), [`../governance/23_KNOWLEDGE_PASSPORT.md`](../governance/23_KNOWLEDGE_PASSPORT.md)
- Contracts: Planned policy-lineage and dashboard-projection contracts
- Related ADRs: [ADR-0002](ADR-0002-canonical-assertion-and-evidence-model.md), [ADR-0003](ADR-0003-fact-specific-source-of-truth-rules.md), [ADR-0004](ADR-0004-campaign-commitment-fulfillment.md), [ADR-0005](ADR-0005-outcome-measurement-and-causal-impact.md), [ADR-0006](ADR-0006-minimum-knowledge-passport-contract.md), [ADR-0008](ADR-0008-public-source-acquisition-privacy-and-security-boundaries.md)
- RFCs or issues: None

## Decision record

- Outcome: Accepted
- Decision date: 2026-07-29
- Deciders: Project maintainer
- Rationale for outcome: Preserve separate, evidence-linked views of fulfillment, implementation, finance, outputs, outcomes, impact, policy lineage, and review while establishing dashboard-to-detail and printable-report consistency without a composite political score.

## Revision notes

- 2026-07-29: Initial proposal created after maintainer validation of the formalization scope.
- 2026-07-29: Accepted by the project maintainer.
