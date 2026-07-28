# ADR-0007: Raw-Evidence Retention, Redaction, and Legal Removal

**Status:** Accepted  
**Owner:** Maintainers  
**Proposed:** 2026-07-28  
**Accepted:** 2026-07-28  
**Deciders:** Project maintainer  
**Supersedes:** None  
**Superseded by:** None

## Context

IAgora's accepted model treats raw evidence as immutable in normal operation so that later claims and transformations remain reproducible. Immutability cannot override applicable deletion, intellectual-property, privacy, safety, court, or security obligations. Public sources can be corrected, withdrawn, unlawfully published, malicious, or unsuitable for indefinite retention.

The [GDPR](https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng?eliuri=eli%3Areg%3A2016%3A679%3Aoj&locale=fr) establishes purpose limitation, data minimization, accuracy, storage limitation, erasure rights, and data protection by design. The [CNIL recommendations for reusers of online data](https://www.cnil.fr/fr/recommandations-reutilisateurs-donnees-internet) require a reuser to assess legal basis, information, rights, minimization, accuracy, security, and limited retention even when data is already public.

A governed exception model is therefore needed before production acquisition. This ADR defines lifecycle principles, not legal conclusions or fixed retention durations.

## Decision drivers

- Preserve reproducibility and historical evidence without claiming that retention is unlimited.
- Separate original captured bytes from public or redacted derivatives.
- Make corrections additive and reviewable.
- Respond promptly to credible legal, privacy, safety, security, and rights requests.
- Propagate restrictions or removals to derivatives, indexes, caches, exports, and backups.
- Preserve the smallest lawful audit trail without retaining prohibited content.
- Define recovery and approval controls for destructive operations.

## Decision

Raw evidence will be immutable **within a governed lifecycle**. IAgora must never silently overwrite a captured object, but it may restrict, quarantine, redact a derived copy, or remove content under an approved procedure.

### Separate records

The system must keep distinct:

- the original captured bytes and acquisition metadata;
- non-destructive annotations and corrections;
- public redacted or normalized derivatives;
- canonical assertions and interpretations;
- restriction, withdrawal, retention, and removal decisions;
- tombstones and downstream invalidation records.

A redacted derivative must reference its source and redaction method. It must never replace the original while that original may lawfully be retained.

### Retention classification

Every acquisition requires a versioned retention decision based on:

- documented purpose and legal basis when personal data is involved;
- source and artifact type;
- applicable licence, terms, intellectual-property, and access constraints;
- evidentiary and reproducibility need;
- personal, sensitive, secret, illegal, or harmful content risk;
- expected correction and appeal horizon;
- contractual or public-record obligations;
- backup, cache, and derived-data behavior;
- a review date, retention period or decision rule, and responsible role.

There is no universal `retain forever` default. Absence of an accepted retention class blocks production acquisition or publication for that source type.

### Lifecycle states

At minimum, raw objects must support:

- `active`: retained and available to authorized processing;
- `restricted`: retained but access is limited for a documented reason;
- `quarantined`: isolated pending security, legality, or rights review;
- `withdrawn`: no longer used or publicly accessible while disposition is decided;
- `scheduled_for_removal`: approved for deletion under a recorded plan;
- `removed`: content deleted from governed stores to the extent required and feasible;
- `retention_expired`: retention rule reached and review or removal is required.

Lifecycle state changes are append-only decisions. Public availability is a separate attribute from internal retention.

### Correction and source withdrawal

A source correction creates a new acquisition and explicit supersession relationship. The earlier version remains available according to its retention and access class and is not presented as current.

Source disappearance alone does not prove that retention is unlawful. Conversely, continued public availability does not prove that IAgora may collect, republish, or retain the content indefinitely.

### Restriction and removal procedure

A credible request or detected issue must trigger a recorded case with a reason category, affected object identifiers, requester or detecting channel, time, urgency, and responsible role. The process must:

1. prevent further publication or processing immediately when risk warrants it;
2. preserve evidence of the request without copying unnecessary sensitive content;
3. assess identity, authority, scope, legal basis, licence, security, and downstream dependencies;
4. decide whether to correct, redact a derivative, restrict, quarantine, withdraw, or remove;
5. record the decision, rationale, approving role, scope, and effective time;
6. propagate the decision to canonical records, search indexes, AI retrieval stores, caches, exports, replicas, and published passports;
7. rebuild or withdraw affected outputs whose evidentiary basis is no longer safe or available;
8. address backups through documented expiry, isolation, and non-restoration controls;
9. preserve only a minimal lawful tombstone and audit record;
10. notify affected internal owners and, where required, the requester or public users.

An urgent restriction may precede final review. Permanent removal and restoration require role-separated approval except when an automated security control must isolate malicious content.

### Minimal tombstone

After removal, IAgora should retain only what is lawful and necessary to explain the discontinuity, such as:

- internal object identifier;
- non-sensitive reason code;
- decision and effective timestamps;
- approving role;
- affected downstream identifiers;
- removal scope and completion state;
- a fingerprint only when retaining it is lawful and safe.

The tombstone must not contain the prohibited content, unnecessary personal data, secret values, or a reversible representation.

### Backup and derived-output behavior

Removal plans must define active stores, replicas, object versions, indexes, caches, logs, exports, and backups. When immediate deletion from immutable backups is infeasible, the content must be inaccessible in normal operation, expire under a documented schedule, and not be restored into active service.

Derived outputs are not automatically valid after source removal. Their passports must show the restriction, loss of inspectability, and review result. An output must be withdrawn if continued publication would be unlawful, unsafe, or materially misleading.

### Legal holds and disputes

A documented legal hold may pause routine deletion only when authorized and legally applicable. It must be scoped, access-controlled, periodically reviewed, and released explicitly. A hold is not a general exception to privacy, security, or minimization requirements.

### Prohibited retention behavior

IAgora must not:

- keep prohibited content merely to prove that it once existed;
- silently delete evidence to improve a political or analytical conclusion;
- use redaction to change an assertion's substantive meaning;
- log raw sensitive content in removal workflows;
- restore removed content from backups without reapplying the decision record;
- infer legal permission from source accessibility alone.

## Required invariants

1. Normal corrections never overwrite raw evidence.
2. Immutability is subordinate to lawful removal and safety obligations.
3. Raw originals, redacted derivatives, annotations, and canonical interpretations remain distinct.
4. Every object has an explicit retention and access state before production use.
5. Restriction and removal propagate through all known downstream representations.
6. Tombstones retain no more information than lawfully necessary.
7. Removal never silently rewrites a historical assessment; it produces a visible restriction, invalidation, or supersession state where lawful.
8. Destructive operations are scoped, approved, logged, and recoverable when the governing obligation permits recovery.
9. Backups cannot silently reintroduce removed content.
10. Political convenience or unfavorable evidence is never a valid removal reason.

## Scope

### Included

- Raw-evidence lifecycle, correction, restriction, quarantine, redaction, withdrawal, removal, and tombstones.
- Propagation to derived assets and backups.
- Governance roles and minimum audit information.

### Excluded

- Fixed duration tables for specific source categories.
- Legal advice or a determination of IAgora's future controller or processor status.
- Detailed incident-response playbooks or storage technology.
- Approval to acquire any particular source.

## Consequences

### Benefits

- Reproducibility remains the default without turning immutability into an unsafe absolute.
- Corrections and exceptional removals are distinguishable and auditable.
- Downstream publications cannot quietly continue using withdrawn evidence.
- The approach supports privacy rights, licence obligations, and security incidents.

### Drawbacks and risks

- Propagating restrictions across lineage, indexes, exports, and backups is operationally complex.
- Minimal tombstones may reduce later forensic or reproducibility options.
- Case-by-case legal review can slow acquisition and publication.
- Poor retention classification could either erase valuable evidence too early or retain it too long.

### Follow-up work

- Create a source-class retention schedule after legal and operational review.
- Define roles, service targets, request verification, appeals, and emergency restriction procedures.
- Add contracts for lifecycle state, tombstones, redactions, and downstream invalidation.
- Test deletion propagation, backup non-restoration, correction, and passport disclosure.

## Alternatives considered

### Alternative A: Immutable forever

This maximizes reproducibility but conflicts with legal, privacy, safety, security, and rights obligations and is therefore not viable.

### Alternative B: Overwrite or delete without a retained decision record

This is operationally simple but destroys traceability and could enable politically motivated or accidental disappearance.

### Alternative C: Retain only source URLs

This reduces storage and rights exposure but cannot preserve changing or disappearing evidence and makes transformations hard to reproduce.

### Alternative D: Governed lifecycle with minimal lawful tombstones

This is the selected approach. It balances evidentiary integrity with deletion and safety obligations, at the cost of explicit lifecycle and propagation machinery.

## Migration and rollback

No production evidence store exists. Before ingestion begins, every source class must receive a provisional or accepted retention rule. Changing a rule must not silently extend the retention of existing personal data; affected objects require review. Permanent removal cannot be rolled back when no lawful copy remains, so destructive execution requires validated scope and approval.

## Validation

Implementation must demonstrate that:

- immutable correction tests create new versions;
- lifecycle transitions are authorized and auditable;
- a removal test reaches active storage, replicas, search, AI retrieval, caches, exports, and backup restoration controls;
- no removed bytes appear in tombstones or logs;
- dependent assets are invalidated, rebuilt, or withdrawn according to policy;
- public passports distinguish corrected, restricted, withdrawn, and removed evidence;
- unrelated evidence cannot be deleted through an over-broad request.

Legal review is required before production retention schedules are adopted.

## Governance and evidence impact

This decision qualifies the raw-evidence immutability principle without weakening it for ordinary corrections or political convenience. It adds governed lifecycle decisions to provenance and lineage and makes removal effects visible through Knowledge Passports whenever lawful.

## Related records

- Specifications: [`../governance/17_SOURCE_OF_EVIDENCE.md`](../governance/17_SOURCE_OF_EVIDENCE.md), [`../governance/19_DATA_LINEAGE.md`](../governance/19_DATA_LINEAGE.md), [`../architecture/08_DATA_PIPELINE.md`](../architecture/08_DATA_PIPELINE.md), [`../governance/22_GLOSSARY.md`](../governance/22_GLOSSARY.md)
- Contracts: Planned raw-object lifecycle, redaction, tombstone, and invalidation contracts
- Related ADRs: [ADR-0001](ADR-0001-project-vision-and-pilot-boundary.md), [ADR-0002](ADR-0002-canonical-assertion-and-evidence-model.md), [ADR-0006](ADR-0006-minimum-knowledge-passport-contract.md), [ADR-0008](ADR-0008-public-source-acquisition-privacy-and-security-boundaries.md), [ADR-0009](ADR-0009-project-licensing-policy.md)
- External references: [GDPR](https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng?eliuri=eli%3Areg%3A2016%3A679%3Aoj&locale=fr), [CNIL recommendations for reusers](https://www.cnil.fr/fr/recommandations-reutilisateurs-donnees-internet)
- RFCs or issues: None

## Decision record

- Outcome: Accepted
- Decision date: 2026-07-28
- Deciders: Project maintainer
- Rationale for outcome: A governed lifecycle preserves raw-evidence integrity in normal operation while making legal removal, safety restrictions, redaction, downstream invalidation, and minimal lawful audit records explicit.

## Revision notes

- 2026-07-28: Linked the newly created draft evidence, lineage, and pipeline specifications. No decision semantics changed.
