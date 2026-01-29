---
description: Lightweight one-way sync from beads to tasks.md. Checks off tasks whose beads are closed, with basic file-existence validation.
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Argument Parsing

Parse `$ARGUMENTS` for:
- **Spec folder name**: If provided (e.g., `001-user-auth`), use that spec instead of deriving from branch
- **`--dry-run`**: Report what would change without modifying tasks.md
- **`--no-validate`**: Skip file-existence validation checks

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

### 2. Load tasks.md

Read `FEATURE_DIR/tasks.md` and parse all task lines matching `- [x| ] T### [P?] [US#?] Description`:
- Extract task ID (e.g., T001)
- Extract completion status (`[x]` = done, `[ ]` = pending)
- Extract file paths mentioned in the description

### 3. Load Beads

Query all beads including closed ones:

```bash
bd list --type task --status=all --format json 2>/dev/null || bd list --type task --status=all
```

For each bead:
- Extract task ID if title contains `T###:` pattern
- Map bead ID to task ID
- Map bead ID to status (open/closed)

### 4. Match Closed Beads to Pending Tasks

Find tasks where:
- tasks.md shows `[ ]` (pending)
- A corresponding bead exists and is **closed**

These are candidates for check-off.

Skip tasks that have no matching bead (those are untracked — suggest `/specbeads.beadify`).

### 5. Lightweight Validation (unless `--no-validate`)

For each candidate task, do a basic file-existence check:
- Extract file paths mentioned in the task description
- Verify each referenced file exists on disk

If any referenced file is missing, flag that task as a **warning** and skip checking it off. Report it in the summary.

### 6. Update tasks.md

For each validated candidate (unless `--dry-run`):
- Change `- [ ] T###` to `- [x] T###` in tasks.md

Write the updated tasks.md back to disk.

In `--dry-run` mode, report what would change without writing.

### 7. Report Summary

Output a summary:

```
Sync Report for specs/<feature>
================================

## Results

| Category | Count |
|----------|-------|
| Total tasks in tasks.md | <N> |
| Already complete | <N> |
| Checked off this run | <N> |
| Warnings (skipped) | <N> |
| Tasks without beads | <N> |

## Tasks Checked Off

- T###: <description>
- T###: <description>

## Warnings

- T###: <description> — missing file: <path>

## Untracked Tasks

<N> tasks in tasks.md have no corresponding beads.
Run `/specbeads.beadify` to create beads for these tasks.
```

In `--dry-run` mode, prefix with:
```
DRY RUN - No changes made. The following would occur:
```

And replace "Checked Off" with "Would Check Off".

## Error Handling

- If `bd` commands fail, report the error and abort
- If tasks.md cannot be parsed, report the error and abort
- Validation warnings do not abort — they skip individual tasks and report

## Design Principles

- **One-directional**: Beads → tasks.md only. Does not close beads or create beads.
- **Lightweight**: No builds, no tests, no architecture checks. Just status sync with basic file validation.
- **Safe**: Validation catches obvious mismatches before checking off. `--dry-run` available for preview.
- **Non-destructive**: Only changes `[ ]` to `[x]`. Never unchecks tasks or modifies bead state.
