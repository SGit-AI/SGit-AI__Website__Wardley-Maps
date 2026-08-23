#!/usr/bin/env bash
# Render every maps/*.mmd to maps/*.svg. Run from the repo root: bin/render-maps.sh
#
# The corpus described this pipeline in prose for three months — "Mermaid CLI v11.14.0
# plus the Playwright-bundled Chromium" — with no script, no make target and no CI job,
# and in that time zero of the thirteen wardley-beta sources in the source repo
# rendered. It is a script now. See briefs/05__maps-and-rendering.md §4.
#
# The grep at the end is the load-bearing line. A wardley-beta source with a bad name
# renders a "Syntax error in text" SVG: no error on stderr, exit status 0, and a
# byte-identical file every time. In a batch render that is indistinguishable from
# success until somebody opens the file, which is exactly how thirteen broken maps sat
# in a repo for three months. validate.js enforces the same check at release time.
#
# The parse rule that avoids the whole class of failure: quote every anchor and
# component name, in the declaration AND in every link and evolve line that references
# it. Unquoted, a hyphen, a dot or a slash in a name is a syntax error; quoting fixes
# all three, but quoting only the declaration still fails.
set -euo pipefail
cd "$(dirname "$0")/.."

MERMAID_VERSION="${MERMAID_VERSION:-11.14.0}"
CFG="$(mktemp -t puppeteer-config.XXXXXX.json)"
trap 'rm -f "$CFG"' EXIT

# Mermaid CLI bundles its own Puppeteer and will try to download Chrome. Point it at a
# Chromium that already exists instead — required in any sandbox without egress to
# Google's CDN, and faster everywhere else.
CHROME="${CHROME_PATH:-}"
if [ -z "$CHROME" ]; then
  for c in /opt/pw-browsers/chromium*/chrome-linux/chrome \
           /opt/pw-browsers/chromium/chrome \
           /usr/bin/chromium /usr/bin/chromium-browser /usr/bin/google-chrome; do
    [ -x "$c" ] && { CHROME="$c"; break; }
  done
fi
if [ -n "$CHROME" ]; then
  printf '{"executablePath":"%s","args":["--no-sandbox","--disable-dev-shm-usage"]}\n' "$CHROME" > "$CFG"
  echo "chromium: $CHROME"
else
  printf '{"args":["--no-sandbox","--disable-dev-shm-usage"]}\n' > "$CFG"
  echo "chromium: letting mermaid-cli find its own"
fi

fail=0
for f in maps/*.mmd; do
  out="${f%.mmd}.svg"
  echo "· $f -> $out"
  npx --yes "@mermaid-js/mermaid-cli@${MERMAID_VERSION}" \
      -i "$f" -o "$out" -p "$CFG" -b white -w 1400 -H 900 >/dev/null
  if grep -q 'error-text' "$out"; then
    echo "  ✗ FAILED: $f rendered a syntax error — check that every name is quoted everywhere"
    fail=1
  fi
done
[ "$fail" -eq 0 ] && echo "render-maps: OK — $(ls maps/*.mmd | wc -l) maps rendered"
exit "$fail"
