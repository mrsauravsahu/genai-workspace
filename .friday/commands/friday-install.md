---
description: Vendor a third-party skill/command as a git submodule and wire it into .friday/skills or .friday/commands.
argument-hint: [ssh-url to vendor repo]
---

# /friday-install — add a third-party skill or command

Adds a third-party skill/command repo under `.friday/vendor/<repo>` and exposes the
individual skills/commands it provides through `.friday/skills/` and `.friday/commands/`,
so every harness (which already resolves its skills/commands path through a symlink into
`.friday/`, see `.friday/init`) picks it up automatically.

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
