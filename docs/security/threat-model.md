# Falvorn AI v0.2 — Threat model and deployment gates

**Deployment classification: experimental self-hosted single-node. Not an audited public SaaS.**

## Assets and trust boundaries
- API secrets, LLM provider credentials, browser session state and websites accessed by user tasks.
- Untrusted webpages can attempt prompt injection and malicious links.
- Browser workers may request internal network endpoints, cloud metadata or downloadable files.
- Screenshots and extracted content may contain personal/customer data.

## Existing mitigations
- URL syntax, private-address and DNS address checks before navigation and on intercepted browser routes.
- Domain restrictions per request; browser creates independent contexts and blocks downloads/service workers.
- Configurable API key, with public bind refused when absent; local-only default.
- Default deny for typing and non-link clicks; sensitive fields and consequential actions blocked by heuristics.
- Bounded content, step and browser counts; cancellation and persisted event history.

## Unresolved security risks
- **DNS rebinding/TOCTOU, SSRF and browser escape:** code checks alone are insufficient. Put browsers in hardened containers with no host networking and explicit egress policy; block cloud metadata and internal subnets at firewall/proxy level.
- **Prompt injection:** hostile website text can steer LLM outputs. Enforce policy at action execution and require human confirmations for privileged external effects.
- **Credential vault:** not implemented. Do not submit real login credentials or recovery codes.
- **Tenancy:** a single API key cannot separate users or organizations. Do not expose publicly as a multi-tenant service.
- **Retention/privacy:** events currently include task goals, URLs and snippets. Run only on permitted content and set an appropriate data policy/retention before production use.
- **Availability:** SQLite and in-process asyncio are single-node only; rate limiting, quotas and audit integrity need production hardening.

## Release gates (must pass before calling production-ready)
1. External security review: SSRF, prompt injection, isolation, auth, audit/data retention.
2. Dedicated egress-isolated workers and per-tenant identity/authorization.
3. Persistent distributed job queue, cancellation, replay safeguards, retries, alerting and backups.
4. Browser evaluation: multi-site tasks with honest success, latency and cost statistics.
5. License and dependency review, supply-chain scanning and incident response plan.

Never add CAPTCHA bypass, stealth credential harvesting, or bypass of access controls as a feature.
