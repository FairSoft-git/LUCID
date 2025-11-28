# ADR-0004: Spellcheck Linter Implementation

## Status
**Accepted**

## Date
2025-11-27

## Context

Documentation and code quality are critical for maintainability. Spelling errors in:
- Docstrings
- Comments
- Variable/function names
- Markdown documentation

...reduce readability, confuse developers, and create a less professional codebase. Manual spell-checking is error-prone and time-consuming.

All LUCID projects need an automated way to identify spelling errors while respecting:
- Technical vocabulary (Python keywords, library names)
- Domain-specific terms (project-specific terminology)
- Project-specific abbreviations and conventions

## Decision

All LUCID projects include a custom Python-based spellcheck linter (`scripts/spellcheck.py`) that:

1. **Uses `pyspellchecker`** - A pure Python spell-checking library
2. **Loads external dictionary files** in order:
   - `data/dictionaries/generic_dictionary.txt` - Common programming terms (shared across all projects)
   - `data/dictionaries/project_dictionary.txt` - Project-specific vocabulary
3. **Intelligently parses Python files** - Uses `ast` for docstrings and identifiers
4. **Handles naming conventions** - Splits camelCase and snake_case into individual words
5. **Outputs actionable results** - Generates `spelling_errors.txt`

### Dictionary Architecture

```
data/dictionaries/
├── generic_dictionary.txt       # Reusable across ALL LUCID projects
├── project_dictionary.txt       # Project-specific terms
└── PROJECT_DICTIONARY_TEMPLATE.txt  # Template for new projects
```

### How This Enforces LUCID

| Principle | Enforcement |
|-----------|-------------|
| **L - Lean** | Single script, no external binaries, pure Python |
| **C - Contracted** | Docstrings are checked—encourages quality documentation |
| **D - Driven** | Dictionary is data-driven (text files, not hardcoded) |
| **D - Driven** | Automated checking, not manual review |

## Benefits for All Projects

1. **Shared Generic Dictionary**: `generic_dictionary.txt` contains common programming terms usable by any project
2. **Template Included**: `PROJECT_TEMPLATE` includes the spellcheck script and dictionary structure
3. **CI-Ready**: Can be integrated into pre-commit hooks or GitHub Actions
4. **No Code Changes for Vocabulary**: Add words to text files, not Python code
5. **Interactive Fix Mode**: `--fix` flag for efficient error correction

### File Types Checked
- `.py` - Python source files (docstrings, comments, identifiers)
- `.md` - Markdown documentation
- `.txt` - Plain text files

### Directories Ignored
- `.git`, `__pycache__`, `.venv`, `venv`, `env`
- `node_modules`, `data`, `logs`, `output`, `build`, `dist`

## Usage

```powershell
# Report mode (default) - find errors and write to file
python scripts/spellcheck.py

# Interactive fix mode - fix errors one by one
python scripts/spellcheck.py --fix
```

### Interactive Fix Mode Actions
| Key | Action |
|-----|--------|
| `1-5` | Apply the numbered suggestion |
| `m` | Enter a manual correction |
| `g` | Add word to **generic** dictionary (common programming term) |
| `p` | Add word to **project** dictionary (project-specific term) |
| `s` | Skip this error |
| `q` | Quit interactive mode |

## Alternatives Considered

| Alternative | Why Not Chosen |
|-------------|----------------|
| VS Code spell-check extension | Per-developer, not automated, not CI-compatible |
| `codespell` | Less flexible dictionary management |
| `aspell`/`hunspell` | External binary dependency, complex setup |
| Hardcoded dictionary | Less maintainable, requires code edits |
| No spell-checking | Allows quality degradation over time |

## Consequences

### Positive
- **Consistent quality**: Automated detection of spelling errors
- **Low friction**: Single command to check entire project
- **Extensible dictionary**: Easy to add new domain terms via text files
- **Reusable**: Generic dictionary shared across all LUCID projects
- **CI-ready**: Integrates with pre-commit hooks

### Negative
- **Two files to maintain**: Generic and project dictionaries
- **False positives possible**: New technical terms may be flagged until added

## Related
- ADR-0001: Adopt LUCID Development Philosophy
- `PROJECT_TEMPLATE/scripts/spellcheck.py` — Implementation
- `PROJECT_TEMPLATE/data/dictionaries/` — Dictionary files
