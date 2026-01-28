---
name: review-docs
description: Review repository documentation for quality, completeness, and consistency. Use when asked to review docs, check README files, audit documentation, or ensure docs follow progressive disclosure. Creates bug beads for errors/inconsistencies and task beads for missing content.
allowed_tools:
  - Bash(bd create *)
---

# Documentation Review

Review documentation in the specified path (default: entire repository).

## Arguments

- `[path]` - Optional path to review (default: repo root, reviews all docs)
- `--dry-run` - List issues without creating beads

## Workflow

1. Find all README and documentation files in scope
2. Evaluate against quality criteria
3. Check for existing beads: `bd list --status=open`
4. For each issue found, skip if a bead already exists with matching file/issue
5. Create beads only for new issues

### Deduplication

Before creating a bead, check if one already exists:
- Run `bd list --status=open` to see all open issues
- Compare your findings against existing bead titles and descriptions
- Skip creating beads for issues that already have matching open beads
- When in doubt, show the user the potential duplicate rather than creating

## Quality Criteria

### Structure (Progressive Disclosure)

**Root README.md**:
- Project purpose (why it exists)
- What it does (brief overview)
- Quick start instructions
- Links to component docs
- NO deep architectural details

**Component READMEs**:
- Component's purpose in detail
- Architectural decisions
- Component-specific setup
- Internal APIs/interfaces

### Content Quality

- **Concise**: No unnecessary words or redundancy
- **Clear**: Jargon explained, unambiguous
- **Accurate**: Examples work, paths exist, commands valid
- **Complete**: Prerequisites listed, all steps included
- **Consistent**: Uniform terminology and formatting

## Checklist

- [ ] Root README has: purpose, overview, quick start
- [ ] Root README links to component docs
- [ ] Major directories have READMEs if non-trivial
- [ ] No outdated references (paths, commands)
- [ ] Code examples syntactically correct
- [ ] Referenced files/commands exist
- [ ] Consistent terminology
- [ ] No duplicate information
- [ ] Progressive disclosure maintained

## Output

For each issue: note file, severity, brief explanation.

**Normal mode**:

- Errors/inconsistencies → bug beads:
  ```bash
  bd create --type=bug --priority=<1-3> --title="Docs: <issue>" --description="<file and explanation>"
  ```

- Missing content → task beads:
  ```bash
  bd create --type=task --priority=<2-4> --title="Docs: <what to add>" --description="<what's needed and why>"
  ```

**Dry-run mode**: List issues in a table format without creating beads:
| Type | Severity | File | Issue | Would Create |
|------|----------|------|-------|--------------|
| bug | major | README.md | Description | `bd create --type=bug ...` |
| task | P3 | docs/ | Missing X | `bd create --type=task ...` |
