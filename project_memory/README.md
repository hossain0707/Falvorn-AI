# Falvorn AI — module memory index

Dates use Asia/Seoul. `CURRENT.md` is a living module handover; dated journals preserve change history. Root `PROJECT_MEMORY.md` is the canonical cross-chat handover; [`project_memory/PROJECT_MEMORY.md`](PROJECT_MEMORY.md) is its reviewed in-folder copy. A code change touching multiple modules updates each applicable module and the project-wide memory.

| Scope | Handover | Latest log |
|---|---|---|
| Overall | [Master copy](PROJECT_MEMORY.md) · [Root canonical](../PROJECT_MEMORY.md) | [2026-10-29](PROJECT_MEMORY_2026-10-29.md) |
| Agent | [CURRENT](modules/agent/CURRENT.md) | [2026-10-29](modules/agent/PROJECT_MEMORY_2026-10-29.md) |
| Browser | [CURRENT](modules/browser/CURRENT.md) | [2026-10-29](modules/browser/PROJECT_MEMORY_2026-10-29.md) |
| API | [CURRENT](modules/api/CURRENT.md) | [2026-10-29](modules/api/PROJECT_MEMORY_2026-10-29.md) |
| Core | [CURRENT](modules/core/CURRENT.md) | [2026-10-29](modules/core/PROJECT_MEMORY_2026-10-29.md) |

**Routing:** `agent.py` → Agent. `browser.py` → Browser. `api.py`, `sdk.py`, `cli.py`, `mcp_server.py`, `extract.py`, `static/` → API. `config.py`, `security.py`, `models.py`, `store.py` → Core (run-store also affects Agent and monitoring).

Remote publication and ChatGPT Project Sources updates are manual/explicitly authorized only. See [the repository memory skill](../.agents/skills/falvorn-project-memory/SKILL.md) and [template](templates/DAILY_ENTRY.md).

**Sync rule:** When a meaningful change is explicitly approved for GitHub publication, refresh both `../PROJECT_MEMORY.md` and `project_memory/PROJECT_MEMORY.md` in the same commit. Nothing updates ChatGPT Project Sources automatically.
