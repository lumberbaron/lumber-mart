# specbeads

A Claude Code plugin that integrates [spec-kit](https://github.com/spec-kit/specify) with [beads](https://github.com/beads-project/beads) for streamlined specification-driven development.

## Overview

This plugin bridges two tools:
- **spec-kit**: Manages feature specifications, plans, and design artifacts
- **beads**: Tracks work items (epics, tasks, bugs) with dependencies

The plugin decomposes spec-kit design artifacts directly into beads for implementation tracking, plus provides review skills that create beads for issues found.

## Prerequisites

- [spec-kit CLI](https://github.com/spec-kit/specify) (`specify` command)
- [beads CLI](https://github.com/beads-project/beads) (`bd` command)
- Git repository

## Installation

Copy this plugin to your Claude Code plugins directory or reference it in your project's `.claude/settings.json`.

## Skills

| Skill | Description | Model-Invocable |
|-------|-------------|-----------------|
| `/specbeads:init` | Initialize a repository with both spec-kit and beads | No (user-only) |
| `/specbeads:beadify` | Decompose plan.md + spec.md into beads (epics for phases, tasks as children) | Yes |
| `/specbeads:review-spec` | Validate implementation against spec-kit artifacts (spec.md, plan.md, constitution.md) | Yes |
| `/specbeads:review-code` | Review code for quality issues, create bug beads for findings | Yes |
| `/specbeads:review-docs` | Review documentation for completeness and accuracy | Yes |
| `/specbeads:review-tests` | Review tests for coverage and quality issues | Yes |

### Workflow

1. **Initialize**: Run `/specbeads:init` to set up spec-kit and beads in your repo
2. **Create specs**: Use spec-kit to create feature specs (spec.md, plan.md, data-model.md, contracts/)
3. **Decompose into beads**: Run `/specbeads:beadify` to create phase epics and task beads directly from specs
4. **Review the plan**: Beadify outputs a formatted implementation plan — refine by running beadify again with instructions
5. **Work on tasks**: Use `bd ready` to see available work, `bd close` when done
6. **Review quality**: Run review skills to find issues in code, tests, docs, or spec conformance

### Natural Language Triggers

Model-invocable skills can be triggered by natural language:

- **beadify**: "generate beads for this feature", "convert this feature into beads", "create tasks from the spec", "decompose this into work items"
- **review-spec**: "check if code matches the spec", "validate implementation", "review spec conformance"
- **review-code**: "review the code in api/", "check this code for bugs", "audit this module"
- **review-docs**: "review the docs for this project", "check the documentation", "validate CLAUDE.md files"
- **review-tests**: "review the tests", "check test quality", "audit test coverage"

### Usage Examples

```
/specbeads:init
/specbeads:beadify 001-user-auth
/specbeads:beadify --dry-run
/specbeads:review-code src/auth/
/specbeads:review-docs --create-beads
/specbeads:review-tests tests/unit/
/specbeads:review-spec 001-user-auth --create-beads
```

All review skills support `--create-beads` to create beads for findings (default is report-only).

## Skill Options

### specbeads:beadify

- `[spec-folder]` - Specific spec folder (e.g., `001-user-auth`)
- `--dry-run` - Preview implementation plan without creating beads
- `--force` - Create beads even if duplicates detected
- `<refinement instructions>` - When existing beads are detected, modify the decomposition (e.g., "split auth into its own phase")

### specbeads:review-spec

- `[path]` - Path to focus the review (default: entire repo)
- `[spec-folder]` - Specific spec folder (e.g., `001-user-auth`)
- `--create-beads` - Create beads for findings (default: report only)

### specbeads:review-code / review-docs / review-tests

- `[path]` - Path to review (required for review-code and review-tests)
- `--create-beads` - Create beads for findings (default: report only)

## Version Compatibility

- spec-kit: >= 1.0.0
- beads: >= 1.0.0

## Migration from v3.x

v4.0.0 converts all commands to the skills format:

| Change | Details |
|--------|---------|
| `commands/` → `skills/` | All command files moved to `skills/<name>/SKILL.md` format |
| Model invocation | All skills except `init` are now model-invocable via natural language |
| Validation script | `review-docs` now includes `scripts/validate-claude-md.py` for deterministic CLAUDE.md validation |

The skill names and functionality remain the same. Invocation syntax is unchanged (`/specbeads:<skill-name>`).

## Migration from v2.x

v3.0.0 removed three commands and rewrote beadify:

| Removed | Replacement |
|---------|-------------|
| `/specbeads:sync` | No longer needed — beads is the single source of truth. Use `bd list`, `bd ready`, `bd show` directly. |
| `/specbeads:status` | No longer needed — use `bd ready`, `bd list --status=all`, or `bd stats` for progress. |
| `/specbeads:setup-hooks` | Removed (was stashed in v2.x). |

**beadify** no longer reads tasks.md. It now reads plan.md and spec.md directly, absorbing the task decomposition logic. Beads are the single source of truth for implementation work — there is no intermediate tasks.md file.
