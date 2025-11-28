"""
Spellcheck linter for LUCID projects.

Scans Python files (docstrings, comments, identifiers) and text files (.md, .txt)
for spelling errors using pyspellchecker with external dictionary files.

Usage:
    python scripts/spellcheck.py           # Report only (default)
    python scripts/spellcheck.py --fix     # Interactive fix mode

Dictionaries:
    - data/dictionaries/generic_dictionary.txt  - Common programming terms
    - data/dictionaries/project_dictionary.txt  - Project-specific vocabulary

Output:
    spelling_errors.txt - List of potential spelling errors with file:line format
"""

import re
import ast
import sys
import tokenize
import argparse
from spellchecker import SpellChecker
from pathlib import Path

# Configuration
IGNORE_DIRS = {
    ".git",
    "__pycache__",
    ".venv",
    "venv",
    "env",
    "node_modules",
    "data",
    "logs",
    "output",
    "build",
    "dist",
}
IGNORE_FILES = {"spelling_errors.txt"}  # Self-generated output
IGNORE_EXTENSIONS = {
    ".json",
    ".csv",
    ".pyc",
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".ico",
    ".svg",
    ".pdf",
    ".zip",
    ".tar",
    ".gz",
}
CHECK_EXTENSIONS = {".py", ".md", ".txt"}

# Dictionary file paths (relative to project root)
GENERIC_DICT_PATH = Path("data/dictionaries/generic_dictionary.txt")
PROJECT_DICT_PATH = Path("data/dictionaries/project_dictionary.txt")


def load_dictionary(file_path: Path) -> set[str]:
    """
    Load words from a dictionary file.

    Args:
        file_path: Path to the dictionary file

    Returns:
        Set of lowercase words from the dictionary

    Preconditions:
        - file_path should point to a text file with one word per line
        - Lines starting with # are treated as comments

    Postconditions:
        - Returns empty set if file doesn't exist
        - All words are lowercased
    """
    words = set()
    if not file_path.exists():
        print(f"Warning: Dictionary not found: {file_path}")
        return words

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            # Skip empty lines and comments
            if line and not line.startswith("#"):
                words.add(line.lower())

    return words


def add_to_dictionary(word: str, dictionary_path: Path) -> bool:
    """
    Add a word to a dictionary file.

    Args:
        word: Word to add (will be lowercased)
        dictionary_path: Path to the dictionary file

    Returns:
        True if successful, False otherwise
    """
    try:
        with open(dictionary_path, "a", encoding="utf-8") as f:
            f.write(f"\n{word.lower()}")
        return True
    except Exception as e:
        print(f"Error adding to dictionary: {e}")
        return False


def initialize_spellchecker() -> tuple[SpellChecker, set[str]]:
    """
    Initialize the spellchecker with generic and project dictionaries.

    Returns:
        Tuple of (SpellChecker instance, combined custom words set)

    Postconditions:
        - Generic dictionary is loaded first
        - Project dictionary is loaded second (can override/extend)
        - All custom words are added to the spellchecker
    """
    spell = SpellChecker()

    # Load dictionaries in order: generic first, then project-specific
    generic_words = load_dictionary(GENERIC_DICT_PATH)
    project_words = load_dictionary(PROJECT_DICT_PATH)

    # Combine dictionaries (project words extend generic)
    all_custom_words = generic_words | project_words

    # Add all custom words to the spellchecker
    spell.word_frequency.load_words(all_custom_words)

    print(
        f"Loaded {len(generic_words)} generic words, {len(project_words)} project words"
    )

    return spell, all_custom_words


# Initialize spellchecker with external dictionaries
spell, CUSTOM_WORDS = initialize_spellchecker()


def split_camel_case(text: str) -> list[str]:
    """Split camelCase text into individual words."""
    return re.sub("([a-z0-9])([A-Z])", r"\1 \2", text).split()


def split_snake_case(text: str) -> list[str]:
    """Split snake_case or kebab-case text into individual words."""
    return text.replace("_", " ").replace("-", " ").split()


def extract_words(text: str) -> list[str]:
    """
    Extract individual words from text, handling various naming conventions.

    Args:
        text: Input text to extract words from

    Returns:
        List of words longer than 2 characters
    """
    # Remove non-alphabetic characters but keep spaces
    # Allow accented characters for Pokémon
    clean_text = re.sub(r"[^a-zA-Z\u00C0-\u00FF\s]", " ", text)
    words = []
    for token in clean_text.split():
        # Handle camelCase and snake_case
        if "_" in token or "-" in token:
            words.extend(split_snake_case(token))
        elif any(c.isupper() for c in token) and any(c.islower() for c in token):
            words.extend(split_camel_case(token))
        else:
            words.append(token)
    return [w for w in words if len(w) > 2]  # Ignore short words


class SpellingError:
    """Represents a spelling error with context for fixing."""

    def __init__(
        self,
        word: str,
        file_path: Path,
        line_num: int,
        context: str,
        line_content: str = "",
    ):
        self.word = word
        self.file_path = file_path
        self.line_num = line_num
        self.context = context
        self.line_content = line_content
        self.suggestions = list(spell.candidates(word) or [])[:5]

    def __str__(self) -> str:
        return f"{self.file_path}:{self.line_num} - '{self.word}' (Context: {self.context})"


def check_text_detailed(
    text: str, file_path: Path, line_num: int, context: str = "", line_content: str = ""
) -> list[SpellingError]:
    """
    Check text for spelling errors with detailed information.

    Args:
        text: Text to check
        file_path: Source file path
        line_num: Line number
        context: Description of where the text came from
        line_content: The full line content for display

    Returns:
        List of SpellingError objects
    """
    words = extract_words(text)
    unknown = spell.unknown(words)
    errors = []

    for word in unknown:
        # Double check if it's really unknown (case insensitive)
        if word.lower() in CUSTOM_WORDS or word.lower() in spell:
            continue
        # Ignore if it looks like a hex code or random string
        if re.match(r"^[a-f0-9]+$", word.lower()):
            continue

        errors.append(SpellingError(word, file_path, line_num, context, line_content))

    return errors


def process_python_file_detailed(file_path: Path) -> list[SpellingError]:
    """
    Process a Python file for spelling errors with detailed information.

    Args:
        file_path: Path to the Python file

    Returns:
        List of SpellingError objects
    """
    errors = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            lines = content.splitlines()

        def get_line(n: int) -> str:
            """Get line content safely."""
            if 0 < n <= len(lines):
                return lines[n - 1]
            return ""

        # Check file name
        errors.extend(check_text_detailed(file_path.stem, file_path, 0, "Filename"))

        # Parse AST for docstrings and identifiers
        try:
            tree = ast.parse(content)
            for node in ast.walk(tree):
                # Check docstrings
                if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Module)):
                    docstring = ast.get_docstring(node)
                    if docstring:
                        lineno = getattr(node, "lineno", 1)
                        errors.extend(
                            check_text_detailed(
                                docstring,
                                file_path,
                                lineno,
                                "Docstring",
                                get_line(lineno),
                            )
                        )

                # Check function/class names
                if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                    errors.extend(
                        check_text_detailed(
                            node.name,
                            file_path,
                            node.lineno,
                            "Definition Name",
                            get_line(node.lineno),
                        )
                    )

                # Check variable assignments (targets)
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            errors.extend(
                                check_text_detailed(
                                    target.id,
                                    file_path,
                                    node.lineno,
                                    "Variable Name",
                                    get_line(node.lineno),
                                )
                            )
        except SyntaxError:
            pass  # Ignore syntax errors in parsing

        # Check comments using tokenize
        with open(file_path, "rb") as f:
            try:
                tokens = tokenize.tokenize(f.readline)
                for token in tokens:
                    if token.type == tokenize.COMMENT:
                        errors.extend(
                            check_text_detailed(
                                token.string,
                                file_path,
                                token.start[0],
                                "Comment",
                                get_line(token.start[0]),
                            )
                        )
            except tokenize.TokenizeError:
                pass  # Ignore tokenize errors

    except Exception as e:
        print(f"Error processing {file_path}: {e}")

    return errors


def process_text_file_detailed(file_path: Path) -> list[SpellingError]:
    """
    Process a text file (.md, .txt) for spelling errors with detailed information.

    Args:
        file_path: Path to the text file

    Returns:
        List of SpellingError objects
    """
    errors = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # Check file name
        errors.extend(check_text_detailed(file_path.stem, file_path, 0, "Filename"))

        in_code_block = False
        for i, line in enumerate(lines):
            original_line = line
            # Track code blocks in markdown
            if file_path.suffix == ".md":
                if line.strip().startswith("```"):
                    in_code_block = not in_code_block
                    continue
                if in_code_block:
                    continue
                # Skip inline code
                if "`" in line:
                    # Remove inline code segments before checking
                    line = re.sub(r"`[^`]+`", "", line)

            errors.extend(
                check_text_detailed(
                    line, file_path, i + 1, "Text Content", original_line.rstrip()
                )
            )

    except Exception as e:
        print(f"Error processing {file_path}: {e}")

    return errors


def fix_in_file(file_path: Path, old_word: str, new_word: str, line_num: int) -> bool:
    """
    Replace a word in a file at a specific line.

    Args:
        file_path: Path to the file
        old_word: Word to replace
        new_word: Replacement word
        line_num: Line number (1-indexed, 0 means filename - skip)

    Returns:
        True if successful, False otherwise
    """
    if line_num == 0:
        print("  Cannot fix filenames automatically. Please rename manually.")
        return False

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        if 0 < line_num <= len(lines):
            # Case-insensitive replacement, preserving case of first letter
            pattern = re.compile(re.escape(old_word), re.IGNORECASE)
            lines[line_num - 1] = pattern.sub(new_word, lines[line_num - 1], count=1)

            with open(file_path, "w", encoding="utf-8") as f:
                f.writelines(lines)
            return True
        else:
            print(f"  Line {line_num} out of range for {file_path}")
            return False

    except Exception as e:
        print(f"  Error fixing: {e}")
        return False


def interactive_fix(errors: list[SpellingError]) -> dict:
    """
    Interactively prompt user to fix each spelling error.

    Args:
        errors: List of SpellingError objects

    Returns:
        Statistics dictionary with counts of actions taken
    """
    stats = {"fixed": 0, "skipped": 0, "added_to_dict": 0, "quit": False}

    print("\n" + "=" * 60)
    print("INTERACTIVE FIX MODE")
    print("=" * 60)
    print("\nFor each error, choose an action:")
    print("  [1-5] Apply suggested fix")
    print("  [m]   Enter manual correction")
    print("  [g]   Add to generic dictionary (common programming term)")
    print("  [p]   Add to project dictionary (project-specific term)")
    print("  [s]   Skip this error")
    print("  [q]   Quit interactive mode")
    print("=" * 60 + "\n")

    for i, error in enumerate(errors):
        if stats["quit"]:
            break

        print(f"\n[{i+1}/{len(errors)}] {error.file_path}:{error.line_num}")
        print(f"  Context: {error.context}")
        if error.line_content:
            # Highlight the misspelled word
            highlighted = error.line_content.replace(
                error.word, f"\033[91m{error.word}\033[0m"
            )
            print(f"  Line: {highlighted}")
        print(f"\n  Misspelled: '\033[93m{error.word}\033[0m'")

        if error.suggestions:
            print(f"  Suggestions:")
            for j, suggestion in enumerate(error.suggestions, 1):
                print(f"    [{j}] {suggestion}")
        else:
            print("  No suggestions available")

        while True:
            choice = input("\n  Action [1-5/m/g/p/s/q]: ").strip().lower()

            if choice == "q":
                stats["quit"] = True
                print("\n  Quitting interactive mode...")
                break

            elif choice == "s":
                stats["skipped"] += 1
                print("  Skipped.")
                break

            elif choice == "g":
                if add_to_dictionary(error.word, GENERIC_DICT_PATH):
                    CUSTOM_WORDS.add(error.word.lower())
                    stats["added_to_dict"] += 1
                    print(f"  Added '{error.word}' to generic dictionary.")
                break

            elif choice == "p":
                if add_to_dictionary(error.word, PROJECT_DICT_PATH):
                    CUSTOM_WORDS.add(error.word.lower())
                    stats["added_to_dict"] += 1
                    print(f"  Added '{error.word}' to project dictionary.")
                break

            elif choice == "m":
                new_word = input("  Enter correction: ").strip()
                if new_word:
                    if fix_in_file(
                        error.file_path, error.word, new_word, error.line_num
                    ):
                        stats["fixed"] += 1
                        print(f"  Fixed: '{error.word}' -> '{new_word}'")
                    break
                else:
                    print("  No correction entered.")

            elif choice.isdigit() and 1 <= int(choice) <= len(error.suggestions):
                idx = int(choice) - 1
                new_word = error.suggestions[idx]
                if fix_in_file(error.file_path, error.word, new_word, error.line_num):
                    stats["fixed"] += 1
                    print(f"  Fixed: '{error.word}' -> '{new_word}'")
                break

            else:
                print("  Invalid choice. Please try again.")

    return stats


def collect_all_errors() -> list[SpellingError]:
    """Collect all spelling errors from the project."""
    root_dir = Path(".")
    all_errors = []

    for file_path in root_dir.rglob("*"):
        # Skip ignored directories
        if any(part in IGNORE_DIRS for part in file_path.parts):
            continue

        # Skip ignored files
        if file_path.name in IGNORE_FILES:
            continue

        if file_path.is_file() and file_path.suffix in CHECK_EXTENSIONS:
            print(f"Checking {file_path}...")
            if file_path.suffix == ".py":
                all_errors.extend(process_python_file_detailed(file_path))
            else:
                all_errors.extend(process_text_file_detailed(file_path))

    return all_errors


def main():
    """Main entry point for the spellcheck linter."""
    parser = argparse.ArgumentParser(
        description="Spellcheck linter with optional interactive fix mode."
    )
    parser.add_argument(
        "--fix", action="store_true", help="Run in interactive fix mode"
    )
    args = parser.parse_args()

    print("Starting spell check...")
    print(f"Checking extensions: {CHECK_EXTENSIONS}")
    print(f"Ignoring directories: {IGNORE_DIRS}")
    print()

    all_errors = collect_all_errors()

    if not all_errors:
        print("\nSpell check complete. No spelling errors found!")
        return

    print(f"\nFound {len(all_errors)} potential errors.")

    if args.fix:
        # Interactive fix mode
        stats = interactive_fix(all_errors)
        print("\n" + "=" * 60)
        print("SUMMARY")
        print("=" * 60)
        print(f"  Fixed:            {stats['fixed']}")
        print(f"  Added to dict:    {stats['added_to_dict']}")
        print(f"  Skipped:          {stats['skipped']}")
        remaining = (
            len(all_errors) - stats["fixed"] - stats["added_to_dict"] - stats["skipped"]
        )
        if remaining > 0:
            print(f"  Remaining:        {remaining}")
    else:
        # Report mode - write errors to file
        with open("spelling_errors.txt", "w", encoding="utf-8") as f:
            for error in all_errors:
                f.write(str(error) + "\n")

        print("See spelling_errors.txt for details.")
        print("\nRun with --fix for interactive correction mode.")


if __name__ == "__main__":
    main()
