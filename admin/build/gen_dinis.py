#!/usr/bin/env python3
"""Generate /dinis/ — the published record, 2018–2025, and the gap after it.

    python3 admin/build/gen_dinis.py

Source of truth is data/dinis-published.json — 26 items, each with a date-precision flag
because a good number of them are month-and-weekday only and synthesising an exact date
would be inventing evidence. The page renders that flag rather than hiding it.

The editorial frame — the four claims held for seven years, the two silences, the one
clause that is the only public bridge to the agentic work — is in
briefs/03__job-a__dinis-published-material.md and repeated here in the prose blocks.
"""
from collections import defaultdict

from shell import crumb, esc, load, md_inline, page, write

MONTHS = ["", "January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]

# The years with no output are the point of the page, so they are declared rather than
# inferred from missing rows — a gap you have to notice is a gap most readers will not.
SILENCES = {
    2021: ("Nothing published.", "The first silence. The 2020 peak — five sessions with Simon "
           "Wardley in the room, the Map Camp talk — is followed by a year with no output at all."),
    2023: ("Nothing published.", "The second silence, and the longer one in effect: 2024 is two "
           "panels and two shares of other people's work, and 2025 is a single clause."),
}

YEAR_NOTES = {
    2018: ("Founding", "Two blog posts, three Open Security Summit sessions, and the Medium seed "
           "piece. <b>The only year he organised a mapping track himself.</b>"),
    2019: ("Institutional", "The Wardley track runs without him organising it; mapping shows up "
           "inside an OWASP talk and inside a job advert."),
    2020: ("The peak", "Five working sessions with Simon Wardley in the room, plus the Map Camp "
           "talk and its deck. The <a href=\"#a11\">Team Topologies &amp; PST session</a> is the "
           "documented ancestor of everything on "
           "<a href=\"../patterns/pst/index.html\">/patterns/pst/</a>."),
    2022: ("The reflective phase", "Three sessions, including the only fully-authored solo piece "
           "and the flat statement that mapping is the missing half of threat modelling."),
    2024: ("Two panels, two shares", "The two LinkedIn items are <b>shares of other people's "
           "work, not original writing</b>. Presenting them otherwise would be a "
           "straightforward misattribution."),
    2025: ("One clause", "The only public link between seven years of security-era mapping and "
           "194 unpublished files of agentic-era mapping."),
}

FRAGILE = {
    "A15": "The only artefact of the Map Camp talk, behind a Cloudflare wall and unread. "
           "The biggest hole in the record — the crown-jewels thesis rests entirely on it.",
    "A06": "The repository this post describes is already a 404. Only the prose survives.",
    "A20": "LinkedIn: unfetchable, unarchivable, deletable — and a share, not a post.",
    "A21": "LinkedIn: unfetchable, unarchivable, deletable — and a share, not a post.",
}


def yt_id(url: str):
    if not url:
        return None
    if "watch?v=" in url:
        return url.split("watch?v=")[1].split("&")[0]
    return url.rstrip("/").rsplit("/", 1)[-1] or None


def when(item):
    d, p = item["date"], item["date_precision"]
    if not d:
        return ("—", p)
    parts = d.split("-")
    if len(parts) == 3:
        return (f"{int(parts[2])} {MONTHS[int(parts[1])]} {parts[0]}", p)
    if len(parts) == 2:
        return (f"{MONTHS[int(parts[1])]} {parts[0]}", p)
    return (d, p)


def main():
    d = load("dinis-published.json")
    items = d["items"]
    by_year = defaultdict(list)
    for it in items:
        y = int(it["date"][:4]) if it["date"] else None
        by_year[y].append(it)

    videos = [it for it in items if it.get("video") and it["id"] != "A26"]

    timeline = ""
    for year in sorted([y for y in by_year if y]):
        label, note = YEAR_NOTES.get(year, ("", ""))
        timeline += f'\n<section class="yr" id="y{year}">\n'
        timeline += (f'  <h3>{year} <span class="dim">{len(by_year[year])} item'
                     f'{"s" if len(by_year[year]) != 1 else ""}</span>'
                     f'{f" — <em>{label}</em>" if label else ""}</h3>\n')
        if note:
            timeline += f'  <p class="blurb">{note}</p>\n'
        for it in sorted(by_year[year], key=lambda x: (x["date"], x["id"])):
            date_str, prec = when(it)
            prec_note = ""
            if prec == "month":
                prec_note = ('<span class="prec" title="The session page carries a weekday but no '
                             'date, and the index renders a stale schedule table. Month and year '
                             'are what is established.">month precision</span>')
            elif prec.startswith("derived"):
                prec_note = ('<span class="prec" title="Derived from the LinkedIn activity id; '
                             'the page itself could not be fetched.">derived</span>')
            elif prec == "not established":
                prec_note = '<span class="prec bad">date not established</span>'
            vid = yt_id(it.get("video"))
            embed = ""
            if vid:
                embed = (f'\n      <div class="vid"><iframe loading="lazy" '
                         f'src="https://www.youtube-nocookie.com/embed/{esc(vid)}" '
                         f'title="{esc(it["title"])}" allowfullscreen '
                         f'referrerpolicy="strict-origin-when-cross-origin"></iframe></div>')
            frag = FRAGILE.get(it["id"])
            collab = it.get("collaborators") or []
            timeline += f"""  <article class="item{' unver' if not it.get('verified') else ''}" id="{it['id'].lower()}">
    <p class="imeta"><span class="idate">{esc(date_str)}</span> {prec_note}
      <span class="itype">{esc(it['type'])}</span>
      <span class="irole">{esc(it['role'])}</span>
      {'<span class="prec bad">not verified by fetching</span>' if not it.get('verified') else ''}</p>
    <h4><a href="{esc(it['url'])}">{esc(it['title'])}</a></h4>
    <p class="small dim">{esc(it['venue'])}{' · with ' + esc(', '.join(collab)) if collab else ''}</p>
    {f'<p class="inote">{md_inline(it["note"])}</p>' if it.get('note') else ''}
    {f'<p class="warnbox"><b>Fragile.</b> {frag}</p>' if frag else ''}{embed}
  </article>\n"""
        timeline += "</section>\n"
        for sy, (head, txt) in SILENCES.items():
            if sy == year + 1:
                timeline += (f'\n<section class="yr silence" id="y{sy}">\n'
                             f'  <h3>{sy} <span class="dim">0 items</span></h3>\n'
                             f'  <p class="blurb"><b>{head}</b> {txt}</p>\n</section>\n')

    standing = [it for it in items if not it["date"]]
    standing_html = "\n".join(
        f'  <li><a href="{esc(it["url"])}">{esc(it["title"])}</a> — {md_inline(it.get("note") or "")}'
        f'{" <b>Participation unconfirmed; listed here rather than claimed.</b>" if it["role"] == "UNCONFIRMED" else ""}</li>'
        for it in standing)

    rel = "dinis/index.html"
    body = f"""{crumb('../', 'Dinis Cruz on mapping')}
<h1>Dinis Cruz on Wardley Mapping, 2018–2025</h1>
<p class="lead">Twenty-six published items over seven years, then a stop. Twenty-two were
verified by fetching them; four could not be — SlideShare and LinkedIn block automated
retrieval, and nothing here routes around a block. The unverified four say so on their face.</p>

<p class="claim">The headline is the last row of the table below. <b>The public record stops in
2025 and the private record starts in 2026.</b> Job A found 26 published items ending in a
single clause; the same research found 194 unpublished files of agentic-era mapping beginning
five months later. The only public link between the two eras is
<a href="#a24">that one clause, in one co-authored article</a>. This site does not report that
bridge. It is the bridge — which means it is making a claim, not describing one.</p>

<div class="tablewrap"><table>
  <thead><tr><th>Period</th><th>Output</th><th>Character</th></tr></thead>
  <tbody>
    <tr><td><a href="#y2018">2018</a></td><td>6 items</td><td>Founding. The only year he organised a mapping track himself.</td></tr>
    <tr><td><a href="#y2019">2019</a></td><td>3 items</td><td>Institutional. The track runs without him.</td></tr>
    <tr><td><a href="#y2020">2020</a></td><td>7 items</td><td><b>The peak.</b> Five sessions with Simon Wardley, plus Map Camp.</td></tr>
    <tr><td><a href="#y2021">2021</a></td><td><b>0</b></td><td>Silence.</td></tr>
    <tr><td><a href="#y2022">2022</a></td><td>3 items</td><td>The reflective phase — the only solo fully-authored piece.</td></tr>
    <tr><td><a href="#y2023">2023</a></td><td><b>0</b></td><td>Silence.</td></tr>
    <tr><td><a href="#y2024">2024</a></td><td>4 items</td><td>Two panels, two <em>shares</em> of other people's work.</td></tr>
    <tr><td><a href="#y2025">2025</a></td><td>1 item</td><td>One clause in one co-authored article.</td></tr>
    <tr><td>2026</td><td><b>0 published</b></td><td>~194 files of unpublished Wardley thinking. <a href="../method/index.html">Four of them are now pages here.</a></td></tr>
  </tbody>
</table></div>

<h2 id="throughline">Four claims, held for seven years</h2>

<h3>2018 — diagrams must become maps</h3>
<p>The Medium post of 7 October 2018 is the intellectual seed and the clearest statement of the
whole position:</p>
<blockquote class="challenge">in most development teams, we are still at the "Why do we need
up-to-date diagrams?" phase. Where the question that we should be looking at is "How can we
make our diagrams every better and more valuable?" And the answer is Maps, which are diagrams
with the following properties — are visual — have context (i.e. specific to purpose /
perspective) — are mode of components — have at least one anchor — have a position (relative to
anchor) — have a consistency of movement</blockquote>
<p>with the complaint that ordinary architecture diagrams <em>"miss the key mapping properties
of: anchor, position (relative to anchor) and consistency of movement."</em></p>

<h3>2018 — maps should be generated, not drawn</h3>
<p><a href="#a06"><em>Creating Wardley Maps using Lambda Functions</em></a> opens on the
frustration of not being able to <em>"programatically create the maps (ideally via [a] DSL or
something like DOT language)"</em> and ends with a map generated inside a Lambda from
programmatic values. <b>That is the same instinct that, in May 2026, becomes Mermaid
<code>wardley-beta</code> in git</b> — eight years apart, one idea. The ending of that story is
that the 2018 repository is now a 404 and
<a href="../maps/index.html">the 2026 version renders</a>.</p>

<h3>2018–2020 — context is the security asset</h3>
<p>The 2018 session deliberately mapped a cup of tea <em>and</em> an AWS attack in the same
hour, and the outcomes page records the argument over <em>"whether the tea picker was
visible"</em> as the teaching moment — position is contested, and that is the point. It becomes
a title in October 2020: <b>"Why context is your crown jewels."</b> In security, <em>crown
jewels</em> means data assets; the talk inverts it — the contextual understanding of your value
chain is the jewel.</p>

<h3>2020–2022 — mapping is the missing half of threat modelling</h3>
<p>Stated flatly in the March 2022 session abstract: <em>"Wardley Maps could be the missing
piece of the puzzle when doing Threat Models."</em> Never followed up in public. The
<a href="../resources/index.html#security">security route through the resources</a> is this
site's attempt to follow it up.</p>

<h3 id="a24-hinge">And the hinge into AI, 2025</h3>
<blockquote class="challenge">MCP represents the <b>commoditization of LLM-to-tool
interfaces</b>, which in turn enables higher-level constructs and rapid innovation (a concept
noted in Wardley Maps' <b>Innovate-Leverage-Commoditize</b> cycle). We are currently in the
<b>"Genesis and Custom Build" phase</b> of agents using MCP…</blockquote>
<p>One clause, co-authored, three years after the last substantive output.
<b>Do not read this site as though a public position on agentic mapping already exists.</b>
It does not. Creating one is what the site is for.</p>

<h2 id="ancestor">The direct ancestor</h2>
<p class="claim"><b>16 June 2020 — <a href="#a11">Team Topologies &amp; PST &amp; Squads &amp;
Tribes</a></b>, with Simon Wardley, Tony Richards and Luke Robbertse. Six years later,
<code>__Send</code> runs three agent teams named Explorer, Villager and Town Planner. The 2026
pattern has a documented 2020 origin with Wardley himself in the conversation, and nobody has
ever put the two side by side. <a href="../patterns/pst/index.html">This site does →</a></p>
<p>Supporting evidence from the same period: the <a href="#a09">December 2019 hiring post</a>
requires candidates to build and present a Wardley Map — <em>"about an industry, about you or
even about a cup of coffee… we also want to see the candidate's experience of creating that
map, the thought process and the learning experience"</em> — and lists Wardley alongside Spotify
Squads, Team Topologies and Cynefin. The cup-of-coffee motif carries straight from the 2018 cup
of tea.</p>

<h2 id="chronology">The chronology</h2>
<p class="small dim">Every item links to its source. Items with month precision say so: the
Open Security Summit mini-summit pages carry a weekday but no date, and every mini-summit index
renders the same stale schedule table — March 2022, July 2022 and September 2024 all show
identical columns. <b>No exact dates were synthesised.</b></p>
{timeline}

<h2 id="standing">Not events</h2>
<ul>
{standing_html}
</ul>

<h2 id="recordings">The recordings</h2>
<p>{len(videos)} recordings, all resolving live in August 2026, all on the Open Security Summit
channel and embedded above via <code>youtube-nocookie</code>. Three more from the wider track
are worth the same shelf and are not Dinis's: <em>Wardley Maps First Aid</em> (Petra Vukmirovic
— note it is dated 5 June 2020 by its own title despite living under a <code>/may/</code> URL
path, because the 2020 summit slipped from May to June and the URLs never moved),
<em>Wardley Maps and services model at Glasswall</em> (Steve Purkis), and <em>Maturity
Mapping</em> (Chris McDermott).</p>

<h2 id="archive">What should be archived before it disappears</h2>
<p>This site should not link to fragile things without mirroring them, and it currently does.
Stated as a debt rather than done: see <a href="../admin/comms.html">the task list</a>.</p>
<ol>
  <li><b>The SlideShare deck (A15).</b> The only artefact of the Map Camp talk, and the sole
    source for the crown-jewels thesis. Export to PDF from a real browser and mirror it.</li>
  <li><b>The year-subdomains</b> — <code>2018.</code>, <code>2019.</code>,
    <code>2020.open-security-summit.org</code>. Separate deployments holding participant lists,
    outcomes and session notes the current site lacks; the canonical index says outright that
    <em>"this list of events and sessions is not complete."</em> The 2018 Maps and Graphs track —
    the only one Dinis organised — has no presence on the current site at all.</li>
  <li><b>The two LinkedIn posts.</b> Unfetchable, unarchivable, deletable, and the only evidence
    of 2024 activity. And label them accurately: both are shares.</li>
  <li><b>The two blog posts.</b> The Blogger feed API confirms the <code>Wardley_Maps</code>
    label holds exactly two entries — that label <em>is</em> the complete list of his Wardley
    blogging.</li>
  <li><b>Dying links inside the session pages themselves</b> — a heysummit registration that now
    reads "This event is not live yet", Zoom links with passwords in the URL, a
    <code>join.slack.com</code> invite, and Google Slides <code>/e/2PACX-…/embed</code> links
    that break the instant the owner unpublishes.</li>
</ol>

<div class="pagenav">
  <a href="../resources/index.html">← The industry resources</a>
  <a href="../patterns/pst/index.html">Explorer / Villager / Town Planner →</a>
</div>"""

    write(rel, page(rel,
                    "Dinis Cruz on Wardley Mapping, 2018–2025 — the published record",
                    "Twenty-six published items over seven years, two silent years, and the "
                    "single clause that is the only public bridge between seven years of "
                    "security-era mapping and 194 unpublished files of agentic-era mapping.",
                    body,
                    og_title="Dinis Cruz on Wardley Mapping — 26 items, 2018–2025, then a gap"))
    print(f"gen_dinis: 1 page, {len(items)} items, {len(videos)} recordings embedded")


if __name__ == "__main__":
    main()
