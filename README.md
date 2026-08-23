# wardley-maps.sgit.ai — maps are claims, not pictures

A Wardley map asserts where every component sits on the evolution axis. That makes it
**arguable** — and almost nobody publishes theirs anywhere it can be argued with. This site
publishes its maps as source next to the render, its doctrine ratings with the artefact each
one rests on, and its resource list with the date every link was last checked.

Live site: https://wardley-maps.sgit.ai (GitHub Pages, deployed from `dev`).

## What is here that is not elsewhere

- **A doctrine assessment that names its evidence** — 40 records across Wardley's six
  categories and four phases, every rating linking the artefact it rests on. Moved here from
  `pki.sgit.ai`, where it sat at appendix depth inside a PKI pack. There is currently no
  working doctrine assessment tool anywhere in the ecosystem.
- **Pioneers–Settlers–Town Planners as three literal AI agent teams** — three directory trees,
  three session contracts, three evolution-stage mandates. Never written up anywhere, including
  by the project that runs it. Includes the finding that 31 of its 33 role definitions never
  mention Wardley.
- **34 industry resources verified rather than listed** — a page each, with limitations stated
  and a verification date. Five things `awesome-wardley-maps`, Wikipedia and Simon Wardley's own
  resources page list as live are dead.

## Structure

- `index.html` — the front page; `index.md` its markdown twin
- `start/` — the teaching path, six rungs
- `method/` — four claims about the method, each naming what would falsify it
- `patterns/pst/` — Explorer / Villager / Town Planner
- `doctrine/` — the 40-record assessment and `doctrine.json`
- `resources/` — 34 resource pages, 11 obituaries, and the link-verification report
- `dinis/` — the published record, 2018–2025, and the gap after it
- `maps/` — four maps, `.mmd` source next to `.svg` render
- `agents/` — the machine surface, and `concepts.json`
- `shipped/` — what ships and what does not, unsoftened
- `glossary/`, `network/`, `about/`, `documents/`, `briefs/` (raw markdown, source of truth)
- `admin/` — comms, versions, and the build tooling
- `bin/` — `render-maps.sh`, `verify-links.js`, `optimise-shots.py`, `bump.py`

## Build

Hand-written static HTML with **programmatically injected chrome**. `admin/build/chrome.py` is
the single definition of the nav, the footer and the version badge, and rewrites them across
every page — which is what stops a 69-page site drifting, and what makes the version badge
enforceable in CI.

```bash
python3 admin/build/gen_resources.py    # if data/industry-resources.json changed
python3 admin/build/gen_dinis.py        # if data/dinis-published.json changed
python3 admin/build/gen_concepts.py     # if briefs/01__concepts-index.md changed
python3 admin/build/gen_documents.py    # if a brief was added
python3 admin/build/gen_surfaces.py     # llms.txt, llms-full.txt, sitemap.xml
python3 admin/build/chrome.py           # nav, footer, version badge everywhere
node admin/build/validate.js            # the gate CI will run
```

Maps: `bin/render-maps.sh` (Mermaid CLI 11.14.0 against an existing Chromium; greps the output
for `error-text`, because a broken `wardley-beta` source renders a byte-identical *"Syntax error
in text"* SVG with exit status zero).

Screenshots: `cd screenshots && npm i playwright && node capture.js`, then
`bin/optimise-shots.py`. Set `PROXY_FETCH=1` where the process has network egress but the
browser does not.

## Release

```bash
bin/bump.py "what changed"     # version.txt + a row in admin/versions.html, in one step
python3 admin/build/chrome.py
node admin/build/validate.js
git commit -am "site vX.Y.Z: what changed" && git push origin dev
```

Every push to `dev` runs `.github/workflows/deploy-pages.yml`: **validate → auto-tag → deploy**.
The tag is verified against `version.txt` *and* the release commit's subject, and the bump must
be the next minor. Pull requests run validation only. Same pipeline as
[SGit-AI__Website__PKI](https://github.com/SGit-AI/SGit-AI__Website__PKI) and
[SGit-AI__Website__Graphs](https://github.com/SGit-AI/SGit-AI__Website__Graphs).

### The release gate — seven checks

Four are the house gate: version agreement, internal links, canonical/CNAME agreement, and a
vault-key tripwire. Three are specific to this site: every raw brief carries its CC BY 4.0
stamp; every `maps/*.mmd` has a rendered `.svg` beside it that is not a syntax error; and every
page under `resources/` carries a `data-verified` stamp.

### The link-verification job

`.github/workflows/verify-links.yml` runs weekly and on demand: fetches every external URL the
site publishes, writes `data/link-check.json` with the run date, commits it if a verdict moved,
and dispatches a deploy. A 403 is recorded as **blocked** (the host refused a robot), not as
**error** (the link is broken); hosts that block outright are **skipped, never ok**. A dead link
does not fail the build — the point is that links rot, and a red pipeline would tempt somebody
to delete the evidence.

No sibling site has one. This site needs one, because it spends a page saying the community's
own indexes list five dead things as live.

## Licence

This site's own content is **CC BY 4.0**. The Wardley ecosystem is **CC BY-SA** — and Simon
Wardley's blog is CC BY-SA **3.0**, a different licence again. Those are compatible for reading
and incompatible for adapting, so ecosystem material appears here as clearly-marked quotation
and link-out, **never as adaptation**. See `about/licensing.html`.

Wardley Mapping is provided courtesy of Simon Wardley, CC BY-SA 4.0. Code under the repository
licence.
