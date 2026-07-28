# Data Quality

**Status:** Draft  
**Owner:** Maintainers  
**Last reviewed:** 2026-07-28

## Purpose

Data quality describes fitness for a stated use. It does not replace source authority, evidence strength, confidence, or truth.

## Initial dimensions

- **completeness:** required fields, periods, entities, and evidence are present;
- **validity:** contracts, vocabularies, types, ranges, and invariants pass;
- **accuracy:** values agree with inspectable sources within stated method limits;
- **consistency:** compatible records do not conflict without explanation;
- **uniqueness:** canonical identity and ingestion rules prevent unintended duplicates;
- **timeliness:** publication, acquisition, validity, and observation needs are met;
- **comparability:** unit, population, scope, time, and method permit the intended comparison;
- **accessibility:** users can inspect and understand the asset and its alternatives;
- **traceability:** provenance, evidence, and lineage coverage are complete.

## Assessment contract

A quality assessment MUST identify asset version, intended use, dimensions, tests, inputs, thresholds or rules, result, limitations, review state, and expiry or reassessment trigger.

## Scoring

IAgora will not use a single opaque `quality_score` or `trust_score`. A composite summary MAY be proposed only through an accepted method that exposes components, weights, sensitivity, limitations, and intended use. Failure in a critical dimension cannot be hidden by averaging.

## Publication behavior

Known material defects are disclosed. A record unfit for the requested use cannot be promoted merely because it is authoritative or complete in another sense. Missing data is not treated as zero.

## Monitoring

Monitor contract failures, unresolved duplicates, stale assets, missing evidence, correction rates, scope incompatibilities, and review disagreement as diagnostics—not targets that encourage suppressing difficult cases.
