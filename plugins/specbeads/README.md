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
| `/specbeads:init` | Initialize a repository with both spec-kit and beads |
| `/specbeads:beadify` | Convert tasks.md into beads (epics for phases, tasks as children) |
| `/specbeads:sync` | Bidirectional sync between beads and tasks.md (check off tasks, close beads, report orphans) |
| `/specbeads:status` | Read-only dashboard showing project progress, phase status, and sync health |

### Workflow

1. **Initialize**: Run `/specbeads:init` to set up spec-kit and beads in your repo
2. **Create specs**: Use spec-kit to create feature specs and task breakdowns
3. **Convert to beads**: Run `/specbeads:beadify` to create trackable work items
4. **Work on tasks**: Use `bd ready` to see available work, `bd close` when done
5. **Stay in sync**: Run `/specbeads:sync` to keep beads and tasks.md aligned
6. **Check progress**: Run `/specbeads:status` to see overall progress and sync health
7. **Review quality**: Run review commands to find issues in code, tests, docs, or spec conformance

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
- `--dry-run` - Preview without creating beads
- `--skip-completed` - Don't create beads for tasks marked `[x]`
- `--force` - Create beads even if duplicates detected

### specbeads:sync

- `[spec-folder]` - Specific spec folder to sync
- `--dry-run` - Report what would change without making modifications
- `--no-validate` - Skip file-existence validation checks
- `--direction <both|beads-to-tasks|tasks-to-beads>` - Sync direction (default: `both`)

### specbeads:status

- `[spec-folder]` - Specific spec folder to report on
- `--verbose` - Show per-task detail tables within each phase

### specbeads:review-spec

- `[path]` - Path to focus the review (default: entire repo)
- `[spec-folder]` - Specific spec folder (e.g., `001-user-auth`)
- `--dry-run` - List findings without creating beads

## Version Compatibility

- spec-kit: >= 1.0.0
- beads: >= 1.0.0

## Migration from v1.x

v2.0.0 removes the `/specbeads:reconcile` command. Its responsibilities are now split across more focused commands:

| Old (reconcile) | New |
|---|---|
| Beads/tasks sync | `/specbeads:sync` (now bidirectional) |
| Build/test validation | `/specbeads:review-spec` |
| Architecture checks | `/specbeads:review-spec` |
| Constitution alignment | `/specbeads:review-spec` |
| Orphan detection | `/specbeads:sync` (orphan reporting) |
| Status dashboard | `/specbeads:status` |

The default `sync` direction is now `both` (bidirectional). To get the old one-way behavior, use `--direction beads-to-tasks`.
