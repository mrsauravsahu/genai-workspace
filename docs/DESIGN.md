# GenAI Workspace — Design Language

The workspace is a terminal. Everything we design should look like it belongs inside one, or like it was printed by one.

Source material: the `gw` tmux/Neovim screenshot (Tokyo Night), the terminal-first repos (`dotfiles`, `cli-config`, `nvim-config`, `wezterm-config`, `paper`), and the quieter, content-first voice of [mrsauravsahu.in](https://mrsauravsahu.in).

---

## Principles

**1. The terminal is the design system.**
Monospace, fixed grid, ANSI colors, block cursors. We don't dress the terminal up as a web app; we let the web page behave like a terminal.

**2. One source of truth, visibly.**
`.friday/` exists so config isn't duplicated. Design follows: one token file, one type scale, one accent. If something appears twice with two values, it's a bug.

**3. Show the real thing.**
Real commands, real output, real file trees. No invented UI, no fake dashboards, no stock illustration. If a screenshot can say it, don't write a paragraph.

**4. Motion is state, not decoration.**
Things animate because something happened — a command ran, a session moved from *Working* to *Completed*, a pane came into view. Nothing loops forever for atmosphere.

**5. Quiet by default, loud once.**
The page is dim. Exactly one element per screen is bright: usually the command you're meant to copy.

**6. Copyable beats clickable.**
The primary call to action is text you can select. Every command block is copy-first; buttons are secondary.

**7. Dark is the default, not the theme.**
There is no light mode to maintain. The workspace runs dark; the site does too, and says so rather than apologizing for it.

**8. Respect the reader's machine.**
No external fonts, no CDN, no tracking, no layout shift. Honor `prefers-reduced-motion`. The page should load fine over tethering on a train.

---

## Tokens

### Color — Tokyo Night

Taken directly from the terminal so the site and the screenshots never disagree.

| Token | Value | Use |
|---|---|---|
| `--bg` | `#1a1b26` | Page background |
| `--bg-raised` | `#1f2335` | Panels, cards |
| `--bg-inset` | `#16161e` | Terminal windows, code blocks |
| `--border` | `#2a2e42` | Hairlines, pane splits |
| `--fg` | `#c0caf5` | Body text |
| `--fg-dim` | `#8b93b8` | Secondary text |
| `--fg-muted` | `#565f89` | Comments, captions, prompts |
| `--blue` | `#7aa2f7` | Primary accent, links, directories |
| `--cyan` | `#7dcfff` | Symlinks, paths, inline code |
| `--green` | `#9ece6a` | Success, active session, the `gw` command |
| `--yellow` | `#e0af68` | Branch names, warnings, "needs input" |
| `--red` | `#f7768e` | Errors, destructive, `~/` root marker |
| `--purple` | `#bb9af7` | Keywords, rare emphasis |

#### Brand marks — the one exception

Harness chips carry their own product color, since recognising them at a glance beats palette purity:

| Chip | Value |
|---|---|
| Claude Code | `#d97757` |
| OpenCode | `#f2f2f2` |
| Codex CLI | `#10a37f` |
| Cursor | `#a5b4fc` |
| Gemini CLI | `#4796e3` |

These are the only off-palette colors on the page. They apply to text and border on `.chip` and nowhere else — never as a fill, a heading, a link, or a section accent.

Rules:
- One accent per section. Mixing blue and green in the same block reads as syntax highlighting, not hierarchy.
- Status colors are reserved: green = done, yellow = waiting on you, red = failed. Never use them decoratively.
- Text on `--bg` must be `--fg`, `--fg-dim`, or a named accent. Nothing else.

### Typography

Monospace only. No display face, no body sans.

```
--font: ui-monospace, "SF Mono", "JetBrains Mono", Menlo, Consolas, monospace;
```

System stack, so it renders as the reader's own terminal font where possible. No webfont download.

| Step | Size | Line height | Use |
|---|---|---|---|
| `--t-hero` | `clamp(2rem, 6vw, 3.5rem)` | 1.1 | Page title |
| `--t-h2` | `1.5rem` | 1.3 | Section headings |
| `--t-h3` | `1.125rem` | 1.4 | Sub-headings |
| `--t-body` | `1rem` | 1.7 | Prose |
| `--t-small` | `0.875rem` | 1.6 | Captions, terminal chrome |
| `--t-micro` | `0.75rem` | 1.5 | Labels, tab bars |

Weights: 400 and 700 only. Letter-spacing: `0.02em` on uppercase micro-labels, `0` everywhere else. Prose measure caps at `68ch`.

### Space

4px base, powers used sparingly.

```
--s-1: 4px    --s-2: 8px    --s-3: 12px   --s-4: 16px
--s-5: 24px   --s-6: 32px   --s-7: 48px   --s-8: 72px   --s-9: 112px
```

Section rhythm: `--s-9` between major sections, `--s-6` inside them. Content column `max-width: 960px`, gutter `--s-5`.

### Border & radius

- Hairlines are `1px solid var(--border)` — panes butt against each other like tmux splits.
- `--radius: 6px` for terminal windows and cards. `0` for inline chips and tab bars.
- Elevation is color, not shadow. One allowed shadow: `0 20px 60px rgba(0,0,0,.4)` on the hero terminal window only.

### Motion

```
--ease: cubic-bezier(.2, .8, .2, 1);
--dur-fast: 120ms   --dur: 240ms   --dur-slow: 480ms
```

- Hover/focus: `--dur-fast`.
- Reveal on scroll: `--dur-slow`, 12px rise + fade, once, never re-triggered.
- Typing effects: 40–60ms per character, one per page, only on a real command.
- Cursor blink: 1s step-end, allowed on prompts.
- All of the above collapse to instant under `prefers-reduced-motion: reduce`.

---

## Components

### Terminal window

The workhorse. A `--bg-inset` panel with a `--radius` corner, a chrome bar (three dots or a tmux-style tab strip in `--t-micro`), and monospace content. Prompt glyph is `❯` in `--green`. Output uses `--fg-dim`. Never scrolls horizontally — wrap or truncate.

### Command block

Single line, `--bg-inset`, left-aligned, `❯` prompt, copy affordance on the right that becomes visible on hover/focus and always visible on touch. Copy state: label swaps to `copied` in `--green` for 1.2s. This is the primary CTA pattern.

### Tab strip

Borrowed from tmux status: `1:gw` `2:zsh` in `--t-micro`, active tab filled `--green` with `--bg` text, inactive `--fg-muted`. Used for switching between code/config examples.

### Status list

Three-state list mirroring the session view: `needs input` (`--yellow`), `working` (`--green`, with a single pulsing dot), `completed` (`--fg-muted`). Same words, same colors as the CLI — the site is documentation of a real UI.

### File tree

Directories `--blue`, symlinks `--cyan` with a `→` and target, plain files `--fg-dim`, tracked-and-important files `--yellow`. Two-space indent, `1.6` line height. Used to explain `.friday/` — the tree *is* the explanation.

### Callout

Left rule 2px in an accent, `--bg-raised` fill, no icon. One per section maximum.

### Link

`--blue`, underline offset `3px`, `text-decoration-color` at 40% opacity rising to 100% on hover in `--dur-fast`. No color change on hover.

---

## Voice

- Lowercase in UI chrome (`copied`, `needs input`, `? for shortcuts`). Sentence case in prose. Never title case.
- Second person, present tense: "one command drops you into a workspace", not "users are dropped".
- Lead with what it does, then why. Cut the adjective if the sentence survives without it.
- Name real files and real commands inline — `gw`, `.friday/init`, `bash .friday/init repos/<name>` — instead of describing them abstractly.
- No exclamation marks, no "simply", no "just", no "powerful", no em-dash-heavy hedging.

## Accessibility

- Body text on `--bg` clears 7:1; `--fg-muted` is for non-essential text only and never below `--t-small`.
- Focus is a 2px `--blue` outline at `2px` offset, never removed.
- Copy buttons carry `aria-live` for the copied state.
- Motion is additive: the page is complete and readable with animation disabled and with JS off.

## Don't

- Don't introduce a light theme, a gradient, a glassmorphic blur, or a rounded-pill button.
- Don't animate anything on a loop for mood.
- Don't use an icon where a glyph the terminal already has (`❯ → ✓ ·`) will do.
- Don't add a font, an analytics script, or a framework to `docs/`. It stays one file.
- Don't invent screenshots. If the feature isn't built, don't picture it.
