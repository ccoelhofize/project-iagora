# API

**Status:** Draft  
**Owner:** Maintainers  
**Last reviewed:** 2026-07-28

## Purpose

The API will expose governed civic knowledge without hiding versions, evidence, or restrictions. Transport technology and endpoint shapes remain open.

## Contract principles

- Public resources use stable canonical identifiers and explicit versions.
- Responses distinguish asset version, contract version, observation cut-off, and retrieval time.
- Assertions link to precise evidence, authority assessments, conflicts, lineage, and their Knowledge Passport.
- Unknown, absent, restricted, conflicted, and not applicable are distinct machine-readable states.
- Pagination, filtering, sorting, localization, and error behavior are deterministic.
- Breaking changes require a new major contract version and migration guidance.
- Write operations require authenticated roles, optimistic concurrency, audit records, and idempotency keys where retries can duplicate effects.

## Initial resource families

Sources and artifacts; evidence fragments; assertions and claims; commitments and mappings; decisions, milestones, and financial observations; conflicts; indicators and observations; fulfillment and impact assessments; reviews; passports; provenance and lineage.

## Publication and security

The public API exposes only assets that passed publication gates. It MUST NOT reveal internal paths, secrets, hidden model reasoning, unnecessary personal data, quarantined content, or restricted evidence. Rate, abuse, caching, and export controls must reflect data sensitivity and operational risk.

## Error model

Errors should provide a stable code, safe explanation, correlation identifier, and contract version. Validation errors MAY identify fields but MUST NOT echo sensitive source content.

## Current state

No API or schema exists. OpenAPI, GraphQL, JSON:API, linked-data vocabularies, and authentication choices require later evaluation.
