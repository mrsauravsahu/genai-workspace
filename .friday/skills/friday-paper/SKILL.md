---
name: friday-paper
description: Generate a styled PDF from a markdown file using the local `paper` CLI. Use when the user asks to "run paper on it", "make a PDF", "create a paper/PDF of this doc", or similar for a markdown file (README, ARCHITECTURE, snippets, etc).
---

# paper

`paper` is a local binary (`~/.mrsauravsahu/bin/paper`, already on `PATH`) that
renders a markdown file to a styled PDF via a dockerized pandoc + xelatex
pipeline. It supports Mermaid diagrams (via `mermaid-filter`) and emoji.

## Usage

```bash
paper <file.md> [-o <output.pdf>] [-n] [--continuous] [--breaks=yes|no] [--title=yes|no] [--pages=yes|no] [-v]
```

- Default output: `<file>.pdf` next to the input if `-o` is omitted.
- `-v` prints verbose docker/pandoc output — useful for diagnosing render
  failures (missing glyphs, mermaid syntax errors, etc).
- `-n` skips auto-opening the resulting PDF.
- Requires Docker running locally (the `paper:latest` image does the actual
  pandoc/xelatex/mermaid-filter work).

## When to use

- User asks to "run paper on it", "make it a PDF", "export this as a PDF",
  referring to a markdown file just written or edited (e.g. README.md,
  ARCHITECTURE.md, a snippet in `snippets/`).
- After adding/updating a Mermaid diagram or other content in a markdown file
  that already has a companion `.pdf` checked in alongside it (e.g.
  `README.md` + `README.pdf`) — regenerate the PDF to keep it in sync.

## Example

```bash
paper README.md -o README.pdf -v
```
