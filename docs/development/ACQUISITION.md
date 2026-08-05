# Governed Acquisition

**Status:** Draft

**Owner:** Maintainers

**Last reviewed:** 2026-08-05

## Scope

This guide covers the local Increment 1, remote Increment 2, and protected
Increment 3 parts of
[RFC-0001](../rfc/RFC-0001-portable-governed-source-acquisition.md). The
implementation can replay a retained response or manually retrieve the one
registered six-school Opendatasoft plan. It validates the exact response shape,
compares the result with the historical baseline, and records safe metadata in
an append-only quarantine store outside the repository.

This is not a scheduled collector, general governed raw-evidence store, or
publication path. A protected admission workflow can propose one eligible
candidate in `data/raw/` through a dedicated branch and draft pull request. It
cannot write to `main`, merge, change canonical records, authorize publication,
or establish a civic conclusion.

## Safety boundary

The command accepts a registered plan identifier, never an arbitrary URL. The
current plan fixes the HTTPS host, endpoint, dataset, selected fields, school
identifiers, stable order, and query limits. The transport also enforces:

- public destination addresses only, with DNS results pinned to the TLS
  connection;
- redirect revalidation and a maximum of two redirects;
- one 20-second global deadline;
- JSON media types with no compressed response;
- a 64 KiB response limit;
- exactly the six reviewed UAI records and fourteen reviewed fields.

Failed, malformed, changed, or unexpected responses never enter the tracked
evidence tree. A structurally valid changed response is only a candidate new
version. It does not establish that its civic content is true or admissible.

## Choose a quarantine directory

Use a dedicated directory outside the repository. The engine rejects a
quarantine path inside the checkout. Absolute local paths are not written to
attempt or artifact metadata.

The examples use `/tmp/iagora-quarantine`. Operators may choose another
untracked location with suitable access controls and available space.

## Offline replay

Replay the retained historical response before considering a live request:

```sh
PYTHONPATH=src python3 -m iagora replay \
  --plan plan-city-schools-pilot-cases \
  --input data/raw/respire-a-la-recre/2026-07-29/records-selected.json \
  --quarantine-dir /tmp/iagora-quarantine
```

The expected outcome is `unchanged`. The run records a safe attempt but does
not duplicate the historical bytes in quarantine.

## Manual live acquisition

Run a live request only after confirming that the registered source, purpose,
rights, privacy class, retention rule, and scope are still appropriate:

```sh
PYTHONPATH=src python3 -m iagora acquire \
  --plan plan-city-schools-pilot-cases \
  --quarantine-dir /tmp/iagora-quarantine
```

The command prints only a safe summary. It does not print the request URL,
response body, local storage path, or secret. A live run is a deliberate
operator action; the test suite does not contact the civic endpoint.

## Outcomes

- `unchanged`: the exact response bytes match the historical baseline;
- `candidate_new_version`: the response is structurally valid but its bytes
  differ; a field-level change report is retained for human review;
- `quarantined_validation_failure`: the response violates the registered
  structure or scope and is not treated as usable evidence;
- a transport failure code: the request was blocked or failed before an
  eligible artifact could be recorded.

All outcomes keep admission and publication set to false.

## Quarantine layout

The local store is content-addressed and append-only:

```text
objects/sha256/<fingerprint>
attempts/<attempt-id>.json
artifacts/<artifact-version-id>.json
change-reports/<report-id>.json
```

Repeated candidate bytes reuse the same object. Attempt history is still
preserved. If recorded object bytes disappear, the engine fails rather than
silently recreating the prior artifact.

## Review and admission

A candidate must be reviewed against its exact plan, response fingerprint,
structural validation, change report, rights, privacy, retention, and security
metadata. Increment 3 implements that bounded remote boundary for the one
reviewed six-school plan.

The `Governed admission` workflow accepts only a receipt issue number, an
`admit` or `reject` decision, and a one-line rationale. Its first job has
read-only repository, Actions, and issue permissions. It resolves package
coordinates only from the open, non-expired `admission_pending` receipt,
downloads that exact package, revalidates every component and relationship,
revalidates the current plan and source-profile versions, reconstructs the
fixed target paths, and publishes a content-free proposal summary.

The second job uses the protected GitHub environment `governed-admission` and
cannot start before human approval. An `admit` decision may create only:

- the exact bounded JSON response under its dated raw-evidence path;
- one acquisition event and one non-interpretive source-change report;
- one admission-review record;
- one `admission/<attempt>` branch and one draft pull request;
- the final metadata-only receipt state and comment.

A `reject` decision creates no branch or evidence target. It records the
review contract in the receipt comment and closes the receipt. Neither decision
can merge, publish, canonicalize, assess a promise, or contact the civic source.
The receipt is fingerprinted before the write-capable phase; any intervening
change fails before repository writes.

The workflow is deliberately inactive until maintainers configure the external
GitHub environment with its required reviewer and set the repository Actions
variable `IAGORA_ADMISSION_ENVIRONMENT_READY` to `true`. Those controls are not
stored in Git and are not currently configured by this implementation. The
workflow MUST be dispatched from the current `main` commit; otherwise its main
commit binding fails closed.

If a provider or network failure occurs after branch or pull-request creation
but before the receipt update, inspect the named `admission/<attempt>` branch,
draft pull request, workflow log, and unchanged receipt before taking another
action. Do not blindly retry: duplicate branch protection is intentional, and
the partial state must be reconciled visibly.

## Manual GitHub Actions acquisition

The `Governed acquisition` workflow exposes one choice input containing only
`plan-city-schools-pilot-cases`. It cannot accept a URL, dataset name, query, or
shell fragment. The acquisition job has `contents: read`, checks out without
persisting credentials, validates the repository and historical fixture,
executes the same core in the `github_actions` environment, and verifies that
the checkout remains unchanged.

The resulting package is retained for 14 days. It contains a validated manifest,
safe summary, exact attempt metadata, receipt, and eligible comparison or
candidate material. A structurally invalid response exports metadata only; its
untrusted raw bytes are not uploaded. The workflow has been implemented, tested
with controlled inputs, and exercised once against the registered public source.

The separate receipt job has `issues: write`, read-only access to the checked-out
adapter code, and no package access. It receives only a validated base64-encoded
issue payload and creates a durable metadata-only issue. Receipts for unchanged
or non-reviewable attempts are closed immediately; a candidate issue remains
open for human review.

The `Acquisition receipt monitor` runs daily and may also be triggered manually.
It reads receipt issues only. It never executes the acquisition command or
contacts a civic source. At day 10 it records one reminder. At or after day 14,
an undecided receipt becomes `expired_without_admission`, records that the
temporary bytes are unavailable, and closes the issue.

## First controlled remote exercise

On 5 August 2026, maintainers manually triggered [workflow run
`31009987688`](https://github.com/ccoelhofize/project-iagora/actions/runs/31009987688)
from merged `main` commit `0bab75e`. Both the read-only acquisition job and the
separately privileged receipt job completed successfully.

The registered City response contained 3,189 bytes and six records. Its
SHA-256 fingerprint,
`62f26237a39465942e18749aa1ba4957885fe7ca1d6979b0620067c99a2517ae`,
exactly matched the governed 29 July 2026 artifact. The deterministic comparison
reported six unchanged records and no added, removed, changed, or field-level
differences. The package therefore contained metadata and comparison material
but no duplicated raw bytes.

GitHub retained package `package-888789dab3e043ceb871a281ef6954cb` for 14 days,
until 19 August 2026. Metadata-only [receipt
`#21`](https://github.com/ccoelhofize/project-iagora/issues/21) was created and
closed as `no_admission_required`. Its package manifest, receipt contract, and
all five component fingerprints were independently revalidated after download.

This exercise establishes that the bounded remote transport, package, and
receipt path operated once as designed. It does not establish source truth,
programme delivery, campaign fulfillment, outcome, impact, production
readiness, or publication authority. It created no candidate and made no
admission decision. The scheduled deadline monitor remains operationally
unexercised because the receipt was never pending.

The successful run created no pending candidate, so it could not exercise the
Increment 3 path. Merge and publication remain separate human decisions.

## Known limitations

- only one registered Opendatasoft JSON plan is executable;
- the quarantine store is local and is not a durable shared evidence store;
- the GitHub acquisition and receipt path has one successful controlled run,
  while the pending-candidate reminder and expiry path remains unexercised;
- the protected remote admission workflow is implemented but its external
  environment is not configured and no real candidate admission has run;
- an apply-phase provider failure can leave a visible partial branch or draft
  pull request that requires manual reconciliation before retry;
- no scheduling, retries, parser sandbox, malware scanning, telemetry stack, or
  production incident process exists;
- the implementation has been tested with retained and injected responses, not
  operated as a production collector.
