---
name: implement-team
description: Implement an entire spec-kit feature using an agent team. Spawns a worker that loops on the bead task list and a code-reviewer that continuously files review findings as new beads. The team is self-coordinating — the lead monitors and handles the final sync. Use when asked to implement a feature with a team, run a team implementation, or set up agents to implement a feature autonomously.
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Argument Parsing

Parse `$ARGUMENTS` for:
- **Feature slug** (e.g., `002-realtime-gateway`): Target feature — **required**. If not provided, ask the user before proceeding.
- **`--dry-run`**: Show what team would be created and which phases targeted, without spawning anything
- **`--workers N`**: Spawn N worker teammates (default: 1). Use 2+ only when phases have many parallel tasks with no file conflicts
- **Additional reviewers**: e.g., `--review-spec`, `--review-tests`, `--review-docs` — spawn additional reviewer teammates running those skills alongside the code reviewer
- **Additional instructions**: Any other text is passed as guidance to worker teammates

## Prerequisites

Agent teams must be enabled:
```json
// settings.json
{ "env": { "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1" } }
```

Check before proceeding:
```bash
bd info
```

If beads is not initialized, stop and instruct the user to run `bd onboard`.

## Outline

### 1. Resolve the Feature

```bash
bd list --type epic --status=open
```

Filter to epics whose description contains `Feature: {FEATURE_SLUG}`. These are the **target epics** for this run — all open phases for the feature.

If no open epics are found for the feature slug, stop: "No open phases found for {FEATURE_SLUG}. Run `bd list --type epic --status=all` to check."

From the first epic's description, parse the **feature header block**:
```
Feature: {FEATURE_SLUG}
Plan: {FEATURE_DIR}/plan.md §<phase section>
Covers: {FEATURE_DIR}/spec.md §<user story>
```

Extract `FEATURE_DIR`. Read `{FEATURE_DIR}/plan.md` briefly for context on what files and subsystems this feature touches — this informs the reviewer's scope.

Output a pre-flight summary:
```
Feature: {FEATURE_SLUG}
Spec:    {FEATURE_DIR}/spec.md
Plan:    {FEATURE_DIR}/plan.md

Target phases:
  Phase N: <title> [<epic-id>]  — X tasks open
  Phase M: <title> [<epic-id>]  — blocked by Phase N
  ...

Team to spawn:
  worker (Sonnet)        — loops on bd ready, implements tasks
  code-reviewer (Sonnet) — continuous review, files P1/P2 beads
  [additional reviewers if requested]
```

Stop here in `--dry-run` mode.

### 2. Create the Team

```bash
TeamCreate team_name="{FEATURE_SLUG}-impl"
```

### 3. Spawn Teammates

#### Worker (spawn 1, or N if `--workers N`)

Each worker receives this prompt:

---

```
You are a worker agent implementing the feature "{FEATURE_SLUG}".

Your loop — repeat until you decide to shut down:

STEP 1: Find work
  Run: bd ready
  From the results, filter to tasks whose description contains "Feature: {FEATURE_SLUG}".

  If no matching tasks are ready:
    Wait ~30 seconds and try again. After 3 consecutive empty checks, approve a
    shutdown request for yourself (the lead will request it when the time comes,
    or you can initiate if the lead is unresponsive).

STEP 2: Claim the highest-priority ready task
  bd update <task-id> --status=in_progress

STEP 3: Read the task
  bd show <task-id>
  The description contains: feature anchor, full repo-root paths to spec sections,
  exact file paths to create or modify, scope boundaries, cross-task handoff notes,
  and a "Done when" clause. Read any spec sections it cites that have detail beyond
  what the description captures.

STEP 4: Implement
  Stay strictly within the stated file scope. The description says what this task
  touches — do not touch anything outside that scope, even if it seems helpful.
  If the description says "this task writes the migration file; task .2 wires it in,"
  do not wire it in.

STEP 5: Verify
  Confirm the "Done when" clause passes. Run whatever it specifies — tests,
  terraform validate, file existence checks, etc. Fix failures before proceeding.
  Do not move on with a failing done-when.

STEP 6: Commit
  git add <files changed>
  git commit -m "feat({FEATURE_SLUG}): <task title> [{task-id}]

  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"

STEP 7: Close
  bd close <task-id>

STEP 8: Phase gate check
  If the task you just closed was the last open task in its parent epic
  (check: bd show <epic-id> and count open children), run the quality gate:
    - Python files changed → uv run pytest (tests relevant to this phase)
    - Terraform files changed → terraform validate
  Fix any failures. Then notify the lead:
    "Phase <N> tasks complete and quality gate passed — ready to close epic <epic-id>."
  Do NOT close the epic yourself. The lead handles that.

STEP 9: Loop back to STEP 1

Blocking issues:
  If you discover something that blocks a task and is outside your scope,
  create a bead and notify the lead:
    bd create --type bug \
      --title "Blocking: <short description>" \
      --description "Feature: {FEATURE_SLUG}
  Discovered while implementing <task-id>.
  <Detail of the problem>

  Done when: <what needs to be true to unblock>"
  Then move on to the next ready task rather than waiting.

{ADDITIONAL_INSTRUCTIONS}
```

---

#### Code Reviewer

```
You are a continuous code reviewer for the feature "{FEATURE_SLUG}".

The spec lives at: {FEATURE_DIR}/
The source files for this feature are those created or modified by the phases:
  {list each epic title and its Plan: section path, from the target epics}

Your loop — repeat until you decide to shut down:

STEP 1: Identify what to review
  Run: git log --oneline -20
  Focus your review on files changed in recent commits. On the first pass,
  review the full set of files the feature plan says will be created.

STEP 2: Review
  Apply these lenses — look for problems that tests and linters won't catch:

  Design issues:
  - Single responsibility violations (a function/class doing too many things)
  - Wrong abstraction level (implementation detail leaking into interface, or
    vice versa)
  - Testability problems (hard dependencies, no injection points, untestable logic)
  - Naming that obscures intent (variables, functions, modules)

  Correctness issues:
  - Missing error handling at system boundaries (external APIs, DB calls, network)
  - Auth or security gaps (missing validation, exposed secrets, injection risk)
  - Race conditions or incorrect assumptions about ordering

  Coverage gaps:
  - Non-trivial logic with no test coverage
  - Edge cases from {FEATURE_DIR}/spec.md §Edge Cases that aren't handled

STEP 3: File beads for P1/P2 findings only
  For each finding rated P1 or P2, create one bead:
    bd create --type task \
      --title "<actionable verb phrase, e.g. 'Add error handling for GoneException in notifications.py'>" \
      --description "Feature: {FEATURE_SLUG}
  Spec: {FEATURE_DIR}/spec.md
  File: <path/to/file.py>:<line number if applicable>

  <2-3 sentences describing the issue clearly>

  Done when: <specific, verifiable fix — e.g. 'GoneException from post_to_connection() is caught, the stale DynamoDB entry is deleted, and the exception is logged at WARNING level'>" \
      --priority <1 or 2>

  Do NOT create beads for P3+ findings. Note them, but keep the task list
  focused on what matters.

  Do NOT fix anything yourself. Your job is to notice and file, not implement.

STEP 4: Check shutdown condition
  This pass created zero new P1/P2 beads.
  AND: bd list --type epic --status=open  →  filter to Feature: {FEATURE_SLUG}  →  none remain.

  If both conditions are true → you are done. Notify the lead:
    "Code review complete. Final pass found no P1/P2 issues and no open feature
    epics remain. Ready to shut down."
  Then approve your own shutdown request when the lead sends it.

  If either condition is false → loop back to STEP 1.
  Between passes, pause briefly (a few minutes) to let the worker make progress
  before you review again. This avoids filing findings about code that's already
  being fixed.
```

---

#### Additional Reviewers (if requested)

If `--review-spec` was specified, spawn a `spec-reviewer` using the same loop structure but running the `specbeads:review-spec` skill instead of the manual review criteria in Step 2 above.

If `--review-tests` was specified, spawn a `test-reviewer` running `specbeads:review-tests`.

If `--review-docs` was specified, spawn a `docs-reviewer` running `specbeads:review-docs`.

All reviewers share the same bead-creation protocol (P1/P2 only, standard description format) and the same shutdown condition.

### 4. Lead Coordination

After spawning, the lead monitors and coordinates. Do not poll manually — teammate notifications arrive automatically.

**When the worker reports a phase gate passed:**
```bash
bd close <epic-id>
```
Then check whether the next phase is now unblocked:
```bash
bd list --type epic --status=open
```
If a previously blocked phase is now ready, message the worker:
"Phase N closed. Phase N+1 [<id>] is now unblocked — continue."

**When the worker messages about a blocking bead:**
Review it. Options:
- If it's small and clearly scoped to your lead context: resolve it directly, then message the worker it's unblocked
- Otherwise: set appropriate priority and let the worker pick it up on the next `bd ready` loop

**When a reviewer creates a new P1/P2 bead while the worker is idle:**
Message the worker: "Reviewer filed a new P1 bead — loop back to bd ready."

**When both worker and reviewer have shut down:**
```bash
# Verify nothing is left
bd list --type epic --status=open
# Filter to Feature: {FEATURE_SLUG} — should be empty

# Sync and push
bd sync
git add .beads/
git commit -m "chore({FEATURE_SLUG}): team implementation complete

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
git push

# Clean up
TeamDelete
```

### 5. Shutdown Protocol

| Teammate | Shuts down when |
|----------|----------------|
| **worker** | `bd ready` returns no feature tasks after 3 consecutive checks |
| **code-reviewer** | Last pass created zero new P1/P2 beads AND no open feature epics remain |
| **other reviewers** | Same as code-reviewer |
| **lead** | All teammates shut down AND no open feature epics remain |

The lead sends explicit `shutdown_request` to each teammate once the shutdown conditions are met. Teammates approve immediately (they should already be idle at this point).

### 6. Report

After `TeamDelete`:

```
Team implementation complete: {FEATURE_SLUG}

Phases completed: N
Tasks implemented: M
Review beads filed and resolved: K

Committed and pushed.

Run `bd list --status=all` to see the full history.
```

## Design Principles

- **Self-healing loop**: The bead task list is the communication channel between worker and reviewer. The worker consumes beads; the reviewer produces them. New reviewer beads are picked up automatically on the worker's next `bd ready` — no explicit coordination needed.
- **Bead-driven**: Task descriptions written by beadify are the source of truth. Workers read and follow them; reviewers write new ones in the same format.
- **Reviewer is a ratchet, not a second implementer**: The reviewer's only job is to notice things the worker missed and file them as actionable beads. It does not fix, refactor, or implement.
- **Phase gates stay with the worker**: Quality gates run after the last task in a phase closes. The lead closes the epic. This keeps responsibilities clear.
- **Commit granularity**: One commit per task. Readable history, surgical rollback.
- **Verify before closing**: Done-when clauses are acceptance criteria, not suggestions.
- **Fail loudly**: Workers create blocking beads and notify the lead rather than working around problems silently.
