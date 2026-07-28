# ADR-0005: Outcome Measurement and Causal Impact Attribution

**Status:** Accepted  
**Owner:** Maintainers  
**Proposed:** 2026-07-28  
**Accepted:** 2026-07-28  
**Deciders:** Project maintainer  
**Supersedes:** None  
**Superseded by:** None

## Context

[ADR-0001](ADR-0001-project-vision-and-pilot-boundary.md) requires IAgora to connect campaign commitments to public action and defensible impact evidence. [ADR-0002](ADR-0002-canonical-assertion-and-evidence-model.md) separates observations, calculations, inferences, evidence, and derived assessments. [ADR-0003](ADR-0003-fact-specific-source-of-truth-rules.md) establishes that no publisher is authoritative for causal impact by status alone. [ADR-0004](ADR-0004-campaign-commitment-fulfillment.md) separates implementation, fulfillment, outcomes, and impact.

The project still needs rules for measuring outcomes and deciding when an observed change may be attributed to a public intervention. A completed action can precede a change without causing it. Weather, demographic change, another public programme, selection into treatment, measurement changes, spillovers, or general trends may explain all or part of the observation.

The European Commission's [Better Regulation Toolbox](https://commission.europa.eu/law/law-making-process/better-regulation/better-regulation-guidelines-and-toolbox/better-regulation-toolbox_en) distinguishes monitoring outputs and results from evaluation of impacts and identifies counterfactual methods for causal effects. France Stratégie's [guide on combining quantitative and qualitative methods](https://www.strategie.gouv.fr/files/files/Publications/Rapport/fs-2022-rapport-evaluations-quantitatives-qualitatives-decembre_0.pdf) emphasizes both counterfactual reasoning and examination of competing explanations. INSEE's [public-policy evaluation methods](https://www.insee.fr/fr/statistiques/1380865) describe identification assumptions and experimental or quasi-experimental approaches.

IAgora should expose useful descriptive outcomes even when causal attribution is impossible. It must not overstate those observations as impact, nor suppress qualitative evidence that explains mechanisms, context, distribution, and unintended effects.

## Decision drivers

- Distinguish outputs, observed outcomes, associations, contribution evidence, and causal effects.
- Define indicators before interpreting movement.
- Preserve baselines, targets, populations, territories, units, and time horizons.
- Require a credible counterfactual or explicit contribution method for causal language.
- Select evaluation designs appropriate to the question, intervention, data, ethics, and context.
- Report effect size, uncertainty, assumptions, missingness, and robustness rather than a binary significance claim.
- Prevent extrapolation from three pilot schools to the whole city without supporting design.
- Examine distributional effects, unintended harms, and contextual drivers.
- Avoid inventing targets when the campaign or policy did not specify them.
- Make analytical code, formulas, exclusions, and transformations reproducible.
- Protect children and other potentially vulnerable populations through data minimization.

## Decision

IAgora will use a versioned, fit-for-purpose measurement and evaluation framework. Monitoring will describe implementation and observed outcomes. Impact attribution will be published only when the evaluation design supports the exact causal claim.

### Theory of change

Every outcome or impact evaluation must begin with an explicit theory of change connecting:

1. inputs and resources;
2. activities and decisions;
3. delivered outputs;
4. near-term outcomes;
5. longer-term impacts;
6. assumptions and contextual factors;
7. possible unintended effects and spillovers.

The theory is a testable model, not evidence that the pathway occurred. Each link must identify what evidence could support, contradict, or leave it unresolved.

### Indicator definition

Every published indicator requires a versioned `IndicatorDefinition` containing:

- canonical identifier and name;
- decision or evaluation question it informs;
- indicator stage: `input`, `activity`, `output`, `outcome`, `impact`, `context`, or `guardrail`;
- concept and population measured;
- numerator, denominator, formula, and aggregation rule when applicable;
- unit, direction, scale, and interpretation;
- territorial and institutional scope;
- reference period, measurement frequency, and time horizon;
- baseline definition and baseline period;
- target and target provenance when one exists;
- source authority and evidence lineage;
- inclusion, exclusion, missingness, and small-cell rules;
- measurement method, instrument, software, and version;
- known validity, reliability, comparability, and fitness-for-use limitations;
- privacy, licence, retention, and accessibility constraints;
- owner, review state, and supersession relationship.

An indicator name without these semantics is insufficient for public comparison.

### Metric selection

Each evaluation should select:

- one to three primary outcome indicators that directly reflect the evaluation question;
- a limited number of output or mechanism indicators that help explain how change could occur;
- one or two guardrail indicators for material harms, inequity, quality loss, or resource trade-offs;
- contextual indicators for major external drivers that could affect interpretation.

More indicators may be retained as exploratory, but they must be labeled and must not displace the primary outcomes after results are observed.

Indicators are selected for relevance, decision usefulness, measurable signal, influenceability, operational feasibility, resistance to gaming, and fitness for the target population and cadence. Proxies must disclose what they fail to measure.

### Targets and benchmarks

Indicator selection and target setting are separate decisions.

- If the campaign commitment specifies a compatible target, that original target governs fulfillment assessment.
- A later administrative target may be shown separately but must not rewrite the campaign denominator.
- When no target was stated, IAgora must not invent one to create a fulfillment threshold.
- Historical values, comparable territories, technical standards, or policy benchmarks may provide context only when their definitions and scopes are compatible.
- Provisional targets require their anchor, assumptions, confidence, and version.

A benchmark is not automatically a causal counterfactual.

### Baseline and observation plan

A baseline must represent the outcome before exposure to the intervention under a compatible definition and measurement method. When a valid pre-intervention baseline is unavailable, the gap must be disclosed and causal options narrowed accordingly.

Each `MeasurementPlan` must record:

- purpose and intended decision;
- evaluation questions;
- unit of analysis and target population;
- intervention, exposure, timing, and implementation variation;
- theory of change;
- primary, mechanism, guardrail, and context indicators;
- baseline and follow-up periods;
- data sources, linkage, access, and quality checks;
- planned subgroup and distributional analysis;
- evaluation design and identification assumptions;
- analysis, uncertainty, robustness, and missing-data methods;
- privacy, ethics, security, licence, retention, and publication constraints;
- method owner, reviewers, version, and deviations.

Prospective plans should be versioned before outcome analysis. Retrospective evaluations must be labeled as such and disclose that design choices were made after implementation or data availability.

### Outcome observation

An `OutcomeObservation` reports a measured value or change under a defined indicator. It must retain the indicator version, source, period, population, territory, method, uncertainty, missingness, and lineage.

An observation may support statements such as “the measured outcome changed under this definition.” It does not by itself support “the intervention caused the change.”

### Causal-claim classes

IAgora will use descriptive classes rather than a numeric evidence score:

- **observed change:** a compatible outcome difference is measured over time or across groups without a design that isolates intervention effect;
- **association:** intervention exposure and outcome vary together under a stated statistical or qualitative analysis, but competing causal explanations remain;
- **contribution supported:** the theory of change, implementation evidence, temporal sequence, mechanisms, context, and competing explanations have been examined and support a bounded contribution claim without a defensible net-effect estimate;
- **causally attributed:** an experimental or quasi-experimental design provides a credible estimate of the counterfactual outcome under explicit identification assumptions and robustness checks;
- **causal status not verifiable:** data, design, comparability, or assumptions are insufficient for a safe causal conclusion.

The classes describe different claim types, not a universal ranking of programme value. `Contribution supported` must not be rewritten as a quantified causal effect.

### Requirements for causal attribution

A `causally attributed` claim requires:

- a precise causal question and estimand;
- defined intervention or exposure;
- defined outcome, population, territory, and time horizon;
- a credible counterfactual or comparison strategy;
- an evaluation design appropriate to assignment and data generation;
- explicit identification assumptions and threats;
- handling of selection, confounding, contamination, spillovers, and concurrent interventions;
- compatible pre-intervention and follow-up data when required;
- effect estimate with uncertainty interval and practical interpretation;
- missing-data, sensitivity, falsification, and robustness checks appropriate to the design;
- code, formulas, data versions, exclusions, and transformations in the lineage record;
- review by a role with suitable evaluation-method expertise;
- limits on internal validity, external validity, and generalization.

Chronology, political credit, official publication, a before-and-after difference, or statistical significance alone is insufficient.

### Fit-for-purpose evaluation designs

Possible designs include:

- randomized assignment when ethical, feasible, adequately powered, and consistent with public obligations;
- difference-in-differences with defensible comparison and trend assumptions;
- regression discontinuity when treatment follows a suitable threshold;
- instrumental-variable designs with justified relevance and exclusion assumptions;
- matching or weighting when selection on observables is credible and overlap is adequate;
- interrupted time series with sufficient observations and modeled concurrent changes;
- synthetic controls when suitable comparison units and pre-intervention fit exist;
- theory-based contribution analysis, process tracing, realist evaluation, comparative case analysis, and mixed methods for complex pathways and contextual mechanisms.

No method is automatically valid because of its label. Design quality, assumptions, data, implementation, and the causal question determine fitness for use. Qualitative evidence should examine mechanisms and alternative explanations and may complement experimental or quasi-experimental estimates.

### Uncertainty and robustness

Public results must report effect magnitude and uncertainty in interpretable units. Where statistical intervals are appropriate, they must accompany rather than replace substantive interpretation.

The assessment must disclose:

- sampling and measurement uncertainty;
- missing data and attrition;
- model and specification dependence;
- multiple outcomes or subgroup analyses;
- sensitivity to exclusions and alternative definitions;
- unresolved conflicts or data-quality limitations;
- whether results were confirmatory or exploratory.

Null, adverse, or inconclusive results remain publishable and must not be suppressed.

### Distribution, equity, and harms

An average effect may hide unequal benefits or harms. When lawful, ethical, adequately powered, and relevant, evaluations should examine distribution across affected groups and territories.

Subgroup analysis must be planned, avoid stigmatizing inference, and protect small populations. Personal data—especially data about children—must be minimized, access-controlled, and excluded when aggregate or non-personal measures can answer the question.

Guardrails may include accessibility, safety, unequal territorial distribution, maintenance burden, resource use, displacement, or unintended environmental and social effects. Exact guardrails depend on the intervention and require source validation.

### Pilot measurement boundary

For “Respire à la récré,” the source inventory may evaluate candidate indicator families such as:

- outputs: schoolyards delivered, compatible transformed surface, planted or shaded elements;
- near-term outcomes: compatible thermal-comfort measures, permeability or water-management measures, and documented use of spaces;
- guardrails: accessibility, safety, maintenance, water use, and unequal coverage;
- contextual factors: weather, site characteristics, concurrent building work, enrollment, and other climate-adaptation actions.

These are candidate families, not accepted metrics or verified available data. The pilot must select only indicators with adequate definitions, authority, feasibility, and privacy posture.

Results from three school case studies must not be generalized to all Clermont-Ferrand schools or to citywide climate resilience without a design supporting that target population and territory.

### Review and AI boundaries

AI may help discover sources, propose indicator mappings, generate code drafts, or summarize reviewed results. It must not:

- invent baselines, targets, comparison groups, measurements, or citations;
- select a favorable specification after observing results;
- assign causal status without deterministic checks and qualified review;
- turn an association or contribution claim into causal attribution;
- suppress null, adverse, conflicting, or uncertain evidence.

Every public causal assessment requires methodological review separate from automated generation.

### Public explanation

Every published outcome or impact result must expose:

- the question being answered;
- indicator and target definitions;
- population, territory, period, and observation cut-off;
- baseline and comparison or counterfactual;
- observed value or effect magnitude;
- causal-claim class;
- method, assumptions, uncertainty, and robustness;
- authoritative sources, evidence, lineage, and code or formula version;
- distributional findings, harms, limitations, and counterevidence;
- reviewer and correction state.

Plain-language explanation must distinguish “changed after,” “associated with,” “contributed to,” and “caused.”

## Method quality requirements and guardrails

### Required integrity measures

- **indicator-contract coverage:** 100% of published outcome and impact measures reference a complete versioned indicator definition;
- **lineage coverage:** 100% of published estimates retain input, transformation, formula or code, and method versions;
- **causal-design coverage:** 100% of causal claims identify their estimand, counterfactual strategy, assumptions, uncertainty, and qualified review;
- **limitation disclosure:** 100% of published assessments expose known material data, design, generalization, and conflict limitations;
- **target provenance:** 100% of displayed targets identify whether they came from the campaign, administration, technical standard, benchmark, or provisional analytical choice.

These are publication requirements, not proof that an evaluation is unbiased or correct.

### Diagnostic measures

IAgora may monitor missing-baseline frequency, data-quality failures, indicator changes, review disagreement, correction rate, evaluation cost, and the share of conclusions in each causal-claim class.

These measures must not become incentives to increase positive effects, causal claims, or statistical significance, or to suppress `not verifiable` results.

### Guardrails

- Never optimize for a positive impact finding.
- Never select indicators or specifications solely because they favor a political actor.
- Never treat a target, output, spending amount, or fulfillment status as impact by itself.
- Never generalize beyond the evaluated population, territory, period, or design.
- Never use statistical significance as the sole decision rule.
- Never interpret missing or low-quality data as zero impact.
- Never expose unnecessary personal or small-cell information.

## Required invariants

1. Indicator definitions precede public interpretation and are versioned.
2. Campaign, administrative, benchmark, and analytical targets remain distinct.
3. Outcomes and causal impacts remain separate record types and claim classes.
4. Every causal claim states the counterfactual strategy and identification assumptions.
5. A simple before-and-after comparison cannot establish causal impact by itself.
6. Effect magnitude, uncertainty, and practical meaning accompany causal estimates.
7. Context, competing interventions, spillovers, and alternative explanations are examined.
8. Null, adverse, conflicting, and inconclusive results remain visible.
9. Generalization does not exceed the evidence population, territory, period, or design.
10. Fulfillment and impact conclusions remain independent unless the promise explicitly defines an outcome target.
11. Analytical code, formulas, data versions, exclusions, and transformations retain lineage.
12. AI cannot provide evidence or final causal authority.
13. Personal data is minimized and protected.
14. Positive-impact and causal-claim rates are never optimization targets.

## Scope

### Included

- Theory of change and indicator contracts.
- Metric selection, targets, baselines, and measurement plans.
- Outcome observations and causal-claim classes.
- Requirements for experimental, quasi-experimental, contribution, qualitative, and mixed-method designs.
- Uncertainty, robustness, distribution, harms, privacy, review, and public explanation.
- Pilot indicator families and generalization limits.
- Method-integrity measures and anti-gaming guardrails.

### Excluded

- Selection of final pilot indicators before source and data-quality inventory.
- A claim that the pilot programme has produced any verified impact.
- A fixed hierarchy declaring one evaluation design universally superior.
- Field-level statistical-analysis contracts or software implementation.
- Approval to collect personal or sensitive data.
- Cost-benefit or cost-effectiveness methodology.
- Citywide comparison or candidate ranking.
- Final Knowledge Passport schema.

## Consequences

### Benefits

- Citizens can distinguish delivery from observed change and causal effect.
- Descriptive evidence remains useful when causal attribution is impossible.
- Indicator and target provenance prevent later objectives from rewriting campaign promises.
- Fit-for-purpose methods support both direct interventions and complex public-policy pathways.
- Null, adverse, and uneven effects remain visible.
- Reproducible lineage allows independent analytical review.

### Drawbacks and risks

- Credible causal evaluation may require unavailable baseline or comparison data.
- Experimental and quasi-experimental designs can be costly, slow, ethically constrained, or too narrow.
- Contribution analysis can retain material judgment and may not quantify net effect.
- Detailed indicator contracts and reproducible analysis increase operating effort.
- Distributional analysis can create privacy and statistical-power risks.
- Conservative claim classes may produce many descriptive or not-verifiable results.
- Method complexity may be difficult to communicate without careful accessible design.

### Follow-up work

- Inventory pilot outcome, context, and guardrail data sources.
- Assess data quality and source authority before selecting indicators.
- Create the normative indicator and measurement-plan contracts.
- Select one to three primary pilot outcome indicators only after feasibility review.
- Define the pilot theory of change with affected stakeholders and domain experts.
- Determine whether any credible comparison or counterfactual design is feasible.
- Establish statistical, qualitative, privacy, ethics, and review roles.
- Define correction, challenge, and analytical-reproduction procedures.
- Project outcome and impact records into the Knowledge Passport specification.

## Alternatives considered

### Alternative A: Before-and-after monitoring as impact

Measure indicators before and after implementation and attribute the difference to the programme. This is operationally simple but cannot separate intervention effects from trends, weather, selection, other policies, or measurement changes.

This alternative is rejected for causal claims. Before-and-after data may remain descriptive evidence.

### Alternative B: Require randomized trials for every impact claim

Randomization can provide strong causal identification when well designed, but it may be infeasible, unethical, underpowered, or unsuitable for already implemented and system-level interventions.

This alternative is rejected as a universal requirement.

### Alternative C: Use qualitative contribution narrative only

Theory, process, and stakeholder evidence can explain mechanisms and context, especially in complex interventions. Used alone, it may not estimate net effect or eliminate competing explanations sufficiently for every causal claim.

This alternative is retained as a valid bounded claim class but not as universal causal attribution.

### Alternative D: Fit-for-purpose measurement with explicit causal classes

Use versioned indicator contracts, descriptive outcomes, contribution evidence, and experimental or quasi-experimental designs as appropriate, while exposing assumptions and limiting causal language to what each design supports.

This is the proposed alternative.

## Migration and rollback

No production outcome or impact assessments existed when this ADR was accepted, so acceptance required no data migration.

After acceptance, merging observed outcomes with causal impacts, removing counterfactual requirements, weakening indicator lineage, or allowing unsupported generalization requires a superseding ADR. Indicator and design refinements may use versioned specifications when they preserve this decision and historical assessments retain their original versions.

## Validation

Before this decision is considered implemented:

- the pilot has a reviewed theory of change;
- candidate indicators pass source-authority, definition, data-quality, feasibility, privacy, and accessibility review;
- each selected indicator has a complete versioned contract;
- campaign and later administrative targets remain distinguishable;
- outcome observations can be published without implying causal impact;
- any causal claim defines an estimand, counterfactual, assumptions, uncertainty, robustness, and generalization boundary;
- before-and-after evidence is prevented from producing causal status without an adequate design;
- output, outcome, contribution, and causal-effect records remain distinct;
- null, adverse, and inconclusive results pass the same publication process as positive results;
- analytical lineage reproduces representative estimates from versioned inputs;
- three-school evidence cannot produce a citywide claim without supporting population design;
- privacy review prevents unnecessary child-level or small-cell publication;
- non-specialist users can distinguish observation, association, contribution, and causation in plain-language testing.

## Governance and evidence impact

- Indicator definitions, measurement plans, and evaluation designs become versioned governance artifacts.
- Outcome observations are evidence-backed assertions; impact conclusions are derived assessments.
- Source authority applies to measurements and records, not automatically to causal interpretation.
- Methodological reviewers require competence appropriate to the design and domain.
- Deviations, specification changes, null results, and corrections remain inspectable.
- Knowledge Passports must expose causal-claim class, design, assumptions, uncertainty, limits, and lineage.
- AI assistance remains subordinate to deterministic checks and qualified review.

## Related records

- Vision and pilot boundary: [`ADR-0001`](ADR-0001-project-vision-and-pilot-boundary.md)
- Canonical assertion and evidence model: [`ADR-0002`](ADR-0002-canonical-assertion-and-evidence-model.md)
- Fact-specific Source of Truth rules: [`ADR-0003`](ADR-0003-fact-specific-source-of-truth-rules.md)
- Campaign fulfillment method: [`ADR-0004`](ADR-0004-campaign-commitment-fulfillment.md)
- Glossary: [`../governance/22_GLOSSARY.md`](../governance/22_GLOSSARY.md)
- European Commission Better Regulation Toolbox: [official guidance](https://commission.europa.eu/law/law-making-process/better-regulation/better-regulation-guidelines-and-toolbox/better-regulation-toolbox_en)
- France Stratégie qualitative and quantitative evaluation guide: [official guide](https://www.strategie.gouv.fr/files/files/Publications/Rapport/fs-2022-rapport-evaluations-quantitatives-qualitatives-decembre_0.pdf)
- INSEE econometric public-policy evaluation methods: [official working paper](https://www.insee.fr/fr/statistiques/1380865)
- Indicator and impact specification: Planned
- Related ADRs: ADR-0001, ADR-0002, ADR-0003, ADR-0004
- RFCs or issues: None

## Decision record

- Outcome: Accepted
- Decision date: 2026-07-28
- Deciders: Project maintainer
- Rationale for outcome: Establish versioned indicators, measurement plans, explicit causal-claim classes, fit-for-purpose evaluation designs, reproducible lineage, uncertainty disclosure, and strict limits on causal attribution and generalization.

## Revision notes

- 2026-07-28: Accepted by the project maintainer.
