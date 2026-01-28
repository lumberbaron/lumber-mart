# specbeads

A Claude Code plugin that integrates [spec-kit](https://github.com/spec-kit/specify) with [beads](https://github.com/beads-project/beads) for streamlined specification-driven development.

## Overview

This plugin bridges two tools:
- **spec-kit**: Manages feature specifications, plans, and task breakdowns
- **beads**: Tracks work items (epics, tasks, bugs) with dependencies

The plugin provides commands to convert spec-kit tasks into beads and keep them synchronized, plus review skills that create beads for issues found.

## Prerequisites

- [spec-kit CLI](https://github.com/spec-kit/specify) (`specify` command)
- [beads CLI](https://github.com/beads-project/beads) (`bd` command)
- Git repository

## Installation

Copy this plugin to your Claude Code plugins directory or reference it in your project's `.claude/settings.json`.

## Commands

| Command | Description |
|---------|-------------|
| `/specbeads.init` | Initialize a repository with both spec-kit and beads |
| `/specbeads.beadify` | Convert tasks.md into beads (epics for phases, tasks as children) |
| `/specbeads.reconcile` | Validate and sync state between beads, tasks.md, and implementation |

### Workflow

1. **Initialize**: Run `/specbeads.init` to set up spec-kit and beads in your repo
2. **Create specs**: Use spec-kit to create feature specs and task breakdowns
3. **Convert to beads**: Run `/specbeads.beadify` to create trackable work items
4. **Work on tasks**: Use `bd ready` to see available work, `bd close` when done
5. **Stay in sync**: Run `/specbeads.reconcile` periodically to catch discrepancies

## Skills

| Skill | Description |
|-------|-------------|
| `specbeads.review-code` | Review code for quality issues, create bug beads for findings |
| `specbeads.review-docs` | Review documentation for completeness and accuracy |
| `specbeads.review-tests` | Review tests for coverage and quality issues |

### Usage

```
/specbeads.review-code src/auth/
/specbeads.review-docs --dry-run
/specbeads.review-tests tests/unit/
```

All review skills support `--dry-run` to preview findings without creating beads.

## Command Options

### specbeads.beadify

- `[spec-folder]` - Specific spec folder (e.g., `001-user-auth`)
- `--dry-run` - Preview without creating beads
- `--skip-completed` - Don't create beads for tasks marked `[x]`
- `--force` - Create beads even if duplicates detected

### specbeads.reconcile

- `[spec-folder]` - Specific spec folder to reconcile
- `--dry-run` - Report discrepancies without making changes
- `--skip-tests` - Skip build/test validation
- `--verbose` - Show detailed validation output

## Version Compatibility

- spec-kit: >= 1.0.0
- beads: >= 1.0.0
