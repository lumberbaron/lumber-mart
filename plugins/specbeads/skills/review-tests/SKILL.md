---
name: review-tests
description: Review tests for completeness, usefulness, isolation, and readability. Use when asked to review tests, check test quality, audit test coverage, or validate test files.
---

# Tests Review

Review tests in the specified path for quality issues.

> [!IMPORTANT]
> Consult [REFERENCE.md](REFERENCE.md) for the expected output format and level of detail.

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

### Step 1 — Discover test files

Find all test files in the specified path using language-appropriate patterns: `*_test.go`, `test_*.py`, `*_test.py`, `*.test.ts`, `*.test.js`, `*.spec.ts`, `*.spec.js`, `__tests__/**`, etc. Record the full file list and count.

### Step 2 — Choose execution strategy

- **1–2 files → Direct mode**: Read the files, evaluate against the Quality Criteria below, then proceed to Deduplication and Bead Check.
- **3+ files → Parallel mode**: Batch files, spawn subagents, collect results, merge, then proceed to Deduplication and Bead Check.

### Parallel Review Mode

Use this mode when 3 or more test files are discovered.

#### Batching

Group files into batches based on total file count:

| Total files | Files per batch | ~Subagents |
|-------------|-----------------|------------|
| 3–10        | 1               | 3–10       |
| 11–20       | 2               | 6–10       |
| 21+         | 3               | 7–10       |

#### Spawn subagents

For each batch, use `Agent(subagent_type="general-purpose")`. **Spawn all subagents in a single message** so they run in parallel.

Each subagent prompt MUST include:

1. The file paths in its batch (instruct the subagent to read them)
2. The **Quality Criteria** section from this skill — copy it verbatim into the prompt
3. The **Severity** section from this skill — copy it verbatim into the prompt
4. The structured output format below
5. The explicit instruction: **"Do NOT use the Bash tool. Do NOT run any shell commands. Use only Read, Grep, and Glob tools. Do NOT create beads, do NOT run `bd` commands. Return findings only."**
6. The explicit instruction: **"For every P3 finding, you MUST state a concrete falsifiability claim in the `explanation` field: 'if \<specific code change\> were made, this test would incorrectly pass.' Omit P3 findings that lack this claim."**
7. The explicit instruction: **"For the `pattern` field, use a short, reusable label that names the underlying anti-pattern (e.g., 'module-scope mutable mocks', 'tautological assertions'). If two findings in your batch stem from the same root cause, they MUST use the same pattern label."**

Instruct each subagent to return findings in this exact delimited format (one block per finding):

```
---FINDING---
priority: P<1|2|3>
location: <file:line>
title: <short title>
category: <Completeness|Usefulness|Output Validation|Isolation|Readability|Integration Test Specifics>
pattern: <short label for the underlying anti-pattern, e.g. "module-scope mutable mocks" or "tautological assertions" — use the SAME label across findings that share the same root cause>
explanation: <what is wrong or missing and why it matters>
fix: <concrete prescription>
done_when: <verifiable criterion>
---END---
```

If the subagent finds no issues for its batch, it should return `---NO-FINDINGS---`.

#### Collect and merge

After all subagents return:

1. Parse each subagent's structured findings
2. Combine into a single list, sorted by priority (P1 first)
3. Deduplicate: if two findings share the same `location` (file:line) AND the same `category`, keep only the one with the highest priority
4. Group findings by `pattern` label — findings from different subagents that used the same (or very similar) pattern label share a root cause and will be collapsed in the Pattern Collapsing step

#### Error fallback

If a subagent fails or returns unparseable output, review those files directly (as in direct mode) and include a note in the report: `Note: Files [list] were reviewed directly due to subagent failure.`

### Pattern Collapsing

Both direct mode and parallel mode flow into this step before bead creation.

After merging all findings, look for findings that share the **same root cause** — i.e., the same testing anti-pattern repeated across multiple test files. Examples:

- Multiple test files flagged for "module-level mutable mock leaks between tests" → one pattern: "test suite uses module-scope mocks instead of per-test setup"
- Multiple test files flagged for "globalThis.fetch replaced at module scope" → one pattern: "fetch mocking is done at import time instead of in beforeEach"
- Multiple test files flagged for "assertions only check error status, not return values" → one pattern: "tests validate calls were made but not results returned"

When you identify a shared root cause:

1. **Collapse** the N per-file findings into **one finding** that names the pattern, lists all affected files, and prescribes the codebase-wide fix
2. **Set severity** to the highest severity among the collapsed findings
3. **Keep separate** any findings that happen to share a category but have genuinely different root causes

This is critical: N beads for N instances of the same pattern creates noise. One bead that names the pattern and lists the affected locations is actionable.

### Deduplication and Bead Check

Before creating a bead, check if one already exists:
- Run `bd list --status=open` to see all open issues
- Run `bd list --status=closed` to see previously resolved issues
- Compare your findings against existing bead titles and descriptions
- Skip creating beads for issues that already have matching open beads
- **Check closed beads before suppressing.** Use `bd show <id>` on relevant closed beads and verify the fix actually resolved the issue in the current code. Only suppress if the fix is complete — if the problem still exists (in the same or different locations), create a new bead for the remaining instances. The goal is to prevent flip-flopping on intentional resolutions, not to give closed beads permanent immunity.
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

- **P1**: Tests that **literally cannot fail** — tautological assertions (asserting against a freshly-created mock, asserting truthiness on a value that is always truthy), tests that mask real production bugs (e.g., simulating events differently than the browser does, hiding double-fires). **Shared mutable state is P1 only when it causes actual test interference** (tests fail or produce different results depending on run order). If the shared state is merely a code smell but tests still pass reliably in any order, that is P2.
- **P2**: Shared mutable state that hasn't caused interference yet but is fragile, missing assertions on return values, unclear test names, no isolation
- **P3**: Missing edge cases or assertions where you can state a **concrete falsifiability claim** — i.e., "if \<specific code change\> were made, this test would incorrectly pass." Do **not** raise P3 for suggestions that only make a test more thorough without identifying a realistic false-pass scenario.

## Output

You MUST produce a report following the exact structure shown in `REFERENCE.md`. When using parallel mode, the lead assembles the unified report from subagent findings. The report format is identical regardless of execution mode.

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
