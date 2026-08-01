# Jailed Claude Code sandbox

A minimal Docker image that runs **Claude Code** confined to a single project
directory, with **mise** available for per-project runtimes. Replaces the
heavier OpenSandbox approach — the jail is just a Docker bind mount.

## How the jail works

The container only sees what `run.sh` bind-mounts: the current working
directory (`-v "$PWD:/workspace"`) and the host's `~/.claude` config
(`-v "$HOME/.claude:/home/dev/.claude"`, so your existing Claude subscription /
login carries over). Everything else on the host (`~/.ssh`, `~/.aws`, other
repos) is invisible inside the container because it was never mounted. On macOS,
Docker runs in a Linux VM that never had your `~` anyway, so those two bind
mounts are the only exposed paths.

## Build

```bash
docker build -t claude-mise:latest sandbox/
```

## Run

```bash
export ANTHROPIC_API_KEY=sk-ant-...    # or mount ~/.claude, see run.sh
cd /path/to/the/repo/you/want/to/jail
/path/to/GenAI-Workspace/sandbox/run.sh
```

Args pass straight through to `claude`, e.g. `sandbox/run.sh -p "run the tests"`.

## Contents

- **Ubuntu 26.04 LTS** base
- **mise** (arch-agnostic installer) — so a mounted repo's `mise.toml` /
  `.tool-versions` provisions its own Node/Python/Go/etc.
- **Claude Code** via the official native installer (`claude.ai/install.sh`, no
  Node runtime required)
- runs as non-root user `dev` so files written into the mount aren't root-owned

## Caveats

- **Network is still open.** A filesystem jail doesn't stop network egress. If
  your threat model needs it, add `--network none` (breaks Claude's API calls)
  or a proxy allowlist.
- **Auth.** `run.sh` mounts `~/.claude` so your host subscription/login works
  inside the container; this shares that config dir with the container. Remove
  the mount and forward `ANTHROPIC_API_KEY` instead if you'd rather not.
- The mount is read-write — Claude can modify the jailed repo. Use a branch or
  git worktree if you want a throwaway copy.
