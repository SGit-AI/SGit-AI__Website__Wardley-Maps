#!/usr/bin/env python3
"""Bump the site version, exactly once per release, in the two places that own it.

    bin/bump.py "what changed in this release"

Does three things and stops:
  1. admin/build/version.txt -> the next minor (or --major for vR.M+1.0)
  2. admin/versions.html     -> a new row at the top of the history table
  3. prints the commit subject CI requires

The pipeline enforces all of this from the other side: tag-release reads version.txt,
finds the commit whose subject carries the same version, and refuses to tag if the two
disagree or if the bump was not the next minor. Doing it by hand is how a release ends
up with a duplicated row in the table or a tag pointing at the wrong commit, both of
which have happened on sibling sites. So it is a script.

Run chrome.py afterwards — it propagates the new version to every page's badge, to
llms.txt, llms-full.txt and index.md, and validate.js fails the build if any of them
disagree.
"""
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION_FILE = ROOT / "admin/build/version.txt"
VERSIONS_HTML = ROOT / "admin/versions.html"


def main() -> int:
    args = [a for a in sys.argv[1:] if a != "--major"]
    major = "--major" in sys.argv[1:]
    if len(args) != 1:
        print(__doc__)
        return 2
    summary = args[0]

    cur = VERSION_FILE.read_text().strip()
    m = re.fullmatch(r"v(\d+)\.(\d+)\.(\d+)", cur)
    if not m:
        print(f"version.txt does not carry a vX.Y.Z version: {cur!r}", file=sys.stderr)
        return 1
    rel, maj, mnr = (int(x) for x in m.groups())
    new = f"v{rel}.{maj + 1}.0" if major else f"v{rel}.{maj}.{mnr + 1}"

    html = VERSIONS_HTML.read_text()
    if f'class="vnum">{new}<' in html:
        print(f"admin/versions.html already lists {new} — the version was not bumped", file=sys.stderr)
        return 1

    row = (f'    <tr><td class="vnum">{new}</td><td>{date.today().isoformat()}</td>'
           f'<td>{summary}</td></tr>\n')
    marker = "<!-- releases -->\n"
    if marker not in html:
        print(f"admin/versions.html has no '{marker.strip()}' marker to insert above", file=sys.stderr)
        return 1
    VERSIONS_HTML.write_text(html.replace(marker, marker + row, 1))
    VERSION_FILE.write_text(new + "\n")

    print(f"{cur} -> {new}")
    print(f"  · admin/build/version.txt")
    print(f"  · admin/versions.html (row added)")
    print()
    print("next:")
    print("  python3 admin/build/chrome.py")
    print("  node admin/build/validate.js")
    print(f'  git commit -am "site {new}: {summary}" && git push origin dev')
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
