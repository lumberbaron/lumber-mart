#!/usr/bin/env python3
"""Validate CLAUDE.md files for structural correctness."""

import sys
import re
import json
from pathlib import Path


def validate_claude_md(file_path: Path) -> dict:
    """Validate a single CLAUDE.md file."""
    issues = []

    if not file_path.exists():
        return {"file": str(file_path), "exists": False, "issues": ["File not found"]}

    content = file_path.read_text()
    directory = file_path.parent

    # Check for tabular index
    table_pattern = r'\|.*\|.*\|.*\|'
    has_table = bool(re.search(table_pattern, content))
    if not has_table:
        issues.append({"type": "missing_table", "severity": "P2", "message": "No markdown table found"})

    # Check table headers
    header_patterns = [
        r'\|\s*(File|Directory)\s*\|',
        r'\|\s*What\s*\|',
        r'\|\s*When to read\s*\|'
    ]
    for pattern in header_patterns:
        if not re.search(pattern, content, re.IGNORECASE):
            col = pattern.split('*')[1].split('\\')[0]
            issues.append({"type": "missing_column", "severity": "P3", "message": f"Missing '{col}' column"})

    # Extract referenced files/directories from table
    # Pattern: | `name` | or | `name/` |
    refs = re.findall(r'\|\s*`([^`]+)`\s*\|', content)

    for ref in refs:
        ref_path = directory / ref.rstrip('/')
        if not ref_path.exists():
            issues.append({
                "type": "missing_reference",
                "severity": "P2",
                "message": f"Referenced path does not exist: {ref}"
            })

    # Check for files in directory not in index (index drift)
    if has_table:
        # Normalize refs for comparison
        indexed = {r.rstrip('/') for r in refs}

        # Files/dirs to ignore
        ignore = {'.git', 'node_modules', '__pycache__', 'dist', 'build',
                  '.DS_Store', '.gitkeep', '*.pyc', '.env'}

        for item in directory.iterdir():
            name = item.name
            if name.startswith('.') or name in ignore:
                continue
            if name == 'CLAUDE.md':
                continue
            if name not in indexed and f"{name}/" not in indexed:
                issues.append({
                    "type": "index_drift",
                    "severity": "P3",
                    "message": f"Not indexed: {name}"
                })

    return {
        "file": str(file_path),
        "exists": True,
        "has_table": has_table,
        "references": refs,
        "issues": issues
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: validate-claude-md.py <path> [--json]", file=sys.stderr)
        sys.exit(1)

    path = Path(sys.argv[1])
    json_output = "--json" in sys.argv

    results = []

    if path.is_file() and path.name == "CLAUDE.md":
        results.append(validate_claude_md(path))
    elif path.is_dir():
        for claude_md in path.rglob("CLAUDE.md"):
            results.append(validate_claude_md(claude_md))

    if json_output:
        print(json.dumps(results, indent=2))
    else:
        for r in results:
            print(f"\n{r['file']}:")
            if not r['exists']:
                print("  NOT FOUND")
                continue
            if not r['issues']:
                print("  OK")
            else:
                for issue in r['issues']:
                    print(f"  [{issue['severity']}] {issue['type']}: {issue['message']}")


if __name__ == "__main__":
    main()
