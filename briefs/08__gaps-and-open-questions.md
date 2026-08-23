# 08 — Gaps, open questions and honest tensions

---

## 1. Must be written fresh — nothing in the corpus covers these

| # | Page | Why |
|---|---|---|
| **G1** | **The front page** | 300 words that open the argument for a cold reader. The pieces exist — maps-as-claims, the token-spend diagnostic, the rotted link layer — and nobody has assembled them. |
| **G2** | **The PST pattern write-up** | The corpus's most original contribution exists only as `.claude/` configuration plus one February brief. `library/guides/agentic-setup/` has five guides; **none mentions Explorer, Villager or Town Planner.** `02__` is the raw material. |
| **G3** | **`/agents/` and the definitions endpoint** | 33 concepts as machine-readable JSON, plus the coordinate contract, the parse rules and the epistemic guardrail. The commission was explicitly about agents; there is no surface today. |
| **G4** | **A teaching path** | One 846-word primer, then a cliff into advanced application. **Nothing bridges them** — no worked example that builds a map from a blank page. `01__`'s six altitudes are the skeleton. |
| **G5** | **A glossary** | Spelling drift (commoditise/-ize, productise/-ize) and name drift (Explorer/Pioneer, Villager/Settler) run through the whole corpus. |
| **G6** | **`/shipped/`** | Nothing renders, the evolution map is six months stale, maps-as-graphs is unimplemented. Without this page the site over-claims and breaks the convention the siblings are built on. |
| **G7** | **Consistent attribution** | **Only two documents in the entire corpus cite Simon Wardley with a URL.** Most assert doctrine without a source. A public Wardley site cannot do that. Three documents already model the right footer — copy it everywhere. |

---

## 2. Artefacts that were commissioned and never made

Each is a specific, dated promise the corpus records and does not keep. Any of them would make a good launch page.

1. **The three maps commissioned 28 July** — air gap, translation, evidence chain. The reality doc records all three as PROPOSED: *"all three need to be built, rendered, and published"*.
2. **The TLS/SSL skills-landscape map**, commissioned 8 June 2026. Never produced.
3. **A competitive-comparison map** of the kind the Cartographer REFERENCE specifies (*"Issues-FS vs GitHub Issues, vs Jira, vs Linear"*). The only competitive map that exists is Map 8, which is on the do-not-publish list.
4. **An alternative-axis map.** Six alternative axes are proposed — openness, automation, documentation, test coverage, graph connectivity, plus visibility and risk overlays — and **zero maps use one.** Even the axis the 28 July verdict explicitly sanctions (air gap → file → API → event-driven) was never drawn.
5. **A doctrine assessment inside `__Send`.** A standing Cartographer responsibility with a named principle list. Never produced. (The one that exists is pki.sgit.ai's — a different project.)
6. **A gameplay analysis.** Gameplays are named in three places — ILC, ecosystem play, tower-and-moat, Red Queen, sensing engines, open approaches — and applied in one paragraph.
7. **A Claude skill for maps.** Asked for twice. `library/skills/` has no mapping skill.
8. **"A map that shows us badly."** Asked for explicitly as the honesty test of the whole series. **This is the one to draw first.** It would be the most credible page on the site.

---

## 3. Open questions worth publishing unresolved

Following the `pki.sgit.ai` convention of numbering open questions in public.

| # | Question | Where the corpus gets closest |
|---|---|---|
| **Q1** | **If the evolution axis encodes consensus rather than fact, what is a map's epistemic status?** Edgar's critique and the corpus's own *"a map is a claim, not a picture"* are the same worry from opposite directions — and neither says what to do about it. | W23; Edgar 2017 |
| **Q2** | **When is a relabelled axis still a Wardley map?** The 28 July rule — *relabel when the thing genuinely evolves; use a maturity model when it merely improves* — is the sharpest answer anyone has given. Does it hold for the risk and visibility overlays? | W6, W6b, W7 |
| **Q3** | **Can you map a gap after all?** *"you cannot map a gap, because a gap has no evolution"* is stated absolutely. But the air-gap map exists and is called the sharpest single map in the estate. Which is it? | W12 |
| **Q4** | **Is de-commoditisation a gap in doctrine or a misreading of it?** It is presented as the former. The strongest counter-argument — that Wardley's ILC already covers a commodity enabling higher-order custom activity — has not been engaged with. | W8, W9 |
| **Q5** | **What makes an evolution placement defensible?** The doctrine assessment demands every rating name its artefact. **No map in the corpus attaches evidence to a placement.** Should they? | doctrine.json; W23 |
| **Q6** | **Should an agent be allowed to place components at all**, or only to render placements a human has made? `04__` §5 says surface them as contestable claims. That is a policy, not an answer. | — |
| **Q7** | **Does the PST→agent-team mapping actually improve outcomes**, or is it a legible metaphor? There is no measurement. The one operationalised role definition out of 33 is thin evidence either way. | `02__` §5 |
| **Q8** | **Who maintains a living map, now that we know nobody did?** The map died on 26 Feb 2026 against the corpus's own warning. If the discipline failed with a named role and a stated responsibility, what would make it work? | `02__` §5 |

---

## 4. Honest tensions

Things the site should hold rather than resolve.

1. **The site is CC BY inside a CC BY-SA ecosystem.** Manageable, but it constrains real editorial choices — see `07__` §1. Say so on the licence page rather than hoping nobody notices.
2. **The corpus is far ahead of the artefacts.** 33 concepts, 194 files, and eight working PNGs. A map of this mapping practice would put most of it at Genesis, and that is a slightly awkward thing for a mapping site to admit. Admit it anyway.
3. **The most original contribution is the least implemented.** PST-as-agent-teams is genuinely novel and 31 of 33 role definitions never got the memo.
4. **The public record and the private record do not touch.** Seven years of security-era mapping, then silence, then 194 unpublished files of agentic-era mapping. **The bridge is one clause in one co-authored article.** The site is that bridge — which means it is making a claim, not reporting one.
5. **Curating an ecosystem while criticising its indexes.** Pointing out that `awesome-wardley-maps` lists five dead things is fair and useful. It is also the CC0 resource this site benefits from most. Credit it warmly while correcting it.
6. **"Maps are graphs with position" is the best idea here and has no code.** It is the corpus's strongest architectural claim and it is listed PROPOSED. Publishing it as method rather than as software is honest; publishing it without saying so is not.
7. **A doctrine self-assessment is the weakest kind of evidence** — the pki page says so itself. Its answer, naming the artefact behind every rating, is good. It is not the same as an external audit, and the page should keep saying so.

---

## 5. Loose ends worth ten minutes each

- **The Map Camp 2020 recording** for *"Cybersecurity: Why Context is your Crown Jewels"*. Sessions are on the Leading Edge Forum YouTube channel; a 13-video playlist exists at `youtube.com/playlist?list=PLP0vnsXbJsRXpKWEFe956zjGrawwQ0wb3`. **Manual clicking will find it.**
- **The SlideShare deck.** The only artefact of that talk, unread behind a Cloudflare wall. Export from a real browser.
- **`youtube.com/watch?v=l59LK8246-s`** — *"Wardley Maps in Cyber Security - Panel"*. Title and channel confirmed; no session page found; **Dinis's participation unconfirmed.** Resolve or omit.
- **`swardley/WARDLEY-MAP-REPOSITORY`'s licence.** README says CC BY-SA, the GitHub field says GPL-3.0. **Ask.** 147 maps are worth one email.
- **The exact dates** for OSS mini-summit sessions A12, A16–A19, A22, A23. The index pages render a stale schedule table; only month+weekday is established. The year-subdomains may hold the real dates.
- **`nhi.sgit.ai`'s four unrendered permissions maps**, including *"Hope Driven Development"*, recorded by `graphs.sgit.ai` but absent from `nhi.sgit.ai/hope/`. Find them, render them, ship them.

---

This document is released under the Creative Commons Attribution 4.0 International licence (CC BY 4.0).
