---
description: Implement a change in a GenAI-Workspace repo (nested repo under repos/, or the hub itself) using an isolated git worktree under that repo's w/ dir (branch name == worktree name). Leaves changes staged — never commits.
argument-hint: "[<repo|hub>: <task>, e.g. 'payobills: add login button']"
---

# /friday-impl — implement in a worktree

Implement `$ARGUMENTS` following the **friday-impl** skill. The non-negotiable convention,
for any GenAI-Workspace repo (nested `repos/<repo>` or the hub root):

- Worktree at `<repo-root>/w/<name>`, on branch `<name>` — **branch name and worktree
  directory name must match** (kebab-case, type prefix: `feat-`/`fix-`/`chore-`/`docs-`).
- Never edit the repo's main checkout for feature work.
- **Stage the changes, do not commit.** The user commits, raises the PR, merges on the
  remote, and then asks for a local pull.

Minimal flow:

```bash
REPO=~/GenAI-Workspace/repos/<repo>   # or ~/GenAI-Workspace for the hub itself
NAME=<branch-name>                    # e.g. feat-ui-login / feat-friday-impl
git -C "$REPO" fetch origin
git -C "$REPO" worktree add "w/$NAME" -b "$NAME" origin/main
```

Then move into `<repo-root>/w/$NAME`, make the change there, `git add` the changed files
(including a `/w` line in `.gitignore` if the repo doesn't already ignore it), and stop —
no `git commit`, no push, no merge. Report the branch and worktree path, then hand off.

When asked to **open the changes**, open the worktree with nvim in a new tmux tab:
`tmux new-window -c "<repo-root>/w/$NAME" -n "$NAME" "zsh -i -c 'nvim .'"` (only inside tmux;
else print the path).

See the `friday-impl` skill for full steps and edge cases (reusing an existing branch,
multiple repos, the hub caveat, and the pull-only-when-asked follow-up).
