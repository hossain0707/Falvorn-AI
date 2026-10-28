# Falvorn Core — PROJECT_MEMORY_2026-10-29

## Initial historical baseline
- GitHub memory initialized at commit `f234cdc9`; original v0.1 module contained relevant implementation, with no new code in the memory-only commit.

## Later local v0.2 candidate
- Runtime configuration and bounded settings
- Pydantic request models with scheduler subscription validation
- API key and private-IP/domain URL checks
- SQLite WAL event and monitor-subscription store

## Evidence
- Overall local suite: **14 passed**; no isolated claim for this module. API localhost HTML extraction verified. Chromium navigation outside in-memory pages blocked by sandbox policy.

## Limitations
- DNS checks are not a firewall or SSRF prevention guarantee
- SQLite and API key single-node/single-user only
- No encrypted credential vault, immutable audit or RBAC

## Next work
- [ ] Create threat-model-informed egress controls
- [ ] Design tenant/auth/secrets architecture

## Publication policy
- Local candidate not automatically committed/pushed; user approval required for remote write. ChatGPT Sources are not auto-updated.
