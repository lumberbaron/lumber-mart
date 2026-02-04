---
name: sb:review-spec
description: Validate implementation against spec-kit artifacts (spec.md, plan.md, constitution.md). Use when asked to check spec conformance, validate implementation matches specs, or audit code against specifications.
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
- **`--create-beads`**: Create beads for findings (default: report only)

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
> ERROR if spec.md is missing. Instruct user to run `/speckit.spec` first.

If a spec folder name was provided in arguments, override `FEATURE_DIR` to `specs/<folder-name>`.

### 2. Load Context Documents

Read from `FEATURE_DIR`:
- **Required**: `spec.md`
- **Optional**: `plan.md`, `.specify/memory/constitution.md`

Note which optional documents are present — validation criteria are gated on document availability.

### 3. Read Implementation Code

If a path argument was provided, scope to that path. Otherwise, read the project's source code (excluding vendor, node_modules, build output, and other generated directories).

Build a working understanding of the implementation: files, modules, public APIs, imports, configuration, and test files.

### 4. Validation

Run each applicable validation section below. Skip sections whose required documents are not present.

**Status Definitions** (use consistently throughout):
- ✅ PASS: Fully implemented as specified
- ⚠️ PARTIAL: Implemented but with minor deviations from spec
- ❌ GAP: Missing or significantly divergent

**Evidence Format** (mandatory): `file:line - brief explanation`

#### 4.1 Specification Conformance (requires spec.md)

Extract ALL functional requirements and acceptance criteria from spec.md. Create a table row for EACH item—do not summarize or skip any.

**Functional Requirements**: Scan spec.md for all FR-xxx identifiers or numbered requirements. For each:
- Compare the implementation against the requirement
- Evaluate: behavior coverage, edge case handling, constraint enforcement, API surface match
- Record status and evidence

**Acceptance Criteria**: Scan spec.md for all user stories (USx-x format) and their scenarios. For each scenario:
- Verify the described behavior is implemented
- Record status and notes

#### 4.2 Architecture Consistency (requires plan.md)

Extract ALL architectural declarations from plan.md. This includes:
- Module/package structure
- Naming conventions
- Technology choices (frameworks, libraries, databases)
- Configuration patterns
- External integrations

Create a table row for EACH declaration. Evaluate:
- Does the code use the declared frameworks/libraries? (check imports, config files, dependency manifests)
- Is code organized per the declared directory structure?
- Do external service integrations match the plan?
- Does the data layer match (database driver, ORM, migration tool)?

#### 4.3 Constitution Alignment (requires constitution.md)

For EACH numbered principle in constitution.md, create a table row and evaluate whether the code adheres to it. Common principle categories:
- API design standards
- Security requirements
- Infrastructure-as-code requirements
- Testing standards
- Code organization conventions

Only flag cases where code clearly contradicts a stated principle. Do not flag ambiguous or inapplicable cases.

### 5. Deduplication

Before creating beads, check for existing ones:

- Run `bd list --status=open` to see all open issues
- Compare findings against existing bead titles and descriptions
- Skip creating beads for issues that already have matching open beads

### 6. Report Format (Mandatory)

You MUST produce a report following this exact structure. This format is required for every review—do not deviate.

**Table Format**: Use markdown tables (pipe-delimited) for ALL tables. Do not use ASCII box-drawing characters or other formats.

```
---
Spec Review for specs/<feature-name>

Documents Reviewed
- spec.md: Yes
- plan.md: Yes | Not found
- constitution.md: Yes | Not found

---
## 4.1 Specification Conformance Analysis

### Functional Requirements vs Implementation

| FR | Requirement | Status | Evidence |
|----|-------------|--------|----------|
| FR-001 | <text from spec> | ✅ PASS | file.tf:42 - <explanation> |
| FR-002 | <text from spec> | ⚠️ PARTIAL | file.ts:100 - <explanation> |
| FR-003 | <text from spec> | ❌ GAP | Not implemented |

### Acceptance Criteria Coverage

| User Story | Scenario | Status | Notes |
|------------|----------|--------|-------|
| US1-1 | <scenario text> | ✅ | <notes> |
| US1-2 | <scenario text> | ⚠️ | <notes> |

---
## 4.2 Architecture Consistency (plan.md)

| Plan Declaration | Status | Evidence |
|------------------|--------|----------|
| <declaration> | ✅ | file:line - <explanation> |

(Skip this section if plan.md not found)

---
## 4.3 Constitution Alignment

| Principle | Status | Notes |
|-----------|--------|-------|
| I. <Principle Name> | ✅ PASS | <explanation> |
| II. <Principle Name> | ✅ PASS | <explanation> |

(Skip this section if constitution.md not found)

---
## Summary

| Category | Issues Found |
|----------|--------------|
| Specification conformance | N |
| Architecture consistency | N |
| Constitution alignment | N |
| **Total** | **N** |

(or "No issues found" if all items passed)

---
## Findings

(Only include this section if there are issues. Insert a blank line between each finding for readability.)

1. **FR-002 / US1-2**: <Short title>

   <Prose explanation: what the spec requires, what the implementation does, why it's a gap/partial>

2. **FR-014 / US3-3**: <Short title>

   <Prose explanation>

---
To create beads for these findings, re-run with --create-beads
```

**Important**: The "Findings" section provides detailed prose explanations for each non-passing item. Reference the FR/US codes from the tables above for traceability. Always include a blank line between findings.

### 7. Bead Creation (`--create-beads` mode)

When `--create-beads` is specified, create beads for each finding:

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

After creating beads, append to the report:

```
## Beads Created

- <bead-id>: "<title>"
- ...
```

Omit the "To create beads..." footer when beads have been created.

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
