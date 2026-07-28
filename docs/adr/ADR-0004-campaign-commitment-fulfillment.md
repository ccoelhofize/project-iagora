# ADR-0004: Campaign Commitment Decomposition and Fulfillment Assessment

**Status:** Accepted  
**Owner:** Maintainers  
**Proposed:** 2026-07-28  
**Accepted:** 2026-07-28  
**Deciders:** Project maintainer  
**Supersedes:** None  
**Superseded by:** None

## Context

[ADR-0001](ADR-0001-project-vision-and-pilot-boundary.md) establishes that IAgora should connect campaign commitments to public decisions, resources, delivery, outcomes, and defensible impact evidence. [ADR-0002](ADR-0002-canonical-assertion-and-evidence-model.md) defines campaign commitments, canonical assertions, commitment mappings, evidence, conflicts, and derived assessments as separate versioned records. [ADR-0003](ADR-0003-fact-specific-source-of-truth-rules.md) establishes authority by fact type and prevents later public communication from rewriting the original promise.

The project still needs a public method for answering which commitments were fulfilled. Campaign wording varies: a commitment may describe an action, a quantified output, an intended outcome, several conditions, or an aspiration without a deadline. A binary “kept” or “broken” label would hide this structure. A completion percentage could falsely combine unrelated components or reward strategic decomposition into many small actions.

The pilot observation cut-off is 31 December 2025, potentially before the end of the mandate associated with the 2020 campaign. The method must therefore distinguish progress from final fulfillment and must not label an unfinished but not-yet-due commitment as unfulfilled.

Fulfillment and impact also answer different questions. A promised action may be delivered without producing the intended outcome, while an outcome may improve for reasons unrelated to the action. Both must remain visible without being collapsed into one political score.

## Decision drivers

- Preserve the exact campaign wording and conditions.
- Make decomposition reproducible without inflating or shrinking the denominator.
- Distinguish implementation progress from fulfillment conclusion.
- Support action, output, outcome, and quantified-target commitments.
- Treat deadlines and observation cut-offs explicitly.
- Keep impact assessment separate unless impact is itself the promised target.
- Require fact-specific authoritative evidence and expose counterevidence.
- Avoid opaque weights, arbitrary percentages, and candidate rankings.
- Make status changes versioned, reviewable, correctable, and explainable in plain language.
- Permit AI assistance without delegating final methodological judgment to a model.

## Decision

IAgora will evaluate campaign commitments through a versioned, component-based method with two distinct outputs:

1. an **implementation state** describing evidenced public action at the observation cut-off;
2. a **fulfillment conclusion** comparing the complete evidenced state with the original commitment under explicit rules.

Neither output is evidence. Both are derived assessments under ADR-0002.

### Commitment eligibility

A statement is eligible for fulfillment assessment only when it:

- is attributable to a candidate, list, or authorized campaign actor;
- is preserved from an authenticated primary campaign artifact, or explicitly marked as primary-source unverified;
- describes a future action, output, outcome, or condition sufficiently concrete to evaluate;
- identifies or permits defensible determination of the relevant territory and responsible public competence;
- is distinguishable from general values, criticism, rhetorical aspiration, or prediction.

If primary campaign evidence is missing, IAgora may preserve secondary evidence and prepare a provisional decomposition, but the public fulfillment conclusion must be `not verifiable` until the governing method explicitly permits and labels a reviewed exception.

### Original commitment record

Before decomposition, IAgora must preserve:

- verbatim wording within lawful quotation limits;
- campaign artifact, version, location, and publication date;
- attributed candidate, list, or campaign organization;
- election, territory, and office sought;
- stated deadline, quantity, target population, conditions, and dependencies;
- relevant surrounding text needed to avoid misleading extraction;
- ambiguity and primary-source verification state.

Canonical decomposition must never replace or silently rewrite this record.

### Decomposition rules

A commitment may be decomposed into atomic components only when each component is independently verifiable and the complete set preserves the original meaning.

Each component must record:

- canonical subject, action or outcome, object, and scope;
- component type: `action`, `output`, `outcome`, `impact_target`, or `condition`;
- stated quantity, unit, baseline, target population, territory, and deadline when present;
- responsible institution or competence when evidenced;
- whether the component is `essential` or `supporting` to the commitment;
- decomposition rationale, method version, reviewer, and uncertainty;
- relationship to the original wording and sibling components.

The following rules apply:

1. Conjunctions may become separate components when they describe independently testable obligations.
2. Means and intended effects remain separate components.
3. A quantified target retains its original numerator, denominator, unit, and scope.
4. An unstated target, deadline, or weight must not be invented.
5. A mandate-end deadline may be inferred only when campaign context clearly makes the mandate the delivery horizon; the inference must be visible and reviewable.
6. Components must not be split merely to increase the number of fulfilled items.
7. Components must not be merged when doing so hides an unfulfilled obligation.
8. Editorial convenience must not change which components are essential.

### Essential and supporting components

An `essential` component expresses an obligation without which the commitment would be materially altered. A `supporting` component adds implementation detail or an ancillary condition whose absence does not negate the principal commitment.

Classification must be justified from the original wording and context. IAgora will not apply hidden numerical weights. If reasonable reviewers disagree materially, the disagreement is recorded and the fulfillment conclusion remains provisional or not verifiable until resolved.

### Implementation states

Each atomic component receives one implementation state at an observation cut-off:

- **no evidenced action:** no qualifying implementation action has been found;
- **planned:** an evidenced plan or announced implementation exists without competent authorization;
- **authorized:** a competent decision authorizes the action or resources;
- **funded:** applicable resources are evidenced at the relevant financial stage;
- **in progress:** evidenced implementation has begun but the component is not delivered;
- **delivered:** the promised action or output is evidenced as completed within scope;
- **outcome observed:** the promised outcome target is measured under an accepted indicator definition;
- **discontinued:** competent evidence shows implementation ended before delivery;
- **unknown:** available evidence cannot establish the state safely.

These states describe evidence, not political merit. More than one underlying milestone may exist, but the public summary uses the most advanced state supported for the exact component and cut-off. Financial authorization alone must not produce `delivered`.

### Fulfillment conclusions

The commitment-level conclusion uses one of these labels:

- **fulfilled:** every essential component due by the cut-off is fulfilled under its component rule, with no unresolved conflict capable of changing the conclusion;
- **partially fulfilled:** at least one material essential component due by the cut-off is fulfilled or measurably advanced, while another remains unmet, incomplete, reduced, or outside the promised scope;
- **not fulfilled:** the applicable deadline has passed and one or more essential components remain unmet, were discontinued, or are contradicted by authoritative evidence, with sufficient evidence to conclude non-fulfillment;
- **changed:** competent later action materially replaces the commitment's objective, scope, target, or delivery mechanism such that direct fulfillment comparison would mislead;
- **not yet assessable:** the applicable deadline has not passed and the evidence does not yet support a final conclusion;
- **not verifiable:** the original commitment, implementation evidence, scope, or method is insufficient or materially conflicted such that no safe conclusion can be reached.

`Changed` is descriptive, not a positive or negative judgment. A changed commitment may also expose implementation progress, but it must not be relabeled fulfilled solely because a different action occurred.

### Component fulfillment rules

Component evaluation depends on the promise type:

- **action commitment:** fulfilled when the specified competent action is completed within its conditions and scope;
- **output commitment:** fulfilled when the promised deliverable and quantity are evidenced within scope;
- **outcome commitment:** fulfilled when the accepted indicator reaches the stated target under the stated period and population;
- **impact-target commitment:** fulfilled only when the promised impact measure is observed; causal attribution is required only if the wording promises that the intervention will cause the change;
- **condition:** fulfilled when the stated constraint or dependency is satisfied.

A component may be partially fulfilled only when partiality has a defensible basis, such as a compatible quantitative denominator, separable geographic coverage, or independently evidenced subcomponents. Narrative impressions are insufficient.

### Quantitative progress

A progress ratio may be calculated only when:

- the original commitment contains or clearly defines a quantitative target;
- numerator and denominator use compatible definitions, units, territory, population, and period;
- the data lineage and rounding rule are recorded;
- later target changes do not silently replace the original denominator.

The displayed ratio is:

`evidenced compatible delivery / original compatible target`

IAgora may show delivery above the original target rather than silently cap the result at 100%. The fulfillment label remains governed by the original conditions and essential components.

Ratios must not be averaged across heterogeneous components or commitments. IAgora will not publish an overall candidate, list, or administration fulfillment percentage until a separate accepted decision establishes a defensible aggregation method and its risks.

### Deadlines and observation cut-offs

Fulfillment is evaluated at an explicit observation cut-off.

- A stated campaign deadline governs when compatible with the commitment.
- If the campaign clearly commits delivery during the mandate but gives no date, the mandate end may be used with a visible inference record.
- If no defensible deadline exists, `not fulfilled` must not be inferred solely from elapsed time.
- Evidence published after the cut-off may inform a later assessment version but must not rewrite the historical result.
- An early assessment normally uses `not yet assessable`, while still exposing implementation progress.

### Relationship to impact

Fulfillment and impact are separate assessments:

- fulfillment asks whether the commitment was delivered as stated;
- outcome measurement asks what changed;
- impact assessment asks whether and to what extent the intervention caused a material change.

An action commitment may be fulfilled even when its impact is unknown, neutral, or adverse. Conversely, an improved city indicator does not fulfill a promised action that was not performed.

When the original promise is itself an outcome or impact target, the target is evaluated as a component, but causal language still requires the methodology accepted for impact attribution.

### Evidence and authority requirements

Every component state and fulfillment conclusion must retain:

- original campaign evidence;
- commitment mapping versions;
- fact-specific authority assessments under ADR-0003;
- supporting, contradictory, and contextual evidence;
- unresolved conflicts and their materiality;
- observation cut-off;
- method and rule version;
- reviewer role, review state, rationale, and limitations.

Absence of evidence is not evidence of non-fulfillment. `Not fulfilled` requires positive evidence or a sufficiently complete authoritative record showing that a due essential obligation was not met.

### Review and correction

AI may propose extraction, decomposition, mappings, and candidate states. It must not assign the final public fulfillment conclusion.

Before public release:

- the decomposition must be reviewed by a role distinct from the automated or human extractor;
- the evidence and authority basis must be reviewed;
- every summary conclusion must receive a methodological review;
- material reviewer disagreement must remain visible or block final publication;
- corrections create new assessment versions and preserve the earlier public state;
- challenges and appeals must be attributable to evidence and resolved through a future governed workflow.

Reviewer identity should be recorded by role unless a stronger accountability requirement is accepted, avoiding unnecessary personal data.

### Public explanation

For each assessed commitment, the public view must expose:

- original wording and campaign source;
- decomposition into essential and supporting components;
- deadline and observation cut-off;
- implementation state for each component;
- fulfillment conclusion and rule version;
- authoritative sources and precise evidence;
- counterevidence, conflicts, missing information, and uncertainty;
- separate output, outcome, and impact information;
- review and correction state.

Plain-language explanation must accompany methodological terms.

## Method quality requirements and guardrails

The method will use integrity requirements rather than targets for political outcomes.

### Required integrity measures

- **citation coverage:** 100% of published factual component states and conclusions have precise evidence citations;
- **authority coverage:** 100% of material published component states identify the applicable authority assessment or disclose that authority is undetermined;
- **method coverage:** 100% of published conclusions identify the method and rule version;
- **review coverage:** 100% of public summary conclusions have completed methodological review;
- **conflict disclosure:** 100% of known material conflicts affecting a conclusion are exposed.

These are publication requirements, not evidence that the method is unbiased or correct.

### Diagnostic measures

IAgora may monitor the distribution of conclusions, the share of primary-source-unverified commitments, the share of `not verifiable` results, review effort, correction rate, and inter-reviewer disagreement.

These measures are diagnostic. They must not become targets that encourage reviewers to increase fulfillment rates, reduce `not verifiable` outcomes, suppress conflicts, or avoid corrections.

### Guardrails

- Never optimize for a higher or lower political fulfillment rate.
- Never compare candidates or administrations using raw counts without compatible corpus, scope, dates, and method versions.
- Never interpret `not verifiable` as `not fulfilled`.
- Never treat spending volume as delivery or impact by itself.
- Never hide changed scope, missed conditions, or counterevidence behind a headline percentage.
- Never use model confidence as methodological confidence.

## Required invariants

1. Original campaign wording remains immutable and inspectable.
2. Decomposition preserves the full meaning and cannot be used to manipulate the denominator.
3. Implementation state and fulfillment conclusion remain separate.
4. Essential and supporting classifications have explicit rationale.
5. Deadlines and observation cut-offs are explicit.
6. `Not fulfilled` is not assigned before the applicable deadline or from evidence absence alone.
7. Quantitative ratios use compatible definitions, units, territory, population, and period.
8. Heterogeneous components and commitments are not averaged.
9. Fulfillment, outcome, and causal impact remain separate.
10. Every public conclusion retains evidence, authority, method, lineage, counterevidence, and review state.
11. Material conflicts remain visible and may block a final conclusion.
12. AI cannot assign the final public fulfillment conclusion.
13. Corrections create new assessment versions without erasing history.
14. Fulfillment distribution is never an optimization target.

## Scope

### Included

- Commitment eligibility and source requirements.
- Atomic decomposition and essential/supporting classification.
- Implementation states and fulfillment conclusions.
- Component-type evaluation rules.
- Quantitative progress, deadlines, and observation cut-offs.
- Separation of fulfillment, outcomes, and impact.
- Evidence, authority, review, explanation, and correction requirements.
- Method-integrity measures and anti-gaming guardrails.

### Excluded

- Aggregated ranking or score for a candidate, list, mandate, or administration.
- Exact causal impact-evaluation design.
- Final field-level data contracts and API payloads.
- User-interface design.
- Full appeals, moderation, or publication governance workflow.
- Selection of the complete campaign corpus beyond the pilot.
- Benchmark targets for review cost, speed, or disagreement.

## Consequences

### Benefits

- Citizens can inspect how a headline conclusion follows from the original promise and evidence.
- Progress before a deadline is visible without premature failure labels.
- Quantified and qualitative commitments can be evaluated without a universal percentage.
- Impact evidence remains visible without being confused with delivery.
- Anti-gaming rules reduce incentives to manipulate decomposition or denominators.
- Historical assessments can be reproduced at their original cut-off.

### Drawbacks and risks

- Decomposition and review require substantial human and domain effort.
- Essential-component classification can remain contestable.
- Some commitments will legitimately remain `not verifiable` or `not yet assessable`.
- The absence of an overall score may frustrate users seeking a simple ranking.
- Different method versions may limit comparisons over time.
- Political actors may contest labels even when evidence and rules are public.
- Requiring independent review may constrain publication speed and operating cost.

### Follow-up work

- Create the normative fulfillment methodology specification and data contract.
- Define the pilot campaign corpus and authenticate the primary commitment artifact.
- Define component, implementation-state, and assessment schemas.
- Define conflict materiality and resolution behavior.
- Define outcome indicators and causal impact methodology.
- Establish reviewer roles, appeals, corrections, and publication governance.
- Test decomposition and assessment on the pilot commitment before expanding the corpus.
- Conduct plain-language and accessibility review with representative users.

## Alternatives considered

### Alternative A: Binary kept or broken label

This is simple and recognizable but hides partial delivery, deadlines, changed scope, missing evidence, and heterogeneous components. It encourages political judgment unsupported by the record.

This alternative is rejected.

### Alternative B: Universal completion percentage

Calculate delivered items divided by promised items. This appears comparable but depends on arbitrary decomposition, weights unlike obligations equally, and confuses action, output, outcome, and impact. It is easy to game.

This alternative is rejected for commitment and administration-level assessment.

### Alternative C: Editorial narrative without formal states

Publish a sourced explanation without standardized states. This preserves nuance and lowers modeling cost but makes results difficult to compare, validate, reproduce, and correct consistently.

This alternative may complement but cannot replace the structured method.

### Alternative D: Component method with separate progress and fulfillment

Preserve original wording, decompose under explicit rules, expose component progress, and derive a limited fulfillment conclusion with evidence and review. This is more costly but directly supports IAgora's accepted mission and guardrails.

This is the proposed alternative.

## Migration and rollback

No production fulfillment assessments existed when this ADR was accepted, so acceptance required no data migration.

After acceptance, changing the conclusion taxonomy, essential-component semantics, deadline rules, or separation of fulfillment and impact requires a superseding ADR and an assessment migration plan. Method refinements that preserve these decisions may be introduced through versioned specifications, but historical results retain their original method versions.

## Validation

Before this decision is considered implemented:

- the original pilot commitment is authenticated or clearly marked primary-source unverified;
- independent reviewers can reproduce its decomposition from the original wording;
- every component has type, scope, deadline, essentiality, and rationale;
- implementation states resolve from evidence without being mistaken for fulfillment conclusions;
- an assessment before the mandate deadline can return `not yet assessable` while showing progress;
- `not fulfilled` cannot be produced solely from missing evidence;
- quantitative progress rejects incompatible numerator and denominator definitions;
- changed scope is visible and cannot silently become fulfilled;
- output delivery does not automatically produce an impact conclusion;
- every public conclusion satisfies citation, authority, method, review, and conflict-disclosure requirements;
- AI-proposed decomposition and mappings remain distinguishable from reviewed records;
- corrections create a new version and preserve the historical assessment;
- plain-language review confirms that non-specialists can distinguish progress, fulfillment, and impact.

## Governance and evidence impact

- Fulfillment becomes an explicit derived assessment, never a raw fact.
- Original campaign artifacts and later public records retain distinct authority roles.
- Review rationale and material disagreement become part of the Knowledge Passport.
- Method versions govern comparability across commitments and time.
- Public corrections preserve the earlier conclusion and explain the change.
- Accessibility and plain-language explanation are publication requirements.
- No administration-level fulfillment score may be introduced without a later accepted ADR.

## Related records

- Vision and pilot boundary: [`ADR-0001`](ADR-0001-project-vision-and-pilot-boundary.md)
- Canonical assertion and evidence model: [`ADR-0002`](ADR-0002-canonical-assertion-and-evidence-model.md)
- Fact-specific Source of Truth rules: [`ADR-0003`](ADR-0003-fact-specific-source-of-truth-rules.md)
- Product scope: [`../vision/02_PRODUCT_SCOPE.md`](../vision/02_PRODUCT_SCOPE.md)
- Glossary: [`../governance/22_GLOSSARY.md`](../governance/22_GLOSSARY.md)
- Fulfillment methodology specification: Planned
- Related ADRs: ADR-0001, ADR-0002, ADR-0003
- RFCs or issues: None

## Decision record

- Outcome: Accepted
- Decision date: 2026-07-28
- Deciders: Project maintainer
- Rationale for outcome: Establish component-based campaign commitment assessment with separate implementation and fulfillment states, explicit deadlines and evidence, impact separation, reproducible review, and anti-gaming guardrails.

## Revision notes

- 2026-07-28: Accepted by the project maintainer.
