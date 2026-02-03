---
name: sb:review-tests
description: Review tests for completeness, usefulness, isolation, and readability. Use when asked to review tests, check test quality, audit test coverage, or validate test files.
---

# Tests Review

Review tests in the specified path for quality issues.

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Argument Parsing

Parse `$ARGUMENTS` for:
- **Path**: Required path to review (file or directory containing tests)
- **`--create-beads`**: Create beads for findings (default: report only)

## Workflow

1. Find and read test files in the specified path
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

### Completeness
- Edge cases covered
- Error paths tested
- Boundary conditions checked
- Happy path and failure scenarios both present

### Usefulness
- Tests catch real bugs, not just chase coverage
- Tests would fail if code broke
- Tests validate behavior, not implementation details

### Output Validation
- Assertions check actual results
- Not just "no error thrown"
- Expected values are meaningful, not arbitrary

### Isolation
- No shared mutable state between tests
- Tests can run in any order
- Tests can run in parallel
- External dependencies mocked/stubbed appropriately

### Readability
- Clear, descriptive test names
- Obvious arrange-act-assert structure
- Test intent immediately clear
- Setup/teardown not hiding important context

### Integration Test Specifics
- Proper cleanup of test data
- Appropriate use of test fixtures
- Reasonable timeouts configured
- Clear distinction from unit tests

## Output

For each issue: note file, severity (critical/major/minor), brief explanation.

**Default mode**: List issues in a table format without creating beads:
| Severity | File | Issue | Would Create |
|----------|------|-------|--------------|
| major | tests/user.test.ts | Description | `bd create --type=bug ...` |

**`--create-beads` mode**: Create beads for issues found:
```bash
bd create --type=bug --priority=<1-3> --title="Test: <issue>" --description="<file and explanation>"
```
