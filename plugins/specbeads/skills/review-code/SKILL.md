---
name: sb:review-code
description: Review code for quality issues including code smells, concurrency problems, error handling, security vulnerabilities, and maintainability. Use when asked to review code quality, find bugs, audit code, or check for issues.
---

# Code Review

Review code in the specified path for quality issues.

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Argument Parsing

Parse `$ARGUMENTS` for:
- **Path**: Required path to review (file or directory)
- **`--create-beads`**: Create beads for findings (default: report only)

## Workflow

1. Read/explore code in the specified path
2. Evaluate against quality criteria
3. Check for existing beads: `bd list --status=open`
4. For each issue found, skip if a bead already exists with matching file/issue
5. Create beads only for new critical/major issues

### Deduplication

Before creating a bead, check if one already exists:
- Run `bd list --status=open` to see all open issues
- Compare your findings against existing bead titles and descriptions
- Skip creating beads for issues that already have matching open beads
- When in doubt, show the user the potential duplicate rather than creating

## Quality Criteria

### Code Smells
- Long functions doing too many things
- God classes with too many responsibilities
- Duplicated logic to extract
- Deep nesting, complex conditionals
- Magic numbers/strings without constants
- Dead code, unused parameters

### Concurrency Issues
- Race conditions (shared mutable state without sync)
- Potential deadlocks (lock ordering)
- Missing/improper mutex usage
- Thread leaks
- Unsafe concurrent map/slice access

### Error Handling
- Swallowed errors (caught but not handled)
- Missing error checks
- Sensitive info leaked in error messages
- Inconsistent error handling patterns

### Resource Management
- Unclosed files, connections, channels
- Missing defer (Go) / finally (TS) for cleanup
- Memory leaks, holding references too long

### Security
- Input validation gaps
- Injection vulnerabilities (SQL, command, etc.)
- Hardcoded secrets/credentials

### Maintainability
- Unclear naming
- Missing/misleading comments on complex logic
- Tight coupling between modules

## Output

For each issue: note file:line, severity (critical/major/minor), brief explanation.

**Default mode**: List issues in a table format without creating beads:
| Severity | File:Line | Issue | Would Create |
|----------|-----------|-------|--------------|
| critical | path:42 | Description | `bd create --type=bug ...` |

**`--create-beads` mode**: Create beads for critical/major issues:
```bash
bd create --type=bug --priority=<1-3> --title="Code: <issue>" --description="<file:line and explanation>"
```
