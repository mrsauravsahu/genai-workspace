---
description: Vendor a third-party skill/command as a git submodule and wire it into .friday/skills or .friday/commands.
argument-hint: [ssh-url to vendor repo, or a description of the skill to find]
---

# /friday-install — add a third-party skill or command

Adds a third-party skill/command repo under `.friday/vendor/<repo>` and exposes the
individual skills/commands it provides through `.friday/skills/` and `.friday/commands/`,
so every harness (which already resolves its skills/commands path through a symlink into
`.friday/`, see `.friday/init`) picks it up automatically.

## Finding the skill

If the argument is already an SSH URL (or a GitHub `blob` link to a specific `SKILL.md`),
skip this section and go straight to **Steps** — you know the repo and path to vendor.

Otherwise the user is describing a capability, not pointing at a repo ("install a skill for
X", "is there a skill that does X"). Discover it first with the vendored `find-skills`
skill (`.friday/skills/find-skills`):

- Invoke `find-skills` to search the open skills ecosystem (`npx skills find …`, the
  skills.sh leaderboard) and identify the best-matching skill and its GitHub repo.
- Follow that skill's quality checks (install count, source reputation, stars) and confirm
  the chosen skill with the user before vendoring.
- Take only the resolved **GitHub repo** and the **path to the skill/command** within it,
  then continue with **Steps** below.
- Do **not** run `npx skills add` to install — that drops the skill into a tool-specific
  path and breaks our single-source-of-truth rule. `find-skills` is for *discovery* only;
  vendoring is always done via the submodule steps below.

## Steps

1. **Vendor the repo as a shallow submodule:**
   ```
   git submodule add <ssh-url> .friday/vendor/<repo>
   ```
   Then add `shallow = true` to its stanza in `.gitmodules` — vendor repos only need
   current tip, not history.

2. **Declare which paths to expose** with a repeated `fridaySymlink` key in the same
   stanza, one entry per skill/command (paths relative to the vendor repo root):
   ```
   [submodule ".friday/vendor/<repo>"]
   	path = .friday/vendor/<repo>
   	url = <ssh-url>
   	shallow = true
   	fridaySymlink = <path-to-skill-or-command-in-repo>
   	fridaySymlink = <path-to-another-skill-or-command-in-repo>
   ```
   (Dots aren't valid in git config key names, so this can't be namespaced as
   `friday.symlinkPath` — `fridaySymlink` is the flat key.)

3. **Create the symlinks** — for each declared path, symlink its basename into
   `.friday/skills/<basename>` (or `.friday/commands/<basename>` if it's a command)
   pointing at `../vendor/<repo>/<path>`:
   ```
   ln -s ../vendor/<repo>/<path> .friday/skills/<basename>
   ```
   Verify with `git config -f .gitmodules --get-all 'submodule.<path>.fridaySymlink'`.

4. **Do not commit these symlinks.** `.gitignore` already ignores everything under
   `.friday/skills/*` and `.friday/commands/*` except entries prefixed `friday-` — vendor
   symlinks keep their upstream name and stay untracked/regenerable by design.

## Local (non-vendor) skills/commands

If you're authoring a skill or command yourself rather than vendoring one, name the file
`friday-<name>` (e.g. `.friday/commands/friday-<name>.md`, invoked as `/friday-<name>`) so
it's tracked instead of ignored.
