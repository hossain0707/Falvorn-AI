# Falvorn AI v0.2 — Independent capability comparison

This document describes **implementation status**, not TinyFish compatibility or validated parity. TinyFish is a proprietary third-party product; Falvorn AI is independently written and not affiliated with TinyFish. Public feature naming is used solely as a high-level comparison.

| Public category | Falvorn v0.2 implementation | Validation state | Missing for commercial parity |
| --- | --- | --- | --- |
| Web page fetch | HTTPX fetch + optional JS rendering | Synthetic local fetch verified; external sites pending | Scale, retry, advanced rendering cases |
| Web search | SearXNG adapter | Requires configured server | Hosted search infra, quality benchmarking |
| Browser session control | Local Playwright contexts | In-memory DOM/action tests | Remote fleet, persistent auth sessions, isolation |
| Goal-based web agent | Model-compatible planner, bounded steps | Parser/API tests; live-site agent runs not verified | Planning quality and independent task benchmarks |
| Run tracking | SQLite persistence, event history, cancellation | Local persistence tests | Distributed queues, tracing and replay safety |
| Screenshot | Authorized session PNG | In-memory Chromium screenshot test | Redaction/privacy policies, secure video streaming |
| Monitoring | Manual hash check; optional interval subscription | Storage tests; external notifications absent | Delivery/retries, alerts, robust content diff |
| API and SDK | REST, Python, CLI, optional MCP | Local unit tests | Stable contracts, multi-language SDK validation |
| Credential vault | None | Not implemented | Key management, user consent, encryption |
| SaaS organizations | None | Not implemented | Tenant RBAC, billing, usage metering, audit |
| Commercial reliability | Not claimed | Not validated | Production SLAs, security reviews, load tests |

Do not equate an implemented adapter to a complete managed service. Detailed readiness gates: [docs/roadmap.md](docs/roadmap.md).
