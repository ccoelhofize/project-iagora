# ADR-0008: Public-Source Acquisition Privacy and Security Boundaries

**Status:** Accepted  
**Owner:** Maintainers  
**Proposed:** 2026-07-28  
**Accepted:** 2026-07-28  
**Deciders:** Project maintainer  
**Supersedes:** None  
**Superseded by:** None

## Context

IAgora intends to acquire legally accessible public records, including documents and structured data from municipal portals. Public accessibility does not remove privacy, intellectual-property, terms-of-access, security, or ethical constraints. It also does not make downloaded content trustworthy.

The [CNIL's guidance for reusers](https://www.cnil.fr/fr/recommandations-reutilisateurs-donnees-internet) requires assessment of legal basis, information, individual rights, minimization, accuracy, security, and retention for personal data already published online. The [ANSSI hygiene guide](https://messervices.cyber.gouv.fr/guides/guide-dhygiene-informatique) provides a baseline for access control, updates, separation, logging, and security governance. OWASP documents threats from [malicious files](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html), [server-side request forgery](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html), and [indirect prompt injection](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html).

The pilot concerns schools, which heightens the need to avoid collecting or exposing information about children, families, or staff when programme-level or aggregate evidence is sufficient.

## Decision drivers

- Collect only information needed for a documented civic question and lawful purpose.
- Prevent a transparency platform from becoming a private-person monitoring system.
- Treat every remote source, file, metadata field, and embedded instruction as untrusted input.
- Isolate acquisition and parsing from canonical data, secrets, internal networks, and publication.
- Preserve provenance and raw evidence while minimizing harmful content and public exposure.
- Make security, privacy, rights, and licence review part of publication eligibility.
- Keep controls proportional to source and content risk without trusting official domains blindly.

## Decision

IAgora will use a risk-tiered acquisition boundary. A source may enter production only through a registered source profile, constrained acquisition path, isolated processing, deterministic validation, and governed publication review.

### Purpose and source registration

Before recurring or production acquisition, each source profile must record:

- public-interest purpose and concrete product question;
- source owner, publisher, technical endpoint, and authoritative scope;
- expected artifact and data categories;
- personal, sensitive, child-related, secret, and security risk classification;
- access basis, licence, terms, robots or rate constraints, and permitted reuse;
- acquisition frequency, volume, retention class, and observation scope;
- authentication and secret requirements;
- responsible owner, review date, and suspension conditions.

Unregistered discovery may inspect minimal metadata in a controlled environment but must not become continuous collection or public ingestion.

### Privacy boundary

IAgora must:

- define and document a lawful purpose and legal basis where personal data is processed;
- collect adequate, relevant, and necessary fields only;
- prefer non-personal, aggregate, or role-based records;
- keep information about public officials only when relevant to their documented public function;
- avoid private contact details, home information, family connections, sensitive categories, inferred traits, and unrelated history;
- exclude personal data about children from the pilot unless a later explicit decision, legal assessment, necessity test, and safeguards authorize a narrowly defined use;
- define information notices, rights handling, retention, access, correction, objection, and erasure processes before publication involving personal data;
- perform an appropriate privacy risk assessment and, where legally required, a data-protection impact assessment before high-risk processing;
- prevent identification through small cells, rare combinations, maps, free text, or linked datasets;
- avoid facial recognition, identity resolution of private persons, political profiling, social-graph construction, and generalized monitoring.

Public officials are not treated as private citizens for facts strictly relevant to their official acts, but necessity, accuracy, temporal relevance, and contextual integrity still apply.

### Network and retrieval boundary

Acquisition services must:

- use allowlisted protocols and reject local files, internal network ranges, cloud metadata services, loopback, and unsafe schemes;
- revalidate destinations after redirects and name resolution;
- enforce request, response, file-size, redirect, depth, decompression, and time limits;
- apply rate limits, source terms, and identifiable access behavior where appropriate;
- run with least privilege and no access to production secrets or unrelated internal services;
- separate source credentials by connector and prevent their inclusion in logs or evidence;
- record acquisition outcomes, fingerprints, headers needed for provenance, and security decisions without logging sensitive payloads unnecessarily.

### File and parser boundary

Every artifact is untrusted even when obtained from an official domain. The pipeline must:

- verify allowed type, extension, media type, signature, size, and structural limits;
- quarantine mismatches, encrypted or unsupported content, malware indicators, decompression bombs, and parser failures;
- disable active content, macros, embedded scripts, external references, and automatic execution;
- parse in a sandboxed, resource-limited, non-privileged environment with no unnecessary network access;
- keep original bytes read-only and publish only sanitized derivatives when rendering could execute active content;
- patch and monitor parsers and dependencies;
- prevent user-controlled filenames, paths, archive entries, or metadata from escaping assigned storage;
- require review before releasing quarantined material.

### AI and retrieved-content boundary

Source content is data, never an instruction to IAgora, an AI model, or an agent. The system must:

- separate trusted instructions from retrieved content structurally;
- strip or neutralize active remote content before model use where possible;
- constrain tool access, identity, secrets, and network permissions independently of model behavior;
- require allowlisted, schema-valid tool inputs and outputs;
- treat prompt injection, poisoned metadata, forged citations, and instructions embedded in documents as attack content;
- validate factual output against cited source fragments and deterministic publication rules;
- require human approval for high-impact publication or external action;
- log material tool and publication decisions without storing hidden reasoning or unnecessary source payloads.

Model refusal or prompt wording alone is not a sufficient security control.

### Canonicalization and publication boundary

Parsed content cannot enter canonical or public stores merely because parsing succeeded. Promotion requires:

- contract and schema validation;
- provenance and lineage completeness;
- source-authority and evidence classification;
- contradiction and temporal checks;
- privacy, small-cell, licence, retention, and access validation;
- sanitization appropriate to the output medium;
- review for personal data in unstructured text and attachments;
- a valid Knowledge Passport disclosure state.

Failure is quarantined or rejected, not silently coerced into a plausible value. AI-generated extraction remains a candidate until deterministic checks and required review succeed.

### Access, operations, and incident response

IAgora must apply least privilege, role separation, strong authentication, secret management, dependency and vulnerability management, environment separation, encrypted transport, protected backups, audit logging, monitoring, and tested incident response proportional to risk.

Security events must link to affected acquisitions and downstream assets. Incident containment may restrict evidence immediately under ADR-0007. Restoration must reapply restriction and removal decisions.

### Pilot restrictions

The “Respire à la récré” pilot will use official institutional and lawful public sources only. It will not acquire:

- pupil, family, or private staff profiles;
- social-media monitoring or private-person comments;
- precise child-level attendance, health, location, behavior, or educational records;
- facial images for recognition or identity analysis;
- leaked, bypassed, access-controlled, or unlawfully obtained material.

School-level public facts may be used only when necessary for the programme question and safe against re-identification or harm.

## Required invariants

1. Public availability never substitutes for purpose, legal basis, licence, privacy, or security review.
2. Every production source has a registered, reviewed source profile.
3. Remote content is untrusted regardless of publisher authority.
4. Acquisition and parsing cannot reach internal services, production secrets, or unrestricted tools.
5. Active content is never executed as part of evidence processing.
6. Retrieved text cannot issue instructions or authorize actions.
7. Parsing success does not authorize canonicalization or publication.
8. Personal data is minimized and private-person surveillance features are prohibited.
9. Child-related personal data is excluded from the pilot absent a later explicit decision and safeguards.
10. Publication requires provenance, contract, privacy, licence, retention, and security validation.
11. Security and privacy failures remain attributable through lineage and incident records.

## Scope

### Included

- Source registration, privacy boundaries, network retrieval, file parsing, AI isolation, canonical promotion, publication, and operational controls.
- Pilot-specific exclusions.

### Excluded

- Final technology, hosting, cloud, identity provider, or security product selection.
- Authorization for sensitive or child-level data.
- A complete security architecture, threat model, DPIA, or incident-response plan.
- Field-level data contracts and retention durations.

## Consequences

### Benefits

- The platform can use public evidence without equating availability with safety or permission.
- Isolation limits the effect of malicious files, URLs, and prompt injection.
- Privacy exclusions preserve the civic mission without enabling private-person surveillance.
- Publication becomes a governed promotion step rather than an automatic scraper output.

### Drawbacks and risks

- Source onboarding and isolated parsing add engineering and review cost.
- Some useful documents may remain quarantined until safe tooling or legal clarity exists.
- Automated personal-data detection is incomplete and can create false assurance.
- Risk classifications and legal bases require periodic expert review.

### Follow-up work

- Produce the full security architecture, threat model, source-profile contract, and privacy assessment workflow.
- Define source risk tiers and control baselines.
- Specify publication gates, quarantine operations, incident procedures, and audit tests.
- Complete a pilot privacy and licence inventory before acquisition.
- Seek qualified legal and security review before production deployment.

## Alternatives considered

### Alternative A: Trust official sources and domains

Official sources may be authoritative for some facts, but their files, dependencies, or compromised endpoints can still be unsafe. Authority is not a security control.

### Alternative B: Collect broadly, filter only at publication

This maximizes future analytical options but creates unnecessary privacy, legal, storage, and breach exposure before value is demonstrated.

### Alternative C: Prohibit all personal data

This is simple but would prevent legitimate attribution of official decisions and public roles. It also confuses necessity-based governance with an impossible absolute.

### Alternative D: Risk-tiered acquisition with isolated promotion

This is the selected approach. It supports legitimate civic records while containing technical and privacy risks, at the cost of explicit source registration and review.

## Migration and rollback

No acquisition implementation exists. Prototype collectors must remain non-production until source profiles and controls are reviewed. A connector can be suspended without changing canonical definitions. Assets acquired under weaker controls must be quarantined and revalidated before promotion.

## Validation

Before production, tests must demonstrate:

- denial of internal, loopback, metadata-service, redirected, and unsafe-scheme requests;
- safe handling of malicious, oversized, mislabeled, active, nested, and path-traversal files;
- parser isolation and absence of secret or unrestricted network access;
- prompt-injection content cannot authorize tools, change contracts, or bypass publication gates;
- source and publication records include required privacy, licence, retention, provenance, and review states;
- small-cell and unstructured-personal-data cases fail safely;
- quarantined content cannot enter canonical, search, AI retrieval, or public stores;
- incident containment and recovery preserve ADR-0007 restrictions.

Independent security review and qualified privacy review are required before production operation.

## Governance and evidence impact

This decision separates evidentiary authority from technical trust. It adds source and security metadata to provenance and requires publication eligibility to include privacy, licence, retention, and safety status. It does not make security review evidence that a civic claim is true.

## Related records

- Specifications: [`../architecture/08_DATA_PIPELINE.md`](../architecture/08_DATA_PIPELINE.md), [`../architecture/14_SECURITY.md`](../architecture/14_SECURITY.md), [`../governance/18_DATA_CONTRACTS.md`](../governance/18_DATA_CONTRACTS.md), [`../governance/21_DATA_PROVENANCE.md`](../governance/21_DATA_PROVENANCE.md), [`../governance/22_GLOSSARY.md`](../governance/22_GLOSSARY.md)
- Contracts: Planned source profile, acquisition event, quarantine, and publication-gate contracts
- Related ADRs: [ADR-0001](ADR-0001-project-vision-and-pilot-boundary.md), [ADR-0002](ADR-0002-canonical-assertion-and-evidence-model.md), [ADR-0006](ADR-0006-minimum-knowledge-passport-contract.md), [ADR-0007](ADR-0007-raw-evidence-retention-redaction-and-legal-removal.md), [ADR-0009](ADR-0009-project-licensing-policy.md)
- External references: [CNIL reuser recommendations](https://www.cnil.fr/fr/recommandations-reutilisateurs-donnees-internet), [ANSSI hygiene guide](https://messervices.cyber.gouv.fr/guides/guide-dhygiene-informatique), [OWASP file upload](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html), [OWASP SSRF](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html), [OWASP prompt injection](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html)
- RFCs or issues: None

## Decision record

- Outcome: Accepted
- Decision date: 2026-07-28
- Deciders: Project maintainer
- Rationale for outcome: Risk-tiered acquisition and isolated promotion support legitimate civic evidence while preventing public availability from being mistaken for legal permission, privacy safety, or technical trust.

## Revision notes

- 2026-07-28: Linked the newly created draft pipeline, security, contract, and provenance specifications. No decision semantics changed.
