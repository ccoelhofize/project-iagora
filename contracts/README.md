# Executable contracts

**Status:** Pre-stable implementation
**Owner:** Maintainers
**Last reviewed:** 2026-07-30

The `v1` directory contains the first field-level contracts for the bounded
“Respire à la récré” proof of concept. They implement a deliberately small
subset of the accepted logical model and do not freeze a future database or API.

The campaign-artifact contract records an archived primary fragment without
redistributing restricted HTML. The commitment-mapping contract records one
essential, unquantified action component and an explicit scope comparison with
the later municipal programme. It is an AI-assisted proposal with mandatory
independent review, not an accepted mapping or fulfillment conclusion.

The pilot-snapshot contract accepts the historical `1.0.0` state and the
additive `1.1.0` through `1.4.0` evidence references; both snapshot files remain
validateable, while the current build uses `0.5.0`. The `1.2.0` Knowledge
Passport projection exposes the proposed mapping and partial candidate procurement chain without changing the
fail-closed publication state.
The acquisition-event contract covers the two bounded City API responses and
binds each request, exact bytes, fingerprint, rights, minimization, security
result, and limitations. It is not a general production acquisition contract.

The administrative-evidence contract binds ten official document versions to
precise fragments while keeping adopted policy, budget authorization, executed
expenditure, reported delivery, funding forecasts, and publication events
distinct. The procurement-evidence contract separately records candidate
evidence for a 2020 study, a 2025 competition, and two service awards without
treating them as direct Respire records, works, payments, completion, or
fulfillment. It enforces procurement-identifier amount
grain because the City response repeats values for each holder. BOAMP response
bytes remain unretained while dataset rights are unresolved. The administrative
bundle also records two bounded procurement searches as gaps that MUST NOT be
interpreted as evidence that no relevant contract exists. The PDF bytes
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
