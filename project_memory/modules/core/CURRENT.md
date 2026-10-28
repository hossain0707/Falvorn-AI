# Falvorn Core — CURRENT

> Revision: 2026-10-29.1 · Asia/Seoul · Status: **Initial implementation** · Last source baseline: `6f17f8fdd1b4e3686b4ff22c56c6718f47f158f5`

## Owned source
- `falvorn/config.py`
- `falvorn/models.py`
- `falvorn/security.py`

## Implemented / source-observed
- Environment-based settings and bounded operational limits.
- Pydantic models for agent, browser, fetch, search, and monitor requests.
- API-key check, URL syntax/domain validation, DNS/IP screening, and guarded unsafe-target handling.
- Private-target access disabled by default, with explicit test-only override controls.

## Limitations / validation gaps
- DNS validation alone is not a complete SSRF barrier; proxy/firewall egress enforcement is required.
- API-key-only deployment is not enterprise identity management.
- No RBAC, organization scoping, secrets vault, metering, signed audit records, or compliance review.

## Next actions
- [ ] Define tenant identity, permission and approval policy contracts.
- [ ] Harden egress validation against DNS rebinding and redirect edge cases.
- [ ] Add threat model, secret-handling design, and security regression tests.

## Current dated journal
- [PROJECT_MEMORY_2026-10-29.md](PROJECT_MEMORY_2026-10-29.md)

## Maintenance
When this module's code actually changes, prepare a dated entry using [template](../../templates/DAILY_ENTRY.md) and update this file and root [project handover](../../../PROJECT_MEMORY.md). For a no-change day, do nothing. No automatic GitHub writes/deployments.
