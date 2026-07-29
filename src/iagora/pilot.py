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
]:
    profiles_path = root / SOURCE_PROFILES.relative_to(ROOT)
    snapshot_path = root / SNAPSHOT.relative_to(ROOT)
    profiles = validate_files(profiles_path, root / "contracts/v1/source-profiles.schema.json")
    snapshot = validate_files(snapshot_path, root / "contracts/v1/pilot-snapshot.schema.json")
    campaign_path = root / snapshot["campaign_artifact"]["local_path"]
    campaign_artifact = validate_files(
        campaign_path, root / "contracts/v1/campaign-artifact.schema.json"
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
    return profiles, snapshot, dataset, campaign_artifact, acquisition_event, raw_dataset


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
    profiles, snapshot, dataset, campaign_artifact, acquisition_event, _ = validate_inputs(root)
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
                "limites à des états scolaires rapportés, sans conclure à sa réalisation ni à "
                "son impact."
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
                "and demonstrates source-linked delivery states for three school cases, but the "
                "commitment-to-programme mapping, public fulfillment conclusion, observed outcome, "
                "and causal impact remain unverified."
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
                "event_id": "lineage-project-knowledge-passport-001",
                "event_type": "projection",
                "input": snapshot["source_dataset"]["local_path"],
                "input_sha256": snapshot["source_dataset"]["sha256"],
                "rule_version": "iagora.pilot.project-passport/0.2.0",
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
                "Executed expenditure conclusion",
                "Outcome or causal-impact conclusion",
                "Generalization beyond the three selected cases",
            ],
            "fitness": "fit_for_local_prototype_only",
            "known_limitations": [
                "The exact bounded open-data response is preserved, but broader source history is not.",
                "Campaign HTML is fingerprinted but not retained because redistribution is blocked.",
                "Source values have not been corroborated with competent completion records.",
                "Dataset acquisition occurred after the historical observation cut-off.",
            ],
        },
        "conflicts_and_uncertainty": [
            "The primary campaign fragment is unquantified and does not state a delivery date, budget, or number of schoolyards.",
            "The all-neighbourhood scope appears in supporting interview evidence, not in the retained primary fragment.",
            "Pierre-et-Marie-Curie has different reported states for its maternelle and élémentaire units; this is a scope difference, not a resolved contradiction.",
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
    <p>Le document primaire est <strong>authentifié avec limites</strong>. Le respect de la promesse reste néanmoins <strong>non vérifiable</strong>, car le rapprochement méthodologique et la chaîne administrative ne sont pas encore validés. Les lignes ci-dessous sont des états déclarés par le jeu de données municipal, acquis après la date d’observation du 31 décembre 2025.</p>
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
