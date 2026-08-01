# Knowledge Passport

**Status:** Draft  
**Owner:** Maintainers  
**Last reviewed:** 2026-07-30

## Purpose

This specification operationalizes [ADR-0006](../adr/ADR-0006-minimum-knowledge-passport-contract.md). A passport is a versioned projection of canonical governance records, not an independent truth store.

## Core profile

Every public passport MUST expose:

- stable passport, asset, asset-version, and contract identifiers;
- asset type, canonical definition, plain-language description, and lifecycle state;
- subject, territory, institution, population, unit, period, temporal validity, and observation cut-off where applicable;
- assertion content and epistemic kind;
- fact-specific authority rule and assessment;
- supporting, contradictory, and contextual evidence;
- publisher, source, acquisition, rights, access, and retention provenance;
- input, transformation, validation, and review lineage;
- quality, fitness, conflicts, uncertainty, and limitations;
- review, correction, challenge, and supersession state;
- accessible explanation and non-visual equivalents.

Unknown, absent, restricted, and not applicable are distinct contract states.

## Assessment extension

Fulfillment, outcome, and impact passports additionally expose original commitment and decomposition, implementation states, method version, indicators, baseline and target provenance, formula and units, result and uncertainty, causal class and design, assumptions, robustness, generalization limits, and adverse or inconclusive evidence.

## Generated-content extension

Persisted generated material identifies itself as non-evidence and records purpose, model and instruction versions, input assets, cited fragments, validations, review, limitations, and correction path.

## Presentation projections

Territory dashboards, thematic views, indicator pages, programme or commitment detail, and printable reports MUST reference the same governed asset and method versions as their Knowledge Passport. Progressive disclosure may reduce visible detail, but it MUST NOT change the represented conclusion, cut-off, scope, evidence state, conflicts, uncertainty, or limitations.

A printable report records its generation time, territory, period, filters, source and method versions, and correction state. It is a publication projection, not an independent truth store. The extended dashboard and policy-lineage rules are governed by accepted [ADR-0010](../adr/ADR-0010-multidimensional-accountability-and-policy-lineage.md). A bounded field-level contract and local product projection exist for the pilot; generalized contracts and production components remain unimplemented.

## Disclosure profiles

Internal and public profiles MAY differ for a documented legal, privacy, safety, security, or contractual reason. Public views disclose a lawful non-sensitive reason code for restricted fields. If redaction would make the asset materially misleading, publication is blocked.

## Initial transport

JSON is the initial prototype interchange representation and accessible HTML is its local human-readable projection. The [pre-stable field-level schema](../../contracts/v1/knowledge-passport.schema.json) covers the bounded pilot profile, including the authenticated-with-limitations campaign fragment, its attribution and retained-fragment specificity, its separate fact-specific authority, the separately resolvable [canonical programme assertion](../../data/pilot/canonical-assertions.json), the cautious AI-assisted [commitment-mapping proposal](../../data/pilot/commitment-mapping.json), its separate [review packet](../../data/pilot/commitment-mapping-review.json), and a [partial candidate procurement-service bundle](../../data/pilot/procurement-evidence.json). The passport also projects an inventoried secondary campaign interview as contextual, non-authoritative evidence. The mapping remains without a human decision: the packet preserves all historical advisory runs and identifies one current `accept` recommendation for each advisory role on corrected version `0.3.0`. A future maintainer decision cannot authorize publication or replace the two independent human reviews required before public release. The procurement sources do not directly name Respire, and study or design-service procurement cannot substitute for works, payment, competent completion, outcome, or impact evidence. None of these additions changes the `not_verifiable` fulfillment or blocked-publication state. Controlled vocabularies, general compatibility rules, restricted disclosure profiles, and public conformance examples remain incomplete. Both representations must convey equivalent material meaning.

## Validation

Publication requires schema validity, resolvable identifiers and citations, complete required governance states, accessible rendering, correction and supersession behavior, and proof that generated content cannot satisfy evidence requirements.
