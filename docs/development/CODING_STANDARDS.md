# Coding Standards

**Status:** Draft  
**Owner:** Maintainers  
**Last reviewed:** 2026-07-28

## Scope

These standards apply when implementation begins. Language-specific rules must be added only after the relevant technology is selected.

## Design

- Keep modules aligned with documented responsibilities and dependency direction.
- Prefer typed interfaces, explicit schemas, small functions, and source-agnostic domain names.
- Make transformations deterministic where enforceable behavior depends on them.
- Preserve exact inputs and create versions instead of overwriting governed state.
- Make retries idempotent and side effects explicit.
- Keep persistence, search, AI, and transport behind contracts.

## Data semantics

Use canonical glossary terms. Represent units, territories, institutions, time types, lifecycle states, uncertainty, and absence explicitly. Never use ambiguous fields such as generic `status`, `date`, `cost`, `source`, or `trust_score` without governed semantics.

## Errors and logging

Fail safely with stable error categories and correlation identifiers. Do not silently coerce invalid data. Logs MUST NOT contain secrets, tokens, raw sensitive content, unnecessary personal data, or hidden model reasoning.

## Security and dependencies

Treat external input as untrusted. Use least privilege, safe defaults, bounded resources, output encoding, and dependency pinning appropriate to the selected ecosystem. New dependencies require purpose, maintenance, licence, security, portability, and removal-cost review.

## Documentation

Public interfaces, contracts, non-obvious invariants, migrations, and operational procedures require concise documentation. Comments explain why a constraint exists, not restate code.

## Prototype quality commands

The current local slice uses Python 3.11 or later without third-party runtime packages. Validate contracts and run tests with:

```sh
PYTHONPATH=src python3 -m iagora validate
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

Formatting, linting, static type checking, dependency scanning, and continuous integration remain to be selected before the prototype becomes a distributed service. The current Python choice is a reversible prototype implementation, not an accepted platform-language decision.
