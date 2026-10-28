# Falvorn API — PROJECT_MEMORY_2026-10-29

## Initial historical baseline
- GitHub memory initialized at commit `f234cdc9`; original v0.1 module contained relevant implementation, with no new code in the memory-only commit.

## Later local v0.2 candidate
- REST/OpenAPI; local browser and run endpoints with history/cancel
- HTML extraction and verified localhost sample
- Search adapter requiring SearXNG
- Manual and optional scheduled change monitoring
- Python SDK, CLI, optional MCP and dashboard

## Evidence
- Overall local suite: **14 passed**; no isolated claim for this module. API localhost HTML extraction verified. Chromium navigation outside in-memory pages blocked by sandbox policy.

## Limitations
- Monitor scheduler off by default; no external alerts
- API contracts not broadly production validated
- No tenants, rate-limit layer or billing

## Next work
- [ ] Add contract test suite and API versioning
- [ ] Build reliable event/alert service

## Publication policy
- Local candidate not automatically committed/pushed; user approval required for remote write. ChatGPT Sources are not auto-updated.
