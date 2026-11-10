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

## GitHub Stars

- `context/github-stars.csv` is a snapshot of the user's GitHub starred repos (repo, url, description, language, topics, stars, pushed_at, archived, lists, starred_at), grouped by the user's current GitHub star-list categories (AI & GenAI, Web/UI & Design, Backend & Languages, Cloud/DevOps & Homelab, CLI/Shell & Editor, Platforms & Desktop Apps, Dev Tools & Build/Test, Reference & Awesome Lists, plus a few personal lists).
- `context/` is gitignored — not pushed to GitHub, same as `snippets/`, `research/`, `repos/`. Not every checkout of this repo will have `context/github-stars.csv` present, so check for its existence before relying on it.
- When coding and a task calls for a library, CLI tool, or service (e.g. "need a Kubernetes dashboard", "need a Go CLI framework"), and the file exists, grep it before reaching for an unfamiliar dependency — the user has often already starred a relevant option. Surface the match and let the user decide whether to use it.
- `/friday-install` also consults this file (if present) before searching the open skills ecosystem — see that command for details.
- Stale over time (stars/pushed dates drift); regenerate via the GitHub GraphQL API (`gh api graphql`) rather than trusting old rows for recency-sensitive checks (e.g. "is this still maintained").

## Skills

- Any directory inside `genai-workspace` that installs a third-party skill must vendor it under `.friday/vendor/<repo>` (git submodule) and symlink the individual skill dir(s) into `.friday/skills/<name>`, not install directly into `.claude/skills/`, `.opencode/skills/`, or similar tool-specific paths.
- This keeps a single source of truth: every harness already resolves its skills path through a symlink into `.friday/skills` (see `.friday/init`), so vendoring once propagates to all configured tooling automatically.
- Run `/friday-install` for the full step-by-step (submodule add, `shallow = true`, `fridaySymlink` declarations, symlink creation).
- `.friday/skills/*` and `.friday/commands/*` mix two kinds of entries: vendor symlinks (generated, not source) and locally authored skills/commands (source, tracked). `.gitignore` ignores everything in both dirs except entries prefixed `friday-`, so:
  - Vendor symlinks keep their upstream name and are never committed — untracked by design, safe to leave dangling until the submodule is checked out.
  - Locally authored skills/commands must be named `friday-<name>` so they're tracked.

## Settings

- `.friday/settings.json` is the canonical settings file, written in Claude Code's schema. Edit it there — never edit a tool-specific settings path directly.
- `.friday/init` symlinks it to `.claude/settings.json` (same schema, no translation needed). `/.claude/settings.json` is gitignored as generated.
- Every other tool gets it *translated*, not symlinked: after `.friday/init`, ask the agent to translate `.friday/settings.json` into each selected tool's own config format and path. Options with no equivalent are dropped, not invented — the agent should say which it dropped.
- `.claude/settings.local.json` stays local and untracked; it's per-machine, not part of the canonical set.

## Editor

- The harness and the user's editor work together over MCP. `.friday/mcp.json` registers the connected editor's MCP server under the fixed name `editor`, so every harness reaches it the same way whatever the editor (nvim, VS Code, Cursor, …). `editor` in `.friday/config.json` says which editor it is; `gw` starts it alongside the harness.
- Use the `editor` server to work in the user's editor: open/show files, read open buffers and selections, diagnostics, LSP. Never spawn a new editor instance, tmux window, or pane to show a file.
- Layout: the harness always runs on the **right** of the screen (with `settings.openHarnessInEditor` it's a terminal split inside nvim). Whenever a file is opened — because the user asked or because the harness wants to show one — open it in the **middle** editor window, the main code window between any file tree/sidebar on the left and the harness on the right. Never open a file in, replace, close, resize, or move focus into the harness window. In nvim, that means picking a normal (non-`terminal`, non-sidebar) window and running `:edit` there, e.g. `nvim_win_call(win, function() vim.cmd.edit(path) end)`, rather than `:edit` in the current window, which may be the harness. If no such window exists, make one with `:leftabove vsplit` from the harness window, so the harness stays on the right.
- If there is no `editor` server, or it can't connect to the running editor: don't guess — ask the user which editor they use and which MCP server connects to it, then record it as `editor` in `.friday/mcp.json` (and `editor` in `.friday/config.json`).
- mrsauravsahu currently uses nvim with Claude Code. Its `editor` server is [`nvim-mcp`](https://github.com/linw1995/nvim-mcp) (`--connect auto` attaches to the nvim whose git root matches the harness's); the nvim side is the `linw1995/nvim-mcp` plugin in nvim-config, and the binary comes from `cargo install nvim-mcp`.

## Git

- Use SSH remotes (`git@github.com:owner/repo.git`) for all clone/remote operations, not HTTPS.
- Before opening a PR, check that `gh` is installed. If it is not, do **not** reach for
  another route (API tokens, credential helpers, installing `gh`) — ask the user to confirm
  pushing the branch, push it, and give them the `pull/new/<branch>` link so they open the
  PR themselves.

## Repos

- Cloned GitHub projects live under `repos/` (each cloned via SSH), so they can be reused across tasks.
- `repos/` is gitignored — not pushed to GitHub.

## Notes to self

- Keep persistent project preferences and conventions in this `CLAUDE.md` (project folder), not in a separate memory directory.
