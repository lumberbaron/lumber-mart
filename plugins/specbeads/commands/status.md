---
description: Show project progress dashboard with task/bead completion, phase status, sync health, and actionable recommendations. Read-only.
---

# Status Dashboard

Display a read-only overview of project progress and sync health.

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Argument Parsing

Parse `$ARGUMENTS` for:
- **Spec folder name**: If provided (e.g., `001-user-auth`), use that spec instead of deriving from branch
- **`--verbose`**: Show per-task detail tables within each phase

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

### 2. Load Data

#### tasks.md

Read `FEATURE_DIR/tasks.md` and parse:
- Phase headings (`## Phase N: Title`)
- Tasks per phase (`- [x| ] T### ...`)
- Extract completion status for each task

#### Beads

> [!IMPORTANT]
> Do NOT use a bare `bd list --type task --status=all` to load beads.
> `bd list` defaults to `--limit 50`, silently dropping beads beyond the first 50
> and causing status to report incorrect sync health. Use the epic-walk approach below.

**Step 1**: Enumerate phase epics:

```bash
bd list --type epic --status=all
```

Filter to epics whose title matches `Phase N:`.

**Step 2**: Walk each epic's children:

For each phase epic, run `bd show <epic-id>` and parse the `CHILDREN` section.
Each child line contains a bead ID, status indicator (`✓` closed, `○` open, `?` deleted), and title.

**Step 3**: Search for unmatched tasks:

After the epic walk, compare task IDs from tasks.md against the map built in Step 2.
For any task ID **not yet found**, search directly with `bd search "T029:" --type task --status=all --limit 0`.
This catches beads created outside of phase epics. Run one search per missing task ID.

> `bd search` also defaults to `--limit 50`; always pass `--limit 0`.

**Step 4**: Build the bead-to-task map:

For each discovered bead (from Steps 2 and 3):
- Extract task ID if title contains `T###:` pattern
- Map bead ID to task ID and status (open/closed)
- Skip children with `?` status (deleted beads)
- Skip children with `?` status (deleted beads)

### 3. Compute Metrics

#### Overall Progress

- Tasks completed vs total (from tasks.md)
- Beads closed vs total (from beads)

#### Phase Progress

For each phase:
- Count completed tasks / total tasks
- Derive status:
  - **Not started**: 0 tasks complete
  - **In progress**: some but not all tasks complete
  - **Complete**: all tasks complete

#### Sync Health

Cross-reference tasks.md and beads to identify:
- **Agreed**: Task and bead status match (both complete or both pending)
- **Task ahead**: Task `[x]` but bead still open
- **Bead ahead**: Bead closed but task still `[ ]`
- **Unbeadified**: Task exists in tasks.md but has no bead
- **Orphan beads**: Bead has `T###:` title but no matching task in tasks.md

### 4. Display Dashboard

Output the dashboard:

```
Status for specs/<feature>
===========================

## Overall Progress

Tasks: <completed>/<total> (<percentage>%)
Beads: <closed>/<total> (<percentage>%)

## Phase Progress

| Phase | Title | Tasks | Status |
|-------|-------|-------|--------|
| 1 | <title> | <done>/<total> | <Not started | In progress | Complete> |
| 2 | <title> | <done>/<total> | <status> |
| ... | ... | ... | ... |

## Sync Health

| Category | Count |
|----------|-------|
| In agreement | <N> |
| Task ahead (task [x], bead open) | <N> |
| Bead ahead (bead closed, task [ ]) | <N> |
| Unbeadified tasks | <N> |
| Orphan beads | <N> |

## Recommendations

- <actionable recommendation based on findings>
- ...
```

#### Recommendations Logic

Generate recommendations based on the metrics:

- If **task ahead** > 0: "Run `/specbeads.sync` to close N beads that match completed tasks."
- If **bead ahead** > 0: "Run `/specbeads.sync` to check off N tasks that match closed beads."
- If **unbeadified** > 0: "Run `/specbeads.beadify` to create beads for N untracked tasks."
- If **orphan beads** > 0: "N orphan beads found — review manually for removed or renamed tasks."
- If everything is in sync: "All tasks and beads are in sync. No action needed."

### 5. Verbose Output (if `--verbose`)

After the main dashboard, show per-phase detail tables:

```
## Phase 1: <Title> — <status>

| Task | Description | tasks.md | Bead | Bead Status |
|------|-------------|----------|------|-------------|
| T001 | <desc> | [x] | <bead-id> | closed |
| T002 | <desc> | [ ] | <bead-id> | open |
| T003 | <desc> | [ ] | — | (no bead) |

## Phase 2: <Title> — <status>
...
```

## Error Handling

- If `bd` commands fail, report the error and show what data is available (tasks.md-only view)
- If tasks.md cannot be parsed, report the error and abort

## Design Principles

- **Strictly read-only**: Never mutates beads or tasks.md
- **Actionable**: Recommendations point to specific commands to resolve issues
- **Quick overview**: Default output is concise; use `--verbose` for detail
- **No prerequisites beyond data**: Does not require builds, tests, or spec documents beyond tasks.md
