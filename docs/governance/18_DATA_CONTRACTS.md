# Data Contracts

**Status:** Draft  
**Owner:** Maintainers  
**Last reviewed:** 2026-08-03

## Purpose

Data contracts make system boundaries explicit and testable. A contract defines structure, semantics, metadata, compatibility, validation, and failure behavior.

## Minimum contract content

Every contract MUST state:

- name, owner, status, identifier, and semantic version;
- producer and consumer boundary;
- field names, types, cardinality, controlled vocabularies, and identifiers;
- canonical definitions, units, scopes, and temporal semantics;
- required provenance, lineage, evidence, rights, access, and retention metadata;
- validation rules and cross-record invariants;
- unknown, absent, not-applicable, restricted, and conflicted behavior;
- compatibility, deprecation, migration, and rollback policy;
- rejection, quarantine, retry, and observability behavior;
- representative synthetic examples clearly labeled as such.

## Compatibility

Additive optional fields MAY be backward compatible when consumers ignore them safely. Semantic changes, renamed meanings, removed fields, stricter required fields, identifier changes, and vocabulary changes require a version assessment. Breaking public changes require a new major version.

## Validation

Deterministic schema and semantic validation runs before canonical promotion and publication. Validation MUST NOT silently coerce incompatible units, dates, territories, identifiers, or accounting stages. Failure retains diagnostics and lineage without promoting the record.

## Contract families to create

Source profile, acquisition event, artifact version, evidence fragment, assertion, authority assessment, evidence relationship, conflict, commitment mapping, financial observation, indicator, assessment, retention lifecycle, removal tombstone, review, publication gate, dataset manifest, and Knowledge Passport.

## Current state

Pre-stable executable contracts now exist for [source profiles](../../contracts/v1/source-profiles.schema.json), [archived campaign-artifact metadata](../../contracts/v1/campaign-artifact.schema.json), a bounded [canonical assertion and evidence-relationship bundle](../../contracts/v1/canonical-assertions.schema.json), [commitment mapping](../../contracts/v1/commitment-mapping.schema.json), the separate [commitment-mapping review packet](../../contracts/v1/commitment-mapping-review.schema.json), [administrative evidence](../../contracts/v1/administrative-evidence.schema.json), [bounded procurement evidence](../../contracts/v1/procurement-evidence.schema.json), [bounded historical acquisition events](../../contracts/v1/acquisition-event.schema.json), [governed acquisition plans](../../contracts/v1/acquisition-plan.schema.json), [generalized acquisition attempts](../../contracts/v1/acquisition-attempt.schema.json), [source artifact versions](../../contracts/v1/source-artifact-version.schema.json), [safe attempt receipts](../../contracts/v1/acquisition-receipt.schema.json), [human admission reviews](../../contracts/v1/admission-review.schema.json), the [bounded pilot snapshot](../../contracts/v1/pilot-snapshot.schema.json), and the [Knowledge Passport prototype](../../contracts/v1/knowledge-passport.schema.json). A deterministic standard-library validator and contract tests implement the keywords used by those schemas. The campaign contract records fingerprinted metadata, a stable fragment identifier, and a governed non-retention reason rather than copying rights-restricted HTML. The canonical assertion contract resolves the mapping target separately from its two source fragments. The mapping contract preserves a cautious candidate correspondence. Its review packet binds the exact proposal and four evidence fragments to two non-binding AI advisory roles and one interim maintainer review for local POC use, while retaining two separated independent human roles as a public-release requirement. AI preparation, AI audit outputs, and interim maintainer review cannot authorize publication. The historical acquisition-event contract remains unchanged. The five generalized acquisition contracts add policy and lifecycle vocabulary without implementing network access or pretending that missing historical custody metadata existed. The procurement contract preserves candidate rather than asserted programme relationships, service-versus-works scope, post-cut-off publication state, multi-school lots, and one-value-per-procurement-identifier aggregation.

The remaining contract families listed above are still absent or represented only by bounded profiles. The current schemas are local prototype contracts, not a stable public API, network collector, evidence store, or generalized publication-review workflow.
