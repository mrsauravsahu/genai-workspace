---
name: friday-impl
description: Implement any change to a GenAI-Workspace repo — a nested repo under GenAI-Workspace/repos or the GenAI-Workspace hub itself — in an isolated git worktree at <repo-root>/w/<name>, with the branch name identical to the worktree name (e.g. feat-ui-login at repos/payobills/w/feat-ui-login; the hub uses GenAI-Workspace/w/<name>). Stage changes, never commit; the user commits, opens the PR, and merges on the remote. Use when asked to implement, add, fix, refactor, or change code/config/skills in a GenAI-Workspace repo.
argument-hint: "<repo|hub>: <task>"
---

# friday-impl — implement in a worktree

Every change to a GenAI-Workspace repo happens in a **git worktree**, never the main checkout.

**Hand-off:** stage the changes and stop — do **not** commit, push, merge, or pull. The user
commits, opens the PR, merges on the remote, then asks you to pull.

## Convention

`<repo-root>` = `~/GenAI-Workspace/repos/<repo>` (nested) or `~/GenAI-Workspace` (the hub).

- Worktree: `<repo-root>/w/<name>`; branch `<name>` — identical, always.
- `<name>`: kebab-case with a type prefix (`feat-`/`fix-`/`chore-`/`docs-`); no slashes.
- e.g. `feat-ui-login` -> `repos/payobills/w/feat-ui-login`; `feat-friday-impl` ->
  `GenAI-Workspace/w/feat-friday-impl`.
- Multiple repos -> a worktree in each, same branch name.

## Steps

```bash
REPO=~/GenAI-Workspace/repos/<repo>   # or ~/GenAI-Workspace
NAME=feat-thing                       # type prefix; == worktree dir
git -C "$REPO" fetch origin
git -C "$REPO" worktree add "w/$NAME" -b "$NAME" origin/main   # drop -b if branch exists
```

1. Base on `origin/main` unless the task says otherwise.
2. If `w/` isn't ignored (`git -C "$REPO" check-ignore -q w`), add `/w` to `.gitignore`
   inside the worktree.
3. Work only in `<repo-root>/w/$NAME` (opencode: `session_move`).
4. **Stage, don't commit:** `git add` the files you changed; never `git commit`.
5. Report repo-root, branch, worktree path, staged files, verification. Stop.

## Open the changes

When asked, open the worktree in a new tmux tab running nvim (inside tmux only; else print
the path):
```bash
tmux new-window -c "<repo-root>/w/$NAME" -n "$NAME" "zsh -i -c 'nvim .'"
```

## Pull (only when asked)

After the PR merges:
`git -C "$REPO" fetch origin && git -C "$REPO" merge --ff-only origin/main`, then
`git -C "$REPO" worktree remove "w/$NAME"`.

## Rules

- Branch name == worktree dir name, always.
- Never edit a main checkout; never commit, push, merge, or pull on your own.
- Never `git add -A` from a main checkout.
- Follow the repo's own rules (`CLAUDE.md`/`AGENTS.md`).
- Hub skills/commands go live only after the change merges and is pulled.
