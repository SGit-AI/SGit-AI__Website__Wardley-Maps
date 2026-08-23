# 04 — Job B: the industry resources, and how to build a page for each

> *"find the best industry resources about it, and per resource create a page with the details, screenshots and links to those resources"*

**34 resources profiled + 11 dead-or-dying entries.** All structured data is in `sources__industry-resources.json` — category, URL, type, maintainer, start date, **status as of August 2026**, **licence**, what it is, why it matters, limitations, best link, screenshot target, and the **exact attribution string** to use.

`screenshots/targets.json` carries 30 capture targets with the same licence and attribution strings attached, so the screenshot and its credit line can never drift apart.

---

## 1. The angle that makes these pages worth writing

Not "here are some links." **"Here is every link, verified on a stated date, with what is actually dead."**

The community's own canonical indexes are wrong in August 2026:

| Dead thing | Still listed as live by |
|---|---|
| **MapKeep** (ceased 30 May 2026 — the only real-time collaborative tool) | awesome-wardley-maps · Wikipedia · **Simon Wardley's own resources page** |
| **MapScript** | awesome-wardley-maps · Wikipedia |
| **Every doctrine assessment tool** (`doctrine.wardleymaps.com` + Stach's) | awesome-wardley-maps |
| **The Map Camp Slack invite** (404) | awesome-wardley-maps · `map-camp.com/_pages/slack/` |
| **The Leading Edge Forum course** (404) | awesome-wardley-maps · Courses section |

And two Map Camp domains actively contradict each other: **`map-camp.com`** stops at Sept 2024 and advertises the dead Slack invite; **`mapcamp.co.uk`** carries the current position — Map Camp 2027 and a workshop on **12 November 2026**. A visitor landing on the `.com` will reasonably conclude the conference is dead. **Always link `mapcamp.co.uk`.**

Every resource page should therefore carry a **verification stamp** — `Verified 2026-08-23 · HTTP 200 · captured.json` — sourced from the file `capture.js` writes. That single design decision is the site's whole competitive position in this category.

**One live opportunity falls straight out of this:** there is currently **no working doctrine assessment tool anywhere in the ecosystem**, and `pki.sgit.ai` has a working 41-record doctrine assessment sitting inside a PKI pack. Moving it here (build order step 1) fills a real, named gap.

---

## 2. The page template

Every resource page uses this shape. Nine fields, all of them already in the JSON.

```
/resources/<slug>/

  <Name>                                  [category badge] [status badge]
  ─────────────────────────────────────────────────────────────────────
  [screenshot — screenshots/<id>.png, with the capture date beneath it]

  What it is           4–6 sentences of substance, not a paraphrase of the title
  Why it matters       what it is uniquely best for
  Limitations          stated plainly; a page with no limitations section is marketing
  Maintainer           person or org, and whether they are still active
  Started              first published
  Status               Aug 2026: actively maintained / dormant / archived / DEAD
  Licence              exact, and what it permits — see §4
  Best single link     the one URL to send someone
  ─────────────────────────────────────────────────────────────────────
  Verified 2026-08-23 · HTTP 200 · <attribution string>
```

**Two rules for the template.** The status badge is not decoration — it is the reason to visit. And the **attribution string is not optional** for anything CC BY-SA: it is a licence condition, and it is pre-written per resource in the JSON so nobody has to guess.

---

## 3. Ranked top ten

If a reader looks at ten things, these ten, in this order:

1. **Wardley Maps, Ch.1 — On Being Lost** — `medium.com/wardleymaps/on-being-lost-2ef5f05eb1ec`. The primary source, and the chapter that establishes *why* before *how*. The CC BY-SA 4.0 licence on it is what makes the whole ecosystem exist.
2. **Learn Wardley Mapping** — `learnwardleymapping.com`. The pedagogy the book lacks. Ben Mosior / Hired Thought. The free reference alone, especially the four-phase doctrine grid, is the fastest route from confusion to competence.
3. **Crossing the River by Feeling the Stones** — `infoq.com/presentations/stuational-awareness/`. 48 free minutes of Wardley doing the thing. The highest-conversion artefact in the list.
4. **OnlineWardleyMaps + its DSL reference** — `docs.onlinewardleymaps.com/docs/dsl-reference/`. You do not understand mapping until you have drawn one. Also the format standard the whole ecosystem targets. MIT.
5. **awesome-wardley-maps** — `list.wardleymaps.com`. The community index, and **the only major resource under CC0** — so also the only one you can freely reuse as a base. (Rank it here for discovery, and correct its five dead entries on your own page.)
6. **Wardley Mapping 101** — `wardleymaps.com/guides/wardley-mapping-101`. The best free 15-minute end-to-end worked example, one sustained case study.
7. **What do Wardley maps really map? A settler writes** — Matt Edgar, 2017. **Read the strongest objection early**, before over-committing. The consensus-vs-evolution argument will change how you use the technique.
8. **Wardley Maps in Mermaid (`wardley-beta`)** — `mermaid.js.org/syntax/wardley.html`. The most consequential recent development: maps in git, in pull requests, in documentation, with no tool. See `05__`.
9. **Simon Wardley's map repository** — `github.com/swardley/WARDLEY-MAP-REPOSITORY`, best browsed via the rendered Mermaid mirror. **147 real maps across 22 industries.** Twenty of these teach more than two more chapters. ⚠️ licence flagged — link, do not mirror.
10. **Where the map ends** — Danny Buerkli. The four structural limitations, stated fairly. The thing that stops mapping becoming a religion.

---

## 4. The licence problem — read this before copying anything

**The Wardley ecosystem is CC BY-SA. This site is CC BY. Those do not mix cleanly.**

ShareAlike is viral: publish an **adaptation** of CC BY-SA material and that page must itself be CC BY-SA 4.0, not CC BY 4.0. Quoting and linking are fine; adapting is what binds you.

> **The practical rule for the whole site: keep CC BY-SA material as clearly-marked quotation and link-out, never as adaptation.** Then every page stays CC BY 4.0 and the estate's licence stays uniform. `07__` has the full treatment.

Four regimes, and six things flagged:

| Regime | Examples | What you may do |
|---|---|---|
| **CC0** | awesome-wardley-maps | Anything. No attribution required. The best base for your own list. |
| **CC BY-SA 4.0** | the book, all compiled editions, Learn Wardley Mapping's free reference, the Mapping Canvas, wardleymaps.com, Wikipedia | Quote and screenshot with attribution. **Adapt only if you accept CC BY-SA on that page.** |
| **CC BY-SA 3.0** ⚠️ | `blog.gardeviance.org` — Simon's blog | **Not 4.0. Keep the notice separate; do not merge the two.** |
| **MIT / AGPL** | OWM, Mermaid, wardleyToGo, cli-owm, ArcKit (MIT) · Obsidian plugin, Tranquil's Map (**AGPL-3.0 — network clause**) | Retain the notice. AGPL's network clause matters if you ever embed one in a service. |
| **All rights reserved** | LWM's paid course, InfoQ, YouTube, GCATI, Hudson's book, The Value Flywheel Effect, Xebia | Brief quotation and a page screenshot for identification. **No re-hosting, no clipping, no reproducing their diagrams.** |

**🚩 Six flagged — link only until resolved:**

- **`swardley/WARDLEY-MAP-REPOSITORY`** — README says CC BY-SA, the GitHub licence field says **GPL-3.0**. Contradictory. **Do not mirror.** (Craddock's mirror splits it: content CC BY-SA 4.0, code GPL-3.0.)
- **WardleyPedia** — no licence stated. Do not assume the MediaWiki default.
- **Matt Edgar's critique** — no statement, assume ARR. **The highest-value critique with the least clear rights.** Quote briefly, link out.
- **Open Security Summit session pages** — no licence stated, and this includes Dinis's own sessions.
- **Miro / Figma / draw.io templates** — mostly unstated and varying. Assume nothing; check per template.
- **Discord and forum content** — personal messages. **Never quote a member without consent.**

---

## 5. Three "start here" paths

The site should ship these as three routes through `/resources/`, not one list.

**Newcomer** → Wardley Mapping 101 (15 min) → *Crossing the River* (48 min) → **draw one** in OnlineWardleyMaps using the Mapping Canvas as process, mapping *something you already understand deeply — not your company* → LWM's free reference → the doctrine grid, self-assessed against Phase 1 → book chapters 1–6 → **the Edgar critique, before you evangelise** → Discord via mapcamp.co.uk, and **12 Nov 2026** in the diary.

**Security practitioner** → Wardley Mapping 101 (don't skip it because you're senior) → **Xebia's threat-modelling method** (map first, mark team boundaries as bias hotspots, ask what can be *deleted*, then STRIDE the areas the map flagged) → the OSS *Threat Models and Wardley Maps* session → Mario Platt's SABSA webinar → ***Where the map ends*, which matters most for you**: two of its four limitations are directly disabling in security — components only evolve under competitive pressure (much of internal security faces none), and you cannot map what you cannot see (which is definitionally the threat that gets you) → doctrine Phase 1, which reads as a security maturity model with the serial numbers filed off → put maps in git with Mermaid so they sit next to ADRs and get reviewed in PRs.

**An agent** → this is `/agents/`, and it is the path the site is uniquely placed to write:

1. **Grammar first.** The OWM DSL reference and the Mermaid syntax page. The error-prone fact: coordinates are **`[visibility, evolution]`**, not `[x, y]`. `05__` §2 proves it by rendering rather than asserting it.
2. **Semantics.** A map has four constituents — anchor, position, type, evolution — and evolution is measured by **ubiquity vs certainty**, *not* by time or adoption curve. **Do not use diffusion-curve reasoning.**
3. **Ground truth.** The 147-map repository, ~4,905 components, ~5,172 links, 22 sectors. The Mermaid mirror provides paired OWM/Mermaid representations with verified 1:1 fidelity — an excellent format-translation training pair.
4. **Don't reinvent ArcKit.** MIT, actively maintained. Note its decomposition into `wardley.value-chain`, `wardley.doctrine`, `wardley.gameplay`, `wardley.climate` rather than one monolithic "make a map" action. Mirror that decomposition.
5. **Deterministic rendering** — `cli-owm` (stdin→SVG, real OWM parser) or `wardleyToGo` — so the output is verifiable rather than merely plausible.
6. **The epistemic guardrail, and it is mandatory.** The evolution axis plausibly encodes **consensus, not objective fact**. An LLM placing components on it is generating consensus-shaped output with no underlying evidence — Edgar's *"laundering assumptions into facts"*, at scale and at speed. **An agent must surface its evolution placements as explicitly contestable claims requiring human challenge, never as findings.**

That last point is not a caveat to bury in a footer. It is the most important sentence on the `/agents/` page, and it rhymes exactly with the corpus's own position — *"a map is a claim, not a picture"* — and with the doctrine assessment's discipline of naming the artefact behind every rating.

---

## 6. Ecosystem health, in one paragraph

Worth saying on the front page, because it is not what the dead links suggest. **The technique is healthy and arguably in an upswing**: Map Camp is returning after a two-year gap, Mermaid support has made maps native to git, OnlineWardleyMaps got a full rewrite in 2025, ArcKit is bringing mapping into agentic workflows with real adoption (2,000+ installs), and the VS Code extension shows ~4,856 installs. What has rotted is the **link layer**, not the practice. Which is a fixable problem, and fixing it is a good reason for this site to exist.

---

This document is released under the Creative Commons Attribution 4.0 International licence (CC BY 4.0).
