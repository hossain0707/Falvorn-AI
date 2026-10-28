# Project Memory Manager — implementation guide

Project-wide and per-module journal files are human-readable Markdown. Update the root `PROJECT_MEMORY.md`, the top-level dated journal, and each affected module's current and dated logs after an actual code change, with explicit user authorization for GitHub publication.

1. Read `AGENTS.md`, latest GitHub state and source code; compare the actual changes.
2. Classify changed modules (Agent/Browser/API/Core) and collect tests/evidence.
3. Use Asia/Seoul calendar date; append new entries on an existing day instead of overwriting previous development records.
4. Distinguish verified implementation, reported historical tests, failed checks and outstanding tasks.
5. Commit or deploy **only** with explicit approval. Do not enable an automatic writer or push via CI.
6. Optionally upload root `PROJECT_MEMORY.md` manually to the user's ChatGPT Project → Sources to improve cross-chat handovers; Github and ChatGPT Sources are not automatically synced.
