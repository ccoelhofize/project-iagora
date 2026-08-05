# Governed Acquisition

**Status:** Draft

**Owner:** Maintainers

**Last reviewed:** 2026-08-05

## Scope

This guide covers the local Increment 1 and remote Increment 2 parts of
[RFC-0001](../rfc/RFC-0001-portable-governed-source-acquisition.md). The
implementation can replay a retained response or manually retrieve the one
registered six-school Opendatasoft plan. It validates the exact response shape,
compares the result with the historical baseline, and records safe metadata in
an append-only quarantine store outside the repository.

This is not a scheduled collector, governed raw-evidence store, admission
workflow, or publication path. No command or workflow in this guide admits
bytes to `data/raw/`, changes canonical records, or authorizes a civic
conclusion.

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

There is intentionally no admission command in this increment. A candidate
must be reviewed against its exact plan, response fingerprint, structural
validation, change report, rights, privacy, retention, and security metadata.
The future admission path requires a separate implementation and human
decision before any eligible material can be proposed for `data/raw/`.

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
untrusted raw bytes are not uploaded. The workflow has been implemented and
tested with controlled inputs but has not yet been remotely exercised.

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

Neither workflow implements admission. A later Increment 3 must revalidate the
exact package under protected human approval before it can propose a pull
request. Merge and publication remain separate human decisions.

## Known limitations

- only one registered Opendatasoft JSON plan is executable;
- the quarantine store is local and is not a durable shared evidence store;
- the GitHub acquisition and receipt workflows are present but have not yet
  been remotely exercised;
- no remote admission workflow exists;
- no scheduling, retries, parser sandbox, malware scanning, telemetry stack, or
  production incident process exists;
- the implementation has been tested with retained and injected responses, not
  operated as a production collector.
