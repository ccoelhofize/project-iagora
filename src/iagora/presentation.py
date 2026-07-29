# SPDX-License-Identifier: EUPL-1.2

"""Accessible, static product projections for the bounded local pilot."""

from __future__ import annotations

import html
from decimal import Decimal
from typing import Any


PAGE_STYLES = """
:root {
  color-scheme: light;
  --ink: #17211b;
  --muted: #59675f;
  --paper: #f4f2eb;
  --surface: #fffef9;
  --line: #ced5cf;
  --forest: #123c31;
  --forest-soft: #dfece5;
  --lime: #dce98a;
  --amber: #f1c27d;
  --amber-soft: #fff2dc;
  --terracotta: #b85836;
  --slate: #486158;
  --shadow: 0 1.1rem 3rem rgba(18, 60, 49, .08);
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  line-height: 1.55;
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body { margin: 0; color: var(--ink); background: var(--paper); }
a { color: var(--forest); text-decoration-thickness: .11em; text-underline-offset: .18em; }
a:hover { text-decoration-thickness: .18em; }
button { font: inherit; }
:focus-visible { outline: .2rem solid var(--terracotta); outline-offset: .2rem; }
.skip-link { position: fixed; left: 1rem; top: -5rem; z-index: 10; background: var(--surface); padding: .7rem 1rem; }
.skip-link:focus { top: 1rem; }
.site-header { background: var(--surface); border-bottom: 1px solid var(--line); }
.site-header__inner { max-width: 74rem; min-height: 4.6rem; margin: auto; padding: .75rem 1.25rem; display: flex; align-items: center; gap: 1.5rem; }
.brand { display: inline-flex; align-items: center; gap: .65rem; color: var(--ink); font-size: 1.05rem; font-weight: 850; text-decoration: none; letter-spacing: -.02em; }
.brand__mark { width: 2rem; height: 2rem; display: grid; place-items: center; border-radius: 50%; color: var(--surface); background: var(--forest); font-size: .76rem; letter-spacing: -.04em; }
.site-nav { margin-left: auto; display: flex; align-items: center; gap: 1.1rem; }
.site-nav a { color: var(--muted); font-size: .92rem; font-weight: 700; text-decoration: none; }
.site-nav a[aria-current="page"] { color: var(--ink); text-decoration: underline; text-decoration-color: var(--lime); text-decoration-thickness: .28rem; text-underline-offset: .35rem; }
.local-badge, .eyebrow, .tag { display: inline-flex; align-items: center; gap: .35rem; border-radius: 999px; font-weight: 800; letter-spacing: .03em; }
.local-badge { padding: .38rem .68rem; color: var(--forest); background: var(--forest-soft); font-size: .72rem; text-transform: uppercase; white-space: nowrap; }
.page { max-width: 74rem; margin: auto; padding: 2.2rem 1.25rem 5rem; }
.hero { display: grid; grid-template-columns: minmax(0, 1.45fr) minmax(15rem, .55fr); gap: 2rem; align-items: end; padding: 2.4rem 0 2.1rem; }
.eyebrow { margin: 0 0 .85rem; color: var(--forest); font-size: .76rem; text-transform: uppercase; }
h1, h2, h3 { line-height: 1.08; letter-spacing: -.035em; }
h1 { max-width: 15ch; margin: 0; font-size: clamp(2.6rem, 7vw, 5.7rem); }
h2 { margin: 0; font-size: clamp(1.55rem, 3vw, 2.4rem); }
h3 { margin: 0; font-size: 1.22rem; }
.lede { max-width: 42rem; margin: 1.15rem 0 0; color: var(--muted); font-size: 1.12rem; }
.hero-note { border-left: .32rem solid var(--lime); padding: .2rem 0 .2rem 1rem; color: var(--muted); }
.hero-note strong { display: block; color: var(--ink); }
.section-heading { display: flex; justify-content: space-between; align-items: end; gap: 1rem; margin: 3.1rem 0 1.1rem; }
.section-heading p { max-width: 39rem; margin: 0; color: var(--muted); }
.panel, .theme-card, .kpi, section.content-card { background: var(--surface); border: 1px solid var(--line); border-radius: 1rem; box-shadow: var(--shadow); }
.panel { padding: clamp(1.2rem, 3vw, 2rem); }
.macro-grid { display: grid; grid-template-columns: minmax(0, 1.65fr) minmax(14rem, .55fr); gap: 1rem; }
.macro-figure { margin: 0; }
.macro-plot { min-height: 19rem; margin-top: 1.5rem; padding: 1.2rem; display: grid; align-content: center; gap: 1.35rem; border-radius: .8rem; border: 1px solid var(--line); background-color: #f7f8f4; background-image: linear-gradient(to right, rgba(18, 60, 49, .08) 1px, transparent 1px), linear-gradient(to bottom, rgba(18, 60, 49, .08) 1px, transparent 1px); background-size: 20% 100%, 100% 25%; }
.pending-series { display: grid; grid-template-columns: 6.8rem 1fr; align-items: center; gap: 1rem; color: var(--muted); font-size: .82rem; font-weight: 750; }
.pending-series__line { height: 0; border-top: .16rem dashed var(--slate); opacity: .55; }
.pending-series:nth-child(2) .pending-series__line { border-color: var(--terracotta); }
.pending-series:nth-child(3) .pending-series__line { border-color: #8c7628; }
.pending-series:nth-child(4) .pending-series__line { border-color: #546879; }
figcaption { margin-top: 1rem; color: var(--muted); font-size: .9rem; }
.coverage-panel { color: var(--surface); background: var(--forest); border-color: var(--forest); }
.coverage-panel p { color: #d6e3dc; }
.coverage-number { display: block; margin: 1rem 0 .2rem; color: var(--lime); font-size: 4.3rem; font-weight: 900; line-height: 1; letter-spacing: -.07em; }
.theme-grid, .kpi-grid, .summary-grid { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 1rem; }
.theme-card { min-height: 15rem; padding: 1.35rem; display: flex; flex-direction: column; color: var(--ink); text-decoration: none; }
.theme-card--active:hover { transform: translateY(-.18rem); border-color: var(--forest); }
.theme-card--active { transition: transform .16s ease, border-color .16s ease; }
.theme-card--muted { box-shadow: none; background: rgba(255, 254, 249, .62); }
.theme-card__top { display: flex; justify-content: space-between; gap: .7rem; align-items: start; }
.tag { padding: .28rem .55rem; color: var(--forest); background: var(--forest-soft); font-size: .67rem; text-transform: uppercase; }
.tag--pending { color: #6f4613; background: var(--amber-soft); }
.theme-card__metrics { display: grid; grid-template-columns: repeat(2, 1fr); gap: .7rem; margin-top: auto; padding-top: 1.25rem; }
.mini-metric strong { display: block; font-size: 1.65rem; line-height: 1; }
.mini-metric span { display: block; margin-top: .35rem; color: var(--muted); font-size: .76rem; }
.theme-card__cta { margin-top: auto; padding-top: 1rem; font-weight: 850; }
.method-strip { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; }
.method-step { padding: 1.2rem 0; border-top: .24rem solid var(--forest); }
.method-step span { color: var(--terracotta); font-weight: 900; }
.method-step p { margin-bottom: 0; color: var(--muted); }
.breadcrumbs { margin: .4rem 0 1.8rem; color: var(--muted); font-size: .88rem; }
.breadcrumbs a { color: inherit; }
.page-title { max-width: 22ch; font-size: clamp(2.4rem, 6vw, 4.9rem); }
.actions { display: flex; gap: .7rem; flex-wrap: wrap; }
.button { display: inline-flex; align-items: center; justify-content: center; min-height: 2.8rem; padding: .65rem 1rem; border: 1px solid var(--forest); border-radius: 999px; color: var(--surface); background: var(--forest); font-weight: 800; text-decoration: none; cursor: pointer; }
.button--secondary { color: var(--forest); background: transparent; }
.notice { margin: 1rem 0; padding: 1rem 1.1rem; border-left: .32rem solid var(--terracotta); background: var(--amber-soft); }
.notice strong { display: block; }
.kpi { padding: 1.15rem; }
.kpi__value { display: block; font-size: clamp(2rem, 5vw, 3.5rem); font-weight: 900; line-height: 1; letter-spacing: -.06em; }
.kpi__label { display: block; margin-top: .65rem; color: var(--muted); font-size: .88rem; }
.kpi--primary { color: var(--surface); background: var(--forest); border-color: var(--forest); }
.kpi--primary .kpi__label { color: #d6e3dc; }
.two-column { display: grid; grid-template-columns: minmax(0, 1.2fr) minmax(17rem, .8fr); gap: 1rem; }
.status-bar { height: 2rem; display: flex; overflow: hidden; margin: 1.4rem 0 1.1rem; border-radius: 999px; background: #e6e9e5; }
.status-bar span { min-width: 1px; }
.status-complete { background: var(--forest); }
.status-progress { background: var(--amber); }
.status-incomplete { background: var(--terracotta); }
.legend { display: grid; gap: .65rem; margin: 0; padding: 0; list-style: none; }
.legend li { display: grid; grid-template-columns: .8rem 1fr auto; gap: .65rem; align-items: center; }
.legend__swatch { width: .7rem; height: .7rem; border-radius: 50%; }
.legend small { color: var(--muted); }
.timeline { position: relative; margin: 1.7rem 0 0; padding: 0; list-style: none; }
.timeline::before { content: ""; position: absolute; left: .48rem; top: .4rem; bottom: .6rem; border-left: .12rem dashed var(--slate); }
.timeline li { position: relative; padding: 0 0 1.4rem 2rem; }
.timeline li::before { content: ""; position: absolute; left: 0; top: .3rem; width: .82rem; height: .82rem; border: .18rem solid var(--surface); border-radius: 50%; background: var(--forest); box-shadow: 0 0 0 .1rem var(--forest); }
.timeline time { color: var(--terracotta); font-size: .78rem; font-weight: 900; letter-spacing: .06em; }
.timeline p { margin: .25rem 0 0; color: var(--muted); }
.finance-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: .8rem; }
.finance-item { padding: 1rem; border: 1px solid var(--line); border-radius: .75rem; }
.finance-item strong { display: block; font-size: 1.45rem; }
.finance-item span { color: var(--muted); font-size: .82rem; }
.school-list { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: .8rem; }
.school-card { padding: 1rem; border: 1px solid var(--line); border-radius: .8rem; }
.school-card p { margin-bottom: 0; color: var(--muted); font-size: .88rem; }
.summary-grid { grid-template-columns: repeat(3, minmax(0, 1fr)); margin: 1.5rem 0; }
.summary-item { padding: 1rem; border: 1px solid var(--line); border-radius: .8rem; }
.summary-item strong { display: block; margin-top: .3rem; font-size: 1.08rem; }
.summary-item span { color: var(--muted); font-size: .76rem; font-weight: 800; letter-spacing: .04em; text-transform: uppercase; }
.report-shell { max-width: 68rem; margin: auto; padding: 1.4rem 1rem 4rem; }
.report-shell > section, .report-shell > .content-card { background: var(--surface); margin-top: 1.2rem; padding: 1.25rem; border: 1px solid var(--line); border-radius: .75rem; }
.banner { border: .18rem solid #6c4514; border-radius: .55rem; background: #fff4dc; padding: 1rem; }
table { width: 100%; border-collapse: collapse; }
caption { text-align: left; font-weight: 800; padding-bottom: .5rem; }
th, td { padding: .65rem; border: 1px solid #9eaaa2; text-align: left; vertical-align: top; }
.table-wrap { overflow-x: auto; }
.site-footer { border-top: 1px solid var(--line); background: var(--surface); }
.site-footer__inner { max-width: 74rem; margin: auto; padding: 1.5rem 1.25rem; display: flex; justify-content: space-between; gap: 1rem; color: var(--muted); font-size: .82rem; }
@media (max-width: 900px) {
  .theme-grid, .kpi-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .hero, .macro-grid, .two-column { grid-template-columns: 1fr; }
  .summary-grid, .school-list { grid-template-columns: 1fr; }
}
@media (max-width: 620px) {
  .site-header__inner { align-items: flex-start; flex-wrap: wrap; }
  .site-nav { order: 3; width: 100%; margin: 0; overflow-x: auto; padding-bottom: .2rem; }
  .local-badge { margin-left: auto; }
  .page { padding-top: 1rem; }
  .hero { padding-top: 1.5rem; }
  .theme-grid, .kpi-grid, .finance-grid, .method-strip { grid-template-columns: 1fr; }
  .section-heading { align-items: start; flex-direction: column; }
  .site-footer__inner { flex-direction: column; }
}
@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  .theme-card--active { transition: none; }
}
@media print {
  :root { --paper: #fff; --surface: #fff; --shadow: none; }
  .no-print, .site-header, .site-footer, .actions { display: none !important; }
  body { background: #fff; font-size: 10.5pt; }
  .page, .report-shell { max-width: none; padding: 0; }
  .hero { display: block; padding: 0 0 1rem; }
  h1 { font-size: 28pt; }
  h2 { font-size: 18pt; }
  .panel, .theme-card, .kpi, .report-shell > section, .report-shell > .content-card { break-inside: avoid; box-shadow: none; }
  .table-wrap { overflow: visible; }
  a[href^="http"]::after { content: " (" attr(href) ")"; font-size: 8pt; overflow-wrap: anywhere; }
}
"""


STATUS_LABELS = {
    "reported_complete": "Achèvement déclaré",
    "reported_in_progress": "En cours selon la source",
    "reported_not_complete": "Non achevé selon la source",
    "mixed_by_school_unit": "États différents selon l’unité",
}


def _format_number_fr(value: int | float | Decimal, decimals: int = 0) -> str:
    rendered = f"{value:,.{decimals}f}"
    return rendered.replace(",", "_").replace(".", ",").replace("_", "\u202f")


def _format_euro(value: Decimal) -> str:
    if value >= 1_000_000 and value % 10_000 == 0:
        millions = _format_number_fr(
            value / Decimal(1_000_000), 2
        ).rstrip("0").rstrip(",")
        return f"{millions} M€"
    decimals = 2 if value % 1 else 0
    return f"{_format_number_fr(value, decimals)} €"


def dashboard_metrics(passport: dict[str, Any]) -> dict[str, Any]:
    records = [
        record for case in passport["case_studies"] for record in case["records"]
    ]
    state_counts = {
        state: sum(record["reported_state"] == state for record in records)
        for state in (
            "reported_complete",
            "reported_in_progress",
            "reported_not_complete",
        )
    }
    milestones = {
        item["evidence_id"]: item
        for item in passport["administrative_chain"]["milestones"]
    }

    def amount(evidence_id: str) -> Decimal:
        return Decimal(str(milestones[evidence_id]["amount"]["value"]))

    return {
        "school_units": len(records),
        "case_studies": len(passport["case_studies"]),
        "state_counts": state_counts,
        "reported_surface_m2": sum(
            float(record["deimpermeabilized_surface_m2"] or 0) for record in records
        ),
        "reported_trees": sum(int(record["trees_planted"] or 0) for record in records),
        "finance": {
            "programme_authorization": amount("evidence-apcp-respire-total-2022"),
            "payment_credits_2023": amount("evidence-budget-2023-cp-opened"),
            "executed_2022": amount("evidence-account-2022-respire-expenditure"),
            "cumulative_mandates_before_2023": amount(
                "evidence-budget-2023-prior-mandates"
            ),
        },
    }


def render_site_header(active: str, prefix: str = "") -> str:
    home_current = ' aria-current="page"' if active == "home" else ""
    education_current = ' aria-current="page"' if active == "education" else ""
    detail_current = ' aria-current="page"' if active == "detail" else ""
    return f"""
<a class="skip-link" href="#contenu">Aller au contenu</a>
<header class="site-header no-print">
  <div class="site-header__inner">
    <a class="brand" href="{prefix}index.html" aria-label="IAgora — accueil Clermont-Ferrand">
      <span class="brand__mark" aria-hidden="true">IA</span>
      <span>IAgora</span>
    </a>
    <nav class="site-nav" aria-label="Navigation principale">
      <a href="{prefix}index.html"{home_current}>Vue ville</a>
      <a href="{prefix}education/index.html"{education_current}>Éducation</a>
      <a href="{prefix}programmes/respire-a-la-recre/index.html"{detail_current}>Dossier Respire</a>
    </nav>
    <span class="local-badge">Prototype local</span>
  </div>
</header>
"""


def render_footer() -> str:
    return """
<footer class="site-footer">
  <div class="site-footer__inner">
    <span>IAgora — Transformer les données en connaissance.</span>
    <span>Prototype local · Publication bloquée · Sources inspectables</span>
  </div>
</footer>
"""


def _document_head(title: str, description: str) -> str:
    return f"""<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{html.escape(description, quote=True)}">
  <title>{html.escape(title)}</title>
  <style>{PAGE_STYLES}</style>
</head>
"""


def render_dashboard_html(passport: dict[str, Any]) -> str:
    metrics = dashboard_metrics(passport)
    finance = metrics["finance"]
    complete = metrics["state_counts"]["reported_complete"]
    return (
        _document_head(
            "IAgora — Clermont-Ferrand",
            "Prototype local du tableau de bord civique IAgora pour Clermont-Ferrand.",
        )
        + """
<body>
"""
        + render_site_header("home")
        + f"""
<main id="contenu" class="page">
  <section class="hero" aria-labelledby="titre-ville">
    <div>
      <p class="eyebrow">Clermont-Ferrand · Observation au 31 décembre 2025</p>
      <h1 id="titre-ville">L’action publique, reliée à ses preuves.</h1>
      <p class="lede">Une lecture synthétique de la ville, avec un chemin direct vers les indicateurs, les décisions, les finances et les sources.</p>
    </div>
    <p class="hero-note"><strong>Première tranche locale</strong>Seul le domaine Éducation dispose actuellement d’un parcours alimenté. Cette interface n’est pas une publication civique autorisée.</p>
  </section>

  <div class="section-heading">
    <div><p class="eyebrow">Vue d’ensemble</p><h2>Trajectoire de Clermont-Ferrand</h2></div>
    <p>Le composant macro est prêt, mais aucune série transversale n’est encore suffisamment définie et revue pour être affichée comme résultat de la ville.</p>
  </div>
  <div class="macro-grid">
    <figure class="panel macro-figure" aria-labelledby="macro-title">
      <h3 id="macro-title">Évolution des grands domaines</h3>
      <div class="macro-plot" aria-hidden="true">
        <div class="pending-series"><span>Éducation</span><span class="pending-series__line"></span></div>
        <div class="pending-series"><span>Finances</span><span class="pending-series__line"></span></div>
        <div class="pending-series"><span>Culture</span><span class="pending-series__line"></span></div>
        <div class="pending-series"><span>Sécurité</span><span class="pending-series__line"></span></div>
      </div>
      <figcaption>Données insuffisantes pour une comparaison macro. Les pointillés signalent une série à définir, pas une valeur nulle.</figcaption>
    </figure>
    <aside class="panel coverage-panel" aria-label="Couverture actuelle du prototype">
      <h3>Couverture du prototype</h3>
      <span class="coverage-number">1/4</span>
      <p>Un domaine dispose d’une première tranche vérifiable. Les autres restent visibles pour montrer le produit cible sans inventer de KPI.</p>
    </aside>
  </div>

  <div class="section-heading">
    <div><p class="eyebrow">Politiques publiques</p><h2>Explorer par domaine</h2></div>
    <p>Chaque bloc accueillera un ou deux indicateurs phares, puis donnera accès aux définitions et preuves détaillées.</p>
  </div>
  <div class="theme-grid">
    <a class="theme-card theme-card--active" href="education/index.html">
      <div class="theme-card__top"><h3>Éducation</h3><span class="tag">Première tranche</span></div>
      <p>Végétalisation des cours d’école et première lecture du programme « Respire à la récré ».</p>
      <div class="theme-card__metrics">
        <span class="mini-metric"><strong>{metrics['school_units']}</strong><span>unités scolaires documentées</span></span>
        <span class="mini-metric"><strong>{complete}</strong><span>achèvements déclarés</span></span>
      </div>
      <span class="theme-card__cta">Explorer l’éducation →</span>
    </a>
    <a class="theme-card theme-card--active" href="education/index.html#finances">
      <div class="theme-card__top"><h3>Finances</h3><span class="tag tag--pending">Périmètre programme</span></div>
      <p>Premières observations financières disponibles uniquement pour « Respire à la récré ».</p>
      <div class="theme-card__metrics">
        <span class="mini-metric"><strong>{_format_euro(finance['programme_authorization'])}</strong><span>autorisation de programme</span></span>
        <span class="mini-metric"><strong>{_format_euro(finance['executed_2022'])}</strong><span>dépense 2022 déclarée</span></span>
      </div>
      <span class="theme-card__cta">Voir le périmètre financier →</span>
    </a>
    <article class="theme-card theme-card--muted">
      <div class="theme-card__top"><h3>Culture</h3><span class="tag tag--pending">À documenter</span></div>
      <p>Aucun KPI n’est encore sélectionné. Une source et une définition seront nécessaires avant toute visualisation.</p>
      <span class="theme-card__cta">Données en préparation</span>
    </article>
    <article class="theme-card theme-card--muted">
      <div class="theme-card__top"><h3>Sécurité</h3><span class="tag tag--pending">À documenter</span></div>
      <p>Aucun KPI n’est encore sélectionné. Les futures données devront être agrégées et éviter toute surveillance individuelle.</p>
      <span class="theme-card__cta">Données en préparation</span>
    </article>
  </div>

  <div class="section-heading"><div><p class="eyebrow">Principe de lecture</p><h2>Du chiffre à la preuve</h2></div></div>
  <div class="method-strip">
    <div class="method-step"><span>01</span><h3>Voir</h3><p>Un indicateur lisible, son périmètre et sa date.</p></div>
    <div class="method-step"><span>02</span><h3>Comprendre</h3><p>La méthode, les limites et les valeurs incompatibles.</p></div>
    <div class="method-step"><span>03</span><h3>Vérifier</h3><p>Les décisions, documents, données et transformations.</p></div>
  </div>
</main>
"""
        + render_footer()
        + "\n</body>\n</html>\n"
    )


def render_policy_timeline(passport: dict[str, Any]) -> str:
    milestones = {
        item["evidence_id"]: item
        for item in passport["administrative_chain"]["milestones"]
    }

    def evidence_link(evidence_id: str, label: str) -> str:
        source_url = html.escape(
            milestones[evidence_id]["source_url"], quote=True
        )
        return (
            f'<a href="{source_url}" rel="external noreferrer">'
            f"{html.escape(label)}</a>"
        )

    archive_url = html.escape(
        passport["provenance"]["campaign_artifact"]["archive_url"], quote=True
    )
    return f"""
<ol class="timeline">
  <li><time datetime="2019">2019</time><strong>Promesse de campagne archivée</strong><p><a href="{archive_url}" rel="external noreferrer">« Végétalisation des cours d’école »</a>, sans quantité, budget ni échéance dans le fragment primaire.</p></li>
  <li><time datetime="2022">2022</time><strong>Financement et premières réalisations documentés</strong><p>Les pièces conservées établissent une {evidence_link("evidence-apcp-respire-total-2022", "autorisation de programme")} et un {evidence_link("evidence-transition-nestor-reported-use", "usage déclaré à Nestor-Perret")}, pas leur filiation avec la promesse.</p></li>
  <li><time datetime="2023">2023</time><strong>Politique éducative adoptée</strong><p>Le {evidence_link("evidence-pev-adoption-2023", "projet éducatif municipal")} définit « Respire à la récré » dans un périmètre plus large que la promesse.</p></li>
  <li><time datetime="2025-12-31">2025</time><strong>Observation historique du POC</strong><p>Trois cas scolaires sont décrits ; marchés, réception compétente, résultats et impacts restent incomplets.</p></li>
</ol>
"""


def render_multidimensional_summary() -> str:
    items = (
        ("Respect de la promesse", "Non vérifiable"),
        ("Mise en œuvre", "Actions documentées"),
        ("Exécution financière", "Programme partiellement documenté"),
        ("Productions", "Sorties déclarées limitées"),
        ("Résultats et impact", "Non établis"),
        ("Filiation", "Indéterminable"),
        ("Preuves et revue", "Partielles · revue en attente"),
    )
    return '<div class="summary-grid">' + "".join(
        f'<div class="summary-item"><span>{html.escape(label)}</span><strong>{html.escape(value)}</strong></div>'
        for label, value in items
    ) + "</div>"


def render_education_html(passport: dict[str, Any]) -> str:
    metrics = dashboard_metrics(passport)
    counts = metrics["state_counts"]
    finance = metrics["finance"]
    total = metrics["school_units"]
    case_cards = "".join(
        "<article class=\"school-card\">"
        f"<h3>{html.escape(case['school_name'])}</h3>"
        f"<p>{html.escape(STATUS_LABELS[case['reported_summary']])}. Les unités scolaires restent distinctes.</p>"
        "</article>"
        for case in passport["case_studies"]
    )
    return (
        _document_head(
            "IAgora — Éducation à Clermont-Ferrand",
            "Première tranche du tableau de bord Éducation de Clermont-Ferrand.",
        )
        + "<body>\n"
        + render_site_header("education", "../")
        + f"""
<main id="contenu" class="page">
  <nav class="breadcrumbs" aria-label="Fil d’Ariane"><a href="../index.html">Clermont-Ferrand</a> / Éducation</nav>
  <section class="hero" aria-labelledby="titre-education">
    <div>
      <p class="eyebrow">Tableau de bord thématique · Première tranche</p>
      <h1 id="titre-education" class="page-title">Éducation</h1>
      <p class="lede">Une première lecture bornée de la végétalisation des cours d’école, reliée à la promesse, aux décisions, aux finances et aux sources disponibles.</p>
    </div>
    <div>
      <p class="hero-note"><strong>Périmètre limité</strong>Trois écoles et six unités scolaires. Ces chiffres ne décrivent pas l’ensemble des écoles de Clermont-Ferrand.</p>
      <div class="actions no-print"><a class="button" href="../programmes/respire-a-la-recre/index.html">Ouvrir le dossier complet</a><button class="button button--secondary" type="button" onclick="window.print()">Imprimer</button></div>
    </div>
  </section>

  <div class="kpi-grid" aria-label="Indicateurs principaux du périmètre pilote">
    <div class="kpi kpi--primary"><span class="kpi__value">{metrics['school_units']}</span><span class="kpi__label">unités scolaires documentées dans le POC</span></div>
    <div class="kpi"><span class="kpi__value">{counts['reported_complete']}</span><span class="kpi__label">achèvements déclarés par la source, sans réception indépendante</span></div>
    <div class="kpi"><span class="kpi__value">{_format_number_fr(metrics['reported_surface_m2'])}</span><span class="kpi__label">m² désimperméabilisés déclarés dans quatre lignes renseignées</span></div>
    <div class="kpi"><span class="kpi__value">{metrics['reported_trees']}</span><span class="kpi__label">arbres plantés déclarés dans quatre lignes renseignées</span></div>
  </div>

  <div class="section-heading"><div><p class="eyebrow">Avancement déclaré</p><h2>Six unités, trois états</h2></div><p>Le graphique décrit uniquement les six lignes du jeu de données borné. Il ne mesure ni la promesse globale ni toutes les écoles.</p></div>
  <div class="two-column">
    <section class="panel" aria-labelledby="repartition-title">
      <h3 id="repartition-title">Répartition des états déclarés</h3>
      <div class="status-bar" role="img" aria-label="{counts['reported_complete']} unités déclarées achevées, {counts['reported_in_progress']} en cours et {counts['reported_not_complete']} non achevée">
        <span class="status-complete" style="width:{100 * counts['reported_complete'] / total:.4f}%"></span>
        <span class="status-progress" style="width:{100 * counts['reported_in_progress'] / total:.4f}%"></span>
        <span class="status-incomplete" style="width:{100 * counts['reported_not_complete'] / total:.4f}%"></span>
      </div>
      <ul class="legend">
        <li><span class="legend__swatch status-complete"></span><span>Achèvement déclaré</span><strong>{counts['reported_complete']}</strong></li>
        <li><span class="legend__swatch status-progress"></span><span>En cours selon la source</span><strong>{counts['reported_in_progress']}</strong></li>
        <li><span class="legend__swatch status-incomplete"></span><span>Non achevé selon la source</span><strong>{counts['reported_not_complete']}</strong></li>
      </ul>
    </section>
    <aside class="panel">
      <h3>Cas documentés</h3>
      <div class="school-list">{case_cards}</div>
    </aside>
  </div>

  <div class="section-heading"><div><p class="eyebrow">Filiation</p><h2>Promesse, décisions et réalisations</h2></div><p>La chronologie rend les étapes visibles. Elle ne prouve pas que le programme est inédit ni qu’il prolonge une politique antérieure.</p></div>
  <section class="panel" aria-labelledby="timeline-title">
    <div class="theme-card__top"><h3 id="timeline-title">Filiation actuellement indéterminable</h3><span class="tag tag--pending">Revue nécessaire</span></div>
    {render_policy_timeline(passport)}
  </section>

  <div id="finances" class="section-heading"><div><p class="eyebrow">Finances du programme</p><h2>Des étapes, pas un total unique</h2></div><p>Les périodes et stades diffèrent. Aucun taux d’exécution n’est calculé et aucune somme n’est attribuée à une école sans preuve.</p></div>
  <section class="panel" aria-labelledby="finance-title">
    <h3 id="finance-title">Observations disponibles pour « Respire à la récré »</h3>
    <div class="finance-grid">
      <div class="finance-item"><strong>{_format_euro(finance['programme_authorization'])}</strong><span>autorisation de programme documentée</span></div>
      <div class="finance-item"><strong>{_format_euro(finance['payment_credits_2023'])}</strong><span>crédits de paiement ouverts pour 2023</span></div>
      <div class="finance-item"><strong>{_format_euro(finance['executed_2022'])}</strong><span>dépense d’investissement 2022 déclarée</span></div>
      <div class="finance-item"><strong>{_format_euro(finance['cumulative_mandates_before_2023'])}</strong><span>mandats cumulés avant 2023, pas une preuve de paiement final</span></div>
    </div>
  </section>

  <section class="panel notice" aria-labelledby="conclusion-education">
    <h2 id="conclusion-education">Ce que cette tranche permet de dire</h2>
    <p>Des actions, décisions et montants sont documentés. Le respect global de la promesse, la filiation avec une politique antérieure, les résultats et l’impact sur la ville restent non vérifiables.</p>
    <a href="../programmes/respire-a-la-recre/index.html">Examiner la méthode et les preuves →</a>
  </section>
</main>
"""
        + render_footer()
        + "\n</body>\n</html>\n"
    )
