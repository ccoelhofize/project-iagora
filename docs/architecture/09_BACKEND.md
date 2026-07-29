# Backend

**Status:** Draft  
**Owner:** Maintainers  
**Last reviewed:** 2026-07-28

## Responsibility

The backend will implement the modular boundaries defined in the architecture, enforce contracts and policy gates, and expose governed application services. No framework or runtime is selected.

## Initial module boundaries

- source registry and acquisition control;
- evidence and document processing;
- canonical entities and assertions;
- authority, evidence, conflict, and review workflows;
- commitment, fulfillment, indicator, and impact methodology;
- provenance, lineage, quality, rights, and retention;
- Knowledge Passport projection and publication;
- search indexing and retrieval;
- identity, authorization, audit, and operations.

## Service rules

Commands MUST validate authorization, input contracts, lifecycle state, and expected version. Reads MUST respect access and disclosure profiles. Writes MUST be transactional within an aggregate boundary, idempotent where retried, and append history rather than silently overwrite governed records.

Publication services MUST fail closed when evidence, authority, lineage, review, rights, privacy, security, or passport requirements are incomplete. AI services cannot bypass application policies.

## Persistence boundary

Repositories or ports should isolate domain logic from storage. The logical graph does not require a graph database. Search indexes, caches, and vector representations are disposable projections rebuilt from canonical records.

## Current state and open choices

A dependency-free Python prototype implements contract validation and deterministic local projection only. It is not a backend-service or platform-language decision. Framework, database, migrations, job execution, authentication, network API, and deployment still require evidence from pilot contracts and operating constraints.

## Related records

- [Architecture](04_ARCHITECTURE.md)
- [API](10_API.md)
- [Data model](06_DATA_MODEL.md)
