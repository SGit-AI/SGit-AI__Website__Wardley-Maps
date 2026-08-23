#!/usr/bin/env python3
"""The page shell every generator emits, and the small helpers they share.

Not a template engine. It writes the `<head>`, the empty `<nav class="site">` and
`<footer class="site">` blocks that chrome.py fills in, and gets out of the way. The
body is the caller's problem, because the body is the part a human should be able to
open and edit.

Hand-written pages are written by hand with the same shape. This exists so the 45
resource pages, the 10 document readers and the chronology do not have to be.
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HOST = (ROOT / "CNAME").read_text().strip()
VERSION = (ROOT / "admin/build/version.txt").read_text().strip()

esc = html.escape


def up_for(rel: str) -> str:
    """'resources/dead/index.html' -> '../../'"""
    return "../" * (rel.count("/"))


def page(rel: str, title: str, description: str, body: str, *,
         og_title: str = None, og_description: str = None,
         extra_head: str = "", main_class: str = "doc") -> str:
    """Return a complete page. `rel` is the path from the site root."""
    up = up_for(rel)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="https://{HOST}/{rel}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="{HOST}">
<meta property="og:url" content="https://{HOST}/{rel}">
<meta property="og:title" content="{esc(og_title or title)}">
<meta property="og:description" content="{esc(og_description or description)}">
<meta name="twitter:card" content="summary">
<link rel="stylesheet" href="{up}assets/site.css">{extra_head}
</head>
<body>

<nav class="site"></nav>

<main class="{main_class}">
{body}
</main>

<footer class="site"></footer>
</body>
</html>
"""


def write(rel: str, text: str) -> Path:
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)
    return p


def load(name: str):
    return json.loads((ROOT / "data" / name).read_text())


def crumb(up: str, *trail) -> str:
    """`trail` is (label, href) pairs, then a final bare label."""
    parts = [f'<a href="{up}index.html">wardley-maps.sgit.ai</a>']
    for item in trail:
        if isinstance(item, tuple):
            parts.append(f'<a href="{up}{item[1]}">{esc(item[0])}</a>')
        else:
            parts.append(esc(item))
    return '<p class="crumb">' + " / ".join(parts) + "</p>"


def slugify(name: str, limit: int = 60) -> str:
    """A stable, readable slug. Truncates at a word boundary — cutting mid-word gives
    URLs like `...-limitations-cr.html`, which look like a bug even when they are not."""
    s = name.lower().replace("&", " and ")
    s = re.sub(r"-{2,}", "-", re.sub(r"[^a-z0-9]+", "-", s)).strip("-")
    if len(s) <= limit:
        return s
    cut = s[:limit]
    return (cut.rsplit("-", 1)[0] if "-" in cut else cut).strip("-")


# --- the small amount of markdown the source data uses ---------------------
# The resource JSON writes **bold**, *italic*, `code` and bare URLs inside prose
# fields. Rendering those four is worth 12 lines; pulling in a markdown library to
# render four constructs into a static site is not.
_URL = re.compile(r'(?<![("\w])(https?://[^\s<>")\]]+[^\s<>")\].,;:])')


def plain(text: str) -> str:
    """Markdown markers stripped, for a meta description — where a stray backtick or a pair
    of asterisks is just noise in a search result."""
    out = re.sub(r"[`*_]+", "", text)
    return re.sub(r"\s+", " ", out).strip()


def md_inline(text: str, *, link_urls: bool = True) -> str:
    out = esc(text)
    # Some prose fields carry a fenced example inline. Render the fence as a block rather
    # than leaving a pair of stray backticks wrapped around a <code> span.
    out = re.sub(r"``\s*<?code>?(.+?)</?code>?\s*``", r"<code>\1</code>", out, flags=re.S)
    out = re.sub(r"```+([^`]+)```+", r"<pre class=\"shell\">\1</pre>", out, flags=re.S)
    out = re.sub(r"`([^`]+)`", r"<code>\1</code>", out)
    out = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", out)
    out = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", out)
    if link_urls:
        out = _URL.sub(lambda m: f'<a href="{m.group(1)}">{m.group(1)}</a>', out)
    return out
