---
name: implement
description: Implement a spec-kit feature phase or standalone bug/task beads. Executes tasks one at a time, committing after each, with diff verification before closing. Use --all for multiple phases, --standalone [filter] for bug/task beads outside a feature plan.
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Argument Parsing

Parse `$ARGUMENTS` for:
- **Epic bead ID** (e.g., `sam-cp7l`): Implement that specific phase epic
- **Standalone bead ID** (e.g., `sam-b3i`): Implement that specific bug or task bead (see Standalone Mode below)
- **Feature slug** (e.g., `002-realtime-gateway`): Find and implement the next ready phase for that feature
- **`--standalone [filter]`**: Implement ready standalone bug and task beads (see Standalone Mode below). Optional filter text after the flag narrows which beads are selected by matching against bead titles (case-insensitive substring). Example: `--standalone code bugs` selects only beads whose title contains "code"; `--standalone test` selects only test-related beads.
- **`--all`**: Implement all currently unblocked phases sequentially, continuing after each completes
- **`--dry-run`**: Show the execution plan without making any changes
- **Additional instructions**: Any other text (not following `--standalone`) is treated as implementation guidance (constraints, approach hints, scope limits) applied throughout

If no arguments: find the next ready phase — the first unblocked phase epic with open tasks — and implement it. If multiple feature slugs are present in the project, confirm with the user which feature to work on.

## Standalone Mode

Standalone mode handles bug and task beads that are not part of a spec-kit phase epic — for example, beads created by `review-code --create-beads`.

### Resolving the bead list

**Single bead ID given:**
```bash
bd show <bead-id>
```
Use that bead directly. Confirm it is type `bug` or `task`; if it is an `epic`, switch to phase mode.

**`--standalone [filter]`:**
```bash
bd ready
```
Filter results to type `bug` or `task` (exclude epics and their subtasks). If a filter string was provided, further narrow to beads whose title contains the filter text (case-insensitive). Show the selected list to the user before proceeding.

> [!CAUTION]
> If no matching beads are ready, stop and report: "No standalone beads match. Run `bd ready` to check."

### Executing standalone beads

Process each selected bead sequentially — one at a time, in the order returned by `bd ready`.

For each bead:

1. `bd update <bead-id> --status=in_progress`
2. `bd show <bead-id>` — read the full description
3. **Synthesize a "Done when" clause if absent.** If the description does not contain a `Done when:` section, derive one from the description text and state it explicitly before coding:
   - Identify the specific functions, files, or behaviours that must change
   - Write a criterion that can be confirmed by reading the diff (e.g., "Both X and Y call shared helper Z; no duplicated logic remains in either")
   - Show the synthesized criterion to the user
4. **Implement the fix.** Stay within the files and functions named in the description.
5. **Verify the "Done when" clause** — either the one from the description or the one synthesized in step 3:
   - Run `git diff HEAD` and check that every file or function named in the description was actually changed
   - If the description references a file that was not touched, stop and explain the gap before closing
   - Run any tests cited in the description or relevant to the changed files
6. **Commit:**
   ```bash
   git add <files changed>
   git commit -m "fix: <bead title> [<bead-id>]

   Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
   ```
7. `bd close <bead-id>`

Repeat for the next bead. Do not bundle multiple beads into one commit.

---

## Outline

### 1. Resolve the Target Phase

#### If an epic bead ID was given
```bash
bd show <epic-id>
```
Use that epic directly.

#### If a feature slug was given
```bash
bd list --type epic --status=open
```
Filter to epics whose description contains `Feature: <slug>`. Select the lowest-numbered phase with open tasks and no blocking dependencies.

#### If no argument
```bash
bd ready --type epic
```
Select the first result (lowest-priority-numbered ready epic with open tasks).

> [!CAUTION]
> If no ready epic is found (all blocked or all closed), stop and report: "No phases are ready to implement. Run `bd ready` to check dependencies."

#### If `--all`
Resolve the first target phase as above. After completing it, re-resolve to find the next unblocked phase and continue. Stop when no more ready phases exist.

### 2. Load Phase Context

```bash
bd show <epic-id>
```

Parse the epic description's **feature header block** (written by the beadify skill):
```
Feature: {FEATURE_SLUG}
Plan: {FEATURE_DIR}/plan.md §<phase section>
Covers: {FEATURE_DIR}/spec.md §<user story>
```

Extract:
- `FEATURE_SLUG` — the feature identifier (e.g., `002-realtime-gateway`)
- `FEATURE_DIR` — the spec folder path (e.g., `specs/002-realtime-gateway`)
- `PLAN_SECTION` — the exact plan.md section heading for this phase
- Covered user stories from spec.md

Read the referenced plan section for architecture context and implementation notes. This is background — the tasks themselves are the primary work queue.

> [!NOTE]
> If the feature header block is missing (older bead format), fall back to reading `specs/` for any plan.md and ask the user to confirm the feature.

### 3. Load and Sequence Tasks

```bash
bd show <epic-id>
```

Collect all child tasks. For each, note status, bead ID, title, and `blockedBy` list. Skip closed tasks. Treat `in_progress` tasks as open (resume from the beginning of that task).

**Build a dependency-ordered execution plan** by topological sort:
- Group tasks into **waves** — tasks in the same wave have no dependencies between them and can run in parallel
- Tasks with `blockedBy` wait for their blockers to complete before starting

Output the execution plan to the user before starting:
```
Phase N: <Title> [<epic-id>]
Feature: {FEATURE_SLUG}

Execution plan:
  Wave 1 (parallel): <task titles>
  Wave 2 (sequential): <task title>  ← blocked by Wave 1
  ...

Tasks remaining: X of Y
```

Stop here in `--dry-run` mode.

### 4. Execute Tasks

Work through waves in order.

#### Single task in wave → implement directly

1. `bd update <task-id> --status=in_progress`
2. `bd show <task-id>` — read the full description: feature anchor, full spec paths, exact files to touch, scope boundaries, cross-task handoff notes, and the "Done when" clause
3. Read any spec sections explicitly cited that have detail beyond what the description captures
4. **Implement the task.** Stay strictly within the stated file scope — if the description says "this task writes the migration; task .2 wires it in," do not wire it in
5. **Verify the "Done when" clause.** Run whatever checks it specifies (tests, `terraform validate`, file existence, etc.). Additionally, run `git diff HEAD` and confirm that every file or function explicitly named in the description was actually changed. If any named file was not touched, stop and explain the gap before closing the task. Fix failures before proceeding
6. **Commit:**
   ```bash
   git add <files changed>
   git commit -m "feat({FEATURE_SLUG}): <task title> [{task-id}]

   Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
   ```
7. `bd close <task-id>`

#### Multiple tasks in wave → spawn parallel subagents

Use the Task tool — one subagent per task, running concurrently. Each subagent receives:
- Full task description (verbatim from `bd show <task-id>`)
- Feature slug and spec dir
- Instruction to: mark in_progress → implement → verify done-when → commit → mark complete
- Commit message format: `feat({FEATURE_SLUG}): <task title> [{task-id}]`
- Any user-provided additional instructions from `$ARGUMENTS`

Wait for all subagents in the wave to complete before starting the next wave. If any subagent reports failure, stop and surface the error — do not continue to dependent tasks.

> [!CAUTION]
> Verify no two tasks in the same wave edit the same file before spawning. If they do, treat them as sequential. The beadify scope boundary rule should have prevented this, but verify.

### 5. Phase Quality Gate

After all tasks in the phase are complete:

| Phase type signals | Quality gate |
|--------------------|--------------|
| Python files changed | `uv run pytest` (subset relevant to this phase) |
| Terraform files changed | `terraform validate` in the module directory |
| Both | Run both |
| Integration / hardening phase | Done-when clauses define their own verification |

If the quality gate fails:
1. Report which check failed and the output
2. Fix the issue (staying within the scope of this phase)
3. Re-run until it passes
4. Do NOT close the epic until the gate passes

### 6. Close the Phase and Sync

```bash
bd close <epic-id>
bd sync
git add .beads/
git commit -m "chore({FEATURE_SLUG}): complete Phase N [{epic-id}]

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
git push
```

Verify push succeeded. If it fails (remote diverged), `git pull --rebase` and push again.

### 7. Report and Hand Off

```
Phase N complete: <Title> [{epic-id}]
Feature: {FEATURE_SLUG}

Tasks completed: X
  ✓ <task title> [<id>]   — <one-line summary of what was done>
  ...

Quality gate: passed (uv run pytest: X passed / terraform validate: ok)

Committed and pushed.

Next:
  Unblocked by this phase: <next phase title> [<id>]
  Run `/implement` to continue, or `bd show <next-epic-id>` to review.
```

If `--all` was specified and another phase is now ready, proceed automatically.

## Handling Interruptions and Partial Progress

If invoked on a phase that is partially complete (some tasks closed, some open):
1. Report: "Phase N is X% complete — Y tasks done, Z remaining."
2. Skip all closed tasks.
3. Resume from the first open/in_progress task in dependency order.
4. Run the full quality gate at the end regardless of how many tasks were skipped.

## Scope Discipline

- Do not implement tasks from other phases even if they seem related
- Do not refactor outside the task's stated file scope
- Do not add features beyond the "Done when" clause
- If a task references a spec decision as background only, do not act on it unless the task explicitly says to

If you discover a blocking issue outside your scope, create a bead:
```bash
bd create --type bug \
  --title "Blocking: <description>" \
  --description "Feature: {FEATURE_SLUG}
Discovered while implementing {task-id}. <detail>

Done when: <resolution criterion>"
```
Then surface it to the user rather than working around it silently.

## Design Principles

- **Bead-driven**: Task descriptions (written by beadify) are the source of truth — feature anchor, spec paths, file scope, done-when. Trust and follow them.
- **Commit granularity**: One commit per task. Readable history, surgical rollback.
- **Verify before closing**: The "Done when" clause is not a suggestion. Never close a task without confirming it passes.
- **Parallel when safe**: Independent tasks run concurrently via subagents. Dependency order is always respected.
- **Fail loudly**: Surface errors rather than working around them. Do not continue to dependent tasks after a failure.
- **Scope discipline**: Implement exactly what the task says — no more, no less.
