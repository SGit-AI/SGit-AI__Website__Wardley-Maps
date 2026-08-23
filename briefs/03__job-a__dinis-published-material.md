# 03 — Job A: everything Dinis Cruz has published on Wardley Maps

> *"do a research on other materials (videos, infographics, docs) that I have published around wardley maps"*

**26 items, 2018–2025.** Full structured data in `sources__dinis-wardley-published.json` — id, date, date-precision, type, URL, role, collaborators, video URL, verification flag, and a note per item. **22 of 26 verified by fetching; 4 could not be fetched** (SlideShare and LinkedIn block automated retrieval, and I did not route around them).

This should become `/dinis/` on the new site: a chronology, the videos embedded, and — the part that matters — the fragile items archived before they disappear.

---

## 1. The shape of it

| Period | Output | Character |
|---|---|---|
| **2018** | 6 items | Founding. Two blog posts, three OSS sessions, the Medium seed piece. **The only year he organised a mapping track himself.** |
| **2019** | 3 items | Institutional. The Wardley track runs without him organising it; mapping appears in an OWASP talk and a job ad. |
| **2020** | 7 items | **The peak.** Five OSS sessions with Simon Wardley in the room, plus the Map Camp talk and its deck. |
| **2021** | **0** | Silence. |
| **2022** | 3 items | The reflective phase — including the only solo, fully-authored piece. |
| **2023** | **0** | Silence. |
| **2024** | 4 items | Two panels, two LinkedIn **shares of other people's work**. |
| **2025** | 1 item | One clause in one co-authored article. |
| **2026** | **0 published** | ~194 files of unpublished Wardley thinking in `__Send`. |

**The headline for the site is that last row.** The public record stops in 2022 and the private record starts in 2026. There is no public bridge between them.

---

## 2. The through-line — four claims, held for seven years

**(a) 2018: diagrams must become maps.** The Medium post of 7 Oct 2018 is the intellectual seed and the clearest statement of the whole position:

> *"in most development teams, we are still at the 'Why do we need up-to-date diagrams?' phase. Where the question that we should be looking at is 'How can we make our diagrams every better and more valuable?' And the answer is Maps, which are diagrams with the following properties - are visual - have context (i.e. specific to purpose / perspective) - are mode of components - have at least one anchor - have a position (relative to anchor) - have a consistency of movement"*

with the complaint that ordinary architecture diagrams *"miss the key mapping properties of: anchor, position (relative to anchor) and consistency of movement."*

**(b) 2018: maps should be generated, not drawn.** *Creating Wardley Maps using Lambda Functions* opens on the frustration of not being able to *"programatically create the maps (ideally via [a] DSL or something like DOT language)"* and ends with a map generated inside a Lambda from programmatic values. **This is the same instinct that, in May 2026, becomes Mermaid `wardley-beta` in git** — eight years apart, one idea. That is the site's best narrative spine, and the fact that the 2018 code is now a 404 while the 2026 version renders is the story's ending.

**(c) 2018–2020: context is the security asset.** The 2018 session deliberately mapped a cup of tea *and* an AWS attack in the same hour, and the outcomes page records the argument over *"whether the tea picker was visible"* as the teaching moment — position is contested, and that's the point. It becomes a title in Oct 2020: **"Why context is your crown jewels."** In security, "crown jewels" means data assets; he inverts it — the contextual understanding of your value chain is the jewel.

**(d) 2020–2022: mapping is the missing half of threat modelling.** Stated flatly in the Mar 2022 session abstract: *"Wardley Maps could be the missing piece of the puzzle when doing Threat Models."*

**And the hinge into AI (2025):**

> *"MCP represents the **commoditization of LLM-to-tool interfaces**, which in turn enables higher-level constructs and rapid innovation (a concept noted in Wardley Maps' **Innovate-Leverage-Commoditize** cycle). We are currently in the **'Genesis and Custom Build' phase** of agents using MCP…"*

One clause, co-authored, five years after the last substantive output. **Do not write the site as though a public position on agentic mapping already exists.** It doesn't. Creating it is the commission.

---

## 3. The direct ancestor worth building a page on

**16 June 2020 — "Team Topologies & PST & Squads & Tribes"**, with Simon Wardley, Tony Richards and Luke Robbertse. Video: `youtube.com/watch?v=YKHPUZJMkUs`. Materials included a PDF, *Cell Structure for Organisations v2.5*.

Six years later, `__Send` runs three agent teams named Explorer, Villager and Town Planner. **The 2026 pattern in `02__` has a documented 2020 origin, with Wardley himself in the conversation.** Put the two side by side on one page. That is the single most satisfying connection in the whole research, and nobody has ever drawn it.

Supporting evidence from the same period: the Dec 2019 hiring post requires candidates to build and present a Wardley Map — *"about an industry, about you or even about a cup of coffee… we also want to see the candidate's experience of creating that map, the thought process and the learning experience"* — and lists Wardley alongside Spotify Squads, Team Topologies and Cynefin. The cup-of-coffee motif carries straight from the 2018 cup of tea.

---

## 4. Claims that exist in exactly one place

Flag these on the page. Each is load-bearing and single-sourced:

| Claim | Only source | Risk |
|---|---|---|
| The "crown jewels" thesis itself | SlideShare deck 238855895 | **The deck's contents are unread.** The title and a third-party agenda listing are all that survives. This is the biggest hole in the record. |
| *"one of the most innovative and powerful frameworks that has emerged in the last decade"* | OSS session page, Jul 2022 | Site could go offline |
| *"Wardley Maps could be the missing piece of the puzzle when doing Threat Models"* | OSS session page, Mar 2022 | Same |
| The Lambda map generator | Dec 2018 blog post | **The repo is already 404.** Only the prose description survives. |

---

## 5. Archive before you publish — priority order

The site should not link to fragile things without mirroring them. In order:

1. **The SlideShare deck.** The only artefact of the Map Camp talk. Export to PDF from a real browser and mirror it. Do the same for the OSS 2018 outcomes deck and Steve Purkis's *"What do Wardley Maps mean to me"* from the same Map Camp.
2. **The year-subdomains** — `2018.`, `2019.`, `2020.open-security-summit.org`. These are separate deployments holding participant lists, outcomes and session notes the current site lacks, and the canonical index openly says *"this list of events and sessions is not complete, we are still in the process of importing."* **The 2018 Maps and Graphs track — the only one Dinis organised — has no presence on the current site at all.**
3. **The two LinkedIn posts.** Unfetchable, unarchivable, deletable, and the only evidence of 2024 activity. Capture by hand. And label them accurately: **both are shares of other people's work, not original writing.**
4. **The 13 YouTube recordings.** All resolved live, all embeddable, all on one third-party channel. Ten are Dinis sessions (ids in the JSON); three more are the wider track — *Wardley Maps First Aid* (Petra Vukmirovic, `dQdQS4TaQ7U`), *Wardley Maps and services model at Glasswall* (Steve Purkis, `GS8Vndr-B4A`), *Maturity Mapping* (Chris McDermott, `ytYT8nhC5RQ`). Note several OSS pages embed `youtube-nocookie.com`.
5. **The two blog posts.** The Blogger feed API confirms the `Wardley_Maps` label holds **exactly two entries** — that label *is* the complete list of his Wardley blogging. Mirror both in full.
6. **Dying links inside the OSS pages themselves** — heysummit registration (now "This event is not live yet"), Zoom links with passwords in the URL, a `join.slack.com` invite, and **Google Slides `/e/2PACX-…/embed` published-deck links** that break the instant the owner unpublishes. Export those decks to PDF.

---

## 6. Three things not to get wrong

1. **The two LinkedIn items are shares.** Presenting them as authored posts would be a straightforward misattribution.
2. **Mini-summit dates are month-precision only.** OSS session pages carry a weekday but no date, and every mini-summit index page renders a **stale schedule table** — Mar 2022, Jul 2022 and Sep 2024 all return the identical "Monday 9th – Friday 13th" columns, which actually match Dec 2024. Items A12, A16–A19, A22, A23 are month+year+weekday only. **Do not synthesise exact dates.** The JSON carries a `date_precision` field for exactly this.
3. **A26 is unconfirmed.** The video *"Wardley Maps in Cyber Security - Panel"* (`l59LK8246-s`) surfaces on searches for his name, but no session page was found and his participation is not established. Leave it out or mark it clearly.

Two smaller traps: **"Wardley Maps First Aid" is dated 5 June 2020** by its YouTube title despite living under a `/may/` URL path — the 2020 summit slipped from May to June and the URLs never moved. And the `community.wardleymaps.com` crosspost of the Gen-Z templates post renders as **27/02/2024**, which is a Discourse migration artefact, not a republication.

---

This document is released under the Creative Commons Attribution 4.0 International licence (CC BY 4.0).
