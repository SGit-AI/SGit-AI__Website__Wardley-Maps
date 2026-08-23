# 02 — Explorer / Villager / Town Planner: PST as three literal agent teams

**This is the page only this site can write.** Simon Wardley's Pioneers–Settlers–Town Planners model is well known as an *organisational* pattern for human teams. What exists in `__Send` is different: PST used as the **architecture of an AI agent system** — three separate directory trees, three session contracts, three evolution-stage mandates, and a documented handover between them.

It has never been written up. Not on any site, not in `library/guides/`, not anywhere. It exists as `.claude/` configuration plus one February brief. Writing it up is the highest-value original page available.

---

## 1. What actually exists on disk

```
.claude/CLAUDE.md              .claude/explorer/CLAUDE.md      (816 words)
                               .claude/villager/CLAUDE.md      (1,836 words)
                               .claude/town-planner/CLAUDE.md  (942 words)

team/roles/              <-- THE EXPLORER TEAM  (note: no "explorer/" prefix)
team/villager/roles/
team/town-planner/roles/
```

**There is no `team/explorer/` directory.** The Explorer team is the *unprefixed default* — `team/roles/` — confirmed by `.claude/CLAUDE.md`, which annotates `roles/` as `# Explorer team role-based review documents`.

That asymmetry is not an accident worth apologising for; it is a design statement worth surfacing. **The Explorer is the origin state.** Villager and Town Planner are named departures from it. Everything starts unprefixed and at Genesis, and acquiring a prefix is what evolution looks like in a filesystem.

---

## 2. The operative table

From `.claude/CLAUDE.md`, verbatim — the most authoritative statement of the mapping:

| Team | Focus | Wardley Stage | Output |
|---|---|---|---|
| **Explorer** | Discover, experiment, build first versions | Genesis → Custom-Built | Minor versions (IFD) |
| **Villager** | Stabilise, harden, deploy to production | Custom-Built → Product | Major versions (IFD releases) |
| **Town Planner** | Transmute technical output into investment and business value | Product → Commodity | Investor materials, business strategy |

Preceded by: *"As of v0.5.8, the project operates with **three teams** based on Wardley Maps methodology"*.

Each team's own `CLAUDE.md` restates its stage in the second person — *"You operate at the **Genesis → Custom-Built** stages of the Wardley evolution axis"* — which is the mechanism that makes this more than a diagram. **The agent is told which stage it is standing on before it does anything.**

Note the Town Planner's twist: its `CLAUDE.md` says *"**Product → Commodity** stages… but with a twist"*. The twist is that its output is not more commoditised *code* — it is investor materials. The Town Planner commoditises **the story**, not the software. That is a genuine deviation from Wardley's model and the page should say so.

---

## 3. Which roles sit in which population

From the founding brief (14 Feb 2026), verbatim headings and rationales:

- **Primarily Explorer** — Architect (*"Designing new components, experimenting with approaches"*), Designer, Dev, Journalist, Ambassador, Advocate, Sherpa
- **Primarily Villager** — DevOps (*"Deployment, infrastructure, performance, monitoring"*), QA, GRC, DPO
- **Across Both** — Conductor (*"Orchestrates both teams, manages the handover"*), CISO, AppSec, Librarian, Historian, Cartographer (*"Maps the system at both stages"*)

**On-disk populations today:**

| Team | Directory | Count | Roles |
|---|---|---:|---|
| Explorer | `team/roles/` | **17** | advocate, alchemist, ambassador, appsec, architect, cartographer, conductor, designer, dev, devops, dpo, grc, historian, journalist, librarian, qa, sherpa |
| Villager | `team/villager/roles/` | **17** | as above, minus alchemist, **plus `translator`** |
| Town Planner | `team/town-planner/roles/` | **4** | accountant, alchemist, designer, librarian |

Two things here are worth a paragraph each on the page.

**The Villager-exclusive `translator`.** `.claude/villager/CLAUDE.md` describes it as *"**Villager-exclusive**… the first role that exists **only** in the Villager team"*. This is Wardley-consistent and rather elegant: translation is a productisation activity. Nothing at Genesis needs translating, because nothing at Genesis has a second audience yet.

**The Town Planner team was created a week after being deferred.** The founding brief is explicit: *"❌ **Town Planners Team** — not yet… Attempting to create the Town Planners team now would be premature. We don't have anything at commodity stage yet."* It was created on 20–21 Feb 2026, with the Alchemist as its founding role — **earlier than the brief's own stated criterion, and for a business rather than a technical reason.** Publish that. A documented deviation from your own plan, with the date and the reason, is exactly the kind of evidence the doctrine assessment style demands.

> **Do not use the investor one-pager's counts** (Explorer 15 / Villager 16 / Town Planner 3). They disagree with the filesystem, and that file is on the do-not-publish list anyway.

---

## 4. The finding that makes this page honest

**Of 33 `ROLE.md` files in the repo, exactly two mention Wardley.**

- `team/villager/roles/cartographer/ROLE.md` (682 words, 6 mentions) — genuinely operationalised. Core mission: *"Map the production topology, deployment architecture, and evolution progress — track components as they move from custom-built to product stage on the Wardley evolution axis."* It carries a quality gate reading *"Every component has a Wardley evolution stage label"* and a workflow step *"Flag components approaching commodity stage (candidate for future Town Planners team)"*.
- `team/town-planner/roles/accountant/ROLE.md` (385 words, 1 passing mention).

**`team/roles/cartographer/ROLE.md` — the Explorer Cartographer, 2,057 words, the longest cartographer document in the repo — mentions Wardley zero times.** Its five core principles are about ASCII art, layering and dependency graphs. Its effectiveness table counts unmapped components and undiagrammed data flows. No evolution axis, no doctrine, no gameplay.

The founding brief called the Cartographer *"central to this entire structure"*. Its role definition is a document in which the structure does not appear. Every other Explorer `ROLE.md` — architect (1,974 w), conductor (1,803 w), librarian (1,961 w) — is likewise silent.

**So: the teams know their stage; the roles inside them do not.** The mandate lives in the session contract and never reaches the role definition. That is a real, specific, fixable defect, and naming it is what separates a pattern write-up from a brochure.

---

## 5. Asserted vs implemented

| Claim | Status |
|---|---|
| Three teams exist as directories | **Implemented** |
| Three distinct session contracts | **Implemented** — 816 / 1,836 / 942 words |
| Each team bound to a Wardley stage | **Asserted** consistently in four places |
| The seven separation rules (*"Villagers do NOT add features"*, *"Explorers do NOT deploy to production"*, distinct environments) | **Asserted** in `.claude/CLAUDE.md`; environment separation was still open decision AD-1 as of 14 Feb 2026 |
| Individual roles know their population | **Not implemented** — 31 of 33 silent |
| The Cartographer maintains a living evolution map | **Partially, then abandoned.** Three real maps, all 26 Feb 2026. The `reviews/` tree ends 11 Mar 2026. |
| Handover briefs at `team/roles/explorer/handovers/` | **Not implemented** — the path named in `.claude/explorer/CLAUDE.md` does not exist |
| Doctrine assessments, gameplay analyses | **Not implemented** |
| Written up as a reusable pattern | **No.** `library/guides/agentic-setup/` has five guides; none mentions Explorer, Villager or Town Planner. |

The Cartographer's own REFERENCE supplies the verdict on row 6: *"a map that was accurate three months ago and hasn't been updated is worse than no map."* It is now six months.

---

## 6. The two ideas that make the pattern more than a rename

**The theft.** *"The key dynamic is what Wardley calls the **'theft'** — the villagers take (pinch) what the explorers have built and turn it into a product."* [S] — but the agentic version is new: in a human org the theft is a political event needing management. Between agent teams it is a **file move plus a version bump**, and it can be logged. That is a genuine advantage of doing PST with agents, and the page should claim it.

**PST applied to artefacts, not people.** This is the strongest extension in the corpus (W14, 4 Jun 2026):

> *"the lifecycle of a skill is to start as massive LLM, held together with string and gum, very expensive, lots of tokens, all the way to a product, all the way to code, and it almost becomes a commodity, eventually disappearing, because maybe it is absorbed by something else."*

with the mechanism — *"the natural progression of a skill is to start in English and end up in code. As you refine the skill, you reduce the scope, you reduce the variability"* — and the consequence, which is the corpus's best line:

> *"**Anybody who spends a lot of money on tokens has an engineering problem. They are using explorer-type code and solutions in a commodity environment.**"*

That last sentence turns a strategy framework into an **operational cost diagnostic**. It is the single most useful thing this site can hand a working engineer, and it is currently unpublished.

Related, and worth its own section: **the same skill differs by character** — *"a skill, the same skill for a town planner, is very different for an explorer, for a villager"* — and **the seniority inversion** in the vibe-coding article, which assigns Villager work to *"junior and mid-level engineers"* and Town Planner work to *"the most experienced engineers on the team"*, inverting the usual assumption that the exciting new thing goes to the seniors.

---

## 7. How to write the page

1. **Lead with the filesystem**, not the theory. Three directory trees is a more arresting opening than a restatement of PST, and it is the part that is new.
2. **Cite Wardley properly and early** — `blog.gardeviance.org/2015/03/on-pioneers-settlers-town-planners-and.html`, **CC BY-SA 3.0, not 4.0** (see `07__`). The corpus carries this citation in exactly one file; the site must carry it everywhere.
3. **State the rename in one sentence** and never drift again: Explorer = Pioneer, Villager = Settler, Town Planner = Town Planner.
4. **Publish §4 and §5 unsoftened.** A pattern write-up that admits 31 of 33 roles never got the memo is credible. One that doesn't, isn't.
5. **Draw the map of the pattern itself.** Where do the three teams sit on an evolution axis? Where does `translator` sit? It does not exist yet and it is an obvious, cheap, original artefact.

---

This document is released under the Creative Commons Attribution 4.0 International licence (CC BY 4.0).
