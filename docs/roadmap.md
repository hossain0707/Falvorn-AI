# Falvorn AI product roadmap

| Priority | Capability | Current status | Exit requirement |
|---|---|---|---|
| P0 | Branded MVP / local dashboard | Initial implementation | All tests and manual smoke checks pass |
| P0 | Safe browser navigation | Partial | Reproducible live-site cases and action logs |
| P0 | Goal-based agent | Initial implementation | Correct task completion measured on a published task suite |
| P0 | API + Python CLI/SDK + MCP | Initial adapters | Contract tests, stable schemas and versioning |
| P1 | Persistent runs / retry / cancellation | Not implemented | Durable event store, idempotency and replay |
| P1 | Screenshot + accessibility reasoning | Not implemented | Measurable uplift vs DOM-only baseline |
| P1 | Remote browser workers / CDP | Not implemented | Isolated workers + session cleanup guarantees |
| P1 | Login consent / vault | Not implemented | Secret encryption, approval and access audit |
| P2 | Organizations, RBAC, metering | Not implemented | Tenant-isolated end-to-end tests |
| P2 | Distributed agent execution | Not implemented | Load tests, autoscaling and cost controls |
| P2 | Scheduled monitoring + notifications | Not implemented | Reliable scheduling and delivery tests |
| P3 | Public SaaS / billing | Not implemented | Security review, observability, support and compliance |

**Benchmark policy:** record workload, websites, sample size, success criterion, model, seed/temperature, median/P95 latency, cost per successful task, and failure breakdown. Do not claim commercial parity until independently tested.
