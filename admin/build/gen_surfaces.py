#!/usr/bin/env python3
"""Generate the text surfaces: llms.txt, llms-full.txt, index.md and sitemap.xml.

    python3 admin/build/gen_surfaces.py

Four files that describe the whole site, and four files that go stale the instant a page
is added — which is exactly why they are generated from the tree rather than maintained.
`llms.txt` is the map; `llms-full.txt` is the territory (every markdown document and
every map source, concatenated); `index.md` is the front page as markdown, linked from
the front page's own `<link rel="alternate">`; `sitemap.xml` is every page with its file
mtime as `lastmod`.

The version string in the first three is stamped by chrome.py and enforced by
validate.js, so the surfaces cannot claim a version the site is not on. The sibling site
this pattern comes from hand-edited that string and silently missed it twice.
"""
import re
import subprocess
from datetime import date, datetime, timezone
from pathlib import Path

from shell import HOST, ROOT, VERSION, write

SKIP_DIRS = {".git", ".github", "node_modules", ".sg_vault"}

# The narrative order — the order a reader, or a model, should meet the site in. Anything
# in the tree that is not listed here still appears, under "everything else", so a new
# page cannot silently fall out of the surface.
ORDER = [
    ("Start", [
        ("index.html", "The front page. Maps are claims, not pictures — the thesis, the three things this site has that others do not, and one rendered map."),
        ("start/index.html", "The teaching path: six rungs from 'I read the introduction' to 'I can argue about a placement'."),
        ("glossary/index.html", "35 concepts with the words they were first stated in, classified as standard doctrine, extension, or original contribution."),
    ]),
    ("The method — four claims, each naming what would falsify it", [
        ("method/index.html", "Index of the four, plus the two reading techniques the site assumes."),
        ("method/de-commoditisation.html", "A thing can be commoditised at one phase of evolution while still being custom-built at the next. Includes the counter-argument (ILC) that has not been answered."),
        ("method/custom-axes.html", "Relabel the axis when the thing genuinely evolves; use a maturity model when it merely improves. Six alternative axes were proposed and none was ever drawn."),
        ("method/broken-middle.html", "You cannot map a gap, because a gap has no evolution. The ends are solved; the middle is people. Contains an unresolved contradiction, stated as one."),
        ("method/maps-as-graphs.html", "A map is a graph with positional metadata; map queries are graph queries with positional filters. NO IMPLEMENTATION — published as design."),
    ]),
    ("Doctrine and the pattern", [
        ("doctrine/index.html", "40 Wardley doctrines in six categories and four phases, self-assessed, with the artefact behind every rating. Moved here from pki.sgit.ai."),
        ("doctrine/doctrine.json", "ENDPOINT. The assessment as data: id, cat, phase, name, what, status, us, evidence. Self-describing."),
        ("patterns/pst/index.html", "Pioneers–Settlers–Town Planners as three literal AI agent teams — three directory trees, three session contracts, three evolution-stage mandates. Never published anywhere before. Includes the finding that 31 of 33 role definitions never mention Wardley."),
    ]),
    ("The resources — verified, not listed", [
        ("resources/index.html", "34 resources, a page each, with three start-here routes and a ranked top ten."),
        ("resources/dead/index.html", "11 dead or dying, and which canonical indexes still list them as live. MapKeep ceased 30 May 2026."),
        ("resources/verification.html", "The link-verification run: every external URL, checked weekly, with the run date published. Blocked hosts recorded as skipped, never as ok."),
        ("dinis/index.html", "Dinis Cruz's published Wardley material, 2018–2025: 26 items, two silent years, and the single clause that is the only public bridge to the agentic work."),
    ]),
    ("For agents", [
        ("agents/index.html", "The machine surface: the coordinate contract proven by rendering, the complete parse rule, what the axis measures, and the epistemic guardrail."),
        ("agents/concepts.json", "ENDPOINT. 35 concept records with quotation, date, source and classification. Read the `class` field: S means it is Wardley's."),
        ("maps/index.html", "Four maps, source next to render, each stating what it claims and what would falsify it. Plus the render pipeline and the coordinate proof."),
        ("data/link-check.json", "ENDPOINT. Every external URL with its last check, status, and whether it redirected."),
        ("screenshots/captured.json", "ENDPOINT. Every screenshot attempt including failures, with timestamps and the transformation applied to each published image."),
    ]),
    ("Honesty", [
        ("shipped/index.html", "What ships and what does not. Zero of 13 map sources rendered; the living map died 26 Feb 2026; maps-as-graphs has no code; the map that shows us badly has not been drawn."),
        ("about/licensing.html", "CC BY inside a CC BY-SA ecosystem: the rule, the 3.0/4.0 split, six flagged licences, and what is deliberately not published."),
        ("about/participant.html", "Participant disclosure, and four places this site's approach is the wrong one."),
        ("network/index.html", "Seven sites, who owns what, and the four siblings that mention Wardley zero times."),
    ]),
    ("Site", [
        ("documents/index.html", "The research this site was built from, in full. The raw markdown in /briefs/ is the source of truth."),
        ("admin/index.html", "How the site is built, validated, tagged and deployed. The seven-check release gate."),
        ("admin/comms.html", "Numbered asks (N1…), tasks (T1…), and eight open questions published without answers."),
        ("admin/versions.html", "Release history."),
    ]),
]

INTRO = f"""# wardley-maps.sgit.ai

> Maps are claims, not pictures. A Wardley map asserts where each component sits on the
> evolution axis, which makes it arguable — and almost nobody publishes theirs anywhere it
> can be argued with.

Site version: {VERSION} · CC BY 4.0 · part of the sgit.ai network

A research site for Wardley Mapping. Three things here are not available elsewhere: a
40-record doctrine self-assessment where every rating names the artefact it rests on; the
first write-up of Pioneers–Settlers–Town Planners built as three literal AI agent teams; and
34 industry resources verified on a stated date rather than listed, because the community's
own canonical indexes currently list five dead things as live.

## What to read first if you are a model

Three facts on this site are easy to get wrong and expensive to get wrong:

1. **Coordinates are `[visibility, evolution]`, not `[x, y]`** — in both the OnlineWardleyMaps
   DSL and Mermaid's `wardley-beta`. Transposing them renders without error and asserts
   something else. Proven by rendering at /agents/index.html#coordinates, not repeated from
   documentation.
2. **Quote every anchor and component name, everywhere it appears** — declaration, link lines
   and `evolve` statements. Unquoted, a hyphen, a dot or a slash is a syntax error, and the
   failure is a silent byte-identical "Syntax error in text" SVG with exit status zero.
3. **The evolution axis plausibly encodes consensus rather than objective fact.** A model
   placing components on it is generating consensus-shaped output with no underlying evidence.
   Surface every placement as an explicitly contestable claim requiring human challenge, never
   as a finding. This is not a caveat; it is the most important sentence on /agents/.

## Licence, and why it constrains this site

This site is CC BY 4.0. The Wardley ecosystem is CC BY-SA 4.0 — and Simon Wardley's blog is
CC BY-SA **3.0**, a different licence. Those are compatible for reading and incompatible for
adapting, so material from that ecosystem appears here as clearly-marked quotation and
link-out, never as adaptation. Wardley Mapping is provided courtesy of Simon Wardley,
CC BY-SA 4.0. See /about/licensing.html.
"""


def walk(d: Path):
    for p in sorted(d.iterdir()):
        if p.name in SKIP_DIRS:
            continue
        if p.is_dir():
            yield from walk(p)
        else:
            yield p


def mtime(p: Path) -> str:
    """Prefer the file's last commit date — a checkout's mtimes are all the clone time."""
    try:
        out = subprocess.run(["git", "log", "-1", "--format=%cs", "--", str(p)],
                             cwd=ROOT, capture_output=True, text=True, timeout=10)
        if out.returncode == 0 and out.stdout.strip():
            return out.stdout.strip()
    except Exception:
        pass
    return datetime.fromtimestamp(p.stat().st_mtime, timezone.utc).date().isoformat()


def main():
    listed = {rel for _, group in ORDER for rel, _ in group}
    all_html = sorted(str(p.relative_to(ROOT)) for p in walk(ROOT) if p.suffix == ".html")

    # --- llms.txt ---------------------------------------------------------
    out = [INTRO]
    for heading, group in ORDER:
        out.append(f"## {heading}\n")
        for rel, gist in group:
            out.append(f"- [/{rel}](https://{HOST}/{rel}): {gist}")
        out.append("")

    rest = [r for r in all_html if r not in listed]
    out.append("## Everything else\n")
    out.append("Generated from the tree, so a page cannot fall out of this surface by being "
               "forgotten. Mostly the 34 resource pages and the 11 document readers.\n")
    for rel in rest:
        out.append(f"- [/{rel}](https://{HOST}/{rel})")
    out.append("")
    out.append("## Raw sources\n")
    out.append("The research this site was built from, served as markdown. This is the source "
               "of truth; /documents/ renders these same files rather than copying them.\n")
    for p in sorted((ROOT / "briefs").iterdir()):
        out.append(f"- [/briefs/{p.name}](https://{HOST}/briefs/{p.name})")
    out.append("")
    out.append("Every map's `wardley-beta` source sits next to its rendered SVG in /maps/. "
               "Full text of everything above: /llms-full.txt\n")
    write("llms.txt", "\n".join(out))

    # --- llms-full.txt ----------------------------------------------------
    full = [f"""# wardley-maps.sgit.ai — full text
# Site version: {VERSION} · generated {date.today().isoformat()} · CC BY 4.0
#
# Every markdown document and every map source on this site, concatenated. The HTML pages
# are not included: they are presentation over this material plus the JSON endpoints at
# /doctrine/doctrine.json, /agents/concepts.json, /data/link-check.json and
# /screenshots/captured.json.
#
# Wardley Mapping is provided courtesy of Simon Wardley, CC BY-SA 4.0. Everything below is
# this site's own work and is CC BY 4.0; where it quotes the ecosystem it quotes rather than
# adapts. See https://{HOST}/about/licensing.html
"""]
    for p in sorted((ROOT / "briefs").glob("*.md")):
        full.append(f"\n\n{'=' * 78}\n=== /briefs/{p.name}\n{'=' * 78}\n")
        full.append(p.read_text())
    for p in sorted((ROOT / "maps").glob("*.mmd")):
        full.append(f"\n\n{'=' * 78}\n=== /maps/{p.name} — wardley-beta source\n{'=' * 78}\n")
        full.append(p.read_text())
    idx = ROOT / "index.md"
    if idx.exists():
        full.append(f"\n\n{'=' * 78}\n=== /index.md\n{'=' * 78}\n")
        full.append(idx.read_text())
    write("llms-full.txt", "".join(full))

    # --- sitemap.xml ------------------------------------------------------
    ordered = [r for _, g in ORDER for r, _ in g if r.endswith(".html")] + rest
    urls = "\n".join(
        f"  <url><loc>https://{HOST}/{rel}</loc><lastmod>{mtime(ROOT / rel)}</lastmod></url>"
        for rel in ordered)
    write("sitemap.xml",
          '<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          f"{urls}\n</urlset>\n")

    print(f"gen_surfaces: llms.txt ({len(all_html)} pages listed), llms-full.txt "
          f"({sum(len(x) for x in full) // 1000}k chars), sitemap.xml")


if __name__ == "__main__":
    main()
