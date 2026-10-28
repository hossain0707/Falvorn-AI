# Falvorn AI roadmap / delivery gates

| Stage | Capability | Current status | Proof required |
| --- | --- | --- | --- |
| v0.2 | Branded dashboard / REST / SDK / MCP | Implemented local MVP | API and browser tests on target OS |
| v0.2 | Durable run history and cancellation | Implemented single-node | Restart + interrupted-run tests |
| v0.2 | Screenshot snapshot endpoint | Implemented | Auth and controlled browser regression |
| v0.2 | Monitor subscriptions | Implemented; scheduler optional | Live timer delivery and restart tests |
| v0.2 | Product demos, README, architecture and proprietary license | Provided as artifacts | Media integrity and GitHub rendering check |
| P0 | Browser egress isolation and adversarial security | Not complete | Independent security review |
| P0 | Reproducible public-site navigation benchmarks | Not complete | Measured success/latency and honest failure reporting |
| P1 | Durable task queue / retries / replay / worker fleet | Not implemented | Load + failure recovery tests |
| P1 | Screenshot + accessibility model reasoning | Not implemented | Measured accuracy improvement |
| P1 | User-consented auth vault / persistent profiles | Not implemented | Vault/key rotation/privacy tests |
| P2 | Tenant-aware SaaS, billing, RBAC, organization controls | Not implemented | Tenant isolation and payment audit |
| P2 | Real monitor notifications and dashboard monitoring | Partial | Scheduled delivery SLA test |
| P3 | Production release | Not declared | Security, reliability, legal/compliance gates |

The media assets are product demos, **not evidence of production certification**.
