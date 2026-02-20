---
name: implement
description: Implement a spec-kit feature phase by reading its beads and executing tasks one at a time, committing after each. By default implements a single phase; can be given instructions to do more. Use when asked to implement a phase, work through tasks, or execute a feature plan.
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Argument Parsing

Parse `$ARGUMENTS` for:
- **Epic bead ID** (e.g., `sam-cp7l`): Implement that specific phase epic
- **Feature slug** (e.g., `002-realtime-gateway`): Find and implement the next ready phase for that feature
- **`--all`**: Implement all currently unblocked phases sequentially (still one phase at a time, but continues after each completes)
- **`--dry-run`**: Show what would be done without making any changes
- **Additional instructions**: Any other text is treated as implementation guidance (constraints, approach hints, scope limits) applied throughout

If no arguments: find the next ready phase — the first unblocked phase epic with open tasks — and implement it.

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
Filter to epics whose description contains `Feature: <slug>`. Select the lowest-numbered phase with open (not yet closed) tasks and no blocking dependencies.

#### If no argument
```bash
bd ready --type epic
```
Select the first result (lowest-priority-numbered ready epic with open tasks). If multiple feature slugs are present in the project, confirm with the user which feature to work on.

> [!CAUTION]
> If no ready epic is found (all blocked or all closed), stop and report: "No phases are ready to implement. Run `bd ready` to check dependencies."

#### If `--all`
Resolve the first target phase as above. After completing it, re-resolve to find the next unblocked phase and continue. Stop when no more ready phases exist.

### 2. Load Phase Context

Run:
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

Read the referenced plan section:
```
Read {FEATURE_DIR}/plan.md  (navigate to §{PLAN_SECTION})
```

This gives the phase goal, architecture context, and any implementation notes from the designer. This is background — the tasks themselves are the primary work queue.

> [!NOTE]
> If the epic description is missing the feature header block (older bead format), fall back to reading `specs/` for any plan.md and ask the user to confirm the feature.

### 3. Load and Sequence Tasks

```bash
bd show <epic-id>
```

Collect all child tasks. For each task, note:
- Status (open / in_progress / closed) — skip closed tasks
- Bead ID and title
- Blocking dependencies (`blockedBy` list)

**Build a dependency-ordered execution plan**:

1. Group tasks into **waves** — a wave is a set of tasks with no unresolved dependencies between them (topological sort layer by layer).
2. Within a wave, tasks are independent and can run in parallel.
3. Tasks with `blockedBy` relationships must wait for their blockers to complete before starting.

Example:
```
Wave 1 (parallel): sam-cp7l.1, sam-cp7l.2, sam-cp7l.3
Wave 2 (parallel): sam-cp7l.4   ← blocked by .1 and .3
```

Skip any tasks already closed. If a task is `in_progress` (possibly from a previous interrupted session), treat it as open and resume from the start of that task.

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

In `--dry-run` mode, stop here.

### 4. Execute Tasks

Work through waves in order. Within each wave:

#### Single task in wave → implement directly

Mark the task in progress:
```bash
bd update <task-id> --status=in_progress
```

Read the full task description:
```bash
bd show <task-id>
```

The task description contains everything needed: the feature anchor, full paths to referenced spec sections, exact file paths to create/modify, scope boundaries, cross-task handoff notes, and a "Done when" clause. Read any referenced spec sections that contain detail beyond what the description captures (per the "inline over reference" rule in beadify — if it was worth citing, it's worth reading).

**Implement the task.** Follow the description precisely. Stay within the stated scope — if the description says "this task writes the migration file; task .2 wires it in," do not wire it in.

**Verify the "Done when" clause.** The done-when is the acceptance criterion. Run whatever commands or checks are needed to confirm it passes — unit tests, `terraform validate`, file existence, etc. If verification fails, fix the implementation before proceeding.

**Commit**:
```bash
git add <files changed>
git commit -m "feat({FEATURE_SLUG}): <task title> [{task-id}]

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
```

Mark the task complete:
```bash
bd close <task-id>
```

#### Multiple tasks in wave → spawn parallel subagents

When a wave has 2+ independent tasks, use the Task tool to spawn general-purpose subagents — one per task — running them concurrently.

Each subagent receives a self-contained prompt including:
- The full task description (copy verbatim from `bd show <task-id>`)
- The feature slug and spec dir
- Instruction to: mark in_progress → implement → verify done-when → commit → mark complete
- The commit message format: `feat({FEATURE_SLUG}): <task title> [{task-id}]`
- Any user-provided additional instructions from `$ARGUMENTS`

Wait for all subagents in the wave to complete before starting the next wave. If a subagent reports failure, stop and surface the error — do not continue to dependent tasks.

> [!CAUTION]
> Parallel subagents must not edit the same file. Before spawning, check each task's file paths. If two tasks in the same wave touch the same file, treat them as sequential even if no explicit `bd dep` exists between them — the beadify scope boundary rule should have prevented this, but verify.

### 5. Phase Quality Gate

After all tasks in the phase are complete, run a phase-level verification pass based on the phase type:

| Phase type signals | Quality gate |
|--------------------|--------------|
| Contains Python files (`src/`, `tests/`, `lambda/`) | `uv run pytest` (or the subset of tests relevant to this phase) |
| Contains Terraform (`.tf` files) | `terraform validate` in the relevant module directory |
| Contains both | Run both |
| Integration / hardening phase | Check the phase's task done-when clauses — they define their own verification |

If the quality gate fails:
1. Report which check failed and the output
2. Fix the issue (staying within the scope of this phase)
3. Re-run the quality gate
4. Do NOT close the epic until the gate passes

### 6. Close the Phase and Sync

Once all tasks are complete and the quality gate passes:

```bash
bd close <epic-id>
bd sync
git add .beads/
git commit -m "chore({FEATURE_SLUG}): complete Phase N [{epic-id}]

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
git push
```

Verify push succeeded. If it fails (remote diverged), pull --rebase and push again.

### 7. Report and Hand Off

Output a completion summary:

```
Phase N complete: <Title> [{epic-id}]
Feature: {FEATURE_SLUG}

Tasks completed: X
  ✓ <task title> [<id>]   — <one-line summary of what was done>
  ✓ <task title> [<id>]
  ...

Quality gate: passed (uv run pytest: X passed / terraform validate: ok)

Committed and pushed: {FEATURE_SLUG} Phase N

Next:
  Unblocked by this phase: <next phase title> [<id>]
  Run `/implement` to continue, or `bd show <next-epic-id>` to review.
```

If `--all` was specified and another phase is now ready, proceed to it automatically. Otherwise stop.

## Handling Interruptions and Partial Progress

If the skill is invoked on a phase that is partially complete (some tasks closed, some open):

1. Report the current state: "Phase N is X% complete — Y tasks done, Z remaining."
2. Skip all closed tasks.
3. Resume from the first open/in_progress task in dependency order.
4. Run the full quality gate at the end regardless of how many tasks were skipped.

## Scope Discipline

The skill must stay within the phase it was asked to implement:
- Do not implement tasks from other phases even if they seem related
- Do not refactor code outside the task's stated file scope
- Do not add features or generalize beyond the "Done when" clause
- If a task description references a decision in the spec as background context only, do not act on that decision unless the task explicitly says to

If you discover that a task is blocked by something outside the phase (a missing dependency, a design gap), create a bead to track it:
```bash
bd create --type bug --title "Blocking issue: <description>" --description "Discovered while implementing {task-id}. ..."
```
Then surface it to the user rather than working around it silently.

## Design Principles

- **Bead-driven**: The bead is the source of truth. Task descriptions (written by beadify) contain everything needed — feature anchor, spec paths, file scope, done-when. The skill trusts and follows them.
- **Commit granularity**: One commit per task. This makes git history readable and rollback surgical.
- **Verify before closing**: The "Done when" clause is not a suggestion. Never close a task without confirming it passes.
- **Parallel when safe**: Independent tasks run concurrently via subagents. Dependency order is always respected.
- **Fail loudly**: If a task fails or a quality gate doesn't pass, stop and surface the issue. Do not continue to dependent tasks or close the phase.
- **Scope discipline**: Implement exactly what the task says — no more, no less.
