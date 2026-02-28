---
name: create-skill
description: Creates a new Claude Code skill with proper structure, naming, descriptions, and quality patterns, scaffolding the directory and writing the SKILL.md with bundled resources. Use when a user wants to create a new skill, build a skill from scratch, scaffold a skill directory, or write a SKILL.md file. Covers skill anatomy, progressive disclosure, frontmatter conventions, bundled resources, validation, and evaluation-driven iteration.
---

# Create Skill

## User Input

```text
$ARGUMENTS
```

The input describes what the skill should do (e.g., "a skill for generating PDF reports", "review pull requests for security issues", "scaffold React components").

If `$ARGUMENTS` is empty, ask the user what skill they want to create.

## Workflow

### Step 1: Understand with concrete examples

Gather concrete examples of how the skill will be used. This understanding can come from direct user examples or generated examples validated with feedback.

**Key questions to explore:**

- "What functionality should this skill support?"
- "Can you give examples of how it would be used?"
- "What would a user say that should trigger this skill?"

Avoid asking too many questions in a single message. Start with the most important and follow up as needed.

**Conclude** when you have a clear sense of the functionality, the trigger phrases for the description, and concrete usage examples.

### Step 2: Determine the target plugin and directory

Check whether the skill belongs in an existing plugin or needs a new one. Identify the `skills/` directory where the new skill will live.

### Step 3: Generate a skill name

Convert the user's description into a kebab-case skill name.

- **Examples**: `create-skill`, `review-code`, `circuit-synth`, `pdf-editor`, `datasheet`
- **Technical rules**: Lowercase letters, digits, and hyphens only. No leading/trailing/consecutive hyphens. Max 64 characters.

See [../../references/naming-and-descriptions.md](../../references/naming-and-descriptions.md) for full naming conventions.

### Step 4: Scaffold the skill directory

Run the init script to create the directory structure:

```bash
bash ${CLAUDE_PLUGIN_ROOT}/skills/create-skill/scripts/init-skill.sh <skill-name> <parent-directory>
```

This creates a skill directory with a SKILL.md template, `scripts/`, and `references/` subdirectories.

> [!NOTE]
> The script validates the skill name format before creating anything. If the name is invalid, it prints the rules and exits.

### Step 5: Plan reusable contents

Analyze the concrete examples from Step 1 to identify what bundled resources would help:

- **Scripts**: Same code would be rewritten repeatedly, or deterministic reliability is needed
- **References**: Detailed information Claude should reference while working (schemas, API docs, domain knowledge)
- **Assets**: Files used in output (templates, images, boilerplate code)

### Step 6: Research the codebase

Before writing the skill, investigate the project to understand relevant patterns:

- Existing skills in the same plugin for conventions and structure
- Related code, APIs, or tools the skill will interact with
- Existing documentation that covers related processes

> [!IMPORTANT]
> The goal is to write a skill with real commands and real paths, not generic placeholders. Every script invocation and file reference should actually work.

### Step 7: Write the skill

Edit the scaffolded SKILL.md, replacing all template placeholders:

#### 7a. Metadata (frontmatter)

Write the `name` and `description` fields. The description is the primary triggering mechanism — include what the skill does and all trigger phrases. Use third-person voice ("Guides creation of..." not "Guide the creation of...").

See [../../references/naming-and-descriptions.md](../../references/naming-and-descriptions.md) for description writing patterns.

#### 7b. Body (markdown instructions)

Write the instructions Claude will follow when the skill triggers:

- Only include what Claude doesn't already know
- Use progressive disclosure — keep the body under 500 lines, move details to references
- Use imperative form
- Include `$ARGUMENTS` block if the skill accepts user input
- Prefer concrete examples over abstract explanations

See [../../references/quality-patterns.md](../../references/quality-patterns.md) for workflow patterns, output patterns, and anti-patterns.

#### 7c. Scripts and resources

Implement the scripts, references, and assets identified in Step 5:

- **Test scripts** by running them to verify they work correctly
- **Delete** any scaffolded example files not needed for this skill
- Scripts should solve complete problems — no placeholder logic, no "adjust as needed" stubs

### Step 8: Validate

Run the validation script against the skill:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/create-skill/scripts/validate-skill.py <path/to/skill-directory>
```

Fix any errors and re-run until validation passes. Use `--json` for machine-readable output.

### Step 9: Register the skill in the plugin CLAUDE.md

> [!IMPORTANT]
> This step is critical. Skills only get used if agents and developers know they exist. The plugin's `CLAUDE.md` is the reference that tells Claude what's available — if a skill isn't listed there, it effectively doesn't exist.

Read the plugin's `CLAUDE.md`. Add a row to the directory table for the new skill, following the existing format.

### Step 10: Present for review

Show the user the completed skill and ask if anything needs adjustment. Highlight any areas where you had to make assumptions due to limited information.

## Skill Anatomy Reference

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

### What NOT to include

A skill should only contain files that directly support its functionality. Do **not** create README.md, CHANGELOG.md, or other auxiliary documentation inside a skill directory. The skill is for an AI agent — include only what that agent needs to do the job.

## References

Detailed conventions and best practices (shared across skill-creator skills):

| Reference | When to read |
|-----------|--------------|
| [../../references/naming-and-descriptions.md](../../references/naming-and-descriptions.md) | Writing skill names and descriptions |
| [../../references/quality-patterns.md](../../references/quality-patterns.md) | Structuring workflows, output, and scripts |
| [../../references/evaluation-and-iteration.md](../../references/evaluation-and-iteration.md) | Testing and iterating on skills |
| [../../references/checklist.md](../../references/checklist.md) | Final quality review before completion |
