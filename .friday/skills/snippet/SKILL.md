---
name: snippet
description: Create a one-pager markdown snippet, then optionally publish it to the Notion "snippets" folder.
argument-hint: [topic or path-to-snippet.md]
---

# snippet — create a one-pager (then optionally publish to Notion)

Primary job: turn a topic (or existing draft) into a clean, self-contained **one-pager**
under `snippets/`. Publishing to Notion is an opt-in step offered only after the file is
written.

**One-pager bar:** ≤400 words / ≤60 lines, one H1, ~3–6 tight sections. If you'd scroll
more than once to read it, cut it down.

## Input

`$ARGUMENTS` is a topic to draft, a `snippets/*.md` path to refine, or empty (then ask
what the snippet is about).

## Part 1 — Create (do first)

1. Draft/refine from the topic; ask the user for facts you don't know rather than inventing.
2. Shape to the one-pager bar: H1 title, one-line intro, tight sections with bullets and
   fenced code where useful. Preserve any existing frontmatter (`notion:` / `Link:`).
3. Write to `snippets/<kebab-case-title>.md` (or overwrite the given path). `snippets/` is
   gitignored — never lands on GitHub.
4. Report the path and a one-line summary.

## Part 2 — Publish to Notion (ask first)

After saving, **ask whether to publish.** If no, stop. If yes:

1. `printenv GENAI_WORKSPACE__NOTION_ROOT_PAGE_URL`. If empty/unset, ask the user — don't guess.
2. Via Notion MCP, find the child page **"snippets"** under the root; create it if missing.
3. If frontmatter `Link:`/`notion:` is set, confirm update-vs-create.
4. Create/update the page: H1 → page title, body → content.
5. Write the page URL back as `Link: <url>`, preserving other keys.
6. Report the URL and file.
