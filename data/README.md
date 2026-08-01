# Pilot data boundary

**Status:** Prototype data
**Owner:** Maintainers
**Last reviewed:** 2026-07-30

Files under `sources/` are IAgora governance metadata. Files under `pilot/` are
bounded prototype inputs and carry their own rights and acquisition metadata.

`pilot/open-data-subset.json` is a normalized six-record extract from the City of
Clermont-Ferrand open-data dataset “Respire à la récré et Les enfants d'abord”.
The upstream dataset is published under Licence Ouverte 2.0. Attribution:
Direction Enfance Jeunesse, Ville de Clermont-Ferrand.

The normalized file omits image metadata and coordinates that are unnecessary
for the POC. Its exact selected-field API response is preserved under
`raw/respire-a-la-recre/2026-07-29/` with an acquisition event, byte size, and
SHA-256 fingerprint. Validation deterministically proves that the six normalized
records reproduce those raw fields. This is one bounded acquisition artifact,
not a production connector or general immutable store.

No child-level personal data is included. School-level aggregate counts remain
third-party public data and retain their source licence.

`pilot/campaign-artifact.json` contains metadata, a content fingerprint, a
precise locator, and a short citation from an archived 2019 campaign page.
It does not contain the archived HTML. The archived legal notice reserves
reproduction rights, so full-page repository storage is blocked pending
qualified review. `pilot/pilot-snapshot-0.1.json` preserves the earlier missing-
source state; `pilot/pilot-snapshot.json` is the current `0.5.0` evidence state.

`pilot/commitment-mapping.json` is an AI-assisted, review-pending proposal that
preserves the primary wording as one essential, unquantified action component.
It compares territory, action, quantity, deadline, geographic extent,
institutional continuity, and chronology with “Respire à la récré.” It does not
establish direct continuity, delivery, fulfillment, outcomes, or impact.

`pilot/administrative-evidence.json` is a metadata-only bundle for ten City PDF
versions reviewed for the POC. It records exact URLs, acquisition timestamps,
byte sizes, SHA-256 fingerprints, page-level evidence, authority limits,
financial stages, school or programme scope, and non-retention decisions. The
bundle documents adopted policy, programme budget authorization, programme
expenditure, reported site delivery, and site funding forecasts. It does not
contain the PDFs, infer missing procurement, establish competent works
acceptance, or support an outcome or causal-impact conclusion.

`pilot/procurement-evidence.json` is a separate executable bundle for three
procurement records: the 2020 study service, the 2025 design competition, and
the later-published award notice for its two lots. The exact eight-row City API
response is preserved under `raw/procurement/city-contracts/2026-07-30/` under
Licence Ouverte 2.0. Values are aggregated once per procurement identifier,
never once per holder row. BOAMP response bytes are not retained because its
official dataset catalog does not state a licence; the bundle keeps only the
official notice identifiers, minimal metadata, response size, fingerprint, and
non-retention reason. These records are candidate evidence for services because
their objects concern schoolyard regreening, but they do not directly name the
Respire programme and do not establish attributable works, payment, competent
completion, outcomes, impact, or campaign fulfillment.
