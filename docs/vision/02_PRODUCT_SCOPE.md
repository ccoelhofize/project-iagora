# Product Scope

**Status:** Draft  
**Owner:** Maintainers  
**Last reviewed:** 2026-07-27

## Scope of this draft

This document proposes the smallest useful product scope for validating IAgora's evidence and traceability model by connecting a campaign commitment to later public action and observed effects. It does not authorize publication, unsupported political assessment, or collection beyond the sources described here.

## Pilot question

The proposed pilot should answer:

> As of 31 December 2025, what did the successful 2020 municipal campaign commit to regarding greener schoolyards, how was that commitment translated into public decisions, resources, and reported delivery through “Respire à la récré,” what effects were observed, and where did the evidence remain conflicting or incomplete?

The pilot is intended to support an inspectable fulfillment assessment. It should expose the underlying atomic states—such as promised, authorized, budgeted, co-funded, reported in progress, reported complete, measured, disputed, or unknown—before presenting any summary status.

A summary such as fulfilled, partially fulfilled, not fulfilled, changed, or not verifiable may be published only under a separately accepted methodology whose inputs and limitations remain visible.

Observed outcomes and attributed impacts must remain distinct. A completed schoolyard or measured temperature change is not, by itself, proof of a programme-wide causal impact on the city.

## Why this pilot is feasible

The following official sources are currently available and show that the programme can exercise several IAgora concepts:

- the City describes the programme and its initial objectives on its [programme page](https://clermont-ferrand.fr/respire-la-recre);
- the Education Department publishes a multi-year investment figure and a school target on its [presentation page](https://clermont-ferrand.fr/direction-de-leducation-de-presentation);
- another City page reports programme progress and a different target formulation on its [progress page](https://clermont-ferrand.fr/respire-la-recre-0);
- the 2025 City budget identifies funding for additional schoolyards on the [budget page](https://clermont-ferrand.fr/budget-2025);
- council records are available through the [municipal council archive](https://clermont-ferrand.fr/archives-des-conseils-municipaux);
- the official open-data portal publishes a dataset for schools affected by “Respire à la récré” or “Les Enfants d'abord” in the [dataset catalogue](https://opendata.clermont-ferrand.fr/explore/dataset/respire-a-la-recre-et-les-enfants-d-abord-vcf/).

Availability does not establish completeness, accuracy, or authority for every fact. Those properties must be assessed per assertion.

A [contemporaneous campaign interview](https://www.clermontinfos63.fr/actualite-18339-olivier-bianchi-nous-voulons-instaurer-le-droit-de-petition.html) describes schoolyard regreening as a flagship measure of the successful list. This is evidence that the measure was presented during the campaign, but it does not replace the original programme, manifesto, profession of faith, or archived campaign publication. Acquiring at least one such primary campaign artifact is a pilot validation requirement.

## Included scope

### Time

- Programme history from its reported launch in 2021.
- Observation cut-off at 31 December 2025.
- Later publications may be acquired as new evidence but must not rewrite the historical snapshot.

### Institutions

- City of Clermont-Ferrand as the principal programme owner and source producer.
- Other public bodies only when they issue a relevant decision, funding record, or authoritative dataset.
- City and metropolitan records must retain distinct institutional identities.

### Analysis levels

1. Original campaign commitment and its attributed author, list, election, scope, and wording.
2. Programme-level objectives, decisions, funding statements, reported delivery, and observed effects.
3. Three school-level case studies selected after a source inventory.

Initial candidates are Nestor-Perret, Pierre-et-Marie-Curie, and Jean-Zay. This list is provisional: a candidate may be replaced if the evidence chain is too incomplete to test the intended workflow.

### Source classes

The pilot may acquire:

- original campaign programmes, manifestos, professions of faith, and archived campaign pages;
- dated campaign statements as supporting evidence when the primary artifact is missing;
- municipal deliberations and their annexes;
- published administrative acts and funding agreements;
- budget and financial-account documents;
- official open datasets and metadata;
- official programme pages, reports, and press material as supporting evidence;
- official photographs or video metadata when legally reusable and necessary.

The authority of a source must be evaluated for the specific fact. For example, an initial budget (`budget primitif`) may be authoritative for an approved forecast but not for final expenditure.

## Excluded scope

The first pilot excludes:

- automated monitoring of every municipal commitment;
- candidate rankings, endorsements, or political recommendations;
- causal impact claims that do not meet an accepted evaluation method;
- citywide impact claims unrelated to the selected commitment;
- social-media monitoring and general media coverage beyond specifically approved contemporaneous campaign evidence;
- unpublished procurement or accounting records;
- comparison with other cities;
- personal data about children, families, or staff;
- a single composite confidence or completion score.

Absence of collected evidence must not be presented as evidence that an event did not occur.

## Minimum knowledge model to validate

Terms in this section use the definitions in the [canonical glossary](../governance/22_GLOSSARY.md).

The pilot should test these concepts without fixing their implementation technology:

- public body and territory;
- election, campaign list, campaign artifact, and commitment;
- programme and school site;
- atomic assertion and quantified objective;
- milestone and temporal validity;
- financial observation qualified by accounting stage;
- output, outcome, indicator, baseline, and impact claim;
- source, document version, and cited fragment;
- supporting, contradicting, and contextual evidence;
- acquisition and transformation record;
- methodological review;
- versioned Knowledge Passport snapshot.

## User journey

A non-specialist user should be able to:

1. read the original campaign commitment and its attribution;
2. read a plain-language fulfillment summary and inspect the method behind it;
3. compare dated objectives without conflating schools, school groups, and schoolyards;
4. follow a timeline from campaign through decision, funding, delivery, and observed effects;
5. open the exact evidence supporting each material assertion;
6. distinguish outputs, outcomes, and causally attributed impacts;
7. see relevant differences between campaign, official, and other evidence sources;
8. understand missing evidence and the limits of any conclusion;
9. inspect or export the corresponding Knowledge Passport.

## Acceptance criteria

The pilot is ready for evaluation when:

- the original campaign commitment is preserved from a primary artifact or explicitly marked as not yet verified;
- every commitment-to-action mapping is explicit, reviewable, and supported by evidence;
- any fulfillment status is reproducible from an accepted public method and its visible inputs;
- every published factual assertion cites a precise source fragment;
- acquired raw material has acquisition metadata and a content fingerprint;
- corrections and re-acquisitions create new versions rather than overwrite evidence;
- programme, school, school group, and schoolyard scopes remain distinct;
- forecast, authorization, grant, commitment, payment, and final cost are not conflated;
- outputs, outcomes, and impacts remain distinct;
- causal language is used only when the accepted evaluation design supports it;
- conflicting or differently scoped official values remain visible;
- each case study has an inspectable chronology;
- missing or changed sources do not erase previously recorded lineage;
- transformations can be reproduced from recorded inputs and versions;
- the user-facing result meets defined keyboard, screen-reader, contrast, and plain-language checks;
- no unnecessary personal data is collected or exposed.

## Decisions still required

- Accept or revise the pilot question and observation cut-off.
- Acquire and authenticate the primary 2020 campaign artifact.
- Confirm the three school-level case studies after source inventory.
- Define the campaign-commitment decomposition and fulfillment methodology.
- Define outcome indicators, baselines, and rules for impact attribution.
- Define the canonical assertion and evidence relationship.
- Define authority rules by fact type.
- Adopt retention, redaction, licence, and privacy rules before acquisition.
- Define who may approve methodological reviews and corrections.
