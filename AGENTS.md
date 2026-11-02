# Falvorn AI — agent/contributor instructions

Read `PROJECT_MEMORY.md`, `project_memory/README.md`, the latest module `CURRENT.md`, `README.md`, `docs/roadmap.md`, and relevant source before changing anything. The repo is an experimental modular monolith with four product boundaries, not four commercial services.

- Never conflate implemented code with a validated deployment or claims of full TinyFish equivalence.
- Date meaningful history in Asia/Seoul as `PROJECT_MEMORY_YYYY-MM-DD.md`. Create entries only on actual changes; append a timestamped block if there are multiple updates the same day.
- Refresh the affected module `CURRENT.md` and the root cross-chat `PROJECT_MEMORY.md` after inspecting real diffs and tests. Record evidence and remaining risks.
- Never write secrets, credentials, authentication cookies, private account details or sensitive site contents to Markdown logs.
- Never auto-push, auto-merge, auto-deploy, schedule a GitHub writer or silently change ChatGPT Project Sources. **Each remote write requires specific user authorization.**
- The repository skill at `.agents/skills/falvorn-project-memory/SKILL.md` guides compatible coding agents; it is not automatically installed as a global ChatGPT skill.
- Application runtime state and project-development memory are distinct things. SQLite records runtime events; Markdown records engineering history.

- **New isolated product (2026-11-02):** `products/social-orchestrator/` is an engineering beta. Use `project_memory/modules/social/CURRENT.md` for its scope and dated history; keep the separate API, key space, scheduled worker and integration status distinct from the original four modules. Do not claim external social publishing is validated without real API integration tests.
