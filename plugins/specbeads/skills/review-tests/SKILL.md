---
name: review-tests
description: Review tests for completeness, usefulness, isolation, and readability. Use when asked to review tests, check test quality, audit test coverage, or validate test files.
---

# Tests Review

Review tests in the specified path for quality issues.

> [!IMPORTANT]
> Consult `REFERENCE.md` in this skill directory for the expected output format and level of detail.

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
- Run `bd list --status=closed` to see previously resolved issues
- Compare your findings against existing bead titles and descriptions
- Skip creating beads for issues that already have matching open beads
- **Skip findings where a closed bead's fix introduced the pattern you're flagging.** Use `bd show <id>` on relevant closed beads. If the current code is the intentional resolution of a prior bug, do not re-raise it.
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

## Severity

- **P1**: Shared mutable state, tests that never fail, tests masking real bugs
- **P2**: Missing assertions on return values, unclear test names, no isolation
- **P3**: Missing edge cases, minor readability issues

## Output

You MUST produce a report following the exact structure shown in `REFERENCE.md`.

**`--create-beads` mode**: Use `bug` for test quality failures; use `task` for missing coverage that needs to be added.

Each bead description MUST be structured in three parts:

```
<file:line>

<Explanation of the problem: what is wrong or missing and why it matters.>

Fix: <Concrete prescription. For quality bugs, specify exactly what must change
(e.g., "replace the shared `db` package-level var with a per-test instance
constructed in each test's setup"). For coverage tasks, specify exactly what
scenario or assertion is missing (e.g., "add a test case where the input
slice is nil; the current table has only empty-slice and non-empty cases").>

Done when: <A verifiable criterion. Must be checkable by reading the test file.
Example: "TestFoo has no package-level mutable state; all state is initialized
inside t.Run or TestFoo itself."
NOT: "The test is properly isolated.">
```

- Quality bugs (shared state, assertions that never fail, tests that mask bugs):
  ```bash
  bd create --type=bug --priority=<1-2> --title="Test: <issue>" \
    --description="<file:line>

  <explanation>

  Fix: <concrete prescription>

  Done when: <verifiable criterion>"
  ```

- Missing coverage (edge cases, error paths, boundary conditions):
  ```bash
  bd create --type=task --priority=<2-3> --title="Test: <what to add>" \
    --description="<file:line>

  <explanation>

  Fix: <concrete prescription>

  Done when: <verifiable criterion>"
  ```
