# ADR-0001: Project Vision and Initial Pilot Boundary

**Status:** Accepted  
**Owner:** Maintainers  
**Proposed:** 2026-07-27  
**Accepted:** 2026-07-28  
**Deciders:** Project maintainer  
**Supersedes:** None  
**Superseded by:** None

## Context

Project IAgora currently has a documented mission and a proposed strategic roadmap but no accepted architectural decision. The repository contains no implementation, data contract, schema, or production system.

The project intends to make fragmented public information understandable and verifiable without concealing source conflicts or treating generated content as fact. Its intended civic value also requires campaign commitments to be crossed with later public data so users can inspect which commitments were fulfilled and what effects followed for the city.

This requires more than matching phrases. The system must preserve the original promise, map it to competent public action, assess delivery under a public method, and distinguish observed outcomes from causally attributable impacts. Attempting to define the complete platform before testing this governance model would create speculative documentation, while assessing an entire campaign first would risk embedding unsupported editorial judgments in the canonical model.

An initial, bounded pilot is needed to validate whether campaign commitments, assertions, evidence, authority, provenance, lineage, temporal validity, financial observations, outcomes, impacts, and Knowledge Passports can work together on real public records.

Official Clermont-Ferrand sources provide programme pages, municipal records, budget information, and open data for the “Respire à la récré” schoolyard transformation programme. The available publications also appear to use different targets and units, making the programme suitable for testing whether IAgora can preserve and explain differences without silently selecting a preferred value.

A [contemporaneous campaign interview](https://www.clermontinfos63.fr/actualite-18339-olivier-bianchi-nous-voulons-instaurer-le-droit-de-petition.html) describes schoolyard regreening as a flagship measure of the successful 2020 list. The original primary campaign artifact has not yet been acquired and must be verified before the pilot can claim a definitive campaign-to-delivery chain.

## Decision drivers

- Deliver a useful outcome for citizens and journalists without requiring a complete platform.
- Connect original campaign commitments to later decisions, resources, delivery, outcomes, and defensible impact evidence.
- Make fulfillment assessments transparent and reproducible rather than editorial or model-generated labels.
- Test the distinction between source authority and supporting evidence.
- Exercise conflicting values, temporal scope, financial stages, and institutional boundaries.
- Avoid political scoring and unsupported promise-status judgments.
- Preserve a source-agnostic canonical model that can later support other territories.
- Minimize speculative architecture and irreversible implementation choices.
- Establish inspectable accessibility, privacy, legal, and security boundaries before publication.
- Keep the initial corpus and review workload small enough to audit manually.

## Decision

Project IAgora will be designed as an evidence-driven civic knowledge platform in which campaign commitments can be crossed with public decisions, resources, delivery data, and observed effects. Every material published assertion and assessment can be inspected through its sources, evidence relationships, provenance, lineage, temporal scope, method, and uncertainty.

The first proposed product validation will be a bounded Clermont-Ferrand pilot focused on the municipal “Respire à la récré” programme.

The pilot will answer:

> As of 31 December 2025, what did the successful 2020 municipal campaign commit to regarding greener schoolyards, how was that commitment translated into public decisions, resources, and reported delivery through “Respire à la récré,” what effects were observed, and where did the evidence remain conflicting or incomplete?

The pilot will:

- acquire and preserve the original campaign commitment, or visibly record that primary verification is still missing;
- cover programme history from its reported launch in 2021 through the observation cut-off;
- examine programme-level objectives, decisions, funding statements, and reported delivery;
- include three school-level case studies selected after a documented source inventory;
- prioritize official municipal decisions, acts, budgets, financial accounts, and open data according to their authority for each fact type;
- retain official editorial pages and press material as attributed supporting evidence rather than automatically authoritative financial or legal records;
- expose atomic evidence-backed states instead of a single political completion judgment;
- support a summary fulfillment assessment only after its categories and rules are accepted and inspectable;
- distinguish delivered outputs, observed outcomes, and causally attributed impacts;
- preserve distinctions among schools, school groups, schoolyards, institutions, accounting stages, publication dates, and validity periods;
- produce a versioned Knowledge Passport representation as a pilot outcome;
- remain technology-neutral until the minimum governance model and contracts are accepted.

The pilot may state that a commitment is fulfilled, partially fulfilled, not fulfilled, changed, or not verifiable only under a separately accepted, evidence-backed methodology that exposes the underlying atomic states and limitations.

The pilot may describe observed changes using defined indicators. It may attribute those changes to the programme only when an accepted evaluation design supports the causal claim.

The pilot must not begin external publication or production acquisition until applicable licensing, retention, redaction, privacy, and security rules are accepted or explicitly recorded as blocking conditions.

## Scope

### Included

- Citizens and journalists as the primary pilot audience.
- The original 2020 campaign commitment, its campaign artifact, attribution, wording, scope, and conditions.
- City of Clermont-Ferrand as the principal programme owner and source producer.
- Other public bodies only when they issue a relevant authoritative decision, funding record, or dataset.
- Official documents, structured data, source fragments, and acquisition metadata required for the pilot question.
- Assertions, commitment mappings, fulfillment assessments, evidence relationships, conflicts, provenance, lineage, temporal validity, financial observations, outcomes, impact claims, methodological review, and Knowledge Passport exposure.
- Accessible plain-language presentation and inspectable machine-readable output.

### Excluded

- Monitoring every municipal or electoral commitment.
- Candidate rankings, political endorsements, or recommendations.
- Causal impact claims without an accepted evaluation method.
- Comparison with other cities or territories.
- General media and social-media monitoring.
- Unpublished procurement, accounting, or personal records.
- Personal data about children, families, or staff.
- Selection of application frameworks, databases, AI providers, search engines, or hosting platforms.
- A public launch date or production service commitment.

## Consequences

### Benefits

- The project gains a concrete validation target without committing to a complete platform architecture.
- Campaign-to-action traceability directly tests the project's intended civic value.
- Real differences among official publications can test conflict and scope handling.
- Programme-level and school-level views exercise both aggregation and traceability.
- The pilot can reveal whether the proposed governance concepts are understandable to non-specialists.
- Technology choices can follow observed data, review, and operating needs.
- A bounded corpus makes manual verification and accessibility review feasible.

### Drawbacks and risks

- A single education and climate-adaptation programme may not represent all civic domains.
- Official sources may be incomplete, change location, or use inconsistent identifiers and units.
- Three school case studies may expose only a subset of acquisition and financial patterns.
- Separating announcements, decisions, funding, delivery, and measured outcomes adds modeling and editorial complexity.
- Campaign wording may be ambiguous, conditional, composite, or unavailable from a stable primary source.
- Fulfillment assessment and impact attribution introduce methodological and reputational risk if their rules are unclear.
- A historical cut-off requires careful handling of evidence published later.
- The inability to publish a simple completion score may make the first output less immediately marketable.
- Legal and privacy review may delay acquisition or limit retention of otherwise public material.

### Follow-up work

- Confirm the three school case studies through a source inventory.
- Acquire and authenticate the primary 2020 campaign artifact.
- Define campaign-commitment decomposition, mapping, and fulfillment rules.
- Define the canonical assertion and evidence relationship.
- Define Source of Truth authority rules by fact type.
- Specify conflict representation and temporal behavior.
- Specify financial-observation semantics against applicable French public-accounting concepts.
- Define the minimum Knowledge Passport contract.
- Define outcome indicators, baselines, and the evidence threshold for causal impact claims.
- Adopt acquisition, licensing, retention, redaction, privacy, and security rules.
- Define methodological review roles and correction procedures.
- Establish deterministic validation and accessibility acceptance criteria.

## Alternatives considered

### Alternative A: Complete the target architecture before selecting a pilot

This would produce a comprehensive documentation set before implementation. It could improve apparent consistency and expose broad questions early. However, most decisions would be based on hypothetical needs, increasing documentary debt and the migration cost when real sources reveal different constraints.

This alternative is not proposed because it conflicts with the project's preference for simplicity before speculative scale.

### Alternative B: Assess the complete municipal campaign programme first

This could create an immediately recognizable public product and cover more political topics. It would also require a general commitment taxonomy, fulfillment methodology, source-authority policy, impact model, and editorial review process before those concepts have been validated.

This alternative is not proposed because it creates a high risk of unsupported political judgments and premature canonical modeling.

### Alternative C: Build a technology prototype using synthetic data

This could validate user-interface and infrastructure choices without legal or source-access complexity. It would not adequately test authority, real evidence conflicts, changing publications, acquisition provenance, or public-accounting semantics.

This alternative may be used for isolated technical tests, but not as the primary product-validation strategy.

### Alternative D: Use a bounded, evidence-rich municipal programme

This option limits the domain while retaining real decisions, financial records, structured data, differing official statements, and identifiable realizations. Its narrower representativeness is accepted as a pilot limitation.

This is the proposed alternative.

## Migration and rollback

No production system or public contract currently exists, so accepting this ADR would not require a technical migration.

If the pilot proves infeasible before implementation, a later ADR may supersede this decision with another bounded case while preserving the vision and the evidence gathered about feasibility. If the project vision itself changes, the superseding ADR must identify affected specifications, contracts, and public claims.

Now that this ADR is accepted, a material change requires a superseding ADR. The accepted record remains in the repository.

## Validation

The decision is ready to be considered implemented only when:

- the three case studies have a documented and reviewable source inventory;
- the original campaign commitment is preserved from a primary artifact or its absence is explicitly disclosed;
- the campaign commitment is decomposed and mapped to public action through reviewable evidence;
- any fulfillment summary is reproducible from an accepted method, atomic states, and visible inputs;
- every published pilot assertion cites a precise versioned source fragment;
- source authority is evaluated per fact type rather than by a global ranking;
- differently scoped or conflicting official values remain visible;
- acquisition, provenance, lineage, and transformation versions are reproducible;
- financial forecasts, authorizations, grants, commitments, payments, and final costs remain distinct;
- outputs, outcomes, and impacts remain distinct;
- causal attribution appears only where an accepted evaluation design supports it;
- later evidence does not silently rewrite the 31 December 2025 snapshot;
- no unsupported political or impact conclusion is generated;
- no unnecessary personal data is collected or exposed;
- the defined user journey passes documented plain-language and accessibility review;
- the Knowledge Passport exposes applicable evidence, uncertainty, conflicts, licences, and review state.

These criteria validate implementation of the decision; they do not by themselves validate the programme's political or environmental performance.

## Governance and evidence impact

- Source authority must be defined independently from evidence support.
- Campaign artifacts are authoritative for what a campaign stated, while later municipal records are evaluated for decisions, delivery, expenditure, and outcomes according to fact type.
- Raw source acquisitions must normally remain immutable and versioned, subject to governed legal, privacy, and security exceptions.
- Evidence relationships must support at least supporting, contradicting, and contextual roles.
- City and metropolitan institutions must retain separate canonical identities.
- Observation time, publication time, acquisition time, and validity time must remain distinguishable.
- Generated artifacts must remain labeled and must never be treated as evidence.
- Enforceable publication rules must use deterministic validation where practicable.
- Public output must expose material conflicts, missing evidence, and methodological limitations.
- The pilot must not use a single opaque confidence, trust, quality, or completion score.
- Fulfillment labels and impact claims must expose their methods, inputs, counterevidence, and limitations.

## Related records

- Vision: [`../vision/00_VISION.md`](../vision/00_VISION.md)
- Product scope: [`../vision/02_PRODUCT_SCOPE.md`](../vision/02_PRODUCT_SCOPE.md)
- Roadmap: [`../vision/03_ROADMAP.md`](../vision/03_ROADMAP.md)
- Glossary: [`../governance/22_GLOSSARY.md`](../governance/22_GLOSSARY.md)
- Contracts: None yet
- Related ADRs: None
- RFCs or issues: None

## Decision record

- Outcome: Accepted
- Decision date: 2026-07-28
- Deciders: Project maintainer
- Rationale for outcome: Establish campaign-to-public-data traceability, inspectable fulfillment assessment, and evidence-bounded impact analysis as IAgora's initial product direction, validated through a narrow Clermont-Ferrand pilot.

## Revision notes

- 2026-07-27: Before acceptance, expanded the proposed decision to make campaign-to-public-data linkage, fulfillment assessment, and impact evidence explicit. At that point, the ADR remained `Proposed` pending review of this material scope change.
- 2026-07-28: Accepted by the project maintainer after review of the expanded scope.
