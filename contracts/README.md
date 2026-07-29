# Executable contracts

**Status:** Pre-stable implementation
**Owner:** Maintainers
**Last reviewed:** 2026-07-29

The `v1` directory contains the first field-level contracts for the bounded
“Respire à la récré” proof of concept. They implement a deliberately small
subset of the accepted logical model and do not freeze a future database or API.

The campaign-artifact contract records an archived primary fragment without
redistributing restricted HTML. The pilot-snapshot contract accepts the
historical `1.0.0` state and the additive `1.1.0` and `1.2.0` evidence
references; both snapshot files remain validateable, while the current build
uses `0.3.0`.
The acquisition-event contract covers the single bounded official API response
and binds its request, exact bytes, fingerprint, rights, minimization, security
result, and limitations. It is not a general production acquisition contract.

The administrative-evidence contract binds ten official document versions to
precise fragments while keeping adopted policy, budget authorization, executed
expenditure, reported delivery, funding forecasts, and publication events
distinct. It also records two bounded procurement searches as gaps that MUST
NOT be interpreted as evidence that no relevant contract exists. The PDF bytes
are fingerprinted but not retained pending qualified rights and privacy review.

The contracts use JSON Schema 2020-12 vocabulary. The prototype validator
enforces the keywords used by these files with the Python standard library; a
future full JSON Schema implementation may replace it without changing the
contract semantics.

Run:

```sh
PYTHONPATH=src python3 -m iagora validate
```

Breaking changes require a new major contract directory. Additive optional
fields require explicit review because publication consumers must be able to
ignore them safely.

These contracts are present and executable. They are not yet a stable public API
and do not authorize production acquisition or publication.
