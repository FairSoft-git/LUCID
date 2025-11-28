# Scripts Directory

⚠️ **LOCAL ONLY - NOT PUSHED TO REPOSITORY**

This directory contains the master CLI and development scripts.

## Master CLI - `cli.py`

The primary way to run project features from the command line:

```powershell
# Show all options
python scripts/cli.py --help

# Spellcheck
python scripts/cli.py -C              # Run spellcheck
python scripts/cli.py -C --fix        # Interactive fix mode

# Git Operations
python scripts/cli.py -G --commit "feat: new feature"  # Mock Push (Commit)
python scripts/cli.py -G --push                        # Push to remote
```

## Development Scripts

Scripts in this folder are for development and testing only:

| Script | Status | Purpose |
|--------|--------|---------|
| `cli.py` | **MVP** | Master CLI for all features |
| `spellcheck.py` | Tool | Spellcheck linter |

## Architecture Rules

1. **Scripts import from `features/`** - All business logic lives in `features/`
2. **Scripts are LOCAL ONLY** - Listed in `.gitignore`, not pushed to repo
3. **MVP features use master CLI** - Once a feature is complete, add it to `cli.py`
4. **Dev scripts for in-progress work** - Keep numbered scripts while developing

## Feature Development Workflow

1. **Create dev script** - Write numbered script (e.g., `10_new_feature.py`) for prototyping
2. **Refactor to features/** - Move business logic to appropriate `features/` subpackage
3. **Add to master CLI** - Add command flag to `cli.py`
4. **Remove dev script** - Or keep for debugging, but document as "Dev"

## Script Structure Template

```python
"""
my_feature.py - Development script for feature X.

This script bypasses the GUI for quick testing.
All business logic imports from features/.
"""
import sys
from pathlib import Path

# Add project root to path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'features'))

from features.my_package import MyClass

if __name__ == '__main__':
    # Quick test code
    obj = MyClass()
    obj.run()
```
