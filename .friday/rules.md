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
  - Vendor symlinks keep their upstream name (e.g. `.friday/skills/<vendor-skill>`) and are never committed — untracked by design, safe to leave dangling until the submodule is checked out.
  - Locally authored skills/commands must be named `friday-<name>` (e.g. `.friday/commands/friday-<name>.md`, invoked as `/friday-<name>`) so they're tracked.
- Always vendor skill/command submodules with `shallow = true` in `.gitmodules` — we only ever need the current tip of a vendored repo, not its history, so shallow clones keep the working tree light.
- Each vendor submodule stanza declares which paths get symlinked via a repeated `fridaySymlink = <path-in-repo>` key (dots aren't valid in git config key names, so it can't be namespaced as `friday.symlinkPath`). One `fridaySymlink` entry per skill/command to expose, e.g.:
  ```
  [submodule ".friday/vendor/<repo>"]
  	path = .friday/vendor/<repo>
  	url = <ssh-url>
  	shallow = true
  	fridaySymlink = <path-to-skill-or-command-in-repo>
  	fridaySymlink = <path-to-another-skill-or-command-in-repo>
  ```
  Query all declared paths for a submodule with `git config -f .gitmodules --get-all 'submodule.<path>.fridaySymlink'`, then symlink each basename into `.friday/skills/<basename>` (or `.friday/commands/<basename>`) pointing at `../vendor/<repo>/<path>`.

## Git

- Use SSH remotes (`git@github.com:owner/repo.git`) for all clone/remote operations, not HTTPS.

## Repos

- Cloned GitHub projects live under `repos/` (each cloned via SSH), so they can be reused across tasks.
- `repos/` is gitignored — not pushed to GitHub.

## Notes to self

- Keep persistent project preferences and conventions in this `CLAUDE.md` (project folder), not in a separate memory directory.
