# ADR-0001: Single repository with modular product components

**Status:** Accepted (2026-10-28)

## Context
Falvorn Agent, Browser, API, and Core are strongly coupled during MVP development. Separate repos would add release and dependency coordination before the interfaces are stable.

## Decision
Start with a single `Falvorn-AI` repository. Keep implementation in a Python `falvorn/` package grouped by module; preserve versioned API contracts and establish clear components in documentation. Split services or repos only after deployment, ownership and scaling constraints justify it.

## Consequences
Simpler CI, reviews and atomic changes, but eventual service separation will require contract tests and migration planning. Current architecture is a **modular monolith**, not a completed multi-service platform.
