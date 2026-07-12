# CLAUDE.md

## Snippets

- `snippets/` is gitignored — not pushed to GitHub.
- Once a snippet `.md` file has been synced to Notion, add frontmatter to it recording the Notion page URL, e.g.:

```markdown
---
notion: https://app.notion.com/p/<page-id>
---
```

## Git

- Use SSH remotes (`git@github.com:owner/repo.git`) for all clone/remote operations, not HTTPS.

## Repos

- Cloned GitHub projects live under `repos/` (each cloned via SSH), so they can be reused across tasks.

## Notes to self

- Keep persistent project preferences and conventions in this `CLAUDE.md` (project folder), not in a separate memory directory.
