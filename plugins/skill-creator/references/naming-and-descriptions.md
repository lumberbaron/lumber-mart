# Naming and Descriptions

Conventions for skill names, descriptions, and content writing.

## Naming Conventions

### Good Names

Pick a short, descriptive name that conveys what the skill does:

- `create-skill` — verb-noun action
- `review-code` — verb-noun action
- `circuit-synth` — recognized shorthand
- `pdf-editor` — clear tool identity
- `datasheet` — single-domain noun
- `bigquery` — general domain assistance
- `kubernetes` — general domain assistance

### Names to Avoid

- **Vague names**: `helper`, `utils`, `tools`, `assistant`
- **Redundant prefixes**: `skill-for-`, `claude-` (it's already a skill for Claude)
- **Overly long names**: Keep it scannable; the description carries detail
- **Underscores or camelCase**: Always use hyphens

### Technical Requirements

| Rule | Detail |
|------|--------|
| Characters | Lowercase letters (`a-z`), digits (`0-9`), hyphens (`-`) |
| Leading/trailing hyphens | Not allowed |
| Consecutive hyphens | Not allowed (`my--skill` is invalid) |
| Maximum length | 64 characters |
| Must match directory | Directory name must equal the `name` field value |

## Description Writing

### Voice: Third-Person (Required)

Descriptions must use third-person voice. The description is metadata read by the system to decide when to activate the skill — it is not the skill speaking about itself.

**Good** (third-person):
- "Guides creation of effective Claude Code skills with validation and best practices."
- "Extracts structured information from IC datasheets into markdown format."
- "Reviews code for quality issues and creates bug beads for findings."

**Bad** (first-person or imperative):
- "I help you create skills" — skills don't speak
- "Create effective skills" — imperative is for the body, not metadata
- "This skill helps with..." — unnecessary preamble

### Trigger Phrases

The description is the primary triggering mechanism. Include specific scenarios, file types, or tasks that should activate the skill. Use a structured pattern:

```
[What it does]. Use when [trigger 1], [trigger 2], or [trigger 3].
```

**Example:**
```
Comprehensive document creation, editing, and analysis with support for
tracked changes, comments, formatting preservation, and text extraction.
Use when Claude needs to work with professional documents (.docx files)
for: (1) Creating new documents, (2) Modifying or editing content,
(3) Working with tracked changes, or any other document tasks.
```

### Description Quality Heuristics

| Criterion | Guideline |
|-----------|-----------|
| Length | 80–1024 characters. Under 80 is likely too vague. |
| No angle brackets | `<` and `>` are not allowed |
| Specificity | Mention concrete artifacts (file types, tools, domains) |
| Completeness | Cover all major use cases so the skill triggers reliably |

## Content Guidelines

### Consistent Terminology

Pick one term for each concept and use it consistently throughout the skill:

- Decide between "skill" and "command" — don't alternate
- Decide between "run" and "execute" — don't alternate
- If the domain has standard terms, use them

### Imperative Form in Body

The SKILL.md body uses imperative form for instructions:

- "Run the validation script" not "You should run the validation script"
- "Check the frontmatter" not "The frontmatter should be checked"

### Avoid Time-Sensitive Information

Don't include version numbers, release dates, or links that will go stale. Instead, describe the capability generically or reference a script that checks versions at runtime.
