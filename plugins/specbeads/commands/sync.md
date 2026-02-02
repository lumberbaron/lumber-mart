---
description: Bidirectional sync between beads and tasks.md. Checks off tasks for closed beads, closes beads for completed tasks, and reports orphans.
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Argument Parsing

Parse `$ARGUMENTS` for:
- **Spec folder name**: If provided (e.g., `001-user-auth`), use that spec instead of deriving from branch
- **`--dry-run`**: Report what would change without modifying tasks.md or closing beads
- **`--no-validate`**: Skip file-existence validation checks
- **`--direction <both|beads-to-tasks|tasks-to-beads>`**: Sync direction (default: `both`)

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

> [!IMPORTANT]
> Do NOT use a bare `bd list --type task --status=all` to load beads.
> `bd list` defaults to `--limit 50`, silently dropping beads beyond the first 50
> and causing sync to miss closed work. Use the epic-walk approach below.

#### 3a. Enumerate phase epics

```bash
bd list --type epic --status=all
```

Filter to epics whose title matches `Phase N:` (these are created by `/specbeads:beadify`).

#### 3b. Walk each epic's children

For each phase epic, run:

```bash
bd show <epic-id>
```

Parse the `CHILDREN` section. Each child line contains:
- Bead ID (e.g., `wine-db-x76b.2`)
- Status indicator (`✓` = closed, `○` = open, `?` = unknown/deleted)
- Title (contains `T###:` pattern for task-mapped beads)

#### 3c. Search for unmatched tasks

After the epic walk, compare task IDs from tasks.md against the map built in 3b.
For any task ID **not yet found**, search for it directly:

```bash
bd search "T029:" --type task --status=all --limit 0
```

This catches beads created outside of phase epics (e.g., manually created).
Run one search per missing task ID — each returns a small, targeted result set.
Add any matches to the map.

> `bd search` also defaults to `--limit 50`; always pass `--limit 0`.

#### 3d. Build the bead-to-task map

For each discovered bead (from 3b and 3c):
- Extract task ID if title contains `T###:` pattern
- Map bead ID to task ID
- Map bead ID to status (open/closed)
- Skip children with `?` status (deleted beads)

#### 3e. Verify completeness

Compare the final map against task IDs from tasks.md.
Any task IDs still not found feed into orphan detection in step 4c.

### 4a. Beads to Tasks (skip if `--direction tasks-to-beads`)

Find tasks where:
- tasks.md shows `[ ]` (pending)
- A corresponding bead exists and is **closed**

These are candidates for check-off.

#### Validation (unless `--no-validate`)

For each candidate task, do a basic file-existence check:
- Extract file paths mentioned in the task description
- Verify each referenced file exists on disk

If any referenced file is missing, flag that task as a **warning** and skip checking it off.

#### Apply

For each validated candidate (unless `--dry-run`):
- Change `- [ ] T###` to `- [x] T###` in tasks.md

Write the updated tasks.md back to disk.

### 4b. Tasks to Beads (skip if `--direction beads-to-tasks`)

Find beads where:
- A corresponding task exists in tasks.md and is marked `[x]` (complete)
- The bead is still **open**

These are candidates for auto-close.

#### Validation (unless `--no-validate`)

For each candidate bead, do a basic file-existence check:
- Extract file paths mentioned in the bead description or the corresponding task description
- Verify each referenced file exists on disk

If any referenced file is missing, flag that bead as a **warning** and skip closing it.

#### Apply

For each validated candidate (unless `--dry-run`):

```bash
bd close <bead-id> --reason "Auto-closed by /specbeads.sync - task marked complete in tasks.md"
```

### 4c. Orphan Detection

Identify and report (never auto-create or auto-delete):

- **Unbeadified tasks**: Tasks in tasks.md with no corresponding bead
- **Orphan beads**: Beads with a `T###:` title pattern but no matching task in tasks.md

These are reported in the summary only.

### 5. Report Summary

Output a summary:

```
Sync Report for specs/<feature>
================================

## Direction: <both | beads-to-tasks | tasks-to-beads>

## Beads → Tasks

| Category | Count |
|----------|-------|
| Total tasks in tasks.md | <N> |
| Already complete | <N> |
| Checked off this run | <N> |
| Warnings (skipped) | <N> |

### Tasks Checked Off

- T###: <description>
- ...

### Warnings

- T###: <description> — missing file: <path>

## Tasks → Beads

| Category | Count |
|----------|-------|
| Total beads | <N> |
| Already closed | <N> |
| Closed this run | <N> |
| Warnings (skipped) | <N> |

### Beads Closed

- <bead-id> (T###): <description>
- ...

### Warnings

- <bead-id> (T###): <description> — missing file: <path>

## Orphans

| Category | Count |
|----------|-------|
| Unbeadified tasks | <N> |
| Orphan beads | <N> |

### Unbeadified Tasks

<N> tasks in tasks.md have no corresponding beads.
Run `/specbeads.beadify` to create beads for these tasks.

### Orphan Beads

<N> beads have T### titles but no matching task in tasks.md.
Review these beads manually — they may reference removed or renamed tasks.
```

In `--dry-run` mode, prefix with:
```
DRY RUN - No changes made. The following would occur:
```

And replace "Checked Off" / "Closed" with "Would Check Off" / "Would Close".

## Error Handling

- If `bd` commands fail, report the error and abort
- If tasks.md cannot be parsed, report the error and abort
- Validation warnings do not abort — they skip individual items and report

## Design Principles

- **Bidirectional**: Syncs both beads→tasks.md and tasks.md→beads by default
- **Lightweight**: No builds, no tests, no architecture checks. Just status sync with basic file validation.
- **Safe**: Validation catches obvious mismatches before syncing. `--dry-run` available for preview.
- **Direction control**: Use `--direction` to limit to one direction if needed. The old one-way behavior is available via `--direction beads-to-tasks`.
- **Report-only orphans**: Orphan detection never auto-creates or auto-deletes — only reports.
