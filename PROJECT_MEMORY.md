# Falvorn AI — canonical project handover

> **Snapshot:** 2026-10-29 (Asia/Seoul) · **Published release:** [v0.2.0](https://github.com/hossain0707/Falvorn-AI/releases/tag/v0.2.0). Release and binary assets verified on GitHub; code/media branch baseline `a6b58f7ef1f1831cf5399ebba745945336698d3f`. Verify the live repository before making subsequent claims.

## Identity

- Brand: **Falvorn AI**, tagline **Intelligence without limits**; proprietor: **Md Najmul Hossain**.
- Github: https://github.com/hossain0707/Falvorn-AI (public repo at last read).
- Concept: independent TinyFish-like AI browser automation and agent platform; no proprietary TinyFish code, endorsement or full-parity claim.
- **Falvorn Agent**, **Falvorn Browser**, **Falvorn API** and **Falvorn Core** are conceptual modules within the current single-package Python monolith.
- Proprietary all-rights-reserved LICENSE; third-party libraries retain their own licenses.

## GitHub and source-of-truth policy

GitHub `main` includes v0.2 release source and media as of commit `a6b58f7ef1f1831cf5399ebba745945336698d3f` (previous memory commit `f234cdc9f09788e0a0ee103accdc02d63463f08a` remains in history). The [v0.2.0 GitHub Release](https://github.com/hossain0707/Falvorn-AI/releases/tag/v0.2.0) is published with source ZIP, GIF and MP4 assets. Read the live repository before changing remote code. **No unattended commits, pushes, deployments, project-memory syncing or ChatGPT Sources writes.**

## Engineering state — v0.1 baseline (2026-10-28)

Earlier source included a bounded optional LLM planner, local Chromium/Playwright sessions, HTML extraction, SearXNG search adapter, FastAPI, Python SDK/CLI, MCP adapter, manual SQLite hash monitor and a responsive dashboard. Nine automated tests were historically reported passing. Real external-site task completion was **not** verified; memory files were initialized on GitHub on 2026-10-29.

## Published v0.2.0 release (2026-10-29)

- Added persistent **SQLite WAL run/event store** with restart marking of interrupted tasks; run list and cancellation endpoints. The system remains **single-node/in-process**.
- Added **authenticated screenshot endpoint** for active browser session views.
- Added persisted **monitor subscriptions**, optional single-process interval scheduler (off by default), CRUD/pause/resume API, extended Python SDK.
- Updated dashboard with recent runs and cancellation controls, README and separate product walkthrough assets: original SVG hero, animated architecture, GIF preview, 41-second MP4 with original soundtrack.
- Added proprietary LICENSE, updated security threat model, architecture, evaluation protocol, roadmap and tests.
- **Verified in current environment:** 14 tests passed, code compiled, local `POST /v1/fetch` returned structured content for synthetic localhost page.
- **Not verified:** Chromium live URL navigation (blocked by sandbox administrator), production SaaS, distributed workers, real-world agent success, user credential vault, notifications, load/security review. Product video's planner trace is **explicitly illustrative**.
- **Remote status:** source and media published to `main`; public v0.2.0 GitHub Release and its ZIP/GIF/MP4 attachments independently verified on 2026-10-29. This is a GitHub software release, **not** a live hosted SaaS deployment.

## Module handovers

- [Agent](project_memory/modules/agent/CURRENT.md): optional LLM planner, bounded loops, durable run/event history, cancel and basic SSE.
- [Browser](project_memory/modules/browser/CURRENT.md): Playwright contexts, guarded actions/URLs, DOM and screenshot snapshot.
- [API](project_memory/modules/api/CURRENT.md): FastAPI, SDK, MCP, extraction, search adapter, subscriptions and UI.
- [Core](project_memory/modules/core/CURRENT.md): config, Pydantic models, URL policy, single-node SQLite store.

## Safety/reliability gaps that must not be overstated

No production-grade DNS-pinned egress firewall, secure vault, tenancy, distributed queue, cost-controlled multi-model routing, comprehensive anti-injection or human-approval workflow, immutable audits, multi-domain benchmarks or production SLOs. The production-grade *presentation* of the documentation is distinct from the application's actual production readiness.

## Next engineering priorities

1. Containerized worker isolation and network-level private-IP/metadata deny policies; independent security review.
2. Durable Redis/Postgres-backed task queue with idempotency and replay controls before multi-worker SaaS.
3. Screenshot/accessibility navigation, reliability and end-to-end authorized browser task benchmarking.
4. Robust authentication, per-tenant access controls, encrypted secret vault and approval workflow.
5. Deploy a private beta only after CI, OS smoke tests and threat model gates pass.

## Continuous documentation convention

Read [AGENTS.md](AGENTS.md) and [project_memory index](project_memory/README.md). Each approved meaningful change should update the project journal and every affected module's dated journal and `CURRENT.md`. No-change days do not produce empty files. Project Sources in ChatGPT only update when user manually uploads a refreshed `PROJECT_MEMORY.md`; a repo commit does not itself update Sources.

## Project memory folder mirror

- A **reviewed copy** of this handover is maintained at [project_memory/PROJECT_MEMORY.md](project_memory/PROJECT_MEMORY.md) to keep the module histories and master snapshot together.
- The root `PROJECT_MEMORY.md` remains canonical. Both copies must be updated together on **explicitly approved** documentation changes; there is no automatic synchronization or background GitHub writer.
