---
description: Sync a snippet markdown file to the Notion "snippets" folder and record the page URL in its frontmatter.
argument-hint: [path-to-snippet.md]
---

# /snippet — sync a snippet to Notion

Sync a markdown snippet from `snippets/` to Notion (under the workspace's snippets
folder) and write the resulting Notion page URL back into the file's `Link:`
frontmatter field.

## Target file

Use the file path in `$ARGUMENTS`. If none was given, list the `.md` files under
`snippets/` and ask which one to sync.

## Steps

1. **Resolve the Notion root.** Read `GENAI_WORKSPACE__NOTION_ROOT_PAGE_URL` from the
   environment (`printenv GENAI_WORKSPACE__NOTION_ROOT_PAGE_URL`). If it is empty or
   unset, **stop and ask the user** for the root page URL — do not guess.

2. **Locate the snippets folder.** Using the Notion MCP server, find a child page named
   **"snippets"** directly under the root page. If it does not exist, create it under the
   root page.

3. **Check for an existing page.** Read the target file's frontmatter. If `Link:` is
   already populated, confirm with the user whether to update that existing Notion page
   or create a new one.

4. **Push the content.** Create (or update) a Notion page under the snippets folder using
   the markdown file's H1 as the page title and the body as the page content, via the
   Notion MCP server.

5. **Record the link.** Take the created/updated Notion page URL and write it into the
   file's frontmatter as `Link: <url>` (create the `Link:` key if absent, preserving the
   rest of the frontmatter and body).

6. **Report.** Print the Notion page URL and the file that was updated.

## Notes

- Frontmatter key is `Link:` (per the workspace request). The existing `snippets/`
  convention in CLAUDE.md also documents a `notion:` field — do not remove other keys.
- `snippets/` is gitignored, so these files never get pushed to GitHub; Notion is the
  shared copy.
