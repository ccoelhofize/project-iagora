# Release Policy

**Status:** Draft  
**Owner:** Maintainers  
**Last reviewed:** 2026-07-28

## Release units

Documentation, contracts, software, methods, datasets, and public knowledge snapshots have distinct versions. A software release does not silently re-version a dataset or historical assessment.

## Versioning

Public software and contract versions should use semantic versioning where applicable. Method, schema, dataset, and passport versions must preserve their own compatibility and supersession rules. Pre-stable versions may change, but breaking changes remain explicit.

## Release gates

A release requires:

- scoped and reviewed changes with no unrelated files;
- aligned ADRs, specifications, contracts, migrations, and tests;
- passing applicable quality, security, privacy, accessibility, licence, and recovery checks;
- complete provenance, lineage, dependency, and third-party notices;
- documented rollback and known limitations;
- approval by the responsible maintainer role.

Dataset or public-knowledge publication additionally requires source rights, privacy, retention, authority, evidence, conflict, methodology, and Knowledge Passport validation.

## Artifacts

Release notes distinguish added, changed, deprecated, removed, corrected, security-relevant, and methodology-relevant behavior. Checksums or signatures should protect distributed artifacts once release tooling exists.

## Rollback and correction

Software rollback restores a compatible prior service state. Civic corrections create superseding knowledge versions rather than erasing history. Legal removal follows ADR-0007 and may make restoration impermissible.

## Current state

No release automation, version baseline, changelog, artifact registry, deployment environment, or public release exists.
