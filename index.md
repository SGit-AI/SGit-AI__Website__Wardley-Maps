# Maps are claims, not pictures

*wardley-maps.sgit.ai · site v0.1.2 · CC BY 4.0 · part of the [sgit.ai](https://sgit.ai) network*

A Wardley map asserts where every component sits on the evolution axis. That makes it
**arguable** — and almost nobody publishes theirs anywhere it can be argued with. This site
publishes its maps as source next to the render, its doctrine ratings with the artefact each
one rests on, and its resource list with the date every link was last checked. Everything here
is meant to be disagreed with in a pull request.

- [Start here](start/index.html) — six rungs from "I read the introduction" to "I can argue about a placement"
- [The doctrine assessment](doctrine/index.html) — 40 records, each naming its evidence
- [34 resources, verified](resources/index.html) — not listed

---

## Three things here that are not anywhere else

**[A doctrine assessment that names its evidence](doctrine/index.html).** Forty records across
Wardley's six categories and four phases, every rating carrying the artefact it rests on so a
reader who disagrees has the evidence in front of them. There is currently **no working doctrine
assessment tool anywhere in the ecosystem** — both are dead, and the community index still lists
them.

**[Pioneers–Settlers–Town Planners as three literal agent teams](patterns/pst/index.html).** Not
a metaphor: three directory trees, three session contracts, three evolution-stage mandates. The
agent is told which stage of the evolution axis it is standing on before it does anything. And
31 of the 33 role definitions inside those teams never got the memo, which the page says out
loud.

**[Thirty-four resources with a date on every one](resources/index.html).** MapKeep is dead.
MapScript is dead. Every doctrine assessment tool is dead. The Map Camp Slack invite 404s. All
of them are still listed as live by `awesome-wardley-maps`, by Wikipedia, and in two cases by
Simon Wardley's own resources page.

---

## Four claims about the method

Each one comes out of applying mapping to an agentic software project for six months, and each
names what evidence would change it.

| The claim | Why it matters |
|---|---|
| [De-commoditisation](method/de-commoditisation.html) | A thing can be commoditised at one phase of evolution while still being meaningfully custom-built at the next. The map shows the commodity; it does not show the shield. |
| [The custom-axis verdict](method/custom-axes.html) | *Relabel the axis when the thing genuinely evolves; use a maturity model when the thing merely improves.* |
| [You cannot map a gap](method/broken-middle.html) | A gap has no evolution, so it cannot be positioned. What you get instead is a shape: the ends are solved, the middle is people. |
| [Maps are graphs with position](method/maps-as-graphs.html) | A map is a projection of a graph; map queries are graph queries with positional filters. **And it has no implementation.** |

---

> **Anybody who spends a lot of money on tokens has an engineering problem. They are using
> explorer-type code and solutions in a commodity environment.**

4 June 2026, and unpublished until now. It turns a strategy framework into an operational cost
diagnostic: an invoice becomes evidence of a position on the evolution axis.
[The skill lifecycle it comes from →](patterns/pst/index.html#skills)

---

## What is not here

- **Zero of the thirteen Mermaid map sources in the source repository rendered.** Two mundane
  causes. The eight PNGs from 24 May were the only working visuals in the whole corpus.
- **The living evolution map died on 26 February 2026** — six months stale, against the corpus's
  own warning that *"a map that was accurate three months ago and hasn't been updated is worse
  than no map."*
- **The best idea here has no code.** *Maps are graphs with position* is listed as PROPOSED.
- **The map that shows us badly has not been drawn**, and it was asked for explicitly as the test
  of whether these are analysis or marketing.

[All of it, unsoftened →](shipped/index.html)

---

## If you are an agent

[/llms.txt](llms.txt) and [/llms-full.txt](llms-full.txt) are the whole surface;
[/agents/concepts.json](agents/concepts.json) is the definitions endpoint; and
[/agents/](agents/index.html) carries the two things that are easy to get wrong.

**First:** Mermaid and OnlineWardleyMaps coordinates are `[visibility, evolution]`, not
`[x, y]`. Transposing them renders without an error and asserts something else entirely — proven
there by rendering, not repeated from documentation.

**Second, and it is not a footnote:** the evolution axis plausibly encodes consensus rather than
objective fact, so a model placing components on it is generating consensus-shaped output with
no underlying evidence. **An agent must surface its placements as contestable claims requiring
challenge, never as findings.**

---

*Wardley Mapping is provided courtesy of Simon Wardley, CC BY-SA 4.0. His blog,
blog.gardeviance.org, is CC BY-SA 3.0 — a different licence, quoted under a separate notice.
Nothing here is an adaptation of either. [The licence position in full](about/licensing.html).*

*This page is released under the Creative Commons Attribution 4.0 International licence
(CC BY 4.0).*
