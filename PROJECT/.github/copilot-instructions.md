<!--
This file guides AI coding agents working in this repository.
-->
# Copilot instructions for this repository

**Purpose:** Quick, actionable guidance for an AI coding agent to become productive in this repository.

---

## ⚠️ CRITICAL: Read Development Philosophy First

Before writing ANY code, read: **`docs/development/LUCID/DEVELOPMENT_PHILOSOPHY.md`**

### The LUCID Philosophy (Summary)
1. **L - Lean:** KISS, DRY, Max 3 indents
2. **U - User-First:** UI drives architecture
3. **C - Contracted:** Pre/postconditions, docstrings
4. **I - Immutable:** Functional internals, pure functions
5. **D - Driven:** **TESTS FIRST**, Data-driven (no hardcoding)

### The Golden Rule
```
NO implementation code exists without a FAILING TEST first.
```

### Commit Convention
```
<type>(<scope>): <subject>

Types: feat, fix, docs, refactor, test, chore, wip
```

**WIP commits** (`[WIP]` or `wip:`) skip CI tests but still run linting.

---

**Initial discovery (first steps)**
- **Scan for high-level manifests:** Look for `README.md`, `package.json`, `pyproject.toml`, `setup.cfg`, `Pipfile`, `requirements.txt`, `Cargo.toml`, `go.mod`, `composer.json`, `Makefile`, `Dockerfile`, and `.github/workflows/*.yml`.
- **Locate source roots:** Search for top-level folders like `src/`, `app/`, `lib/`, `services/`, or `packages/`.
- **Identify tests and CI:** Find `tests/`, `spec/`, `.github/workflows/`, or any `*.test.*`/`*_test.*` files.
- **Commands to run locally (PowerShell):**
  - Search for manifests: `Get-ChildItem -Recurse -File -Include package.json,pyproject.toml,README.md,Makefile,Dockerfile | Format-Table FullName`
  - Search for agent docs: `Get-ChildItem -Recurse -File -Include AGENT.md,AGENTS.md,CLAUDE.md,copilot-instructions.md | Select-Object FullName`

**How to infer the "big picture" architecture**
- **Start with manifests and entry points:** `package.json` `main`/`scripts`, `pyproject.toml` `tool.poetry.scripts`, `Dockerfile` `CMD`/`ENTRYPOINT` are primary clues to how the project runs.
- **Follow imports/exports:** Build a small dependency map by scanning `import`/`require`/`from` statements to locate service boundaries and shared modules.
- **Check `README.md` and `.github/workflows/`:** CI jobs often reveal build/test steps and integrations (e.g., database services, linters, test matrix).

**Critical developer workflows**
- **Build:** If `package.json` present, prefer `npm run build` or `yarn build`; if `pyproject.toml`, prefer `python -m build` or `pip install -e .`.
- **Tests:** Look for `pytest`, `npm test`, `go test`, or `cargo test` in manifests. Use CI workflow files to reproduce the same test matrix locally.
- **Debugging:** If the project uses Docker, inspect `docker-compose.yml` or `Dockerfile` for service ports and volumes to reproduce behavior.

**Project-specific conventions & patterns**
- **When files exist:** Use concrete examples from the repository. For example, if you find `src/api/server.ts` and `src/workers/*`, treat them as the public API server vs background workers.
- **Naming patterns to respect:** Prefer existing folder names and exports; do not rename `src/` to `lib/` unless the project already uses that pattern.

**Integration points & external dependencies**
- **Look for credential and config patterns:** Common locations: `.env`, `config/`, `secrets/`, `Azure`, `AWS`, or `GCP` infra files. Do not attempt to create or commit secrets.
- **Cross-component communication:** Search for REST endpoints, message broker clients (`rabbitmq`,`kafka`), or database clients. Note queue/topic names and schemas when present.

**Merging strategy (if this file already exists)**
- Preserve existing sections unless clearly incorrect.
- Append a `Discovery log` section with timestamped findings.
- Highlight changed commands or new CI workflow references under a `Local commands` subsection.

**Minimal actionable checklist for the agent**
1. Run the manifest search commands (PowerShell) above.
2. If no manifests found, report back to the human: "Repository contains no source files or manifests—please point me to the project folder or add files.".
3. If manifests found, extract build/test scripts and add them to the `Local commands` subsection here.
4. Identify top 3 files that define architecture (entrypoint, main service, and tests) and list them in `Discovery log`.

**When to ask the human**
- If the repo is empty or missing manifests, request the path to the code to scan.
- If secrets/configs are required to run tests or services, ask for a redacted example `.env` or access instructions.

**Contact & iteration**
- After making changes, create a concise summary of what you changed and why in a PR description or commit message and ask for feedback.

---
<!-- End of file. Agent: after running discovery steps, update the "Discovery log" and "Local commands" sections with concrete findings. -->
