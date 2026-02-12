---
name: creating-skills
description: Guides creation and review of Claude Code skills with proper structure, naming, descriptions, and quality patterns. Use when a user wants to create a new skill, improve an existing skill, review or audit a skill for best practices, or learn skill authoring conventions. Covers skill anatomy, progressive disclosure, frontmatter conventions, bundled resources, validation, and evaluation-driven iteration.
---

# Creating Skills

This skill guides you through creating and reviewing Claude Code skills.

## Workflow Routing

Determine the task type:

- **Creating a new skill or improving an existing one?** → Follow the [Creation Workflow](#creation-workflow) below
- **Reviewing or auditing an existing skill?** → Follow the [Review Workflow](#review-workflow) below

## About Skills

Skills are modular packages that extend Claude's capabilities with specialized knowledge, workflows, and tools. They transform Claude from a general-purpose agent into a specialized one equipped with procedural knowledge no model fully possesses.

### Three-Level Loading

Skills use progressive disclosure to manage context efficiently:

1. **Metadata** (name + description) — Always in context (~100 words)
2. **SKILL.md body** — Loaded when the skill triggers (<500 lines)
3. **Bundled resources** — Loaded as needed by Claude (scripts, references, assets)

The context window is a public good. Skills share it with system prompts, conversation history, other skills' metadata, and the user's request. Every line must justify its token cost.

## Core Principles

### Conciseness

**Default assumption: Claude is already very smart.** Only add context Claude doesn't already have. Challenge each piece of information: "Does Claude really need this explanation?" Prefer concise examples over verbose explanations.

### Degrees of Freedom

Match specificity to the task's fragility and variability:

- **High freedom** (text-based instructions): Multiple approaches are valid, decisions depend on context. *An open field — many routes work.*
- **Medium freedom** (pseudocode or parameterized scripts): A preferred pattern exists but some variation is acceptable.
- **Low freedom** (specific scripts, few parameters): Operations are fragile, consistency is critical, a specific sequence must be followed. *A narrow bridge with cliffs — guardrails required.*

### Progressive Disclosure

Keep SKILL.md under 500 lines. Split content into separate reference files when approaching this limit, and reference them clearly from SKILL.md so the reader knows they exist and when to use them.

See [references/quality-patterns.md](references/quality-patterns.md) for progressive disclosure patterns and examples.

## Skill Anatomy

### Directory Structure

```
skill-name/
├── SKILL.md              (required)
│   ├── YAML frontmatter  (required: name, description)
│   └── Markdown body     (required: instructions)
└── Bundled Resources     (optional)
    ├── scripts/          Executable code (Python/Bash/etc.)
    ├── references/       Documentation loaded into context as needed
    └── assets/           Files used in output (templates, images, fonts)
```

### Frontmatter

Every SKILL.md starts with YAML frontmatter containing `name` and `description`. These are the **only** fields Claude reads to decide when to use the skill — they are the primary triggering mechanism.

#### Name

- **Format**: Gerund form recommended (e.g., `creating-skills`, `reviewing-code`, `generating-reports`). Verb-noun form also acceptable (e.g., `circuit-synth`, `pdf-editor`).
- **Technical rules**: Lowercase letters, digits, and hyphens only. No leading/trailing/consecutive hyphens. Max 64 characters.

See [references/naming-and-descriptions.md](references/naming-and-descriptions.md) for full naming conventions.

#### Description

- **Voice**: Third-person ("Guides creation of..." not "I guide..." or "Guide the creation of...")
- **Content**: What the skill does AND when to use it. Include trigger phrases — specific scenarios, file types, or tasks.
- **Length**: Max 1024 characters. No angle brackets.

> [!IMPORTANT]
> All "when to use" information belongs in the description, not the body. The body only loads after triggering, so "When to Use This Skill" sections in the body waste tokens.

See [references/naming-and-descriptions.md](references/naming-and-descriptions.md) for description writing patterns and examples.

### Body Conventions

- Use imperative/infinitive form for instructions
- Structure with clear markdown headings
- Include `$ARGUMENTS` block if the skill accepts user input
- Use callout blocks (`> [!NOTE]`, `> [!CAUTION]`, `> [!IMPORTANT]`) for critical guidance
- Prefer concrete examples over abstract explanations

### Bundled Resources

#### Scripts (`scripts/`)

Executable code for tasks requiring deterministic reliability or frequently rewritten logic.

- **When to use**: Same code is rewritten repeatedly, or deterministic reliability is needed
- **Benefits**: Token efficient, deterministic, can execute without loading into context
- **Best practices**: Test scripts by running them. Solve complete problems — no placeholder logic, no magic numbers, no "adjust as needed" stubs. Scripts should produce verifiable intermediate outputs where possible.

#### References (`references/`)

Documentation loaded into context as needed to inform Claude's process.

- **When to use**: Detailed information Claude should reference while working (schemas, API docs, domain knowledge, policies)
- **Best practice**: If files exceed ~10k words, include grep patterns in SKILL.md. Keep references one level deep — all should link directly from SKILL.md.
- **Avoid duplication**: Information lives in SKILL.md *or* a reference file, not both. Keep only essential procedural guidance in SKILL.md; move detailed reference material out.

#### Assets (`assets/`)

Files used in output, not loaded into context.

- **When to use**: Templates, images, boilerplate code, fonts, sample documents
- **Benefits**: Separates output resources from documentation; Claude uses files without context cost

### What NOT to Include

A skill should only contain files that directly support its functionality. Do **not** create:

- README.md, CHANGELOG.md, INSTALLATION_GUIDE.md, or other auxiliary documentation
- Files aimed at human readers rather than Claude
- Extraneous scaffolding that adds clutter

The skill is for an AI agent. Include only what that agent needs to do the job.

## Creation Workflow

Creating a skill involves seven steps. Follow them in order, skipping only when there is a clear reason a step doesn't apply.

1. Understand with concrete examples
2. Plan reusable contents
3. Initialize the skill directory
4. Write the skill
5. Validate
6. Test and iterate
7. Final review

### Step 1: Understand with Concrete Examples

Skip only when usage patterns are already clearly understood.

Gather concrete examples of how the skill will be used. This understanding can come from direct user examples or generated examples validated with feedback.

**Key questions to explore:**

- "What functionality should this skill support?"
- "Can you give examples of how it would be used?"
- "What would a user say that should trigger this skill?"
- "What trigger phrases should appear in the description?"

Avoid asking too many questions in a single message. Start with the most important and follow up as needed.

**Conclude** when you have a clear sense of the functionality, the trigger phrases for the description, and concrete usage examples.

### Step 2: Plan Reusable Contents

Analyze each concrete example to identify what bundled resources would help:

1. Consider how to execute the example from scratch
2. Identify what scripts, references, and assets would be helpful for repeated execution

**Examples:**

- Rotating PDFs repeatedly → `scripts/rotate_pdf.py`
- Building frontend apps → `assets/hello-world/` template directory
- Querying BigQuery → `references/schema.md` with table schemas

Produce a list of scripts, references, and assets to include.

### Step 3: Initialize the Skill Directory

Skip if the skill already exists and only needs iteration.

Run the init script to scaffold a new skill directory:

```bash
scripts/init-skill.sh <skill-name> [parent-directory]
```

The script creates the skill directory with a SKILL.md template containing proper frontmatter (name pre-filled, description with third-person reminder) and optional `scripts/` and `references/` subdirectories.

> [!NOTE]
> The script validates the skill name format before creating anything. If the name is invalid, it prints the rules and exits.

### Step 4: Write the Skill

Work through these areas in order:

#### 4a. Metadata (frontmatter)

Write the `name` and `description` fields. The description is the primary triggering mechanism — include what the skill does and all trigger phrases.

See [references/naming-and-descriptions.md](references/naming-and-descriptions.md) for conventions and examples.

#### 4b. Body (markdown instructions)

Write the instructions Claude will follow when the skill triggers. Apply these guidelines:

- Only include what Claude doesn't already know
- Use progressive disclosure — keep the body lean, move details to references
- Use imperative form
- Include concrete examples over abstract explanations

See [references/quality-patterns.md](references/quality-patterns.md) for workflow patterns, output patterns, and anti-patterns to avoid.

#### 4c. Scripts and resources

Implement the scripts, references, and assets identified in Step 2.

- **Test scripts** by running them to verify they work correctly
- **Delete** any scaffolded example files not needed for this skill
- If the user needs to provide assets (brand files, templates, etc.), ask for them now

### Step 5: Validate

Run the validation script against the skill:

```bash
scripts/validate-skill.py <path/to/skill-directory>
```

The script checks:
- SKILL.md existence and frontmatter format
- Name format (lowercase, hyphens, digits; max 64 chars)
- Description quality (third-person voice, trigger phrases, length)
- Body line count (warns if >500 lines)
- Reference file reachability from SKILL.md
- Extraneous files
- Path style (no backslashes)

Fix any errors and re-run until validation passes. Use `--json` for machine-readable output.

### Step 6: Test and Iterate

After the skill passes validation, test it on real tasks and iterate.

**Quick iteration loop:**

1. Use the skill on real tasks
2. Notice struggles or inefficiencies
3. Identify how SKILL.md or bundled resources should be updated
4. Implement changes and re-validate

For deeper evaluation methodology — including evaluation-driven development, the Claude A/B pattern, and cross-model testing — see [references/evaluation-and-iteration.md](references/evaluation-and-iteration.md).

### Step 7: Final Review

Before considering the skill complete, run through the comprehensive quality checklist.

See [references/checklist.md](references/checklist.md) for the full checklist covering metadata, structure, content quality, scripts, and testing.

## Review Workflow

Use this workflow to review an existing skill for conformance to best practices. The review produces a findings report with actionable recommendations.

### Step 1: Run Automated Validation

Run the validation script first to catch structural and metadata issues:

```bash
scripts/validate-skill.py <path/to/skill-directory>
```

Record all errors and warnings.

### Step 2: Read the Skill

Read SKILL.md fully, then read any bundled references, scripts, and assets. Build a complete picture of what the skill does and how it's structured.

### Step 3: Assess Against Best Practices

Evaluate the skill against each area, using the reference files for detailed criteria:

| Area | Reference |
|------|-----------|
| Name and description quality | [references/naming-and-descriptions.md](references/naming-and-descriptions.md) |
| Content patterns and anti-patterns | [references/quality-patterns.md](references/quality-patterns.md) |
| Full quality checklist | [references/checklist.md](references/checklist.md) |

For each issue found, note the **location** (file and section), the **problem**, and a **recommendation**.

### Step 4: Produce Findings Report

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
