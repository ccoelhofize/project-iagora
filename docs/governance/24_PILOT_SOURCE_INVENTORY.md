# “Respire à la récré” Pilot Source Inventory

**Status:** Active inventory
**Owner:** Maintainers
**Last verified:** 2026-07-28
**Observation cut-off:** 2025-12-31

## Purpose

This inventory records which sources were actually located for the accepted proof of concept, what each source may establish, and what remains missing. Availability is not authority, and authority is assessed per fact type under [ADR-0003](../adr/ADR-0003-fact-specific-source-of-truth-rules.md).

The machine-readable source profiles are in [`../../data/sources/source-profiles.json`](../../data/sources/source-profiles.json). The list below is a review surface, not a substitute for those profiles or for acquired artifact versions.

## Inventory

| ID | Source | Verified state | Candidate authority | Rights and acquisition decision |
| --- | --- | --- | --- | --- |
| `src-campaign-2020-primary` | Original “Naturellement Clermont” 2020 programme, manifesto, profession of faith, or authenticated campaign archive | **Missing** after targeted web search | Original wording, scope, conditions, and target of the campaign commitment | No acquisition authorized until located and rights-reviewed |
| `src-campaign-2020-interview` | [Info Clermont Métropole interview, 2 March 2020](https://www.clermontinfos63.fr/actualite-18339-olivier-bianchi-nous-voulons-instaurer-le-droit-de-petition.html) | Available, contemporaneous secondary evidence | Supporting evidence that schoolyard regreening was presented as a campaign measure; not a replacement for the primary artifact | Link and short lawful citation only; redistribution rights unresolved |
| `src-election-2020-results` | [Ministry of the Interior municipal-election archive](https://www.archives-resultats-elections.interieur.gouv.fr/resultats/municipales-2020/063/C2063113.php) | Available | List name, lead candidate, election context and result records within the competent archive scope | Site states Licence Ouverte 2.0 unless otherwise noted; profile remains limited to election facts |
| `src-city-2021-launch` | [City programme launch page](https://clermont-ferrand.fr/respire-la-recre) | Available | Authoritative only for what the City reported about programme launch, intended methods, and first schools | Link-only until page-level reuse and retention review is complete |
| `src-city-progress` | [City progress and transformed-school page](https://clermont-ferrand.fr/respire-la-recre-0) | Available and mutable | Authoritative with limitation for dated City-reported progress; not sufficient for executed expenditure, outcome, or causal impact | Link-only; each later acquisition must create a version because the page changes over time |
| `src-city-education-overview` | [City Education Department overview](https://clermont-ferrand.fr/direction-de-leducation-de-presentation) | Available but automated retrieval was unstable during verification | Supporting evidence for programme targets and investment claims; underlying adopted records remain preferable | Link-only; authority and rights review incomplete |
| `src-city-open-data-schools` | [Official open-data dataset](https://opendata.clermont-ferrand.fr/explore/dataset/respire-a-la-recre-et-les-enfants-d-abord-vcf/) and [API](https://opendata.clermont-ferrand.fr/api/explore/v2.1/catalog/datasets/respire-a-la-recre-et-les-enfants-d-abord-vcf/records) | Available; 62 records; source metadata modified 26 June 2026; stated temporal coverage ends 31 December 2025 | Authoritative with limitation for the values and school-unit states the City dataset reports; not a completion certificate or impact evaluation | Licence Ouverte 2.0; approved for the bounded local prototype subset; acquisition after the observation cut-off is explicit |
| `src-city-budget-2025-summary` | [City 2025 budget presentation](https://clermont-ferrand.fr/budget-2025) | Available | Authoritative only for the City’s published summary that €1.5 million was presented for ten additional courtyards; not executed expenditure | Link-only; adopted budget and accounting records still required for stronger financial authority |
| `src-city-council-archive` | [Municipal council archive](https://clermont-ferrand.fr/archives-des-conseils-municipaux) | Available, individual records require selection | Discovery point for adopted deliberations and annexes; the archive page itself is not the adopted act | Metadata discovery approved; each document needs its own source profile or artifact review |
| `src-city-transition-report-2022` | [2021 transition progress report presented in 2022](https://clermont-ferrand.fr/docs/delib/CM18112022/CM18112022_003_A1.pdf) | Available | City-reported programme progress and context for the period covered by the report | Link-only pending document-level rights and retention review |
| `src-city-education-project-2023` | [Adopted municipal education project annex](https://clermont-ferrand.fr/docs/delib/CM05052023/CM05052023_004_annexe_0.pdf) | Available | Competent adopted policy context when linked to the final deliberation and scope | Link-only pending final-act verification and rights review |

## Confirmed case studies

The official dataset contains distinct school-unit records that make all three cases useful:

| Case | Evidence available in the official dataset | POC purpose |
| --- | --- | --- |
| Nestor-Perret | Maternelle and élémentaire records report 2022 vegetation work as complete; the élémentaire row carries the shared-cour values | Completed-output path, shared-cour semantics, precise row citations |
| Pierre-et-Marie-Curie | Maternelle reports 2023 completion while élémentaire reports work still to come | Scope-difference path; proves that a school group cannot receive one silently aggregated state |
| Jean-Zay | Maternelle and élémentaire records report 2025 work as in progress | Cut-off path; prevents an unfinished item from being reported as delivered |

These are source claims in a dataset acquired after the historical cut-off. They are not independently verified completion facts and do not establish outcomes or causal impact.

## Blocking gaps

1. The authenticated primary 2020 campaign artifact remains missing.
2. Adopted budget documents, executed expenditure, procurement, and competent completion records have not yet been mapped to the three cases.
3. No reviewed baseline, outcome indicator, comparison design, or causal evaluation is available.
4. Page-level rights, retention classes, and privacy assessments remain incomplete for link-only sources.
5. Current web pages may incorporate information published after the observation cut-off; a later acquisition must not be represented as contemporaneous 2025 evidence.

These gaps block a public fulfillment or impact conclusion. They do not block a local contract-and-lineage prototype that visibly returns `not verifiable`.

## Maintenance rules

- Every source-profile change MUST retain its prior version or a review history.
- Every acquisition MUST record acquisition time, resolved URL, media type, fingerprint, rights state, retention class, and security result.
- A source moving or disappearing MUST NOT erase its inventory record.
- New sources do not silently change the 31 December 2025 analytical snapshot.
- This inventory MUST be reverified before production acquisition or public release.
