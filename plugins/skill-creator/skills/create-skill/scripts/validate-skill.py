#!/usr/bin/env python3
"""
Validate a skill directory for structure, metadata, and content quality.

Usage:
    validate-skill.py <skill-directory>
    validate-skill.py <skill-directory> --json

Checks:
    - SKILL.md existence
    - YAML frontmatter format and required fields
    - Name rules (lowercase/hyphens/digits, max 64, no bad hyphens)
    - Description quality (third-person, trigger phrases, length)
    - Body line count (<500 warning)
    - Reference file reachability from SKILL.md
    - Extraneous file warnings
    - Path style (no backslashes)

Zero external dependencies — uses only Python 3 stdlib.
"""

import json
import os
import re
import sys
from pathlib import Path


def parse_frontmatter(content):
    """Parse YAML frontmatter from SKILL.md content.

    Handles simple key: value pairs (strings only). Does not support
    nested YAML, lists, or multi-line values beyond simple scalars.
    Returns (dict, body_text) or raises ValueError.
    """
    if not content.startswith("---"):
        raise ValueError("No YAML frontmatter found (file must start with ---)")

    parts = content.split("---", 2)
    if len(parts) < 3:
        raise ValueError("Invalid frontmatter format (missing closing ---)")

    frontmatter_text = parts[1].strip()
    body = parts[2]

    result = {}
    for line in frontmatter_text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()
        # Remove surrounding quotes if present
        if len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'"):
            value = value[1:-1]
        result[key] = value

    return result, body


def validate_skill(skill_path):
    """Validate a skill directory. Returns (errors, warnings) lists."""
    skill_path = Path(skill_path).resolve()
    errors = []
    warnings = []

    # Check SKILL.md exists
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        errors.append("SKILL.md not found")
        return errors, warnings

    content = skill_md.read_text(encoding="utf-8")

    # Parse frontmatter
    try:
        frontmatter, body = parse_frontmatter(content)
    except ValueError as e:
        errors.append(str(e))
        return errors, warnings

    # Check required fields
    if "name" not in frontmatter:
        errors.append("Missing 'name' in frontmatter")
    if "description" not in frontmatter:
        errors.append("Missing 'description' in frontmatter")

    # Validate name
    name = frontmatter.get("name", "")
    if name:
        if not re.match(r"^[a-z0-9-]+$", name):
            errors.append(
                f"Name '{name}' must be lowercase letters, digits, and hyphens only"
            )
        elif name.startswith("-") or name.endswith("-") or "--" in name:
            errors.append(
                f"Name '{name}' cannot start/end with hyphen or contain consecutive hyphens"
            )

        if len(name) > 64:
            errors.append(f"Name is too long ({len(name)} chars, max 64)")

        # Check name matches directory
        if name != skill_path.name:
            warnings.append(
                f"Name '{name}' does not match directory name '{skill_path.name}'"
            )

    # Validate description
    description = frontmatter.get("description", "")
    if description:
        if "<" in description or ">" in description:
            errors.append("Description cannot contain angle brackets (< or >)")

        if len(description) > 1024:
            errors.append(
                f"Description is too long ({len(description)} chars, max 1024)"
            )

        if len(description) < 80:
            warnings.append(
                f"Description is short ({len(description)} chars). "
                "Consider adding trigger phrases for better skill activation."
            )

        # Check third-person voice heuristics
        desc_lower = description.lower()
        first_person_starts = ("i ", "i'm ", "i'll ", "we ", "we're ")
        imperative_patterns = (
            "create ", "guide ", "help ", "make ", "build ", "generate ",
            "run ", "use ", "check ", "validate ",
        )
        if desc_lower.startswith(first_person_starts):
            warnings.append(
                "Description appears to use first-person voice. "
                "Use third-person instead (e.g., 'Guides...' not 'I guide...')"
            )
        elif any(desc_lower.startswith(p) for p in imperative_patterns):
            # Check if it's actually imperative (no -s/-es ending on first word)
            first_word = description.split()[0] if description.split() else ""
            if first_word and not (first_word.endswith("s") or first_word.endswith("es")):
                warnings.append(
                    "Description may use imperative voice. "
                    "Use third-person instead (e.g., 'Creates...' not 'Create...')"
                )

        # Check for trigger phrases
        trigger_indicators = ("use when", "use for", "use to", "used when", "used for")
        if not any(ind in desc_lower for ind in trigger_indicators):
            warnings.append(
                "Description lacks trigger phrases. "
                "Consider adding 'Use when...' to improve skill activation."
            )

    # Check body line count
    body_lines = body.strip().splitlines()
    if len(body_lines) > 500:
        warnings.append(
            f"SKILL.md body is {len(body_lines)} lines (recommended max 500). "
            "Consider splitting content into reference files."
        )

    # Check for backslash paths in content
    backslash_paths = re.findall(r"[a-zA-Z0-9_]+\\[a-zA-Z0-9_]+", content)
    if backslash_paths:
        warnings.append(
            f"Possible Windows-style paths found: {', '.join(backslash_paths[:3])}. "
            "Use forward slashes."
        )

    # Check reference file reachability
    # Find all markdown links in SKILL.md
    linked_files = set()
    link_pattern = re.compile(r"\[.*?\]\(((?!http)[^)#]+)\)")
    for match in link_pattern.finditer(content):
        linked_files.add(match.group(1))

    # Check that linked files exist
    for linked in linked_files:
        linked_path = skill_path / linked
        if not linked_path.exists():
            errors.append(f"Linked file not found: {linked}")

    # Check for reference files not linked from SKILL.md
    refs_dir = skill_path / "references"
    if refs_dir.is_dir():
        for ref_file in refs_dir.iterdir():
            if ref_file.is_file() and ref_file.suffix == ".md":
                rel_path = f"references/{ref_file.name}"
                if rel_path not in linked_files:
                    warnings.append(
                        f"Reference file '{rel_path}' is not linked from SKILL.md"
                    )

    # Check for extraneous files
    extraneous_names = {
        "README.md", "CHANGELOG.md", "CONTRIBUTING.md",
        "INSTALLATION_GUIDE.md", "QUICK_REFERENCE.md",
    }
    for item in skill_path.iterdir():
        if item.name in extraneous_names:
            warnings.append(
                f"Extraneous file '{item.name}' — skills should not include "
                "auxiliary documentation"
            )

    # Check allowed frontmatter keys
    allowed_keys = {"name", "description", "license", "allowed-tools", "metadata",
                    "disable-model-invocation"}
    unexpected = set(frontmatter.keys()) - allowed_keys
    if unexpected:
        warnings.append(
            f"Unexpected frontmatter key(s): {', '.join(sorted(unexpected))}. "
            f"Allowed: {', '.join(sorted(allowed_keys))}"
        )

    return errors, warnings


def main():
    if len(sys.argv) < 2:
        print("Usage: validate-skill.py <skill-directory> [--json]")
        sys.exit(1)

    skill_dir = sys.argv[1]
    json_output = "--json" in sys.argv

    if not os.path.isdir(skill_dir):
        if json_output:
            print(json.dumps({"valid": False, "errors": [f"Not a directory: {skill_dir}"], "warnings": []}))
        else:
            print(f"Error: Not a directory: {skill_dir}")
        sys.exit(1)

    errors, warnings = validate_skill(skill_dir)
    valid = len(errors) == 0

    if json_output:
        print(json.dumps({
            "valid": valid,
            "errors": errors,
            "warnings": warnings,
        }, indent=2))
    else:
        if errors:
            for e in errors:
                print(f"ERROR: {e}")
        if warnings:
            for w in warnings:
                print(f"WARNING: {w}")
        if valid and not warnings:
            print("Skill is valid!")
        elif valid:
            print(f"\nValid with {len(warnings)} warning(s).")
        else:
            print(f"\nFailed with {len(errors)} error(s) and {len(warnings)} warning(s).")

    sys.exit(0 if valid else 1)


if __name__ == "__main__":
    main()
