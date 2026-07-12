#!/usr/bin/env bash
#
# .friday/bootstrap.sh — wire the canonical .friday/ files into the paths each
# harness reads. Run from the project root:
#
#     ./.friday/bootstrap.sh
#
# Idempotent: re-running fixes drifted links. Existing real (non-symlink) files
# are backed up to <file>.bak instead of being overwritten.

set -euo pipefail

# Resolve project root as the parent of this script's directory.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(dirname "$SCRIPT_DIR")"
cd "$ROOT"

# link <target-under-.friday> <link-path-at-root>
link() {
  local target="$1" link="$2"

  # Already the correct symlink? Nothing to do.
  if [ -L "$link" ] && [ "$(readlink "$link")" = "$target" ]; then
    echo "ok    $link -> $target"
    return
  fi

  # A real file/dir sits here — back it up before replacing.
  if [ -e "$link" ] && [ ! -L "$link" ]; then
    mv "$link" "$link.bak"
    echo "backup $link -> $link.bak"
  fi

  rm -f "$link"
  ln -s "$target" "$link"
  echo "link  $link -> $target"
}

# rules.md is the single source of truth for cross-harness instructions.
link ".friday/rules.md" "CLAUDE.md"      # Claude Code
link ".friday/rules.md" "AGENTS.md"      # OpenCode, Codex CLI
link ".friday/rules.md" ".cursorrules"   # Cursor

# MCP server definitions.
link ".friday/mcp.json" ".mcp.json"      # Claude Code

# Skills: Claude Code reads .claude/skills/<name>/.
mkdir -p .claude
link "../.friday/skills" ".claude/skills"

echo "done. bootstrap complete."
