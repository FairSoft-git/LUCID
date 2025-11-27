# Development Guide

> **Project:** [Project Name]
> **Status:** Active
> **Owner:** LF

This document contains project-specific information for the codebase.
For general coding standards and principles, see the **LUCID** philosophy documents.

---

## Project Overview

[Brief description of what the project does and its main goals]

---

## Quick Start

### 1. Environment Setup

```bash
# Clone the repo
git clone [repo-url]

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # or .\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 2. Running the Application

```bash
python scripts/main.py
```

### 3. Running Tests

```bash
pytest
```

---

## Architecture

### Directory Structure
- `features/`: Core business logic modules
- `data/`: Data storage (JSON, CSV, SQLite)
- `scripts/`: CLI tools and entry points
- `tests/`: Unit and integration tests

### Key Concepts
- **Concept 1**: Description
- **Concept 2**: Description

---

## Workflow

1. **Create a Branch**: `feat/feature-name` or `fix/bug-name`
2. **Write Tests**: Follow the "Test First" rule.
3. **Implement**: Write code to pass tests.
4. **Lint/Format**: Ensure code quality.
5. **Submit PR**: Request review.
