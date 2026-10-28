# Project memory and ChatGPT continuity

Falvorn AI uses [Project Memory Manager v1.0](../.agents/skills/falvorn-project-memory/SKILL.md). The purpose is to preserve **engineering continuity**, not to imply that ChatGPT automatically observes repositories or edits Project Sources.

## In a new ChatGPT conversation
Read this repository's [PROJECT_MEMORY.md](../PROJECT_MEMORY.md), [AGENTS.md](../AGENTS.md), the appropriate module `CURRENT.md`, the most recent dated entries and actual source code. Treat code and recent verified GitHub history as the authority if memory prose is outdated.

## After meaningful development
Prepare an updated project-wide journal entry plus separate entries for each affected module. For example, a change to browser navigation and safety URL checks impacts **browser** and **core**, so both must receive a dated entry. Never create journal spam when nothing changed.

## ChatGPT Project Sources
The canonical cross-chat handover is the complete repository-root **PROJECT_MEMORY.md**. The user can download or copy it into **ChatGPT Project → Sources** and replace the earlier copy after major approved changes. **No tool action in this workflow silently updates Project Sources.** A different ChatGPT conversation does not necessarily have live knowledge of a new GitHub commit until it reads it.

## GitHub write policy
Reading is fine. For each publication to GitHub, ask for explicit permission describing the files, repository and intended change; do **not** turn on scheduled journal commits, GitHub Actions push writers, auto-merge or deployment. If a user only asked for a memory draft, keep it local.

## Quality bar
Each entry must specify exact date (Asia/Seoul), changed paths, evidence, what works, what is unverified, tests executed now versus historical reports, security limitations, decisions and next tasks. Keep sensitive data out of public repositories.
