---
name: falvorn-project-memory
description: Maintain source-grounded project-wide and per-module Falvorn AI development history without automatic remote writes.
---

# Falvorn Project Memory Manager v1.0

1. Read `AGENTS.md`, `PROJECT_MEMORY.md`, `project_memory/README.md` and `project_memory/modules/<module>/CURRENT.md`.
2. Inspect actual latest source and changed commits/diffs before assuming any current feature or deployment state.
3. Classify changes among **agent**, **browser**, **api**, **core**; cross-cutting changes may affect more than one module.
4. Use Korea-local date (`Asia/Seoul`) in `project_memory/PROJECT_MEMORY_YYYY-MM-DD.md` and corresponding module-dated entries. Append entries to existing dates rather than overwriting previous histories.
5. Update current module summaries and root `PROJECT_MEMORY.md`, including changed files, verified tests, risks, decisions, next work. Distinguish historical test claims from tests actually executed now.
6. No new daily journal on days with no meaningful change.
7. Do not store API keys, personal data, private web content or session cookies.
8. **No automatic GitHub push/merge/deployment/Project Sources modification.** Explicit user permission is required for each remote update.
9. In a new ChatGPT conversation, provide root `PROJECT_MEMORY.md` as an optional **manual** ChatGPT Project → Sources upload. This does not synchronize itself.

The skill file is repository guidance for compatible assistants, **not a globally installed ChatGPT skill**.
