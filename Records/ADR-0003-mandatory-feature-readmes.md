# ADR-0003: Mandatory Feature READMEs

## Status
**Accepted**

## Date
2025-11-27

## Context

As codebases grow, understanding the purpose, scope, and dependencies of individual features becomes difficult. Information is often scattered across code comments, global documentation, or lost entirely. We need a decentralized documentation strategy that keeps context close to the code ("Locality of Reference").

This applies to all LUCID projects regardless of domain.

## Decision

Every feature directory (e.g., `features/<feature_name>/`) must contain a `README.md` file that serves as the definitive source of truth for that feature.

### Required Structure
1. **Scope:** What this feature does (and what it does NOT do)
2. **Value:** Why this feature exists and what business value it provides
3. **Architecture:** Mermaid diagrams (Class/Sequence) explaining internal design
4. **Dependencies:**
   - **Internal:** Which other features this one relies on (coupling)
   - **External:** Third-party libraries used
5. **Investigations:** Links to any `docs/development/investigations/` related to this feature
6. **Metrics (Fun Part):** Automated statistics about the feature

### How This Enforces LUCID

| Principle | Enforcement |
|-----------|-------------|
| **L - Lean** | Feature scope is explicit—prevents feature creep |
| **U - User-First** | "Value" section forces us to articulate user benefit |
| **C - Contracted** | Dependencies and scope form an implicit contract |
| **D - Driven** | Metrics section is data-driven, not guesswork |

## Benefits for All Projects

1. **Onboarding**: New developers can understand any feature in any LUCID project the same way
2. **Template Included**: `PROJECT_TEMPLATE/features/FEATURE_README_TEMPLATE.md` provides the structure
3. **Coupling Visibility**: Explicit dependency listing highlights coupling issues early
4. **Consistency**: All features, all projects, same documentation standard
5. **Maintenance**: Documentation lives with code, increasing update likelihood

## Alternatives Considered

1. **Centralized Docs:** Keeping all docs in `docs/`
   - *Cons:* Docs rot faster when separated from code
2. **Docstrings Only:** Relying solely on Python docstrings
   - *Cons:* Good for API details, bad for high-level overview

## Consequences

### Positive
- **Discoverability:** New developers can open a folder and immediately understand "What is this?"
- **Maintenance:** Documentation lives with the code
- **Visibility:** Explicit dependency listing highlights coupling issues early

### Negative
- **Overhead:** Requires creating and maintaining an extra file per feature
- **Duplication:** Potential overlap with global architecture docs

## Related
- ADR-0002: Standardize on Mermaid for Diagrams
- `PROJECT_TEMPLATE/features/FEATURE_README_TEMPLATE.md`
