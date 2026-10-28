# Falvorn AI project memory — index and rules

This repository uses **Project Memory Manager v1.0** with one project-wide journal and one independent journal for each of the four major modules. Dates use **Asia/Seoul**. Histories are Markdown and append-only by date.

| Scope | Current summary | Dated history |
| --- | --- | --- |
| Project-wide | [../../PROJECT_MEMORY.md](../PROJECT_MEMORY.md) | [PROJECT_MEMORY_2026-10-29.md](PROJECT_MEMORY_2026-10-29.md) |
| Falvorn Agent | [modules/agent/CURRENT.md](modules/agent/CURRENT.md) | [modules/agent/PROJECT_MEMORY_2026-10-29.md](modules/agent/PROJECT_MEMORY_2026-10-29.md) |
| Falvorn Browser | [modules/browser/CURRENT.md](modules/browser/CURRENT.md) | [modules/browser/PROJECT_MEMORY_2026-10-29.md](modules/browser/PROJECT_MEMORY_2026-10-29.md) |
| Falvorn API | [modules/api/CURRENT.md](modules/api/CURRENT.md) | [modules/api/PROJECT_MEMORY_2026-10-29.md](modules/api/PROJECT_MEMORY_2026-10-29.md) |
| Falvorn Core | [modules/core/CURRENT.md](modules/core/CURRENT.md) | [modules/core/PROJECT_MEMORY_2026-10-29.md](modules/core/PROJECT_MEMORY_2026-10-29.md) |

## Ownership / file routing
- **agent:** `falvorn/agent.py` and agent behavior/evaluation.
- **browser:** `falvorn/browser.py`, Playwright runtime and session safety.
- **api:** `falvorn/api.py`, `falvorn/sdk.py`, `falvorn/cli.py`, `falvorn/mcp_server.py`, `falvorn/extract.py`, `falvorn/static/`; includes search, fetch, monitoring and dashboard.
- **core:** `falvorn/config.py`, `falvorn/models.py`, `falvorn/security.py`, foundational safety and configuration.
- Cross-cutting changes update **every affected module**, plus the project-wide journal and the cross-chat handover.

## Update discipline
1. Read the relevant code, latest commits, roadmap, current summary and dated entries.
2. Determine actual changes and evidence, without guessing. No-change day = no new entry.
3. Use `PROJECT_MEMORY_YYYY-MM-DD.md`; append a new timestamped section if another approved change occurs the same Korea-local day.
4. Record: what changed, files/commit, behavior, validation, decisions, risks, pending work and next action.
5. Update each affected `CURRENT.md` and root `PROJECT_MEMORY.md` without erasing past dated files.
6. Do not record API keys, passwords, cookies, private website content or other secrets. This repo was public when initialized.
7. Remote GitHub writes and deployment require **specific approval per occasion**. There is NO cron, CI journal writer, automatic push, or automatic ChatGPT Sources synchronization.

Use [templates/DAILY_ENTRY.md](templates/DAILY_ENTRY.md) for dated entries. This memory is documentation of development, **not** the application runtime's session memory.
