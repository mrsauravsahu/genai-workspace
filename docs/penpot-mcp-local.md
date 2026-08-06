# Penpot MCP + self-hosted Penpot (local, in Docker)

Runbook for driving Penpot from an AI client on this machine. Captures the
working setup and the one still-pending piece.

Last verified: 2026-08-02.

## TL;DR status

- Penpot MCP server: RUNNING in Docker, Claude Code connected. Works.
- Self-hosted Penpot app (localhost:9001): NOT up yet - image pull was
  interrupted by a transient Docker Hub TLS timeout on `sj26/mailcatcher`.
  Retry command below. Until it is up, point the plugin at cloud Penpot
  (https://design.penpot.app).

## Why Docker (not npx)

`npx @penpot/mcp@latest` bootstraps the monorepo via the host's pnpm, which
hard-fails here with `ERR_PNPM_IGNORED_BUILDS` (pnpm 11 blocks esbuild/sharp
build scripts as a supply-chain guard). Building in a clean `node:22` container
sidesteps the host pnpm/npmrc entirely; the vendored source's
`pnpm-workspace.yaml` already declares `allowBuilds`, so the container install
is clean.

## The MCP container (working)

Built from the vendored source at `mcps/penpot/mcp`.

Ports (container binds 0.0.0.0, published to host):

| Port | Purpose | Who connects |
|------|---------|--------------|
| 4401 | MCP HTTP endpoint (`/mcp`, `/sse`) | the AI client (Claude Code) |
| 4400 | plugin server (`/manifest.json`)   | your browser (loads the plugin) |
| 4402 | WebSocket                          | the in-browser plugin -> server |
| 4403 | REPL (not published)               | - |

Key env overrides baked into the image (defaults bind `localhost`, which does
not work through published ports):

- `PENPOT_MCP_SERVER_HOST=0.0.0.0`
- `PENPOT_MCP_PLUGIN_SERVER_HOST=0.0.0.0`
- `WS_URI=http://localhost:4402`  (browser reaches WS via the published host port)

Registered MCP tools: `execute_code`, `high_level_overview`, `penpot_api_info`,
`export_shape`, `import_image`.

### Rebuild + run

Dockerfile (kept in the job tmp dir during setup; reproduced here):

```dockerfile
FROM node:22-bookworm-slim
ENV PENPOT_MCP_SERVER_HOST=0.0.0.0 \
    PENPOT_MCP_PLUGIN_SERVER_HOST=0.0.0.0 \
    WS_URI=http://localhost:4402 \
    CI=1
WORKDIR /app
RUN corepack enable && corepack prepare pnpm@11.10.0 --activate
COPY . /app
RUN pnpm -r install && pnpm run build
EXPOSE 4400 4401 4402 4403
CMD ["pnpm", "run", "start"]
```

```bash
# build (context = the vendored MCP source)
docker build -f <path>/penpot-mcp.Dockerfile -t penpot-mcp:local \
  /Users/Saurav_Sahu/GenAI-Workspace/mcps/penpot/mcp

# run
docker run -d --name penpot-mcp --restart unless-stopped \
  -p 4400:4400 -p 4401:4401 -p 4402:4402 penpot-mcp:local

# logs / lifecycle
docker logs -f penpot-mcp
docker stop penpot-mcp ; docker start penpot-mcp
```

### Register with Claude Code (user scope)

```bash
claude mcp add -s user -t http penpot http://localhost:4401/mcp
claude mcp get penpot          # expect: Status ✔ Connected
claude mcp remove penpot -s user   # to undo
```

NOTE: MCP tools attach at session start. A Claude Code session started BEFORE
registration will not show `mcp__penpot__*` tools - start a fresh session.

## Self-hosted Penpot app (pending)

Official compose (prebuilt images) is vendored at
`mcps/penpot/docker/images/docker-compose.yaml`. Frontend serves at
http://localhost:9001. Version pinned to 2.17 to match the MCP build.

The full `up` failed on a transient TLS timeout pulling `sj26/mailcatcher`
(a dev SMTP catcher, non-essential), which interrupted the other pulls.

Services: penpot-frontend, penpot-backend, penpot-exporter, penpot-postgres,
penpot-valkey, penpot-mcp (bundled, internal-only - no host ports, so it does
NOT conflict with our :4401 container), penpot-mailcatch.

Retry WITHOUT the flaky mailcatcher service:

```bash
cd /Users/Saurav_Sahu/GenAI-Workspace/mcps/penpot/docker/images
PENPOT_VERSION=2.17 docker compose up -d \
  penpot-postgres penpot-valkey penpot-backend penpot-exporter penpot-frontend
# then open http://localhost:9001 and register a local account
```

(The bundled `penpot-mcp` service ships with the compose but is unpublished;
we use our own port-exposed `penpot-mcp:local` container instead.)

## Human steps to actually use it (cannot be automated)

1. Open Penpot in a browser:
   - local: http://localhost:9001 (once the app stack is up), or
   - cloud: https://design.penpot.app
   Open a design file.
2. Plugins menu -> load plugin via URL: http://localhost:4400/manifest.json
3. In the plugin UI, click "Connect to MCP server" (status -> Connected).
   Keep the plugin panel open and the tab active while working.
   If Chromium blocks localhost (private network access), approve the popup.
4. Use a fresh Claude Code session so the `penpot` MCP tools are loaded.

## Prereqs / environment

- Colima (Docker runtime) must be running: alias `colima_start` in ~/.zshrc.
- Docker Compose v2 (`docker compose`), node 22, `claude` CLI - all present.
