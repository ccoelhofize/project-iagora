# Data Lineage

**Status:** Draft  
**Owner:** Maintainers  
**Last reviewed:** 2026-08-01

## Purpose

Lineage records how exact input versions, transformations, validations, and reviews produced an output. It complements provenance, which records origin and custody.

## Lineage event contract

Each material processing event MUST record:

- event identifier, type, time, status, and environment;
- exact input and output identifiers and versions;
- rule, software, schema, model, prompt, or method versions as applicable;
- parameters, formula, units, rounding, exclusions, and material assumptions;
- validation outcomes and safe error codes;
- responsible deterministic process or reviewer role;
- parent event and correlation identifiers;
- access, rights, and restriction effects.

## Required coverage

Lineage applies to acquisition, parsing, extraction, normalization, entity mapping, calculation, evidence evaluation, authority assessment, conflict handling, fulfillment, outcome and impact analysis, generated explanation, redaction, publication, correction, restriction, and removal.

## Reproducibility

Given available lawful inputs and the same rule version, deterministic transformations SHOULD reproduce the same result. Nondeterministic processing MUST record enough configuration and output state for review and must not become the sole enforcement mechanism.

## Invalidation

Changed, restricted, or removed inputs trigger an impact traversal. Dependent assets are marked stale, invalid, restricted, rebuilt, or withdrawn. The reason and decision remain visible through their passport when lawful.

## Current state

The local vertical slice emits campaign-artifact authentication, three bounded City acquisitions, deterministic school-data normalization, an AI-assisted mapping proposal, administrative- and procurement-evidence reviews, passport projection, and publication-gate lineage events. Tests bind the three retained raw City fingerprints to their acquisition events, verify school raw-to-normalized equality, distinguish framework maxima from expenditure, protect procurement amounts from holder-grain duplication, and verify deterministic passport replay. The BOAMP contributions record their response fingerprints and governed non-retention decisions rather than replayable raw artifacts. No persistent lineage store, general dependency traversal, restriction propagation, or production replay mechanism exists. Physical representation remains open.
