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
.site-nav a { padding-block: .25rem; }
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
.commitment-brief { margin-bottom: 1rem; }
.commitment-brief__header { display: grid; grid-template-columns: minmax(0, 1.5fr) minmax(14rem, .5fr); gap: 1.5rem; align-items: start; }
.commitment-brief__label { margin: 0; color: var(--muted); font-size: .78rem; font-weight: 800; letter-spacing: .04em; text-transform: uppercase; }
.commitment-brief__headline { margin: .25rem 0 0; font-size: clamp(1.65rem, 3vw, 2.35rem); }
.commitment-brief__programme { margin: .45rem 0 0; }
.commitment-brief__mapping { margin: .65rem 0 0; }
.campaign-source { margin: 1rem 0 0; padding: .9rem 1rem; border: 1px solid var(--line); border-radius: .8rem; background: #f7f8f4; }
.campaign-source p { margin: .35rem 0 0; color: var(--muted); font-size: .88rem; }
.missing-specifics { display: flex; flex-wrap: wrap; gap: .4rem; margin: .8rem 0 0; padding: 0; list-style: none; }
.missing-specifics li { padding: .28rem .55rem; border-radius: 999px; color: #6f4613; background: var(--amber-soft); font-size: .74rem; font-weight: 800; }
.hero--compact { grid-template-columns: minmax(0, 1fr) auto; align-items: center; padding: .8rem 0 1.5rem; }
.hero--compact h1 { font-size: clamp(2.4rem, 5vw, 3.8rem); }
.hero--compact .lede { margin-top: .55rem; }
.commitment-brief__verdict { padding: 1rem; border-radius: .8rem; color: var(--surface); background: var(--forest); }
.commitment-brief__verdict span { display: block; color: #d6e3dc; font-size: .76rem; font-weight: 800; letter-spacing: .04em; text-transform: uppercase; }
.commitment-brief__verdict strong { display: block; margin-top: .3rem; color: var(--lime); font-size: 1.45rem; }
.commitment-brief__verdict .technical-status { margin-top: .75rem; color: #d6e3dc; font-size: .76rem; font-weight: 650; letter-spacing: 0; text-transform: none; }
.theme-list { display: flex; flex-wrap: wrap; gap: .45rem; margin: 1rem 0 0; padding: 0; list-style: none; }
.theme-list li { padding: .28rem .6rem; border: 1px solid var(--line); border-radius: 999px; background: #f7f8f4; font-size: .78rem; font-weight: 750; }
.state-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: .8rem; margin-top: 1.25rem; }
.status-figure { margin: 1rem 0 0; }
.status-figure figcaption { display: flex; justify-content: space-between; gap: 1rem; align-items: baseline; margin: 0; }
.status-figure figcaption span { color: var(--muted); font-size: .8rem; }
.status-bar--summary { height: 1.35rem; margin: .55rem 0 0; }
.status-bar--summary > * + * { border-left: .16rem solid var(--surface); }
.state-card { padding: 1rem; border: 1px solid var(--line); border-top: .32rem solid var(--forest); border-radius: .75rem; color: var(--ink); text-decoration: none; }
.state-card:hover { border-color: var(--forest); }
.state-card--progress { border-top-color: #a86d16; }
.state-card--incomplete { border-top-color: var(--terracotta); }
.state-card strong { display: block; font-size: 1.45rem; }
.state-card span { display: block; color: var(--muted); font-size: .84rem; }
.state-card__label { display: none !important; }
.commitment-brief__limit { margin: 1rem 0 0; padding: .8rem 1rem; border-left: .3rem solid var(--terracotta); background: var(--amber-soft); }
.scope-details { margin-top: 1rem; border-top: 1px solid var(--line); }
.scope-details summary { padding: 1rem 0 .2rem; color: var(--forest); font-weight: 850; cursor: pointer; }
.scope-details dl { display: grid; grid-template-columns: minmax(9rem, .35fr) minmax(0, 1fr); gap: .6rem 1rem; margin-bottom: 0; }
.scope-details dt { font-weight: 850; }
.scope-details dd { margin: 0; color: var(--muted); }
.two-column { display: grid; grid-template-columns: minmax(0, 1.2fr) minmax(17rem, .8fr); gap: 1rem; }
.status-bar { height: 2rem; display: flex; overflow: hidden; margin: 1.4rem 0 1.1rem; border-radius: 999px; background: #e6e9e5; }
.status-bar > span, .status-bar > a { min-width: 1px; }
.status-bar > a { display: block; text-decoration: none; }
.status-complete { background: var(--forest); }
.status-progress { background: var(--amber); }
.status-incomplete { background: var(--terracotta); }
.sr-only { position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px; overflow: hidden; clip: rect(0, 0, 0, 0); white-space: nowrap; border: 0; }
.evidence-chain { display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap: .55rem; margin: 1rem 0 0; padding: 0; list-style: none; }
.evidence-chain a { min-height: 8.2rem; display: flex; flex-direction: column; padding: .85rem; border: 1px solid var(--line); border-top: .32rem solid var(--forest); border-radius: .75rem; color: var(--ink); text-decoration: none; background: #f7f8f4; }
.evidence-chain a:hover { border-color: var(--forest); }
.evidence-chain .chain--pending { border-top-color: #a86d16; }
.evidence-chain .chain--missing { border-top-color: var(--terracotta); }
.chain__number { color: var(--terracotta); font-size: .75rem; font-weight: 900; letter-spacing: .06em; }
.chain__state { margin-top: auto; color: var(--muted); font-size: .76rem; }
.chain-note { margin: .7rem 0 0; color: var(--muted); font-size: .88rem; }
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
.state-detail-list { display: grid; gap: 1rem; }
.state-detail { scroll-margin-top: 1rem; padding: 1rem; border: 1px solid var(--line); border-radius: .8rem; }
.state-detail h3 { display: flex; justify-content: space-between; gap: .8rem; align-items: baseline; }
.state-detail h3 span { color: var(--muted); font-size: .78rem; font-weight: 700; letter-spacing: normal; }
.unit-list { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: .7rem; margin: 1rem 0 0; padding: 0; list-style: none; }
.unit-card { padding: .85rem; border: 1px solid var(--line); border-radius: .7rem; background: #f7f8f4; }
.unit-card strong, .unit-card span { display: block; }
.unit-card span, .unit-card p { color: var(--muted); font-size: .82rem; }
.unit-card p { margin: .6rem 0; }
.unit-card a { font-size: .82rem; font-weight: 800; }
.finance-status-grid { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: .7rem; margin: 1rem 0; }
.finance-status { padding: .85rem; border: 1px solid var(--line); border-radius: .7rem; background: #f7f8f4; }
.finance-status span { display: block; color: var(--muted); font-size: .75rem; font-weight: 800; text-transform: uppercase; }
.finance-status strong { display: block; margin-top: .25rem; }
.source-card-grid, .change-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: .8rem; }
.source-card, .change-card { padding: 1rem; border: 1px solid var(--line); border-radius: .8rem; background: #f7f8f4; }
.source-card p, .change-card p { margin-bottom: 0; color: var(--muted); font-size: .88rem; }
.source-kind { display: block; margin-bottom: .4rem; color: var(--terracotta); font-size: .72rem; font-weight: 900; letter-spacing: .04em; text-transform: uppercase; }
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
  .hero, .macro-grid, .two-column, .commitment-brief__header, .hero--compact { grid-template-columns: 1fr; }
  .summary-grid, .school-list, .unit-list, .finance-status-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .evidence-chain { grid-template-columns: repeat(3, minmax(0, 1fr)); }
}
@media (max-width: 620px) {
  .site-header__inner { align-items: flex-start; flex-wrap: wrap; }
  .site-nav { order: 3; width: 100%; margin: 0; overflow-x: auto; padding-bottom: .2rem; }
  .local-badge { margin-left: auto; }
  .page { padding-top: 1rem; }
  .hero { padding-top: 1.5rem; }
  .hero--compact { padding-top: .4rem; }
  .hero--compact h1 { font-size: 2.55rem; }
  .hero--compact .lede { display: none; }
  .hero--compact .actions { gap: .45rem; }
  .hero--compact .button { min-height: 2.5rem; padding: .5rem .75rem; font-size: .86rem; }
  .breadcrumbs { margin-bottom: .9rem; }
  .theme-grid, .kpi-grid, .finance-grid, .method-strip, .unit-list, .finance-status-grid, .source-card-grid, .change-grid, .evidence-chain { grid-template-columns: 1fr; }
  .evidence-chain a { min-height: 0; }
  .commitment-brief__verdict { padding: .75rem; }
  .commitment-brief__verdict strong { font-size: 1.3rem; }
  .commitment-brief__verdict p { margin: .25rem 0 0; font-size: .8rem; }
  .state-grid { grid-template-columns: repeat(3, minmax(0, 1fr)); gap: .35rem; }
  .status-figure figcaption { align-items: start; flex-direction: column; gap: .1rem; }
  .state-card { padding: .65rem .45rem; text-align: center; }
  .state-card strong { font-size: 1.05rem; }
  .state-card__label { display: block !important; color: var(--ink) !important; font-size: .72rem !important; font-weight: 750; }
  .state-card__detail { display: none !important; }
  .scope-details dl { grid-template-columns: 1fr; gap: .15rem; }
  .scope-details dd { margin-bottom: .65rem; }
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


def _format_date_fr(value: str) -> str:
    year, month, day = value[:10].split("-")
    months = (
        "janvier", "février", "mars", "avril", "mai", "juin",
        "juillet", "août", "septembre", "octobre", "novembre", "décembre",
    )
    return f"{int(day)} {months[int(month) - 1]} {year}"


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
      <figcaption>Nous n’avons pas encore assez de données pour comparer ces grands domaines. Les pointillés signifient « donnée manquante », pas zéro.</figcaption>
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
      <div class="theme-card__top"><h3>Finances</h3><span class="tag tag--pending">Données partielles</span></div>
      <p>Premières observations financières disponibles uniquement pour « Respire à la récré ».</p>
      <div class="theme-card__metrics">
        <span class="mini-metric"><strong>{_format_euro(finance['programme_authorization'])}</strong><span>budget total autorisé</span></span>
        <span class="mini-metric"><strong>{_format_euro(finance['executed_2022'])}</strong><span>dépenses enregistrées en 2022</span></span>
      </div>
      <span class="theme-card__cta">Comprendre ces montants →</span>
    </a>
    <article class="theme-card theme-card--muted">
      <div class="theme-card__top"><h3>Culture</h3><span class="tag tag--pending">À documenter</span></div>
      <p>Aucun indicateur principal n’est encore prêt. Il faut d’abord trouver des données fiables et expliquer ce qu’elles mesurent.</p>
      <span class="theme-card__cta">Données en préparation</span>
    </article>
    <article class="theme-card theme-card--muted">
      <div class="theme-card__top"><h3>Sécurité</h3><span class="tag tag--pending">À documenter</span></div>
      <p>Aucun indicateur principal n’est encore prêt. Les futures données devront protéger les personnes et ne jamais servir à les surveiller.</p>
      <span class="theme-card__cta">Données en préparation</span>
    </article>
  </div>

  <div class="section-heading"><div><p class="eyebrow">Principe de lecture</p><h2>Du chiffre à la preuve</h2></div></div>
  <div class="method-strip">
    <div class="method-step"><span>01</span><h3>Voir</h3><p>Un chiffre lisible, ce qu’il concerne et sa date.</p></div>
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
  <li><time datetime="2019">2019</time><strong>La phrase de campagne est retrouvée</strong><p><a href="{archive_url}" rel="external noreferrer">« Végétalisation des cours d’école »</a>. Le texte retrouvé ne précise ni combien d’écoles, ni quel budget, ni quelle date de fin.</p></li>
  <li><time datetime="2022">2022</time><strong>Un budget et une première école apparaissent dans les documents</strong><p>Les documents montrent un {evidence_link("evidence-apcp-respire-total-2022", "budget total autorisé")} et indiquent que {evidence_link("evidence-transition-nestor-reported-use", "les élèves utilisent le nouvel espace de Nestor-Perret")}. Ils ne disent pas clairement que ces actions viennent de la promesse.</p></li>
  <li><time datetime="2023">2023</time><strong>Le conseil municipal adopte le projet éducatif qui contient « Respire à la récré »</strong><p>Le {evidence_link("evidence-pev-adoption-2023", "projet éducatif municipal")} décrit cette action. Elle est plus large que la phrase prononcée pendant la campagne.</p></li>
  <li><time datetime="2025-12-31">2025</time><strong>Dernière date étudiée par ce prototype</strong><p>Nous disposons d’informations sur trois écoles. Il manque encore les contrats de travaux, les documents confirmant leur fin et les mesures de leurs effets.</p></li>
</ol>
"""


def render_multidimensional_summary(passport: dict[str, Any]) -> str:
    metrics = dashboard_metrics(passport)
    complete = metrics["state_counts"]["reported_complete"]
    in_progress = metrics["state_counts"]["reported_in_progress"]
    not_complete = metrics["state_counts"]["reported_not_complete"]
    items = (
        (
            "Ce qui a été promis",
            "Végétaliser des cours d’école, sans nombre, date ni budget dans le texte retrouvé",
        ),
        (
            "Ce qui est documenté",
            f"{metrics['school_units']} unités étudiées : {complete} indiquées comme terminées par la mairie",
        ),
        (
            "Ce qui reste dans les données étudiées",
            f"{in_progress} unités indiquées en cours et {not_complete} non terminée",
        ),
        (
            "Ce que nous ne pouvons pas vérifier",
            "Toute la promesse, le coût final, les résultats et les effets sur la ville",
        ),
        (
            "Argent public retrouvé",
            "4,07 M€ autorisés pour le programme ; 1,09 M€ de dépenses enregistrées en 2022",
        ),
        (
            "État des sources",
            "Sources partielles et lien promesse-programme encore à vérifier",
        ),
    )
    return '<div class="summary-grid">' + "".join(
        f'<div class="summary-item"><span>{html.escape(label)}</span><strong>{html.escape(value)}</strong></div>'
        for label, value in items
    ) + "</div>"


def render_execution_chain(passport: dict[str, Any]) -> str:
    archive_url = html.escape(
        passport["provenance"]["campaign_artifact"]["archive_url"], quote=True
    )
    steps = (
        (
            archive_url,
            "",
            "01",
            "Promesse",
            "Texte de campagne retrouvé",
        ),
        (
            "#filiation",
            "chain--pending",
            "02",
            "Lien avec le programme",
            "Lien possible, pas encore validé",
        ),
        (
            "#filiation",
            "",
            "03",
            "Décision de la mairie",
            "Projet éducatif contenant l’action adopté",
        ),
        (
            "#finances",
            "chain--pending",
            "04",
            "Argent public",
            "Une partie des budgets et dépenses est connue",
        ),
        (
            "#cas-documentes",
            "chain--missing",
            "05",
            "Travaux dans les écoles",
            "États publiés par la mairie ; documents officiels de fin manquants",
        ),
    )
    return f"""
    <div aria-labelledby="chaine-title">
      <h3 id="chaine-title">Ce que nous pouvons suivre, de la promesse aux travaux</h3>
      <ol class="evidence-chain">
        {''.join(
            '<li><a class="' + css_class + '" href="' + href + '">'
            '<span class="chain__number">' + number + '</span>'
            '<strong>' + label + '</strong>'
            '<span class="chain__state">' + state + '</span>'
            '</a></li>'
            for href, css_class, number, label, state in steps
        )}
      </ol>
      <p class="chain-note"><strong>Pourquoi n’affichons-nous pas 20 %, 50 % ou 100 % ?</strong> Pour calculer un pourcentage, il faudrait savoir combien d’écoles le candidat avait promis de transformer. Le texte retrouvé ne le dit pas. Afficher un pourcentage serait donc trompeur.</p>
    </div>
"""


def render_observed_state_details(passport: dict[str, Any]) -> str:
    source_url = html.escape(passport["provenance"]["source_url"], quote=True)
    records = [
        record for case in passport["case_studies"] for record in case["records"]
    ]
    groups = (
        (
            "reported_complete",
            "etat-realise",
            "Travaux indiqués comme terminés par la mairie",
            "Nous n’avons pas encore le document administratif qui confirme officiellement la fin des travaux.",
        ),
        (
            "reported_in_progress",
            "etat-en-cours",
            "Travaux indiqués comme étant en cours par la mairie",
            "Il faudra vérifier leur fin dans une prochaine mise à jour.",
        ),
        (
            "reported_not_complete",
            "etat-non-acheve",
            "Travaux indiqués comme non terminés par la mairie",
            "Cette information concerne cette unité scolaire seulement. Elle ne permet pas de juger toute la promesse.",
        ),
    )
    sections = []
    for state, anchor, heading, qualification in groups:
        unit_cards = []
        for record in sorted(
            (item for item in records if item["reported_state"] == state),
            key=lambda item: (item["school_name"], item["school_unit"]),
        ):
            measures = []
            if record["deimpermeabilized_surface_m2"] is not None:
                measures.append(
                    f"{_format_number_fr(record['deimpermeabilized_surface_m2'])} m² de sol rendus perméables d’après la mairie"
                )
            if record["trees_planted"] is not None:
                measures.append(f"{record['trees_planted']} arbres plantés d’après la mairie")
            measure_text = " · ".join(measures) if measures else "La mairie ne donne aucun chiffre de réalisation pour cette unité dans la ligne étudiée."
            unit_cards.append(
                f"""
                <li class="unit-card">
                  <strong>{html.escape(record['school_name'])}</strong>
                  <span>{html.escape(record['school_unit'])} · année indiquée : {html.escape(record['vegetation_year'])}</span>
                  <p>{html.escape(measure_text)}</p>
                  <a href="{source_url}" rel="external noreferrer">Voir les données de cette école (identifiant UAI : {html.escape(record['uai'])}) →</a>
                </li>
"""
            )
        sections.append(
            f"""
            <section id="{anchor}" class="state-detail" aria-labelledby="{anchor}-title">
              <h3 id="{anchor}-title">{heading}<span>{len(unit_cards)} unité{'s' if len(unit_cards) > 1 else ''}</span></h3>
              <p>{qualification}</p>
              <ul class="unit-list">{''.join(unit_cards)}</ul>
            </section>
"""
        )
    return '<div class="state-detail-list">' + "".join(sections) + "</div>"


def render_finance_table(passport: dict[str, Any]) -> str:
    milestones = {
        item["evidence_id"]: item
        for item in passport["administrative_chain"]["milestones"]
    }
    evidence = {item["evidence_id"]: item for item in passport["evidence"]}
    rows = (
        (
            "evidence-apcp-respire-total-2022",
            "Budget total autorisé",
            "2022",
            "Ensemble du programme · détail des financeurs non disponible",
            "La mairie pouvait utiliser cette somme pour le programme. Cela ne veut pas dire qu’elle a été entièrement dépensée.",
            "Décision budgétaire du 29 juin 2022",
        ),
        (
            "evidence-apcp-respire-rephasing-2022",
            "Budget déplacé à l’année suivante",
            "2022 → 2023",
            "Ensemble du programme",
            "Cette somme était prévue en 2022 puis reportée à 2023 parce que les travaux avaient du retard. Ce n’est pas une économie.",
            "Décision budgétaire du 29 juin 2022",
        ),
        (
            "evidence-budget-2023-cp-opened",
            "Somme autorisée pour l’année",
            "2023",
            "Ensemble du programme",
            "Cette somme pouvait être utilisée en 2023. Le document ne dit pas qu’elle a été entièrement dépensée.",
            "Annexe du budget 2023 (AP/CP)",
        ),
        (
            "evidence-account-2022-respire-expenditure",
            "Dépenses enregistrées",
            "2022",
            "Ensemble du programme",
            "Le compte officiel de la mairie enregistre ce montant de dépenses d’investissement pour 2022.",
            "Compte administratif 2022 adopté",
        ),
        (
            "evidence-budget-2023-prior-mandates",
            "Ordres de paiement enregistrés",
            "Avant le 1er janvier 2023",
            "Ensemble du programme",
            "C’est un total arrêté à une date précise. Ce n’est pas le coût final du programme ni le total payé aujourd’hui.",
            "Annexe du budget 2023 (AP/CP)",
        ),
        (
            "evidence-pierre-curie-reported-cost",
            "Coût annoncé pour une école",
            "Travaux commencés en 2023",
            "École maternelle Pierre-et-Marie-Curie · financement annoncé par la mairie",
            "La mairie annonce ce coût. Nous n’avons pas encore la facture ni la preuve du paiement.",
            "Communiqué municipal Pierre-et-Marie-Curie",
        ),
        (
            "evidence-jean-zay-forecast-cost",
            "Coût estimé avant la fin des travaux",
            "2025",
            "Jean-Zay",
            "C’est une estimation hors taxes, pas le coût final.",
            "Plan de financement Jean-Zay",
        ),
        (
            "evidence-jean-zay-subsidy-amount",
            "Subvention indiquée dans le plan",
            "2025",
            "Jean-Zay · organisme qui verse la subvention non précisé dans l’extrait",
            "Le plan affiche cette somme. Nous n’avons pas encore la preuve qu’elle a été accordée ou versée.",
            "Plan de financement Jean-Zay",
        ),
    )
    rendered_rows = []
    for evidence_id, stage, period, scope, meaning, source_label in rows:
        item = milestones[evidence_id]
        amount = item["amount"]
        tax_basis = f" {amount['tax_basis']}" if amount["tax_basis"] != "not_stated" else ""
        rendered_rows.append(
            f"""
            <tr>
              <td>{html.escape(stage)}</td>
              <td><strong>{_format_euro(Decimal(str(amount['value'])))}{html.escape(tax_basis)}</strong></td>
              <td>{html.escape(period)}</td>
              <td>{html.escape(scope)}</td>
              <td>{html.escape(meaning)}</td>
              <td><a href="{html.escape(item['source_url'], quote=True)}" rel="external noreferrer">{html.escape(source_label)}</a></td>
            </tr>
"""
        )

    procurement_rows = (
        (
            "evidence-procurement-city-study-2020",
            "Contrat pour une étude",
            "2020",
            "Végétalisation des cours et îlots de fraîcheur",
            "Montant du contrat hors taxes. Le registre ne dit pas clairement qu’il appartient au programme « Respire à la récré ».",
            "Registre municipal des marchés publics",
        ),
        (
            "evidence-procurement-boamp-award-26-4348",
            "Contrats de conception et d’accompagnement",
            "Publié en 2026, après la dernière date couverte par cette démonstration",
            "Deux groupes comprenant plusieurs écoles",
            "Ces contrats concernent la préparation et l’accompagnement. Ils ne prouvent ni les travaux, ni leur paiement, ni leur fin.",
            "Avis officiel d’attribution (BOAMP)",
        ),
    )
    procurement = {
        item["evidence_id"]: item
        for item in passport["administrative_chain"]["procurement_records"]
    }
    for evidence_id, stage, period, scope, meaning, source_label in procurement_rows:
        item = procurement[evidence_id]
        amount = item["amount"]
        rendered_rows.append(
            f"""
            <tr>
              <td>{html.escape(stage)}</td>
              <td><strong>{_format_euro(Decimal(str(amount['value'])))} {html.escape(amount['tax_basis'])}</strong></td>
              <td>{html.escape(period)}</td>
              <td>{html.escape(scope)}</td>
              <td>{html.escape(meaning)}</td>
              <td><a href="{html.escape(evidence[evidence_id]['source_url'], quote=True)}" rel="external noreferrer">{html.escape(source_label)}</a></td>
            </tr>
"""
        )
    return f"""
    <div class="finance-status-grid" aria-label="Questions auxquelles les documents financiers actuels ne répondent pas complètement">
      <div class="finance-status"><span>Total réellement payé aujourd’hui</span><strong>Nous ne le savons pas encore</strong></div>
      <div class="finance-status"><span>Le budget a-t-il été respecté ?</span><strong>Impossible à dire avec les documents actuels</strong></div>
      <div class="finance-status"><span>Économies ou coûts évités</span><strong>Aucun document trouvé</strong></div>
      <div class="finance-status"><span>Qui a financé ?</span><strong>Une partie seulement est connue</strong></div>
    </div>
    <div class="table-wrap">
      <table>
        <caption>Les montants trouvés dans les documents officiels — ils ne veulent pas tous dire la même chose</caption>
        <thead><tr><th scope="col">À quoi correspond ce montant ?</th><th scope="col">Montant</th><th scope="col">Date ou période</th><th scope="col">Ce que cela concerne / qui finance</th><th scope="col">Comment lire ce montant</th><th scope="col">Document d’origine</th></tr></thead>
        <tbody>{''.join(rendered_rows)}</tbody>
      </table>
    </div>
    <p class="chain-note">Nous n’additionnons pas ces montants : certains parlent du même argent à des moments différents ; d’autres concernent une année ou une école particulière.</p>
"""


def render_public_context(passport: dict[str, Any]) -> str:
    milestones = {
        item["evidence_id"]: item
        for item in passport["administrative_chain"]["milestones"]
    }
    interview = passport["provenance"]["supporting_context_sources"][0]
    cards = (
        (
            "Article de presse pendant la campagne",
            "Entretien avec Olivier Bianchi — Info Clermont Métropole",
            interview["source_url"],
            "Cet article montre ce que le candidat déclarait pendant la campagne. Il aide à comprendre le contexte, mais ne prouve pas que la promesse a été réalisée.",
        ),
        (
            "Communication de la mairie",
            "Rapport municipal de transition 2022",
            milestones["evidence-transition-nestor-reported-use"]["source_url"],
            "La Ville déclare l’usage de l’espace Nestor-Perret depuis septembre 2022 et son inauguration en avril 2023.",
        ),
        (
            "Communiqué de la mairie",
            "Cour Pierre-et-Marie-Curie",
            milestones["evidence-pierre-curie-reported-delivery"]["source_url"],
            "La mairie dit que la cour maternelle a été réaménagée. Nous n’avons pas encore le document administratif qui confirme officiellement la fin des travaux.",
        ),
    )
    rendered = "".join(
        f"""
        <article class="source-card">
          <span class="source-kind">{html.escape(kind)}</span>
          <h3><a href="{html.escape(url, quote=True)}" rel="external noreferrer">{html.escape(title)}</a></h3>
          <p>{html.escape(description)}</p>
        </article>
"""
        for kind, title, url, description in cards
    )
    return f"""
    <div class="source-card-grid">
      {rendered}
      <article class="source-card">
        <span class="source-kind">Presse et autres déclarations</span>
        <h3>Cette recherche reste à faire</h3>
        <p>Nous n’avons pas encore réuni et vérifié un ensemble complet d’articles de presse, de déclarations d’élus et de corrections. Cela ne signifie pas que ces documents n’existent pas.</p>
      </article>
    </div>
"""


def render_changes_and_counterevidence() -> str:
    return """
    <div class="change-grid">
      <article class="change-card">
        <span class="source-kind">Le projet a changé ou s’est élargi</span>
        <h3>Le programme va plus loin que la phrase de campagne</h3>
        <p>« Respire à la récré » ne parle pas seulement de végétation : il ajoute la lutte contre la chaleur, l’écoulement de l’eau, l’accessibilité et la participation des usagers. Cela peut être une évolution de la promesse, mais nous devons encore vérifier le lien exact.</p>
      </article>
      <article class="change-card">
        <span class="source-kind">Décision qui va clairement contre la promesse</span>
        <h3>Nous n’en avons trouvé aucune dans les documents étudiés</h3>
        <p>Notre recherche n’est pas terminée. Ne rien avoir trouvé ne signifie pas qu’une telle décision n’existe pas.</p>
      </article>
    </div>
"""


def render_commitment_brief(passport: dict[str, Any]) -> str:
    metrics = dashboard_metrics(passport)
    counts = metrics["state_counts"]
    commitment = passport["campaign_commitment"]
    mapping = passport["commitment_mapping"]
    attribution = commitment["attribution"]
    campaign_artifact = passport["provenance"]["campaign_artifact"]
    archive_url = html.escape(campaign_artifact["archive_url"], quote=True)
    capture_date = _format_date_fr(campaign_artifact["capture_at"])
    total = metrics["school_units"]
    return f"""
  <section class="panel commitment-brief" aria-labelledby="essentiel-title">
    <div class="commitment-brief__header">
      <div>
        <p class="eyebrow">L’essentiel en un regard</p>
        <p class="commitment-brief__label">Promesse de campagne</p>
        <h2 id="essentiel-title" class="commitment-brief__headline">«&nbsp;{html.escape(commitment['wording'])}&nbsp;»</h2>
        <p><strong>{html.escape(attribution['actor'])}</strong> · liste {html.escape(attribution['campaign_list'])} · municipales 2020 à Clermont-Ferrand</p>
        <p class="commitment-brief__programme">Programme municipal qui pourrait correspondre : <strong>« {html.escape(mapping['target_programme_name'])} »</strong></p>
      </div>
      <div class="commitment-brief__verdict">
        <span>La promesse a-t-elle été tenue ?</span>
        <strong>Pas assez de preuves pour répondre</strong>
        <p>Le candidat n’a pas indiqué combien d’écoles il voulait transformer dans le texte retrouvé.</p>
        <span class="technical-status">Statut conservé dans les données : Non vérifiable</span>
      </div>
    </div>
    <div id="preuve-promesse" class="campaign-source">
      <strong>D’où vient cette phrase ? <a href="{archive_url}" rel="external noreferrer">D’une page de campagne archivée le {capture_date}</a></strong>
      <p>Cette page confirme que la phrase a bien été publiée pendant la campagne. Dans le passage retrouvé, le candidat n’explique pas combien d’écoles sont concernées, quand les travaux doivent être terminés, combien ils coûteront ni comment ils seront organisés.</p>
      <ul class="missing-specifics" aria-label="Informations absentes du texte de campagne retrouvé">
        <li>Nombre d’écoles non indiqué</li>
        <li>Calendrier non indiqué</li>
        <li>Budget non indiqué</li>
        <li>Financement non indiqué</li>
        <li>Organisation des travaux non indiquée</li>
      </ul>
    </div>
    {render_execution_chain(passport)}
    <figure class="status-figure">
      <figcaption><strong>Les six unités scolaires que nous avons pu vérifier</strong><span>Données publiées par la mairie · mises à jour jusqu’au 31 décembre 2025 · ce graphique ne représente pas toute la ville</span></figcaption>
      <div class="status-bar status-bar--summary" role="group" aria-label="Selon les données publiées par la mairie : {counts['reported_complete']} unités indiquées comme terminées, {counts['reported_in_progress']} en cours et {counts['reported_not_complete']} non terminée, sur les six unités scolaires étudiées">
        <a class="status-complete" href="#etat-realise" style="width:{100 * counts['reported_complete'] / total:.4f}%"><span class="sr-only">Voir les {counts['reported_complete']} unités déclarées réalisées</span></a>
        <a class="status-progress" href="#etat-en-cours" style="width:{100 * counts['reported_in_progress'] / total:.4f}%"><span class="sr-only">Voir les {counts['reported_in_progress']} unités déclarées en cours</span></a>
        <a class="status-incomplete" href="#etat-non-acheve" style="width:{100 * counts['reported_not_complete'] / total:.4f}%"><span class="sr-only">Voir l’unité déclarée non achevée</span></a>
      </div>
    </figure>
    <div class="state-grid" aria-label="La mairie indique trois unités terminées, deux encore en cours et une non terminée ; les documents administratifs confirmant la fin des travaux n’ont pas été retrouvés">
      <a class="state-card" href="#etat-realise"><strong>{counts['reported_complete']} unités</strong><span class="state-card__label">terminées</span><span class="state-card__detail">travaux indiqués comme terminés par la mairie ; document administratif de fin non retrouvé</span></a>
      <a class="state-card state-card--progress" href="#etat-en-cours"><strong>{counts['reported_in_progress']} unités</strong><span class="state-card__label">en cours</span><span class="state-card__detail">travaux encore en cours d’après la mairie</span></a>
      <a class="state-card state-card--incomplete" href="#etat-non-acheve"><strong>{counts['reported_not_complete']} unité</strong><span class="state-card__label">non terminée</span><span class="state-card__detail">travaux indiqués comme non terminés par la mairie</span></a>
    </div>
    <p class="chain-note">Dans les données de la mairie, la maternelle et l’élémentaire sont comptées séparément, même lorsqu’elles portent le même nom d’école.</p>
    <p class="commitment-brief__mapping"><strong>La promesse et le programme ne disent pas exactement la même chose :</strong> « Respire à la récré » prévoit davantage que la seule végétalisation. Nous avons des indices qui relient les deux. Ce lien doit encore être contrôlé par le responsable du POC, puis revu par des personnes indépendantes avant toute publication.</p>
    <p class="commitment-brief__limit"><strong>Attention :</strong> ces informations concernent seulement six unités dans trois écoles. Elles ne décrivent pas toutes les écoles de Clermont-Ferrand et ne permettent pas de dire que toute la promesse est tenue ou non tenue.</p>
    <p><strong>Thèmes proposés</strong></p>
    <ul class="theme-list" aria-label="Thèmes de navigation proposés">
      <li>Éducation</li>
      <li>Cadre de vie et transition écologique</li>
    </ul>
    <details class="scope-details">
      <summary>Voir ce qui a changé entre la promesse et le programme</summary>
      <dl>
        <dt>Ce qui a été promis</dt>
        <dd>« {html.escape(commitment['wording'])} », sans nom de programme, nombre d’écoles, calendrier, budget ou couverture complète de la ville.</dd>
        <dt>Ce que prévoit ensuite le programme municipal</dt>
        <dd>« {html.escape(mapping['target_programme_name'])} » définit une transformation plus large : végétalisation, fraîcheur, perméabilité, inclusion et co-conception.</dd>
        <dt>Ce que nous pouvons comparer</dt>
        <dd>Les deux textes parlent des cours d’école de Clermont-Ferrand. Nous ne pouvons pas encore prouver que le programme est la mise en œuvre directe de la promesse, ni dire si son déploiement est plus ou moins important.</dd>
      </dl>
      <p><a href="../programmes/respire-a-la-recre/index.html#correspondance">Voir la comparaison complète et ses sources →</a></p>
    </details>
  </section>
"""


def render_education_html(passport: dict[str, Any]) -> str:
    metrics = dashboard_metrics(passport)
    counts = metrics["state_counts"]
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
  <section class="hero hero--compact" aria-labelledby="titre-education">
    <div>
      <p class="eyebrow">Tableau de bord thématique · Version de démonstration</p>
      <h1 id="titre-education" class="page-title">Éducation</h1>
      <p class="lede">Ce que nous savons aujourd’hui sur la végétalisation des cours d’école : la promesse, les décisions de la mairie, l’argent public et les travaux retrouvés.</p>
    </div>
    <div class="actions no-print"><a class="button" href="../programmes/respire-a-la-recre/index.html">Ouvrir le dossier complet</a><button class="button button--secondary" type="button" onclick="window.print()">Imprimer</button></div>
  </section>

  {render_commitment_brief(passport)}

  <div class="kpi-grid" aria-label="Indicateurs principaux du périmètre pilote">
    <div class="kpi kpi--primary"><span class="kpi__value">{metrics['school_units']}</span><span class="kpi__label">unités scolaires étudiées dans cette démonstration</span></div>
    <div class="kpi"><span class="kpi__value">{counts['reported_complete']}</span><span class="kpi__label">unités indiquées comme terminées par la mairie ; document administratif de fin non retrouvé</span></div>
    <div class="kpi"><span class="kpi__value">{_format_number_fr(metrics['reported_surface_m2'])}</span><span class="kpi__label">m² de sol rendus perméables d’après la mairie, pour quatre unités renseignées</span></div>
    <div class="kpi"><span class="kpi__value">{metrics['reported_trees']}</span><span class="kpi__label">arbres plantés d’après la mairie, pour quatre unités renseignées</span></div>
  </div>

  <div id="cas-documentes" class="section-heading"><div><p class="eyebrow">Écoles étudiées</p><h2>D’où viennent les trois états affichés ?</h2></div><p>Cliquez sur une partie du graphique pour retrouver les écoles concernées et les chiffres publiés par la mairie.</p></div>
  <section class="panel" aria-labelledby="cas-title">
    <h3 id="cas-title">Trois écoles · six unités scolaires · ce n’est pas toute la ville</h3>
    {render_observed_state_details(passport)}
  </section>

  <div id="filiation" class="section-heading"><div><p class="eyebrow">Du discours aux actes</p><h2>Le programme vient-il vraiment de la promesse ?</h2></div><p>Les dates montrent ce qui s’est passé dans quel ordre. Elles ne suffisent pas à prouver que le programme est entièrement nouveau ou qu’il vient directement de la promesse.</p></div>
  <section class="panel" aria-labelledby="timeline-title">
    <div class="theme-card__top"><h3 id="timeline-title">Le lien semble possible, mais il doit encore être vérifié</h3><span class="tag tag--pending">Vérification humaine requise</span></div>
    {render_policy_timeline(passport)}
  </section>

  <div id="finances" class="section-heading"><div><p class="eyebrow">Argent public</p><h2>Combien a été prévu et dépensé ?</h2></div><p>Les documents disponibles ne donnent pas encore le coût complet du programme. Nous montrons chaque montant séparément pour éviter de compter deux fois le même argent.</p></div>
  <section class="panel" aria-labelledby="finance-title">
    <h3 id="finance-title">Les montants retrouvés pour « Respire à la récré »</h3>
    {render_finance_table(passport)}
  </section>

  <div class="section-heading"><div><p class="eyebrow">Ce qui a été dit publiquement</p><h2>Campagne, communications de la mairie et presse</h2></div><p>Une déclaration permet de savoir ce qu’un candidat ou la mairie affirme. Pour prouver une décision, un paiement ou la fin de travaux, il faut aussi le document officiel correspondant.</p></div>
  <section class="panel" aria-labelledby="context-title">
    <h3 id="context-title">Les déclarations et articles déjà retrouvés</h3>
    {render_public_context(passport)}
  </section>

  <div class="section-heading"><div><p class="eyebrow">Ce qui peut changer le bilan</p><h2>Le projet a-t-il évolué ou rencontré des décisions contraires ?</h2></div><p>Nous devons montrer aussi clairement ce qui va contre la promesse que ce qui semble aller dans son sens. Quand la recherche n’est pas terminée, nous le disons.</p></div>
  <section class="panel" aria-labelledby="changes-title">
    <h3 id="changes-title">Les changements déjà visibles et ce qu’il reste à chercher</h3>
    {render_changes_and_counterevidence()}
  </section>

  <section class="panel notice" aria-labelledby="conclusion-education">
    <h2 id="conclusion-education">Ce que nous pouvons dire aujourd’hui</h2>
    <p>La mairie a lancé un programme, transformé certaines cours d’école et enregistré des dépenses. Mais les documents actuels ne suffisent pas pour dire si toute la promesse a été tenue, si le projet prolongeait une politique plus ancienne, ni quels effets il a eus sur les enfants et sur la ville.</p>
    <a href="../programmes/respire-a-la-recre/index.html">Examiner la méthode et les preuves →</a>
  </section>
</main>
"""
        + render_footer()
        + "\n</body>\n</html>\n"
    )
