# FALVORN AI — CANONICAL PROJECT MEMORY

> **Revision:** 2026-10-29.1 (Asia/Seoul) · **Reference repository:** https://github.com/hossain0707/Falvorn-AI · **Memory format:** Project Memory Manager v1.0

## Purpose / cross-chat instructions
This is the **complete handover snapshot** intended for manual inclusion in **ChatGPT Project → Falvorn AI → Sources**. Read it before resuming work. Also inspect repository code and latest commits; this static snapshot will not update itself. Never infer that ChatGPT Project Sources changed because GitHub files changed.

## Identity and objectives
- **Brand:** Falvorn AI — *Intelligence Without Limits*.
- **Flagship product:** Falvorn Agent. Supporting components: Falvorn Browser, Falvorn API and Falvorn Core.
- **Goal:** Independently engineered autonomous web agent/browser automation system with self-hosted/private-first potential; publicly observable TinyFish capabilities may inform comparisons, but proprietary code is not copied.
- **Engineering form:** a modular monolith implemented in the `falvorn/` Python package, **not** four deployed production services.
- **Repository:** `hossain0707/Falvorn-AI`; branch `main`; repository was **public** at baseline review. Do not commit secrets or private client information.

## Confirmed baseline
- **v0.1.0** source was published on **2026-10-28**; verified baseline GitHub main commit at time of this review: `6f17f8fdd1b4e3686b4ff22c56c6718f47f158f5`.
- Working-source features: bounded goal agent loop, local Playwright/Chromium contexts, FastAPI endpoints, optional SearXNG search, HTML extraction, manual SQLite page-change checks, Python SDK/CLI, optional MCP adapter and web dashboard.
- Previously **reported**: 9 passing tests in the initial local prototype build. **Not rerun in this memory-integration session.**
- Production deployment, live public-site automation, commercial performance parity, authenticated browser vault, distributed workers, multi-tenancy and scheduled monitoring have **not been verified as complete**.

## Module reference snapshots
- **Falvorn Agent:** [current](project_memory/modules/agent/CURRENT.md) · [baseline](project_memory/modules/agent/PROJECT_MEMORY_2026-10-29.md)
- **Falvorn Browser:** [current](project_memory/modules/browser/CURRENT.md) · [baseline](project_memory/modules/browser/PROJECT_MEMORY_2026-10-29.md)
- **Falvorn API:** [current](project_memory/modules/api/CURRENT.md) · [baseline](project_memory/modules/api/PROJECT_MEMORY_2026-10-29.md)
- **Falvorn Core:** [current](project_memory/modules/core/CURRENT.md) · [baseline](project_memory/modules/core/PROJECT_MEMORY_2026-10-29.md)

## Architecture and dependencies
- Agent planning in `falvorn/agent.py` uses the Browser pool and Core settings/models.
- API in `falvorn/api.py` exposes browser sessions, agent runs, fetch/search/monitor and uses Core safety checks.
- Supporting API-facing components live in `falvorn/sdk.py`, `falvorn/cli.py`, `falvorn/mcp_server.py`, `falvorn/extract.py`, `falvorn/static/index.html`.
- Core configuration and safety are in `falvorn/config.py`, `falvorn/models.py`, `falvorn/security.py`.

## Development decisions
1. One repo and four primary product domains; preserve modular monolith boundary until explicit service decomposition is justified.
2. Private-first, bounded, safety-conscious execution; prompt-injection and network-safety defenses are **not** guaranteed by current heuristics.
3. Separate implemented capability from roadmap and unverified claims; no 100% TinyFish replica claims.
4. Date each meaningful memory change in Asia/Seoul; preserve history and keep module-specific entries.
5. **Never auto-push, auto-deploy, auto-update Project Sources or silently publish memory.** Require explicit authorization per remote change.

## Current known risks
- SSRF / DNS rebinding needs network-isolated browser egress.
- Agent prompt-injection resistance and consequential action approvals require hardening.
- Runs/sessions are volatile; no durable queue, credential vault or tenant auth.
- API reliability, live-site success and production readiness still need measured validation.

## Next engineering actions
- [ ] Define public, repeatable benchmark tasks with success criteria, latency and cost reporting.
- [ ] Add durable run state, cancellation/retry and trace/audit persistence.
- [ ] Harden outbound egress and isolate browser workers in containers.
- [ ] Expand contract/security tests and verify live site behavior where permitted.
- [ ] Keep module histories current **when explicitly requested and supported by evidence**.

## Memory maintenance
- **Project journal:** [project_memory/PROJECT_MEMORY_2026-10-29.md](project_memory/PROJECT_MEMORY_2026-10-29.md)
- **Rules & file ownership:** [project_memory/README.md](project_memory/README.md)
- **Skill guide:** [.agents/skills/falvorn-project-memory/SKILL.md](.agents/skills/falvorn-project-memory/SKILL.md)
- **Cross-chat runbook:** [docs/memory_workflow.md](docs/memory_workflow.md)
- **Repository AI instructions:** [AGENTS.md](AGENTS.md)

**ChatGPT Sources status:** no automatic upload/sync is configured. To use this handover as ChatGPT Project Sources, the user must manually add or replace the complete `PROJECT_MEMORY.md` file.
