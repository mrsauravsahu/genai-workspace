#!/usr/bin/env bash
# Run Claude Code jailed to the current directory.
#
# The container only ever sees what is bind-mounted below: the current working
# directory. Nothing else on the host (~/.ssh, ~/.aws, other repos) is reachable
# from inside, because it was never mounted.
#
# Usage:
#   sandbox/run.sh                 # interactive claude in $PWD
#   sandbox/run.sh -p "fix tests"  # pass args straight through to claude
set -euo pipefail

IMAGE="${CLAUDE_SANDBOX_IMAGE:-claude-mise:latest}"

# Auth: forward the API key from the host env. Alternatively, mount a config dir
# with:  -v "$HOME/.claude:/home/dev/.claude"  (widens the jail to that file).
exec docker run --rm -it \
  -v "$PWD:/workspace" \
  -w /workspace \
  -e ANTHROPIC_API_KEY \
  "$IMAGE" "$@"
