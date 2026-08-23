#!/usr/bin/env python3
"""Generate /documents/ — in-page readers over the raw markdown in /briefs/.

    python3 admin/build/gen_documents.py

The house split, inherited from pki.sgit.ai: `/briefs/` is the raw markdown, served
as-is and unedited, and it is the **source of truth**; `/documents/` is a reader page
per document that renders that same file in-page. Nothing is copied. If the two ever
disagree it is a rendering bug, not an editorial one, and the raw link is right there.

That matters more here than on a sibling site, because these documents are the research
this site was built from — including the two places where the research disagrees with
the artefacts it describes (admin/comms.html, N1 and N2). Publishing the source lets a
reader check both the site and its brief.
"""
import re

from shell import ROOT, crumb, esc, page, write

BRIEFS = ROOT / "briefs"

# Title and one-line gist per document. The files carry their own H1; these are the
# shelf labels, written for somebody deciding what to open.
DOCS = [
    ("00__README.md", "The brief pack, read me first",
     "What the commission was, what each document does, and the four things that will bite "
     "you — the licence collision first among them."),
    ("00__BRIEF.md", "The brief",
     "The commission, two corrections to its premise, the thesis, the five pages only this "
     "site can write, the honesty constraint, and the build order."),
    ("01__concepts-index.md", "The concepts index",
     "Every distinct idea in the corpus with the words it was first stated in, its date and "
     "its classification. The source this site's glossary and concepts endpoint are parsed "
     "from — and the header whose counts do not match its own table."),
    ("02__pioneers-settlers-town-planners.md", "Explorer / Villager / Town Planner",
     "The raw material for the pattern write-up: what is on disk, which roles sit where, and "
     "the finding that 31 of 33 role definitions never mention Wardley."),
    ("03__job-a__dinis-published-material.md", "Job A — the published record",
     "Twenty-six items over seven years, the four claims held throughout, the two silences, "
     "and the archive priority order for the fragile ones."),
    ("04__job-b__industry-resources.md", "Job B — the industry resources",
     "The angle that makes a curation page worth writing, the per-resource template, the "
     "ranked top ten, the licence minefield and the three start-here routes."),
    ("05__maps-and-rendering.md", "Maps and rendering",
     "What maps exist, the coordinate contract proven by rendering rather than repeated, the "
     "complete wardley-beta parse rule, and the pipeline as something runnable."),
    ("06__site-architecture.md", "Site architecture",
     "The house pattern, the six markers, page-by-page IA, and what moves here versus what "
     "gets referenced."),
    ("07__boundaries-and-licensing.md", "Boundaries and licensing",
     "The CC BY / CC BY-SA collision in full, the do-not-publish list, screenshot ethics and "
     "house style."),
    ("08__gaps-and-open-questions.md", "Gaps and open questions",
     "Seven things that had to be written fresh, eight artefacts commissioned and never made, "
     "eight open questions and seven honest tensions."),
    ("LICENSE.md", "The pack's licence",
     "CC BY 4.0, and the four regimes it does not cover."),
]

EXTRA = [
    ("09__source-manifest.csv", "The source manifest",
     "73 rows. Every source, tiered 0–3, with its proposed page and whether it is publishable. "
     "Served as CSV — there is no reader page, because a spreadsheet is not prose."),
]


def words(text: str) -> int:
    return len(re.findall(r"\S+", text))


def main():
    made = []
    for fname, title, gist in DOCS:
        src = BRIEFS / fname
        if not src.exists():
            raise SystemExit(f"missing brief: {fname}")
        raw = src.read_text()
        slug = re.sub(r"^\d+__", "", fname.replace(".md", "")) or fname.replace(".md", "")
        slug = re.sub(r"[^a-z0-9-]+", "-", slug.lower().replace("__", "-")).strip("-")
        rel = f"documents/{slug}.html"
        wc = words(raw)
        body = f"""{crumb('../', ('The documents', 'documents/index.html'), title)}
<h1>{esc(title)}</h1>
<p class="lead">{esc(gist)}</p>
<div class="docmeta">
  <span class="k">Source of truth</span><span class="v"><a href="../briefs/{esc(fname)}">briefs/{esc(fname)}</a></span>
  <span class="k">Words</span><span class="v">{wc:,}</span>
  <span class="k">Licence</span><span class="v">CC BY 4.0</span>
</div>
<p class="mdread-label">Rendered below from the raw markdown, which is the source of truth —
<a href="../briefs/{esc(fname)}">open it directly</a> if you would rather read it that way, or
if this page fails to render it.</p>
<div id="mdread" class="mdread" data-src="../briefs/{esc(fname)}"></div>

<div class="pagenav">
  <a href="index.html">← All the documents</a>
  <a href="../shipped/index.html">What ships, and what doesn't →</a>
</div>"""
        write(rel, page(rel, f"{title} · documents · wardley-maps.sgit.ai", gist, body).replace(
            "</body>",
            '<script src="https://cdn.jsdelivr.net/npm/marked@12/marked.min.js"></script>\n'
            '<script src="../assets/mdreader.js" defer></script>\n</body>'))
        made.append((fname, slug, title, gist, wc))

    rows = "\n".join(
        f'    <tr><td><a href="{slug}.html">{esc(title)}</a></td>'
        f'<td class="small">{esc(gist)}</td>'
        f'<td class="small dim">{wc:,}</td>'
        f'<td class="small"><a href="../briefs/{esc(fname)}"><code>{esc(fname)}</code></a></td></tr>'
        for fname, slug, title, gist, wc in made)
    extra_rows = "\n".join(
        f'    <tr><td>{esc(title)}</td><td class="small">{esc(gist)}</td>'
        f'<td class="small dim">—</td>'
        f'<td class="small"><a href="../briefs/{esc(fname)}"><code>{esc(fname)}</code></a></td></tr>'
        for fname, title, gist in EXTRA)

    total = sum(wc for *_, wc in made)
    rel = "documents/index.html"
    body = f"""{crumb('../', 'The documents')}
<h1>The documents</h1>
<p class="lead">The research this site was built from, published in full. Ten documents,
{total:,} words, plus a 73-row source manifest. <b>The raw markdown in
<a href="../briefs/00__BRIEF.md">/briefs/</a> is the source of truth</b> — the reader pages
render those same files rather than copying them, so the two cannot drift.</p>

<p class="claim">Publishing the brief alongside the site is not generosity, it is the same
discipline as <a href="../maps/index.html">shipping a map's source next to its render</a> and
<a href="../doctrine/index.html">naming the artefact behind every doctrine rating</a>. It also
lets you catch us: <b>in two places the research disagrees with the artefacts it describes</b>,
this site publishes the artefacts' numbers, and you can now check which is right —
<a href="../admin/comms.html#n1">N1</a> and <a href="../admin/comms.html#n2">N2</a>.</p>

<div class="tablewrap"><table>
  <thead><tr><th>Document</th><th>What it does</th><th>Words</th><th>Raw</th></tr></thead>
  <tbody>
{rows}
{extra_rows}
  </tbody>
</table></div>

<h2 id="data">And the data</h2>
<p>Three of these documents ship structured data alongside the prose. It is served as-is:</p>
<ul>
  <li><a href="../data/industry-resources.json"><code>/data/industry-resources.json</code></a> —
    34 resources and 11 dead entries, each with licence and a pre-written attribution string.
    <a href="../resources/index.html">The pages built from it →</a></li>
  <li><a href="../data/dinis-published.json"><code>/data/dinis-published.json</code></a> — 26
    published items with date-precision and verification flags.
    <a href="../dinis/index.html">The chronology →</a></li>
  <li><a href="../agents/concepts.json"><code>/agents/concepts.json</code></a> — 35 concept
    records, parsed from the concepts index rather than retyped.
    <a href="../glossary/index.html">The glossary →</a></li>
  <li><a href="../doctrine/doctrine.json"><code>/doctrine/doctrine.json</code></a> — 40 doctrine
    records with evidence links. <a href="../doctrine/index.html">The assessment →</a></li>
  <li><a href="../screenshots/targets.json"><code>/screenshots/targets.json</code></a> and
    <a href="../screenshots/captured.json"><code>captured.json</code></a> — the 30 capture
    targets with their licence strings, and what actually happened to each.</li>
</ul>

<p class="small dim">All of it CC BY 4.0. Every markdown document carries the stamp, and
<a href="../admin/index.html#gate">the release gate fails the build</a> if one does not.</p>

<div class="pagenav">
  <a href="../about/licensing.html">← Licensing</a>
  <a href="../admin/comms.html">Comms →</a>
</div>"""
    write(rel, page(rel,
                    "The documents — the research this site was built from",
                    f"Ten documents, {total:,} words, published in full. The raw markdown is the "
                    "source of truth and the reader pages render it rather than copying it.",
                    body))
    print(f"gen_documents: {len(made)} readers + index ({total:,} words)")


if __name__ == "__main__":
    main()
