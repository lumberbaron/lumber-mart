---
name: beadify
description: Convert spec-kit artifacts (plan.md, spec.md) into beads for tracking implementation. Use when asked to generate beads, create tasks from specs, decompose a feature into work items, or convert specifications into trackable work.
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Argument Parsing

Parse `$ARGUMENTS` for:
- **Spec folder name**: If provided (e.g., `001-user-auth`), use that spec instead of deriving from branch
- **`--dry-run`**: Preview what would be created without actually creating beads
- **`--force`**: Create beads even if duplicates are detected (skip duplicate check)
- **Refinement instructions**: If existing phase epics are detected and arguments are present (but not `--dry-run` or `--force` alone), treat the arguments as a modification request (see Iterative Refinement)

## Outline

### 1. Validate Prerequisites

Run prerequisite checks:

```bash
./.specify/scripts/bash/check-prerequisites.sh --json
```

Parse the JSON response to get `FEATURE_DIR` (e.g., `specs/002-realtime-gateway`).

Then verify beads is initialized:

```bash
bd info
```

> [!CAUTION]
> ERROR if beads is not initialized. Instruct user to run `bd onboard` first.
> ERROR if plan.md or spec.md is missing. Instruct user to create specs first.

If a spec folder name was provided in arguments, override `FEATURE_DIR` to `specs/<folder-name>`.

**Derive `FEATURE_SLUG`** from the last path component of `FEATURE_DIR`:
- `specs/002-realtime-gateway` → `FEATURE_SLUG = 002-realtime-gateway`
- `specs/001-user-auth` → `FEATURE_SLUG = 001-user-auth`

Both `FEATURE_DIR` and `FEATURE_SLUG` are used throughout bead creation to anchor every bead to its feature. Never use bare filenames like `plan.md` in bead descriptions — always use the full path from repo root.

### 2. Load Context Documents

Read from `FEATURE_DIR` and build a **doc index** of full paths from repo root:

| Key | Path | Required |
|-----|------|----------|
| `PLAN` | `{FEATURE_DIR}/plan.md` | Yes |
| `SPEC` | `{FEATURE_DIR}/spec.md` | Yes |
| `DATA_MODEL` | `{FEATURE_DIR}/data-model.md` | If present |
| `CONTRACTS` | `{FEATURE_DIR}/contracts/` | If present |
| `RESEARCH` | `{FEATURE_DIR}/research.md` | If present |

Note which optional documents are present — decomposition uses all available documents. Use only these full paths when writing bead descriptions, never bare filenames.

### 3. Check for Existing Beads

#### Fresh Run (no existing phase epics, or `--force`)

Proceed to step 4 (Decomposition).

#### Existing Phase Epics Found (no `--force`)

Search for existing phase epics:

```bash
bd list --type epic --status=all
```

Filter to epics whose title matches `Phase N:`.

If existing phase epics are found:

- **If `$ARGUMENTS` contains refinement instructions**: Enter Iterative Refinement mode (step 7)
- **If `$ARGUMENTS` is empty** (or only contains a spec folder name): Warn the user and ask whether to:
  1. Show the current implementation plan (read-only)
  2. Recreate from scratch (equivalent to `--force`)
  3. Provide refinement instructions

### 4. Decomposition

Extract implementation structure from the design artifacts.

#### 4a. Extract from plan.md
- Tech stack and dependencies
- Project directory structure
- Build/deployment configuration

#### 4b. Extract from spec.md
- User stories with priorities (P1, P2, P3, etc.)
- Acceptance criteria for each story
- Edge cases and constraints

#### 4c. Extract from data-model.md (if present)
- Entities and their attributes
- Relationships between entities
- Map entities to user stories — shared entities become foundational phase tasks

#### 4d. Extract from contracts/ (if present)
- API endpoints and schemas
- Map endpoints to user stories they serve

#### 4e. Extract from research.md (if present)
- Setup decisions (tooling choices, infrastructure)
- Extract as infrastructure/setup tasks

### 5. Create Phase Epics and Task Beads

#### Phase Structure → Epics

- **Phase 1: Setup** — project init, dependencies, tooling (P1 epic)
- **Phase 2: Foundational** — blocking prereqs: DB, API framework, core models (P1 epic)
- **Phase 3+: User Stories** — one phase per story in priority order (priority from spec.md)
- **Final: Polish** — cross-cutting concerns (P3 epic)

For each phase, create an epic bead:

```bash
bd create --type epic \
  --title "Phase N: <Title>" \
  --description "<description>" \
  --priority <1-3>
```

**Priority mapping for epics**:
- Setup/Foundational phases: P1
- User Story phases: match user story priority from spec.md
- Polish phase: P3

#### Epic Description Format

Every epic description MUST open with a feature header block, then a narrative body:

```
Feature: {FEATURE_SLUG}
Plan: {FEATURE_DIR}/plan.md §<Exact phase section heading>
Covers: {FEATURE_DIR}/spec.md §<User Story N — Title> [, §<User Story M — Title>]

<2–4 sentences: what this phase achieves, why it exists in this order, and what is
observable/true when the phase is complete. Name the key files or subsystems produced.>
```

Example:
```
Feature: 002-realtime-gateway
Plan: specs/002-realtime-gateway/plan.md §Phase 1: Database Trigger + Notification Listener
Covers: specs/002-realtime-gateway/spec.md §User Story 2 — Real-Time Catalog Notifications

Creates the PostgreSQL trigger that fires on catalog table changes and the EC2 notification
listener that receives those events and pushes them to connected WebSocket clients via
post_to_connection(). Also includes the lightweight auth service JWT decoder needed by the
REST gateway. Phase complete when catalog writes produce WebSocket notifications in the dev
environment with mocked DynamoDB.
```

For phases that span multiple user stories (e.g., Foundational blocks all of them), list all covered stories in `Covers:`. For Setup phases with no direct user story, write `Covers: all stories (prerequisite)`.

**Epic description quality rules**:

1. **Full paths only**: All document references use `{FEATURE_DIR}/filename.md §Section` — never bare `plan.md` or `data-model.md`.
2. **Observable completion**: The narrative must describe a concrete, verifiable end state — not just "implement X" but "what is true when this phase is done."
3. **No implementation detail**: Epics describe the goal and scope; tasks describe the how. Epics should be readable in 10 seconds by someone doing triage.

#### Task Beads (children of phase epics)

For each task within a phase, create a task bead with the phase epic as parent:

```bash
bd create --type task \
  --parent <phase-epic-id> \
  --title "<Actionable description>" \
  --description "<full description>" \
  --priority <priority>
```

Each task bead:
- **Title**: Actionable description (e.g., "Implement product search with multi-criteria filtering")
- **Description**: Compose using the rules below. Must include: what to do, exact file path(s), feature anchor, source spec reference, and a "Done when" clause.
- **Priority**: Inherited from parent phase/story priority
- No T### IDs (beads have native IDs)
- No [P] markers (tasks without `bd dep` are implicitly parallel)

**Task description quality rules**:

1. **Feature anchor + full paths**: Open every task description with `Feature: {FEATURE_SLUG}` on its own line, then use full repo-root paths for all document references — e.g., `specs/002-realtime-gateway/data-model.md §Trigger Function` or `specs/002-realtime-gateway/plan.md §Phase 2 step 1`. Never write bare `plan.md §...` or `data-model.md §...` — a fresh agent reading the bead in isolation must be able to open the right file immediately.

2. **Shared-file scope boundary**: If two tasks in the same phase touch the same file, each description must include a sentence explicitly bounding its scope — e.g., *"This task writes the SQL migration file; task .2 wires it into the Lambda entrypoint."*

3. **Inline over reference for short content**: Before adding a spec reference, check whether the referenced content is substantively longer than the task description. If the plan step is ≤ 2 sentences and already captured in the description, omit the reference — it adds noise. Only include references when the target section has detail the implementor will genuinely need.

4. **Done when clause**: End every description with: `Done when: <specific verifiable outcome>` — e.g., *"Done when: trigger fires on INSERT to wine_cellar and the pg_notify payload matches specs/002-realtime-gateway/data-model.md §Trigger Payload."*

5. **Cross-task handoff notes**: For tasks within a phase that are sequential (one task's output is another's input), add a handoff note to both descriptions. Upstream task: `Produces: <artifact path or name>`. Downstream task: `Consumes output of task .<N>: <artifact>`. Also wire `bd dep add` between them (see Step 6).

**Priority mapping for tasks**:
- Tasks in Setup/Foundational phases: P1
- Tasks for high-priority user stories (P1, P2 in spec.md): P1
- Tasks for medium-priority user stories (P3, P4): P2
- Tasks for lower-priority user stories: P3
- Polish tasks: P3

### 6. Set Dependencies

After all phases are created, establish dependencies:

```bash
# Foundational depends on Setup
bd dep add <foundational-id> <setup-id>

# Each user story phase depends on Foundational
bd dep add <story-phase-id> <foundational-id>

# Polish depends on all story phases
bd dep add <polish-id> <story-phase-id>
```

**Dependency rules**:
- Setup blocks Foundational
- Foundational blocks all user story phases
- User story phases can run in parallel after Foundational
- Polish depends on all story phases
- Within phases: set explicit deps where one task needs another's output (e.g., models before services). When you do, add cross-task handoff notes to both task descriptions (see Task description quality rules above).

### 7. Iterative Refinement

If existing phase epics are detected and the user provides refinement instructions:

1. Load existing beads (phase epics + children via epic-walk using `bd show <epic-id>` for each phase)
2. Interpret `$ARGUMENTS` as a modification request (e.g., "split auth into its own phase", "add caching tasks to phase 2", "remove the polish phase")
3. Output the updated implementation plan showing changes (additions, removals, moves)
4. Apply changes: create new beads, update existing ones, set/remove dependencies as needed
5. When updating existing bead descriptions, ensure the feature header block is present — add it if missing

### 8. Output Implementation Plan

Every beadify invocation (including `--dry-run`) outputs a formatted implementation plan:

```
Implementation Plan: {FEATURE_SLUG}
Spec: {FEATURE_DIR}/spec.md
Plan: {FEATURE_DIR}/plan.md
=====================================

Phase 1: Setup (P1)
  1. Create project structure with api/, scrapers/, infra/ directories
  2. Initialize Go module with gqlgen, pgx dependencies  [api/go.mod]
  3. Initialize Node.js project with Playwright deps     [scrapers/package.json]
  ...

Phase 2: Foundational (P1) — blocks all user stories
  1. Create database migrations for extensions, retailers, products, stores, stock
  2. Set up GraphQL server with gqlgen                    [api/internal/graph/]
  3. Create base repository layer                         [api/internal/repository/base.go]
  ...

Phase 3: US1 — Search Products by Attributes (P1)
  1. Implement multi-criteria product search               [api/internal/repository/product.go]
  2. Implement trigram text search for product name         [api/internal/repository/product.go]
  ...

Phase N: Polish (P3) — after all stories complete
  ...

Dependencies: Setup → Foundational → [US1, US2, US3 in parallel] → Polish
Epics: N | Tasks: M | Ready to start: K
```

In normal mode, beads are created and the plan is shown.
In `--dry-run` mode, only the plan is shown (no beads created).

### 9. Report Summary

After the implementation plan, output a creation summary:

```
Created beads from {FEATURE_DIR}:

Epics: N (Phase 1-N)
  - Phase 1: Setup → <bead-id>
  - Phase 2: Foundational → <bead-id>
  ...

Tasks: M total
  - Created: X
  - Skipped (duplicates): Y

Dependencies established:
  - Setup → Foundational → User story phases
  - User story phases → Polish

Next steps:
  - Run `bd ready` to see available work
  - Run `bd show <epic-id>` to see tasks in a phase
  - Spec: {FEATURE_DIR}/spec.md | Plan: {FEATURE_DIR}/plan.md
```

In `--dry-run` mode, prefix with:
```
DRY RUN - No beads were created. The following would be created:
```

## Duplicate Detection (skip if `--force`)

Before creating each phase epic or task bead, check for existing matches:

```bash
# Check for phase epics
bd list --type epic --status=all 2>/dev/null | grep -c "Phase [0-9]" || echo "0"

# Check for task beads by title similarity
bd search "<task title fragment>" 2>/dev/null || true
```

If duplicates found:
- In `--dry-run` mode: Report what would be skipped
- Otherwise: Warn user and ask whether to continue, skip duplicates, or abort

## Error Handling

- If `bd create` fails, report the error and continue with remaining items
- Track failures and include in summary: `Failed: N (see errors above)`
- If all phase epic creations fail, abort (cannot create child tasks without parents)

## Design Principles

- **Spec-direct**: Reads plan.md and spec.md directly — no intermediate tasks.md file
- **Beads-native**: Uses bead IDs, dependencies, and epic hierarchy natively
- **Context-complete**: Every bead (epic or task) is self-contained — a fresh agent reading it with only `bd show <id>` has everything needed to find the feature, locate the design docs, and understand the scope. Feature slug and full spec paths are mandatory, not optional.
- **Iterable**: Run once for initial decomposition, run again with instructions to refine
- **Readable output**: Always produces a formatted implementation plan for human review
- **Idempotent**: Duplicate detection prevents accidental double-creation (default)
