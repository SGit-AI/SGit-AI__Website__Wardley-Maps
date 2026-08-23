# 05 — Maps, rendering, and two things this session established by testing

Everything here was verified by rendering, not by reading documentation. Where the corpus already knew something, that is said; where this session extended it, that is said too.

---

## 1. What maps exist today

| Form | Count | Where | Renders? |
|---|---:|---|---|
| **Rendered PNGs** | **8** | `…/briefs/05/24/sg-send-thread/wardley-maps/` — all `784 x 523, 8-bit/color RGB` | **Yes.** The only working visuals in the entire corpus. |
| **Mermaid `wardley-beta` sources** | **13** | 8 in `…wardley-maps-rendered.md`, 1 in `…setup-and-mermaid-capability.md`, 4 in `…productizing-commoditizing-permissions…md` | **No — all 13 fail.** See §5. |
| **ASCII maps** | **9** | across the cartographer reviews, the founding brief, the primer, the air-gap brief, the skill-lifecycle brief | Yes, in monospace |
| **Position tables as maps** | **8** | `…first-pass-eight-maps-user-needs-before-after.md` — `Component / Visibility / Today / With our service` | Unrendered, but **the most analytically dense maps in the corpus** and trivially convertible |
| **`.owm` files, map JSON, map SVG** | **0** | — | OWM interchange is specified in the Cartographer REFERENCE and never implemented |

Plus, live on the network: **8 PNGs** served from the `sgit.ai` Strategy Maps vault (client-side decrypted, a `MutationObserver` rewrites vault-path image refs to blob URLs), **6 inline SVGs** generated client-side on `sgit.ai/demos/sgit-maps.html`, and **10 Mermaid maps** across two `pki.sgit.ai` packs — the estate's first use of `wardley-beta` in published HTML.

**This pack adds the first rendered SVG Wardley maps in the estate: `maps/`, four of them, source and output.**

---

## 2. The coordinate contract — proven, not asserted

`graphs.sgit.ai` warns that coordinates are `[visibility, evolution]`, not `[x, y]`, and that transposing them *"renders without error while asserting a different claim"*. The corpus says the same (W13, 24 May 2026). **This session tested it.**

Probe rendered with Mermaid CLI 11.14.0, plot area x∈[48,852], y∈[48,552], y growing downward:

```
anchor    "A_high_vis_genesis"    [0.90, 0.10]   -->  drawn at x≈128, y≈95
component "B_low_vis_commodity"   [0.10, 0.90]   -->  drawn at x≈780, y≈494
```

`0.90` put the first component **near the top** (high visibility) and `0.10` put it **near the left** (genesis). Confirmed:

> **First number = visibility → the Y axis, 1 = top, visible to the user.
> Second number = evolution → the X axis, 1 = right, commodity.**

There is no error and no warning if you transpose them. The map renders, looks plausible, and says something else. **This is the single highest-value fact on the `/agents/` page**, and the site should state it with this evidence rather than as received wisdom.

---

## 3. The parse rules — the corpus was right, and incomplete

The corpus records (W13b, 24 May 2026) that *"component and anchor names that contain a hyphen, an ampersand, or a slash cause a parse error"*, and recommends *"keep component and anchor names to letters and spaces"*.

That is correct but avoidable. This session established the full rule and the fix, by bisection on Mermaid **11.14.0**:

| In an **unquoted** name | Result |
|---|---|
| spaces (`Draw a map`) | **OK** |
| underscores (`Real_time`) | **OK** |
| parentheses (`Draw (fast)`) | **OK** |
| **hyphen** (`Real-time collab`) | **FAILS** |
| **dot** (`doctrine.wardleymaps.com`) | **FAILS** |
| **slash** (`AI/ML`) | **FAILS** |

**The fix is quoting** — `component "Real-time collab" [0.7, 0.6]` parses fine, and so does `"doctrine.wardleymaps.com"`. But there is a trap:

> **Quoting the declaration and not the link still fails.** `component "Real-time collab" …` followed by `User --> Real-time collab` is a syntax error. **Quote the name everywhere it appears** — declaration, link lines, and `evolve` statements.

Failure mode: **a silent "Syntax error in text" SVG**, byte-identical in size across every broken input, with no line number. In a batch render that looks exactly like success until you open the file. `capture`-style pipelines should grep the output for `error-text` — that is what this session did, and it is what caught it.

**Practical rule for the site: quote every anchor and component name, always.** It costs two characters and removes the whole class of failure. The four maps in `maps/` do this.

---

## 4. The render pipeline — proven, and it should be a script

The corpus describes the recipe in prose only — *"Mermaid CLI v11.14.0 plus the Playwright-bundled Chromium"* — with no script, no Makefile target and no CI job. Here it is as something runnable:

```bash
# puppeteer-config.json
{"executablePath":"/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
 "args":["--no-sandbox","--disable-dev-shm-usage"]}

for f in maps/*.mmd; do
  npx @mermaid-js/mermaid-cli@11.14.0 \
      -i "$f" -o "${f%.mmd}.svg" \
      -p puppeteer-config.json -b white -w 1400 -H 900
  grep -q "error-text" "${f%.mmd}.svg" && echo "FAILED: $f"   # <- the check that matters
done
```

Two notes. Mermaid CLI ships its own Puppeteer and will try to download Chrome; pointing `executablePath` at an existing Chromium is what makes it work in a sandbox. And **the `grep` is not optional** — without it a broken map ships silently.

Ship this as `bin/render-maps.sh` plus a CI job, and add a check that every `.mmd` has a current `.svg`. That closes gap 3 in `08__`.

---

## 5. The 13 broken sources — day-one fix

None of the 13 Mermaid sources in the repo render, for two mundane reasons:

1. **Wrong code fence.** Eight-plus use a bare ` ``` ` with `wardley-beta` on the *next* line; four use ` ```wardley-beta `. Neither is recognised. GitHub and Mermaid both want ` ```mermaid ` with `wardley-beta` as the first line *inside* the block.
2. **One unquoted `note`.** In the 19 June brief: `note Genesis or custom built today: bespoke, manual, hope driven [0.34, 0.04]` — `note` requires quotes around its text.

Both are trivial. Fixing them turns 13 dead code blocks into 13 rendered maps and is the cheapest high-visibility win available. Do it before writing any new maps.

Then convert the **8 position tables** from the 23 June brief — they are already `Component | Visibility | Today | With our service`, which is `wardley-beta` in all but syntax, and they carry the **paired before/after** structure (W28) that makes them arguments rather than diagrams: *"The distance between the two is the case for the service."*

---

## 6. The four maps this pack ships

In `maps/`, each as `.mmd` source and rendered `.svg`. They are drawn about the site's own subject matter so they can go straight onto pages.

| Map | What it claims | Page |
|---|---|---|
| **M1 — The tool ecosystem, August 2026** | Authoring and versioning are product-to-commodity; **collaboration, doctrine assessment and agent authoring sit at Genesis with nothing under them** — the holes MapKeep and the doctrine tools left | `/resources/` opener |
| **M2 — The two absences** | The same point stated as loss: two user needs that had working implementations in 2025 and have none in August 2026 | `/resources/dead/` |
| **M3 — Maps for agents** | The new user need. Reading is served; **writing, and especially contesting a placement, are not** — "evidence for placement" is the least evolved node on the map | `/agents/` |
| **M4 — The site as a value chain** | What this site is, mapped. Resource pages and doctrine at custom-built; the `llms.txt` surface as the shared component; static hosting as commodity | `/about/` |

**They are claims, not decorations.** Every placement is arguable and should be argued with — which is the whole thesis. Publish the `.mmd` next to the `.svg` so a reader can fork the argument in a pull request. That is the corpus's own standard, from `pki.sgit.ai`: *"the maps live in the source and are reviewable in a diff."*

---

## 7. What is still missing after this pack

- **No `.owm` export.** A site that wants to interoperate with the Wardley community has nothing to hand it. `cli-owm` and `wardleyToGo` both consume OWM text; a converter is small.
- **No map diffs.** *"every significant change comes with a map diff — a before/after showing what moved"* is specified in the Cartographer REFERENCE. There is exactly one dated pair in the corpus and no mechanism.
- **No Claude skill for maps**, despite being asked for twice.
- **No stored map graph.** The corpus's strongest architectural claim — maps are graphs with position, so map queries are graph queries with positional filters — is listed as PROPOSED and has no implementation in any of the four repos. **If the site wants to demonstrate it, it will have to build it.** Say that on `/shipped/` rather than implying otherwise.
- **No "map that shows us badly."** Asked for explicitly as the honesty test of the whole series: *"Is there a map that shows us badly? Worth drawing, as the test of whether these are analysis or marketing."* It still does not exist. **Drawing it would be the most credible single page on the site.**

---

This document is released under the Creative Commons Attribution 4.0 International licence (CC BY 4.0).
