# Pilot data boundary

**Status:** Prototype data
**Owner:** Maintainers
**Last reviewed:** 2026-07-29

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
precise locator, and a five-word citation from an archived 2019 campaign page.
It does not contain the archived HTML. The archived legal notice reserves
reproduction rights, so full-page repository storage is blocked pending
qualified review. `pilot/pilot-snapshot-0.1.json` preserves the earlier missing-
source state; `pilot/pilot-snapshot.json` is the current `0.2.0` evidence state.
