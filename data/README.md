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
source state; `pilot/pilot-snapshot.json` is the current `0.10.0` evidence state.

`pilot/commitment-mapping.json` is an AI-assisted, review-pending proposal that
preserves the primary wording as one essential, unquantified action component.
It compares territory, action, quantity, deadline, geographic extent,
institutional continuity, and chronology with “Respire à la récré.” Version
`0.3.0` records a `candidate_correspondence`, not an implementation assertion,
and makes the 2015 and 2018 education-policy predecessors explicit. It does not
establish direct continuity, novelty, delivery, fulfillment, outcomes, or impact.

`pilot/canonical-assertions.json` makes the mapping target independently
resolvable as assertion version `0.1.0`. The assertion records only that the
adopted education project defines “Respire à la récré” as a municipal
schoolyard-transformation action. Its two evidence relationships resolve to the
programme-definition and adoption fragments; they do not prove implementation
or campaign continuity.

`pilot/commitment-mapping-review.json` is the executable, fail-closed review
packet. It binds the exact mapping version and four precise evidence fragments,
configures separate methodology and evidence-authority AI advisory audits, and
requires both audits before one interim human maintainer decision for continued
local POC use. The packet preserves the two non-binding audits of superseded
mapping version `0.2.0`: the methodology audit recommended `accept`, while the
evidence-authority audit requested changes. Mapping version `0.3.0` implements
the two traceability corrections. Its current evidence-authority and final
methodology audits both recommend `accept` for continued local POC use; one
intermediate methodology run and its corrected presentation defects remain
visible in the audit history. The maintainer has not yet reviewed the corrected
version. Neither AI output nor the maintainer's
interim decision counts as independent publication review. Two distinct human
review roles remain required before public release.

`pilot/administrative-evidence.json` is a metadata-only bundle for ten City PDF
versions reviewed for the POC. It records exact URLs, acquisition timestamps,
byte sizes, SHA-256 fingerprints, page-level evidence, authority limits,
financial stages, school or programme scope, and non-retention decisions. The
bundle documents adopted policy, programme budget authorization, programme
expenditure, reported site delivery, site funding forecasts, and policy-history
context from 2015 and 2018. It does not
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
