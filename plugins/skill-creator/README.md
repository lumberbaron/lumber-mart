# skill-creator

A plugin for creating high-quality Claude Code skills with built-in validation, scaffolding, and best-practice guidance.

## Overview

The skill-creator plugin provides a comprehensive skill (`creating-skills`) that guides Claude through the full skill-creation workflow: understanding requirements, scaffolding directories, writing effective SKILL.md files, validating structure, and iterating with evaluation-driven development. It bundles reference material on naming conventions, quality patterns, evaluation strategies, and a final-review checklist.

## Skills

| Skill | Description |
|-------|-------------|
| `creating-skills` | End-to-end guide for creating and refining Claude Code skills |

### creating-skills

Guides Claude through a 7-step workflow for creating skills:

1. Understand the skill with concrete examples
2. Plan reusable contents (scripts, references, assets)
3. Initialize the skill directory (`init-skill.sh`)
4. Write the skill (metadata, body, scripts)
5. Validate structure and metadata (`validate-skill.py`)
6. Test and iterate with evaluation-driven development
7. Final review against quality checklist

**Bundled scripts:**

| Script | Language | Purpose |
|--------|----------|---------|
| `init-skill.sh` | Bash | Scaffold a new skill directory with SKILL.md template |
| `validate-skill.py` | Python 3 | Validate skill structure, metadata, and content quality |

**Reference material:**

| Reference | Topic |
|-----------|-------|
| `naming-and-descriptions.md` | Naming conventions, description writing, content guidelines |
| `quality-patterns.md` | Progressive disclosure, workflow patterns, output patterns, anti-patterns |
| `evaluation-and-iteration.md` | Eval-driven development, Claude A/B testing, cross-model testing |
| `checklist.md` | Comprehensive quality checklist for final review |
