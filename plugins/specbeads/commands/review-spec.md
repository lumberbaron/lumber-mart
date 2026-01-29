---
description: Validate that implementation matches spec-kit artifacts (spec.md, plan.md, constitution.md). Creates bug beads for spec violations found.
---

# Spec Review

Validate that the implementation conforms to its spec-kit artifacts.

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Argument Parsing

Parse `$ARGUMENTS` for:
- **Path**: Optional path to focus the review (default: entire repo)
- **Spec folder name**: If provided (e.g., `001-user-auth`), use that spec instead of deriving from branch
- **`--dry-run`**: List findings without creating beads

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
> ERROR if spec.md is missing. Instruct user to run `/speckit.spec` first.

If a spec folder name was provided in arguments, override `FEATURE_DIR` to `specs/<folder-name>`.

### 2. Load Context Documents

Read from `FEATURE_DIR`:
- **Required**: `spec.md`
- **Optional**: `plan.md`, `tasks.md`, `.specify/memory/constitution.md`

Note which optional documents are present — validation criteria are gated on document availability.

### 3. Read Implementation Code

If a path argument was provided, scope to that path. Otherwise, read the project's source code (excluding vendor, node_modules, build output, and other generated directories).

Build a working understanding of the implementation: files, modules, public APIs, imports, configuration, and test files.

### 4. Validation

Run each applicable validation section below. Skip sections whose required documents are not present.

#### 4.1 Specification Conformance (requires spec.md)

Compare the implementation against spec.md:

- **Behavior coverage**: Are behaviors described in spec.md implemented in code?
- **Edge case handling**: Are edge cases listed in the spec handled?
- **Constraint enforcement**: Are constraints from the spec enforced (validation rules, limits, error conditions)?
- **API surface**: Do public API signatures match spec descriptions (endpoints, function signatures, data shapes)?

For each gap, record the spec section and what is missing or divergent.

#### 4.2 Architecture Consistency (requires plan.md)

Compare the implementation against plan.md architectural decisions:

- **Frameworks and libraries**: Does the code use the declared frameworks/libraries? (check imports, config files, dependency manifests)
- **Directory structure**: Is code organized per the declared directory structure?
- **External integrations**: Do external service integrations match the plan (client libraries, API patterns)?
- **Data layer**: Does the data layer match (database driver, ORM, migration tool)?

For each mismatch, record the plan.md declaration and the actual implementation.

#### 4.3 Constitution Alignment (requires constitution.md)

For each principle declared in the project's constitution, evaluate whether the code in scope adheres to it:

- API design standards
- Security requirements
- Infrastructure-as-code requirements
- Testing standards
- Code organization conventions

Only flag cases where code clearly contradicts a stated principle. Do not flag ambiguous or inapplicable cases.

#### 4.4 Acceptance Criteria Coverage (requires spec.md + test files in scope)

Check that acceptance criteria from spec.md are tested:

- Does each user story / acceptance criterion have a corresponding test?
- Are error scenarios from the spec tested?
- Are boundary conditions from the spec tested?

#### 4.5 Task Completion Validation (requires tasks.md)

For tasks marked `[x]` in tasks.md:

- Do the referenced files exist and contain meaningful implementations?
- Are there completed tasks whose implementations appear incomplete or stubbed?

### 5. Deduplication

Before creating beads, check for existing ones:

- Run `bd list --status=open` to see all open issues
- Compare findings against existing bead titles and descriptions
- Skip creating beads for issues that already have matching open beads

### 6. Output

For each finding: note the source document, the violated section/principle, the relevant code location, and a brief explanation.

**Normal mode**: Create beads for findings:

```bash
bd create --type=bug --priority=<1-3> \
  --title="Spec: <issue>" \
  --description="**Source**: <spec.md|plan.md|constitution.md>
**Violated**: <quote from source>
**Code**: <file:line>
<explanation>"
```

**Priority mapping**:
- Missing core behavior from spec: P1
- Architecture divergence from plan: P2
- Constitution violations: P2
- Missing acceptance test coverage: P2
- Incomplete task implementations: P3

**Dry-run mode**: List findings in a table format without creating beads:

| Source | Section | Code Location | Issue | Would Create |
|--------|---------|---------------|-------|--------------|
| spec.md | US1 | src/auth.ts:42 | Description | `bd create --type=bug ...` |

### 7. Report Summary

Output a summary:

```
Spec Review for specs/<feature>
================================

## Documents Reviewed

- spec.md: Yes
- plan.md: <Yes | Not found>
- constitution.md: <Yes | Not found>
- tasks.md: <Yes | Not found>

## Findings

| Category | Issues Found |
|----------|-------------|
| Specification conformance | <N> |
| Architecture consistency | <N> |
| Constitution alignment | <N> |
| Acceptance criteria coverage | <N> |
| Task completion validation | <N> |
| **Total** | **<N>** |

## Beads Created

- <bead-id>: "<title>"
- ...

(or "No issues found" if clean)
```

In `--dry-run` mode, prefix with:
```
DRY RUN - No beads were created. The following would be created:
```

## Error Handling

- If `bd` commands fail, report the error and continue with remaining findings
- If spec.md cannot be read, abort (it is the only hard requirement)
- Missing optional documents skip their corresponding validation sections silently

## Design Principles

- **Spec-aware**: This command reads and understands spec-kit artifacts, unlike the generic review commands
- **Code-level validation**: Evaluates actual code against specs, not just file existence or build output
- **Gated sections**: Each validation section is gated on its required document being present
- **Non-destructive**: Creates bug beads for findings, never modifies source code or spec artifacts
- **Focused scope**: Validates spec conformance only — use `review-code`, `review-tests`, `review-docs` for generic quality
