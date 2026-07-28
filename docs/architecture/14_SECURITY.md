# Security Architecture

**Status:** Draft  
**Owner:** Maintainers  
**Last reviewed:** 2026-07-28

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

ADR-0008 establishes boundaries, but no controls are implemented and no production security assessment, DPIA, or incident plan exists.
