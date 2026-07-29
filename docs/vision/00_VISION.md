# Project IAgora Vision

**Status:** Draft  
**Owner:** Maintainers  
**Last reviewed:** 2026-07-29

## Purpose

Project IAgora aims to turn fragmented public information into knowledge that people can understand, inspect, and verify.

Public records may be legally available while remaining difficult to find, connect, or interpret. IAgora should preserve those records, describe how information was acquired and transformed, and allow each material public claim to be traced to supporting or contradictory evidence.

## Intended users

IAgora is intended for:

- citizens seeking understandable accounts of public action;
- journalists and civil-society organizations investigating public decisions;
- researchers and students studying institutions and public policy;
- public administrations improving the accessibility of their own records;
- developers building evidence-aware civic tools.

## Intended outcomes

Users should be able to:

- connect campaign commitments to later public decisions, resources, delivery, and observed effects;
- scan a territory-level dashboard, identify a small number of primary indicators by policy theme, and drill down without losing definitions or caveats;
- understand which commitments are assessed as fulfilled, partially fulfilled, not fulfilled, changed, or not verifiable under a published method;
- distinguish what was announced, decided, funded, delivered, and measured;
- distinguish a new initiative from a continuation, extension, acceleration, reorientation, renaming, replacement, or indeterminate lineage when evidence permits;
- identify which institution and source is authoritative for a particular fact;
- inspect the evidence supporting or contradicting an assertion;
- understand relevant dates, territorial scope, uncertainty, and missing information;
- reproduce material calculations and transformations;
- print or export a territory, theme, indicator, programme, or commitment report from the same governed records;
- use AI-assisted explanations without treating model output as evidence.

IAgora should distinguish delivery from impact. Completing an announced action does not by itself demonstrate that the action caused the intended change in the city.

## Product position

IAgora is a verifiable civic knowledge platform. It is not only an open-data portal, document search engine, dashboard, or chatbot.

The intended public experience is a hosted interactive civic dashboard: a territory home presents a macro trajectory and thematic blocks, each theme exposes a limited number of primary indicators, and every summary can be explored through indicator, programme, commitment, evidence, and Knowledge Passport views. Printable reports are reproducible export views, not the product's only interface or a separate source of truth. The core remains reusable across territories even though the first deployment is bounded to Clermont-Ferrand.

The first proposed deployment focuses on Clermont-Ferrand, France. The canonical model must remain usable across territories and public institutions and must not adopt a portal-specific field as a shared domain definition.

## Boundaries

IAgora must not:

- monitor private citizens;
- infer political intent as fact;
- campaign, endorse candidates, or recommend political choices;
- predict elections;
- hide credible contradictory evidence;
- treat media coverage or generated content as authoritative when primary records exist;
- publish an opaque confidence, quality, trust, or completion score.

## Current decision status

This document is a draft restatement of the direction described in the repository `README.md` and `AGENTS.md`. The dashboard hierarchy is specified further in the draft [frontend architecture](../architecture/11_FRONTEND.md), while multidimensional accountability and policy lineage are governed by accepted [ADR-0010](../adr/ADR-0010-multidimensional-accountability-and-policy-lineage.md). No dashboard, macro indicator set, SaaS deployment, or report generator is implemented by this draft or the accepted decision alone.
