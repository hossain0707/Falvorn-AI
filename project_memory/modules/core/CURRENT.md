# Falvorn Core — CURRENT

> 2026-10-29 (Asia/Seoul) · v0.2 **local release candidate**, not verified production

## Owned files
- `falvorn/config.py`
- `falvorn/models.py`
- `falvorn/security.py`
- `falvorn/store.py`

## Implemented/source-observed
- Runtime configuration and bounded settings
- Pydantic request models with scheduler subscription validation
- API key and private-IP/domain URL checks
- SQLite WAL event and monitor-subscription store

## Gaps
- DNS checks are not a firewall or SSRF prevention guarantee
- SQLite and API key single-node/single-user only
- No encrypted credential vault, immutable audit or RBAC

## Next actions
- [ ] Create threat-model-informed egress controls
- [ ] Design tenant/auth/secrets architecture

## Journal
[PROJECT_MEMORY_2026-10-29.md](PROJECT_MEMORY_2026-10-29.md)
