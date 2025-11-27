# Helper Documentation Template

Use this template to document any helper script, tool, or process.

---

```markdown
# Helper: [Name]

## Purpose

Brief description of what this helper does and why it exists.

## Usage

```bash
python scripts/helper_name.py [options] [arguments]
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--input` | Input file path | Required |
| `--output` | Output file path | `./output/` |
| `--verbose` | Enable verbose logging | `False` |

### Examples

```bash
# Basic usage
python scripts/helper_name.py --input data.json

# With all options
python scripts/helper_name.py --input data.json --output results/ --verbose
```

## Inputs

### Required
- `input_file`: Path to the input data file (JSON format)

### Optional
- `config_file`: Custom configuration (default: uses built-in config)

## Outputs

- `output/results.json`: Processed results
- `output/report.txt`: Human-readable summary

## Process Flow

```
Input → Validate → Process → Transform → Output
                      ↓
                   Logging
```

## Dependencies

### Python Packages
- `requests>=2.28.0`
- `pydantic>=2.0`

### External Tools
- None

### Data Files
- `data/config.json`: Configuration settings

## Error Handling

| Error Code | Meaning | Resolution |
|------------|---------|------------|
| 1 | Invalid input | Check input file format |
| 2 | Network error | Check internet connection |
| 3 | Output error | Check write permissions |

## Maintenance

- **Owner:** LF
- **Last Updated:** YYYY-MM-DD
- **Run Frequency:** [On-demand / Daily / Weekly]

## Related

- `docs/development/DEVELOPMENT_GUIDE.md`
- `scripts/README.md`
```

---

## Tips

1. **Keep it practical** — Focus on "how to use" over internal implementation
2. **Include examples** — Real command examples are invaluable
3. **Document errors** — Help users troubleshoot common issues
4. **Update when changing** — Outdated docs are worse than no docs
