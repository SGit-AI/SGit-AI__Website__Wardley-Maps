#!/usr/bin/env python3
"""The single definition of this site's nav and footer, and the tool that applies it.

Run from anywhere: python3 admin/build/chrome.py

Every page is hand-written static HTML — that stays true, because a human should be
able to open any file and edit it. What is NOT hand-maintained is the chrome: the nav
row (including the version badge that validate.js requires to agree everywhere) and the
footer columns. Those are defined once here and rewritten in place across the tree,
which is what stops a hundred-page site from drifting.

Adding a page: add it to NAV or FOOTER if it belongs there, write the file with any
nav/footer block at all, then run this. The block contents are replaced; the `here`
state is set from the page's own path.

Same tool, same rules, as pki.sgit.ai and graphs.sgit.ai.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VERSION = (ROOT / "admin/build/version.txt").read_text().strip()
GH = "https://github.com/SGit-AI/SGit-AI__Website__Wardley-Maps"
PARENT = "https://sgit.ai"
PARENT_TITLE = ("sgit.ai — the parent project: the vault layer, the shipped CLI, and the "
                "Strategy Maps vault this site's map inventory draws on")

# The nav, two levels. Each entry is (label, own page, [(sub-label, href), ...], prefixes).
#
# Two rules the structure has to keep, inherited from the house component:
#   · A group label is always a link to a real page, never a menu-only stub. Nothing on
#     this site should be reachable only by opening a dropdown.
#   · `prefixes` decides the "here" state, so a page that is not itself in the nav — and
#     on this site that is most of them, since /resources/ alone is 45 pages — still
#     lights up the group it belongs to.
NAV = [
    ("Learn", "start/index.html", [
        ("Start here", "start/index.html"),
        ("The map gallery", "maps/index.html"),
        ("Glossary", "glossary/index.html"),
    ], ("start/", "glossary/", "maps/")),
    ("Method", "method/index.html", [
        ("The four claims", "method/index.html"),
        ("De-commoditisation", "method/de-commoditisation.html"),
        ("The custom-axis verdict", "method/custom-axes.html"),
        ("The broken middle", "method/broken-middle.html"),
        ("Maps are graphs with position", "method/maps-as-graphs.html"),
    ], ("method/",)),
    ("Doctrine", "doctrine/index.html", [
        ("The 40-record assessment", "doctrine/index.html"),
        ("Explorer / Villager / Town Planner", "patterns/pst/index.html"),
    ], ("doctrine/", "patterns/")),
    ("Resources", "resources/index.html", [
        ("All 34, verified", "resources/index.html"),
        ("Dead or dying", "resources/dead/index.html"),
        ("Link verification", "resources/verification.html"),
        ("Dinis Cruz on mapping, 2018–2025", "dinis/index.html"),
    ], ("resources/", "dinis/")),
    ("For agents", "agents/index.html", [
        ("The machine surface", "agents/index.html"),
        ("What ships, and what doesn't", "shipped/index.html"),
        ("The network", "network/index.html"),
    ], ("agents/", "shipped/", "network/")),
    ("Site", "admin/comms.html", [
        ("Comms: tasks &amp; requests", "admin/comms.html"),
        ("Release history", "admin/versions.html"),
        ("Admin &amp; engineering", "admin/index.html"),
        ("The documents", "documents/index.html"),
        ("Licensing", "about/licensing.html"),
        ("Where we lose", "about/participant.html"),
    ], ("admin/", "about/", "documents/")),
]

FOOTER = [
    ("Start", [
        ("&#8594; Start here", "start/index.html"),
        ("The map gallery", "maps/index.html"),
        ("Glossary", "glossary/index.html"),
        ("What ships, and what doesn't", "shipped/index.html"),
    ]),
    ("The four claims", [
        ("De-commoditisation", "method/de-commoditisation.html"),
        ("The custom-axis verdict", "method/custom-axes.html"),
        ("The broken middle", "method/broken-middle.html"),
        ("Maps are graphs with position", "method/maps-as-graphs.html"),
        ("Explorer / Villager / Town Planner", "patterns/pst/index.html"),
    ]),
    ("The record", [
        ("The doctrine assessment", "doctrine/index.html"),
        ("34 resources, verified", "resources/index.html"),
        ("Dead or dying", "resources/dead/index.html"),
        ("Dinis Cruz, 2018–2025", "dinis/index.html"),
        ("The documents", "documents/index.html"),
    ]),
    ("Site", [
        ("Comms: tasks &amp; requests", "admin/comms.html"),
        ("Release history", "admin/versions.html"),
        ("Licensing", "about/licensing.html"),
        ("llms.txt", "llms.txt"),
        ("llms-full.txt", "llms-full.txt"),
    ]),
]

BLURB = ("Wardley Mapping as a research site: the technique, an original doctrine assessment, "
         "34 industry resources verified rather than listed, and the mapping thinking behind "
         "the <a href=\"https://sgit.ai\" style=\"display:inline;padding:0\"><b>sgit.ai</b></a> "
         "network. This site's own content is CC BY 4.0; the ecosystem it quotes is CC BY-SA — "
         "<a href=\"{up}about/licensing.html\" style=\"display:inline;padding:0\">the difference "
         "matters</a>.")
WARDLEY = ('Wardley Mapping is provided courtesy of Simon Wardley, CC BY-SA 4.0. His blog, '
           '<a href="https://blog.gardeviance.org/" style="display:inline;padding:0">'
           'blog.gardeviance.org</a>, is CC BY-SA <b>3.0</b> — a different licence, quoted '
           'under a separate notice. Nothing here is an adaptation of either.')
PARTNOTE = ('⚠ Participant disclosure: published by the sgit project, which uses the mapping '
            'practice this site documents and is assessed by the doctrine page it hosts. '
            '<a href="{up}about/participant.html" style="display:inline;padding:0">'
            'Read the disclosure</a>.')
PARTNOTE_SELF = '⚠ Participant disclosure: published by the sgit project. You are on the disclosure page.'
NETLINE = ('<a href="https://sgit.ai"><b>↗ sgit.ai</b></a> — the parent project and the Strategy '
           'Maps vault · <a href="https://graphs.sgit.ai/v1/maps/index.html">↗ graphs.sgit.ai</a> — '
           'maps as graphs · <a href="https://pki.sgit.ai">↗ pki.sgit.ai</a> — where the doctrine '
           'assessment was built · <a href="https://sgit.ai/network/index.html">↗ the network</a>')


def nav_html(rel, up):
    groups = []
    for label, own, subs, prefixes in NAV:
        active = rel == own or any(rel.startswith(pre) for pre in prefixes)
        links = "\n".join(
            f'      <a class="sl{" here" if href == rel else ""}" href="{up}{href}">{text}</a>'
            for text, href in subs)
        groups.append(
            f'    <div class="ni ni-has">\n'
            f'      <a class="nl{" here" if active else ""}" href="{up}{own}">{label}'
            f'<span class="caret">&#9662;</span></a>\n'
            f'      <div class="sub">\n{links}\n      </div>\n'
            f'    </div>')
    rows = "\n".join(groups)
    return (f'<nav class="site"><div class="row">\n'
            f'  <a class="brand" href="{up}index.html">wardley-maps<span>.sgit.ai</span></a>\n'
            f'  <a class="parent" href="{PARENT}" title="{PARENT_TITLE}">↗ part of <b>sgit.ai</b></a>\n'
            f'  <span class="stage-pill">research site</span>\n'
            f'  <a class="ver" href="{up}admin/versions.html" title="Site release history">{VERSION}</a>\n'
            f'  <button class="nav-toggle" type="button" aria-expanded="false" aria-label="Menu">Menu</button>\n'
            f'  <div class="nav-items">\n{rows}\n  </div>\n'
            f'  <a class="gh" href="{GH}">★ GitHub</a>\n'
            f'  <script src="{up}assets/nav.js" defer></script>\n'
            f'</div></nav>')


def footer_html(rel, up):
    partnote = PARTNOTE_SELF if rel == "about/participant.html" else PARTNOTE.format(up=up)
    md_twin = f' · <a href="{up}index.md">this page as markdown</a>' if rel == "index.html" else ""
    cols = "\n".join(
        "  <div>\n"
        f"    <h4>{head}</h4>\n"
        + "\n".join(f'    <a href="{l if l.startswith("http") else up + l}">{t}</a>' for t, l in links)
        + "\n  </div>"
        for head, links in FOOTER)
    return (f'<footer class="site"><div class="cols">\n'
            f'  <div>\n'
            f'    <div class="brandline">wardley-maps<span>.sgit.ai</span></div>\n'
            f'    <p>{BLURB.format(up=up)}</p>\n'
            f'    <p class="netline">{NETLINE}</p>\n'
            f'    <p class="partnote">{partnote}</p>\n'
            f'    <p class="partnote">{WARDLEY}</p>\n'
            f'    <p class="verline">site <a href="{up}admin/versions.html">{VERSION}</a> · '
            f'<a href="{up}admin/index.html">engineering</a> · '
            f'<a href="{up}about/licensing.html">CC BY 4.0</a>{md_twin}</p>\n'
            f'  </div>\n{cols}\n</div></footer>')


ICON = ('<link rel="icon" href="{up}assets/favicon.svg" type="image/svg+xml">\n'
        '<link rel="mask-icon" href="{up}assets/favicon.svg" color="#0f766e">')


def ensure_icon(text, up):
    """The favicon is chrome too. Injected here rather than written into every page for
    the same reason the nav is: 69 pages, one definition, and no page can be missed."""
    if 'rel="icon"' in text:
        return re.sub(r'<link rel="icon"[^>]*>\n<link rel="mask-icon"[^>]*>',
                      lambda _: ICON.format(up=up), text, count=1)
    return text.replace(f'<link rel="stylesheet" href="{up}assets/site.css">',
                        ICON.format(up=up) + f'\n<link rel="stylesheet" href="{up}assets/site.css">',
                        1)


def stamp_text_twins():
    """The version also appears in llms.txt, llms-full.txt and index.md, and validate.js
    enforces that they agree. Nothing used to SET it there on the sibling sites, so it
    was hand-edited every release — and hand-editing it silently missed twice. Own it
    here instead."""
    out = []
    for name, pattern, repl in (
        ("llms.txt", r"Site version: v\d+\.\d+\.\d+", f"Site version: {VERSION}"),
        ("llms-full.txt", r"Site version: v\d+\.\d+\.\d+", f"Site version: {VERSION}"),
        ("index.md", r"· site v\d+\.\d+\.\d+ ·", f"· site {VERSION} ·"),
    ):
        f = ROOT / name
        if not f.exists():
            continue
        t = f.read_text()
        t2, n = re.subn(pattern, repl, t, count=1)
        if n and t2 != t:
            f.write_text(t2)
            out.append(name)
    return out


def main():
    changed, missing = [], []
    skip = {".git", ".github", "node_modules", ".sg_vault"}
    for path in sorted(ROOT.rglob("*.html")):
        if skip & set(path.parts):
            continue
        rel = path.relative_to(ROOT).as_posix()
        up = "../" * (len(path.relative_to(ROOT).parts) - 1)
        text = before = path.read_text()
        text = ensure_icon(text, up)
        text, n_nav = re.subn(r'<nav class="site">.*?</nav>', lambda _: nav_html(rel, up),
                              text, count=1, flags=re.S)
        text, n_foot = re.subn(r'<footer class="site">.*?</footer>', lambda _: footer_html(rel, up),
                               text, count=1, flags=re.S)
        if not n_nav or not n_foot:
            missing.append(f"{rel}: missing {'nav' if not n_nav else ''}"
                           f"{' and ' if not n_nav and not n_foot else ''}{'footer' if not n_foot else ''}")
        if text != before:
            path.write_text(text)
            changed.append(rel)
    changed += stamp_text_twins()
    for m in missing:
        print(f"  ! {m}", file=sys.stderr)
    print(f"chrome: {VERSION} applied — {len(changed)} file(s) updated"
          + (f", {len(missing)} without a chrome block" if missing else ""))


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        sys.stdout = None
