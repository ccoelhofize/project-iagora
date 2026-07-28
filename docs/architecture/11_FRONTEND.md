# Frontend

**Status:** Draft  
**Owner:** Maintainers  
**Last reviewed:** 2026-07-28

## Product responsibility

The public experience should help non-specialists move from a plain-language question to the evidence and method behind an answer.

## Initial information architecture

- programme and commitment overview;
- original campaign wording and decomposition;
- timeline of decisions, resources, delivery, and observations;
- component-level fulfillment states;
- separate outcomes and causal-impact section;
- source, evidence, conflict, and uncertainty panels;
- Knowledge Passport and machine-readable export;
- correction and challenge route.

## Presentation rules

Observed fact, official claim, calculation, inference, editorial explanation, and generated content MUST be visually and semantically distinguishable. A summary label MUST link to atomic states. Missing and conflicting information cannot be hidden by chart defaults or progressive disclosure.

## Accessibility

The interface MUST use semantic structure, keyboard operation, visible focus, sufficient contrast, scalable text, descriptive labels, non-color status cues, table and chart alternatives, understandable language, and predictable navigation. Accessibility acceptance criteria and assistive-technology testing belong in the test plan.

## Safety and privacy

Rendered source content is sanitized. External links identify destination and source. The interface must not expose restricted fragments, small-cell personal data, internal review notes, or private identifiers.

## Current state

The vertical slice generates a static French HTML review page with semantic headings, explicit text status, table captions, keyboard-scrollable tables, visible focus, and a machine-readable passport peer. It is a local prototype, not an approved public frontend or design system. Framework, component library, visualization toolkit, localization system, and analytics provider remain open.
