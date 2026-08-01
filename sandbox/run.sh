#!/usr/bin/env bash
# Run Claude Code jailed to the current directory.
#
# The container sees two host paths and nothing else: the current working
# directory (mounted at /workspace) and the host's ~/.claude config, so your
# existing Claude subscription / login carries over. No other host paths
# (~/.ssh, ~/.aws, other repos) are reachable from inside.
#
# Usage:
#   sandbox/run.sh                 # interactive claude in $PWD
#   sandbox/run.sh -p "fix tests"  # pass args straight through to claude
set -euo pipefail

IMAGE="${CLAUDE_SANDBOX_IMAGE:-claude-mise:latest}"

exec docker run --rm -it \
  -v "$PWD:/workspace" \
  -v "$HOME/.claude:/home/dev/.claude" \
  -w /workspace \
  -e ANTHROPIC_API_KEY \
  "$IMAGE" "$@"
