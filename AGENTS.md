# AGENTS.md

## Purpose

This file defines how Codex and other AI agents must work in the Project IAgora repository. It applies to the entire repository unless a more specific `AGENTS.md` in a subdirectory adds narrower instructions.

The repository is intended to be self-explanatory. Conversation history is useful context, but it is never the authoritative specification. Repository documents, accepted ADRs, contracts, tests, and source evidence take precedence.

## Mission

Project IAgora is an open-source civic intelligence platform that transforms fragmented public information into reliable, understandable, and verifiable knowledge.

Its mission is:

> **Transforming Data into Knowledge.**  
> **Transforming Knowledge into Empowerment.**

The initial deployment focuses on Clermont-Ferrand, France. The core platform must remain reusable across territories and public institutions.

IAgora is evidence-driven and methodologically neutral. It documents public action and supports informed interpretation; it does not campaign, recommend political choices, monitor private citizens, or present AI-generated content as fact.

## Non-negotiable principles

Agents must preserve these principles in every proposal and implementation:

1. **Evidence before conclusion.** Never invent, cherry-pick, or manufacture support for a claim.
2. **Source authority and supporting evidence are distinct.** Do not collapse Source of Truth and Source of Evidence into one concept.
3. **Raw evidence is immutable.** Corrections, annotations, and canonical interpretations are separate, versioned records.
4. **Traceability is end to end.** Public facts, transformations, analytical outputs, and AI answers must retain provenance and lineage.
5. **Conflicts remain visible.** Never silently discard a credible contradictory value or source.
6. **AI is not a source of truth.** Label generated material and cite the evidence behind factual statements.
7. **Scores must be explainable.** Confidence, quality, trust, or completion scores require documented inputs, rules, and limitations.
8. **Methodological neutrality.** Separate observed facts, official claims, calculations, inferences, and editorial explanations.
9. **Privacy and legality by design.** Use only public or otherwise lawfully accessible information; do not create private-person surveillance features.
10. **Accessibility is a requirement.** Prefer plain language, usable information architecture, semantic interfaces, and inclusive visual design.
11. **Canonical concepts stay source-agnostic.** A portal-specific field or French administrative label must not redefine a shared domain concept.
12. **Simplicity before speculative scale.** Prefer a modular monolith and explicit boundaries until measured needs justify additional infrastructure.

## Start every task with repository discovery

Before editing:

1. Read this file and the root `README.md` completely.
2. Inspect the repository tree and current Git status.
3. Look for more specific `AGENTS.md` files in the target path.
4. Read the documents, ADRs, contracts, schemas, tests, and code directly relevant to the request.
5. Identify existing user changes and preserve unrelated work.
6. Determine whether the requested artifact already exists under another name before creating a duplicate.

Do not require every task to reread the entire knowledge base. Use the README's reading paths and follow references relevant to the change.

When the repository is incomplete, distinguish clearly between:

- **present and accepted**;
- **present but draft**;
- **planned but absent**;
- **proposed by the agent**.

Never present a planned file or feature as implemented.

## Onboarding mode for a new or poorly understood repository

When asked to establish the project, consolidate its architecture, or make broad changes before sufficient context exists, do not start producing files immediately. Complete this sequence first:

### 1. Discover

- Explore the repository.
- Read the root entry points and relevant specifications.
- Build a model of the product, users, domain, architecture, and governance system.

### 2. Restate understanding

Explain in your own words:

- the problem IAgora solves;
- why it exists;
- its users and intended outcomes;
- its product boundaries;
- its key domain and governance concepts;
- decisions already accepted;
- assumptions and unresolved questions.

Do not merely reproduce document headings.

### 3. Review critically

Identify concrete strengths, inconsistencies, missing decisions, security or legal risks, documentary debt, likely technical debt, and opportunities to simplify. Challenge existing decisions when evidence supports doing so.

### 4. Recommend

For material choices, present viable alternatives with benefits, costs, risks, and migration impact. Make a clear recommendation.

### 5. Validate scope

Wait for user approval when a choice would materially change product scope, public methodology, governance, architecture, legal posture, cost, or external state.

### 6. Produce

After direction is clear, create the smallest coherent change, validate it, and report remaining uncertainty.

This onboarding sequence is not a reason to block routine, local, well-specified work.

## Source hierarchy for decisions

Use the following precedence when instructions conflict:

1. Current user request and applicable repository instructions.
2. Accepted ADRs.
3. Accepted normative specifications and data contracts.
4. Tests, schemas, and executable validation rules.
5. Draft specifications.
6. Roadmap items and proposals.
7. Conversation history and agent inference.

If two accepted artifacts conflict, stop treating either interpretation as settled. Identify the conflict and propose a corrective ADR or documentation change.

For civic facts, follow the governance specifications rather than this documentation precedence. Source authority, evidence quality, temporal validity, and conflicts must be evaluated according to `docs/governance/`.

## Documentation rules

- Write technical and governance documentation in English unless the artifact is explicitly user-facing or a localization request says otherwise.
- Use concise, direct language. Define specialized terms in the glossary.
- Include a document status and owner when the surrounding document family uses them.
- Use stable relative links; update inbound links when moving or renaming a document.
- Keep examples clearly labeled as real, illustrative, synthetic, or provisional.
- Never use invented civic values in a way that could be mistaken for real data.
- Avoid decorative duplication across documents. Keep one normative definition and link to it elsewhere.
- Use normative words deliberately: **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY**.
- A document marked `Draft` is not an accepted decision unless an accepted ADR explicitly says otherwise.
- Update `docs/99_ARCHITECTURE_INDEX.md` and relevant indexes when adding, moving, renaming, accepting, deprecating, or superseding documents.

## ADR and RFC policy

Create or propose an ADR when a decision:

- changes a system boundary, canonical entity, governance rule, public contract, security model, or major dependency;
- has long-lived consequences or meaningful migration cost;
- resolves a disputed architectural choice;
- supersedes an earlier accepted decision.

Do not rewrite accepted ADR history to make a new decision appear original. Create a superseding ADR and link both records.

Use an RFC before implementation when a proposal is broad, cross-cutting, still open to alternatives, or needs community discussion. Small, reversible implementation details do not require an ADR or RFC.

Every ADR should contain at least:

- title and identifier;
- status;
- context;
- decision;
- consequences, including drawbacks;
- alternatives considered;
- related specifications and supersession links where applicable.

Update `docs/adr/ADR-INDEX.md` with every ADR lifecycle change.

## Data and knowledge governance

When adding or changing a data flow, entity, indicator, claim, or AI answer, assess all applicable concerns:

- canonical definition and identifiers;
- source authority;
- supporting and contradictory evidence;
- provenance and acquisition metadata;
- lineage and transformation version;
- contract and schema validation;
- temporal validity and supersession;
- data quality and fitness for use;
- confidence and uncertainty;
- access, privacy, license, and retention;
- Knowledge Passport exposure;
- citation precision.

Do not use a single opaque `trust_score` to replace these dimensions. A composite score may summarize them only when users can inspect its components and method.

For derived metrics, preserve the formula, inputs, units, territorial scope, time period, software or rule version, and rounding behavior. For manual review, record the reviewer role, decision, timestamp, and rationale without exposing unnecessary personal information.

## AI behavior and generated content

AI features must be designed around evidence retrieval and constrained generation.

Agents MUST:

- distinguish extraction from interpretation;
- cite the source fragments used for factual output;
- preserve source dates, validity periods, and territorial scope;
- surface relevant contradictions and missing evidence;
- express uncertainty in plain language;
- make deterministic validation responsible for enforceable rules;
- store model and prompt versions when generated artifacts are persisted.

Agents MUST NOT:

- treat model output as evidence;
- fabricate citations, document identifiers, quotations, values, or legal conclusions;
- expose hidden chain-of-thought or claim that such text proves correctness;
- infer political intent as fact;
- assign a promise status solely from a model's unsupported judgment;
- publish sensitive personal data merely because it appears in a public source.

Explainability should expose evidence selection, rules applied, conflicts, calculations, and material assumptions—not private model reasoning.

## Engineering expectations

When implementation begins:

- Respect existing component boundaries and public contracts.
- Prefer typed interfaces, explicit schemas, deterministic transformations, and idempotent ingestion.
- Preserve raw inputs and make derived outputs reproducible.
- Design collectors so a source-specific change does not alter canonical domain definitions.
- Add tests in proportion to risk: unit, contract, integration, lineage, migration, accessibility, and security tests as applicable.
- Include observability for critical ingestion and publication paths.
- Keep secrets out of source, fixtures, logs, screenshots, and generated artifacts.
- Avoid new infrastructure or dependencies without a demonstrated need and documented trade-off.
- Do not perform destructive migrations without a rollback or recovery strategy and explicit approval.

## Verification checklist

Before considering a change complete, verify the applicable items:

- The requested outcome is implemented, not only described.
- Links, indexes, and status fields are consistent.
- Terminology matches the canonical dictionary and glossary.
- New data boundaries have contracts and validation.
- Provenance, lineage, evidence, and temporal behavior remain intact.
- Relevant tests or document checks pass.
- No secrets, personal paths, or accidental metadata were introduced.
- Examples cannot be confused with verified civic facts.
- User-facing content is understandable and accessible.
- Significant decisions are captured in an ADR or explicitly listed as open.
- `git diff` contains no unrelated or accidental changes.

If a verification step cannot be run, state that clearly in the handoff.

## Git and external actions

- Preserve existing user work and avoid unrelated edits.
- Do not commit, push, create branches, open pull requests, publish, deploy, or modify external services unless the user explicitly requests that action.
- When authorized to commit, use focused commits that tell the architectural story of the change.
- Never rewrite shared history or use destructive Git operations without explicit approval.
- Treat repository visibility as unrelated to licensing, production readiness, or permission to publish derived data.

## Communication and handoff

Lead with the outcome. Keep progress updates concise and make assumptions visible.

At completion, report:

- what changed;
- why it changed;
- what was validated;
- affected specifications, ADRs, contracts, or tests;
- unresolved questions, risks, and suggested next step.

Do not claim maturity, compliance, neutrality, accuracy, or production readiness without evidence.

## Final working principle

Do not ask users to trust IAgora—or the agent—blindly.

Build every important result so that a contributor or citizen can inspect its definition, source, evidence, transformations, uncertainty, and governing decision.
