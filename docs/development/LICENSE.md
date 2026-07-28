# Licensing Guide

**Status:** Draft  
**Owner:** Maintainers  
**Last reviewed:** 2026-07-28

## Governing decision

[ADR-0009](../adr/ADR-0009-project-licensing-policy.md) accepts a licence policy by artifact class. This guide explains that decision; it is not a substitute for the exact legal texts or qualified legal review.

## Artifact classes

| Artifact | Accepted policy | Publication condition |
| --- | --- | --- |
| Original IAgora software | EUPL-1.2 only (`EUPL-1.2`) | Exact root licence text, ownership and compatibility review, SPDX metadata |
| Original reusable documentation | CC BY 4.0 (`CC-BY-4.0`) | Clear notice and exclusion of differently licensed material |
| IAgora-owned open dataset | Licence Ouverte 2.0 | Dataset-specific rights, privacy, provenance, confidentiality, and compatibility review |
| Third-party evidence or data | Original rights apply | Record source rights; do not relicense without authority |
| Name, logo, and branding | Not granted by the above licences | Future brand or trademark policy |

## Required records

Each published artifact or dataset must identify its licence or rights state, rights holder where known, attribution, source licences, exclusions, access and redistribution limits, and review status. `Rights unknown` blocks redistribution.

## Contributions

Contributions use inbound-equals-outbound terms for the target artifact. No copyright assignment, CLA, proprietary relicensing right, or dual-licensing model is adopted. A future DCO workflow may record contributor attestation without changing the licence.

## Dependencies and combined works

Dependencies require an inventory and compatibility review before distribution. The EUPL compatibility list does not remove the need to examine how code is combined, distributed, or operated. Automated scans assist discovery but do not establish ownership or compliance.

## Evidence and datasets

Open-source code does not make input evidence or output datasets open. When analysis is lawful but redistribution is not, IAgora may publish governed metadata, references, or lawful fragments without mirroring the source artifact.

## Implementation status

The root `LICENSE`, documentation notice, dataset manifest contract, third-party notice, dependency inventory, and SPDX checks are still absent. Until those items and the required rights review are complete, repository visibility must not be treated as a completed licence grant.

## Authoritative licence sources

- [EUPL-1.2](https://spdx.org/licenses/EUPL-1.2)
- [Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/)
- [Licence Ouverte 2.0](https://www.etalab.gouv.fr/wp-content/uploads/2017/04/ETALAB-Licence-Ouverte-v2.0.pdf)
