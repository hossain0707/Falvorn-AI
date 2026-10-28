# Public TinyFish capability map → Independent WebAgent Studio

**Date:** 28 October 2026. These are public observable features, not a reconstruction of proprietary algorithms. This file tracks engineering targets only and should not be read as a claim of commercial equivalence.

Sources (official):
- https://www.tinyfish.ai/
- https://www.tinyfish.ai/browser
- https://tinyfish.chat/agent
- https://github.com/tinyfish-io/tinyfish-cookbook

| Public product feature | Our implementation | Remaining work |
|---|---|---|
| TinySearch: fresh results / typed JSON | Partial: SearXNG JSON adapter | search engine quality/ranking, freshness validation, rate limits |
| TinyFetch: rendered page → clean data | Partial: HTTP + Playwright HTML extraction | site-specific extraction, structured schemas, batching, caching |
| TinyBrowser: cloud Chromium / CDP | Partial: Playwright-controlled Chromium contexts | remote CDP sessions, isolation fleet, proxy routing, persistence |
| TinyAgent: goal-based website actions | Partial: OpenAI-compatible action loop | multimodal reasoning, robust retries, benchmark-verified success |
| TinyMonitor: change watching | Partial: manual SQLite content hash comparison | scheduler, notifications, alert filters, history and retention |
| TinyVault: secure login credentials | Missing | KMS-backed secrets and dedicated authorization flows |
| Authenticated session persistence | Missing | secure browser state encryption, expiry, per-user scoping |
| SSE streaming | Partial: run event stream | reconnect semantics, heartbeats, persistent event history |
| Batch / parallel agents | Partial: concurrent bounded runs | distributed workers and batch APIs |
| Python SDK | Minimal | typed models, retries, async APIs |
| TypeScript SDK | Missing | generated client |
| CLI | Minimal | packaging, auth, config, rich output |
| MCP | Minimal stdio adapter | hosted OAuth-protected MCP |
| API keys | Minimal | user/organization scoped RBAC / rotation |
| Billing / usage wallet | Missing | metering, pricing, invoices, quota enforcement |
| Agent observability | Partial: volatile run events | screenshots, trace export, auditing, dashboards |
| Anti-bot/proxies | Missing | access compliance and legitimate site integrations |
| Enterprise reliability and SLA | Unverified | independent testing, incident process, controls |

## Ethics and IP

Use only public docs, API contracts that are lawfully accessible, controlled black-box tests with authorized accounts, and permissively licensed independent components. Avoid confidential code, credential extraction, security bypass, and brand impersonation. Our service deliberately uses its own distinct names and endpoints.

## Initial engineering milestone

The source bundle includes a runnable API, dashboard, light Python SDK, CLI, MCP adapter, browser automation loop, extraction, monitoring, and automated tests. It is **not deployed** and **not a commercial product**. Live network automation and any model-dependent task completion must still be tested in the target deployment environment.
