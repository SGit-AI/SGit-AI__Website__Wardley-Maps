# Licence

## This pack

Everything in this brief pack — the nine numbered documents, `09__source-manifest.csv`, both `sources__*.json` files, the four maps in `maps/` (both `.mmd` source and rendered `.svg`), `screenshots/capture.js`, `screenshots/targets.json`, this file and `README.md` — is released under the **Creative Commons Attribution 4.0 International licence (CC BY 4.0)**.

    Copyright (c) 2026 Dinis Cruz
    Licensed under CC BY 4.0 — https://creativecommons.org/licenses/by/4.0/

Attribution: **Dinis Cruz**, with AI co-authorship (Claude, Anthropic). Where a source document names model co-authors, carry those names forward.

The four maps are **original works**, drawn from this pack's own research. They carry no ShareAlike obligation. The *technique* they use is Simon Wardley's and is credited as such — crediting a technique is good practice, not a licence condition.

## The site this pack commissions

**The entire content of `wardley-maps.sgit.ai`** — every page, `/documents/`, `/llms.txt`, `/llms-full.txt` and the admin surfaces — is to be published under **CC BY 4.0**, consistent with the rest of the `*.sgit.ai` network. Put the licence in `/llms.txt`, in the page footer, and at the foot of every raw markdown document:

    This document is released under the Creative Commons Attribution 4.0 International licence (CC BY 4.0).

Use `licence-audit.py` (shipped in the `graphs.sgit.ai` pack) in `--check` mode as a CI gate so the stamp cannot drift.

---

## ⚠️ The one that matters: CC BY vs CC BY-SA

**This site sits inside a CC BY-SA ecosystem.** That is the single biggest licensing trap in the build, and it does not apply to any other site in the network.

ShareAlike is viral. **Quoting** CC BY-SA material with attribution is fine. **Adapting** it — rewriting, restructuring, translating, building a derivative table from it — obliges you to license the resulting page CC BY-SA 4.0, not CC BY 4.0.

> **The rule: CC BY-SA material appears as clearly-marked quotation and link-out, never as adaptation.** Then every page stays CC BY 4.0 and the network's licence stays uniform. Where you genuinely want to adapt, do it on a page carrying its own CC BY-SA 4.0 notice and say why at the top.

Standard attribution string, used across the ecosystem:

> *Wardley Mapping is provided courtesy of Simon Wardley, CC BY-SA 4.0.*

**Watch the version split.** The book and most of the ecosystem are **CC BY-SA 4.0**. Simon Wardley's blog `blog.gardeviance.org` is **CC BY-SA 3.0**. Different licences, different notices — do not merge them into one footer.

---

## What this licence does not cover

| Material | Regime | What the site must do |
|---|---|---|
| **Simon Wardley's book, Learn Wardley Mapping's free reference, the Mapping Canvas, wardleymaps.com, Wikipedia** | **CC BY-SA 4.0** | Quote and screenshot with the attribution string. Do not adapt. |
| **`blog.gardeviance.org`** | **CC BY-SA 3.0** ⚠️ | Same, with a *separate* 3.0 notice. |
| **awesome-wardley-maps** | **CC0 1.0** | Anything, no attribution required. The best base for your own list — and it lists five dead things as live, so correct it while crediting it. |
| **OWM, Mermaid, wardleyToGo, cli-owm, ArcKit** | **MIT** | Retain the notice. Technique credit to Wardley is separate. |
| **Obsidian plugin, Tranquil's Map** | **AGPL-3.0** ⚠️ | Network clause — matters if you ever embed one in a service. |
| **The 8 prior-art articles on `docs.diniscruz.ai`** | **CC0 1.0** | More permissive than CC BY, so republishing is fine — but attribute anyway and keep `rel="canonical"` on the original URL with the recorded `first_published` date. |
| **InfoQ, YouTube, GCATI, Xebia, LWM's paid course, Hudson's and Bell/Thorpe's books** | **All rights reserved** | Brief quotation and a page screenshot for identification. **No re-hosting, no clipping, no reproducing their diagrams.** |
| **Vault contents** at `sgit.ai/demos/vaults/` | Per-vault; read keys publishable, **write keys never** | Confirm the write key is escrowed before linking. Publishing a read key for a vault whose write key is lost freezes it permanently. |
| **Tier-3 rows in the manifest** (6 rows) | Internal | **Do not publish, quote or paraphrase.** Listed so you know to skip them. |
| **Tier-2 rows** (7 rows) | Partial | Marked `EXTRACT ONLY` / `IDEA ONLY` / `CARE` / `ARCHIVE FIRST`. Read the `why_it_matters` column before touching them. |

## 🚩 Six flagged — link only until resolved

- **`swardley/WARDLEY-MAP-REPOSITORY`** — README says CC BY-SA, GitHub licence field says **GPL-3.0**. **Do not mirror.** 147 maps are worth one email to resolve.
- **WardleyPedia** — no licence stated. Do not assume the MediaWiki default.
- **Matt Edgar's critique** — no statement, assume ARR. Highest-value critique, least clear rights.
- **Open Security Summit session pages** — no licence stated, including Dinis's own sessions.
- **Miro / Figma / draw.io templates** — mostly unstated, varying. Check per template.
- **Discord and forum content** — personal messages. Never quote a member without consent.

## Third-party names

Naming a technique, framework, standard, tool or public author is fine — Simon Wardley, Ben Mosior, Chris Daniel, Matt Edgar, Danny Buerkli, Tristan Slominski and the others in `04__` are credited for public work. Recording that MapKeep shut down on 30 May 2026 and crediting Slominski for building it is a factual obituary the community needs.

Attaching maturity or capability judgements to **named commercial competitors** is not fine — that is why Map 8 of the eight-maps brief is marked REDACT and why the whole `library/alchemist/materials/` tree is Tier-3.

---

This file is released under the Creative Commons Attribution 4.0 International licence (CC BY 4.0).
