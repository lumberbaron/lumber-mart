---
description: Validate and reconcile state between beads, tasks, and implementation. Creates issues for discrepancies.
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Argument Parsing

Parse `$ARGUMENTS` for:
- **Spec folder name**: If provided (e.g., `001-user-auth`), use that spec instead of deriving from branch
- **`--dry-run`**: Report discrepancies without creating beads or closing any
- **`--skip-tests`**: Skip running build/tests (faster validation)
- **`--verbose`**: Show detailed validation output

## Outline

### 1. Validate Prerequisites

Run prerequisite checks:

```bash
./.specify/scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks
```

Parse the JSON response to get `FEATURE_DIR`.

Then verify beads is initialized:

```bash
bd info
```

> [!CAUTION]
> ERROR if beads is not initialized. Instruct user to run `bd onboard` first.
> ERROR if tasks.md is missing. Instruct user to run `/speckit.tasks` first.

If a spec folder name was provided in arguments, override `FEATURE_DIR` to `specs/<folder-name>`.

### 2. Load Context Documents

Read from `FEATURE_DIR`:
- **Required**: `tasks.md`, `spec.md`
- **Optional**: `plan.md`, `.specify/memory/constitution.md`

### 3. Build Comparison Model

#### 3.1 Parse tasks.md

Extract the following structure:

**Tasks**: Lines matching `- [x| ] T### [P?] [US#?] Description`
- `[x]` = completed, `[ ]` = pending
- `T###` = task ID (e.g., T001, T042)
- Extract file paths from descriptions (e.g., `internal/auth/handler.go`)

Store:
- Task ID → completion status mapping
- Task ID → description mapping
- Task ID → file paths mentioned

#### 3.2 Parse beads

Query existing beads:

```bash
bd list --type task --status=all --format json 2>/dev/null || bd list --type task --status=all
bd list --type epic --status=all --format json 2>/dev/null || bd list --type epic --status=all
```

For each bead:
- Extract task ID if title contains `T###:` pattern
- Map bead ID to task ID
- Map bead ID to status (open/closed)

### 4. Reconciliation Checks

#### 4.1 Beads ↔ Tasks.md Sync

Compare task completion status against bead status:

| Condition | Action |
|-----------|--------|
| Task `[x]` in tasks.md, bead open | Auto-close the bead (unless `--dry-run`) |
| Task `[ ]` in tasks.md, bead closed | Create discrepancy bead |
| Task in tasks.md, no bead | Count for beadify suggestion |
| Bead exists with T### title, no matching task in tasks.md | Create discrepancy bead (orphan) |

#### 4.2 Deep Implementation Validation (unless `--skip-tests`)

Run quality gates (adapt commands to the project's build system):

```bash
# Examples - use project-specific commands
make build 2>&1    # or: go build ./..., npm run build, cargo build
make test 2>&1     # or: go test ./..., npm test, cargo test
make lint 2>&1     # or: golangci-lint run, npm run lint, cargo clippy
```

Track results:
- Build: PASSED/FAILED
- Tests: PASSED/FAILED (with counts if available)

For any failure when tasks are marked complete (`[x]` in tasks.md OR closed bead):
- Create discrepancy bead indicating tests/build failing despite completion

#### 4.3 Architecture Consistency

Compare plan.md architectural decisions against implementation. Examples of validation checks:

| Plan Element | Validation Check |
|--------------|------------------|
| Language/runtime version | Check version in go.mod, package.json, Cargo.toml, etc. |
| Framework choice | Verify framework config files exist (e.g., next.config.js, vite.config.ts) |
| Database driver | Grep for expected imports/dependencies |
| External services | Check for client library imports or config files |
| Directory structure | Verify expected directories exist |

Adapt checks based on what's specified in plan.md. For each mismatch, create discrepancy bead.

#### 4.4 Constitution Alignment

If the project has a constitution (`.specify/memory/constitution.md`), perform spot-checks for each principle. Examples:

| Principle Type | Example Check |
|----------------|---------------|
| API design standards | Verify endpoint patterns match declared style (REST, GraphQL, gRPC) |
| Infrastructure requirements | Check for IaC files if declared (Terraform, Pulumi, CloudFormation) |
| Security requirements | Verify auth middleware exists, secrets not hardcoded |
| Testing requirements | Check test coverage meets declared thresholds |
| Code organization | Verify directory structure matches declared patterns |

Adapt checks based on the actual principles in the project's constitution. For violations, create discrepancy bead.

### 5. Auto-Close Completed Tasks

For tasks where:
- tasks.md shows `[x]` (complete)
- Corresponding bead is still open
- Tests pass (if running tests) OR `--skip-tests` specified

Auto-close the bead:

```bash
bd close <bead-id> --reason "Auto-closed by /specbeads.reconcile - task marked complete in tasks.md"
```

In `--dry-run` mode, report what would be closed without executing.

### 6. Create Discrepancy Beads

For each discrepancy found (unless `--dry-run`), create a bead:

```bash
bd create --type task \
  --title "RECONCILE: <short description>" \
  --description "<detailed description>" \
  --priority 1
```

**Description template**:

```
## Discrepancy Found

**Type**: <Beads-Tasks Mismatch | Test Failure | Architecture Drift | Constitution Violation>
**Detected**: <timestamp>
**Source**: `/specbeads.reconcile` validation

## Details

<Clear explanation of what was expected vs what was found>

## Context

- **Task ID**: T### (if applicable)
- **Bead ID**: beads-xxx (if applicable)
- **File(s)**: <relevant paths>

## Question for User

What should be done about this discrepancy?

1. **Fix the implementation** - Update code to match the task/plan
2. **Update the task** - The task definition was wrong/outdated
3. **Close as won't-fix** - Accept the current state
4. **Investigate further** - Need more information

Please update this bead with your decision and close it when resolved.
```

### 7. Handle Non-Beadified Tasks

If tasks.md contains tasks without corresponding beads, report:

```
Found <N> tasks in tasks.md without corresponding beads.

Run `/specbeads.beadify` to create beads for these tasks.
```

Do NOT auto-create beads (that's beadify's job).

### 8. Report Summary

Output a summary report:

```
Reconciliation Report for specs/<feature>
================================================

## Validation Results

Build: <PASSED | FAILED | SKIPPED>
Tests: <PASSED (N passed, M failed) | FAILED | SKIPPED>
Architecture: <CONSISTENT | N issues found>
Constitution: <ALIGNED | N violations found>

## Sync Status

| Category | Count |
|----------|-------|
| Tasks in tasks.md | <N> |
| Tasks with beads | <N> |
| Tasks without beads | <N> |
| Open beads | <N> |
| Closed beads | <N> |

## Actions Taken

- Closed <N> beads (tasks marked complete)
- Created <N> discrepancy beads:
  - <bead-id>: "<title>"
  - ...

## Recommendations

1. <recommendation based on findings>
2. ...

## Discrepancy Beads Created

| Bead ID | Type | Summary |
|---------|------|---------|
| <id> | <type> | <summary> |
| ... | ... | ... |
```

In `--dry-run` mode, prefix with:
```
DRY RUN - No changes made. The following would occur:
```

And replace "Actions Taken" with "Actions That Would Be Taken".

## Error Handling

- If `bd` commands fail, report the error and continue with remaining checks
- If build/test commands fail, capture output and include in discrepancy bead description
- Track failures and include in summary
- If beads is not initialized, abort early with clear instructions

## Design Principles

- **Discrepancies create beads, not auto-fix**: User must decide resolution
- **Build/test failures are discrepancies**: Don't silently pass broken code
- **Non-beadified tasks → suggest beadify**: Don't duplicate that command's logic
- **Auto-close only when confident**: tasks.md `[x]` + tests pass = safe to close
- **Priority 1 for discrepancy beads**: These need attention
- **Read-only in dry-run**: No mutations, only reporting
