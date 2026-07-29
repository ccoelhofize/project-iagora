# Frontend

**Status:** Draft  
**Owner:** Maintainers  
**Last reviewed:** 2026-07-29

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

The multidimensional semantics and policy-lineage method are governed by accepted [ADR-0010](../adr/ADR-0010-multidimensional-accountability-and-policy-lineage.md). This frontend specification remains a draft, and its components, routes, KPI selections, and interaction design are not implemented or accepted by the ADR alone.

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

The vertical slice generates one static French HTML review page with semantic headings, explicit text status, table captions, keyboard-scrollable tables, visible focus, and a machine-readable passport peer. It represents the programme or commitment-detail level only. No territory home, thematic dashboard, macro visualization, generalized indicator explorer, printable report generator, account system, public frontend, or SaaS deployment exists. Framework, component library, visualization toolkit, localization system, analytics provider, and production interaction design remain open.

## Related records

- [Vision](../vision/00_VISION.md)
- [Product scope](../vision/02_PRODUCT_SCOPE.md)
- [Roadmap](../vision/03_ROADMAP.md)
- [ADR-0010](../adr/ADR-0010-multidimensional-accountability-and-policy-lineage.md)
- [Knowledge Passport](../governance/23_KNOWLEDGE_PASSPORT.md)
