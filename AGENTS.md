# Agent instructions — Falvorn AI

This file is for coding assistants, ChatGPT workflows and human contributors. Read it **before modifying** code or project records.

1. Start with [PROJECT_MEMORY.md](PROJECT_MEMORY.md), [project_memory/README.md](project_memory/README.md), [README.md](README.md), [docs/roadmap.md](docs/roadmap.md), and the current notes for affected modules.
2. This is one **experimental modular monolith**, not four independent production-ready products. Keep feature claims aligned with the actual implementation.
3. Map touched files to modules using [project_memory/README.md](project_memory/README.md). A cross-cutting change can update several module histories.
4. After a **substantive change**, prepare a truthful dated entry (`PROJECT_MEMORY_YYYY-MM-DD.md`) for each affected module and the project-wide log; update the current summaries and changelog when appropriate. Reuse the same Asia/Seoul calendar date; append clearly delimited entries if changed twice in one day.
5. Separate **verified tests** from historical reports, assumptions and pending validation. Never fabricate metrics, releases, GitHub activity or deployment success.
6. Preserve historical dated files: never delete/rewrite old dates as a shortcut. No-change day = no new daily file.
7. **No automatic GitHub push, commit, merge, deploy, GitHub Actions memory-writer or ChatGPT Project Sources mutation.** Ask for **explicit authorization for each remote write**. Local draft updates are allowed only when the user asks for the memory workflow.
8. ChatGPT Project → Sources must be updated **manually by the user** with the complete [PROJECT_MEMORY.md](PROJECT_MEMORY.md) snapshot; repository edits do not synchronize those sources.
9. Do not write credentials, tokens, cookies, personal data, browser session content or proprietary third-party code to memory files.
10. Use [.agents/skills/falvorn-project-memory/SKILL.md](.agents/skills/falvorn-project-memory/SKILL.md) for the practical handover procedure.

Current release baseline: v0.1.0 (2026-10-28). This memory system was initialized as a documentation-only change on 2026-10-29 (Asia/Seoul).
