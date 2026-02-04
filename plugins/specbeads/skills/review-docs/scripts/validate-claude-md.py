#!/usr/bin/env python3
"""Validate CLAUDE.md files for structural correctness."""

import subprocess
import sys
import re
import json
from pathlib import Path


def find_git_root(path: Path) -> Path | None:
    """Find the git repository root for a given path."""
    try:
        result = subprocess.run(
            ['git', 'rev-parse', '--show-toplevel'],
            cwd=path if path.is_dir() else path.parent,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            return Path(result.stdout.strip())
    except FileNotFoundError:
        pass
    return None


def is_gitignored(file_path: Path, git_root: Path | None) -> bool:
    """Check if a file is ignored by git."""
    if git_root is None:
        return False
    try:
        result = subprocess.run(
            ['git', 'check-ignore', '-q', str(file_path)],
            cwd=git_root,
            capture_output=True
        )
        return result.returncode == 0
    except FileNotFoundError:
        return False


def extract_navigation_table_refs(content: str, directory: Path) -> tuple[list[str], list[str]]:
    """Extract file references from tables, separating nav refs from doc refs.

    Returns (nav_refs, doc_refs) where:
    - nav_refs: References to actual files/dirs that should exist in the directory
    - doc_refs: References in documentation tables describing subdirectory structure
    """
    nav_refs = []
    doc_refs = []
    lines = content.split('\n')
    in_table = False
    is_doc_table = False

    for i, line in enumerate(lines):
        # Detect start of table (separator row with dashes)
        if re.match(r'\|\s*-+\s*\|', line):
            in_table = True
            # Look back for section headers that indicate doc tables
            # Check for patterns like "### Per-Feature", "## File Layout", etc.
            is_doc_table = False
            for j in range(max(0, i - 5), i):
                header_line = lines[j].lower()
                if re.match(r'^#{1,6}\s+.*\b(per-|file layout|structure|template)\b', header_line):
                    is_doc_table = True
                    break
            continue

        # Detect end of table (blank line or non-table line)
        if in_table:
            if not line.strip() or not line.strip().startswith('|'):
                in_table = False
                is_doc_table = False
                continue

        # Extract refs from table rows
        if in_table:
            match = re.search(r'\|\s*`([^`]+)`\s*\|', line)
            if match:
                ref = match.group(1)
                if is_doc_table:
                    doc_refs.append(ref)
                else:
                    nav_refs.append(ref)

    return nav_refs, doc_refs


def is_covered_by_indexed_children(name: str, indexed: set[str]) -> bool:
    """Check if a directory is implicitly covered by indexing its children.

    For example, if indexed contains 'cmd/server/main.go' and 'cmd/api/main.go',
    then 'cmd' is considered covered.
    """
    prefix = f"{name}/"
    return any(ref.startswith(prefix) for ref in indexed)


def validate_claude_md(file_path: Path, git_root: Path | None) -> dict:
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

    # Check table headers - accept common variations
    header_checks = [
        # Accept: File, Directory, File/Directory, File / Directory, Path, etc.
        (r'\|\s*(File|Directory|Path)(\s*/\s*(File|Directory|Path))?\s*\|', "File/Directory"),
        (r'\|\s*What\s*\|', "What"),
        (r'\|\s*When to (read|use|run)\s*\|', "When to read/use/run"),
    ]
    for pattern, col_name in header_checks:
        if not re.search(pattern, content, re.IGNORECASE):
            issues.append({"type": "missing_column", "severity": "P3", "message": f"Missing '{col_name}' column"})

    # Extract referenced files/directories from tables
    nav_refs, doc_refs = extract_navigation_table_refs(content, directory)
    refs = nav_refs  # For backward compatibility in output

    # Only check existence for navigation refs (not doc refs describing subdirectory structure)
    for ref in nav_refs:
        ref_path = directory / ref.rstrip('/')
        if not ref_path.exists():
            issues.append({
                "type": "missing_reference",
                "severity": "P2",
                "message": f"Referenced path does not exist: {ref}"
            })

    # Check for files in directory not in index (index drift)
    if has_table:
        # Normalize refs for comparison (use nav_refs for drift detection)
        indexed = {r.rstrip('/') for r in nav_refs}

        # Always skip these regardless of gitignore
        always_skip = {'CLAUDE.md'}

        # Lock files: committed to git but never useful for Claude to document
        lock_files = {
            'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml',
            'uv.lock', 'poetry.lock', 'Pipfile.lock',
            'Cargo.lock', 'Gemfile.lock', 'composer.lock',
            'go.sum', 'mix.lock', 'pubspec.lock', 'pom.xml.lock',
        }

        for item in directory.iterdir():
            name = item.name
            if name in always_skip or name in lock_files:
                continue
            # Skip dotfiles (config files, .git, etc.) - rarely documented in CLAUDE.md
            if name.startswith('.'):
                continue
            # Use git to check if file is ignored
            if is_gitignored(item, git_root):
                continue
            # Check direct indexing
            if name in indexed or f"{name}/" in indexed:
                continue
            # Check if covered by indexed children (e.g., cmd/server/main.go covers cmd)
            if is_covered_by_indexed_children(name, indexed):
                continue
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


def is_in_build_directory(file_path: Path) -> bool:
    """Check if a file is inside a build/artifact directory."""
    build_dirs = {'build', 'dist', 'out', 'target', '.next', '__pycache__', 'node_modules'}
    for parent in file_path.parents:
        if parent.name in build_dirs:
            return True
    return False


def main():
    if len(sys.argv) < 2:
        print("Usage: validate-claude-md.py <path> [--json]", file=sys.stderr)
        sys.exit(1)

    path = Path(sys.argv[1])
    json_output = "--json" in sys.argv

    # Find git root once for the entire run
    git_root = find_git_root(path)

    results = []

    if path.is_file() and path.name == "CLAUDE.md":
        results.append(validate_claude_md(path, git_root))
    elif path.is_dir():
        for claude_md in path.rglob("CLAUDE.md"):
            # Skip CLAUDE.md files inside build/artifact directories
            if is_in_build_directory(claude_md):
                continue
            # Skip gitignored CLAUDE.md files
            if is_gitignored(claude_md, git_root):
                continue
            results.append(validate_claude_md(claude_md, git_root))

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
