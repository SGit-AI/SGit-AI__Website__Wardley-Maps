#!/usr/bin/env python3
"""Parse the concepts index into a machine-readable endpoint, and build the glossary.

    python3 admin/build/gen_concepts.py

Writes:
  agents/concepts.json   — the definitions endpoint. 35 rows, each with the quotation
                           it rests on, its date, its canonical source file inside the
                           private corpus, and its classification: standard doctrine [S],
                           extension [E] or original contribution [O].
  glossary/index.html    — the same data as a page, plus the two vocabulary problems the
                           corpus has and this site does not get to inherit.

The source of truth is briefs/01__concepts-index.md — a markdown table. Parsing it rather
than retyping it means the page and the endpoint cannot drift from the research, and that
a correction lands in one place. The classification column is the site's editorial spine:
standard doctrine is Wardley's and gets linked, not restated (which is also the
licence-safe move — see about/licensing.html). Extensions and originals are what this
site is for.
"""
import json
import re

from shell import ROOT, crumb, esc, md_inline, page, write

SRC = ROOT / "briefs/01__concepts-index.md"

CLASSES = {
    "S": ("standard", "Standard doctrine",
          "Wardley's, and his book says it first and better. Linked, not restated."),
    "E": ("extension", "Extension",
          "Standard doctrine pushed somewhere it is not usually taken."),
    "O": ("original", "Original contribution",
          "Not found in the doctrine or in the ecosystem's literature. The reason this site exists."),
}

# Concepts that have a page of their own. Everything else is a paragraph somewhere.
PAGES = {
    "W1": "../patterns/pst/index.html",
    "W2": "../patterns/pst/index.html",
    "W5": "../method/maps-as-graphs.html",
    "W6": "../method/custom-axes.html",
    "W6b": "../method/custom-axes.html",
    "W7": "../method/custom-axes.html",
    "W8": "../method/de-commoditisation.html",
    "W9": "../method/de-commoditisation.html",
    "W12": "../method/broken-middle.html",
    "W13": "../agents/index.html",
    "W13b": "../agents/index.html",
    "W14": "../patterns/pst/index.html",
    "W15": "../patterns/pst/index.html",
    "W23": "../index.html",
    "W24": "../patterns/pst/index.html",
    "W31": "../shipped/index.html",
}

ALTITUDES = [
    ("What a map is",
     "Anchor, position, evolution, the four stages. This belongs to Wardley — "
     "<a href=\"../resources/wardley-maps-the-book-medium-serialisation.html\">link out to the "
     "book</a> and to Wardley Mapping 101; this site does not rewrite it.",
     []),
    ("How to read one",
     "Three named reading techniques, each of which changes what you see.",
     ["W29", "W28", "W10"]),
    ("How to write one that survives review",
     "The coordinate contract, the parse rules, and the two rules that make a map arguable "
     "rather than decorative.",
     ["W13", "W13b", "W23", "W31"]),
    ("Where doctrine bends",
     "The site's centre of gravity. Four opinionated pages.",
     ["W7", "W6", "W6b", "W8", "W12"]),
    ("Maps as organisation",
     "Pioneers–Settlers–Town Planners, applied to agent teams and to artefacts rather than "
     "to people.",
     ["W1", "W2", "W14", "W16", "W18", "W24", "W25"]),
    ("Maps as data",
     "The most architecturally ambitious layer and the least implemented. Labelled as "
     "design, not as shipped.",
     ["W5", "W21", "W22", "W26", "W27"]),
]


def strip_md(s: str) -> str:
    """Table cells carry **bold**, *italics*, `code` and — quotes. Keep the text."""
    s = re.sub(r"</?[a-z]+>", "", s)
    s = s.replace("\\|", "|").replace("&nbsp;", " ")
    return s.strip()


def parse():
    rows = []
    in_table = False
    for line in SRC.read_text().splitlines():
        if line.startswith("| ID | Concept"):
            in_table = True
            continue
        if in_table:
            if not line.startswith("|"):
                break
            cells = [c.strip() for c in line.strip().strip("|").split(" | ")]
            if len(cells) < 8 or set(cells[0]) <= set("-: "):
                continue
            cid, concept, quote, source, dt, words, maturity, cls = cells[:8]
            cid = strip_md(cid).strip("*")
            klass = "O" if "[O]" in cls else "E" if "[E]" in cls else "S"
            note = re.sub(r"^\[.\]\s*—?\s*", "", strip_md(cls)).strip()
            rows.append({
                "id": cid,
                "concept": strip_md(concept),
                "quote": strip_md(quote),
                "source": strip_md(source).strip("`"),
                "date": strip_md(dt),
                "maturity": strip_md(maturity),
                "class": klass,
                "class_label": CLASSES[klass][1],
                "class_note": note if note and note != CLASSES[klass][1] else "",
                "page": PAGES.get(cid, "").replace("../", "/") or None,
            })
    return rows


def main():
    rows = parse()
    # The source table's own header says "33 entries — 14 [O], 13 [E], 6 [S]". Parsing it
    # yields 35 rows classified 17/14/4: four are lettered sub-entries (W6b, W13b, W15b,
    # W25b) of a parent concept, which accounts for the row count but not the class split.
    # The parse is what ships, the discrepancy is published rather than smoothed over
    # (admin/comms.html, N2), and this assert exists so a future edit to the table that
    # changes the shape has to be looked at rather than silently absorbed.
    if len(rows) != 35:
        raise SystemExit(f"expected 35 rows in briefs/01__concepts-index.md, parsed {len(rows)}")
    by_id = {r["id"]: r for r in rows}
    counts = {k: sum(1 for r in rows if r["class"] == k) for k in "OES"}

    # --- the endpoint -----------------------------------------------------
    endpoint = {
        "schema": "wardley-maps-sgit-ai/concepts/v1",
        "source": "https://wardley-maps.sgit.ai/briefs/01__concepts-index.md",
        "compiled": "2026-08-23",
        "licence": "CC BY 4.0",
        "note": (
            "Thirty-five rows — 31 primary concepts plus 4 lettered sub-entries — drawn from a "
            "private corpus of 194 files. The `class` field "
            "is the important one: S means it is standard Wardley doctrine and belongs to Simon "
            "Wardley — quote it and link it, do not treat this file as a source for it. E and O "
            "are this corpus's own extensions and original contributions. The `source` paths are "
            "inside a private repository and are recorded for provenance, not for retrieval."),
        "classes": {k: {"label": v[1], "note": v[2]} for k, v in CLASSES.items()},
        "counts": {"total": len(rows), "original": counts["O"],
                   "extension": counts["E"], "standard": counts["S"]},
        "concepts": rows,
    }
    write("agents/concepts.json", json.dumps(endpoint, indent=1, ensure_ascii=False) + "\n")

    # --- the glossary page ------------------------------------------------
    def card(r):
        cls_key, cls_label, _ = CLASSES[r["class"]]
        page_link = (f' <a class="gopage" href="{PAGES[r["id"]]}">read the page →</a>'
                     if r["id"] in PAGES else "")
        return f"""  <article class="gterm c-{cls_key}" id="{esc(r['id'].lower())}">
    <h4><span class="did inline">{esc(r['id'])}</span> {md_inline(r['concept'], link_urls=False)}</h4>
    <p class="badges"><span class="badge b-{cls_key}">{esc(cls_label)}</span>
      <span class="badge b-type">{esc(r['maturity'])}</span>
      <span class="badge b-type">{esc(r['date'])}</span></p>
    <blockquote>{md_inline(r['quote'], link_urls=False)}</blockquote>
    {f'<p class="small dim">{md_inline(r["class_note"], link_urls=False)}</p>' if r['class_note'] else ''}
    <p class="small dim">Source: <code>{esc(r['source'])}</code>{page_link}</p>
  </article>"""

    groups = ""
    for key in ("O", "E", "S"):
        cls_key, cls_label, cls_note = CLASSES[key]
        members = [r for r in rows if r["class"] == key]
        groups += (f'\n<h3 id="{cls_key}">{cls_label} <span class="dim">{len(members)}</span></h3>\n'
                   f'<p class="blurb">{cls_note}</p>\n'
                   + "\n".join(card(r) for r in members) + "\n")

    ladder = ""
    for i, (title, blurb, ids) in enumerate(ALTITUDES, 1):
        links = " · ".join(
            f'<a href="#{i_.lower()}">{esc(by_id[i_]["concept"].split(" — ")[0].split(",")[0])}</a>'
            for i_ in ids if i_ in by_id)
        ladder += (f'  <div class="cap"><span class="num">{i}</span>'
                   f'<h3>{esc(title)}</h3><p>{blurb}</p>'
                   f'{f"<p class=small>{links}</p>" if links else ""}</div>\n')

    rel = "glossary/index.html"
    body = f"""{crumb('../', 'Glossary')}
<h1>Thirty-five concepts, classified</h1>
<p class="lead">Every distinct Wardley-related idea in the corpus this site draws on, with the
words it was first stated in, the date, and — the column that matters — whether it is
<b>standard doctrine</b>, an <b>extension</b>, or an <b>original contribution</b>.</p>

<div class="warnbox"><b>A correction to our own source.</b> The research table this page is
generated from opens by declaring <em>"33 entries — 14 [O], 13 [E], 6 [S]"</em>. Parsing it
yields <b>{len(rows)} rows classified {counts['O']} original / {counts['E']} extension / {counts['S']} standard</b>. Four rows are lettered sub-entries
(W6b, W13b, W15b, W25b) of a parent concept, which explains the row count but not the class
split. The parse is what this page and
<a href="../agents/concepts.json">the endpoint</a> publish, because the table is the artefact
and the header is a summary of it. Logged as
<a href="../admin/comms.html#n2">N2</a>.</div>

<p class="claim">That classification is the site's editorial spine, and it is also the
licence-safe move. Standard doctrine is Simon Wardley's: his book says it first and better, and
restating CC BY-SA material as though it were ours would both mislead and
<a href="../about/licensing.html">infect the page's licence</a>. So standard doctrine is
<em>linked</em>, never rewritten. Extensions and originals are what this site is for.</p>

<div class="hgrid">
  <a class="hstat s-strong" href="#original"><span class="n">{counts['O']}</span><span class="l">Original</span></a>
  <a class="hstat s-partial" href="#extension"><span class="n">{counts['E']}</span><span class="l">Extension</span></a>
  <a class="hstat s-na" href="#standard"><span class="n">{counts['S']}</span><span class="l">Standard doctrine</span></a>
</div>

<h2 id="vocabulary">Two vocabulary problems, fixed here</h2>
<p><b>Spelling.</b> The corpus uses <em>commoditise / commoditize</em> and <em>productise /
productize</em> interchangeably, sometimes in the same document. This site uses
<b>-ise</b> throughout, to match the rest of the network. The <em>-ize</em> spellings are the
same word and carry no different meaning; quotations keep whatever spelling they were written
with.</p>
<p><b>Names.</b> <em>Explorer</em> and <em>Pioneer</em> are the same thing; so are
<em>Villager</em> and <em>Settler</em>. The rename is stated outright exactly once in the entire
corpus — parenthetically, in a brief about something else. This site states it on every first
use and never drifts: <b>Explorer = Pioneer, Villager = Settler, Town Planner = Town
Planner</b>, after Simon Wardley,
<a href="https://blog.gardeviance.org/2015/03/on-pioneers-settlers-town-planners-and.html">
<em>On Pioneers, Settlers, Town Planners and Theft</em></a> (2015), CC BY-SA 3.0. The word
<em>Settler</em> appears once in the entire corpus; it is not adopted here.</p>

<h2 id="ladder">A teaching order, six rungs</h2>
<p>The corpus is dense at the top and thin at the bottom: one 846-word primer, then a cliff.
This is the ladder — <a href="../start/index.html">and /start/ walks it</a>.</p>
<div class="ladder">
{ladder}</div>

<h2 id="all">All thirty-five</h2>
<p class="small dim">Machine-readable at <a href="../agents/concepts.json">/agents/concepts.json</a>.
The source paths are inside a private repository and are recorded for provenance, not
retrieval — see <a href="../shipped/index.html">what is and is not published</a>.</p>
{groups}

<div class="pagenav">
  <a href="../start/index.html">← Start here</a>
  <a href="../agents/index.html">The machine surface →</a>
</div>"""
    write(rel, page(rel,
                    "Glossary — 35 Wardley Mapping concepts, classified",
                    "Thirty-five concepts with the words they were first stated in, their date, "
                    "and whether each is standard Wardley doctrine, an extension of it, or an "
                    "original contribution. Machine-readable at /agents/concepts.json.",
                    body))
    print(f"gen_concepts: {len(rows)} concepts "
          f"({counts['O']} original, {counts['E']} extension, {counts['S']} standard) "
          f"-> agents/concepts.json, glossary/index.html")


if __name__ == "__main__":
    main()
