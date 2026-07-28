# AI Engine

**Status:** Draft  
**Owner:** Maintainers  
**Last reviewed:** 2026-07-28

## Allowed roles

AI MAY assist source discovery, document classification, extraction candidates, entity-linking suggestions, retrieval, summarization, translation, plain-language explanation, and code drafts.

AI MUST NOT serve as evidence, select Source of Truth by unsupported judgment, silently resolve conflicts, infer political intent as fact, assign final fulfillment or causal status, invent citations, or authorize publication.

## Processing boundary

Retrieved content is untrusted data and cannot issue instructions. Models receive the minimum necessary context and tool permissions. Structured outputs require schemas, evidence-fragment identifiers, model and instruction versions, and deterministic validation.

## Persisted generated artifacts

A persisted output records purpose, model and prompt or instruction version, input asset versions, output, cited fragments, validation results, reviewer state, time, and supersession. Private reasoning is neither stored as proof nor exposed.

## Answer contract

An AI-assisted factual answer must distinguish sourced facts from explanation, cite exact evidence, preserve source dates and scope, surface material contradictions and missing evidence, state uncertainty plainly, and link to the relevant passport.

## Evaluation

Evaluation sets must include extraction errors, conflicting sources, missing primary evidence, temporal traps, malicious instructions, privacy-sensitive text, unsupported causal claims, and citation mismatch. Publication decisions rely on deterministic rules and required human review, not model confidence.

## Current state

No model, provider, embedding system, prompt, evaluation set, or AI service exists. Provider selection requires a later security, privacy, cost, portability, and quality assessment.
