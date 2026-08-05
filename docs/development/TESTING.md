# Testing Strategy

**Status:** Draft  
**Owner:** Maintainers  
**Last reviewed:** 2026-08-05

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

## Continuous integration

The [minimal CI workflow](../../.github/workflows/ci.yml) runs the documented validation, standard-library test, and deterministic build commands on Python 3.11 for every pull request and every push to `main`. It uses read-only repository permissions, no project secrets, and official actions pinned to exact revisions.

This workflow is a development control for the bounded prototype. A passing run does not authorize publication or prove civic facts, methodological validity, accessibility, privacy, security, or legal compliance.

## Current state

The first standard-library test suite covers contract rejection, source-snapshot integrity, commitment decomposition and mapping review gates, school-unit scope separation, precise evidence locators, deterministic replay, fail-closed publication, unsupported fulfillment and causal conclusions, separated financial stages, bounded dashboard metrics, route generation, and basic semantic HTML and chart-equivalent content. It also validates the six-school acquisition plan against its exact source profile, rejects an unregistered host, binds all three historical compatibility projections to exact bytes, and keeps the synthetic admission example pending and fail-closed. Twelve local acquisition tests cover deterministic request construction, unregistered plans, loopback and mixed DNS answers, redirect revalidation, media/compression/size bounds, exact unchanged replay, changed-response quarantine and field reports, content-addressed deduplication, malformed scope, safe failures, missing object bytes, CLI output, and quarantine location. Remote-adapter tests cover local-versus-runner equivalence, temporary-package manifests, component fingerprints, valid-candidate-only raw export, metadata-only invalid results, receipt payload safety, one-time day-10 reminders, fail-closed expiry, Actions-only CLI execution, the bounded GitHub issue adapter, tampered-receipt rejection, and static workflow permission and retention guardrails. All acquisition tests use retained or injected responses and contact neither the civic endpoint nor GitHub API. The minimal CI workflow executes these local controls on GitHub-hosted infrastructure. No live-network test, completed remote acquisition run, coverage baseline, browser or assistive-technology run, visual-regression test, full security harness, production integration test, or recovery environment exists.
