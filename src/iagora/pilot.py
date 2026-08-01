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
from .presentation import (
    PAGE_STYLES,
    render_dashboard_html,
    render_education_html,
    render_footer,
    render_multidimensional_summary,
    render_policy_timeline,
    render_site_header,
)


ROOT = Path(__file__).resolve().parents[2]
CONTRACTS = ROOT / "contracts" / "v1"
SOURCE_PROFILES = ROOT / "data" / "sources" / "source-profiles.json"
SNAPSHOT = ROOT / "data" / "pilot" / "pilot-snapshot.json"
CAMPAIGN_ARTIFACT = ROOT / "data" / "pilot" / "campaign-artifact.json"
CANONICAL_ASSERTIONS = ROOT / "data" / "pilot" / "canonical-assertions.json"
COMMITMENT_MAPPING = ROOT / "data" / "pilot" / "commitment-mapping.json"
COMMITMENT_MAPPING_REVIEW = ROOT / "data" / "pilot" / "commitment-mapping-review.json"
ADMINISTRATIVE_EVIDENCE = ROOT / "data" / "pilot" / "administrative-evidence.json"
PROCUREMENT_EVIDENCE = ROOT / "data" / "pilot" / "procurement-evidence.json"


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
    canonical_assertions_path = root / snapshot["canonical_assertions"]["local_path"]
    canonical_assertions = validate_files(
        canonical_assertions_path,
        root / "contracts/v1/canonical-assertions.schema.json",
    )
    mapping_path = root / snapshot["commitment_mapping"]["local_path"]
    commitment_mapping = validate_files(
        mapping_path, root / "contracts/v1/commitment-mapping.schema.json"
    )
    mapping_review_path = root / snapshot["commitment_mapping_review"]["local_path"]
    commitment_mapping_review = validate_files(
        mapping_review_path,
        root / "contracts/v1/commitment-mapping-review.schema.json",
    )
    administrative_path = root / snapshot["administrative_evidence"]["local_path"]
    administrative_evidence = validate_files(
        administrative_path, root / "contracts/v1/administrative-evidence.schema.json"
    )
    procurement_path = root / snapshot["procurement_evidence"]["local_path"]
    procurement_evidence = validate_files(
        procurement_path, root / "contracts/v1/procurement-evidence.schema.json"
    )
    acquisition_path = root / snapshot["source_dataset"]["raw_acquisition_event_path"]
    acquisition_event = validate_files(
        acquisition_path, root / "contracts/v1/acquisition-event.schema.json"
    )
    raw_path = root / snapshot["source_dataset"]["raw_local_path"]
    raw_dataset = load_json(raw_path)
    procurement_acquisition_path = (
        root / procurement_evidence["city_dataset_acquisition"]["acquisition_event_path"]
    )
    procurement_acquisition_event = validate_files(
        procurement_acquisition_path, root / "contracts/v1/acquisition-event.schema.json"
    )
    procurement_raw_path = (
        root / procurement_evidence["city_dataset_acquisition"]["raw_local_path"]
    )
    procurement_raw = load_json(procurement_raw_path)
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

    procurement_hash = file_sha256(procurement_path)
    expected_procurement_hash = snapshot["procurement_evidence"]["sha256"]
    if procurement_hash != expected_procurement_hash:
        raise ContractViolation(
            f"{procurement_path}: fingerprint mismatch; expected "
            f"{expected_procurement_hash}, got {procurement_hash}"
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
    if acquisition_event["source_id"] != "src-city-open-data-schools":
        raise ContractViolation("School acquisition source reference does not resolve")
    if acquisition_event["request"].get("uai") != [
        "0630258N",
        "0630268Z",
        "0630303M",
        "0630307S",
        "0630992L",
        "0631845N",
    ]:
        raise ContractViolation("School acquisition must remain bounded to the six accepted UAIs")
    if acquisition_event["request"]["order_by"] != "uai":
        raise ContractViolation("School acquisition ordering changed unexpectedly")
    if (
        acquisition_event["artifact_version_id"]
        != snapshot["source_dataset"]["raw_artifact_version_id"]
    ):
        raise ContractViolation("Raw artifact version reference does not resolve")
    if not snapshot["source_dataset"]["raw_bytes_preserved"]:
        raise ContractViolation("Current official dataset snapshot must preserve exact raw bytes")

    procurement_raw_hash = file_sha256(procurement_raw_path)
    expected_procurement_raw_hash = procurement_evidence["city_dataset_acquisition"][
        "raw_sha256"
    ]
    if procurement_raw_hash != expected_procurement_raw_hash:
        raise ContractViolation(
            "Raw procurement artifact fingerprint differs from its evidence bundle"
        )
    if procurement_raw_hash != procurement_acquisition_event["raw_artifact"]["sha256"]:
        raise ContractViolation(
            "Raw procurement artifact fingerprint differs from its acquisition event"
        )
    if (
        procurement_raw_path.stat().st_size
        != procurement_acquisition_event["response"]["byte_size"]
    ):
        raise ContractViolation(
            "Raw procurement artifact byte size differs from its acquisition event"
        )
    if procurement_acquisition_event["raw_artifact"]["local_path"] != str(
        procurement_raw_path.relative_to(root)
    ):
        raise ContractViolation(
            "Raw procurement artifact path differs from its acquisition event"
        )
    if procurement_acquisition_event["request"].get("market_ids") != [
        "20202012301",
        "25-119",
        "25-120",
    ]:
        raise ContractViolation(
            "Procurement acquisition must remain bounded to the three reviewed identifiers"
        )
    if (
        procurement_acquisition_event["request"]["order_by"]
        != "marche_id,titulaires_denomination"
    ):
        raise ContractViolation("Procurement acquisition ordering changed unexpectedly")

    source_index = {source["source_id"]: source for source in profiles["sources"]}
    selected_source = source_index.get(snapshot["source_dataset"]["source_id"])
    if not selected_source or selected_source["status"] != "approved_prototype":
        raise ContractViolation("Pilot dataset source is not approved for bounded prototype use")

    procurement_source = source_index.get(
        procurement_evidence["city_dataset_acquisition"]["source_id"]
    )
    if not procurement_source or procurement_source["status"] != "approved_prototype":
        raise ContractViolation(
            "City procurement source is not approved for bounded prototype use"
        )
    boamp_source = source_index.get(procurement_evidence["boamp_acquisition"]["source_id"])
    if not boamp_source or boamp_source["status"] != "link_only":
        raise ContractViolation("BOAMP evidence must remain metadata-only and link-only")
    if boamp_source["rights"]["redistribution"] != "blocked":
        raise ContractViolation("BOAMP raw response redistribution must remain blocked")
    if procurement_evidence["boamp_acquisition"]["raw_bytes_preserved"]:
        raise ContractViolation("Rights-pending BOAMP response bytes must not be committed")

    campaign_source = source_index.get(snapshot["campaign_artifact"]["source_id"])
    if not campaign_source or campaign_source["status"] != "link_only":
        raise ContractViolation("Campaign artifact must remain metadata-only and link-only")
    if campaign_source["rights"]["redistribution"] != "blocked":
        raise ContractViolation("Campaign artifact redistribution must remain blocked")
    if campaign_source["rights"]["state"] != campaign_artifact["rights"]["state"]:
        raise ContractViolation("Campaign source and artifact rights states must remain aligned")
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

    mapping_ref = snapshot["commitment_mapping"]
    mapping_hash = file_sha256(mapping_path)
    if mapping_hash != mapping_ref["sha256"]:
        raise ContractViolation(
            f"{mapping_path}: fingerprint mismatch; expected "
            f"{mapping_ref['sha256']}, got {mapping_hash}"
        )
    if commitment_mapping["mapping_id"] != mapping_ref["mapping_id"]:
        raise ContractViolation("Commitment mapping identifier reference does not resolve")
    if commitment_mapping["mapping_version"] != mapping_ref["mapping_version"]:
        raise ContractViolation("Commitment mapping version reference does not resolve")
    if commitment_mapping["lifecycle_state"] != mapping_ref["lifecycle_state"]:
        raise ContractViolation("Commitment mapping lifecycle reference does not resolve")
    if commitment_mapping["territory"] != snapshot["territory"]:
        raise ContractViolation("Commitment mapping territory differs from the pilot snapshot")
    if commitment_mapping["observation_cutoff"] != snapshot["observation_cutoff"]:
        raise ContractViolation("Commitment mapping cut-off differs from the pilot snapshot")
    if (
        commitment_mapping["original_commitment"]["artifact_version_id"]
        != campaign_artifact["artifact_version_id"]
    ):
        raise ContractViolation("Commitment mapping campaign artifact reference does not resolve")
    if (
        commitment_mapping["original_commitment"]["wording"]
        != campaign_artifact["evidence_fragment"]["quote"]
    ):
        raise ContractViolation("Commitment mapping must preserve the exact primary wording")
    if (
        commitment_mapping["original_commitment"]["evidence_id"]
        != campaign_artifact["evidence_fragment"]["evidence_id"]
    ):
        raise ContractViolation("Campaign evidence identifier does not resolve to its fragment")
    if (
        commitment_mapping["target_programme"]["programme_id"]
        != snapshot["programme"]["programme_id"]
    ):
        raise ContractViolation("Commitment mapping programme reference does not resolve")
    components = commitment_mapping["components"]
    if len(components) != 1:
        raise ContractViolation("The bounded primary wording must remain one unsplit component")
    component = components[0]
    if component["component_id"] != commitment_mapping["mapping"]["component_id"]:
        raise ContractViolation("Commitment mapping component reference does not resolve")
    if component["essentiality"] != "essential" or component["component_type"] != "action":
        raise ContractViolation("The bounded commitment must remain one essential action component")
    if component["quantity"]["state"] != "not_stated":
        raise ContractViolation("The campaign fragment must not receive an invented quantity")
    if component["deadline"]["state"] != "not_stated":
        raise ContractViolation("The campaign fragment must not receive an invented deadline")
    if component["implementation_state"] != "unknown":
        raise ContractViolation("Implementation must remain unknown until mapping review completes")
    if commitment_mapping["mapping"]["state"] != "proposed_review_pending":
        raise ContractViolation("AI-assisted commitment mapping must remain a review-pending proposal")
    if commitment_mapping["method"]["proposal_origin"] != "ai_assisted":
        raise ContractViolation("Generated mapping proposal origin must remain explicit")
    if commitment_mapping["review"]["completed_reviews"]:
        raise ContractViolation("The current commitment mapping has no completed independent review")
    if commitment_mapping["review"]["final_decision"] is not None:
        raise ContractViolation("The current commitment mapping cannot contain a final review decision")
    if not commitment_mapping["lineage"]["generator"]["human_review_required"]:
        raise ContractViolation("AI-assisted commitment mapping must require human review")
    if commitment_mapping["output_constraints"]["fulfillment_conclusion"] != "not_verifiable":
        raise ContractViolation("Proposed mapping cannot change the fulfillment conclusion")
    if commitment_mapping["output_constraints"]["publication_eligible"]:
        raise ContractViolation("Proposed mapping cannot authorize publication")
    if commitment_mapping["mapping"]["relationship_role"] != "candidate_correspondence":
        raise ContractViolation(
            "Review-pending mapping must describe a candidate correspondence, not implementation"
        )
    required_comparison_dimensions = {
        "territory",
        "action_and_object",
        "quantity",
        "deadline",
        "geographic_extent",
        "institutional_continuity",
        "temporal_sequence",
    }
    actual_comparison_dimensions = {
        item["dimension"] for item in commitment_mapping["mapping"]["scope_comparison"]
    }
    if actual_comparison_dimensions != required_comparison_dimensions:
        raise ContractViolation("Commitment mapping scope comparison is incomplete")

    canonical_ref = snapshot["canonical_assertions"]
    if file_sha256(canonical_assertions_path) != canonical_ref["sha256"]:
        raise ContractViolation("Canonical assertion bundle fingerprint does not match snapshot")
    if (
        canonical_assertions["bundle_id"] != canonical_ref["bundle_id"]
        or canonical_assertions["bundle_version"] != canonical_ref["bundle_version"]
    ):
        raise ContractViolation("Canonical assertion bundle reference does not resolve")
    assertions_by_id = {
        item["assertion_id"]: item for item in canonical_assertions["assertions"]
    }
    target_assertion = assertions_by_id.get(
        commitment_mapping["target_programme"]["target_assertion_id"]
    )
    if target_assertion is None:
        raise ContractViolation("Commitment mapping target assertion does not resolve")
    if (
        target_assertion["assertion_version"]
        != commitment_mapping["target_programme"]["target_assertion_version"]
        or target_assertion["assertion_id"]
        != commitment_mapping["mapping"]["target_assertion_id"]
        or target_assertion["assertion_version"]
        != commitment_mapping["mapping"]["target_assertion_version"]
    ):
        raise ContractViolation("Commitment mapping does not bind the exact assertion version")
    if (
        commitment_mapping["target_programme"]["target_assertion_bundle_id"]
        != canonical_assertions["bundle_id"]
    ):
        raise ContractViolation("Commitment mapping assertion bundle does not resolve")
    administrative_fragment_ids = {
        fragment["evidence_id"]
        for document in administrative_evidence["documents"]
        for fragment in document["evidence_fragments"]
    }
    assertion_evidence_ids = set(target_assertion["derivation"]["evidence_ids"])
    if not assertion_evidence_ids <= administrative_fragment_ids:
        raise ContractViolation("Canonical assertion evidence does not resolve")
    relationship_evidence_ids = {
        item["evidence_id"] for item in canonical_assertions["evidence_relationships"]
    }
    if relationship_evidence_ids != assertion_evidence_ids:
        raise ContractViolation("Canonical assertion evidence relationships are incomplete")

    mapping_review_ref = snapshot["commitment_mapping_review"]
    mapping_review_hash = file_sha256(mapping_review_path)
    if mapping_review_hash != mapping_review_ref["sha256"]:
        raise ContractViolation(
            f"{mapping_review_path}: fingerprint mismatch; expected "
            f"{mapping_review_ref['sha256']}, got {mapping_review_hash}"
        )
    if (
        commitment_mapping_review["review_packet_id"]
        != mapping_review_ref["review_packet_id"]
        or commitment_mapping_review["review_packet_version"]
        != mapping_review_ref["review_packet_version"]
        or commitment_mapping_review["lifecycle_state"]
        != mapping_review_ref["lifecycle_state"]
    ):
        raise ContractViolation("Commitment-mapping review packet reference does not resolve")
    review_mapping_ref = commitment_mapping_review["mapping_reference"]
    if (
        review_mapping_ref["mapping_id"] != commitment_mapping["mapping_id"]
        or review_mapping_ref["mapping_version"] != commitment_mapping["mapping_version"]
        or review_mapping_ref["sha256"] != mapping_ref["sha256"]
    ):
        raise ContractViolation("Review packet does not bind the exact mapping version")
    advisory_roles = {
        item["role_id"]: item for item in commitment_mapping_review["ai_advisory_roles"]
    }
    if len(commitment_mapping_review["ai_advisory_roles"]) != 2 or set(advisory_roles) != {
        "ai_methodology_auditor",
        "ai_evidence_authority_auditor",
    }:
        raise ContractViolation("Both AI advisory roles must be configured")
    advisory_runs = commitment_mapping_review["ai_advisory_runs"]
    if any(item["counts_as_human_review"] for item in advisory_runs):
        raise ContractViolation("AI advisory runs cannot count as human review")
    current_runs = [
        item
        for item in advisory_runs
        if item["reviewed_mapping_version"] == commitment_mapping["mapping_version"]
        and item["applicability_state"] == "current"
    ]
    if commitment_mapping_review["lifecycle_state"] == "ready_for_ai_advisory_review":
        if any(item["status"] != "configured_not_run" for item in advisory_roles.values()):
            raise ContractViolation("Current AI advisory roles must be configured but not run")
        if current_runs:
            raise ContractViolation("Corrected mapping cannot retain current-version audit outputs")
    elif commitment_mapping_review["lifecycle_state"] == "ready_for_maintainer_review":
        if any(item["status"] != "completed" for item in advisory_roles.values()):
            raise ContractViolation("Both configured AI advisory roles must be completed")
        if len(current_runs) != 2:
            raise ContractViolation("The maintainer review requires exactly two current AI runs")
        runs_by_role = {item["role_id"]: item for item in current_runs}
        if set(runs_by_role) != set(advisory_roles):
            raise ContractViolation("Each configured AI advisory role must have one current run")
    else:
        raise ContractViolation("Unsupported current commitment-mapping review lifecycle")
    if commitment_mapping_review["maintainer_review"] is not None:
        raise ContractViolation("The maintainer review must follow both AI advisory audits")
    if commitment_mapping_review["independent_human_reviews"]:
        raise ContractViolation("The prepared review packet has no independent human reviews")
    if commitment_mapping_review["independent_final_decision"] is not None:
        raise ContractViolation("The prepared review packet cannot contain an independent final decision")
    if commitment_mapping_review["preparation"]["counts_as_independent_review"]:
        raise ContractViolation("AI-assisted preparation cannot count as independent review")
    review_requirements = commitment_mapping_review["human_review_requirements"]
    if review_requirements["interim_poc_reviewer_role"] != "maintainer_reviewer":
        raise ContractViolation("The local POC pathway must retain one maintainer reviewer")
    if not review_requirements["ai_advisory_required_before_maintainer_review"]:
        raise ContractViolation("Both AI advisory audits must precede maintainer review")
    if set(review_requirements["independent_publication_roles"]) != {
        "methodological_reviewer",
        "evidence_authority_reviewer",
    }:
        raise ContractViolation("Both independent publication-review roles must remain required")
    if not review_requirements["independent_reviewer_separation_required"]:
        raise ContractViolation("Publication-grade independent reviewers must remain separated")
    review_evidence_ids = {
        item["evidence_id"] for item in commitment_mapping_review["evidence_basis"]
    }
    if review_evidence_ids != set(commitment_mapping["mapping"]["evidence_ids"]):
        raise ContractViolation("Review packet evidence differs from the mapping evidence")
    if any(
        set(item["evidence_ids_reviewed"]) != review_evidence_ids
        for item in current_runs
    ):
        raise ContractViolation("Each AI advisory audit must inspect the complete evidence basis")
    required_review_dimensions = {
        "original_formulation",
        "name",
        "territory",
        "beneficiaries",
        "delivery_method",
        "timing",
        "quantity_and_budget",
        "direct_continuity",
        "policy_lineage",
    }
    if {item["dimension"] for item in commitment_mapping_review["findings"]} != required_review_dimensions:
        raise ContractViolation("Commitment-mapping review findings are incomplete")
    if commitment_mapping_review["output_constraints"] != {
        "fulfillment_conclusion": "not_verifiable",
        "publication_eligible": False,
        "implementation_percentage_allowed": False,
    }:
        raise ContractViolation("Review preparation must remain fail-closed")

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
    mapping_evidence_ids = commitment_mapping["mapping"]["evidence_ids"]
    available_mapping_evidence = {
        commitment_mapping["original_commitment"]["evidence_id"], *evidence_ids
    }
    if not set(mapping_evidence_ids).issubset(available_mapping_evidence):
        raise ContractViolation("Commitment mapping references unknown evidence")
    reference_ids = [
        reference["evidence_id"]
        for reference in commitment_mapping["evidence_references"]
    ]
    if len(reference_ids) != len(set(reference_ids)):
        raise ContractViolation("Commitment mapping evidence references must be unique")
    if set(reference_ids) != set(mapping_evidence_ids):
        raise ContractViolation("Commitment mapping evidence list and references differ")
    expected_input_hashes = {
        snapshot["campaign_artifact"]["local_path"]: snapshot["campaign_artifact"]["sha256"],
        snapshot["administrative_evidence"]["local_path"]: snapshot["administrative_evidence"]["sha256"],
        snapshot["canonical_assertions"]["local_path"]: snapshot["canonical_assertions"]["sha256"],
    }
    mapping_input_hashes = {
        item["local_path"]: item["sha256"]
        for item in commitment_mapping["lineage"]["inputs"]
    }
    if mapping_input_hashes != expected_input_hashes:
        raise ContractViolation("Commitment mapping lineage does not bind its exact input versions")
    if (
        administrative_evidence["chain_summary"]["commitment_mapping"]
        != commitment_mapping["mapping"]["candidate_conclusion"]
    ):
        raise ContractViolation("Administrative chain and mapping proposal states differ")
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

    procurement_ref = snapshot["procurement_evidence"]
    if procurement_evidence["bundle_id"] != procurement_ref["bundle_id"]:
        raise ContractViolation("Procurement evidence bundle reference does not resolve")
    if procurement_evidence["bundle_version"] != procurement_ref["bundle_version"]:
        raise ContractViolation("Procurement evidence bundle version reference does not resolve")
    city_acquisition = procurement_evidence["city_dataset_acquisition"]
    if procurement_acquisition_event["source_id"] != city_acquisition["source_id"]:
        raise ContractViolation("Procurement acquisition source reference does not resolve")
    if (
        procurement_acquisition_event["artifact_version_id"]
        != city_acquisition["artifact_version_id"]
    ):
        raise ContractViolation("Procurement artifact version reference does not resolve")
    if procurement_acquisition_event["response"]["record_count"] != city_acquisition[
        "record_count"
    ]:
        raise ContractViolation("Procurement record count differs from its acquisition event")

    procurement_rows = procurement_raw.get("results")
    if (
        procurement_raw.get("total_count") != 8
        or not isinstance(procurement_rows, list)
        or len(procurement_rows) != 8
    ):
        raise ContractViolation("The bounded procurement response must contain eight rows")
    selected_procurement_fields = set(
        procurement_acquisition_event["request"]["selected_fields"]
    )
    if not all(set(row) == selected_procurement_fields for row in procurement_rows):
        raise ContractViolation("Raw procurement rows differ from the selected field contract")
    procurement_rows_by_id: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in procurement_rows:
        procurement_rows_by_id[row["marche_id"]].append(row)
    expected_procurement_row_counts = {"20202012301": 1, "25-119": 4, "25-120": 3}
    actual_procurement_row_counts = {
        market_id: len(items) for market_id, items in procurement_rows_by_id.items()
    }
    if actual_procurement_row_counts != expected_procurement_row_counts:
        raise ContractViolation("Procurement holder-grain row counts changed unexpectedly")
    expected_procurement_amounts = {"20202012301": 45750, "25-119": 81500, "25-120": 76800}
    for market_id, items in procurement_rows_by_id.items():
        amounts = {item["montant"] for item in items}
        if amounts != {expected_procurement_amounts[market_id]}:
            raise ContractViolation(
                f"Procurement amount drift for {market_id}: {sorted(amounts)}"
            )
    row_level_sum = sum(row["montant"] for row in procurement_rows)
    unique_contract_sum = sum(expected_procurement_amounts.values())
    if row_level_sum != 602150 or unique_contract_sum != 204050:
        raise ContractViolation("Procurement duplicate-grain guard values changed")

    procurement_records = procurement_evidence["records"]
    procurement_record_ids = [record["record_id"] for record in procurement_records]
    if len(procurement_record_ids) != len(set(procurement_record_ids)):
        raise ContractViolation("Procurement record identifiers must be unique")
    procurement_evidence_ids = [record["evidence_id"] for record in procurement_records]
    if len(procurement_evidence_ids) != len(set(procurement_evidence_ids)):
        raise ContractViolation("Procurement evidence identifiers must be unique")
    for record in procurement_records:
        if not set(record["source_ids"]).issubset(source_index):
            raise ContractViolation("Procurement evidence references an unknown source")
    award_record = next(
        record for record in procurement_records if record["role"] == "award_notice"
    )
    if award_record["observation_state"] != "post_cutoff_publication_historical_event":
        raise ContractViolation("Post-cutoff award publication must remain explicitly gated")
    if award_record["dates"]["notice_publication"] <= snapshot["observation_cutoff"]:
        raise ContractViolation("Expected the award notice publication to post-date the cut-off")
    if award_record["amount"]["value"] != 158300:
        raise ContractViolation("Published award total must equal the two unique lot values")
    if sum(lot["amount"]["value"] for lot in award_record["lots"]) != 158300:
        raise ContractViolation("Award lot values do not reconcile to the published total")
    if (
        procurement_evidence["chain_summary"]["procurement"]
        != "partial_candidate_services_evidence"
    ):
        raise ContractViolation("Located service procurement must remain a partial chain state")
    if any(
        record["scope"]["relationship_to_programme"]
        != "candidate_relevant_object_not_directly_named"
        for record in procurement_records
    ):
        raise ContractViolation(
            "Procurement records must not silently claim a direct Respire programme relationship"
        )
    if procurement_evidence["chain_summary"]["fulfillment_conclusion"] != "not_verifiable":
        raise ContractViolation("Procurement evidence cannot establish fulfillment")

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
        canonical_assertions,
        commitment_mapping,
        commitment_mapping_review,
        procurement_evidence,
        procurement_acquisition_event,
        procurement_raw,
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
        canonical_assertions,
        commitment_mapping,
        commitment_mapping_review,
        procurement_evidence,
        procurement_acquisition_event,
        _,
    ) = validate_inputs(root)
    current_advisory_runs = [
        item
        for item in commitment_mapping_review["ai_advisory_runs"]
        if item["reviewed_mapping_version"] == commitment_mapping["mapping_version"]
        and item["applicability_state"] == "current"
    ]
    if commitment_mapping_review["lifecycle_state"] == "ready_for_ai_advisory_review":
        mapping_review_progress_limitation = (
            "The cautious commitment correspondence is an AI-assisted proposal. "
            "Two first-cycle advisory audits are retained for the superseded mapping; "
            "the corrected mapping awaits both repeat audits and one interim maintainer decision. "
            "Independent publication review remains pending."
        )
    else:
        mapping_review_progress_limitation = (
            "The cautious commitment correspondence is an AI-assisted proposal with two "
            "completed, non-binding current-version advisory audits awaiting one interim "
            "maintainer decision; independent publication review remains pending."
        )
    source = next(
        item for item in profiles["sources"] if item["source_id"] == "src-city-open-data-schools"
    )
    source_index = {item["source_id"]: item for item in profiles["sources"]}
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
    for record in procurement_evidence["records"]:
        if record["role"] == "study_service_contract":
            artifact_version_id = procurement_evidence["city_dataset_acquisition"][
                "artifact_version_id"
            ]
            source_url = source_index["src-city-procurement-open-data"]["canonical_url"]
        else:
            artifact_version_id = procurement_evidence["boamp_acquisition"][
                "artifact_version_id"
            ]
            notice_id = "25-110034" if record["role"] == "competition_notice" else "26-4348"
            source_url = f"https://www.boamp.fr/pages/avis/?q=idweb:{notice_id}"
        evidence.append(
            {
                "evidence_id": record["evidence_id"],
                "relationship": "supports",
                "artifact_version_id": artifact_version_id,
                "locator": record["source_locators"][0],
                "source_url": source_url,
            }
        )
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
        "contract_version": "1.2.0",
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
                "source-linked delivery states for three school cases. It also documents partial "
                "candidate procurement evidence for study and design services whose source "
                "records do not directly name the programme. The commitment mapping, "
                "attributable works procurement and competent completion chain, public fulfillment conclusion, "
                "observed outcome, and causal impact remain unverified."
            ),
            "fulfillment_conclusion": snapshot["campaign_commitment"]["fulfillment_conclusion"],
            "causal_claim_class": "causal_status_not_verifiable",
        },
        "campaign_commitment": {
            "verification_state": snapshot["campaign_commitment"]["verification_state"],
            "wording": campaign_artifact["evidence_fragment"]["quote"],
            "source_scope": "Clermont-Ferrand municipal campaign",
            "attribution": commitment_mapping["original_commitment"]["attribution"],
            "specificity": commitment_mapping["original_commitment"]["specificity"],
            "scope_limits": commitment_mapping["original_commitment"]["scope_limits"],
            "quantification_state": "unquantified_in_primary_fragment",
            "mapping_state": "review_incomplete",
            "mapping_evidence_state": "candidate_evidence_found",
            "artifact_version_id": campaign_artifact["artifact_version_id"],
            "evidence_id": "evidence-campaign-schoolyards-2020",
        },
        "commitment_mapping": {
            "mapping_id": commitment_mapping["mapping_id"],
            "mapping_version": commitment_mapping["mapping_version"],
            "lifecycle_state": commitment_mapping["lifecycle_state"],
            "method_id": commitment_mapping["method"]["method_id"],
            "method_version": commitment_mapping["method"]["method_version"],
            "proposal_origin": commitment_mapping["method"]["proposal_origin"],
            "review_state": commitment_mapping["review"]["state"],
            "relationship_role": commitment_mapping["mapping"]["relationship_role"],
            "candidate_conclusion": commitment_mapping["mapping"]["candidate_conclusion"],
            "target_programme_id": commitment_mapping["target_programme"]["programme_id"],
            "target_programme_name": commitment_mapping["target_programme"]["name"],
            "component": commitment_mapping["components"][0],
            "scope_comparison": commitment_mapping["mapping"]["scope_comparison"],
            "rationale": commitment_mapping["mapping"]["rationale"],
            "uncertainty": commitment_mapping["uncertainty"],
            "limitations": commitment_mapping["mapping"]["limitations"],
            "fulfillment_conclusion": commitment_mapping["output_constraints"][
                "fulfillment_conclusion"
            ],
            "prohibited_inferences": commitment_mapping["output_constraints"][
                "prohibited_inferences"
            ],
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
            "procurement": procurement_evidence["chain_summary"]["procurement"],
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
            "procurement_records": procurement_evidence["records"],
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
            "supporting_context_sources": [
                {
                    "source_id": item["source_id"],
                    "title": item["title"],
                    "publisher": item["publisher"],
                    "source_class": item["source_class"],
                    "source_url": item["canonical_url"],
                    "authority_state": item["review"]["authority_state"],
                    "rights_state": item["rights"]["state"],
                    "limitations": item["review"]["limitations"],
                }
                for item in profiles["sources"]
                if item["source_id"] == "src-campaign-2020-interview"
            ],
            "administrative_evidence": {
                "bundle_id": administrative_evidence["bundle_id"],
                "bundle_version": administrative_evidence["bundle_version"],
                "local_path": snapshot["administrative_evidence"]["local_path"],
                "content_fingerprint_sha256": snapshot["administrative_evidence"]["sha256"],
                "assembled_at": administrative_evidence["assembled_at"],
                "document_count": len(administrative_evidence["documents"]),
                "raw_bytes_preserved": administrative_evidence["raw_bytes_preserved"],
            },
            "canonical_assertions": {
                "bundle_id": canonical_assertions["bundle_id"],
                "bundle_version": canonical_assertions["bundle_version"],
                "local_path": snapshot["canonical_assertions"]["local_path"],
                "content_fingerprint_sha256": snapshot["canonical_assertions"]["sha256"],
                "assertion_ids": [
                    item["assertion_id"] for item in canonical_assertions["assertions"]
                ],
            },
            "procurement_evidence": {
                "bundle_id": procurement_evidence["bundle_id"],
                "bundle_version": procurement_evidence["bundle_version"],
                "local_path": snapshot["procurement_evidence"]["local_path"],
                "content_fingerprint_sha256": snapshot["procurement_evidence"]["sha256"],
                "assembled_at": procurement_evidence["assembled_at"],
                "record_count": len(procurement_evidence["records"]),
                "city_raw_bytes_preserved": True,
                "boamp_raw_bytes_preserved": procurement_evidence["boamp_acquisition"][
                    "raw_bytes_preserved"
                ],
                "boamp_nonretention_reason": procurement_evidence["boamp_acquisition"][
                    "nonretention_reason"
                ],
            },
            "commitment_mapping": {
                "mapping_id": commitment_mapping["mapping_id"],
                "mapping_version": commitment_mapping["mapping_version"],
                "lifecycle_state": commitment_mapping["lifecycle_state"],
                "local_path": snapshot["commitment_mapping"]["local_path"],
                "content_fingerprint_sha256": snapshot["commitment_mapping"]["sha256"],
                "created_at": commitment_mapping["created_at"],
                "proposal_origin": commitment_mapping["method"]["proposal_origin"],
            },
            "commitment_mapping_review": {
                "review_packet_id": commitment_mapping_review["review_packet_id"],
                "review_packet_version": commitment_mapping_review["review_packet_version"],
                "lifecycle_state": commitment_mapping_review["lifecycle_state"],
                "local_path": snapshot["commitment_mapping_review"]["local_path"],
                "content_fingerprint_sha256": snapshot["commitment_mapping_review"]["sha256"],
                "ai_advisory_roles_configured": len(
                    commitment_mapping_review["ai_advisory_roles"]
                ),
                "ai_advisory_run_count": len(current_advisory_runs),
                "historical_ai_advisory_run_count": len(
                    commitment_mapping_review["ai_advisory_runs"]
                )
                - len(current_advisory_runs),
                "maintainer_review_complete": commitment_mapping_review[
                    "maintainer_review"
                ]
                is not None,
                "independent_review_count": len(
                    commitment_mapping_review["independent_human_reviews"]
                ),
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
                "event_id": "lineage-propose-commitment-mapping-001",
                "event_type": "ai_assisted_mapping_proposal",
                "inputs": commitment_mapping["lineage"]["inputs"],
                "rule_version": commitment_mapping["method"]["method_version"],
                "generator": commitment_mapping["lineage"]["generator"],
                "output": snapshot["commitment_mapping"]["local_path"],
                "output_sha256": snapshot["commitment_mapping"]["sha256"],
                "result": commitment_mapping["lifecycle_state"],
                "deterministic": False,
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
                "event_id": procurement_acquisition_event["event_id"],
                "event_type": "acquisition",
                "input": procurement_acquisition_event["resolved_url"],
                "output": procurement_acquisition_event["raw_artifact"]["local_path"],
                "output_sha256": procurement_acquisition_event["raw_artifact"]["sha256"],
                "result": "accepted_after_contract_validation",
                "deterministic": False,
            },
            {
                "event_id": "lineage-review-procurement-evidence-001",
                "event_type": "evidence_review",
                "inputs": [
                    procurement_evidence["city_dataset_acquisition"]["raw_local_path"],
                    procurement_evidence["boamp_acquisition"]["requested_endpoint"],
                ],
                "rule_version": "iagora.procurement-evidence/0.1.0",
                "output": snapshot["procurement_evidence"]["local_path"],
                "output_sha256": snapshot["procurement_evidence"]["sha256"],
                "result": "partial_candidate_services_evidence",
                "deterministic": False,
            },
            {
                "event_id": "lineage-project-knowledge-passport-001",
                "event_type": "projection",
                "input": snapshot["source_dataset"]["local_path"],
                "input_sha256": snapshot["source_dataset"]["sha256"],
                "rule_version": "iagora.pilot.project-passport/0.5.0",
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
                mapping_review_progress_limitation,
                *procurement_evidence["limitations"],
            ],
            "procurement_findings": procurement_evidence["quality_findings"],
        },
        "conflicts_and_uncertainty": [
            "The primary campaign fragment is unquantified and does not state a delivery date, budget, or number of schoolyards.",
            "The all-neighbourhood scope appears in supporting interview evidence, not in the retained primary fragment.",
            "Pierre-et-Marie-Curie has different reported states for its maternelle and élémentaire units; this is a scope difference, not a resolved contradiction.",
            "The 1.09 million euros reported for 2022 and 1,939,810.63 euros of cumulative mandates before 2023 have different periods and precision; they must not be treated as contradictory or interchangeable.",
            "The located procurement records cover study, design, and user-assistance services but do not directly name the Respire programme; they remain candidate evidence and do not establish attributable schoolyard works or competent completion.",
            "The 2025 design awards were published and issued after the observation cut-off and therefore remain post-cut-off historical evidence.",
            "The Pierre-et-Marie-Curie design lot also covers Alphonse-Daudet and cannot be allocated to one school or linked to the reported 2023 maternal delivery.",
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
            "procurement_evidence": {
                "city_dataset": {
                    "state": source_index["src-city-procurement-open-data"]["rights"]["state"],
                    "license_id": source_index["src-city-procurement-open-data"]["rights"]["license_id"],
                    "redistribution": source_index["src-city-procurement-open-data"]["rights"]["redistribution"],
                    "raw_bytes_preserved": True,
                },
                "boamp": {
                    "state": source_index["src-boamp-schoolyard-regreening-2025"]["rights"]["state"],
                    "redistribution": source_index["src-boamp-schoolyard-regreening-2025"]["rights"]["redistribution"],
                    "raw_bytes_preserved": procurement_evidence["boamp_acquisition"]["raw_bytes_preserved"],
                    "nonretention_reason": procurement_evidence["boamp_acquisition"]["nonretention_reason"],
                },
            },
        },
        "review": {
            "state": "prototype_maintainer_review_only",
            "reviewer_role": "maintainer",
            "methodological_review_complete": False,
            "commitment_mapping_review_state": commitment_mapping["review"]["state"],
            "commitment_mapping_review_packet_state": commitment_mapping_review[
                "lifecycle_state"
            ],
            "interim_maintainer_review_complete": commitment_mapping_review[
                "maintainer_review"
            ]
            is not None,
            "independent_publication_review_complete": False,
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
    evidence_by_id = {
        item["evidence_id"]: item for item in passport["evidence"]
    }

    def milestone_link(evidence_id: str, label: str) -> str:
        item = milestones[evidence_id]
        return (
            f'<a href="{html.escape(item["source_url"], quote=True)}" '
            f'rel="external noreferrer">{html.escape(label)}</a>'
        )

    def evidence_link(evidence_id: str, label: str) -> str:
        item = evidence_by_id[evidence_id]
        return (
            f'<a href="{html.escape(item["source_url"], quote=True)}" '
            f'rel="external noreferrer">{html.escape(label)}</a>'
        )

    mapping_dimension_labels = {
        "territory": "Territoire",
        "action_and_object": "Action et objet",
        "quantity": "Quantité",
        "deadline": "Échéance",
        "geographic_extent": "Étendue géographique",
        "institutional_continuity": "Continuité institutionnelle",
        "temporal_sequence": "Chronologie",
    }
    mapping_result_labels = {
        "compatible": "Compatible, sans preuve suffisante à elle seule",
        "compatible_with_broader_programme": "Compatible avec un programme plus large",
        "indeterminate": "Indéterminé",
        "not_comparable": "Non comparable",
        "pending_additional_evidence": "Preuve complémentaire requise",
    }
    mapping_scope_labels = {
        "territory": (
            "Campagne municipale de Clermont-Ferrand",
            "Politique municipale de la Ville de Clermont-Ferrand",
        ),
        "action_and_object": (
            "Végétalisation de cours d’école",
            "Transformation écologique, plus fraîche, perméable, inclusive et coconçue des cours d’école",
        ),
        "quantity": (
            "Aucun nombre, proportion ou dénominateur indiqué",
            "Des objectifs ultérieurs existent, mais ne deviennent pas des objectifs de campagne",
        ),
        "deadline": (
            "Aucune échéance indiquée",
            "Le projet éducatif adopté couvre 2022–2025",
        ),
        "geographic_extent": (
            "Plusieurs cours, sans couverture de tous les quartiers ni de toute la ville dans le fragment primaire",
            "Programme municipal portant sur plusieurs sites scolaires",
        ),
        "institutional_continuity": (
            "Proposition attribuée à Olivier Bianchi et Naturellement Clermont",
            "Politique adoptée par la Ville, dans un cadre éducatif documenté depuis 2015",
        ),
        "temporal_sequence": (
            "Page de campagne capturée en 2019 avant l’élection municipale de 2020",
            "Actions et politique publique postérieures",
        ),
    }
    mapping_rows = "".join(
        "<tr>"
        f'<th scope="row">{html.escape(mapping_dimension_labels[item["dimension"]])}</th>'
        f'<td>{html.escape(mapping_scope_labels[item["dimension"]][0])}</td>'
        f'<td>{html.escape(mapping_scope_labels[item["dimension"]][1])}</td>'
        f'<td>{html.escape(mapping_result_labels[item["comparison_result"]])}</td>'
        "</tr>"
        for item in passport["commitment_mapping"]["scope_comparison"]
    )

    chain_rows = [
        (
            "Lien entre la promesse et le programme",
            "Correspondance candidate ; aucun document ne prouve encore une mise en œuvre directe",
            milestone_link("evidence-pev-respire-definition-2023", "Définition de Respire")
            + " ; "
            + milestone_link("evidence-pev-policy-history-2023", "PEV antérieurs depuis 2015"),
        ),
        (
            "Décision de la mairie",
            "Le projet éducatif contenant l’action a été adopté",
            milestone_link("evidence-pev-adoption-2023", "Délibération du 5 mai 2023"),
        ),
        (
            "Sommes que la mairie pouvait utiliser",
            "Montants autorisés pour tout le programme ; ce ne sont pas des dépenses",
            milestone_link(
                "evidence-apcp-respire-total-2022",
                "Autorisation totale du programme : 4,07 M€",
            )
            + " ; "
            + milestone_link(
                "evidence-budget-2023-cp-opened",
                "Somme prévue pour 2023 : 810 000 €",
            ),
        ),
        (
            "Dépenses enregistrées",
            "Montants connus pour tout le programme, sans détail par école",
            milestone_link("evidence-account-2022-respire-expenditure", "1,09 M€ en 2022")
            + " ; "
            + milestone_link(
                "evidence-budget-2023-prior-mandates",
                "1 939 810,63 € d’ordres de paiement enregistrés avant 2023",
            ),
        ),
        (
            "Contrats publics retrouvés",
            "Ils concernent des études et de la conception. Ils ne prouvent ni les travaux, ni leur paiement, ni leur fin",
            evidence_link("evidence-procurement-city-study-2020", "Étude notifiée en 2020")
            + " ; "
            + evidence_link("evidence-procurement-boamp-competition-25-110034", "Consultation 2025")
            + " ; "
            + evidence_link("evidence-procurement-boamp-award-26-4348", "Attributions publiées en 2026"),
        ),
        (
            "Fin des travaux",
            "La mairie signale des livraisons sur certains sites ; les documents officiels de fin manquent",
            milestone_link("evidence-transition-nestor-reported-use", "Nestor-Perret")
            + " ; "
            + milestone_link("evidence-pierre-curie-reported-delivery", "Curie maternelle")
            + " ; "
            + milestone_link("evidence-jean-zay-forecast-cost", "Jean-Zay : prévision"),
        ),
        (
            "Résultats et effets sur la ville",
            "Nous ne le savons pas encore",
            "Aucune mesure avant-après ni méthode permettant d’attribuer un effet n’a été validée",
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
              <p>Les lignes par unité scolaire restent distinctes et ne constituent pas une conclusion à l’échelle du programme.</p>
              <p><strong>Documents reliés à cette école :</strong> {len(case['administrative_evidence_ids'])}. Leur présence ne prouve pas à elle seule la fin officielle des travaux ni leurs effets.</p>
              <div class="table-wrap" tabindex="0" aria-label="Tableau défilable des données de {html.escape(case['school_name'])}">
                <table>
                  <caption>Données ouvertes publiées par la mairie pour {html.escape(case['school_name'])}</caption>
                  <thead><tr><th scope="col">Unité</th><th scope="col">Identifiant national de l’école (UAI)</th><th scope="col">Année</th><th scope="col">État déclaré</th><th scope="col">Surface rendue perméable (m²)</th><th scope="col">Arbres plantés</th></tr></thead>
                  <tbody>{''.join(rows)}</tbody>
                </table>
              </div>
            </section>
            """
        )

    blocker_labels = {
        "commitment_mapping_and_methodological_review_incomplete": "La correspondance entre la promesse et le programme attend le contrôle humain du POC, puis deux revues indépendantes avant publication.",
        "campaign_artifact_raw_bytes_not_preserved_for_rights": "La page de campagne complète n’est pas conservée dans le dépôt en raison des droits de reproduction.",
        "methodological_review_incomplete": "La revue méthodologique globale du POC reste incomplète.",
        "attributable_works_procurement_and_competent_completion_evidence_missing": "Nous n’avons pas encore trouvé les contrats de travaux reliés aux écoles étudiées ni les documents officiels confirmant leur fin.",
        "outcome_and_impact_evidence_missing": "Les preuves de résultats et d’impact restent absentes.",
        "production_privacy_security_and_retention_review_incomplete": "Les revues de confidentialité, de sécurité et de conservation nécessaires à la production restent incomplètes.",
    }
    limit_labels = {
        "The primary campaign fragment is unquantified and does not state a delivery date, budget, or number of schoolyards.": "Le fragment primaire n’est pas chiffré et ne précise ni échéance, ni budget, ni nombre de cours d’école.",
        "The all-neighbourhood scope appears in supporting interview evidence, not in the retained primary fragment.": "La portée « tous les quartiers » apparaît dans un entretien de soutien, pas dans le fragment primaire retenu.",
        "Pierre-et-Marie-Curie has different reported states for its maternelle and élémentaire units; this is a scope difference, not a resolved contradiction.": "Pierre-et-Marie-Curie présente des états déclarés différents pour la maternelle et l’élémentaire ; il s’agit d’une différence de périmètre, pas d’une contradiction résolue.",
        "The 1.09 million euros reported for 2022 and 1,939,810.63 euros of cumulative mandates before 2023 have different periods and precision; they must not be treated as contradictory or interchangeable.": "Les 1,09 M€ déclarés pour 2022 et les 1 939 810,63 € d’ordres de paiement enregistrés avant 2023 ne couvrent pas exactement la même période. Nous ne les additionnons pas et ne les remplaçons pas l’un par l’autre.",
        "The located procurement records cover study, design, and user-assistance services but do not directly name the Respire programme; they remain candidate evidence and do not establish attributable schoolyard works or competent completion.": "Les contrats retrouvés portent sur des études, de la conception et de l’accompagnement des usagers. Ils ne nomment pas directement le programme Respire et ne prouvent ni les travaux dans les écoles ni leur fin officielle.",
        "The 2025 design awards were published and issued after the observation cut-off and therefore remain post-cut-off historical evidence.": "Les attributions de conception de 2025 ont été publiées et contractualisées après la date d’observation ; elles restent donc des preuves historiques postérieures à cette date.",
        "The Pierre-et-Marie-Curie design lot also covers Alphonse-Daudet and cannot be allocated to one school or linked to the reported 2023 maternal delivery.": "Le lot de conception mentionnant Pierre-et-Marie-Curie couvre aussi Alphonse-Daudet ; son montant ne peut être attribué à une seule école ni relié à la livraison maternelle déclarée en 2023.",
        "No reviewed baseline, outcome indicator, counterfactual, or contribution analysis is available.": "Nous n’avons pas de mesure de départ validée, ni de mesure des résultats, ni de méthode permettant de savoir si les changements viennent réellement du programme.",
    }
    blockers = "".join(
        f"<li>{html.escape(blocker_labels.get(item, item))}</li>"
        for item in passport["publication"]["blockers"]
    )
    limits = "".join(
        f"<li>{html.escape(limit_labels.get(item, item))}</li>"
        for item in passport["conflicts_and_uncertainty"]
    )
    source_url = html.escape(passport["provenance"]["source_url"], quote=True)
    return f"""<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="Dossier détaillé et traçable du programme Respire à la récré dans le prototype local IAgora.">
  <title>IAgora — Dossier Respire à la récré</title>
  <style>{PAGE_STYLES}</style>
</head>
<body>
{render_site_header("detail", "../../")}
<main id="contenu" class="report-shell">
  <nav class="breadcrumbs no-print" aria-label="Fil d’Ariane"><a href="../../index.html">Clermont-Ferrand</a> / <a href="../../education/index.html">Éducation</a> / Respire à la récré</nav>
  <section class="content-card" aria-labelledby="titre-dossier">
    <p class="eyebrow">Dossier détaillé · Méthode, périmètres et preuves</p>
    <h1 id="titre-dossier" class="page-title">Respire à la récré</h1>
    <p class="lede">Ce dossier explique ce qui a été promis, ce que la mairie indique avoir fait, l’argent retrouvé et ce qui reste impossible à vérifier.</p>
    <div class="actions no-print"><a class="button button--secondary" href="../../education/index.html">Retour à l’éducation</a><button class="button" type="button" onclick="window.print()">Imprimer le dossier</button></div>
  </section>
  <div class="banner" role="status">
    <strong>Prototype local — publication bloquée.</strong>
    Ce dossier est encore en vérification. Il ne permet pas encore de dire que toute la promesse a été tenue ni de mesurer ses effets sur la ville.
  </div>
  <section aria-labelledby="synthese">
    <h2 id="synthese">L’essentiel en six réponses</h2>
    <p>Une action réalisée dans une école ou une dépense enregistrée ne suffit pas à prouver que toute la promesse est tenue.</p>
    {render_multidimensional_summary(passport)}
  </section>
  <section aria-labelledby="conclusion">
    <h2 id="conclusion">La promesse a-t-elle été tenue ?</h2>
    <p><strong>Nous n’avons pas assez de preuves pour répondre.</strong></p>
    <p>Le texte de campagne retrouvé ne donne ni nombre d’écoles, ni date de fin, ni budget. La mairie publie des informations sur six unités scolaires étudiées ici, mais ce petit groupe ne représente pas toute la ville. Le lien avec le programme « Respire à la récré » doit être contrôlé par le responsable du POC, puis revu par deux personnes indépendantes avant toute publication.</p>
  </section>
  <section aria-labelledby="filiation">
    <div class="theme-card__top"><h2 id="filiation">Le programme vient-il de la promesse ?</h2><span class="tag tag--pending">Lien non vérifié</span></div>
    <p>La délibération indique que la politique éducative municipale existait dès 2015 et a connu une deuxième version en 2018. Cela ne suffit pas à classer « Respire à la récré » comme une simple continuation, une extension ou une initiative nouvelle, ni à prouver qu’il vient directement de la promesse.</p>
    {render_policy_timeline(passport)}
  </section>
  <section aria-labelledby="engagement">
    <h2 id="engagement">Qu’avait promis le candidat ?</h2>
    <p>La page de campagne archivée contient cette phrase : <q>{html.escape(passport['campaign_commitment']['wording'])}</q>.</p>
    <p>La capture est <strong>authentifiée avec limites</strong> : elle confirme que cette phrase figurait sur une page de campagne, mais elle ne conserve pas tout le contenu qui a pu exister autour de cette proposition.</p>
    <p><a href="{html.escape(passport['provenance']['campaign_artifact']['archive_url'], quote=True)}" rel="external noreferrer">Consulter la capture archivée</a>. Dans le passage retrouvé, le candidat ne dit pas combien d’écoles seront concernées, quand les travaux finiront, combien ils coûteront ni comment ils seront financés et organisés.</p>
  </section>
  <section aria-labelledby="correspondance">
    <h2 id="correspondance">Pourquoi relions-nous cette promesse à « Respire à la récré » ?</h2>
    <p>IAgora conserve un seul composant essentiel : <strong>végétaliser des cours d’école</strong>. Ajouter une quantité, une échéance, une couverture de tous les quartiers ou les objectifs plus détaillés du programme réécrirait la promesse d’origine.</p>
    <p>La proposition de correspondance s’appuie sur le même territoire municipal, un objet compatible et le {milestone_link("evidence-pev-respire-definition-2023", "projet éducatif adopté")}. Le {milestone_link("evidence-pev-policy-history-2023", "même document rappelle aussi des PEV en 2015 et 2018")}. Le programme est plus large que la formulation de campagne et aucune pièce conservée n’établit encore directement leur continuité.</p>
    <p><strong>Qui a vérifié ce lien ?</strong> Pour le moment, il s’agit d’une proposition assistée par intelligence artificielle. Deux contrôles IA consultatifs sont prévus, puis le responsable du POC devra vérifier lui-même les avis et les sources. Avant toute publication, deux autres personnes devront encore examiner séparément la méthode et la qualité des preuves. Cette proposition ne prouve pas que la promesse a été réalisée.</p>
    <div class="table-wrap" tabindex="0" aria-label="Tableau défilable comparant la promesse et le programme municipal">
      <table>
        <caption>Comparaison explicite des périmètres</caption>
        <thead><tr><th scope="col">Dimension</th><th scope="col">Promesse primaire</th><th scope="col">Programme municipal</th><th scope="col">Lecture proposée</th></tr></thead>
        <tbody>{mapping_rows}</tbody>
      </table>
    </div>
    <p><strong>Conséquence :</strong> la correspondance reste proposée et le respect de la promesse demeure <strong>non vérifiable</strong>.</p>
  </section>
  <section aria-labelledby="chaine">
    <h2 id="chaine">Quelles décisions et quels montants avons-nous retrouvés ?</h2>
    <p>Les montants ne veulent pas tous dire la même chose. Une somme autorisée n’est pas forcément dépensée. Une dépense pour tout le programme ne donne pas le coût de chaque école. Un coût annoncé ne prouve pas que la facture a été payée.</p>
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
    <h2 id="source">Sources et fichier de vérification</h2>
    <p><a href="{source_url}" rel="external noreferrer">Jeu de données de la Ville de Clermont-Ferrand</a>, Licence Ouverte 2.0.</p>
    <p>Les dix PDF administratifs sont enregistrés sous forme de métadonnées, empreintes et citations précises ; leurs octets ne sont pas redistribués avant la revue des droits et de la vie privée.</p>
    <p>La réponse bornée du jeu de marchés de la Ville est conservée sous Licence Ouverte 2.0. Pour BOAMP, seuls les identifiants, métadonnées minimales et l’empreinte de la réponse sont conservés tant que la base de réutilisation n’est pas qualifiée.</p>
    <p>Le fichier <code>passport.json</code> contient les mêmes informations dans un format lisible par une machine.</p>
  </section>
</main>
{render_footer()}
</body>
</html>
"""


def build(output_dir: Path, root: Path = ROOT) -> tuple[Path, Path]:
    passport = build_passport(root)
    output_dir.mkdir(parents=True, exist_ok=True)
    passport_path = output_dir / "passport.json"
    dashboard_path = output_dir / "index.html"
    education_path = output_dir / "education" / "index.html"
    report_path = output_dir / "programmes" / "respire-a-la-recre" / "index.html"
    education_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    passport_path.write_text(
        json.dumps(passport, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    dashboard_path.write_text(render_dashboard_html(passport), encoding="utf-8")
    education_path.write_text(render_education_html(passport), encoding="utf-8")
    report_path.write_text(render_html(passport), encoding="utf-8")
    return passport_path, dashboard_path
