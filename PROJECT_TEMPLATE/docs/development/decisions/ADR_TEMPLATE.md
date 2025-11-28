# Architecture Decision Record Template

Use this template when making significant architectural or design decisions.

## When to Create an ADR

Create an ADR when:
- Choosing between multiple technology options
- Establishing a new pattern or convention
- Making decisions that are hard to reverse
- Introducing new dependencies
- Changing existing architecture
- Deciding NOT to do something (non-decisions are valuable too)

## Template

Copy the template below into a new file: `ADR-NNNN-short-title.md`

---

```markdown
# ADR-NNNN: [Short Descriptive Title]

## Status
[Proposed | Accepted | Deprecated | Superseded by ADR-XXXX]

## Date
YYYY-MM-DD

## Context

What is the issue we're facing? What problem are we trying to solve?
What constraints or requirements influence this decision?

Be specific about:
- The technical challenge
- Business requirements driving the need
- Current limitations or pain points

## Decision

What is the change we're making? Be specific and actionable.

Describe:
- What we will do
- How it will be implemented
- What technologies/patterns/approaches we're adopting

## Alternatives Considered

### 1. [Alternative Name]
- **Description:** Brief explanation
- **Pros:** Benefits of this approach
- **Cons:** Drawbacks or risks

### 2. [Alternative Name]
- **Description:** Brief explanation
- **Pros:** Benefits of this approach
- **Cons:** Drawbacks or risks

### 3. Do Nothing
- **Description:** Keep current approach
- **Pros:** No effort required, no risk of change
- **Cons:** [Why this isn't acceptable]

## Consequences

### Positive
- Good outcomes from this decision
- Benefits gained

### Negative
- Tradeoffs we're accepting
- New constraints this creates
- Risks introduced

### Neutral
- Side effects that aren't clearly good or bad
- Changes to workflow or process

## Related

- ADR-XXXX: [Related decision]
- [Link to relevant documentation]
- Issue #XXX: [Related issue]

## Notes

Any additional context, implementation notes, or follow-up items.
```

---

## File Naming Convention

- Use sequential numbers: `ADR-0001`, `ADR-0002`, etc.
- Use lowercase with hyphens for the title portion
- Keep titles short but descriptive

**Examples:**
- `ADR-0001-development-philosophy.md`
- `ADR-0002-database-choice.md`
- `ADR-0003-api-versioning-strategy.md`

## Status Lifecycle

```
Proposed → Accepted
              ↓
         [In Use]
              ↓
    Deprecated or Superseded
```

- **Proposed:** Under discussion, not yet agreed
- **Accepted:** Decision made and being implemented
- **Deprecated:** No longer applies (context changed)
- **Superseded:** Replaced by a newer ADR (link to it)

## Tips

1. **Keep it brief** — ADRs should be quick to write and read
2. **Focus on "why"** — The reasoning matters more than the decision
3. **Record context** — Future readers need to understand the situation
4. **Include alternatives** — Shows due diligence
5. **Never delete** — Mark as deprecated/superseded instead
6. **Link related ADRs** — Build a decision trail
