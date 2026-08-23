#!/usr/bin/env python3
"""Turn the raw capture PNGs into web-sized WebP, and record that it happened.

    bin/optimise-shots.py [--width 1200] [--max-height 4000] [--keep-png]

capture.js shoots at 1440×900 with a 2× device scale factor and `fullPage` on many
targets, which is right for a capture and wrong for a repository: the raw set is ~32 MB,
and a single full-page shot of a long documentation site runs to five megabytes.

This resizes to a sensible display width, caps runaway full-page heights, and writes
WebP — which handles screenshot text considerably better than JPEG at the same size.

The part that matters: **the transformation is recorded in captured.json**, per image,
with the original byte count and pixel dimensions. A screenshot on this site is offered
as evidence of what a page looked like on a date, so the fact that the published file is
a resized derivative of the capture belongs next to it rather than in a commit message.
"""
import argparse
import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SHOTS = ROOT / "screenshots"

# Titles that mean the capture succeeded technically and captured an interstitial rather
# than the page. Recorded as blocked so no page presents one as a screenshot of the
# resource — the whole value of a dated screenshot is that it shows the thing.
BLOCKED_TITLES = ("attention required", "just a moment", "access denied",
                  "are you a robot", "cloudflare", "403 forbidden")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--width", type=int, default=1200)
    ap.add_argument("--max-height", type=int, default=4000)
    ap.add_argument("--keep-png", action="store_true")
    args = ap.parse_args()

    recs = json.loads((SHOTS / "captured.json").read_text())
    saved_before = saved_after = 0

    for rec in recs:
        title = (rec.get("title") or "").lower()
        rec["blocked"] = bool(rec.get("ok")) and any(b in title for b in BLOCKED_TITLES)

        png = SHOTS / f"{rec['id']}.png"
        if not rec.get("ok") or not png.exists():
            continue

        with Image.open(png) as im:
            rec["source_px"] = list(im.size)
            im = im.convert("RGB")
            if im.width > args.width:
                im = im.resize((args.width, round(im.height * args.width / im.width)),
                               Image.LANCZOS)
            if im.height > args.max_height:
                rec["truncated_height"] = True
                im = im.crop((0, 0, im.width, args.max_height))
            webp = SHOTS / f"{rec['id']}.webp"
            im.save(webp, "WEBP", quality=82, method=6)

        saved_before += png.stat().st_size
        saved_after += webp.stat().st_size
        rec["source_bytes"] = png.stat().st_size
        rec["file"] = webp.name
        rec["bytes"] = webp.stat().st_size
        rec["published_px"] = list(Image.open(webp).size)
        rec["derivative"] = (
            f"Resized to {args.width}px wide and re-encoded as WebP q82 from the "
            f"{rec['source_px'][0]}×{rec['source_px'][1]} PNG capture"
            + (f", cropped to the first {args.max_height}px." if rec.get("truncated_height")
               else "."))
        if not args.keep_png:
            png.unlink()

    (SHOTS / "captured.json").write_text(json.dumps(recs, indent=2) + "\n")
    ok = sum(1 for r in recs if r.get("ok") and not r.get("blocked"))
    blocked = sum(1 for r in recs if r.get("blocked"))
    failed = sum(1 for r in recs if not r.get("ok"))
    print(f"optimise-shots: {ok} usable, {blocked} blocked by an interstitial, {failed} failed · "
          f"{saved_before/1e6:.1f} MB -> {saved_after/1e6:.1f} MB")


if __name__ == "__main__":
    main()
