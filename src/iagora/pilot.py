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


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()


def validate_inputs(root: Path = ROOT) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    profiles_path = root / SOURCE_PROFILES.relative_to(ROOT)
    snapshot_path = root / SNAPSHOT.relative_to(ROOT)
    profiles = validate_files(profiles_path, root / "contracts/v1/source-profiles.schema.json")
    snapshot = validate_files(snapshot_path, root / "contracts/v1/pilot-snapshot.schema.json")
    dataset_path = root / snapshot["source_dataset"]["local_path"]
    dataset = load_json(dataset_path)

    actual_hash = file_sha256(dataset_path)
    expected_hash = snapshot["source_dataset"]["sha256"]
    if actual_hash != expected_hash:
        raise ContractViolation(
            f"{dataset_path}: fingerprint mismatch; expected {expected_hash}, got {actual_hash}"
        )

    source_index = {source["source_id"]: source for source in profiles["sources"]}
    selected_source = source_index.get(snapshot["source_dataset"]["source_id"])
    if not selected_source or selected_source["status"] != "approved_prototype":
        raise ContractViolation("Pilot dataset source is not approved for bounded prototype use")

    rows = dataset.get("records")
    if not isinstance(rows, list) or len(rows) != 6:
        raise ContractViolation("The bounded source snapshot must contain exactly six school-unit rows")
    if len({row.get("uai") for row in rows}) != len(rows):
        raise ContractViolation("Each school-unit record must have a unique UAI")

    expected_schools = {case["school_name"] for case in snapshot["case_studies"]}
    actual_schools = {row.get("school_name") for row in rows}
    if actual_schools != expected_schools:
        raise ContractViolation(
            f"Bounded school set differs: expected {sorted(expected_schools)}, got {sorted(actual_schools)}"
        )
    return profiles, snapshot, dataset


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
    profiles, snapshot, dataset = validate_inputs(root)
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
    evidence = []
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
                "Prototype local montrant comment relier une promesse encore non authentifiée "
                "à des états scolaires rapportés, sans conclure à sa réalisation ni à son impact."
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
                "The available bounded evidence can demonstrate source-linked delivery states for "
                "three school cases, but it cannot yet verify the original campaign commitment, a "
                "public fulfillment conclusion, an observed outcome, or causal impact."
            ),
            "fulfillment_conclusion": snapshot["campaign_commitment"]["fulfillment_conclusion"],
            "causal_claim_class": "causal_status_not_verifiable",
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
        },
        "lineage": [
            {
                "event_id": "lineage-normalize-open-data-subset-001",
                "event_type": "normalization",
                "input": snapshot["source_dataset"]["local_path"],
                "input_sha256": snapshot["source_dataset"]["sha256"],
                "rule_version": "iagora.pilot.transform/0.1.0",
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
                "Normalized subset is not preserved raw HTTP evidence.",
                "Source values have not been corroborated with competent completion records.",
                "Dataset acquisition occurred after the historical observation cut-off.",
            ],
        },
        "conflicts_and_uncertainty": [
            "The original 2020 campaign artifact remains missing.",
            "Pierre-et-Marie-Curie has different reported states for its maternelle and élémentaire units; this is a scope difference, not a resolved contradiction.",
            "No reviewed baseline, outcome indicator, counterfactual, or contribution analysis is available.",
        ],
        "rights": {
            "license_id": dataset["license_id"],
            "attribution": dataset["publisher"],
            "source_rights_apply": True,
            "retention_class": source["retention"]["class"],
            "production_review_required": True,
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
  <section aria-labelledby="conclusion">
    <h2 id="conclusion">Ce que l’on peut conclure</h2>
    <p>La promesse de campagne reste <strong>non vérifiable</strong>, car son document primaire de 2020 n’a pas encore été authentifié. Les lignes ci-dessous sont des états déclarés par le jeu de données municipal, acquis après la date d’observation du 31 décembre 2025.</p>
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
