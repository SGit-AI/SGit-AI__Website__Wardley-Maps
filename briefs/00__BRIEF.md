# 00 — The Brief: `wardley-maps.sgit.ai`

**Version** v0.33.62 · 23 August 2026
**From** Dinis Cruz, via the SG/Send Librarian
**To** the agent commissioned to build `wardley-maps.sgit.ai`
**Licence** CC BY 4.0 — but read `07__boundaries-and-licensing.md` before you copy anything, because this site sits inside a **CC BY-SA** ecosystem and that is the single biggest trap in the whole build

---

## 1. The commission

Three jobs, in the words they were given:

1. Consolidate **"what I have created on Wardley maps on the `__Send` site and the multiple `*.sgit.ai` sites"** — including *"one of them in addition to having a page and vault with maps, we even mapped the doctrines"*.
2. **Job A** — *"do a research on other materials (videos, infographics, docs) that I have published around wardley maps"*.
3. **Job B** — *"find the best industry resources about it, and per resource create a page with the details, screenshots and links to those resources"*.

All three are done. Jobs A and B are `03__` and `04__`. The consolidation is `01__`, `02__` and `05__`.

---

## 2. Two corrections to the premise, up front

**The doctrine mapping is not in a vault.** It is static HTML on `pki.sgit.ai`, at `/packs/registry-mvp/doctrine.html`, with its raw data at `/packs/registry-mvp/doctrine/doctrine.json` — **41 records: 15 strong, 11 partial, 6 weak, 9 no-basis**, across Wardley's 4 phases and 6 categories. `pki.sgit.ai/admin/index.html` states the site is *"not served from an sgit vault"*. The site that has a **page plus a vault** of maps is `sgit.ai` (the *Strategy Maps* vault, `ookq4mn4`, 33 files, 830 KB), and that vault has **no doctrine content at all**. So the thing remembered as one property is actually two, and the doctrine work is currently buried at appendix depth inside a PKI pack. **That single asset is the strongest reason to build this site**, and moving it is task one.

**There is no public bridge between the security-era Wardley work and the agentic-era Wardley work.** Job A found 26 published items running 2018→2025. Job A also found that the 2025–2026 agentic framing — the Explorer/Villager/Town Planner agent teams, de-commoditisation, the skill lifecycle — **has never been published anywhere**. The only public link between the two eras is one clause in one co-authored MCP article from June 2025. Do not write the site as though that bridge already exists in public. Building it *is* the site.

---

## 3. The thesis

> **Maps are claims, not pictures — and almost nobody publishes theirs where they can be argued with.**

The corpus already says this out loud: *"A Wardley map is a **claim**, not a picture: it asserts where each component sits on the evolution axis and is therefore arguable"* (14 Aug 2026). Everything the site does follows from taking that seriously — maps in git, coordinates in text, evidence attached to placements, and a doctrine assessment that names the artefact behind every rating.

There is a second, sharper thesis available, and the research supports it hard:

> **The Wardley ecosystem's link layer has rotted, and its own canonical indexes are now wrong.**

As of August 2026: **MapKeep is dead** (ceased 30 May 2026 — the only tool with real-time collaboration), **MapScript is dead**, **every doctrine assessment tool is dead**, the **Map Camp Slack invite 404s**, and the **Leading Edge Forum course 404s**. All five are still listed as live by `awesome-wardley-maps`, by Wikipedia, and in two cases by Simon Wardley's own resources page. Two Map Camp domains contradict each other about whether the conference still exists. A site that simply **verifies every link and publishes the verification date** is immediately more useful than the community's own index. That is a low bar and a real service.

---

## 4. What is original here — the five pages only this site can write

Ranked. These are the reason to build it rather than curate someone else's list.

| # | Page | The claim | Source |
|---|---|---|---|
| **1** | **Explorer / Villager / Town Planner as three literal agent teams** | Wardley's PST renamed and turned into three separate directory trees, three `CLAUDE.md` session contracts, and three evolution-stage mandates for AI agents. Nobody else has done this. See `02__`. | `.claude/CLAUDE.md`; founding brief 14 Feb 2026 |
| **2** | **De-commoditisation** | *"a thing can be commoditised at one phase of evolution while still being meaningfully custom-built at the next phase… I am going to call this pattern **de-commoditisation**"* — explicitly framed as a gap in doctrine | 17 May 2026, 2,947 w |
| **3** | **The custom-axis verdict** | *"the evolution scale doesn't necessarily need to be Genesis, custom-built, product and commodity; you can go from air gap to file to API to event-driven"* — and then the rule that settles it: ***"relabel the axis when the thing genuinely evolves; use a maturity model when the thing merely improves."*** With sources cited. The sharpest methodological contribution in the corpus. | 28 Jul 2026, 2,956 w |
| **4** | **The broken middle / you cannot map a gap** | *"**you cannot map a gap, because a gap has no evolution**"* and the resulting shape: *"the ends are solved. the middle is people."* An original map *shape*, not just an original map. | 28 Jul 2026 |
| **5** | **Maps are graphs with position** | *"**a Wardley Map is not a separate artifact from the graph. It is a graph with positional metadata.**… The graph is primary; the map is a projection… Map queries are graph queries with positional filters"* | 7 Feb 2026, 4,537 w |

Two more that carry a paragraph each, not a page: **the commodity illusion** (*"a lot of things that feel like a commodity or a product to the user are actually very weak and very immature behind the scenes"*) and **the agent as a user**.

And the most quotable line in the whole corpus, which belongs on the front page or nowhere:

> **"Anybody who spends a lot of money on tokens has an engineering problem. They are using explorer-type code and solutions in a commodity environment."** — 4 June 2026

---

## 5. The honesty constraint

Every sibling site publishes a `/shipped/` page separating what exists from what is designed. This site inherits it, and here it has real work to do, because the corpus over-promises in a specific and documentable way:

- **Zero of the 13 Mermaid map sources in the repo currently render.** Every one has the wrong code fence — bare ` ``` ` or ` ```wardley-beta ` instead of ` ```mermaid ` — and one `note` line is missing its required quotes. The **8 PNGs from 24 May are the only working visuals in the entire corpus.**
- **The living evolution map was abandoned on 26 February 2026** — six months stale, against the corpus's own warning that *"a map that was accurate three months ago and hasn't been updated is worse than no map."*
- **No doctrine assessment and no gameplay analysis was ever produced inside `__Send`**, despite both being specified as standing Cartographer responsibilities. (The one real doctrine assessment that exists is the pki.sgit.ai one — a different project.)
- **31 of 33 `ROLE.md` files never mention Wardley.** The Explorer Cartographer's own 2,057-word role definition — the role the founding brief called *"central to this entire structure"* — mentions Wardley **zero times**.
- **"Maps are graphs with position" has no implementation.** It is architecture; the reality doc lists it as PROPOSED.
- **No `.owm` files, no map JSON, no map SVG** existed in the corpus before this pack.

Say all of that plainly. The gap between the specification and the artefacts is itself an honest and interesting Wardley story — a map of the mapping practice would put most of it at Genesis.

---

## 6. What this pack ships that is new

Not just analysis — four working artefacts:

| Artefact | What it is |
|---|---|
| **`maps/` — 4 maps** | Original `wardley-beta` sources **and rendered SVGs**, produced in this session with Mermaid CLI 11.14.0 + the Playwright Chromium. M1 the tool ecosystem, M2 the two absences, M3 maps for agents, M4 the site's own value chain. These are the first rendered SVG Wardley maps in the estate. |
| **The coordinate proof** | The `[visibility, evolution]` rule was **verified empirically, not repeated**: `[0.90, 0.10]` renders top-left, `[0.10, 0.90]` bottom-right. Method and numbers in `05__`. |
| **The parse-rule finding** | The corpus knew hyphens broke names. This session established the **full rule and the fix**: `-`, `.` and `/` all break unquoted names; quoting fixes all three; **but the quotes must be used in the link lines too**. See `05__` §3. |
| **`screenshots/`** | `capture.js` + a 30-target `targets.json` carrying per-target **licence and attribution strings**. See §7 for why it is a script and not PNGs. |

---

## 7. Why the screenshots are a script, not a folder of PNGs

Job B asked for screenshots per resource. This pack ships the capture **kit** rather than the images, and the reason is worth stating plainly rather than hiding: the sandbox this pack was assembled in has an egress proxy that allows only package registries. Every third-party host returned `ERR_TUNNEL_CONNECTION_FAILED` — including `sgit.ai` itself. Nothing was captured, and I did not route around the block.

So `screenshots/capture.js` does the job wherever the network is open — `npm i playwright && node capture.js`. It writes `captured.json` recording the HTTP status, page title, final URL after redirects, and a UTC timestamp **for every attempt including the failures**. Publish that file next to the images. Given §3 — an ecosystem whose own indexes point at dead tools — a screenshot with a provable capture date is worth considerably more than a screenshot without one.

---

## 8. The numbers

| | |
|---|---|
| **Corpus** | 194 files in `__Send` mention Wardley · **33 concepts** catalogued · earliest 5 Feb 2026, latest 14 Aug 2026 |
| **Existing maps** | 8 rendered PNGs · 13 Mermaid sources (**0 render as-is**) · 9 ASCII maps · 8 position tables · **0 SVG, 0 `.owm`, 0 map JSON** |
| **Doctrine** | **41 records** on pki.sgit.ai — 15 strong, 11 partial, 6 weak, 9 no-basis |
| **Job A** | **26 published items**, 2018–2025 · 13 YouTube recordings, all live · **2 blog posts** (the complete Wardley label on his blog) · silent in 2021, 2023, and effectively 2025–26 |
| **Job B** | **34 industry resources** profiled · **11 dead or dying** · 4 licence regimes, **6 flagged as ambiguous** |
| **Network** | 4 Wardley pages + 1 vault across `sgit.ai`, `pki`, `graphs` · 4 sibling sites mention Wardley **zero times** |
| **This pack** | 9 documents · 4 original maps (source + SVG) · 30 screenshot targets · manifest of **73 rows** — 23 Tier-0, 37 Tier-1, 7 Tier-2, 6 do-not-publish; **98,008 words** of Tier-0+1 local source, every path verified at v0.33.62 |

---

## 9. Build order

1. **Move the doctrine assessment.** `/doctrine/` — the 41 records, the JSON endpoint, the phase filter, the evidence-per-rating discipline. Leave a stub on pki.sgit.ai. This is the site's anchor asset and it already exists.
2. **Fix the 13 broken map fences and render them.** Ship the SVGs. Use the pipeline in `05__` §4 — it is proven, and this pack's four maps are the proof.
3. **`/resources/` — Job B.** 34 pages from `04__` and `sources__industry-resources.json`. Run `capture.js` first so every page opens with a dated screenshot. Lead with the **verified-in-August-2026** angle.
4. **`/dinis/` — Job A.** The chronology from `03__`, embedding the 13 YouTube recordings. Then **archive the fragile ones** — the SlideShare deck is the only artefact of the Map Camp talk and it is behind a Cloudflare wall.
5. **`/patterns/pst/` — the Explorer/Villager/Town Planner write-up.** The site's most original page. `02__` is the raw material; it has never been written up as a pattern anywhere.
6. **`/method/`** — de-commoditisation, the custom-axis verdict, the broken middle, maps-as-graphs. Four opinionated pages.
7. **`/agents/`** — the machine surface: the coordinate contract, the parse rules, the definitions endpoint, and the epistemic guardrail from `04__` (an agent placing components on the evolution axis is generating consensus-shaped output; it must surface placements as contestable claims, never findings).
8. **`/shipped/`** — §5, in full, without softening.

Publish the open questions and the tensions unresolved, per the house pattern. `08__` supplies both.

---

This document is released under the Creative Commons Attribution 4.0 International licence (CC BY 4.0).
