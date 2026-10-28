# Falvorn Core — PROJECT_MEMORY_2026-10-29

> Asia/Seoul · Entry type: initial source-grounded baseline · Source commit reviewed: `6f17f8fdd1b4e3686b4ff22c56c6718f47f158f5`

## Scope
- `falvorn/config.py`
- `falvorn/models.py`
- `falvorn/security.py`

## Documented existing functionality (not newly implemented today)
- Environment-based settings and bounded operational limits.
- Pydantic models for agent, browser, fetch, search, and monitor requests.
- API-key check, URL syntax/domain validation, DNS/IP screening, and guarded unsafe-target handling.
- Private-target access disabled by default, with explicit test-only override controls.

## Validation
- **Executed this session:** reviewed source files and existing project documentation; **application tests not rerun**.
- **Historical statement:** previous v0.1 prototype reported 9 passing local tests (overall project, not this module specifically).
- **Not verified:** production readiness and live external-site end-to-end results.

## Known limitations / risks
- DNS validation alone is not a complete SSRF barrier; proxy/firewall egress enforcement is required.
- API-key-only deployment is not enterprise identity management.
- No RBAC, organization scoping, secrets vault, metering, signed audit records, or compliance review.

## Decisions
- Maintain a dedicated module history and refreshed `CURRENT.md`, plus a project-level handover.
- Do not confuse current code with planned roadmap features.
- Keep all remote edits opt-in and secrets out of public docs.

## Next steps
- [ ] Define tenant identity, permission and approval policy contracts.
- [ ] Harden egress validation against DNS rebinding and redirect edge cases.
- [ ] Add threat model, secret-handling design, and security regression tests.

## Remote / ChatGPT Sources
- Initial repository memory integration requested by user; no future push, deployment or automatic Sources synchronization authorized.
