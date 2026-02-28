# skill-creator

A plugin for creating high-quality Claude Code skills with built-in validation, scaffolding, and best-practice guidance.

## Overview

The skill-creator plugin provides two skills: `create-skill` for scaffolding and writing new skills end-to-end, and `review-skill` for auditing existing skills against best practices. Both skills share a common set of reference material covering naming conventions, quality patterns, evaluation strategies, and a final-review checklist.

## Skills

| Skill | Description |
|-------|-------------|
| `create-skill` | Scaffold and write a new Claude Code skill with proper structure and metadata |
| `review-skill` | Review an existing skill for conformance to best practices |

### create-skill

Guides Claude through a focused workflow for creating skills:

1. Understand the skill with concrete examples
2. Determine the target plugin and directory
3. Generate a skill name
4. Scaffold the directory (`init-skill.sh`)
5. Plan reusable contents (scripts, references, assets)
6. Research the codebase
7. Write the skill (metadata, body, scripts)
8. Validate structure and metadata (`validate-skill.py`)
9. Register in the plugin CLAUDE.md
10. Present for review

### review-skill

Reviews an existing skill against best practices:

1. Locate the skill
2. Run automated validation (`validate-skill.py`)
3. Read the skill completely
4. Assess against best practices
5. Produce findings report (errors, warnings, suggestions)

## Bundled Scripts

| Script | Language | Purpose |
|--------|----------|---------|
| `init-skill.sh` | Bash | Scaffold a new skill directory with SKILL.md template |
| `validate-skill.py` | Python 3 | Validate skill structure, metadata, and content quality |

## Shared References

| Reference | Topic |
|-----------|-------|
| `naming-and-descriptions.md` | Naming conventions, description writing, content guidelines |
| `quality-patterns.md` | Progressive disclosure, workflow patterns, output patterns, anti-patterns |
| `evaluation-and-iteration.md` | Eval-driven development, Claude A/B testing, cross-model testing |
| `checklist.md` | Comprehensive quality checklist for final review |
