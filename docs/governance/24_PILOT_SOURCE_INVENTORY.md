# “Respire à la récré” Pilot Source Inventory

**Status:** Active inventory
**Owner:** Maintainers
**Last verified:** 2026-07-30
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
| `src-city-procurement-open-data` | [City public-procurement dataset from 2020 onward](https://opendata.clermont-ferrand.fr/explore/dataset/marches-publics-a-partir-de-2020-vcf/) and [API](https://opendata.clermont-ferrand.fr/api/explore/v2.1/catalog/datasets/marches-publics-a-partir-de-2020-vcf/records) | Available; source metadata modified 8 July 2026; exact eight-row response for procurement identifiers `20202012301`, `25-119`, and `25-120` preserved 30 July 2026 | Authoritative with limitation for the contract metadata and excluding-tax values the City publishes; relevant records cover a 2020 study and 2025-labelled design and user-assistance services | Licence Ouverte 2.0; exact 4,253-byte response retained with acquisition event and SHA-256. Rows are at holder grain, so each contract value MUST be counted once per procurement identifier |
| `src-boamp-schoolyard-regreening-2025` | BOAMP [competition notice `25-110034`](https://www.boamp.fr/pages/avis/?q=idweb:25-110034) and [award notice `26-4348`](https://www.boamp.fr/pages/avis/?q=idweb:26-4348) | Official records linked by contract-folder identifier; competition published 5 October 2025, award decision dated 26 November 2025, award notice published 15 January 2026 | Authoritative with limitation for the reported procurement procedure, lot scopes, awardees, dates, and values | Executable metadata, notice identifiers, response size, and fingerprint admitted; raw response not retained because the official catalog states no dataset licence. Post-cut-off publication and January 2026 issue dates remain explicit; no link to the reported 2023 Pierre maternal delivery is established |
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

The executable administrative bundle is in [`../../data/pilot/administrative-evidence.json`](../../data/pilot/administrative-evidence.json). It records ten reviewed PDF versions and fifteen precise evidence fragments without committing the PDF bytes. The separate [`../../data/pilot/procurement-evidence.json`](../../data/pilot/procurement-evidence.json) bundle records admitted candidate procurement-service evidence and its quality findings; the source records do not directly name Respire.

| Stage | Present and supported | Still missing or limited |
| --- | --- | --- |
| Campaign-to-programme mapping | A versioned AI-assisted proposal preserves one essential campaign component and compares seven dimensions with the adopted “Respire à la récré” policy using three precise evidence references | Independent methodological and authority reviewers have not accepted direct continuity or the proposed relationship; the proposal cannot establish fulfillment |
| Adopted policy | Final council adoption and attached policy definition | Adoption does not prove implementation or campaign fulfillment |
| Programme authorization | €4.07 million programme authorization; €810,000 of 2023 payment credits; a €350,000 rephasing | No school-level allocation follows from these programme figures |
| Executed expenditure | Approved account reports €1.09 million for 2022; the 2023 budget annex reports €1,939,810.63 in cumulative prior mandates | The two figures have different periods and precision; neither is a transaction or school ledger |
| Procurement | Candidate evidence records a €45,750 excluding-tax study notified in 2020 and a two-lot 2025 design and user-assistance procedure awarded for €81,500 and €76,800 excluding tax. The City and BOAMP records cross-check the later contract references and values | The records do not directly name Respire and concern services, not works. No works contract has been mapped to the reported Nestor-Perret or Pierre maternal delivery; the multi-school values cannot be allocated to one school, and the post-cut-off publication remains explicit |
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

## Acquisition priority queue

| Priority | Evidence target | Verified lead | Remaining action and guardrail |
| --- | --- | --- | --- |
| P0 | Works procurement and competent acceptance for the three pilot cases | No competent acceptance record or clearly attributable schoolyard works contract was located in the bounded searches | Search contract documents, mayoral-decision schedules, final account records, and competent acceptance artifacts by school unit, date, and project object. Unrelated building, boiler, refectory, lift, painting, and energy-renovation contracts MUST remain excluded |
| P0 | School-level accounting | Programme authorizations, cumulative mandates, one reported Pierre maternal cost, and procurement values exist at different scopes | Seek commitments, invoices, payment mandates, final accounts, or equivalent records that identify the school unit and contract. Programme totals and multi-school lot values MUST NOT be allocated to one school without a competent source |
| P1 | Qualified BOAMP rights review | The notice metadata and response fingerprint are admitted, but the official dataset catalog states neither licence nor licence URL | Establish the lawful reuse basis before retaining or redistributing BOAMP response bytes; until then, keep the source link-only and metadata-only |
| P1 | Before/after outcome indicators | The school dataset supplies output measures such as planted trees and de-impermeabilized surface, but no baseline/outcome comparison was located | Seek site-level temperature, permeability, biodiversity, use, comfort, inclusion, or maintenance measurements with dates, definitions, and baselines. City-wide heat-island studies are methodological context, not school outcome evidence |
| P2 | Policy and programme lineage | The authenticated 2019 campaign wording, a 2020 study contract, the 2021 launch, and the 2023 adopted policy are dated anchors | Search pre-2020 schoolyard policy, budget, and works records before classifying the programme as new, continued, or expanded; chronological proximity alone does not establish continuity |

## Acquisition and quality update — 30 July 2026

The following candidate findings are now represented in the executable procurement bundle. They refine the evidence chain without asserting a direct Respire relationship, changing the historical observation cut-off, or changing the `not_verifiable` conclusion:

- The City procurement dataset reports contract `20202012301`, notified on 27 November 2020, for a study on schoolyard regreening and urban cool islands, with a published value of €45,750. This is relevant procurement evidence for a study service, not a works contract, payment, delivery record, outcome, or causal impact.
- BOAMP competition notice `25-110034` covers design and user-assistance services for two lots: Edgard-Quinet with Paul-Bert, and Pierre-et-Marie-Curie with Alphonse-Daudet. Award notice `26-4348` reports awards dated 26 November 2025, contract references `25-119` and `25-120`, and published values of €81,500 and €76,800. The City dataset cross-checks those references and labels its amount field as excluding tax. The contracts were issued and the award notice was published in January 2026, after the observation cut-off.
- The City response contains eight holder-grain rows for three procurement identifiers. Summing rows would produce €602,150, while counting each procurement value once produces €204,050 including the 2020 study. This €398,100 overstatement risk is now an executable test invariant.
- The City fields `marche_nature` and `marche_type` exchange semantic positions between the selected 2020 and 2025-labelled records. Normalization must therefore use controlled values record by record and corroborate the later procedure with BOAMP.
- The 2025 Pierre-et-Marie-Curie lot cannot be attached to the maternal courtyard reported as completed in 2023 without a scope-bearing record. It may concern later work, including the elementary unit that the current school dataset marks as forthcoming.
- Searches for competent acceptance, invoices, payments, and school-unit accounts did not locate a qualifying artifact. Several records mentioning the same schools concern refectories, boilers, lifts, painting, or energy renovation and were excluded because their object does not establish a Respire schoolyard relationship. The absence of a located artifact is not evidence that the action or record does not exist.
- No programme-specific before/after outcome evaluation was located. The available school dataset contains reported outputs, not measured changes in comfort, temperature, use, biodiversity, inclusion, or other outcomes.
- The mutable City progress page reports 511 m² of “surface revégétalisée” and 37 planted trees at Nestor-Perret, while the acquired open-data record reports 1,367 m² of net de-impermeabilized surface and 34 planted trees. The surface fields have different labels and MUST NOT be treated as the same measure. The tree-count difference remains a visible version, date, or scope question pending reconciliation.

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

1. A structured candidate mapping now connects the authenticated, unquantified campaign subject to the adopted municipal programme without adding a target or deadline. It remains an AI-assisted proposal: independent methodological and authority review has not accepted the relationship.
2. Adopted policy, programme authorization, programme expenditure, and limited site evidence are mapped. Candidate procurement records cover study and design services without directly naming Respire. Attributable works procurement, transaction-level or school-level accounting, and competent completion records remain missing.
3. No reviewed baseline, outcome indicator, comparison design, or causal evaluation is available.
4. Page-level rights, retention classes, and privacy assessments remain incomplete for link-only sources; the campaign page and BOAMP raw response remain metadata-only pending qualified rights review.
5. Current web pages may incorporate information published after the observation cut-off; a later acquisition must not be represented as contemporaneous 2025 evidence.

These gaps block a public fulfillment or impact conclusion. They do not block a local contract-and-lineage prototype that visibly returns `not verifiable`.

## Maintenance rules

- Every source-profile change MUST retain its prior version or a review history.
- Every acquisition MUST record acquisition time, resolved URL, media type, fingerprint, rights state, retention class, and security result.
- A source moving or disappearing MUST NOT erase its inventory record.
- New sources do not silently change the 31 December 2025 analytical snapshot.
- This inventory MUST be reverified before production acquisition or public release.
