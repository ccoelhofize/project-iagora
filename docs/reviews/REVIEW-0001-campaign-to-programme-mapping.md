# REVIEW-0001: Campaign-to-programme mapping review packet

**Status:** Ready for maintainer review
**Owner:** Maintainers
**Prepared:** 2026-08-01
**Related issue:** [#11](https://github.com/ccoelhofize/project-iagora/issues/11)

## Purpose

This packet supports an interim single-maintainer review of mapping version `0.3.0` between the 2019 campaign commitment “Végétalisation des cours d’école” and the later municipal programme “Respire à la récré.” Two configured AI roles have audited the corrected mapping separately. The maintainer now inspects both current audits and the original evidence before recording one human decision for continued local POC use.

This interim path is a review aid, not evidence, not an independent review, and not permission to publish. Two distinct independent human reviews remain a future public-release requirement.

The machine-readable review record is [`../../data/pilot/commitment-mapping-review.json`](../../data/pilot/commitment-mapping-review.json). The reviewed proposal is [`../../data/pilot/commitment-mapping.json`](../../data/pilot/commitment-mapping.json).

## Question for reviewers

Is the candidate correspondence sufficiently supported for continued local POC presentation under the publication block when the presentation does not assert direct implementation, novelty, fulfillment, outcomes, impact, or a numerical completion percentage?

The revised relationship is `candidate_correspondence`, not `implements`. Acceptance of this mapping would establish only a reviewed correspondence between two records. It would not establish that the campaign commitment was fulfilled.

## Evidence to inspect

| Evidence | Role | Precise locator | What it can establish |
| --- | --- | --- | --- |
| `evidence-campaign-schoolyards-2020` | Original commitment | Archived “Une ville nature” page, block under “Végétalisation” | The exact, unquantified campaign wording |
| `evidence-pev-respire-definition-2023` | Programme definition | Adopted PEV annex, printed page 25, “Respire à la récré” inset | The later programme name, objectives, beneficiaries, and delivery approach |
| `evidence-pev-adoption-2023` | Policy adoption | Final deliberation, page 2 of 3, decision paragraph | Adoption of the 2022–2025 municipal education project |
| `evidence-pev-policy-history-2023` | Policy-lineage context | Final deliberation, page 2 of 3, opening paragraphs | PEV predecessors in 2015 and 2018 and continuity into the 2022–2025 version |

The artifact versions, URLs, fingerprints, authority limits, and rights states are recorded in the campaign and administrative-evidence bundles. Full campaign HTML and municipal PDF bytes are not redistributed by the repository because their rights reviews remain pending.

## Recorded findings

- The campaign and programme share compatible schoolyard-greening subject matter and municipal territory.
- The later programme is broader: it adds a name, explicit child beneficiaries, ecological and thermal objectives, permeability, inclusion, play-space design, and co-construction.
- The original fragment gives no site count, denominator, budget, financing plan, deadline, or delivery method.
- No retained first-class fragment directly says that “Respire à la récré” implements the campaign proposal.
- The adopted record identifies PEV predecessors in 2015 and 2018. This context blocks an unsupported novelty or political-credit inference, but it does not prove that the 2019 commitment had no influence.
- No material contradiction was identified in the bounded corpus. The corpus is not exhaustive, and this absence is not evidence that no contradiction exists.

## First advisory cycle on superseded mapping version 0.2.0

The machine-readable packet specifies two non-binding roles:

1. `ai_methodology_auditor`: challenges decomposition, scope comparison, candidate-correspondence vocabulary, policy-lineage treatment, prohibited inferences, and plain-language conclusions.
2. `ai_evidence_authority_auditor`: challenges artifact identity, precise fragments, authority boundaries, policy-history context, counterevidence search limits, rights constraints, and version bindings.

Each audit must return a non-binding recommendation (`accept`, `reject`, or `request_changes`), separate blockers from caveats, cite the evidence identifiers inspected, and state limitations and re-review conditions. Neither agent may approve the mapping, create evidence, invent missing campaign terms, or count its output as human review.

These are versioned, manually invoked role specifications rather than autonomous services. Both first-cycle runs are retained separately from the immutable evidence and from the maintainer decision.

| Advisory role | Non-binding recommendation | Main result |
| --- | --- | --- |
| `ai_methodology_auditor` | `accept` | No methodological blocker for continued local POC use under the publication block; four caveats remain. |
| `ai_evidence_authority_auditor` | `request_changes` | Source content and main locators are supported, but the campaign fragment and target assertion do not yet resolve end to end as stable canonical records. |

The methodology caveats concern possible confusion around the proportional six-unit chart, the missing ADR-0010 reference in the mapping method, the precision of the adoption wording, and the need to explain `candidate_correspondence` in plainer language.

The evidence-authority audit identified two blockers for accepting mapping version `0.2.0`: `evidence-campaign-schoolyards-2020` was not assigned directly to the campaign fragment in its source bundle, and `assertion-respire-schoolyard-transformation-policy-2023` had no separately resolvable canonical assertion record. These findings concerned traceability, not the existence or authenticity of the four cited documents.

## Corrections in mapping version 0.3.0

- The campaign fragment now carries `evidence-campaign-schoolyards-2020` directly.
- A separate canonical assertion bundle resolves `assertion-respire-schoolyard-transformation-policy-2023` version `0.1.0` to the exact definition and adoption fragments.
- The mapping lineage binds the canonical assertion bundle and lists ADR-0010 among its governing decisions.
- The timeline now says that the council adopted the education project containing “Respire à la récré,” rather than saying it adopted the programme directly.
- The source inventory now counts four mapping evidence references.
- The campaign source-profile rights state now matches the restrictive archived notice recorded by the campaign bundle.

Both AI roles ran again against mapping version `0.3.0`. The first repeat methodology run requested correction of three overbroad adoption statements; that run is retained as superseded by correction. After the wording was corrected and the POC rebuilt, the final methodology run recommends `accept`. The evidence-authority run also recommends `accept` after confirming that both first-cycle resolution blockers are fixed end to end.

## Current advisory result for mapping version 0.3.0

| Advisory role | Applicable run | Non-binding recommendation | Remaining caveats |
| --- | --- | --- | --- |
| `ai_methodology_auditor` | `ai-review-methodology-003` | `accept` | Test comprehension of the proportional six-unit chart; consider separate adoption and definition links. |
| `ai_evidence_authority_auditor` | `ai-review-evidence-authority-002` | `accept` | Counterevidence corpus and qualified rights review remain incomplete; third-party bytes are not retained. |

Both recommendations apply only to continued local POC use under the publication block. They are not evidence, human review, independent review, a fulfillment conclusion, or permission to publish.

## Interim maintainer decision

After both advisory audits are complete, one `maintainer_reviewer` may record the human decision for the local POC. The maintainer must inspect both audit records and the four original evidence fragments, then record:

- a pseudonymous reviewer reference and role;
- `accept`, `reject`, or `request_changes`;
- timestamp and reviewed mapping version;
- both advisory-run identifiers and all evidence identifiers inspected;
- rationale, remaining limitations, and re-review conditions.

This decision may move the internal mapping to `maintainer_reviewed_independent_review_pending`. It does not count as independent review and cannot authorize publication.

## Publication-grade independent review

Before public release, two different humans must still complete the original roles:

1. `methodological_reviewer`;
2. `evidence_authority_reviewer`.

The AI-assisted preparer is ineligible for these independent roles. Reviewer disagreement remains visible and blocks final acceptance until governed resolution.

## Decision rules

- An interim maintainer `accept` means the revised candidate correspondence is safe enough for continued local POC work under the existing publication block.
- `reject` means the available evidence cannot support even that limited correspondence.
- `request_changes` means the relationship, evidence set, scope comparison, or explanation must change before another review.
- An interim maintainer decision never removes the independent publication-review requirement or any other publication blocker.
- Future independent-review disagreement remains visible and blocks final acceptance until governed resolution.

## Mandatory output constraints

- Fulfillment remains `not_verifiable`.
- Publication remains blocked before and after the interim maintainer review.
- No implementation percentage may be calculated from the undefined campaign denominator.
- Programme details must not be retroactively presented as original campaign terms.
- The 2015 and 2018 predecessors must remain visible in any policy-lineage explanation.
- Spending, reported delivery, outcomes, impact, and political credit remain separate questions.

## Re-review conditions

Re-review is required when direct continuity evidence is found, material counterevidence appears, scope or lineage interpretation changes, the mapping method changes, a correction supersedes the reviewed mapping version, or the project moves from local POC use toward public release.
