#!/usr/bin/env python3
"""Generate /resources/ — the index, 34 resource pages, the dead list, the verification page.

    python3 admin/build/gen_resources.py

Source of truth is data/industry-resources.json; nothing here invents a fact. The only
editorial content added by this file is the ranked top ten and the three start-here
routes, both of which come from briefs/04__job-b__industry-resources.md and are kept
here rather than in the data because they are opinions, not facts about the resources.

The one rule this generator enforces without exception: every page carries a
`data-verified` stamp. validate.js fails the build if one does not. A list of links is
worth very little in an ecosystem where the community's own indexes list five dead
things as live; a list of links with a date on it is the whole point.
"""
import json
import re
from pathlib import Path

from shell import ROOT, crumb, esc, load, md_inline, page, plain, slugify, write

VERIFIED = "2026-08-23"  # the date the resource research in briefs/04__ was compiled

# --- editorial: the ranked top ten, from briefs/04__ §3 --------------------
TOP_TEN = [
    ("Wardley Maps — the book (Medium serialisation)",
     "The primary source, and the chapter that establishes <em>why</em> before <em>how</em>. "
     "The CC BY-SA 4.0 licence on it is what makes the whole ecosystem exist."),
    ("Learn Wardley Mapping (LearnWardleyMapping.com) — Ben Mosior / Hired Thought",
     "The pedagogy the book lacks. The free reference alone — especially the four-phase "
     "doctrine grid — is the fastest route from confusion to competence."),
    ("Crossing the River by Feeling the Stones (talk)",
     "Forty-eight free minutes of Wardley doing the thing. The highest-conversion artefact "
     "in the list: people who bounce off the book do not bounce off this."),
    ("OnlineWardleyMaps (OWM)",
     "You do not understand mapping until you have drawn one. Also the format standard the "
     "whole ecosystem targets, so learning its DSL is not tool lock-in."),
    ("awesome-wardley-maps",
     "The community index, and the only major resource under CC0 — so also the only one you "
     "can freely reuse as a base. Five of its entries are dead; ours says which."),
    ("WardleyMaps.com — Chris (Krzysztof) Daniel",
     "Home of Wardley Mapping 101 — the best free fifteen-minute end-to-end worked example, "
     "one sustained case study rather than a tour of features."),
    ("What do Wardley maps really map? A settler writes (critique)",
     "Read the strongest objection early, before over-committing. The consensus-versus-"
     "evolution argument will change how you use the technique — and it is the argument "
     "this site's <a href=\"../agents/index.html\">agent guardrail</a> is built on."),
    ("Wardley Maps in Mermaid (`wardley-beta`)",
     "The most consequential recent development: maps in git, in pull requests, in "
     "documentation, with no tool at all. See <a href=\"../maps/index.html\">the gallery</a>."),
    ("Simon Wardley's map repository",
     "147 real maps across 22 industries. Twenty of these teach more than two more chapters. "
     "⚠️ Licence contradictory — link, do not mirror."),
    ("Where the map ends: understanding Wardley maps' limitations (critique)",
     "The four structural limitations, stated fairly. The thing that stops mapping "
     "becoming a religion."),
]

# --- editorial: the three start-here routes, from briefs/04__ §5 -----------
ROUTES = [
    ("newcomer", "You have never drawn one",
     "Roughly four hours, in this order. The third step is the one people skip and the "
     "only one that actually teaches anything.",
     [("WardleyMaps.com — Chris (Krzysztof) Daniel", "Wardley Mapping 101 — fifteen minutes, one sustained worked example."),
      ("Crossing the River by Feeling the Stones (talk)", "Forty-eight minutes. Free. Watch Wardley reason with a map rather than present one."),
      ("OnlineWardleyMaps (OWM)", "<b>Now draw one.</b> Map something you already understand deeply — <em>not</em> your company, where you will confuse what you wish were true with what is."),
      ("The Wardley Mapping Canvas", "Use it as the process for that first map: needs, then chain, then position."),
      ("Learn Wardley Mapping (LearnWardleyMapping.com) — Ben Mosior / Hired Thought", "The free reference, then the doctrine grid — self-assess against Phase 1 only."),
      ("Wardley Maps — the book (Medium serialisation)", "Chapters 1–6. Stop there for now; the rest keeps."),
      ("What do Wardley maps really map? A settler writes (critique)", "<b>Before you evangelise.</b> The strongest objection, from someone sympathetic."),
      ("Map Camp", "Discord via mapcamp.co.uk — and put <b>12 November 2026</b> in the diary."),
      ]),
    ("security", "You work in security",
     "Mapping is the missing half of threat modelling — a claim made on this site's own "
     "chronology in <a href=\"../dinis/index.html#a19\">March 2022</a> and never followed up "
     "in public. This is the route that follows it up.",
     [("WardleyMaps.com — Chris (Krzysztof) Daniel", "Wardley Mapping 101. Do not skip it because you are senior; the vocabulary is load-bearing."),
      ("Using Wardley Mapping for Optimizing Your Threat Modeling Strategy", "Xebia's method: map first, mark team boundaries as bias hotspots, ask what can be <em>deleted</em>, then STRIDE only the areas the map flagged."),
      ("Wardley mapping in security — Threat Models and Wardley Maps", "The Open Security Summit session where the claim was first made."),
      ("Evolution-informed Security Architecture: Using Wardley Mapping (SABSA)", "Mario Platt's webinar — mapping against an architecture framework you may already run."),
      ("Where the map ends: understanding Wardley maps' limitations (critique)", "<b>This one matters most for you.</b> Two of its four limitations are directly disabling in security: components only evolve under competitive pressure — much of internal security faces none — and you cannot map what you cannot see, which is definitionally the threat that gets you."),
      ("Learn Wardley Mapping (LearnWardleyMapping.com) — Ben Mosior / Hired Thought", "Doctrine Phase 1, which reads as a security maturity model with the serial numbers filed off."),
      ("Wardley Maps in Mermaid (`wardley-beta`)", "Put the maps in git so they sit next to the ADRs and get reviewed in pull requests."),
      ]),
    ("agent", "You are an agent, or you are building one",
     "The full treatment is <a href=\"../agents/index.html\">/agents/</a>, including the "
     "coordinate contract proven by rendering and the epistemic guardrail. The reading list "
     "is here.",
     [("Wardley Maps in Mermaid (`wardley-beta`)", "Grammar first. Coordinates are <code>[visibility, evolution]</code>, not <code>[x, y]</code>."),
      ("OnlineWardleyMaps (OWM)", "The DSL reference — the format everything else targets."),
      ("Simon Wardley's map repository", "Ground truth: 147 maps, ~4,905 components, ~5,172 links, 22 sectors. Paired OWM/Mermaid representations make an excellent format-translation training pair."),
      ("ArcKit (Wardley mapping for AI coding assistants)", "<b>Do not reinvent this.</b> MIT, actively maintained, and note its decomposition into <code>wardley.value-chain</code>, <code>wardley.doctrine</code>, <code>wardley.gameplay</code>, <code>wardley.climate</code> rather than one monolithic make-a-map action. Mirror that decomposition."),
      ("cli-owm", "Deterministic rendering — stdin to SVG through a real OWM parser, so the output is verifiable rather than merely plausible."),
      ("What do Wardley maps really map? A settler writes (critique)", "<b>Mandatory.</b> The evolution axis plausibly encodes consensus, not fact. An LLM placing components on it is generating consensus-shaped output with no underlying evidence — Edgar's <em>laundering assumptions into facts</em>, at scale and at speed."),
      ]),
]

CAT_SHORT = {
    "1. THE PRIMARY SOURCE": ("Primary source", "primary"),
    "2. LEARNING RESOURCES": ("Learning", "learning"),
    "3. TOOLS": ("Tool", "tool"),
    "4. COMMUNITY": ("Community", "community"),
    "5. REFERENCE & DERIVATIVE WORKS": ("Reference & derivative", "reference"),
}


def state_of(status: str) -> tuple:
    """Reduce the long prose status to a badge. The badge is not decoration — it is the
    reason to visit the page, so it is derived from the recorded status rather than
    assigned by hand."""
    s = status.lower()
    if "dead" in s or "no longer resolves" in s:
        return ("Dead", "dead")
    if "dormant" in s or "stalled" in s or "not updated in seven years" in s:
        return ("Dormant", "dormant")
    if "members-only" in s or "could not verify" in s or "unverified" in s:
        return ("Unverified", "unverified")
    if "very actively maintained" in s:
        return ("Very active", "active")
    if "actively maintained" in s or "alive and returning" in s:
        return ("Active", "active")
    if "low-activity" in s or "very new" in s or "low-velocity" in s:
        return ("Low activity", "quiet")
    return ("Live", "live")


def shot_for(res, targets, captured, shots_dir: Path):
    """Match a resource to a usable captured screenshot, by URL then by name.

    "Usable" excludes a capture that succeeded technically and photographed a Cloudflare
    interstitial rather than the page. Three of the thirty did. Presenting one of those as
    a screenshot of the resource would be the exact failure this section is meant to fix."""
    def usable(t):
        rec = captured.get(t["id"])
        return bool(rec) and not rec.get("blocked") and (shots_dir / (rec.get("file") or "")).exists()

    want = (res.get("screenshot_target") or res["best_link"] or res["url"]).split(" (")[0].strip()
    for t in targets:
        if usable(t) and t["url"].rstrip("/") == want.rstrip("/"):
            return t
    for t in targets:
        if usable(t) and t["name"].split(" — ")[0].lower()[:18] in res["name"].lower():
            return t
    return None


def field(label, value, *, link=False):
    """`link=True` means "this field is expected to be a URL" — but several of them carry
    prose around the URL ("Directory at https://…", "Cheat sheet — https://…"). Rendering
    that as one href produces a link to a filename with a space in it, which the release
    gate correctly refuses to publish. So: linkify only a bare URL, and let md_inline pick
    the URLs out of anything else."""
    if not value:
        return ""
    v = value.strip()
    if link and re.fullmatch(r"https?://\S+", v):
        v = f'<a href="{esc(v)}">{esc(v)}</a>'
    else:
        v = md_inline(value)
    return f"<tr><th>{esc(label)}</th><td>{v}</td></tr>"


def resource_page(res, rank, why, targets, captured, shots_dir):
    slug = slugify(res["name"])
    rel = f"resources/{slug}.html"
    cat_label, cat_key = CAT_SHORT[res["category"]]
    state_label, state_key = state_of(res["status"])
    url = res["url"].split(" (")[0].strip()

    shot = shot_for(res, targets, captured, shots_dir)
    shot_html = ""
    if shot:
        rec = captured[shot["id"]]
        when = (rec.get("capturedAt") or "")[:10]
        f = esc(rec.get("file") or f"{shot['id']}.webp")
        shot_html = f"""
<figure class="shot">
  <a href="../screenshots/{f}"><img src="../screenshots/{f}"
     alt="Screenshot of {esc(shot['name'])}" loading="lazy"></a>
  <figcaption>{esc(shot['name'])} — captured {esc(when or VERIFIED)}{
      ', HTTP ' + str(rec['status']) if rec.get('status') else ''}.
    {esc(rec.get('derivative') or '')}
    <span class="attr">{esc(shot['attribution'])}</span></figcaption>
</figure>"""
    else:
        shot_html = ('<p class="note"><b>No screenshot.</b> Either this resource is not in the '
                     '30-target capture set, or the capture returned an interstitial rather than '
                     'the page — which is recorded as a failure rather than published as a '
                     'screenshot. <a href="verification.html">What was and was not '
                     'captured</a>.</p>')

    rank_html = ""
    if rank:
        rank_html = (f'<p class="claim"><b>#{rank} of the ten to read first.</b> {why}</p>')

    body = f"""{crumb('../', ('Resources', 'resources/index.html'), res['name'].split(' — ')[0])}
<h1>{md_inline(res['name'], link_urls=False)}</h1>
<p class="badges"><span class="badge b-{cat_key}">{esc(cat_label)}</span>
  <span class="badge s-{state_key}">{esc(state_label)}</span>
  <span class="badge b-type">{esc(res['type'])}</span></p>
{rank_html}
{shot_html}

<h2>What it is</h2>
<p>{md_inline(res['what_it_is'])}</p>

<h2>Limitations</h2>
<p>{md_inline(res['limitations'])}</p>

<h2>The details</h2>
<div class="tablewrap"><table class="rfields">
{field('Maintainer', res.get('maintainer'))}
{field('Started', res.get('started'))}
{field('Status, August 2026', res.get('status'))}
{field('Licence', res.get('licence'))}
{field('Home', url, link=True)}
{field('Best single link', res.get('best_link'), link=True)}
</table></div>

<div class="verify" data-verified="{VERIFIED}">
  <p><b>Verified {VERIFIED}</b> — status, licence and links checked against the source on that
  date. The site re-checks every URL it publishes on a schedule and
  <a href="verification.html">publishes the run</a>, successes and failures alike.</p>
  <p class="attr"><b>Attribution.</b> {md_inline(res['attribution'])}</p>
</div>

<div class="pagenav">
  <a href="index.html">← All 34 resources</a>
  <a href="dead/index.html">The 11 dead or dying →</a>
</div>"""

    write(rel, page(rel,
                    f"{res['name'].split(' — ')[0]} · resources · wardley-maps.sgit.ai",
                    (plain(res["what_it_is"])[:180].rsplit(" ", 1)[0] + "…"),
                    body,
                    og_title=f"{res['name'].split(' — ')[0]} — verified {VERIFIED}"))
    return slug, cat_label, cat_key, state_label, state_key


def main():
    # Wipe first. Slugs are derived from resource names, so a renamed resource leaves its
    # old page behind — a stale page that still validates, still has a canonical URL, and
    # still says "verified". On a site whose whole pitch is that the ecosystem's indexes
    # are out of date, shipping an orphan is the one unaffordable bug.
    for old in list((ROOT / "resources").glob("*.html")) + list((ROOT / "resources/dead").glob("*.html")):
        old.unlink()

    d = load("industry-resources.json")
    targets = json.loads((ROOT / "screenshots/targets.json").read_text())
    cap_file = ROOT / "screenshots/captured.json"
    captured = {}
    if cap_file.exists():
        raw = json.loads(cap_file.read_text())
        recs = raw.get("results", raw) if isinstance(raw, dict) else raw
        captured = {r["id"]: r for r in recs if isinstance(r, dict) and r.get("ok")}
    shots_dir = ROOT / "screenshots"

    top = {name: (i + 1, why) for i, (name, why) in enumerate(TOP_TEN)}
    by_name = {r["name"]: r for r in d["resources"]}
    for name in top:
        if name not in by_name:
            raise SystemExit(f"top-ten entry not found in the data: {name!r}")

    made = []
    for res in d["resources"]:
        rank, why = top.get(res["name"], (None, None))
        made.append((res, *resource_page(res, rank, why, targets, captured, shots_dir)))

    slug_of = {res["name"]: slug for res, slug, *_ in made}

    # --- the index --------------------------------------------------------
    routes_html = ""
    for key, heading, blurb, steps in ROUTES:
        items = "\n".join(
            f'  <li><a href="{slug_of[n]}.html">{md_inline(by_name[n]["name"].split(" — ")[0], link_urls=False)}</a>'
            f' — {note}</li>'
            for n, note in steps)
        routes_html += f"""
<section class="route" id="{key}">
  <h3>{heading}</h3>
  <p class="blurb">{blurb}</p>
  <ol class="path">
{items}
  </ol>
</section>"""

    ten = "\n".join(
        f'  <li><a href="{slug_of[n]}.html">{md_inline(by_name[n]["name"].split(" — ")[0], link_urls=False)}</a>'
        f' — {why}</li>'
        for n, why in TOP_TEN)

    by_cat = {}
    for res, slug, cat_label, cat_key, state_label, state_key in made:
        by_cat.setdefault((res["category"], cat_label, cat_key), []).append(
            (res, slug, state_label, state_key))
    cats_html = ""
    for (category, cat_label, cat_key), rows in sorted(by_cat.items()):
        trs = "\n".join(
            f'    <tr><td><a href="{slug}.html">{md_inline(res["name"], link_urls=False)}</a></td>'
            f'<td class="dim">{esc(res["type"])}</td>'
            f'<td><span class="badge s-{state_key}">{esc(state_label)}</span></td>'
            f'<td class="dim small">{esc(res.get("maintainer") or "—")}</td></tr>'
            for res, slug, state_label, state_key in sorted(rows, key=lambda r: r[0]["name"]))
        cats_html += f"""
<h3 id="{cat_key}">{esc(cat_label)} <span class="dim">{len(rows)}</span></h3>
<div class="tablewrap"><table>
  <thead><tr><th>Resource</th><th>Type</th><th>State</th><th>Maintainer</th></tr></thead>
  <tbody>
{trs}
  </tbody>
</table></div>"""

    rel = "resources/index.html"
    body = f"""{crumb('../', 'Resources')}
<h1>34 industry resources, verified rather than listed</h1>
<p class="lead">Not "here are some links". <b>Here is every link, checked on a stated date, with
what is actually dead.</b> As of August 2026 the community's own canonical indexes are wrong:
<a href="dead/index.html">five dead things</a> are still listed as live by
<code>awesome-wardley-maps</code>, by Wikipedia, and in two cases by Simon Wardley's own
resources page.</p>

<p class="claim">That is a low bar and a real service. A site that verifies every link and
publishes the verification date is immediately more useful than the community's index — so
this one does, on a schedule, and <a href="verification.html">publishes the run</a>.</p>

<div class="note"><b>The practice is healthy; the link layer rotted.</b> Map Camp is returning
after a two-year gap with a workshop on <b>12 November 2026</b> and a full conference in 2027,
Mermaid support has made maps native to git, OnlineWardleyMaps got a full rewrite in 2025, and
ArcKit is bringing mapping into agentic workflows with real adoption. What died is the
directory, not the technique. Which is fixable, and fixing it is a good reason for this page
to exist.</div>

<p class="verify" data-verified="{VERIFIED}"><b>Every page below verified {VERIFIED}</b>
— status, licence and links checked against the source on that date, and re-checked on a
schedule since. <a href="verification.html">The runs →</a></p>

<h2 id="start">Three ways in</h2>
<p>A flat A–Z is the wrong primary navigation for 34 things when a reader's actual question is
"where do <em>I</em> start". Three routes, then the list.</p>
{routes_html}

<h2 id="ten">If you only look at ten</h2>
<p>In this order.</p>
<ol class="path ranked">
{ten}
</ol>

<h2 id="all">All 34, by category</h2>
<p class="small dim">Every row links to a page carrying the same nine fields: what it is, its
limitations stated plainly, maintainer, start date, status in August 2026, exact licence, the
best single link, a dated screenshot where one could be captured, and the pre-written
attribution string. A page with no limitations section is marketing.</p>
{cats_html}

<h2 id="licence">Before you copy anything</h2>
<p><b>The Wardley ecosystem is CC BY-SA. This site is CC BY. Those do not mix cleanly.</b>
ShareAlike is viral: publish an <em>adaptation</em> of CC BY-SA material and that page must
itself be CC BY-SA 4.0. Quoting and linking are fine; adapting is what binds you. Six resources
carry a flagged or contradictory licence and are link-only until resolved —
<a href="../about/licensing.html">the full treatment, including which six</a>.</p>

<div class="pagenav">
  <a href="../start/index.html">← Start here</a>
  <a href="dead/index.html">The 11 dead or dying →</a>
</div>"""
    write(rel, page(rel,
                    "34 Wardley Mapping resources, verified — wardley-maps.sgit.ai",
                    "Every significant Wardley Mapping resource with a page each: what it is, "
                    "its limitations, maintainer, licence, best link and a verification date. "
                    "Five things the community's own indexes list as live are dead.",
                    body,
                    og_title="34 Wardley Mapping resources, verified in August 2026"))

    # --- the dead list ----------------------------------------------------
    dead_rows = ""
    for x in d["dead_or_dying"]:
        listed = x.get("still_listed_as_live_by") or []
        listed_html = ("<ul class='wrong'>" + "".join(f"<li>{esc(s)}</li>" for s in listed) + "</ul>"
                       if listed else '<span class="dim">—</span>')
        dead_rows += f"""
  <article class="obit">
    <h3>{md_inline(x['name'], link_urls=False)} <span class="badge s-dead">{esc(x['status'].split(' — ')[0])}</span></h3>
    <p class="small dim">{md_inline(x['status'])}{' · built by ' + esc(x['by']) if x.get('by') else ''}
      {'· <code>' + esc(x['url']) + '</code>' if x.get('url') else ''}</p>
    <p>{md_inline(x['why'])}</p>
    {'<p class="small"><b>Where to go instead.</b> ' + md_inline(x['migration']) + '</p>' if x.get('migration') else ''}
    <div class="stillwrong"><b>Still listed as live by</b>{listed_html}</div>
  </article>"""

    rel = "resources/dead/index.html"
    body = f"""{crumb('../../', ('Resources', 'resources/index.html'), 'Dead or dying')}
<h1>Eleven things that are dead, and who still says they are not</h1>
<p class="lead">An obituary list is not a cheap shot. In an ecosystem whose canonical indexes
are wrong, recording what died and when — with the date, and with credit to whoever built it —
is the useful thing to do. Five of these are still listed as live by
<code>awesome-wardley-maps</code>, by Wikipedia, and in two cases by Simon Wardley's own
resources page.</p>

<p class="claim">The sharpest one: <b>MapKeep</b> was the only tool with genuine real-time
multiplayer collaboration, and it ceased on 30 May 2026. Its loss is a capability gap, not an
inconvenience. Credit to Tristan Slominski for building it, and for shipping OWM export so the
maps outlived the tool.</p>

<p class="verify" data-verified="{VERIFIED}"><b>Verified {VERIFIED}.</b> Every death below
was confirmed by fetching on that date. <a href="../verification.html">The runs →</a></p>

<div class="note"><b>Two Map Camp domains contradict each other.</b> <code>map-camp.com</code>
stops at September 2024 and advertises the dead Slack invite; <code>mapcamp.co.uk</code> carries
the current position — a workshop on <b>12 November 2026</b> and Map Camp 2027. A visitor
landing on the <code>.com</code> will reasonably conclude the conference is dead. It is not.
<b>Always link <code>mapcamp.co.uk</code>.</b></div>

{dead_rows}

<h2>And one live gap worth naming</h2>
<p>There is currently <b>no working doctrine assessment tool anywhere in the ecosystem</b>.
Both are dead and <code>awesome-wardley-maps</code> still lists them. This site hosts a working
40-record assessment with the evidence attached to every rating, and publishes
<a href="../../doctrine/doctrine.json">its JSON</a> as a stable endpoint —
<a href="../../doctrine/index.html">the doctrine page</a>. A public schema plus a worked example
is not a tool. It is the closest thing to one that currently exists, and it costs nothing extra.</p>

<div class="pagenav">
  <a href="../index.html">← All 34 resources</a>
  <a href="../verification.html">The link-verification run →</a>
</div>"""
    write(rel, page(rel,
                    "Dead or dying — 11 Wardley resources, and who still lists them as live",
                    "MapKeep, MapScript, both doctrine assessment tools, the Map Camp Slack "
                    "invite and the Leading Edge Forum course are dead. awesome-wardley-maps, "
                    "Wikipedia and Simon Wardley's own resources page still list them as live.",
                    body))

    # --- the verification page -------------------------------------------
    rel = "resources/verification.html"
    body = f"""{crumb('../', ('Resources', 'resources/index.html'), 'Link verification')}
<h1>The link-verification run</h1>
<p class="lead">Every external URL this site publishes is fetched on a schedule, and the run is
published — <b>failures and skips included</b>. This page renders
<a href="../data/link-check.json"><code>/data/link-check.json</code></a>, which is written by
<code>bin/verify-links.js</code> from a GitHub Actions job every Monday and on demand.</p>

<p class="claim">No sibling site in this network has one. This site needs one, because it spends
a page telling you that <code>awesome-wardley-maps</code>, Wikipedia and Simon Wardley's own
resources page all list five dead things as live. A site that makes that criticism and does not
check its own links has no standing to make it.</p>

<div id="lc"><p class="dim">Loading the verification report…</p></div>

<h2 id="method">Method, and what "verified" does not mean</h2>
<ul>
  <li><b>HEAD first, then GET.</b> A good number of hosts refuse HEAD and serve GET, so a
    HEAD failure is not recorded as a result.</li>
  <li><b>Redirects are followed and the final URL is recorded.</b> A link that now lands
    somewhere else shows as a redirect rather than silently passing — which is how the
    Teachable course deep links were caught: they return 302 to a login wall, not 404.</li>
  <li><b>Hosts that block automated retrieval are recorded as skipped, never as ok.</b>
    LinkedIn, SlideShare, YouTube and Discord are on that list. Claiming a 200 that was not
    received would be worse than admitting the check cannot be made. Those need a human.</li>
  <li><b>A 401, 403, 429, 451 or 999 is <em>blocked</em>, not <em>failed</em>.</b> Medium serves
    403 to anything without a browser, and every chapter of the book is on Medium. Calling
    twenty live chapters dead links would make this report wrong in exactly the way it exists to
    complain about. <b>Blocked means we could not check.</b> Only a 404, a 5xx or a connection
    failure means the link is broken.</li>
  <li><b>Our own host is skipped.</b> Internal links are checked by
    <a href="../admin/build/validate.js">the release gate</a> against the files on disk, which is
    a stronger check than fetching a deployment that may not have happened yet — and it runs
    before every publish rather than weekly.</li>
  <li><b>A dead link does not fail the build.</b> The point of the job is that links rot; a red
    pipeline would tempt somebody to delete the evidence rather than record it.</li>
</ul>
<p><b>What a green row means:</b> the URL responded. It does not mean the content is still what
it was, that the project is maintained, or that the licence has not changed. Those are the
<a href="index.html">resource pages</a>' job, and they carry their own dated verification.</p>

<h2 id="screenshots">The screenshots, and the three that are not screenshots</h2>
<p>The same discipline applies to <a href="../screenshots/captured.json">the capture run</a>.
Thirty targets were attempted: <b>26 produced a usable image</b>, <b>one failed to load at
all</b>, and <b>three succeeded technically while photographing a Cloudflare interstitial rather
than the page</b>. Those three are recorded as blocked and no page presents one as a screenshot
of the resource — a picture of a bot-check is not evidence of anything except a bot-check.
Every published image records the capture timestamp, the HTTP status, the original pixel
dimensions and the fact that the published file is a resized WebP derivative of the PNG that
was captured.</p>

<div class="pagenav">
  <a href="index.html">← All 34 resources</a>
  <a href="dead/index.html">The 11 dead or dying →</a>
</div>

<script src="../assets/linkcheck.js" defer></script>"""
    write(rel, page(rel,
                    "The link-verification run — every URL, checked and dated",
                    "Every external URL this site publishes is fetched on a schedule and the "
                    "result published, failures and skips included. Hosts that block automated "
                    "retrieval are recorded as skipped, never as ok.",
                    body))

    print(f"gen_resources: {len(made)} resource pages, index, dead list "
          f"({len(d['dead_or_dying'])} entries), verification page")


if __name__ == "__main__":
    main()
