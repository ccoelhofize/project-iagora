# Security Architecture

**Status:** Draft  
**Owner:** Maintainers  
**Last reviewed:** 2026-08-05

## Security objectives

Protect evidence integrity, personal and restricted data, service availability, credentials, publication decisions, and the ability to trace and recover from failures.

## Trust boundaries

Remote networks, source files, archives, metadata, extracted text, user input, generated output, dependencies, and search indexes are untrusted. Acquisition and parsing are isolated from canonical stores, internal networks, secrets, and publication authority.

## Required controls

- registered sources and allowlisted retrieval protocols;
- SSRF defenses, redirect revalidation, and resource limits;
- file signature, size, archive, active-content, and malware controls;
- sandboxed non-privileged parsing without unnecessary network access;
- strong authentication, least privilege, role separation, and secret management;
- encrypted transport and protected storage appropriate to classification;
- dependency, vulnerability, patch, backup, recovery, audit, and incident processes;
- output sanitization and content-security controls;
- privacy and rights checks before canonical promotion and publication;
- prompt-injection containment through structural separation and constrained tools.

## Roles

Acquisition, review, publication, permanent removal, and security administration should be separable roles. Emergency quarantine may be automated; restoration and permanent removal require governed approval.

## Verification

Threat modeling and tests must cover malicious files, archive bombs, path traversal, SSRF, parser compromise, XSS, injection, secret leakage, privilege escalation, poisoned retrieval, unauthorized publication, removal propagation, backup restoration, and audit tampering.

## Current state

ADR-0008 establishes the boundaries. The bounded local acquisition prototype
implements a registered plan allowlist, exact query construction, HTTPS-only
retrieval, public-address validation, DNS-result pinning with TLS hostname
verification, redirect revalidation, a global timeout, response-size and media
type limits, compression rejection, exact structural validation, safe metadata,
and append-only quarantine outside the repository. Tests exercise loopback and
mixed-address rejection, changed and cross-host redirects, media and size
failures, missing stored bytes, and safe output without contacting the civic
endpoint.

The remote adapter keeps acquisition at `contents: read`, disables persisted
checkout credentials, accepts one choice-based plan identifier, verifies that
the checkout remains unchanged, and uploads only a 14-day bounded package.
Raw bytes are exported only for a structurally valid candidate; invalid results
export safe metadata. A separate job has `issues: write`, `contents: read` for
the checked-out adapter code, and no package access. It receives only the
validated receipt payload. The deadline monitor reads receipt metadata and
cannot execute acquisition. Official actions are pinned to exact revisions.
These controls are tested statically and with controlled fixtures. The
acquisition and receipt path also completed one controlled remote exercise with
an unchanged response and no raw-byte duplication or admission. The deadline
monitor remains operationally unexercised.

The Increment 3 admission adapter adds an Actions-only boundary, exact open
receipt and package-expiry checks, full component fingerprints, current plan
and source-profile binding, deterministic target paths, and a fresh receipt
fingerprint check before any repository write. Validation runs with read-only
permissions. Only the later `governed-admission` environment job receives
bounded content, issue, and pull-request writes; checkout credentials remain
unpersisted, direct `main` writes and force updates are absent, and every pull
request is draft. A repository variable keeps the workflow disabled until the
external environment protection is explicitly configured. Synthetic tests
exercise tampering, stale state, unsafe paths, permission separation, rejection,
and the lack of automatic merge or publication. The environment is not yet
configured and no real admission has been exercised. A provider failure after
branch creation can require visible manual reconciliation; automatic rollback
is not implemented.

These controls cover only one JSON plan and do not constitute a production
security assessment. No complete threat model, parser sandbox, active-content
or malware scanner, credential system, incident plan, recovery exercise,
qualified security review, or DPIA exists.
