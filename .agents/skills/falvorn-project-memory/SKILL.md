---
name: falvorn-project-memory
description: Maintain truthful, module-specific Falvorn AI project memory and cross-chat handover files without automatic remote writes.
---

# Falvorn Project Memory Manager v1.0

**Trigger:** The user asks to resume, summarize, reconcile, document, update, or hand over work on Falvorn AI, or explicitly approves recording a meaningful implemented change.

## Read
1. Repository `AGENTS.md`, `PROJECT_MEMORY.md`, `project_memory/README.md`.
2. Affected `project_memory/modules/<module>/CURRENT.md`.
3. Latest dated history for the affected modules and project-wide log.
4. Relevant source files and GitHub commit/PR references when available.

## Update (with explicit user approval for remote writes)
1. Identify changed modules **agent / browser / api / core**, with multiple selections if needed.
2. Inspect actual diff and test evidence. Record what was changed, removed, fixed, decided, tested, failed and left pending.
3. In Asia/Seoul date `YYYY-MM-DD`, create or append the matching `PROJECT_MEMORY_YYYY-MM-DD.md` in each affected module and the top-level `project_memory/` history.
4. Refresh affected `CURRENT.md` summaries; update root `PROJECT_MEMORY.md` as the complete cross-chat handover.
5. Retain older history. Do not create entries on days with no substantive change.
6. Check links, source references, status labels and secrets before offering any commit.

## Response / handover
- Give a short change summary, precise files affected, verification evidence and open tasks.
- Offer root `PROJECT_MEMORY.md` for **manual upload/replacement** in ChatGPT Project → Sources.
- A local draft or read-only review does **not** imply GitHub commit/push approval.

## Hard stop rules
- **Never** auto-commit, auto-push, deploy, edit Project Sources, schedule a writer or silently modify remote resources.
- Each remote write must be specifically authorized by the user.
- Never claim the project memory is continuously synchronized with ChatGPT, other chats, GitHub, or a background service.
- Do not put confidential data, credentials, session cookies or private user material in committed Markdown.
- Distinguish implemented, partially validated, planned and unverified capabilities.

This repository skill document provides guidance for compatible agents; **adding it here does not install a global ChatGPT skill**.
