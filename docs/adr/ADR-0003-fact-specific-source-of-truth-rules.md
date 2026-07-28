# ADR-0003: Fact-Specific Source of Truth Rules

**Status:** Accepted  
**Owner:** Maintainers  
**Proposed:** 2026-07-28  
**Accepted:** 2026-07-28  
**Deciders:** Project maintainer  
**Supersedes:** None  
**Superseded by:** None

## Context

[ADR-0001](ADR-0001-project-vision-and-pilot-boundary.md) requires IAgora to connect campaign commitments to later decisions, resources, delivery, outcomes, and defensible impact evidence. [ADR-0002](ADR-0002-canonical-assertion-and-evidence-model.md) separates source artifacts, claims, canonical assertions, evidence relationships, authority assessments, commitment mappings, conflicts, and derived assessments.

Those records still require a governed way to determine which source has the strongest authority for a particular fact. A campaign programme may establish what a list promised but cannot establish what was later spent. An adopted budget may establish authorized forecasts but cannot establish final expenditure. A municipal communication may report that work was completed but cannot, by itself, prove long-term impact or causal attribution.

A single global hierarchy such as “official source over media over civil society” would be misleading. Authority depends on institutional competence, fact type, territory, time, document status, and the exact question being answered. Several sources may be jointly authoritative or may conflict without one being silently discarded.

The project therefore needs Source of Truth rules before it can publish fulfillment or impact assessments.

## Decision drivers

- Select authority according to the fact being evaluated, not source reputation alone.
- Keep Source of Truth separate from Source of Evidence and data quality.
- Preserve original campaign wording independently from later municipal communication.
- Distinguish authorization, forecast, commitment, payment, delivery, outcome, and impact.
- Prevent an official publisher from becoming universally authoritative.
- Preserve co-authoritative and contradictory records.
- Make every authority selection explainable, versioned, and reviewable.
- Support missing, unavailable, superseded, provisional, and corrected sources.
- Avoid legal or causal conclusions unsupported by competent evidence and method.
- Remain reusable across territories and public institutions.

## Decision

IAgora will determine Source of Truth through versioned authority rules defined per fact type and scope. It will not maintain a universal ranking of publishers or source classes.

A Source of Truth is the source or governed set of sources with the strongest applicable authority for one defined fact. Selection establishes authority to speak to that fact; it does not guarantee that the source is complete, error-free, current, or supported by all available evidence.

### Authority-rule structure

Each `AuthorityRule` must define:

- rule identifier and version;
- canonical fact type;
- required institutional or legal competence;
- applicable territory and institutional scope;
- applicable temporal scope;
- required document or record status;
- publication finality and supersession behavior;
- required granularity and identifiers;
- admissible source classes;
- co-authority behavior;
- fallback behavior when the expected source is unavailable;
- conflict and escalation behavior;
- validation and review requirements;
- governing specification or decision.

Each application of a rule produces the versioned `AuthorityAssessment` required by ADR-0002.

### Authority criteria

A source is eligible to be selected only after evaluating the applicable criteria:

1. **Competence:** the source producer has authority or direct responsibility for the fact type.
2. **Authenticity:** the artifact and version can be attributed to the stated producer or lawful custodian.
3. **Status:** draft, proposal, adopted decision, executed record, correction, and archive states remain distinct.
4. **Territory:** the source covers the same geographic or administrative area as the assertion.
5. **Institution:** the source concerns the same competent public body or campaign actor.
6. **Time:** validity, event, publication, acquisition, and observation-cut-off dates are compatible with the question.
7. **Granularity:** programme, school, school group, schoolyard, budget, transaction, and indicator scopes are not conflated.
8. **Semantics:** definitions, units, accounting stages, and measurement methods are compatible.
9. **Version:** corrections and explicit supersession are applied without deleting historical versions.
10. **Accessibility of method:** a calculated or measured value exposes enough method and lineage for its intended use.

Failure on one criterion does not make a source useless. It may remain a Source of Evidence while being ineligible as Source of Truth for the fact under review.

### Authority assessment outcomes

An authority assessment will use one of these outcomes:

- **authoritative:** the source meets the governing rule for the fact and scope;
- **co-authoritative:** more than one source has complementary or shared competence and none may be omitted;
- **authoritative with limitation:** the source is authoritative only for a documented part or status of the fact;
- **not authoritative:** the source may provide evidence but does not have the required competence or scope;
- **undetermined:** the available information is insufficient to select authority safely.

Every outcome must include its fact type, scope, rule version, source version, rationale, limitations, reviewer or deterministic process, and review state.

### Pilot authority applications

The following table establishes the proposed authority pattern for the pilot. Field-level contracts and applicable French legal or accounting definitions still require dedicated specifications.

| Fact type | Expected authoritative source | Boundary |
| --- | --- | --- |
| Original campaign wording | Original programme, manifesto, profession of faith, or other authenticated campaign artifact issued by the candidate, list, or authorized campaign organization | Establishes what was stated, not whether it was later delivered |
| Campaign speaker or list attribution | Authenticated campaign artifact and competent election record where relevant | Media reporting may support attribution but does not replace the primary artifact when available |
| Election result and mandate | Record issued by the competent election or public authority | Establishes the result or office, not fulfillment of the programme |
| Adopted municipal decision | Final adopted deliberation, signed act, or competent official register | Draft agenda, summary, or press article does not replace the adopted record |
| Post-election programme objective | Adopted strategy or decision when one exists; otherwise the exact municipal publication is authoritative only for the objective it reports | Does not retroactively redefine the campaign promise |
| Initial budget authorization or appropriation | Adopted initial budget and relevant deliberations | Establishes authorized forecast, not final expenditure |
| Budget amendment | Adopted amending decision or supplementary budget | Applies only within its exercise, body, budget, and accounting scope |
| Executed expenditure | Approved financial account or competent accounting record | Must remain distinct from budget authorization, commitment, and estimated cost |
| Grant requested | Dated application or competent applicant record | Does not establish award or payment |
| Grant awarded | Award decision or agreement issued by the competent grantor | Does not establish payment or completed work |
| Procurement award or contractual obligation | Competent procurement notice, essential-data record, signed contract, or amendment according to the fact being asserted | Publication summaries may omit legally or commercially protected details |
| Reported output or completion | Competent acceptance, completion, delivery, asset, or operational record; otherwise the official report is authoritative only for the fact that completion was reported | A communication statement does not independently establish quality, outcome, or impact |
| Outcome measurement | Primary measurement dataset or evaluation record with its method, population, period, territory, and producer | Authority for the recorded measurement does not establish causal attribution |
| Causal impact | No publisher is authoritative by status alone; the conclusion must come from an accepted evaluation method applied to governed evidence | Political credit, chronology, or an official claim is insufficient |
| Fulfillment status | IAgora assessment produced under an accepted fulfillment methodology | The status is a derived assessment, not a source fact or evidence item |

### Source of Truth may be a set

Some facts require several complementary authoritative records. For example, a financial chain may require an adopted budget for authorization, a contract for legal commitment, and a financial account for execution. IAgora must not compress these different facts into one value or name one document as universally authoritative.

When two sources are co-authoritative, the public output must identify both roles and scopes.

### Fallback when the expected source is unavailable

When the governing authoritative source is missing, inaccessible, unverifiable, or not published:

1. IAgora must record the expected source class and its absence or access failure.
2. Other credible sources may be retained as Sources of Evidence.
3. A fallback source must not be silently promoted to full authority.
4. Any provisional conclusion must be labeled with its limitation and observation cut-off.
5. If the conclusion cannot be supported safely, the result must be `not verifiable` or equivalent under the accepted methodology.

Absence of the expected record is not evidence that the underlying event did not occur.

### Supersession and correction

A later publication supersedes an earlier authoritative record only when the governing rule, legal status, explicit correction, or version relationship supports supersession. Newer is not automatically more authoritative.

The earlier record remains accessible with its historical validity. An observation made under an earlier cut-off must not be silently recomputed using later evidence.

### Conflicts among authoritative sources

If apparently authoritative sources disagree, IAgora must first evaluate identity, definitions, unit, granularity, institution, territory, time, publication status, and supersession.

If the difference remains material:

- all credible authoritative values remain visible;
- a conflict record is created under ADR-0002;
- the system must not choose a preferred value without a governed rule and rationale;
- dependent fulfillment or impact assessments expose the conflict and its effect;
- manual or deterministic resolution remains versioned and reviewable.

Authority does not erase counterevidence.

### Public explanation

For every material public assertion using Source of Truth selection, IAgora must be able to expose:

- the fact type and scope being evaluated;
- the selected source version or co-authoritative set;
- why the source is competent for that fact;
- the authority-rule version;
- relevant limitations, conflicts, or missing records;
- supporting and contradictory Sources of Evidence;
- the observation cut-off and review state.

The interface must avoid unqualified labels such as “official, therefore true.”

## Required invariants

1. Authority is assessed per fact type and scope.
2. No source or publisher has universal authority.
3. Source authority and evidence relationship remain separate records.
4. Authority and data quality remain separate assessments.
5. Campaign artifacts establish campaign wording; later public action does not rewrite it.
6. Budget authorization, legal commitment, payment, output, outcome, and impact remain distinct fact types.
7. A causal impact claim requires an accepted evaluation method, not merely an authoritative publisher.
8. Missing authoritative evidence is disclosed and never converted into evidence of absence.
9. Co-authoritative and conflicting records remain visible.
10. Supersession is explicit and versioned; publication recency alone is insufficient.
11. Every public authority selection retains its rule, rationale, source version, scope, and review state.
12. Generated content cannot be a Source of Truth.

## Scope

### Included

- Logical authority rules and assessment outcomes.
- Criteria for source eligibility and scope matching.
- Pilot fact-type authority patterns.
- Co-authority, fallback, supersession, and conflict behavior.
- Public explainability requirements.
- Interaction with assertions, evidence, mappings, conflicts, and assessments from ADR-0002.

### Excluded

- Complete field-level Source of Truth and Source of Evidence schemas.
- Jurisdiction-wide legal interpretation of French administrative records.
- Complete French public-accounting semantics.
- Fulfillment-status calculation and thresholds.
- Impact-evaluation methodology.
- Automated source discovery or credibility scoring.
- Physical storage and query implementation.
- Editorial appeals and correction workflow.

## Consequences

### Benefits

- Users can understand why a source is authoritative for one fact but not another.
- Campaign promises, public decisions, spending, delivery, outcomes, and impacts cannot be silently conflated.
- Missing primary sources and provisional conclusions remain visible.
- Conflicting official records can coexist without arbitrary deletion.
- Authority rules can be reused across territories while allowing jurisdiction-specific implementations.
- Derived fulfillment assessments can cite an inspectable authority basis.

### Drawbacks and risks

- Fact-type classification and scope matching add modeling and review work.
- Legal and accounting competence may require specialist review.
- Some facts have distributed authority rather than a single clear source.
- Source status and correction mechanisms may vary across publishers.
- Conservative fallback behavior will produce `not verifiable` results where users may expect a simple answer.
- Poorly designed rules could encode institutional bias while appearing neutral.

### Follow-up work

- Implement executable authority-rule contracts from the accepted Source of Truth specification.
- Implement executable evidence-fragment and relationship contracts from the accepted Source of Evidence specification.
- Define pilot fact types and their French administrative and accounting mappings.
- Define evidence conflict comparison and resolution behavior.
- Define campaign commitment decomposition and fulfillment assessment.
- Define outcome measurement and causal impact requirements.
- Establish review roles, appeals, and correction procedures.
- Test every pilot assertion against the authority matrix and fallback rules.

## Alternatives considered

### Alternative A: Global source hierarchy

Rank source classes once, for example official records above media and civil-society sources. This is simple to implement but ignores fact-specific competence. An official communication could then incorrectly outrank an original campaign artifact for promise wording or an independent evaluation for measured effects.

This alternative is rejected.

### Alternative B: Official sources only

Restrict IAgora to official institutional sources. This simplifies acquisition and reduces some disputes, but it excludes campaign artifacts, independent evidence, and credible contradictions. It would also treat institutional publication as sufficient evidence of impact.

This alternative is rejected because it conflicts with evidence visibility and methodological neutrality.

### Alternative C: Credibility or trust score per publisher

Assign each publisher a reusable score and select the highest score. This appears scalable but collapses competence, quality, temporal validity, evidence support, and uncertainty. It also makes corrections and fact-specific exceptions difficult to explain.

This alternative is rejected.

### Alternative D: Fact-specific, versioned authority rules

Select authority using explicit competence and scope rules, permit co-authority, and retain fallback evidence and conflicts. This requires more governance work but matches the distinctions accepted in ADR-0001 and ADR-0002.

This is the proposed alternative.

## Migration and rollback

No production authority rules or stored assessments existed when this ADR was accepted, so acceptance required no data migration.

After acceptance, replacing fact-specific authority with a global ranking, merging authority into evidence relationships, or weakening the fallback and conflict invariants requires a superseding ADR. Jurisdiction-specific rule refinements may be added through versioned specifications when they do not change this decision.

## Validation

Before this decision is considered implemented:

- every pilot fact type has a versioned authority rule;
- the same source can be authoritative for one fact and not authoritative for another;
- campaign wording resolves to a primary campaign artifact or exposes its absence;
- adopted forecast and executed expenditure resolve to distinct authoritative records;
- an official completion claim remains distinct from an outcome measurement and impact conclusion;
- co-authoritative sources can be represented without collapsing their roles;
- incompatible authoritative records create a visible conflict;
- a corrected record supersedes without deleting the historical source version;
- fallback evidence cannot be silently promoted to full authority;
- public output can explain the selected source, rule, scope, limitations, conflicts, and cut-off;
- generated content is rejected as an authoritative source;
- representative pilot cases pass review by a person familiar with the relevant administrative or accounting domain.

## Governance and evidence impact

- Authority assessments become mandatory inputs for material published assertions and derived assessments.
- Source of Truth selection never removes Source of Evidence relationships.
- Legal, accounting, and causal competence must be reviewed by suitable roles or deterministic rules before publication.
- Authority rules and their changes are versioned governance artifacts.
- The Knowledge Passport must expose the applicable authority basis, conflicts, and limitations.
- AI may help locate candidate sources but cannot assign final authority without governed validation and review.

## Related records

- Vision and pilot boundary: [`ADR-0001`](ADR-0001-project-vision-and-pilot-boundary.md)
- Canonical assertion and evidence model: [`ADR-0002`](ADR-0002-canonical-assertion-and-evidence-model.md)
- Glossary: [`../governance/22_GLOSSARY.md`](../governance/22_GLOSSARY.md)
- Source of Truth specification: [`../governance/16_SOURCE_OF_TRUTH.md`](../governance/16_SOURCE_OF_TRUTH.md)
- Source of Evidence specification: [`../governance/17_SOURCE_OF_EVIDENCE.md`](../governance/17_SOURCE_OF_EVIDENCE.md)
- Related ADRs: ADR-0001, ADR-0002
- RFCs or issues: None

## Decision record

- Outcome: Accepted
- Decision date: 2026-07-28
- Deciders: Project maintainer
- Rationale for outcome: Establish versioned, fact-specific authority rules that distinguish campaign wording, public decisions, financial stages, delivery, outcomes, and causal impact while preserving co-authority, fallback evidence, supersession, and conflicts.

## Revision notes

- 2026-07-28: Accepted by the project maintainer.
- 2026-07-28: Linked the accepted Source of Truth and Source of Evidence specifications and clarified that executable contracts remain follow-up work. No decision semantics changed.
