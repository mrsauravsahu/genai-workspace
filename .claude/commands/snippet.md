---
description: Create a one-pager markdown snippet, then optionally publish it to the Notion "snippets" folder.
argument-hint: [topic or path-to-snippet.md]
---

# /snippet — create a one-pager snippet (and optionally publish to Notion)

Primary job: turn a topic (or existing draft) into a clean, self-contained
**one-pager markdown** file under `snippets/`. Publishing to Notion is a secondary,
opt-in step you offer only after the markdown is written.

## Input

`$ARGUMENTS` may be:

- **A topic / description** — draft a new one-pager about it.
- **A path to a `.md` file** under `snippets/` — treat it as an existing draft to
  refine into one-pager shape.
- **Empty** — ask the user what the snippet should be about (or which existing
  `snippets/*.md` draft to work from).

## Part 1 — Create the one-pager (do this first)

1. **Gather the content.** Draft (or refine) the snippet from the topic/draft. If key
   facts are unknown, ask the user rather than inventing them.

2. **Shape it as a one-pager.** Keep it to roughly a single page:
   - An H1 title (used later as the Notion page title).
   - A short intro/summary line.
   - Tight sections with headings, bullets, and fenced code blocks where useful.
   - Preserve any existing frontmatter keys (e.g. `notion:` / `Link:`); do not remove
     them.

3. **Write the file** to `snippets/<kebab-case-title>.md` (or overwrite the given path).
   Remember `snippets/` is gitignored, so it never lands on GitHub.

4. **Report** the file path and a one-line summary of what was created.

## Part 2 — Offer to publish to Notion (ask first)

After the markdown is saved, **ask the user whether they want to publish it to Notion.**
If they decline, stop here — the one-pager is the deliverable. If they accept, run the
sync below.

### Publish steps

1. **Resolve the Notion root.** Read `GENAI_WORKSPACE__NOTION_ROOT_PAGE_URL` from the
   environment (`printenv GENAI_WORKSPACE__NOTION_ROOT_PAGE_URL`). If it is empty or
   unset, **stop and ask the user** for the root page URL — do not guess.

2. **Locate the snippets folder.** Using the Notion MCP server, find a child page named
   **"snippets"** directly under the root page. If it does not exist, create it under the
   root page.

3. **Check for an existing page.** Read the file's frontmatter. If `Link:` (or `notion:`)
   is already populated, confirm with the user whether to update that existing Notion page
   or create a new one.

4. **Push the content.** Create (or update) a Notion page under the snippets folder using
   the markdown file's H1 as the page title and the body as the page content, via the
   Notion MCP server.

5. **Record the link.** Write the created/updated Notion page URL into the file's
   frontmatter as `Link: <url>` (create the `Link:` key if absent, preserving the rest of
   the frontmatter and body).

6. **Report.** Print the Notion page URL and the file that was updated.

## Notes

- The one-pager markdown is the primary output; Notion publishing is always opt-in.
- Frontmatter key for the Notion URL is `Link:`. The existing `snippets/` convention in
  CLAUDE.md also documents a `notion:` field — do not remove other keys.
- `snippets/` is gitignored, so these files never get pushed to GitHub; Notion is the
  shared copy.
