# Pilot data boundary

**Status:** Prototype data
**Owner:** Maintainers
**Last reviewed:** 2026-07-28

Files under `sources/` are IAgora governance metadata. Files under `pilot/` are
bounded prototype inputs and carry their own rights and acquisition metadata.

`pilot/open-data-subset.json` is a normalized six-record extract from the City of
Clermont-Ferrand open-data dataset “Respire à la récré et Les enfants d'abord”.
The upstream dataset is published under Licence Ouverte 2.0. Attribution:
Direction Enfance Jeunesse, Ville de Clermont-Ferrand.

The file is not represented as immutable raw HTTP evidence: the prototype
normalizes JSON and omits image metadata and coordinates that are unnecessary
for the POC. Its manifest therefore records `raw_bytes_preserved: false`, and
the publication gate remains closed. Production acquisition must preserve the
exact response bytes or a governed reason why they cannot be retained.

No child-level personal data is included. School-level aggregate counts remain
third-party public data and retain their source licence.
