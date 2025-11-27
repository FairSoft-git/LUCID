# The LUCID Development Philosophy - Quick Reference

> **"A design guide for the sane."**

---

## 🧠 The LUCID Acronym

| | Principle | Rule |
|:-:|-----------|------|
| **L** | **Lean** | KISS, DRY, Max 3 Indents |
| **U** | **User-First** | UI drives Architecture |
| **C** | **Contracted** | Pre/Post Conditions |
| **I** | **Immutable** | Functional Internals |
| **D** | **Driven** | **Tests First**, Data-Driven |

---

## ⚠️ THE GOLDEN RULE (Driven)

```
┌─────────────────────────────────────────────┐
│  NO implementation code exists without a    │
│  FAILING TEST first.                        │
│                                             │
│  1. Write test (RED - it fails)             │
│  2. Write code (GREEN - it passes)          │
│  3. Refactor (keep it GREEN)                │
└─────────────────────────────────────────────┘
```

---

## 📝 Function Template

```python
def function_name(param: Type) -> ReturnType:
    """
    Brief description.
    
    Preconditions:
        - param is not None
        - param meets requirements
    
    Postconditions:
        - Returns valid result
        - No side effects
    """
    # Guard clauses first
    if not param:
        raise ValueError("Precondition failed")
    
    # Main logic (max 3 indent levels)
    result = process(param)
    
    return result
```

---

## 📦 Class Template

```python
class ClassName:
    """
    Brief description.
    
    Responsibilities:
        - What this class does
        - What it manages
    
    Collaborators:
        - OtherClass: how they interact
    
    Invariants:
        - What's always true
    """
```

---

## 🧪 Test Structure (AAA) — Write This FIRST!

```python
def test_function_does_expected_behavior():
    # Arrange
    input_data = create_test_data()
    
    # Act
    result = function_under_test(input_data)
    
    # Assert
    assert result == expected_value
```

---

## 📁 Where Things Go

| Type | Location |
|------|----------|
| Features | `features/<module>/` |
| Tests | `tests/test_<module>.py` |
| Scripts | `scripts/` |
| Config | `data/` or env vars |
| Decisions | `docs/development/decisions/ADR-NNNN-*.md` |
| Investigations | `docs/development/investigations/INV-NNNN-*.md` |
| Helpers | `docs/development/helpers/` |

---

## 🔀 Git Commit Format

```
<type>(<scope>): <subject>
```

| Type | When |
|------|------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation |
| `refactor` | Code restructure |
| `test` | Add/fix tests |
| `chore` | Maintenance |
| `wip` | Work in progress (skips CI tests) |

**WIP:** `[WIP]` in message skips test pipeline

---

## ✅ Before Commit Checklist

- [ ] Tests written FIRST
- [ ] Tests pass locally
- [ ] Coverage ≥ 99%
- [ ] No lint errors
- [ ] Docstrings complete
- [ ] No hardcoded values
- [ ] Max 3 indent levels
- [ ] ADR created if architectural decision

---

## 🚫 Don't

- ❌ Nest more than 3 levels deep
- ❌ Use magic numbers/strings
- ❌ Skip function documentation
- ❌ Commit without running tests
- ❌ Hardcode configuration values
- ❌ Delete ADRs (mark deprecated instead)

---

## ✅ Do

- ✓ Write tests first
- ✓ Use guard clauses
- ✓ Document pre/postconditions
- ✓ Extract helper functions
- ✓ Use descriptive names
- ✓ Push at end of session

---

*Full details: `DEVELOPMENT_PHILOSOPHY.md`*
