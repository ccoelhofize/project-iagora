# SPDX-License-Identifier: EUPL-1.2

"""Build the bounded, non-public Respire à la récré vertical slice."""

from __future__ import annotations

import hashlib
import html
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from .contracts import ContractViolation, load_json, validate, validate_files


ROOT = Path(__file__).resolve().parents[2]
CONTRACTS = ROOT / "contracts" / "v1"
SOURCE_PROFILES = ROOT / "data" / "sources" / "source-profiles.json"
SNAPSHOT = ROOT / "data" / "pilot" / "pilot-snapshot.json"
CAMPAIGN_ARTIFACT = ROOT / "data" / "pilot" / "campaign-artifact.json"
ADMINISTRATIVE_EVIDENCE = ROOT / "data" / "pilot" / "administrative-evidence.json"


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()


def normalize_raw_records(raw_dataset: dict[str, Any]) -> list[dict[str, Any]]:
    """Map the bounded official API response to the source-agnostic POC fields."""
    field_map = {
        "uai": "uai",
        "school_name": "denomination_ecole",
        "school_unit": "nature",
        "children_reported": "nombre_d_enfants_concernes",
        "vegetation_year": "annee_vegetalisation",
        "reported_completion": "vegetalisation_terminee",
        "shared_courtyard": "cour_commune",
        "courtyards_reported": "nombre_de_cours_concernees",
        "existing_surface_m2": "surface_de_la_cour_existante",
        "post_vegetation_surface_m2": "surface_de_la_cour_apres_vegetalisation",
        "existing_trees": "nombre_d_arbres_existant",
        "trees_planted": "nb_arbres_plantes",
        "deimpermeabilized_surface_m2": "surface_demineralisee_en_m2_surface_nette",
        "permeable_share_percent": (
            "pourcentage_de_surface_totale_de_la_cour_rendue_permeable"
        ),
    }
    results = raw_dataset.get("results")
    if not isinstance(results, list):
        raise ContractViolation("Raw open-data response must contain a results array")
    return sorted(
        [
            {canonical: row.get(source) for canonical, source in field_map.items()}
            for row in results
        ],
        key=lambda row: row["uai"],
    )


def validate_inputs(
    root: Path = ROOT,
) -> tuple[
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
]:
    profiles_path = root / SOURCE_PROFILES.relative_to(ROOT)
    snapshot_path = root / SNAPSHOT.relative_to(ROOT)
    profiles = validate_files(profiles_path, root / "contracts/v1/source-profiles.schema.json")
    snapshot = validate_files(snapshot_path, root / "contracts/v1/pilot-snapshot.schema.json")
    campaign_path = root / snapshot["campaign_artifact"]["local_path"]
    campaign_artifact = validate_files(
        campaign_path, root / "contracts/v1/campaign-artifact.schema.json"
    )
    administrative_path = root / snapshot["administrative_evidence"]["local_path"]
    administrative_evidence = validate_files(
        administrative_path, root / "contracts/v1/administrative-evidence.schema.json"
    )
    acquisition_path = root / snapshot["source_dataset"]["raw_acquisition_event_path"]
    acquisition_event = validate_files(
        acquisition_path, root / "contracts/v1/acquisition-event.schema.json"
    )
    raw_path = root / snapshot["source_dataset"]["raw_local_path"]
    raw_dataset = load_json(raw_path)
    dataset_path = root / snapshot["source_dataset"]["local_path"]
    dataset = load_json(dataset_path)

    actual_hash = file_sha256(dataset_path)
    expected_hash = snapshot["source_dataset"]["sha256"]
    if actual_hash != expected_hash:
        raise ContractViolation(
            f"{dataset_path}: fingerprint mismatch; expected {expected_hash}, got {actual_hash}"
        )

    campaign_metadata_hash = file_sha256(campaign_path)
    expected_campaign_metadata_hash = snapshot["campaign_artifact"]["sha256"]
    if campaign_metadata_hash != expected_campaign_metadata_hash:
        raise ContractViolation(
            f"{campaign_path}: fingerprint mismatch; expected "
            f"{expected_campaign_metadata_hash}, got {campaign_metadata_hash}"
        )

    administrative_hash = file_sha256(administrative_path)
    expected_administrative_hash = snapshot["administrative_evidence"]["sha256"]
    if administrative_hash != expected_administrative_hash:
        raise ContractViolation(
            f"{administrative_path}: fingerprint mismatch; expected "
            f"{expected_administrative_hash}, got {administrative_hash}"
        )

    raw_hash = file_sha256(raw_path)
    expected_raw_hash = snapshot["source_dataset"]["raw_sha256"]
    if raw_hash != expected_raw_hash:
        raise ContractViolation(
            f"{raw_path}: fingerprint mismatch; expected {expected_raw_hash}, got {raw_hash}"
        )
    if raw_hash != acquisition_event["raw_artifact"]["sha256"]:
        raise ContractViolation("Raw artifact fingerprint differs from its acquisition event")
    if raw_path.stat().st_size != acquisition_event["response"]["byte_size"]:
        raise ContractViolation("Raw artifact byte size differs from its acquisition event")
    if acquisition_event["raw_artifact"]["local_path"] != str(raw_path.relative_to(root)):
        raise ContractViolation("Raw artifact path differs from its acquisition event")
    if (
        acquisition_event["artifact_version_id"]
        != snapshot["source_dataset"]["raw_artifact_version_id"]
    ):
        raise ContractViolation("Raw artifact version reference does not resolve")
    if not snapshot["source_dataset"]["raw_bytes_preserved"]:
        raise ContractViolation("Current official dataset snapshot must preserve exact raw bytes")

    source_index = {source["source_id"]: source for source in profiles["sources"]}
    selected_source = source_index.get(snapshot["source_dataset"]["source_id"])
    if not selected_source or selected_source["status"] != "approved_prototype":
        raise ContractViolation("Pilot dataset source is not approved for bounded prototype use")

    campaign_source = source_index.get(snapshot["campaign_artifact"]["source_id"])
    if not campaign_source or campaign_source["status"] != "link_only":
        raise ContractViolation("Campaign artifact must remain metadata-only and link-only")
    if campaign_source["rights"]["redistribution"] != "blocked":
        raise ContractViolation("Campaign artifact redistribution must remain blocked")
    if campaign_artifact["raw_bytes_preserved"]:
        raise ContractViolation("Restricted campaign HTML must not be committed to the public repository")
    if (
        snapshot["campaign_commitment"]["verification_state"]
        != "primary_source_authenticated_with_limitations"
    ):
        raise ContractViolation("Current snapshot must expose the authenticated primary source state")
    if (
        campaign_artifact["artifact_version_id"]
        != snapshot["campaign_artifact"]["artifact_version_id"]
    ):
        raise ContractViolation("Campaign artifact version reference does not resolve")

    administrative_ref = snapshot["administrative_evidence"]
    if administrative_evidence["bundle_id"] != administrative_ref["bundle_id"]:
        raise ContractViolation("Administrative evidence bundle reference does not resolve")
    if administrative_evidence["bundle_version"] != administrative_ref["bundle_version"]:
        raise ContractViolation("Administrative evidence bundle version does not resolve")
    if administrative_evidence["raw_bytes_preserved"] or administrative_ref["raw_bytes_preserved"]:
        raise ContractViolation("Administrative PDFs must remain metadata-only pending review")

    documents = administrative_evidence["documents"]
    artifact_ids = [document["artifact_version_id"] for document in documents]
    if len(artifact_ids) != len(set(artifact_ids)):
        raise ContractViolation("Administrative artifact version identifiers must be unique")
    evidence_ids = [
        fragment["evidence_id"]
        for document in documents
        for fragment in document["evidence_fragments"]
    ]
    if len(evidence_ids) != len(set(evidence_ids)):
        raise ContractViolation("Administrative evidence identifiers must be unique")
    programme_id = snapshot["programme"]["programme_id"]
    case_ids = {case["case_id"] for case in snapshot["case_studies"]}
    for document in documents:
        profile = source_index.get(document["source_id"])
        if not profile or profile["status"] != "link_only":
            raise ContractViolation(
                f"Administrative source {document['source_id']} must be registered as link-only"
            )
        if profile["rights"]["redistribution"] != "blocked":
            raise ContractViolation("Metadata-only administrative source redistribution must be blocked")
        if document["issued_at"] > snapshot["observation_cutoff"]:
            raise ContractViolation("Administrative evidence issued after the observation cut-off")
        scope = document["scope"]
        if scope["level"] == "programme" and scope["ids"] != [programme_id]:
            raise ContractViolation("Programme administrative evidence must resolve to the pilot programme")
        if scope["level"] == "school_case" and not set(scope["ids"]).issubset(case_ids):
            raise ContractViolation("Administrative school evidence contains an unknown pilot case")
        expected_amount_scope = "programme" if scope["level"] == "programme" else "school_case"
        for fragment in document["evidence_fragments"]:
            amount = fragment.get("amount")
            if amount and amount["scope"] != expected_amount_scope:
                raise ContractViolation("Administrative amount scope differs from its document scope")

    stages = {
        fragment["stage"]
        for document in documents
        for fragment in document["evidence_fragments"]
    }
    required_stages = {
        "adopted_policy",
        "budget_authorization",
        "executed_expenditure",
        "reported_delivery",
        "funding_forecast",
    }
    if not required_stages.issubset(stages):
        raise ContractViolation(
            f"Administrative chain is incomplete; missing stages {sorted(required_stages - stages)}"
        )
    for search in administrative_evidence["procurement_searches"]:
        if search["interpretation"] != "not_evidence_of_absence":
            raise ContractViolation("Procurement search gaps must not become evidence of absence")

    rows = dataset.get("records")
    if not isinstance(rows, list) or len(rows) != 6:
        raise ContractViolation("The bounded source snapshot must contain exactly six school-unit rows")
    if len({row.get("uai") for row in rows}) != len(rows):
        raise ContractViolation("Each school-unit record must have a unique UAI")
    if raw_dataset.get("total_count") != acquisition_event["response"]["record_count"]:
        raise ContractViolation("Raw response count differs from its acquisition event")
    if normalize_raw_records(raw_dataset) != rows:
        raise ContractViolation("Normalized school records do not reproduce the preserved raw response")

    expected_schools = {case["school_name"] for case in snapshot["case_studies"]}
    actual_schools = {row.get("school_name") for row in rows}
    if actual_schools != expected_schools:
        raise ContractViolation(
            f"Bounded school set differs: expected {sorted(expected_schools)}, got {sorted(actual_schools)}"
        )
    return (
        profiles,
        snapshot,
        dataset,
        campaign_artifact,
        acquisition_event,
        raw_dataset,
        administrative_evidence,
    )


def _reported_state(value: str) -> str:
    mapping = {
        "oui": "reported_complete",
        "en cours": "reported_in_progress",
        "non": "reported_not_complete",
    }
    try:
        return mapping[value]
    except KeyError as exc:
        raise ContractViolation(f"Unsupported source completion value: {value!r}") from exc


def build_passport(root: Path = ROOT) -> dict[str, Any]:
    (
        profiles,
        snapshot,
        dataset,
        campaign_artifact,
        acquisition_event,
        _,
        administrative_evidence,
    ) = validate_inputs(root)
    source = next(
        item for item in profiles["sources"] if item["source_id"] == "src-city-open-data-schools"
    )
    rows_by_school: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in dataset["records"]:
        transformed = dict(row)
        transformed["reported_state"] = _reported_state(row["reported_completion"])
        transformed["evidence_locator"] = f"records[uai={row['uai']}]"
        rows_by_school[row["school_name"]].append(transformed)

    case_studies = []
    evidence = [
        {
            "evidence_id": "evidence-campaign-schoolyards-2020",
            "relationship": campaign_artifact["evidence_fragment"]["relationship"],
            "artifact_version_id": campaign_artifact["artifact_version_id"],
            "locator": campaign_artifact["evidence_fragment"]["locator"],
            "source_url": campaign_artifact["archive_url"],
        }
    ]
    administrative_milestones = []
    administrative_evidence_by_case: dict[str, list[str]] = defaultdict(list)
    for document in administrative_evidence["documents"]:
        for fragment in document["evidence_fragments"]:
            milestone = {
                "evidence_id": fragment["evidence_id"],
                "stage": fragment["stage"],
                "statement": fragment["statement"],
                "locator": fragment["locator"],
                "source_title": document["title"],
                "source_url": document["canonical_url"],
                "scope_ids": document["scope"]["ids"],
                "authority_outcome": document["authority"]["outcome"],
            }
            if "amount" in fragment:
                milestone["amount"] = fragment["amount"]
            administrative_milestones.append(milestone)
            evidence.append(
                {
                    "evidence_id": fragment["evidence_id"],
                    "relationship": fragment["relationship"],
                    "artifact_version_id": document["artifact_version_id"],
                    "locator": fragment["locator"],
                    "source_url": document["canonical_url"],
                }
            )
            for scope_id in document["scope"]["ids"]:
                if scope_id.startswith("case-"):
                    administrative_evidence_by_case[scope_id].append(fragment["evidence_id"])
    for case in snapshot["case_studies"]:
        school_rows = sorted(rows_by_school[case["school_name"]], key=lambda row: row["uai"])
        states = sorted({row["reported_state"] for row in school_rows})
        summary = states[0] if len(states) == 1 else "mixed_by_school_unit"
        case_studies.append(
            {
                "case_id": case["case_id"],
                "school_name": case["school_name"],
                "purpose": case["purpose"],
                "reported_summary": summary,
                "scope_warning": "School-unit rows remain distinct and are not a programme-level conclusion.",
                "administrative_evidence_ids": sorted(
                    administrative_evidence_by_case[case["case_id"]]
                ),
                "records": school_rows,
            }
        )
        for row in school_rows:
            evidence.append(
                {
                    "evidence_id": f"evidence-{row['uai'].lower()}",
                    "relationship": "supports",
                    "artifact_version_id": snapshot["source_dataset"]["artifact_version_id"],
                    "locator": row["evidence_locator"],
                    "source_url": dataset["api_url"],
                }
            )

    passport = {
        "contract_id": "iagora.knowledge-passport",
        "contract_version": "1.0.0",
        "passport_id": "passport-pilot-respire-recre-2025",
        "passport_version": snapshot["snapshot_version"],
        "asset": {
            "asset_id": snapshot["snapshot_id"],
            "asset_type": "pilot_assessment_snapshot",
            "asset_version": snapshot["snapshot_version"],
            "lifecycle_state": "internal_prototype",
            "plain_language_description": (
                "Prototype local reliant une promesse de campagne archivée et authentifiée avec "
                "limites à une politique adoptée, à des étapes financières distinctes et à des "
                "états scolaires rapportés, sans conclure à sa réalisation ni à son impact."
            ),
        },
        "scope": {
            "territory": snapshot["territory"],
            "institution": "Ville de Clermont-Ferrand",
            "period_start": "2021-01-01",
            "observation_cutoff": snapshot["observation_cutoff"],
            "population": "three selected public-school case studies",
        },
        "assertion": {
            "epistemic_kind": "methodological_inference",
            "statement": (
                "The bounded evidence authenticates an unquantified primary campaign commitment "
                "and documents adopted policy, programme-level authorization and expenditure, and "
                "source-linked delivery states for three school cases. The commitment mapping, "
                "procurement and competent completion chain, public fulfillment conclusion, "
                "observed outcome, and causal impact remain unverified."
            ),
            "fulfillment_conclusion": snapshot["campaign_commitment"]["fulfillment_conclusion"],
            "causal_claim_class": "causal_status_not_verifiable",
        },
        "campaign_commitment": {
            "verification_state": snapshot["campaign_commitment"]["verification_state"],
            "wording": campaign_artifact["evidence_fragment"]["quote"],
            "source_scope": "Clermont-Ferrand municipal campaign",
            "quantification_state": "unquantified_in_primary_fragment",
            "mapping_state": "review_incomplete",
            "mapping_evidence_state": "candidate_evidence_found",
            "artifact_version_id": campaign_artifact["artifact_version_id"],
            "evidence_id": "evidence-campaign-schoolyards-2020",
        },
        "authority": {
            "fact_type": "reported_output_or_completion",
            "rule_version": "adr-0003-1.0",
            "outcome": "authoritative_with_limitation",
            "rationale": (
                "The competent City department publishes the structured school-unit values. The "
                "dataset is authoritative for what it reports, not for independent completion, "
                "fulfillment, outcomes, expenditure, or causal impact."
            ),
            "limitations": source["review"]["limitations"],
            "campaign_commitment": {
                "fact_type": "original_campaign_wording",
                "source_id": campaign_artifact["source_id"],
                "outcome": "authoritative_with_limitation",
                "rationale": (
                    "The archived campaign-controlled page is primary evidence for its own wording. "
                    "It is not a certified profession of faith and does not establish delivery."
                ),
                "limitations": campaign_artifact["authenticity"]["limitations"],
            },
        },
        "administrative_chain": {
            "rule_version": "adr-0003-and-adr-0004-1.0",
            "commitment_mapping": administrative_evidence["chain_summary"]["commitment_mapping"],
            "policy_adoption": administrative_evidence["chain_summary"]["policy_adoption"],
            "budget_authorization": administrative_evidence["chain_summary"]["budget_authorization"],
            "executed_expenditure": administrative_evidence["chain_summary"]["executed_expenditure"],
            "procurement": administrative_evidence["chain_summary"]["procurement"],
            "competent_completion": administrative_evidence["chain_summary"]["competent_completion"],
            "outcome_evidence": administrative_evidence["chain_summary"]["outcome_evidence"],
            "causal_impact": administrative_evidence["chain_summary"]["causal_impact"],
            "fulfillment_conclusion": administrative_evidence["chain_summary"]["fulfillment_conclusion"],
            "financial_distinctions": [
                "Programme authorization is not annual payment credit.",
                "Annual payment credit is not executed expenditure.",
                "Programme expenditure is not a school allocation.",
                "Reported or forecast site cost is not a contract or payment."
            ],
            "procurement_searches": administrative_evidence["procurement_searches"],
            "milestones": sorted(
                administrative_milestones, key=lambda item: item["evidence_id"]
            ),
        },
        "evidence": sorted(evidence, key=lambda item: item["evidence_id"]),
        "provenance": {
            "source_id": source["source_id"],
            "publisher": dataset["publisher"],
            "source_url": dataset["source_url"],
            "acquired_at": dataset["acquired_at"],
            "source_modified_at": dataset["source_modified_at"],
            "artifact_version_id": snapshot["source_dataset"]["artifact_version_id"],
            "content_fingerprint_sha256": snapshot["source_dataset"]["sha256"],
            "raw_bytes_preserved": dataset["raw_bytes_preserved"],
            "raw_artifact": {
                "artifact_version_id": acquisition_event["artifact_version_id"],
                "acquisition_event_id": acquisition_event["event_id"],
                "local_path": acquisition_event["raw_artifact"]["local_path"],
                "content_fingerprint_sha256": acquisition_event["raw_artifact"]["sha256"],
                "byte_size": acquisition_event["response"]["byte_size"],
                "acquired_at": acquisition_event["acquired_at"],
                "media_type": acquisition_event["response"]["media_type"],
            },
            "campaign_artifact": {
                "source_id": campaign_artifact["source_id"],
                "original_url": campaign_artifact["original_url"],
                "archive_url": campaign_artifact["archive_url"],
                "capture_at": campaign_artifact["capture_at"],
                "acquired_at": campaign_artifact["acquired_at"],
                "artifact_version_id": campaign_artifact["artifact_version_id"],
                "content_fingerprint_sha256": campaign_artifact[
                    "content_fingerprint_sha256"
                ],
                "raw_bytes_preserved": campaign_artifact["raw_bytes_preserved"],
                "nonretention_reason": campaign_artifact["nonretention_reason"],
            },
            "administrative_evidence": {
                "bundle_id": administrative_evidence["bundle_id"],
                "bundle_version": administrative_evidence["bundle_version"],
                "local_path": snapshot["administrative_evidence"]["local_path"],
                "content_fingerprint_sha256": snapshot["administrative_evidence"]["sha256"],
                "assembled_at": administrative_evidence["assembled_at"],
                "document_count": len(administrative_evidence["documents"]),
                "raw_bytes_preserved": administrative_evidence["raw_bytes_preserved"],
            },
        },
        "lineage": [
            {
                "event_id": "lineage-authenticate-campaign-artifact-001",
                "event_type": "evidence_authentication",
                "input": snapshot["campaign_artifact"]["local_path"],
                "input_sha256": snapshot["campaign_artifact"]["sha256"],
                "archived_content_sha256": campaign_artifact["content_fingerprint_sha256"],
                "review_outcome": campaign_artifact["authenticity"]["outcome"],
                "deterministic": False,
            },
            {
                "event_id": acquisition_event["event_id"],
                "event_type": "acquisition",
                "input": acquisition_event["resolved_url"],
                "output": acquisition_event["raw_artifact"]["local_path"],
                "output_sha256": acquisition_event["raw_artifact"]["sha256"],
                "result": "accepted_after_contract_validation",
                "deterministic": False,
            },
            {
                "event_id": "lineage-normalize-open-data-subset-001",
                "event_type": "normalization",
                "input": acquisition_event["raw_artifact"]["local_path"],
                "input_sha256": acquisition_event["raw_artifact"]["sha256"],
                "rule_version": "iagora.pilot.normalize-open-data/0.2.0",
                "output": snapshot["source_dataset"]["local_path"],
                "output_sha256": snapshot["source_dataset"]["sha256"],
                "deterministic": True,
            },
            {
                "event_id": "lineage-review-administrative-evidence-001",
                "event_type": "evidence_review",
                "input": snapshot["administrative_evidence"]["local_path"],
                "input_sha256": snapshot["administrative_evidence"]["sha256"],
                "rule_version": "iagora.pilot.administrative-evidence/0.1.0",
                "result": "partial_chain_validated_publication_still_blocked",
                "deterministic": False,
            },
            {
                "event_id": "lineage-project-knowledge-passport-001",
                "event_type": "projection",
                "input": snapshot["source_dataset"]["local_path"],
                "input_sha256": snapshot["source_dataset"]["sha256"],
                "rule_version": "iagora.pilot.project-passport/0.3.0",
                "output": "knowledge-passport",
                "deterministic": True,
            },
            {
                "event_id": "lineage-publication-gate-001",
                "event_type": "publication_validation",
                "rule_version": "iagora.publication-gate/0.1.0",
                "result": "blocked",
                "blockers": snapshot["publication_gate"]["blockers"],
            },
        ],
        "quality": {
            "intended_use": "Local validation of contracts, lineage, scope separation, and rendering.",
            "excluded_uses": [
                "Public campaign fulfillment conclusion",
                "School-level executed expenditure conclusion",
                "Outcome or causal-impact conclusion",
                "Generalization beyond the three selected cases",
            ],
            "fitness": "fit_for_local_prototype_only",
            "known_limitations": [
                "The exact bounded open-data response is preserved, but broader source history is not.",
                "Campaign HTML is fingerprinted but not retained because redistribution is blocked.",
                "Source values have not been corroborated with competent completion records.",
                "Dataset acquisition occurred after the historical observation cut-off.",
                "Administrative PDF bytes are fingerprinted but not retained pending rights and privacy review.",
                "Programme-level financial records cannot be allocated to individual schools from the reviewed evidence.",
            ],
        },
        "conflicts_and_uncertainty": [
            "The primary campaign fragment is unquantified and does not state a delivery date, budget, or number of schoolyards.",
            "The all-neighbourhood scope appears in supporting interview evidence, not in the retained primary fragment.",
            "Pierre-et-Marie-Curie has different reported states for its maternelle and élémentaire units; this is a scope difference, not a resolved contradiction.",
            "The 1.09 million euros reported for 2022 and 1,939,810.63 euros of cumulative mandates before 2023 have different periods and precision; they must not be treated as contradictory or interchangeable.",
            "No unambiguous Respire procurement record was found in the bounded searches; this is a search gap, not evidence that no contract exists.",
            "No reviewed baseline, outcome indicator, counterfactual, or contribution analysis is available.",
        ],
        "rights": {
            "license_id": dataset["license_id"],
            "attribution": dataset["publisher"],
            "source_rights_apply": True,
            "retention_class": source["retention"]["class"],
            "production_review_required": True,
            "campaign_artifact": {
                "state": campaign_artifact["rights"]["state"],
                "redistribution": campaign_artifact["rights"]["redistribution"],
                "raw_bytes_preserved": campaign_artifact["raw_bytes_preserved"],
                "nonretention_reason": campaign_artifact["nonretention_reason"],
            },
            "administrative_evidence": {
                "state": "rights_review_pending",
                "redistribution": "blocked",
                "raw_bytes_preserved": administrative_evidence["raw_bytes_preserved"],
                "retention_class": "metadata_only",
            },
        },
        "review": {
            "state": "prototype_maintainer_review_only",
            "reviewer_role": "maintainer",
            "methodological_review_complete": False,
            "correction_channel": "repository issue or pull request",
        },
        "accessibility": {
            "language": "fr",
            "plain_language_summary_present": True,
            "non_visual_table_present": True,
            "status_not_conveyed_by_color_only": True,
        },
        "case_studies": case_studies,
        "publication": snapshot["publication_gate"],
    }
    schema = load_json(root / "contracts/v1/knowledge-passport.schema.json")
    validate(passport, schema)
    return passport


def _display(value: Any) -> str:
    if value is None:
        return "Non communiqué"
    return html.escape(str(value))


def render_html(passport: dict[str, Any]) -> str:
    status_labels = {
        "reported_complete": "Achèvement déclaré par la source",
        "reported_in_progress": "En cours selon la source",
        "reported_not_complete": "Non achevé selon la source",
        "mixed_by_school_unit": "États différents selon l’unité scolaire",
    }
    milestones = {
        item["evidence_id"]: item for item in passport["administrative_chain"]["milestones"]
    }

    def milestone_link(evidence_id: str, label: str) -> str:
        item = milestones[evidence_id]
        return (
            f'<a href="{html.escape(item["source_url"], quote=True)}" '
            f'rel="external noreferrer">{html.escape(label)}</a>'
        )

    chain_rows = [
        (
            "Correspondance promesse → programme",
            "Pièce candidate trouvée, revue méthodologique incomplète",
            milestone_link("evidence-pev-respire-definition-2023", "Projet éducatif adopté"),
        ),
        (
            "Politique publique",
            "Adoption établie",
            milestone_link("evidence-pev-adoption-2023", "Délibération du 5 mai 2023"),
        ),
        (
            "Autorisation budgétaire",
            "Établie à l’échelle du programme",
            milestone_link("evidence-apcp-respire-total-2022", "AP de 4,07 M€")
            + " ; "
            + milestone_link("evidence-budget-2023-cp-opened", "810 000 € de CP 2023"),
        ),
        (
            "Dépense exécutée",
            "Établie à l’échelle du programme, non répartie par école",
            milestone_link("evidence-account-2022-respire-expenditure", "1,09 M€ en 2022")
            + " ; "
            + milestone_link(
                "evidence-budget-2023-prior-mandates", "1 939 810,63 € cumulés avant 2023"
            ),
        ),
        (
            "Marchés publics",
            "Aucune pièce non ambiguë localisée dans la recherche bornée",
            "Lacune de recherche — ce n’est pas une preuve d’absence",
        ),
        (
            "Livraison et réception",
            "Livraison déclarée pour certains sites ; réception compétente non localisée",
            milestone_link("evidence-transition-nestor-reported-use", "Nestor-Perret")
            + " ; "
            + milestone_link("evidence-pierre-curie-reported-delivery", "Curie maternelle")
            + " ; "
            + milestone_link("evidence-jean-zay-forecast-cost", "Jean-Zay : prévision"),
        ),
        (
            "Résultats et impact",
            "Non établis",
            "Aucun indicateur de résultat ni dispositif causal revu",
        ),
    ]
    rendered_chain_rows = "".join(
        "<tr>"
        f'<th scope="row">{html.escape(stage)}</th>'
        f"<td>{html.escape(state)}</td>"
        f"<td>{evidence_cell}</td>"
        "</tr>"
        for stage, state, evidence_cell in chain_rows
    )
    sections = []
    for case in passport["case_studies"]:
        rows = []
        for record in case["records"]:
            rows.append(
                "<tr>"
                f"<th scope=\"row\">{_display(record['school_unit'])}</th>"
                f"<td>{_display(record['uai'])}</td>"
                f"<td>{_display(record['vegetation_year'])}</td>"
                f"<td>{_display(status_labels[record['reported_state']])}</td>"
                f"<td>{_display(record['deimpermeabilized_surface_m2'])}</td>"
                f"<td>{_display(record['trees_planted'])}</td>"
                "</tr>"
            )
        sections.append(
            f"""
            <section aria-labelledby="{html.escape(case['case_id'])}">
              <h2 id="{html.escape(case['case_id'])}">{html.escape(case['school_name'])}</h2>
              <p><strong>Lecture :</strong> {html.escape(status_labels[case['reported_summary']])}.</p>
              <p>{html.escape(case['scope_warning'])}</p>
              <p><strong>Pièces administratives reliées :</strong> {len(case['administrative_evidence_ids'])}. Leur présence ne vaut ni réception des travaux ni preuve d’impact.</p>
              <div class="table-wrap" tabindex="0" aria-label="Tableau défilable des données de {html.escape(case['school_name'])}">
                <table>
                  <caption>Données déclarées dans le jeu open data pour {html.escape(case['school_name'])}</caption>
                  <thead><tr><th scope="col">Unité</th><th scope="col">UAI</th><th scope="col">Année</th><th scope="col">État déclaré</th><th scope="col">Surface désimperméabilisée (m²)</th><th scope="col">Arbres plantés</th></tr></thead>
                  <tbody>{''.join(rows)}</tbody>
                </table>
              </div>
            </section>
            """
        )

    blockers = "".join(f"<li>{html.escape(item)}</li>" for item in passport["publication"]["blockers"])
    limits = "".join(f"<li>{html.escape(item)}</li>" for item in passport["conflicts_and_uncertainty"])
    source_url = html.escape(passport["provenance"]["source_url"], quote=True)
    return f"""<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>IAgora — POC Respire à la récré</title>
  <style>
    :root {{ color-scheme: light; font-family: system-ui, sans-serif; line-height: 1.55; }}
    body {{ margin: 0; color: #17211b; background: #f5f7f5; }}
    main {{ max-width: 68rem; margin: auto; padding: 2rem 1rem 4rem; }}
    .banner {{ border: .25rem solid #6c4514; background: #fff4dc; padding: 1rem; }}
    section {{ background: white; margin-top: 1.5rem; padding: 1.25rem; border: 1px solid #c7d0ca; }}
    table {{ width: 100%; border-collapse: collapse; }}
    caption {{ text-align: left; font-weight: 700; padding-bottom: .5rem; }}
    th, td {{ padding: .6rem; border: 1px solid #9eaaa2; text-align: left; }}
    .table-wrap {{ overflow-x: auto; }}
    a {{ color: #004f3d; text-decoration-thickness: .12em; }}
    :focus-visible {{ outline: .2rem solid #7a2e00; outline-offset: .2rem; }}
  </style>
</head>
<body>
<main>
  <h1>POC « Respire à la récré »</h1>
  <div class="banner" role="status">
    <strong>Prototype local — publication bloquée.</strong>
    Ce rendu démontre la traçabilité technique. Il ne conclut ni à la réalisation de la promesse, ni à un impact sur la ville.
  </div>
  <section aria-labelledby="engagement">
    <h2 id="engagement">Engagement de campagne retrouvé</h2>
    <p>La page de campagne archivée présente la proposition <q>{html.escape(passport['campaign_commitment']['wording'])}</q>.</p>
    <p><a href="{html.escape(passport['provenance']['campaign_artifact']['archive_url'], quote=True)}" rel="external noreferrer">Consulter la capture archivée</a>. Le fragment ne précise ni nombre de cours, ni échéance, ni budget. Son rapprochement avec « Respire à la récré » reste à valider.</p>
  </section>
  <section aria-labelledby="conclusion">
    <h2 id="conclusion">Ce que l’on peut conclure</h2>
    <p>Le document primaire est <strong>authentifié avec limites</strong>. La chaîne administrative est maintenant partiellement documentée, mais le respect de la promesse reste <strong>non vérifiable</strong> : le rapprochement méthodologique n’est pas validé et les marchés, réceptions, résultats et impacts restent incomplets. Les états scolaires ci-dessous proviennent d’un jeu de données municipal acquis après la date d’observation du 31 décembre 2025.</p>
  </section>
  <section aria-labelledby="chaine">
    <h2 id="chaine">Croisement avec les décisions et les finances municipales</h2>
    <p>Chaque montant conserve son étape et sa portée. Un budget voté n’est pas une dépense, une dépense de programme n’est pas une dépense par école, et un coût annoncé n’est pas un paiement.</p>
    <div class="table-wrap" tabindex="0" aria-label="Tableau défilable de la chaîne administrative">
      <table>
        <caption>État des preuves administratives au 31 décembre 2025</caption>
        <thead><tr><th scope="col">Étape</th><th scope="col">État vérifiable</th><th scope="col">Pièce ou limite</th></tr></thead>
        <tbody>{rendered_chain_rows}</tbody>
      </table>
    </div>
  </section>
  {''.join(sections)}
  <section aria-labelledby="limites">
    <h2 id="limites">Limites et incertitudes</h2>
    <ul>{limits}</ul>
  </section>
  <section aria-labelledby="blocages">
    <h2 id="blocages">Pourquoi la publication est bloquée</h2>
    <ul>{blockers}</ul>
  </section>
  <section aria-labelledby="source">
    <h2 id="source">Source et passeport</h2>
    <p><a href="{source_url}" rel="external noreferrer">Jeu de données de la Ville de Clermont-Ferrand</a>, Licence Ouverte 2.0.</p>
    <p>Les dix PDF administratifs sont enregistrés sous forme de métadonnées, empreintes et citations précises ; leurs octets ne sont pas redistribués avant la revue des droits et de la vie privée.</p>
    <p>Le fichier <code>passport.json</code> fournit la version machine-readable équivalente.</p>
  </section>
</main>
</body>
</html>
"""


def build(output_dir: Path, root: Path = ROOT) -> tuple[Path, Path]:
    passport = build_passport(root)
    output_dir.mkdir(parents=True, exist_ok=True)
    passport_path = output_dir / "passport.json"
    html_path = output_dir / "index.html"
    passport_path.write_text(
        json.dumps(passport, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    html_path.write_text(render_html(passport), encoding="utf-8")
    return passport_path, html_path
