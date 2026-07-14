# Rules

Source of truth for cross-harness instructions. Symlinked as `CLAUDE.md` and `AGENTS.md` so every harness reads the same file.

## Conventions

- (add coding style, architecture, and workflow rules here)

## Snippets

- `snippets/` is gitignored — not pushed to GitHub.
- Once a snippet `.md` file has been synced to Notion, add frontmatter to it recording the Notion page URL, e.g.:

```markdown
---
notion: https://app.notion.com/p/<page-id>
---
```

## Skills

- Any directory inside `genai-workspace` that installs a third-party skill must vendor it under `.friday/vendor/<repo>` (git submodule) and symlink the individual skill dir(s) into `.friday/skills/<name>`, not install directly into `.claude/skills/`, `.opencode/skills/`, or similar tool-specific paths.
- This keeps a single source of truth: every harness already resolves its skills path through a symlink into `.friday/skills` (see `.friday/init`), so vendoring once propagates to all configured tooling automatically.
- Example: `git submodule add <ssh-url> .friday/vendor/<repo>` then `ln -s ../vendor/<repo>/skills/<name> .friday/skills/<name>`.
- `.friday/skills/*` and `.friday/commands/*` mix two kinds of entries: vendor symlinks (generated, not source) and locally authored skills/commands (source, tracked). `.gitignore` ignores everything in both dirs except entries prefixed `friday-`, so:
  - Vendor symlinks keep their upstream name (e.g. `.friday/skills/ponytail`) and are never committed — untracked by design, safe to leave dangling until the submodule is checked out.
  - Locally authored skills/commands must be named `friday-<name>` (e.g. `.friday/commands/friday-snippet.md`, invoked as `/friday-snippet`) so they're tracked.

## Git

- Use SSH remotes (`git@github.com:owner/repo.git`) for all clone/remote operations, not HTTPS.

## Repos

- Cloned GitHub projects live under `repos/` (each cloned via SSH), so they can be reused across tasks.
- `repos/` is gitignored — not pushed to GitHub.

## Notes to self

- Keep persistent project preferences and conventions in this `CLAUDE.md` (project folder), not in a separate memory directory.
