# Social Orchestrator — CURRENT (2026-11-02 Asia/Seoul)

**Scope:** `products/social-orchestrator/` independent FastAPI/social media operations product. Owner: Md Najmul Hossain. Licensed under parent proprietary LICENSE.

## Implemented and verified locally

- Brand profiles, source-linked RSS signals, optional OpenAI-compatible copy/reply generation + labeled deterministic fallback.
- PNG artwork generator and original silent 6-second vertical MP4 via FFmpeg. Local MP4 output and header inspected.
- Draft→approval→schedule/publish state machine with atomic SQLite WAL claims, single separate worker, audit log, dry-run default.
- LinkedIn text post, Instagram image/reels and YouTube private-video upload adapters; signed Meta messaging webhook, deduplicated inbox and manually approved replies.
- Responsive static dashboard with a non-persisted API-key field, Docker Compose loopback, CI workflow and API/security/integration guides.
- **Evidence:** 12 local automated tests passed; Python compile and JS syntax passed. No authenticated live platform API test or hosted public deployment verified.

## Safety / limitations

- Default `SOCIAL_DRY_RUN=true`. No accounts or API tokens in source. No multi-tenant roles, OAuth refresh vault, HA queue, external security assessment or platform API validation.
- YouTube uploads are **private**; Instagram requires professional account, valid app permissions and HTTPS media; LinkedIn requires approved posting scopes.
- Do not run multiple workers. Unknown provider responses need manual reconciliation, not blind retries. Avoid public exposure of shared-key admin API.

## Next work

1. Connect controlled sandbox/test accounts through official OAuth apps; verify tokens/scopes, webhook payload variants, and real provider publishing/DM flows.
2. Implement secret vault and refresh, per-tenant roles, private reverse proxy, worker crash recovery and per-platform rate limiting.
3. Run browser smoke tests, threat-model review, backup/restore and full external API integration test suite.
