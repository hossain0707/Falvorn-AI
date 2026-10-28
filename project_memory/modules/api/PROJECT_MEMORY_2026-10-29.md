# Falvorn API — PROJECT_MEMORY_2026-10-29

> Asia/Seoul · Entry type: initial source-grounded baseline · Source commit reviewed: `6f17f8fdd1b4e3686b4ff22c56c6718f47f158f5`

## Scope
- `falvorn/api.py`
- `falvorn/sdk.py`
- `falvorn/cli.py`
- `falvorn/mcp_server.py`
- `falvorn/extract.py`
- `falvorn/static/index.html`

## Documented existing functionality (not newly implemented today)
- FastAPI health, fetch, search, agent runs/status/events, browser sessions/actions, and page-change check endpoints.
- HTML-to-Markdown extraction with HTTPX; optional Playwright JS rendering.
- Search adapter requiring configured SearXNG; returns an explicit unconfigured response otherwise.
- Manual page-content hash monitoring with SQLite; Python SDK/CLI and optional MCP stdio adapter; web dashboard.

## Validation
- **Executed this session:** reviewed source files and existing project documentation; **application tests not rerun**.
- **Historical statement:** previous v0.1 prototype reported 9 passing local tests (overall project, not this module specifically).
- **Not verified:** production readiness and live external-site end-to-end results.

## Known limitations / risks
- Manual change-check endpoint is not a scheduler, notification service, or durable task-queue solution.
- Search quality depends on external SearXNG configuration; SDK/REST/MCP contracts have not been independently production certified.
- No multi-tenant isolation, rate-limit infrastructure, billing, or production-facing credential vault.

## Decisions
- Maintain a dedicated module history and refreshed `CURRENT.md`, plus a project-level handover.
- Do not confuse current code with planned roadmap features.
- Keep all remote edits opt-in and secrets out of public docs.

## Next steps
- [ ] Add contract tests and versioned API schemas.
- [ ] Separate monitoring scheduler/notifications from manual hash checks.
- [ ] Introduce persistent execution records and tenant-scoped auth before public SaaS.

## Remote / ChatGPT Sources
- Initial repository memory integration requested by user; no future push, deployment or automatic Sources synchronization authorized.
