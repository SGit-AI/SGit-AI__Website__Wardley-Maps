# 06 — Site Architecture

## The house pattern to follow

**Copy `pki.sgit.ai`.** It is the most complete site in the network — the only one carrying all six house markers — and it already hosts the doctrine work this site is taking over.

| Marker | sgit.ai | **pki** | nhi | sg-sentinel | graphs | riskmandate |
|---|:-:|:-:|:-:|:-:|:-:|:-:|
| `/llms.txt` | ✓ | **✓** | ✓ | ✓ | ✓ | ✓ |
| `/llms-full.txt` | ✓ | **✗** | ✗ | ✗ | ✓ | ✓ |
| `/documents/` | ✗ | **✓** | ✓ | ✓ | ✓ | ✗ |
| `/admin/comms.html` | ✗ | **✓** | ✓ | ✓ | ✓ | ✗ |
| `/admin/versions.html` | ✓ | **✓** | ✓ | ✓ | ✓ | ✗ |
| `/about/participant.html` | ✗ | **✓** | ✓ | ✗ | ✓ | ✗ |
| `/shipped/` | ✗ | **✓** | ✗ | ✗ | ✓ | ✗ |

Take pki's build pipeline too — `pki.sgit.ai/admin/index.html` documents it: hand-written static HTML with **programmatically injected chrome** (nav, footers, version badges) so it cannot drift; every push to `dev` runs link checking, version consistency, canonical-URL verification and **key-leak detection**, then auto-tags and deploys to GitHub Pages. Take its **raw-plus-curated split** (`/documents/` curated, `/briefs/` raw markdown). **Add the `/llms-full.txt` that pki lacks.**

Add one thing no sibling has: **a link-verification job**. Given §1 of `04__`, a site about an ecosystem whose own indexes are wrong should be the one that checks. Publish the run date.

---

## Page by page

### `/` — the front page
300 words, and none of them currently exist in the corpus. Open on the thesis — **maps are claims, not pictures** — then the three things this site has that others don't: the doctrine assessment, the PST-as-agent-teams pattern, and 34 verified resources. Close on the quotable line: *"Anybody who spends a lot of money on tokens has an engineering problem."* One rendered map above the fold — M1.

### `/doctrine/` — **build first**
The 41 records from `pki.sgit.ai/packs/registry-mvp/doctrine.html`, moved wholesale. Keep everything that makes it good: the four-phase grouping, the six categories, the click-to-filter, the distribution bar, the four-level scale (`strong` Practised · `partial` Partly · `weak` Not practised · `na` No basis yet), and above all the discipline that **every rating names the artefact it rests on**, so *"a reader who disagrees has the evidence in front of them."* Keep the self-assessment caveat too — it labels itself the weakest kind of assessment and compensates with evidence.

Serve `doctrine.json` as a stable endpoint (`id, cat, phase, name, what, status, us, evidence`). **There is no working doctrine assessment tool anywhere in the ecosystem right now.** A public JSON schema plus a worked example is the closest thing to one, and costs nothing extra.

Leave a stub on pki.sgit.ai pointing here.

### `/method/` — the opinionated core
Four pages, one per original contribution: **de-commoditisation**, **the custom-axis verdict** (with its rule — *relabel the axis when the thing genuinely evolves; use a maturity model when the thing merely improves*), **you cannot map a gap / the broken middle**, and **maps are graphs with position**. Each opens with the quote, states the claim, shows a map, and names what would falsify it.

### `/patterns/pst/` — the most original page
`02__` in full. Lead with the filesystem, not the theory. Include §4 (31 of 33 roles never got the memo) and §5 (asserted vs implemented) unsoftened. Cite `blog.gardeviance.org/2015/03/…` — **CC BY-SA 3.0**.

### `/resources/` — Job B
34 pages on the template in `04__` §2, plus `/resources/dead/` for the 11 dead-or-dying entries. Three start-here routes (newcomer / security / agent) as the primary navigation, the flat A–Z as secondary. Every page carries a dated verification stamp and the pre-written attribution string.

### `/dinis/` — Job A
The chronology from `03__`, 26 items, the 13 recordings embedded. Show the silences — 2021, 2023, and the 2026 gap where 194 unpublished files sit. Feature the 2020 *Team Topologies & PST* session as the documented ancestor of `/patterns/pst/`. Mirror the fragile items and say which are mirrors.

### `/maps/` — the gallery
The 8 PNGs, the 13 repaired Mermaid sources, the 8 converted position tables, and this pack's 4 SVGs. **Source next to render, every time** — *"the maps live in the source and are reviewable in a diff."* And a page for **the map that shows us badly**, when it is drawn.

### `/agents/` — the machine surface
The coordinate contract with the rendering proof (`05__` §2), the parse rules and the quote-everything rule (`05__` §3), the definitions endpoint for all 33 concepts, and the **epistemic guardrail** from `04__` §5 — placements are contestable claims, never findings. This is the surface the commission was really about.

### `/shipped/`
`00__` §5, unsoftened: 0 of 13 sources render, the evolution map died on 26 Feb 2026, no doctrine or gameplay analysis was ever produced inside `__Send`, maps-as-graphs is PROPOSED, 31 of 33 roles are silent.

### `/network/`
The seven-site map. And note that **four siblings mention Wardley zero times** and should link here:

- **`nhi.sgit.ai`** — strongest candidate. `graphs.sgit.ai` records four unrendered permissions maps including *"Hope Driven Development"*, but `nhi.sgit.ai/hope/` contains no maps at all. Its five-step framework — Enumerate, **Map**, Bound, Observe, Issue no credential — is asking for one.
- **`sg-sentinel.sgit.ai`** — zero mentions across 23 documents. Allowlist-vs-denylist is a natural map.
- **`riskmandate.ai`** — zero mentions. RAMM maturity is adjacent to doctrine.
- **`sgit.ai`** — has the maps, but `/network/` lists four sites and no mapping site. Needs a fifth entry.

### `/admin/`
`comms.html` with numbered asks (N1…) and tasks (T1…), `versions.html`. Per the house pattern, publish the build order **unresolved**, with `08__`'s open questions and tensions visible.

---

## What moves, what gets referenced, what stays

| Asset | Verdict |
|---|---|
| `pki.sgit.ai/packs/registry-mvp/doctrine.html` + `doctrine.json` | **MOVE** — with a stub |
| `pki.sgit.ai/packs/registry-mvp/wardley-maps.html` (6 maps) | **MOVE** |
| `pki.sgit.ai/packs/map-your-case/wardley-maps.html` (4 maps, M1–M4) | **MOVE** |
| `sgit.ai/demos/strategy-maps.html` (8 PNGs, vault-served) | **REFERENCE** — it is a live demo of the vault decryption mechanism; moving it breaks the demo |
| `sgit.ai/demos/sgit-maps.html` (6 inline SVGs) | **REFERENCE** |
| `graphs.sgit.ai/v1/maps/index.html` | **REFERENCE both ways** — it is the methodology-and-inventory page, and its unrendered backlog is ready-made launch content |
| Strategy Maps vault `ookq4mn4` (33 files, 830 KB) | **REFERENCE** — read key is published; there is no doctrine content in it |
| `docs.diniscruz.ai` MCP article | **STAY** — one passing clause; mirror the paragraph, link the original |

**Vault key discipline:** every key on the `sgit.ai` catalogue is an `sgit_rk1_` **read** key, published deliberately; no write keys were exposed anywhere in the survey. Keep it that way. Before linking any vault, confirm its write key is escrowed — publishing a read key for a vault whose write key is lost freezes it permanently.

---

This document is released under the Creative Commons Attribution 4.0 International licence (CC BY 4.0).
