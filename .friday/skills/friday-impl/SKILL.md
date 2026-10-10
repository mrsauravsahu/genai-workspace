---
name: friday-impl
description: Implement any change to a GenAI-Workspace repo — a nested repo under GenAI-Workspace/repos, or the GenAI-Workspace hub repo itself — inside an isolated git worktree at that repo's w/ directory, with the branch name identical to the worktree name (e.g. branch feat-ui-login checked out at repos/payobills/w/feat-ui-login; the hub uses GenAI-Workspace/w/<name>). Changes are left staged, never committed: the user commits, raises the PR, merges on the remote, and then asks for a local pull. Use whenever asked to implement, build, add, fix, refactor, or otherwise change code, config, skills, or commands in a GenAI-Workspace repo.
argument-hint: "<repo|hub>: <task>  (e.g. 'payobills: add login button')"
---

# friday-impl — implement in a worktree

The standard way of working in GenAI-Workspace: every change to a repo is made in a dedicated
**git worktree**, never in the main checkout. This holds for nested repos under `repos/` **and**
for the GenAI-Workspace hub repo itself.

**Hand-off rule:** you stage the changes and stop. You do **not** commit, push, merge, or pull.
The user commits, raises the PR, merges on the remote, and only then asks you to pull locally
on the hub.

## The convention (non-negotiable)

Let `<repo-root>` be the git repo being changed:

- Nested repo: `<repo-root> = ~/GenAI-Workspace/repos/<repo>`
- The hub itself: `<repo-root> = ~/GenAI-Workspace`

Then:

- Worktree location: `<repo-root>/w/<name>`
- Branch: `<name>` — **identical** to the worktree directory name.
- `<name>` is kebab-case with a type prefix: `feat-`, `fix-`, `chore-`, `docs-`. No slashes
  (a slash would nest directories and break the 1:1 name match).
- Examples:
  - nested repo: `feat-ui-login` in `payobills` -> worktree `repos/payobills/w/feat-ui-login`
    on branch `feat-ui-login`.
  - the hub: `feat-friday-impl` in GenAI-Workspace -> worktree `GenAI-Workspace/w/feat-friday-impl`
    on branch `feat-friday-impl`.

If a task spans several repos, create a matching worktree in each, same branch name.

## Input

`$ARGUMENTS` is the target repo — a `repos/<repo>` name, or `hub` / `genai-workspace` for the
hub root — plus the task. If the repo or a usable branch name is missing or ambiguous, ask (or
derive a name and state it).

## Steps

1. **Resolve `<repo-root>` + name.**
   - nested: `~/GenAI-Workspace/repos/<repo>`; hub: `~/GenAI-Workspace`.
   - must be a git repo: `git -C "$REPO" rev-parse --show-toplevel`.
   - derive `NAME` (kebab-case, type prefix) from the task, or use the name the user gave.

2. **Sync + pick the base.**
   - `git -C "$REPO" fetch origin`
   - Default base is the repo's default branch, normally `origin/main` (confirm with
     `git -C "$REPO" symbolic-ref --short refs/remotes/origin/HEAD`). Use another base only
     if the task explicitly says so.

3. **Create the worktree** — path and branch name match:
   ```bash
   git -C "$REPO" worktree add "w/$NAME" -b "$NAME" origin/main
   ```
   - If branch `$NAME` already exists (local or remote), reuse it instead of creating:
     `git -C "$REPO" worktree add "w/$NAME" "$NAME"`.
   - Result: `<repo-root>/w/<name>` checked out on branch `<name>`.

4. **Ensure `w/` is ignored.** From the main checkout, check:
   `git -C "$REPO" check-ignore -q w`. If it is **not** ignored, add a `/w` line to
   `.gitignore` **inside the worktree** and stage it with the rest of the change. The main
   checkout showing an untracked `w/` until the branch merges is expected.

5. **Work in the worktree, not the main checkout.** Move the session into
   `<repo-root>/w/$NAME` (opencode: `session_move`; otherwise `cd`). Do all edits, tests,
   and builds there.

6. **Stage — do not commit.** `git add` exactly the files you changed (including any
   `.gitignore` update). Leave them staged. **Never run `git commit`.**

7. **Report.** `<repo-root>`, branch, worktree path, what changed, what is staged vs. still
   unstaged, how you verified, and anything left over.

8. **Stop.** The user commits, pushes, raises the PR, and merges on the remote. Only when
   they explicitly ask you to **pull/sync** do you bring it into the main checkout:
   ```bash
   git -C "$REPO" fetch origin
   git -C "$REPO" merge --ff-only origin/main
   ```
   After that lands, the worktree can be removed:
   `git -C "$REPO" worktree remove "w/$NAME"` and `git -C "$REPO" branch -d "$NAME"`.

## Opening the changes (new tmux tab)

When the user asks to **open the changes** / **open the worktree** (their tmux prefix + `c`,
i.e. `` ` c `` — the `~`/`` ` `` key then `c` — opens a new tab), open the worktree in a new
tmux window running **nvim**, named after the branch:

```bash
tmux new-window -c "<repo-root>/w/<NAME>" -n "<NAME>" "zsh -i -c 'nvim .'"
```

- Only when running inside tmux (check `$TMUX`). If not in tmux, just print the worktree path
  so the user can open it themselves.
- Pass the command explicitly and use an interactive zsh. A bare `new-window` with no command
  came up in `$HOME` (ignoring `-c`); `zsh -i -c 'nvim .'` starts nvim in the worktree.
- Name the window `<NAME>` so it is obvious which worktree/branch it holds.

## Rules

- Branch name == worktree directory name, always: `w/<name>` on branch `<name>`.
- Never edit the main checkout of a repo for feature work — including the hub.
- **Never commit, push, merge, or pull** as part of `friday-impl`. Stage only; the user drives
  git.
- Never run `git add -A` from the main checkout — it would sweep in the untracked `w/`.
- Understand and follow each repo's own rules (`CLAUDE.md` / `AGENTS.md`; e.g. payobills PRs
  target `main` and rebase against `origin/main` before merging).
- Hub caveat: skills and commands are read from the hub's main checkout
  (`~/.friday/skills`, `~/.friday/commands` via the harness symlinks), so a change to them only
  takes effect across the workspace once it has merged on the remote and been pulled locally.
