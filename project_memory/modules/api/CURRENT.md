# Falvorn API — CURRENT

> Revision: 2026-10-29.1 · Asia/Seoul · Status: **Initial implementation** · Last source baseline: `6f17f8fdd1b4e3686b4ff22c56c6718f47f158f5`

## Owned source
- `falvorn/api.py`
- `falvorn/sdk.py`
- `falvorn/cli.py`
- `falvorn/mcp_server.py`
- `falvorn/extract.py`
- `falvorn/static/index.html`

## Implemented / source-observed
- FastAPI health, fetch, search, agent runs/status/events, browser sessions/actions, and page-change check endpoints.
- HTML-to-Markdown extraction with HTTPX; optional Playwright JS rendering.
- Search adapter requiring configured SearXNG; returns an explicit unconfigured response otherwise.
- Manual page-content hash monitoring with SQLite; Python SDK/CLI and optional MCP stdio adapter; web dashboard.

## Limitations / validation gaps
- Manual change-check endpoint is not a scheduler, notification service, or durable task-queue solution.
- Search quality depends on external SearXNG configuration; SDK/REST/MCP contracts have not been independently production certified.
- No multi-tenant isolation, rate-limit infrastructure, billing, or production-facing credential vault.

## Next actions
- [ ] Add contract tests and versioned API schemas.
- [ ] Separate monitoring scheduler/notifications from manual hash checks.
- [ ] Introduce persistent execution records and tenant-scoped auth before public SaaS.

## Current dated journal
- [PROJECT_MEMORY_2026-10-29.md](PROJECT_MEMORY_2026-10-29.md)

## Maintenance
When this module's code actually changes, prepare a dated entry using [template](../../templates/DAILY_ENTRY.md) and update this file and root [project handover](../../../PROJECT_MEMORY.md). For a no-change day, do nothing. No automatic GitHub writes/deployments.
