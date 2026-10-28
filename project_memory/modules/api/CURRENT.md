# Falvorn API — CURRENT

> 2026-10-29 (Asia/Seoul) · v0.2 **local release candidate**, not verified production

## Owned files
- `falvorn/api.py`
- `falvorn/sdk.py`
- `falvorn/cli.py`
- `falvorn/mcp_server.py`
- `falvorn/extract.py`
- `falvorn/static/index.html`

## Implemented/source-observed
- REST/OpenAPI; local browser and run endpoints with history/cancel
- HTML extraction and verified localhost sample
- Search adapter requiring SearXNG
- Manual and optional scheduled change monitoring
- Python SDK, CLI, optional MCP and dashboard

## Gaps
- Monitor scheduler off by default; no external alerts
- API contracts not broadly production validated
- No tenants, rate-limit layer or billing

## Next actions
- [ ] Add contract test suite and API versioning
- [ ] Build reliable event/alert service

## Journal
[PROJECT_MEMORY_2026-10-29.md](PROJECT_MEMORY_2026-10-29.md)
