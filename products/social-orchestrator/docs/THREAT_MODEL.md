# Security model and production constraints

## Trust boundaries

- **Admin UI and API:** One static administrator API key with constant-time comparison. Not a public multi-user authentication system. Key stays in JS memory only, not browser local storage. Use HTTPS, reverse proxy access controls, and trusted network boundaries; rotate and revoke on compromise.
- **Platform secrets:** Only environment variables; never write OAuth tokens or Meta HMAC secret into SQLite, audit logs or GitHub. Set per-platform least-privilege permissions.
- **External input:** RSS headlines, brand prompts and inbound messages are untrusted. The LLM has no direct publishing tools. All drafted posts and replies are manually reviewed and approved.
- **Webhook:** Signed Meta request body checked with SHA-256 HMAC and deduplicated by platform message ID. Implement provider event-shape regression tests before scaling subscriptions.
- **Media serving:** Files are UUID-named, no arbitrary user-supplied paths. Public endpoint is disabled unless specifically configured. Protect uploaded content and apply copyright and privacy review.
- **Worker:** SQLite `BEGIN IMMEDIATE` transaction prevents duplicate claims in one database. Only one live worker is supported. Uncertain provider result moves to `needs_reconciliation`, not blind retry. On crash during `publishing`, operations remain stuck until human reconciliation.

## Known limitations (must resolve before general production SaaS)

1. No customer identity, roles/permissions, tenant separation, OAuth token refresh or encrypted secrets vault. Never host this single-admin version as shared public SaaS.
2. SQLite is not a distributed job broker; no HA or guaranteed scheduling SLA. Add Postgres/queue, distributed locking, dead-letter and operator recovery.
3. No independent penetration test, vulnerability scanning, abuse throttling, or risk-based content moderation. Add per-route rate limits, CSRF strategy if switching to browser sessions, stricter reverse-proxy security and request-size limits.
4. Third-party API outages, token expiry, permissions and account restrictions need live preflight and integration tests. The client must honor Meta/LinkedIn/YouTube publishing and messaging policies.
5. Human approval is only key holder approval; for regulated enterprise publishing implement immutable audit, staged editorial approval, role segregation, legal review and retention.
6. RSS signals have uncertain reliability and do not imply validated trend popularity or permission to repost source content.
7. The basic MP4 renderer has no audio; creative use rights should be validated before publication. No automatic lip-sync, avatars, stock footage or AI video diffusion is claimed.
8. Do not collect personal data beyond what you are entitled to process. Customer messages are persisted locally until purged manually (no automatic retention/DSAR tooling).

## Release evidence checklist

- [x] Code compilation and offline tests covering auth, state machine, scheduler, signatures, creative poster, local MP4 render, audit.
- [ ] Live sandbox Meta professional publishing and message reply with approved app permissions.
- [ ] Live LinkedIn permissions and text posting test.
- [ ] Live YouTube private video upload and review.
- [ ] Secrets rotation + dedicated vault + token refresh.
- [ ] Non-root Docker hardening, vulnerability audit, dependency pinning, HTTPS reverse proxy and network controls.
- [ ] Multi-tenant isolation and admin access control for SaaS.
- [ ] Load test, worker restart recovery, 99th percentile latency, backup and restore drill.
