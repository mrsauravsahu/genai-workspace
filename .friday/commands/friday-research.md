---
description: Research a topic into a structured markdown doc under research/, then optionally publish it to the Notion "research" folder.
argument-hint: [research goal/topic, plus any known context or constraints]
---

# /friday-research — research a topic (then optionally publish to Notion)

Primary job: turn a research goal into a structured comparative markdown document under
`research/`. Publishing to Notion is an opt-in step offered only after the file is written.

## Input

`$ARGUMENTS` is the research goal/topic, ideally with the context it informs (what the
requester already uses/knows/has, what constraints matter). If that context is missing and
plausibly changes the recommendation, ask before searching.

## Part 1 — Research (do first)

Follow the **friday-research** skill to produce the document: scope, run several
independently-angled web searches (don't rely on prior knowledge — the landscape moves),
categorize findings to fit the decision, compare in a table, sanity-check sources, and
close with a recommendation tailored to the requester's actual context plus a Sources
section.

Save to `research/<kebab-case-topic>.md` in the current project (`research/` is gitignored —
never lands on GitHub). Preserve any existing frontmatter (`notion:` / `Link:`). Report the
path and a one-line summary of the recommendation.

## Part 2 — Publish to Notion (ask first)

After saving, **ask whether to publish.** If no, stop. If yes:

1. `printenv GENAI_WORKSPACE__NOTION_ROOT_PAGE_URL`. If empty/unset, ask the user — don't guess.
2. Via Notion MCP, find the child page **"research"** under the root; create it if missing.
3. If frontmatter `Link:`/`notion:` is set, confirm update-vs-create.
4. Create/update the page: H1 → page title, body → content.
5. Write the page URL back as `Link: <url>`, preserving other keys.
6. Report the URL and file.
