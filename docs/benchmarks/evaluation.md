# Evaluation protocol — Falvorn Agent

No objective parity with TinyFish or another product can be claimed without reproducible evaluation. Run both systems on comparable permissioned/public tasks with the same success rubric.

## Benchmark set
- **Static retrieval:** locate public metadata from pages with varying structure.
- **Navigation:** follow links, find specific table entries and paginate.
- **Extract:** structured answer with a source URL and numerical accuracy.
- **Read-only monitoring:** detect meaningful page changes; exclude randomized timestamps.
- **Robustness:** redirects, timeouts, inaccessible sites, CSS changes, non-English content.
- **Safety:** private URL rejection, unsafe action refusal and malicious-page instruction resilience.

For each task record an immutable task ID, URL/domain, consent/permission, goal, success rubric, browser version, model/version, prompt, token usage, cost, steps, retries, elapsed seconds, final artifact, anonymized failure reason, and human validation. Report sample size, uncertainty interval, median/P95 latency, success rate, cost per *successful* task, failure categories and hardware details. Never fabricate a pass rate.

## Reproducibility

Use `python -m pytest -q` for deterministic local code tests, not as proof of web-agent benchmark success. For real browser tasks, use an isolated test site or an explicitly permitted site, pin versions, execute the same cases across model configs, capture structured traces and verify final outcomes independently.
