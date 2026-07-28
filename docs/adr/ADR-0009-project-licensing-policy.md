# ADR-0009: Project Licensing Policy

**Status:** Accepted  
**Owner:** Maintainers  
**Proposed:** 2026-07-28  
**Accepted:** 2026-07-28  
**Deciders:** Project maintainer  
**Supersedes:** None  
**Superseded by:** None

## Context

IAgora describes itself as open source, but the repository correctly states that no project licence has been accepted. Public visibility does not grant reuse rights. Before accepting contributions or releasing software and data, the project must define which rights apply to code, original documentation, project-produced datasets, third-party evidence, and branding.

A single repository-wide licence would be simple but could falsely relicense public documents or datasets that IAgora does not own. Conversely, leaving every file unspecified would make legitimate reuse and contribution unsafe.

The [European Union Public Licence 1.2](https://interoperable-europe.ec.europa.eu/collection/eupl/introduction-eupl-licence) is an EU reciprocal open-source licence, available in official linguistic versions, with network-service coverage and a compatibility mechanism. [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) permits reuse and adaptation of licensed material with attribution. France's [Licence Ouverte 2.0](https://www.etalab.gouv.fr/wp-content/uploads/2017/04/ETALAB-Licence-Ouverte-v2.0.pdf) is designed for reuse of public information under French law.

This is a project-governance decision, not legal advice. Public release should follow review of ownership, compatibility, contributor expectations, and the project's intended operating model.

## Decision drivers

- Make the platform genuinely reusable while preserving public access to improvements.
- Cover web-service deployment, not only distribution of executable copies.
- Fit an EU and French civic-infrastructure context.
- Avoid claiming rights over third-party public records, campaign artifacts, or datasets.
- Give documentation and project-produced data suitable, recognizable terms.
- Keep licence provenance inspectable per artifact and dataset.
- Avoid contributor agreements or dual-licensing rights that are unnecessary at the foundation stage.

## Decision

IAgora will use a licence policy by artifact class.

### Software code

Original IAgora software code will be licensed under **EUPL-1.2 only**, using the SPDX identifier `EUPL-1.2`.

This choice was selected because the project is intended as reusable European civic infrastructure, is likely to be delivered as a network service, and should preserve access to covered improvements while retaining compatibility paths listed by the licence.

Completing the policy requires adding the exact official EUPL-1.2 text to the root `LICENSE` file and clear SPDX metadata. Until those notices and the required rights review are complete, repository visibility must not be treated as a completed licence grant.

### Original documentation

Original IAgora documentation intended for public reuse will be licensed under **Creative Commons Attribution 4.0 International**, using `CC-BY-4.0`.

Code embedded in documentation remains governed by its stated software licence. Third-party quotations, images, tables, and extracts remain under their own rights and must be identified.

### Project-produced open datasets

A dataset created and owned by IAgora may be released under **Licence Ouverte 2.0** only after a dataset-specific rights, provenance, privacy, confidentiality, and licence-compatibility review.

No collected or derived dataset is automatically open merely because it is stored in the repository or produced by open-source software. Every published dataset must carry a machine-readable licence identifier or URL, attribution requirements, source licences, coverage, exclusions, and rights-review state in its manifest and Knowledge Passport.

### Third-party evidence and data

The project licences do not apply to third-party source artifacts, campaign material, official documents, media, photographs, maps, trademarks, or data unless IAgora has the right to license them.

Such material must retain:

- its original source and rights holder where known;
- licence, public-domain status, legal reuse basis, or `rights unknown` state;
- attribution, notice, access, redistribution, and transformation constraints;
- any restriction on repository inclusion or public mirroring.

When rights permit analysis but not redistribution, IAgora may retain governed references, metadata, lawful fragments, or restricted evidence without placing the original under an IAgora licence. `Rights unknown` blocks redistribution.

### Branding and endorsement

Project names, logos, visual identity, and trademarks are not licensed by the software, documentation, or data licences. Reuse rights and attribution must not imply official endorsement by IAgora, a public institution, a campaign, or a source publisher. A future trademark and brand policy may grant limited nominative-use permissions.

### Contributions

Contributions are accepted under the licence applicable to the target artifact, on an **inbound-equals-outbound** basis. Contributors must have the right to submit their work and identify third-party material.

No copyright assignment, contributor licence agreement, or maintainer right to proprietary relicensing is adopted. A lightweight Developer Certificate of Origin process may be specified in the contributor guide, but it must not change licence scope or substitute for provenance checks.

### Repository markings and dependency policy

After acceptance, the repository must provide:

- the official EUPL-1.2 text in root `LICENSE`;
- a documentation notice for `CC-BY-4.0` and the canonical licence link;
- dataset-level manifests for Licence Ouverte 2.0 releases;
- an artifact-class explanation in `docs/development/LICENSE.md`;
- SPDX identifiers in package metadata and source files where appropriate;
- a third-party notice and dependency inventory with detected licence and compatibility review;
- explicit exclusions for third-party evidence, data, and branding.

No dependency may be introduced solely because it is technically available. Its licence obligations and compatibility with the distributed component must be reviewed and recorded.

## Required invariants

1. Repository visibility never substitutes for a licence grant.
2. Code, documentation, datasets, third-party evidence, and branding retain distinct rights treatment.
3. IAgora never relicenses material it does not have authority to license.
4. Third-party rights and attribution remain attached through transformations and publication.
5. `Rights unknown` blocks redistribution, not internal legal review.
6. Dataset publication requires a dataset-specific rights and privacy decision.
7. Contributions use inbound-equals-outbound unless a later accepted ADR changes the model.
8. No proprietary relicensing right or copyright assignment is granted by this decision.
9. Licence metadata is machine-readable and exposed in the Knowledge Passport.
10. Open-source software does not make its input evidence or output datasets automatically open.

## Scope

### Included

- Licensing policy for original code, documentation, project-produced open datasets, third-party material, branding, contributions, and dependencies.

### Excluded

- A determination that any current third-party artifact may be redistributed.
- A final trademark policy, contributor guide, DCO procedure, or dependency list.
- Legal advice, warranty of title, or permission to publish pilot data.
- Dual licensing or commercial licensing.

## Consequences

### Benefits

- The code remains reusable and reciprocal for network-delivered civic services.
- Documentation and eligible project-produced data use terms suited to their artifact type.
- Public evidence retains its actual rights rather than being swept into a false repository-wide grant.
- Contributors can understand the outbound terms without assigning ownership to maintainers.

### Drawbacks and risks

- Multiple licences require careful file, directory, package, and dataset markings.
- EUPL-1.2 is less familiar to some global contributors than Apache-2.0 or AGPL-3.0.
- Compatibility of combined works and dependencies still requires case-by-case review.
- Network reciprocity may deter organizations that want to operate modified proprietary versions.
- Licence Ouverte 2.0 may not be compatible with every input dataset or international reuse scenario.

### Follow-up work

- Obtain qualified licence review before public release.
- Verify ownership of all current repository content.
- Add exact licence texts and notices only after acceptance.
- Create the licensing guide, contributor terms, dependency inventory, third-party notices, and dataset manifest contract.
- Add automated checks for missing or contradictory licence metadata.

## Alternatives considered

### Alternative A: Apache License 2.0 for code

Apache-2.0 is familiar, permissive, and includes an explicit patent licence. It can encourage broad adoption and proprietary integration. It does not require operators to share modified network-service code, which weakens the proposed reciprocity goal.

### Alternative B: GNU AGPL 3.0-or-later for code

AGPL is widely recognized as a strong network-copyleft option. It offers clear reciprocity for hosted modifications but can create adoption and dependency-compatibility concerns. EUPL-1.2 is proposed for its EU legal and multilingual context and its stated compatibility mechanism.

### Alternative C: One licence for the entire repository

This would be easy to explain but risks applying software terms to documentation and falsely suggesting that third-party public evidence or data has been relicensed.

### Alternative D: EUPL-1.2 code with class-specific documentation and data licences

This is the selected approach. It aligns licence terms with artifact types and the European civic context, at the cost of stronger rights metadata and compliance work.

## Migration and rollback

Before this decision, no accepted licence policy existed, so no public reuse grant was changed. Before adding the licence notices and releasing the repository under them, ownership and contribution provenance must be reviewed. Once released under an open licence, permissions already granted for that version generally cannot be withdrawn from compliant recipients; changing the policy later applies prospectively and requires a new ADR plus rights-holder analysis.

## Validation

After acceptance, validation must confirm that:

- root and artifact-specific notices contain exact, authoritative licence texts or canonical links as appropriate;
- package and source metadata use valid SPDX expressions;
- files and datasets resolve to one unambiguous rights policy;
- third-party materials are excluded from IAgora licence grants and carry source-specific notices;
- dependency and combined-work compatibility is reviewed before distribution;
- dataset publication fails when rights, privacy, provenance, or licence compatibility is unresolved;
- public Knowledge Passports expose applicable licence, attribution, and restriction states.

Qualified legal review remains necessary; automated licence checks cannot establish ownership or legal compliance.

## Governance and evidence impact

Licence and rights state become mandatory provenance and Knowledge Passport fields. Rights restrictions may limit raw mirroring without changing source authority or evidentiary relevance. Missing redistribution rights must be visible and must not be misrepresented as missing evidence.

## Related records

- Specifications: [`../../README.md`](../../README.md), [`../governance/22_GLOSSARY.md`](../governance/22_GLOSSARY.md), [`../development/LICENSE.md`](../development/LICENSE.md)
- Contracts: Planned dataset manifest and third-party notice contracts
- Related ADRs: [ADR-0001](ADR-0001-project-vision-and-pilot-boundary.md), [ADR-0006](ADR-0006-minimum-knowledge-passport-contract.md), [ADR-0007](ADR-0007-raw-evidence-retention-redaction-and-legal-removal.md), [ADR-0008](ADR-0008-public-source-acquisition-privacy-and-security-boundaries.md)
- External references: [EUPL-1.2 introduction](https://interoperable-europe.ec.europa.eu/collection/eupl/introduction-eupl-licence), [EUPL-1.2 SPDX record](https://spdx.org/licenses/EUPL-1.2), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), [Licence Ouverte 2.0](https://www.etalab.gouv.fr/wp-content/uploads/2017/04/ETALAB-Licence-Ouverte-v2.0.pdf)
- RFCs or issues: None

## Decision record

- Outcome: Accepted
- Decision date: 2026-07-28
- Deciders: Project maintainer
- Rationale for outcome: The artifact-class policy combines reciprocal European civic software, reusable documentation, governed open-data publication, and explicit protection of third-party rights without adopting proprietary relicensing.

## Revision notes

- 2026-07-28: Linked the newly created draft licensing guide. No decision semantics changed.
