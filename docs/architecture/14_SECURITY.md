# Security Architecture

**Status:** Draft  
**Owner:** Maintainers  
**Last reviewed:** 2026-08-03

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

These controls cover only one JSON plan and do not constitute a production
security assessment. No complete threat model, parser sandbox, active-content
or malware scanner, credential system, incident plan, recovery exercise,
qualified security review, or DPIA exists.
