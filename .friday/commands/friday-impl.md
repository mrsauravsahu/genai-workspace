---
description: Implement a change in a GenAI-Workspace repo (nested repos/ or the hub) in an isolated git worktree at <repo-root>/w/<name> (branch == worktree name). Stages changes, never commits.
argument-hint: "[<repo|hub>: <task>]"
---

# /friday-impl

Implement `$ARGUMENTS` per the **friday-impl** skill — in a worktree, **stage, never commit**.

```bash
REPO=~/GenAI-Workspace/repos/<repo>   # or ~/GenAI-Workspace (hub)
NAME=<branch-name>                    # kebab-case, type prefix; == worktree dir
git -C "$REPO" fetch origin
git -C "$REPO" worktree add "w/$NAME" -b "$NAME" origin/main
```

Work in `<repo-root>/w/$NAME`, `git add` the changed files (add `/w` to `.gitignore` if
missing), then stop — no commit/push/merge. Report the branch and worktree path.

Open changes with nvim in a new tmux tab:
`tmux new-window -c "<repo-root>/w/$NAME" -n "$NAME" "zsh -i -c 'nvim .'"`.
