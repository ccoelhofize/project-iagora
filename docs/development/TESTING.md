# Testing Strategy

**Status:** Draft  
**Owner:** Maintainers  
**Last reviewed:** 2026-07-28

## Principle

Tests provide evidence about implemented behavior. They do not prove civic facts, neutrality, legal compliance, or causal validity by themselves.

## Test layers

- **unit:** canonical rules, calculations, temporal behavior, state transitions, and deterministic validation;
- **contract:** schemas, vocabularies, compatibility, missing-state semantics, and rejection behavior;
- **integration:** acquisition, parsing, persistence, indexing, publication, and dependency boundaries;
- **lineage:** exact input and transformation coverage, replay, and downstream invalidation;
- **methodology:** commitment decomposition, fulfillment rules, indicator formulas, causal classes, uncertainty, and anti-gaming cases;
- **security:** SSRF, malicious files, archive bombs, injection, authorization, secret leakage, prompt injection, and restore behavior;
- **privacy and rights:** minimization, small cells, restricted fields, removal, attribution, and licence gates;
- **accessibility:** semantic structure, keyboard use, focus, contrast, text scaling, chart alternatives, and assistive technology;
- **migration and recovery:** forward migration, rollback, backup restoration, and non-restoration of removed content.

## Fixtures

Prefer small synthetic fixtures clearly labeled as synthetic. Real civic artifacts require documented source, rights, privacy, retention, and access review. Fixtures MUST NOT contain secrets or unnecessary personal data.

## Publication-critical coverage

Every public assertion must have precise evidence; every assessment must retain method and inputs; every passport must validate; every restriction must propagate; and every generated output must remain non-evidence. These are mandatory boundary tests.

## Reproducibility

Test commands, environments, seeds, dependencies, and expected results must be recorded. Nondeterministic tests require bounded assertions and must not mask intermittent failures.

## Current state

No implementation, test framework, CI workflow, coverage baseline, or executable contract suite exists.
