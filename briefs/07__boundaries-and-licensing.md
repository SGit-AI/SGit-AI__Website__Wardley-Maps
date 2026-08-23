# 07 — Boundaries, licensing and house style

This site has a licensing problem the other `*.sgit.ai` sites do not have, and it is worth getting right before the first page is written.

---

## 1. The CC BY / CC BY-SA collision

**The estate publishes CC BY 4.0. The Wardley ecosystem publishes CC BY-SA 4.0.** They are compatible for *reading* and incompatible for *adapting*.

ShareAlike is viral. Quote CC BY-SA material with attribution and nothing happens. **Adapt** it — rewrite, restructure, translate, build a derivative table from it — and the resulting page must itself be CC BY-SA 4.0. You cannot relicense someone else's adaptation as CC BY.

> **The rule for this site: CC BY-SA material appears as clearly-marked quotation and link-out, never as adaptation.** Then every page stays CC BY 4.0 and the network's licence stays uniform.

Where you genuinely want to adapt — a rewritten doctrine list, a restructured climatic-patterns table — do it on a **clearly-marked page carrying its own CC BY-SA 4.0 notice**, and say why at the top. One or two such pages are fine. A site with a mixed and unlabelled licence is not.

**Watch the 3.0/4.0 split.** Simon Wardley's book and most of the ecosystem are **CC BY-SA 4.0**. His blog `blog.gardeviance.org` is **CC BY-SA 3.0**. These are different licences with different notices. **Do not merge them into one footer.**

Standard attribution string, used across the ecosystem:

> *Wardley Mapping is provided courtesy of Simon Wardley, CC BY-SA 4.0.*

`sources__industry-resources.json` carries the correct string per resource; `screenshots/targets.json` carries the same strings attached to the capture targets so a screenshot and its credit can never drift apart.

---

## 2. What this site's own content is

Everything written for `wardley-maps.sgit.ai` — every page, `/documents/`, `/llms.txt`, `/llms-full.txt`, the admin surfaces, this pack, and the four maps in `maps/` — is **CC BY 4.0**, consistent with the rest of the network. Stamp every raw markdown document:

```
This document is released under the Creative Commons Attribution 4.0 International licence (CC BY 4.0).
```

Run `licence-audit.py` (shipped in the `graphs.sgit.ai` pack) in `--check` mode as a CI gate so the stamp cannot drift.

**The maps this pack ships are original works**, drawn from this pack's own research. They are CC BY 4.0 and carry no ShareAlike obligation. The *technique* they use is Wardley's and should be credited as such — crediting a technique is courtesy and good practice, not a licence condition.

---

## 3. Do not publish

From the `__Send` corpus. These are not judgement calls — each names commercial terms, a competitor, a customer, or a private individual.

| Path | Reason |
|---|---|
| `library/alchemist/materials/` — **the whole tree** | Investor-grade commercial material: pricing (£5/500 credits, £49–999/month), customer count, burn, TAM, a **named-competitor price table** (Intralinks, Datasite), founder CV, pitch decks, revenue and competitive-positioning models. None of it is needed for a Wardley site. |
| `team/town-planner/roles/librarian/reviews/02/21/v0.5.8__review__cbr-investment-catalogue.md` | Catalogues **a separate company's** private investment repository. Third-party commercial detail. |
| `team/town-planner/roles/alchemist/reviews/03/10/` — both files | Investor strategy and internal velocity metrics. |
| `…/07/17/commercial-model/v0.33.49__strategy-brief__sg-send-gen-ai-consulting-model…md` | Contract structure, hourly rates, response-time price ladder, delivery location. **Partial extraction allowed:** the explorer→villager handover section (~2 paragraphs) and the Simon Wardley source citation are publishable; the commercial model is not. |
| `…/06/23/wardley-maps/…first-pass-eight-maps…md` — **Map 8 only** | The competitive-landscape map attaches maturity judgements to living companies: *"NHI security (Astrix, …)"*, *"identity / PAM (Okta, CyberArk, Veza)"*, *"agent observability (LangSmith, …)"*. **Maps 1–7 and the cross-cutting reading are safe.** Redact Map 8 or generalise it to categories. |
| `…/06/08/v0.33.2__research-brief__sg-send-tls-ssl-cybersecurity-skills-landscape.md` | Names a **private individual** as a commercial target. The Wardley task inside it (Research Task 9) is safe in isolation; the surrounding brief is not. |
| `…/06/10/integration-landscape/…mappings-implementation-cost-criteria.md` | Vendor-by-vendor cost and disposition scoring. **The idea of a vendor evolution view is publishable; the scored table is not.** |
| `…/05/26/v0.27.64__strategy-brief__sg-send-security-report-vault-demo-pentest.md` | Pentest material. Only 4 Wardley mentions; not worth the risk. |
| `…/07/31/markets-and-field-demo/…somebody-has-to-be-the-villagers…md` | **Publishable with care.** The Wardley/NFR argument is strong and belongs on the site. But the *"one in five strategic dealmakers walked away"* M&A figure and seven market statistics are loosely attributed (*"reported"*, *"is cited as finding"*), and the brief itself flags that *"much of what circulates is vendor commentary recycling a smaller set of underlying studies."* Re-source or soften. |

Everything else in Tiers 0–1 of the manifest is clean, and most already carries the CC BY 4.0 stamp.

---

## 4. Third-party names — the line

**Fine:** naming a technique, a framework, a standard, or a tool. Naming Simon Wardley, Ben Mosior, Chris Daniel, Matt Edgar, Danny Buerkli, John Grant, Tristan Slominski and the other practitioners in `04__` — they are public authors of public work, credited for it.

**Fine:** saying MapKeep shut down on 30 May 2026 and crediting Tristan Slominski for building it. That is a factual, sourced obituary and the community needs it recorded.

**Not fine:** attaching maturity or capability judgements to named commercial competitors (Map 8), reproducing a vendor cost-scoring table, or naming a private individual as a commercial target.

**Never:** quoting Discord or forum members without consent. Those are personal messages regardless of technical accessibility.

---

## 5. Screenshot ethics

`capture.js` screenshots pages. Three rules:

1. **A page screenshot for identification is defensible almost everywhere**, including ARR material — it is how a directory works. **Clipping content out of a page is not.** Never reproduce Xebia's diagrams, InfoQ's video frames, or GCATI's syllabus.
2. **The attribution string travels with the image.** It is pre-written per target in `targets.json`. Render it under the image, not in a global footer.
3. **Publish `captured.json`.** Status, title, final URL, timestamp — for successes and failures alike. In an ecosystem where the canonical indexes point at dead tools, a screenshot without a provable date is worth much less than one with.

---

## 6. Network boundaries

| Site | Owns | This site defers on |
|---|---|---|
| **`wardley-maps.sgit.ai`** | Mapping technique, doctrine, the PST pattern, the resource index, Dinis's mapping history | — |
| `graphs.sgit.ai` | Graph theory, meaning through connectivity, G³, maps-*as*-graphs rendering methodology | **Cross-link, don't duplicate.** Its `/v1/maps/` page is the methodology-and-inventory surface; this site is the technique surface. |
| `pki.sgit.ai` | PKI, the registry MVP | Keeps the pack context; the doctrine page and both map pages move here with stubs |
| `risks.sgit.ai` | Risk concepts, acceptance, the grounding ladder | Risk-as-an-evolution-axis is a shared idea — one link each way |
| `nhi.sgit.ai`, `sg-sentinel.sgit.ai` | Non-human identity, sentinel | Should link *here*; currently mention Wardley zero times |
| `riskmandate.ai` | Commercial | References, is not referenced |
| `sgit.ai` | The vault product, the demos | Hosts the Strategy Maps vault and the two live demo pages; those stay |

---

## 7. House style

- **`-ise`, not `-ize`**, throughout. The corpus mixes them freely; the site must not. One glossary line noting they are the same word.
- **Explorer / Villager / Town Planner** for the agent teams, always paired with Wardley's originals on first use. *Settler* appears once in the entire corpus — do not adopt it.
- **Quote generously and attribute exactly.** The corpus's best lines are better than any paraphrase of them, and quotation is the licence-safe move anyway.
- **Every map ships its source.** No rendered image without the `.mmd` next to it.
- **Every resource page carries a verification date.** No exceptions — it is the site's entire differentiator in that category.
- **Name what would falsify a claim.** A map is a claim; a page asserting one should say what evidence would change it.

---

This document is released under the Creative Commons Attribution 4.0 International licence (CC BY 4.0).
