# Minimal jailed Claude Code harness: Ubuntu + mise + Claude Code.
# The jail is the bind mount at run time (see run.sh) — only the mounted
# project dir is visible inside the container.
FROM ubuntu:26.04

RUN apt-get update && apt-get install -y --no-install-recommends \
      ca-certificates curl git \
 && rm -rf /var/lib/apt/lists/*

# Run as a non-root user so files created in the mounted repo aren't root-owned.
RUN useradd -ms /bin/bash dev
USER dev
WORKDIR /workspace

# mise via its arch-agnostic installer (works on amd64 and arm64). Present so a
# mounted repo's mise.toml / .tool-versions drives its own runtimes.
RUN curl -fsSL https://mise.run | sh
ENV PATH="/home/dev/.local/bin:/home/dev/.local/share/mise/shims:$PATH"

# Claude Code via the official native installer (no Node required).
RUN curl -fsSL https://claude.ai/install.sh | bash

ENTRYPOINT ["claude"]
