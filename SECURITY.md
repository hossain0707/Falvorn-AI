# Security policy

## Current maturity

**Falvorn AI v0.2 is an experimental single-user MVP, not a hardened production multi-tenant service.** Do not expose it directly to the public Internet, use it to store real credentials, or connect it to high-stakes accounts.

## Sensitive disclosure

Please **do not publish proof-of-concept exploits or secrets in public issues**. Contact the repository owner using GitHub's private security advisory workflow when enabled, or another private channel agreed with the maintainer. Remove credentials and personal data from all logs or reproductions.

## Security model

- The API key gates sensitive endpoints; never reuse production secrets or check them into Git.
- Browser sessions run locally in isolated Playwright contexts, **not** hardened sandboxes.
- Private-network URL filtering is a partial SSRF mitigation, not a substitute for network egress isolation or DNS pinning.
- Untrusted webpage text may prompt-inject a model. The default agent policy restricts actions and favors read-only workflows.
- There is no tenant isolation, KMS-backed vault, or enterprise RBAC. Local run event history persists in SQLite, but it is not a tamper-resistant production audit store.

## Before any public deployment

Implement outbound egress controls, proper tenant identities, durable audit logs, session encryption, per-task approvals for consequential actions, rate limits, and independent penetration testing.
