# Data Provenance

**Status:** Draft  
**Owner:** Maintainers  
**Last reviewed:** 2026-08-03

## Purpose

Provenance records origin, publication, acquisition, and custody. It does not establish authority or describe every later transformation.

## Source identity

Records MUST distinguish publisher, portal or host, competent authority, campaign actor, data supplier, and IAgora collector when these differ. Observed names and URLs map to stable canonical identities without erasing source wording.

## Acquisition event

Each attempt records source profile and endpoint, requested and resolved location, acquisition time, method, response status, relevant headers, media type, size, fingerprint, software version, authentication class without secrets, licence or terms state, retention and access class, and security outcome.

## Artifact version

An acquired version binds the exact bytes or a governed explanation of why bytes cannot be retained to publication date, acquisition event, language, fingerprint, source identifiers, rights, lifecycle state, and supersession relationships.

## Authenticity and custody

Authenticity checks MAY use publisher signatures, hashes, official registers, archival references, or corroborating metadata. The method and limitations must be recorded. IAgora MUST NOT claim legal authenticity from a URL alone.

## Rights and privacy

Provenance carries the actual source licence, rights holder where known, attribution, access conditions, redistribution limits, personal-data classification, and review state. `Rights unknown` blocks redistribution.

## Publication

The Knowledge Passport exposes the source and acquisition context needed for inspection while withholding secrets, unsafe locations, and unnecessary personal data.

## Current implementation

The pilot source registry and normalized open-data subset record publisher, URLs, acquisition and source-modification times, rights, retention class, and a local content fingerprint. Three bounded City API responses are preserved byte-for-byte with validated [historical acquisition events](../../contracts/v1/acquisition-event.schema.json), request parameters, sizes, media types, SHA-256 fingerprints, rights, privacy minimization, security results, and immutable relative paths. The normalized six-record school file must reproduce its selected raw fields exactly. The procurement responses retain eight holder-grain rows for three procurement identifiers and one citywide works-framework row; repeated contract amounts are aggregated once per identifier and framework maxima are not spending.

The pre-stable generalized [attempt](../../contracts/v1/acquisition-attempt.schema.json), [artifact-version](../../contracts/v1/source-artifact-version.schema.json), [safe-receipt](../../contracts/v1/acquisition-receipt.schema.json), and [admission-review](../../contracts/v1/admission-review.schema.json) contracts are executable. Deterministic compatibility projections expose the three historical acquisitions through those boundaries without fabricating missing plan versions, connector-rule versions, package dates, or decision times. No live component emits these records yet.

The archived campaign artifact separately records the original and archive URLs, Wayback capture time, acquisition time, media type, byte size, replay fingerprint, precise fragment, authenticity basis, rights notice, and governed non-retention reason. Its raw HTML is not stored because the archived notice restricts redistribution. BOAMP notice metadata follows the same fail-closed principle: the official catalog stated no dataset licence, so the pilot retains notice identifiers, minimal extracted facts, response size, SHA-256 fingerprint, and non-retention reason, but no raw response bytes. General production acquisition, custody, quarantine storage, and lifecycle operation remain incomplete.
