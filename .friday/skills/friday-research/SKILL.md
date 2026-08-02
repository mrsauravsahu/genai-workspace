---
name: friday-research
description: Research a topic or decision and produce a structured two-page markdown document — current-state findings grouped into decision-relevant categories, compared in tables, closed with a recommendation tailored to the requester's context. Use when asked to "research X", "compare options for X", or "help me understand the landscape for X".
argument-hint: "[research goal/topic, plus any known context or constraints]"
---

# friday-research — structured comparative research

Turn a research goal into a **two-page markdown document**: current-state findings, grouped
into categories relevant to the decision at hand, compared in tables, and closed with a
recommendation tailored to the requester's actual situation — not generic advice that would
apply to anyone.

This skill is domain-agnostic. The topic could be tooling, a technical approach, a market, a
process, a vendor choice — anything where the shape of the answer is "here are the credible
options, grouped and compared, here's what fits you specifically."

## Input

`$ARGUMENTS` is the research goal/topic, ideally with context about what decision it
informs and what the requester already has or is constrained by. If that context is
missing and plausibly changes the recommendation, ask for it before searching — don't
interrogate for context that wouldn't change the output.

## Bar for the document

- Roughly 1000–1400 words: one H1, a handful of H2 sections. If you'd need to scroll more
  than a couple of screens, cut it down.
- At least one comparison table that groups options into categories reflecting the actual
  decision — not an alphabetical or arbitrary list.
- If the topic has a mechanism or concept that's easy to conflate with something else,
  or that the comparison table depends on the reader understanding, include a short
  explainer section before the table — only if it earns its place, not by default.
- A **Recommendation** section that references the requester's stated context/constraints
  by name, ending in a short ordered action plan — not a restatement of the table or an
  "it depends."
- A closing caution/risks paragraph if the domain has real failure modes worth flagging
  (e.g. reliability, provenance, safety, cost traps) — proportionate to the topic, not
  boilerplate.
- A **Sources** section listing every link actually used, as markdown hyperlinks.

## Steps

- **Scope.** Confirm what's being decided and what the requester's current context is
  (what they already use/know/have, what constraints matter). Skip this if it's already
  clear from `$ARGUMENTS`.
- **Budget.** Ask the requester how much subagent and time budget to spend, and size the
  research fan-out in the Search step to their choice:

  | Tier | Research subagents | Time cap |
  | --- | --- | --- |
  | **quick** | up to **2** agents finding details and validating them | ~1 minute |
  | **medium** | up to **4** agents finding details and validating them | ~5 minutes |

  Default to **quick** if they don't care. Each agent takes one angle/category, gathers
  findings, and validates them; keep the whole search phase within the time cap even if
  that means fewer angles.
- **Search.** Use web search/fetch for current state — do not rely on prior knowledge
  alone, the landscape may have moved since training. Fan out into the number of parallel
  research subagents chosen in the Budget step, each taking a distinct angle rather than one
  broad query, so the categories in the next step are populated with real, validated findings.
- **Categorize.** Group findings into categories that map to the decision itself (e.g. by
  risk/maturity, by mechanism, by how well it fits the requester's existing setup) —
  choose groupings that make the table actionable, not just a taxonomy of what exists.
- **Compare.** Build the table(s): option, key trait/mechanism, and a fit/notes column
  written for this requester's context specifically.
- **Sanity-check sources.** Flag anything that looks unreliable — inflated marketing
  claims, unclear maintainer/provenance, near-duplicate forks, thin evidence — rather than
  presenting every source at face value.
- **Recommend.** Write the Recommendation section as a short, ordered plan grounded in
  what the requester already has, explicitly naming the constraints that ruled options in
  or out.
- **Save.** Write to `research/<kebab-case-topic>.md` in the current project (create
  `research/` if it doesn't exist).
- **Report.** State the saved path and a one-line summary of the recommendation.

