# Data Provenance

**Status:** Draft  
**Owner:** Maintainers  
**Last reviewed:** 2026-07-29

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

The pilot source registry and normalized open-data subset record publisher, URLs, acquisition and source-modification times, rights, retention class, and a local content fingerprint. One bounded official API response is now preserved byte-for-byte with a validated [acquisition event](../../contracts/v1/acquisition-event.schema.json), request parameters, size, media type, SHA-256 fingerprint, rights, privacy minimization, security result, and immutable relative path. The normalized six-record file must reproduce the selected raw fields exactly.

The archived campaign artifact separately records the original and archive URLs, Wayback capture time, acquisition time, media type, byte size, replay fingerprint, precise fragment, authenticity basis, rights notice, and governed non-retention reason. Its raw HTML is not stored because the archived notice restricts redistribution. General production acquisition, custody, quarantine, and artifact-version contracts remain incomplete.
