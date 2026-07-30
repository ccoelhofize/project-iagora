# Frontend

**Status:** Draft  
**Owner:** Maintainers  
**Last reviewed:** 2026-07-30

## Product responsibility

The public experience should help non-specialists move from a territory-level overview to a plain-language answer, then to the evidence and method behind it. The intended product is an interactive civic dashboard with inspectable detail and printable reports, not a collection of reports alone.

## Target information architecture

The target public navigation has five levels:

1. **Territory home:** a macro view of the selected territory and thematic blocks.
2. **Thematic dashboard:** a focused view for a policy domain such as education, finance, culture, or public safety.
3. **Indicator detail:** definition, trend, scope, benchmark or target provenance, quality, and evidence.
4. **Programme or commitment detail:** original wording, implementation, finance, outputs, outcomes, impact, policy lineage, uncertainty, and review.
5. **Report and machine-readable export:** a reproducible projection of the selected territory, period, filters, evidence, method, and limitations.

Every summary level links downward to its governed detail. A report is an export projection of the same records, not a separate truth store.

## Territory home

The territory home SHOULD provide rapid orientation without a composite performance score. It contains:

- the selected territory, observation cut-off, freshness, and coverage state;
- one prominent macro visualization of the territory's trajectory;
- thematic blocks with one or two primary indicators each;
- visible missing-data, conflict, and review signals;
- navigation to all available themes and indicators;
- access to methodology, sources, corrections, and reporting.

The macro visualization MUST preserve the definitions and units of its series. Small multiples, selectable series, or another separable design are preferred to averaging unrelated domains into one city score. Selection of the actual Clermont-Ferrand series remains open until complete indicator definitions and source reviews exist.

## Thematic dashboards

Initial candidate themes include education, finance, culture, and public safety. They are proposed navigation categories, not completed datasets or an immutable taxonomy. Each theme requires an identified public question, competent institutions, source inventory, indicator definitions, privacy and rights review, and accountable owner before publication.

Each thematic block SHOULD show no more than one or two primary indicators on the territory home. The block title, chart, and keyboard-accessible control lead to a thematic page where users can inspect additional indicators, definitions, trends, comparisons, sources, and limitations. Material caveats MUST remain visible even when detail is progressively disclosed.

Public-safety views require heightened aggregation, small-cell protection, anti-stigmatization review, and controls against monitoring private individuals or turning reported incidents into unsupported claims about people or neighborhoods.

## First-glance commitment summary

A commitment view MUST answer the following questions before presenting dense documentation:

- what was promised, using the original wording or a faithful short quotation;
- what has been documented as completed;
- what remains in progress or planned;
- what is documented as not completed, discontinued, or outside the delivered scope;
- whether the overall commitment can be assessed with the available evidence;
- whether the implementation used a different name, territory, population, quantity, calendar, or delivery model from the campaign wording.

These answers MUST distinguish the overall commitment from the observed implementation units. A completed school, contract, or work package MUST NOT be presented as proof that a city-wide commitment was fulfilled. Conversely, an absent document MUST NOT be presented as proof that an action did not occur. A “not completed” or equivalent public label requires positive evidence or a sufficiently complete authoritative record, as defined by [ADR-0004](../adr/ADR-0004-campaign-commitment-fulfillment.md).

The first view SHOULD remain compact: plain-language labels, explicit counts or measures, the evidence cut-off, and one prominent limitation. When the evidence supports an honest comparison, it SHOULD include one small chart that answers the primary orientation question. The chart MUST retain its denominator or time range and a direct text equivalent; it MUST NOT be added merely as decoration. Detailed definitions, decompositions, sources, conflicts, calculations, and review history belong in keyboard-accessible drill-down content. Progressive disclosure MUST NOT hide a limitation that could materially change the summary's interpretation.

### Campaign evidence card

The first-glance view MUST link the retained primary campaign evidence and expose its attribution, capture or publication date, authority state, and material scope limits. If the retained primary fragment does not state a quantity, deadline, budget, funding source, deployment method, or complete territorial denominator, the interface MUST say so explicitly. This statement is limited to the retained fragment and MUST NOT be broadened into a claim that the candidate never supplied the information elsewhere.

Supporting interviews, videos, programme PDFs, and press material MAY provide context, but their source class and authority remain visible. A campaign-controlled primary artifact, secondary interview, municipal statement, adopted decision, and competent delivery record are not interchangeable.

### Progress display modes

The interface selects one of three non-interchangeable progress modes:

1. **Quantitative fulfillment:** a zero-to-100-or-more ratio MAY be shown only when the original commitment supplies a compatible target and the observed numerator has the same unit, territory, population, and period. Values MUST NOT be capped at 100 when compatible delivery exceeds the original target. Every segment links to its evidence and calculation.
2. **Unquantified commitment:** when no compatible denominator exists, the interface MUST state that a global percentage is unavailable. It SHOULD present an evidence-linked execution chain covering the original commitment, reviewed mapping, competent decisions, finance, delivery, outcomes, and impact without visually implying that equal stages represent equal completion.
3. **Observed-subset composition:** a chart MAY summarize the states of a bounded sample only when the sample size, source, cut-off, state qualifications, and non-generalization warning are visible. The chart MUST be labelled as an observed subset, never as global promise progress, and each state links to the underlying units.

### Financial accountability

Financial information MUST remain qualified by stage, period, scope, tax basis, and source. Programme authorization, annual payment credit, rephasing, mandate, executed expenditure, forecast cost, reported site cost, subsidy, contract value, invoice, and payment are distinct states. The interface MUST NOT sum or compare values that overlap or lack compatible scope and period.

“Spent to date,” “budget respected,” “savings,” “cost avoided,” and “funding source” require their own evidence. When the available records cannot establish one of these answers, the interface presents a plain-language unknown or missing state instead of deriving a verdict from partial amounts.

### Public statements and counterevidence

Campaign statements, municipal communications, deputy statements, and press archives are contextual claims unless a governance rule establishes authority for the fact at issue. They SHOULD be discoverable alongside, but visually distinct from, competent decisions, payments, delivery records, and outcome evidence.

Credible contradictory evidence, adverse decisions, abandoned components, and material implementation-scope changes MUST be as discoverable as supporting evidence. When the bounded corpus contains no qualified contradiction, the interface states that none has been identified in that corpus and that incomplete research is not evidence of absence.

## Plain civic language and cognitive accessibility

The public interface MUST be understandable without prior knowledge of politics, public administration, procurement, or municipal finance. Institutional literacy is not a prerequisite for civic access. The primary reading path therefore uses common words, short sentences, direct questions, one idea at a time, and concrete explanations of what a document or amount means.

Public content follows this order:

1. a direct answer in plain language;
2. a short explanation of what is known, unknown, or missing;
3. the official administrative term when it is needed for precision or source verification;
4. the detailed method, document, identifier, and governed data for readers who want to inspect further.

Technical vocabulary MUST NOT be the only visible label for a public fact. Terms such as programme authorization, payment credit, rephasing, mandate, procurement lot, competent completion, source authority, scope, or denominator require an immediate plain-language explanation. Acronyms are expanded or explained on first use. Exact source quotations and official document titles remain available and MUST NOT be rewritten as if the simplified explanation were the original wording.

Plain language MUST NOT erase uncertainty, legal distinctions, financial stages, disagreement, or provenance. The goal is simple and exact language, not simplistic conclusions. Unknown remains unknown; it is explained through its practical consequence, such as “we do not yet have enough evidence to answer.”

Usability acceptance SHOULD include participants who are unfamiliar with local institutions, people with limited reading confidence, and people affected by cognitive or language barriers. The pilot has received an editorial simplification pass, but representative comprehension testing has not yet occurred and remains required before public release.

## Cross-theme discovery

A single commitment or programme MAY appear under one primary theme and multiple related themes when this improves public discovery. The thematic assignment is a versioned navigation and editorial classification; it is not evidence, a performance score, or a duplicate civic record.

Every thematic route MUST reuse the same canonical commitment, programme, assessment, and evidence identifiers. A theme-specific summary MAY select relevant indicators, but MUST preserve the same material conclusion, scope, cut-off, and caveats. Initial labels such as Education, Finance, Culture, Public Safety, Urban Planning, or Ecological Transition remain proposed until the taxonomy, ownership, and publication criteria are validated.

## Indicator, programme, and commitment detail

An indicator detail page exposes its versioned definition, purpose, formula, unit, population, territory, period, baseline, target or benchmark provenance, source authority, evidence, lineage, quality, missingness, comparability, and review state.

A programme or commitment view may include:

- original campaign wording and decomposition;
- separate implementation and fulfillment states;
- stage-qualified financial observations;
- outputs, outcomes, and causal-impact classes;
- an evidence-linked policy-lineage timeline;
- source, evidence, conflict, uncertainty, and missing-information panels;
- Knowledge Passport and machine-readable export;
- correction and challenge route.

The multidimensional semantics and policy-lineage method are governed by accepted [ADR-0010](../adr/ADR-0010-multidimensional-accountability-and-policy-lineage.md), and the quantitative-fulfillment constraints by accepted [ADR-0004](../adr/ADR-0004-campaign-commitment-fulfillment.md). This frontend specification remains a draft. The current local routes and bounded KPI projection are implementation evidence, not acceptance of the complete interaction design or of future KPI selections.

## Visualizations

Charts MUST NOT convert missing values to zero, interpolate across undocumented periods, conceal incompatible scopes, or imply causal attribution through visual sequence alone. Every material mark identifies its indicator version, period, territory, and evidence path.

The preferred policy-lineage view is a timeline with separate lanes for earlier public action, campaign commitments, competent decisions and finance, implementation and outputs, and outcome or impact observations. Confirmed and proposed relationships use distinguishable non-color cues. An election boundary is context, not proof of novelty, ownership, or causation.

Every chart requires a structured table or narrative equivalent. Users MUST be able to reach details without hover, fine pointer control, color perception, or visual interpretation.

## Printable reports

Users SHOULD be able to print or export the territory overview, a thematic view, an indicator, or a programme or commitment dossier. An export records:

- generation time and observation cut-off;
- selected territory, period, theme, filters, and comparison scope;
- data, indicator, assessment, and method versions;
- sources, citations, conflicts, uncertainty, and material limitations;
- correction and supersession state;
- a stable route or identifier for the equivalent governed asset.

Print output MUST preserve reading order, headings, labels, table headers, source references, non-color meaning, and a legible fallback for interactive charts. Printing a dashboard does not authorize public release or remove evidence and rights restrictions.

## Presentation rules

Observed fact, official claim, calculation, inference, editorial explanation, and generated content MUST be visually and semantically distinguishable. A summary label MUST link to atomic states. Missing and conflicting information cannot be hidden by chart defaults or progressive disclosure. Dashboard, detail, passport, and report views MUST preserve equivalent material meaning for the same asset version and filter state.

## Accessibility

The interface MUST use semantic structure, keyboard operation, visible focus, sufficient contrast, scalable text, descriptive labels, non-color status cues, table and chart alternatives, understandable language, predictable navigation, and usable print styles. Accessibility acceptance criteria and assistive-technology testing belong in the test plan.

## Safety and privacy

Rendered source content is sanitized. External links identify destination and source. The interface must not expose restricted fragments, small-cell personal data, internal review notes, or private identifiers.

## SaaS and multi-territory boundary

The target product is a hosted software service capable of supporting multiple territories, with Clermont-Ferrand as the first deployment. This direction does not select a shared-tenancy model, account system, billing model, application framework, hosting provider, analytics provider, or deployment architecture. Public evidence views should not require authentication unless a later privacy or abuse-control decision justifies it.

## Current state

The vertical slice deterministically generates three static French HTML routes and one machine-readable passport from the same governed records:

- a Clermont-Ferrand territory home with four visible themes, an explicit coverage state, and a macro-chart placeholder that does not turn missing series into zero;
- an Education dashboard with a primary campaign-evidence card, an explicit no-percentage state, a plain-language evidence chain, clickable bounded output states, explicit name and scope differences, a stage-qualified financial table with citizen-facing explanations, contextual public statements, honest counterevidence empty states, and an evidence-qualified policy timeline;
- a detailed Respire programme dossier with the complete evidence tables, multidimensional summary, policy-lineage sequence, and print styles.

This is a local product-shaped prototype, not an authorized public frontend. Only the Education path is data-backed, Finance is limited to one programme, and Culture and Public Safety are honest empty states. No real macro city series, generalized indicator explorer, production report service, account system, application server, deployment, or SaaS capability exists. Framework, component library, visualization toolkit, localization system, analytics provider, and production interaction design remain open. Automated semantic and content guardrails exist. The current plain-language iteration received a bounded desktop visual review. Its responsive rules exist, but the revised content has not yet been rechecked at a real mobile width; representative comprehension, assistive-technology, formal contrast, broader responsive-layout, and print-output reviews remain to be performed.

## Related records

- [Vision](../vision/00_VISION.md)
- [Product scope](../vision/02_PRODUCT_SCOPE.md)
- [Roadmap](../vision/03_ROADMAP.md)
- [ADR-0010](../adr/ADR-0010-multidimensional-accountability-and-policy-lineage.md)
- [Knowledge Passport](../governance/23_KNOWLEDGE_PASSPORT.md)
