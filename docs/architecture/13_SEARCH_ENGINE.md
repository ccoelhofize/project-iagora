# Search Engine

**Status:** Draft  
**Owner:** Maintainers  
**Last reviewed:** 2026-07-28

## Purpose

Search helps users find governed knowledge and its evidence. It is a discovery projection, not a source of truth.

## Searchable units

Publishable sources, artifacts, evidence fragments, assertions, commitments, programmes, institutions, milestones, indicators, assessments, and passports may be indexed with their version, scope, dates, language, rights, and access state.

## Retrieval rules

- Results MUST respect publication and access decisions.
- Exact identifiers, titles, entities, dates, territories, and structured filters take priority where relevant.
- Lexical retrieval is the baseline; semantic retrieval is optional and must preserve cited source identifiers.
- Ranking features and versions must be documented and testable.
- Contradictory evidence and restrictive status cannot be removed merely to improve relevance.
- Snippets must retain source context and avoid exposing restricted or personal content.

## Index lifecycle

Indexes are rebuildable from canonical records. New versions, corrections, restrictions, and removals must update or invalidate search and AI-retrieval projections. Stale-index age and failed invalidations require monitoring.

## Quality evaluation

Tests should cover known-item retrieval, scope and date filters, multilingual queries, citation precision, conflict discovery, restricted-content leakage, ranking bias, and zero-result explanations.

## Current state

No search engine or vector store exists. Technology selection depends on pilot corpus size, language, latency, relevance, operability, and deletion behavior.
