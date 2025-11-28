# ADR-0002: Standardize on Mermaid for Diagrams

## Status
**Accepted**

## Date
2025-11-27

## Context

Projects often use a mix of ASCII art and ad-hoc methods for visualizing architecture and flows. This leads to:
1. **Inconsistency:** Different styles make documentation harder to read
2. **Maintenance Burden:** ASCII art is difficult to edit and maintain as code changes
3. **Lack of Portability:** ASCII diagrams may render poorly depending on fonts and viewports
4. **Searchability:** Text within ASCII diagrams is often hard to search or parse

We need a standard way to create diagrams that aligns with our "Docs as Code" philosophy and works across all LUCID projects.

## Decision

All LUCID projects will use **Mermaid.js** for architectural, sequence, flow, and state diagrams.

1. **Format:** All diagrams must be written in Mermaid syntax inside markdown code blocks
2. **Location:** Diagrams specific to a feature should live in that feature's `README.md`. Global architecture diagrams live in `docs/`
3. **Tooling:** Developers should use the "Markdown Preview Mermaid Support" extension in VS Code

### How This Enforces LUCID

| Principle | Enforcement |
|-----------|-------------|
| **L - Lean** | Text-based diagrams are simpler to maintain than binary images or complex tools |
| **U - User-First** | Visual diagrams help users understand architecture quickly |
| **C - Contracted** | Diagrams document the "contract" between components visually |
| **D - Driven** | Diagrams as code means they're version-controlled and data-driven |

## Benefits for All Projects

1. **Consistency**: All LUCID projects have the same diagram style
2. **Portability**: Templates in PROJECT_TEMPLATE include diagram examples
3. **Zero External Dependencies**: No Java (PlantUML), no image editors
4. **Native GitHub/GitLab Support**: Renders automatically in repos
5. **Shared Templates**: `DIAGRAM_TEMPLATES.md` works in every project

## Alternatives Considered

1. **PlantUML:** Powerful, but requires Java and often external server rendering
2. **Draw.io / Images:** Binary files are hard to version control and diff
3. **ASCII Art:** Simple but hard to maintain and inconsistent across devices

## Consequences

### Positive
- **Consistency:** Uniform look and feel across all documentation
- **Version Control:** Diagrams are text, allowing for meaningful diffs in PRs
- **Integration:** Natively supported by GitHub, GitLab, and VS Code
- **Maintainability:** Easier to update text than to redraw lines

### Negative
- **Learning Curve:** Developers must learn Mermaid syntax (though it is simple)
- **Rendering:** Requires a compatible markdown viewer

## Related
- ADR-0003: Mandatory Feature READMEs
- `PROJECT_TEMPLATE/docs/development/DIAGRAM_TEMPLATES.md`
