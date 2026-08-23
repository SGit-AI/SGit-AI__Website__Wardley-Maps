# wardley-maps.sgit.ai — brief pack

**For:** the agent commissioned to build `wardley-maps.sgit.ai`
**From:** Dinis Cruz, via the SG/Send Librarian
**Version:** v0.33.62 · 23 August 2026
**Licence:** CC BY 4.0 — **read `LICENSE.md` before copying anything.** This site sits inside a CC BY-SA ecosystem and that collision is the biggest trap in the build.

---

## What this is

A research site for Wardley Mapping, consolidating **194 files of unpublished mapping thinking** in the `__Send` corpus with **26 published items** spanning 2018–2025 and **34 industry resources** verified in August 2026.

Three jobs were commissioned and all three are here:

1. **Consolidate** what exists across `__Send` and the `*.sgit.ai` network — `01__`, `02__`, `05__`, `06__`
2. **Job A** — research Dinis's own published Wardley material — `03__`
3. **Job B** — the best industry resources, a page each, with details, screenshots and links — `04__`

---

## Read in this order

| File | Words | What it does |
|---|---:|---|
| **`00__BRIEF.md`** | 2.0k | **Start here.** The commission, two corrections to the premise, the thesis, the five original pages, the honesty constraint, the numbers, the build order |
| **`02__pioneers-settlers-town-planners.md`** | 1.6k | **The page only this site can write** — Wardley's PST as three literal AI agent teams. Never written up anywhere |
| `04__job-b__industry-resources.md` | 1.8k | Job B: the per-resource page template, the ranked top ten, the licence minefield, three start-here paths |
| `03__job-a__dinis-published-material.md` | 1.5k | Job A: 26 items, the seven-year through-line, and what to archive before it disappears |
| `05__maps-and-rendering.md` | 1.5k | The maps that exist, the coordinate contract **proven by rendering**, the parse rules, the working pipeline |
| `01__concepts-index.md` | 2.8k | 33 concepts with canonical paths and dates, classified standard / extension / **original**, plus a six-altitude teaching order |
| `06__site-architecture.md` | 1.1k | Page-by-page IA, the house pattern to copy, what moves vs what gets referenced |
| `07__boundaries-and-licensing.md` | 1.3k | The CC BY / CC BY-SA collision, the do-not-publish list, screenshot ethics, house style |
| `08__gaps-and-open-questions.md` | 1.4k | 7 write-fresh items, 8 commissioned-but-never-made artefacts, 8 open questions, 7 honest tensions |
| `09__source-manifest.csv` | 73 rows | Every source, tiered 0–3, with proposed page and publishability. **Every path verified at v0.33.62** |
| `sources__dinis-wardley-published.json` | 26 items | Job A data — dates with precision flags, video URLs, verification flags |
| `sources__industry-resources.json` | 34 + 11 | Job B data — licence and **pre-written attribution string** per resource, plus 11 dead-or-dying entries |
| `maps/` | 4 maps | Original `wardley-beta` sources **and rendered SVGs**. The estate's first rendered SVG maps |
| `screenshots/` | script | `capture.js` + 30 targets carrying licence and attribution strings |
| `LICENSE.md` | — | CC BY 4.0, and the four regimes it does not cover |

---

## The four things that will bite you

**1. This site is CC BY inside a CC BY-SA ecosystem.** Quoting Simon Wardley's material is fine. *Adapting* it forces that page to be CC BY-SA 4.0. Keep everything as marked quotation and link-out. And note his blog is **3.0**, not 4.0 — different licence, different notice.

**2. Nothing renders.** All 13 Mermaid map sources in the repo fail, for two mundane reasons (wrong code fence, one unquoted `note`). The 8 PNGs from 24 May are the only working visuals in the corpus. Fixing this is a day-one task and turns 13 dead code blocks into 13 maps.

**3. The doctrine mapping is not in a vault** — it is static HTML at `pki.sgit.ai/packs/registry-mvp/doctrine.html`, 41 records, and it is the site's anchor asset. The vault with maps is a *different* property (`sgit.ai`, Strategy Maps) and has no doctrine content. Moving the doctrine page is build-order step 1.

**4. There is no public bridge between the security-era and agentic-era work.** Job A found 26 published items ending in 2025 and 194 unpublished files starting in 2026, connected by **one clause in one co-authored article**. Do not write the site as though the connection already exists in public. Building it is the commission.

---

## About the screenshots

Job B asked for screenshots. This pack ships the capture **kit**, not the images, and the reason is stated rather than hidden: the sandbox this pack was built in has an egress proxy that allows only package registries. Every third-party host returned `ERR_TUNNEL_CONNECTION_FAILED` — including `sgit.ai` itself. **Nothing was captured and nothing was routed around.**

`screenshots/capture.js` does the job wherever the network is open:

```bash
cd screenshots
npm i playwright && npx playwright install chromium
node capture.js              # all 30 targets
node capture.js 04 07 13     # a subset, by id prefix
```

It writes `captured.json` recording HTTP status, page title, final URL after redirects, and a UTC timestamp for **every attempt including failures**. Publish that file. In an ecosystem whose own canonical indexes point at five dead tools, a screenshot with a provable capture date is the whole point.

---

## About the maps

Four original maps in `maps/`, source and rendered SVG, produced with Mermaid CLI 11.14.0 and the Playwright Chromium. They are drawn about the site's own subject matter so they can go straight onto pages: the tool ecosystem, the two absences (MapKeep and the doctrine tools), maps for agents, and the site as a value chain.

**They are claims, not decorations.** Publish the `.mmd` next to the `.svg` so a reader can fork the argument in a pull request — which is `pki.sgit.ai`'s own standard: *"the maps live in the source and are reviewable in a diff."*

Two findings came out of making them, both in `05__`: the `[visibility, evolution]` coordinate order **verified by rendering rather than repeated**, and the complete `wardley-beta` name-parsing rule — `-`, `.` and `/` all break unquoted names, quoting fixes all three, **and the quotes must be used in the link lines too**.

---

## House pattern

Copy `pki.sgit.ai` — it is the only site in the network with all six house markers, and it already hosts the doctrine work. `/llms.txt` as the whole agent surface; `/documents/` with raw markdown as source of truth; `/admin/comms.html` numbering asks (N1…) and tasks (T1…); `/admin/versions.html`; `/about/participant.html`; `/shipped/` separating what exists from what is designed. Add the `/llms-full.txt` pki lacks, and add one thing no sibling has: **a link-verification job that publishes its run date**.

Publish the build order unresolved, with the open questions and honest tensions visible. `08__` supplies both.

---

This file is released under the Creative Commons Attribution 4.0 International licence (CC BY 4.0).
