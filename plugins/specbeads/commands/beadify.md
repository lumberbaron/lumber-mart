---
description: Decompose spec-kit design artifacts (plan.md, spec.md) directly into beads for tracking implementation work.
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

Parse the JSON response to get `FEATURE_DIR`.

Then verify beads is initialized:

```bash
bd info
```

> [!CAUTION]
> ERROR if beads is not initialized. Instruct user to run `bd onboard` first.
> ERROR if plan.md or spec.md is missing. Instruct user to create specs first.

If a spec folder name was provided in arguments, override `FEATURE_DIR` to `specs/<folder-name>`.

### 2. Load Context Documents

Read from `FEATURE_DIR`:
- **Required**: `plan.md` (tech stack, project structure), `spec.md` (user stories with priorities)
- **Optional**: `data-model.md` (entities), `contracts/` (API schemas), `research.md` (decisions)

Note which optional documents are present — decomposition uses all available documents.

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
- **Description**: What to do, exact file path, user story reference, source spec reference
- **Priority**: Inherited from parent phase/story priority
- No T### IDs (beads have native IDs)
- No [P] markers (tasks without `bd dep` are implicitly parallel)

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
- Within phases: set explicit deps where one task needs another's output (e.g., models before services)

### 7. Iterative Refinement

If existing phase epics are detected and the user provides refinement instructions:

1. Load existing beads (phase epics + children via epic-walk using `bd show <epic-id>` for each phase)
2. Interpret `$ARGUMENTS` as a modification request (e.g., "split auth into its own phase", "add caching tasks to phase 2", "remove the polish phase")
3. Output the updated implementation plan showing changes (additions, removals, moves)
4. Apply changes: create new beads, update existing ones, set/remove dependencies as needed

### 8. Output Implementation Plan

Every beadify invocation (including `--dry-run`) outputs a formatted implementation plan:

```
Implementation Plan: <feature name>
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
Created beads from specs/<feature>:

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
- **Iterable**: Run once for initial decomposition, run again with instructions to refine
- **Readable output**: Always produces a formatted implementation plan for human review
- **Idempotent**: Duplicate detection prevents accidental double-creation (default)
