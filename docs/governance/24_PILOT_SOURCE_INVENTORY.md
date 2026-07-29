# “Respire à la récré” Pilot Source Inventory

**Status:** Active inventory
**Owner:** Maintainers
**Last verified:** 2026-07-29
**Observation cut-off:** 2025-12-31

## Purpose

This inventory records which sources were actually located for the accepted proof of concept, what each source may establish, and what remains missing. Availability is not authority, and authority is assessed per fact type under [ADR-0003](../adr/ADR-0003-fact-specific-source-of-truth-rules.md).

The machine-readable source profiles are in [`../../data/sources/source-profiles.json`](../../data/sources/source-profiles.json). The list below is a review surface, not a substitute for those profiles or for acquired artifact versions.

## Inventory

| ID | Source | Verified state | Candidate authority | Rights and acquisition decision |
| --- | --- | --- | --- | --- |
| `src-campaign-2020-primary` | [Archived “Une ville nature” campaign page](https://web.archive.org/web/20191128144201id_/https://olivierbianchi2020.fr/une-ville-nature/) from `olivierbianchi2020.fr` | **Authenticated with limitations**; Wayback capture dated 28 November 2019 | Primary authority for the short wording “Végétalisation des cours d’école”; no authority for delivery or impact | Metadata, fingerprint, and short fragment only; archived legal notice blocks full-page redistribution without permission |
| `src-campaign-2020-interview` | [Info Clermont Métropole interview, 2 March 2020](https://www.clermontinfos63.fr/actualite-18339-olivier-bianchi-nous-voulons-instaurer-le-droit-de-petition.html) | Available, contemporaneous secondary evidence | Supporting evidence that schoolyard regreening was presented as a campaign measure; not a replacement for the primary artifact | Link and short lawful citation only; redistribution rights unresolved |
| `src-election-2020-results` | [Ministry of the Interior municipal-election archive](https://www.archives-resultats-elections.interieur.gouv.fr/resultats/municipales-2020/063/C2063113.php) | Available | List name, lead candidate, election context and result records within the competent archive scope | Site states Licence Ouverte 2.0 unless otherwise noted; profile remains limited to election facts |
| `src-city-2021-launch` | [City programme launch page](https://clermont-ferrand.fr/respire-la-recre) | Available | Authoritative only for what the City reported about programme launch, intended methods, and first schools | Link-only until page-level reuse and retention review is complete |
| `src-city-progress` | [City progress and transformed-school page](https://clermont-ferrand.fr/respire-la-recre-0) | Available and mutable | Authoritative with limitation for dated City-reported progress; not sufficient for executed expenditure, outcome, or causal impact | Link-only; each later acquisition must create a version because the page changes over time |
| `src-city-education-overview` | [City Education Department overview](https://clermont-ferrand.fr/direction-de-leducation-de-presentation) | Available but automated retrieval was unstable during verification | Supporting evidence for programme targets and investment claims; underlying adopted records remain preferable | Link-only; authority and rights review incomplete |
| `src-city-open-data-schools` | [Official open-data dataset](https://opendata.clermont-ferrand.fr/explore/dataset/respire-a-la-recre-et-les-enfants-d-abord-vcf/) and [API](https://opendata.clermont-ferrand.fr/api/explore/v2.1/catalog/datasets/respire-a-la-recre-et-les-enfants-d-abord-vcf/records) | Available; 62 records; source metadata modified 26 June 2026; stated temporal coverage ends 31 December 2025; exact six-UAI selected-field response preserved 29 July 2026 | Authoritative with limitation for the values and school-unit states the City dataset reports; not a completion certificate or impact evaluation | Licence Ouverte 2.0; exact 3,189-byte bounded response retained with acquisition event and SHA-256; acquisition after the observation cut-off is explicit |
| `src-city-budget-2025-summary` | [City 2025 budget presentation](https://clermont-ferrand.fr/budget-2025) | Available | Authoritative only for the City’s published summary that €1.5 million was presented for ten additional courtyards; not executed expenditure | Link-only; adopted budget and accounting records still required for stronger financial authority |
| `src-city-council-archive` | [Municipal council archive](https://clermont-ferrand.fr/archives-des-conseils-municipaux) | Available, individual records require selection | Discovery point for adopted deliberations and annexes; the archive page itself is not the adopted act | Metadata discovery approved; each document needs its own source profile or artifact review |
| `src-city-transition-report-2022` | [2021 transition progress report presented in 2022](https://clermont-ferrand.fr/docs/delib/CM18112022/CM18112022_003_A1.pdf) | Available | City-reported programme progress and context for the period covered by the report | Link-only pending document-level rights and retention review |
| `src-city-education-project-2023` | [Final deliberation](https://clermont-ferrand.fr/docs/delib/CM05052023/CM05052023_004.pdf) and [adopted municipal education project annex](https://clermont-ferrand.fr/docs/delib/CM05052023/CM05052023_004_annexe_0.pdf) | Final-act and annex relationship verified | Competent authority for policy adoption and definition; candidate evidence for the campaign-to-programme mapping | Metadata, fingerprints, and page-level fragments only; mapping and rights reviews remain incomplete |
| `src-city-apcp-2022` | [29 June 2022 programme-authorization update](https://clermont-ferrand.fr/docs/delib/CM29062022/CM29062022_011.pdf) | Final decision available and adopted unanimously | Respire programme authorization and payment-credit rephasing | Metadata-only; authorization is not procurement, payment, school allocation, or delivery |
| `src-city-budget-2023-adopted` | [Final 2023 budget deliberation](https://clermont-ferrand.fr/docs/delib/CM14122022/CM14122022_008.pdf) and [AP/CP annex](https://clermont-ferrand.fr/docs/delib/CM14122022/CM14122022_008_A2.pdf) | Final decision and annex available; budget adopted by majority | 2023 initial authorization, programme total, payment credits, and cumulative mandates within their respective columns | Metadata-only; programme aggregates cannot be assigned to one school |
| `src-city-account-2022` | [Approved 2022 administrative account](https://clermont-ferrand.fr/docs/delib/CM23062023/CM23062023_005.pdf) | Final decision available; account adopted by majority | Rounded annual programme expenditure reported for 2022 | Metadata-only; not a ledger, contract, invoice, or school allocation |
| `src-city-transition-report-2023` | [2022 transition progress report presented in 2023](https://clermont-ferrand.fr/docs/delib/CM23062023/CM23062023_003_A2.pdf) | Available | City-reported Nestor-Perret use and inauguration chronology | Metadata-only; not competent works acceptance or impact evidence |
| `src-city-pierre-curie-2024` | [Pierre-et-Marie-Curie schoolyard press release](https://clermont-ferrand.fr/sites/default/files/2024-02/CP_0224_respire%20%C3%A0%20la%20r%C3%A9cr%C3%A9%20cour%20pierre%20et%20marie%20curie.pdf) | Available | City-reported maternal-schoolyard work and reported site cost | Metadata-only; press-contact data is not retained; not evidence for the elementary unit, a payment, or acceptance |
| `src-city-jean-zay-funding-2025` | [Jean-Zay funding disclosure](https://clermont-ferrand.fr/attribution-de-subvention-pour-la-vegetalisation-des-cours-du-groupe-scolaire-jean-zay) | Funding plan and publication attestation available | Forecast project cost, displayed subsidy amount, and publication event | Metadata-only; no grant award, payment, procurement, expenditure, or completion is inferred |

## Administrative evidence chain

The executable metadata bundle is in [`../../data/pilot/administrative-evidence.json`](../../data/pilot/administrative-evidence.json). It records ten reviewed PDF versions and fifteen precise evidence fragments without committing the PDF bytes.

| Stage | Present and supported | Still missing or limited |
| --- | --- | --- |
| Campaign-to-programme mapping | The adopted education project explicitly identifies and defines “Respire à la récré” in a way compatible with the campaign subject | A methodological reviewer has not accepted direct continuity, scope equivalence, or component decomposition |
| Adopted policy | Final council adoption and attached policy definition | Adoption does not prove implementation or campaign fulfillment |
| Programme authorization | €4.07 million programme authorization; €810,000 of 2023 payment credits; a €350,000 rephasing | No school-level allocation follows from these programme figures |
| Executed expenditure | Approved account reports €1.09 million for 2022; the 2023 budget annex reports €1,939,810.63 in cumulative prior mandates | The two figures have different periods and precision; neither is a transaction or school ledger |
| Procurement | A bounded council-market annex review and two national essential-data dataset queries were recorded | No unambiguous Respire procurement record was located; that gap is not evidence that no contract exists |
| Site delivery and funding | Nestor-Perret official report; Pierre-et-Marie-Curie maternal communication and reported €20,000 cost; Jean-Zay €210,000 excluding-tax forecast and displayed €55,000 subsidy amount | Competent acceptance, payment, and comparable school-level accounting remain absent; Pierre elementary scope stays separate |
| Outcomes and impact | None | Baseline, observed outcome indicators, comparison design, and causal analysis remain absent |

The financial values above MUST remain attached to their stage, period, tax basis, and scope. They are not interchangeable totals.

## Confirmed case studies

The official dataset contains distinct school-unit records that make all three cases useful:

| Case | Evidence available in the official dataset | POC purpose |
| --- | --- | --- |
| Nestor-Perret | Maternelle and élémentaire records report 2022 vegetation work as complete; the élémentaire row carries the shared-cour values | Completed-output path, shared-cour semantics, precise row citations |
| Pierre-et-Marie-Curie | Maternelle reports 2023 completion while élémentaire reports work still to come | Scope-difference path; proves that a school group cannot receive one silently aggregated state |
| Jean-Zay | Maternelle and élémentaire records report 2025 work as in progress | Cut-off path; prevents an unfinished item from being reported as delivered |

These are source claims in a dataset acquired after the historical cut-off. They are not independently verified completion facts and do not establish outcomes or causal impact.

## Campaign artifact authentication

The campaign artifact metadata is stored in [`../../data/pilot/campaign-artifact.json`](../../data/pilot/campaign-artifact.json). The archived HTML is 44,008 bytes and has SHA-256 fingerprint `6d2ebfb3e06e34db61f9b2540383fe27a878d29c9f4c6482db4ddfd1995451ac` for the replay acquired on 29 July 2026.

Authentication is limited rather than absolute:

- the archived page presents the proposal under `#NaturellementClermont`;
- the archived legal notice identifies Olivier Bianchi as site owner and publication manager;
- a contemporaneous article links the same domain as the candidate campaign site;
- the Ministry election archive associates Olivier Bianchi with the Naturellement Clermont list;
- the capture is not a signed profession of faith or certified legal deposit;
- the primary fragment is unquantified and does not contain the broader “all neighbourhoods” wording found in the interview.

The raw archived HTML is intentionally not committed. The archived legal notice reserves reproduction rights, so the repository retains a fingerprint, precise locator, short citation, rights state, and governed non-retention reason.

## Blocking gaps

1. Candidate mapping evidence now connects the authenticated, unquantified campaign subject to the adopted municipal programme, but methodological review has not accepted the relationship or component decomposition.
2. Adopted policy, programme authorization, programme expenditure, and limited site evidence are mapped. Procurement, transaction-level or school-level accounting, and competent completion records remain missing.
3. No reviewed baseline, outcome indicator, comparison design, or causal evaluation is available.
4. Page-level rights, retention classes, and privacy assessments remain incomplete for link-only sources; the campaign page remains metadata-only pending qualified rights review.
5. Current web pages may incorporate information published after the observation cut-off; a later acquisition must not be represented as contemporaneous 2025 evidence.

These gaps block a public fulfillment or impact conclusion. They do not block a local contract-and-lineage prototype that visibly returns `not verifiable`.

## Maintenance rules

- Every source-profile change MUST retain its prior version or a review history.
- Every acquisition MUST record acquisition time, resolved URL, media type, fingerprint, rights state, retention class, and security result.
- A source moving or disappearing MUST NOT erase its inventory record.
- New sources do not silently change the 31 December 2025 analytical snapshot.
- This inventory MUST be reverified before production acquisition or public release.
