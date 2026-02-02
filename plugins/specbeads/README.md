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

## Commands

| Command | Description |
|---------|-------------|
| `/specbeads:init` | Initialize a repository with both spec-kit and beads |
| `/specbeads:beadify` | Decompose plan.md + spec.md into beads (epics for phases, tasks as children) |

### Workflow

1. **Initialize**: Run `/specbeads:init` to set up spec-kit and beads in your repo
2. **Create specs**: Use spec-kit to create feature specs (spec.md, plan.md, data-model.md, contracts/)
3. **Decompose into beads**: Run `/specbeads:beadify` to create phase epics and task beads directly from specs
4. **Review the plan**: Beadify outputs a formatted implementation plan — refine by running beadify again with instructions
5. **Work on tasks**: Use `bd ready` to see available work, `bd close` when done
6. **Review quality**: Run review commands to find issues in code, tests, docs, or spec conformance

## Skills

| Skill | Description |
|-------|-------------|
| `specbeads:review-code` | Review code for quality issues, create bug beads for findings |
| `specbeads:review-docs` | Review documentation for completeness and accuracy |
| `specbeads:review-tests` | Review tests for coverage and quality issues |
| `specbeads:review-spec` | Validate implementation against spec-kit artifacts (spec.md, plan.md, constitution.md) |

### Usage

```
/specbeads:review-code src/auth/
/specbeads:review-docs --dry-run
/specbeads:review-tests tests/unit/
/specbeads:review-spec 001-user-auth
```

All review skills support `--dry-run` to preview findings without creating beads.

## Command Options

### specbeads:beadify

- `[spec-folder]` - Specific spec folder (e.g., `001-user-auth`)
- `--dry-run` - Preview implementation plan without creating beads
- `--force` - Create beads even if duplicates detected
- `<refinement instructions>` - When existing beads are detected, modify the decomposition (e.g., "split auth into its own phase")

### specbeads:review-spec

- `[path]` - Path to focus the review (default: entire repo)
- `[spec-folder]` - Specific spec folder (e.g., `001-user-auth`)
- `--dry-run` - List findings without creating beads

## Version Compatibility

- spec-kit: >= 1.0.0
- beads: >= 1.0.0

## Migration from v2.x

v3.0.0 removes three commands and rewrites beadify:

| Removed | Replacement |
|---------|-------------|
| `/specbeads:sync` | No longer needed — beads is the single source of truth. Use `bd list`, `bd ready`, `bd show` directly. |
| `/specbeads:status` | No longer needed — use `bd ready`, `bd list --status=all`, or `bd stats` for progress. |
| `/specbeads:setup-hooks` | Removed (was stashed in v2.x). |

**beadify** no longer reads tasks.md. It now reads plan.md and spec.md directly, absorbing the task decomposition logic. Beads are the single source of truth for implementation work — there is no intermediate tasks.md file.

The `--skip-completed` flag has been removed from beadify (no checkboxes to interpret). Use `--force` to recreate beads from scratch or pass refinement instructions to modify existing beads.
