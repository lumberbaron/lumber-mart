---
name: review-skill
description: Reviews an existing Claude Code skill for conformance to best practices, checking structure, metadata, naming, descriptions, content quality, and script completeness. Use when a user wants to review a skill, audit a skill for quality, check if a skill follows conventions, or improve an existing skill's structure and content.
---

# Review Skill

## User Input

```text
$ARGUMENTS
```

The input identifies the skill to review — either a path to the skill directory (e.g., `plugins/circuits/skills/wavejson/`) or a skill name to locate.

If `$ARGUMENTS` is empty, ask the user which skill they want to review.

## Workflow

### Step 1: Locate the skill

If the user provided a skill name rather than a path, search for a matching skill directory. Confirm the path before proceeding.

### Step 2: Run automated validation

Run the validation script to catch structural and metadata issues:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/create-skill/scripts/validate-skill.py <path/to/skill-directory>
```

Record all errors and warnings.

### Step 3: Read the skill

Read SKILL.md fully, then read any bundled references, scripts, and assets. Build a complete picture of what the skill does and how it's structured.

### Step 4: Assess against best practices

Evaluate the skill against each area, using the reference files for detailed criteria:

| Area | Reference |
|------|-----------|
| Name and description quality | [../../references/naming-and-descriptions.md](../../references/naming-and-descriptions.md) |
| Content patterns and anti-patterns | [../../references/quality-patterns.md](../../references/quality-patterns.md) |
| Full quality checklist | [../../references/checklist.md](../../references/checklist.md) |

For each issue found, note the **location** (file and section), the **problem**, and a **recommendation**.

### Step 5: Produce findings report

Present findings grouped by severity:

```
Skill Review: <skill-name>
Path: <path>

## Errors (must fix)

### 1. <Issue title>
**Location:** <file:section>
<Problem description and recommendation>

## Warnings (should fix)

### 2. <Issue title>
**Location:** <file:section>
<Problem description and recommendation>

## Suggestions (consider)

### 3. <Issue title>
**Location:** <file:section>
<Problem description and recommendation>

---
N issues found: X errors, Y warnings, Z suggestions
```

- **Errors**: Violations that will cause problems (invalid metadata, missing files, broken links)
- **Warnings**: Deviations from best practices that weaken the skill (poor description, missing trigger phrases, over-length body)
- **Suggestions**: Improvements that would raise quality (better naming, progressive disclosure opportunities, anti-pattern removal)

If the skill passes clean, say so — don't invent issues.
