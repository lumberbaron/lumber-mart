---
description: Convert tasks from tasks.md into beads (epics and task beads) for tracking implementation work.
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
- **`--skip-completed`**: Skip creation of beads for tasks already marked `[x]` in tasks.md
- **`--force`**: Create beads even if duplicates are detected (skip duplicate check)

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

### 3. Parse tasks.md

Extract the following structure:

**Phases**: Lines matching `## Phase N: Title`
- Extract phase number and title
- Extract purpose from `**Purpose**:` text following the heading
- Extract checkpoint from `**Checkpoint**:` text (usually at end of phase)

**Tasks**: Lines matching `- [x| ] T### [P?] [US#?] Description`
- `[x]` = completed, `[ ]` = pending
- `T###` = task ID (e.g., T001, T042)
- `[P]` marker = parallelizable
- `[US#]` marker = implements user story (e.g., [US1])
- Description includes the rest of the line

Example task line:
```
- [x] T026 [US1] Implement user authentication with JWT tokens in internal/auth/handler.go
```

### 4. Check for Existing Beads (Skip if `--force`)

Search for existing beads to avoid duplicates:

```bash
# Check for phase epics
bd list --type epic 2>/dev/null | grep -c "Phase [0-9]" || echo "0"

# Check for task beads (sample check)
bd search "T001:" 2>/dev/null || true
```

If existing phase epics or task beads are found:
- In `--dry-run` mode: Report what would be skipped
- Otherwise: Warn user and ask whether to continue, skip duplicates, or abort

### 5. Create Epic Beads for Phases

For each phase extracted from tasks.md, create an epic bead:

```bash
bd create --type epic \
  --title "Phase N: <Title>" \
  --description "<description>" \
  --priority 2
```

**Description template** for phases:
```
<Purpose from tasks.md>

**Source**: specs/<feature>/tasks.md Phase N
**Checkpoint**: <Checkpoint text from tasks.md>
```

**Priority mapping**:
- Setup/Foundational phases: P1
- User Story phases: Match user story priority from spec.md
- Infrastructure/Integration phases: P2
- Polish/Cleanup phases: P3

Store the created epic ID for use as parent when creating task beads.

### 6. Create Task Beads as Children

For each task in the phase, create a task bead with the phase epic as parent:

```bash
bd create --type task \
  --parent <phase-epic-id> \
  --title "T###: <Description (truncated to 80 chars)>" \
  --description "<full description>" \
  --priority <priority>
```

**Title format**: `"T008: Create database connection module"` (per CLAUDE.md convention)

**Description template** for tasks:
```
<Full task description from tasks.md>

**Source**: specs/<feature>/tasks.md Phase N
**File path**: <extracted path from description, e.g., internal/db/connect.go>
**Implements**: <US# reference if present, linked to spec.md>
**Parallelizable**: <Yes if [P] marker present, No otherwise>

**Constitution alignment**: <relevant principle based on task content>
```

**Constitution Principle Mapping** (auto-detect based on task keywords):

If the project has a constitution file (`.specify/memory/constitution.md`), map task keywords to relevant principles. Example mappings:

| Task Pattern | Principle Example |
|--------------|-------------------|
| auth, login, session, JWT, OAuth | Security & Authentication |
| API, endpoint, REST, GraphQL | API Design |
| terraform, AWS, infrastructure, deploy | Infrastructure-as-Code |
| test, spec, coverage, mock | Testing Standards |
| database, migration, schema | Data Management |
| cache, performance, optimization | Performance |

Adapt mappings based on the actual principles defined in the project's constitution.

**Priority mapping**:
- Tasks in early phases (Setup/Foundational): P1 (blocking)
- Tasks with high-priority user stories [US1], [US2]: P1
- Tasks with medium-priority user stories [US3], [US4]: P2
- Tasks with lower-priority user stories: P3
- Infrastructure/integration tasks: P2
- Polish/cleanup tasks: P3

### 7. Handle Completed Tasks

For tasks marked `[x]` in tasks.md:

- **Default behavior**: Create the bead, then immediately close it with `bd close <id>`
- **With `--skip-completed`**: Do not create beads for completed tasks at all

This maintains full history while showing current state.

### 8. Set Phase Dependencies

After all phases are created, set up sequential blocking dependencies:

```bash
# Phase 2 blocks Phase 3 (foundational blocks user stories)
bd dep add <phase-3-id> <phase-2-id>

# Each phase blocks the next
bd dep add <phase-4-id> <phase-3-id>
# ... and so on
```

Special dependency rules (derive from tasks.md structure):
- Foundational phases BLOCK all feature/user story phases
- Infrastructure phases typically depend only on foundational phases
- Integration phases may depend only on foundational phases
- Final polish/cleanup phases depend on all feature phases

### 9. Report Summary

Output a summary of what was created:

```
Created beads from specs/<feature>/tasks.md:

Epics: N (Phase 1-N)
  - Phase 1: Setup → beads-abc
  - Phase 2: Foundational → beads-def
  ...

Tasks: M total
  - Created (open): X
  - Created (closed): Y
  - Skipped (duplicates): Z

Dependencies established:
  - Phase 1 → Phase 2 → Feature phases
  - Foundational → Infrastructure phases
  - Feature phases → Polish phase

Next steps:
  - Run `bd ready` to see available work
  - Run `bd show <epic-id>` to see tasks in a phase
```

In `--dry-run` mode, prefix with:
```
DRY RUN - No beads were created. The following would be created:
```

## Error Handling

- If `bd create` fails, report the error and continue with remaining items
- Track failures and include in summary: `Failed: N (see errors above)`
- If all phase epic creations fail, abort (cannot create child tasks without parents)

## Notes

- This command is idempotent when using duplicate detection (default)
- Use `--force` to recreate beads even if they exist
- Task IDs (T001, T002, etc.) are preserved in bead titles for cross-referencing
- Phase epic IDs are stored temporarily during execution to set as parent for tasks
