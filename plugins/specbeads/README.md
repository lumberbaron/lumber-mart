# specbeads

A Claude Code plugin that integrates [spec-kit](https://github.com/spec-kit/specify) with [beads](https://github.com/beads-project/beads) for streamlined specification-driven development.

## Overview

This plugin bridges two tools:
- **spec-kit**: Manages feature specifications, plans, and design artifacts
- **beads**: Tracks work items (epics, tasks, bugs) with dependencies

The plugin converts spec-kit task lists into beads for implementation tracking, plus provides review skills that create beads for issues found.

## Prerequisites

- [spec-kit CLI](https://github.com/spec-kit/specify) (`specify` command)
- [beads CLI](https://github.com/beads-project/beads) (`bd` command)
- Git repository

## Installation

Copy this plugin to your Claude Code plugins directory or reference it in your project's `.claude/settings.json`.

## Skills

| Skill | Description | Model-Invocable |
|-------|-------------|-----------------|
| `/init` | Initialize a repository with both spec-kit and beads | No (user-only) |
| `/beadify` | Convert tasks.md into beads (epics for phases, tasks as children) | Yes |
| `/implement` | Implement a spec-kit feature phase, one task at a time with per-task commits | Yes |
| `/fix` | Implement standalone bug/task beads (e.g. from review findings), one at a time | Yes |
| `/review-spec` | Validate implementation against spec-kit artifacts (spec.md, plan.md, constitution.md) | Yes |
| `/review-code` | Review code for quality issues, create bug beads for findings | Yes |
| `/review-docs` | Review documentation for completeness and accuracy | Yes |
| `/review-tests` | Review tests for coverage and quality issues | Yes |

### Workflow

1. **Initialize**: Run `/init` to set up spec-kit and beads in your repo
2. **Create specs**: Use spec-kit to create feature specs (spec.md, plan.md, data-model.md, contracts/)
3. **Generate tasks**: Run `/speckit.tasks` to decompose specs into tasks.md
4. **Convert to beads**: Run `/beadify` to create phase epics and task beads from tasks.md
5. **Implement**: Run `/implement` to work through phase tasks, or `/implement --all` to continue through all phases
6. **Review quality**: Run review skills to find issues; use `--create-beads` to file findings as beads
7. **Fix findings**: Run `/fix` to work through standalone beads created by review skills

### Natural Language Triggers

Model-invocable skills can be triggered by natural language:

- **beadify**: "generate beads for this feature", "convert this feature into beads", "create tasks from the spec", "decompose this into work items"
- **implement**: "implement the next phase", "implement phase 2", "implement 002-realtime-gateway --all"
- **fix**: "fix the review beads", "work through the code review findings", "fix sam-b3i"
- **review-spec**: "check if code matches the spec", "validate implementation", "review spec conformance"
- **review-code**: "review the code in api/", "check this code for bugs", "audit this module"
- **review-docs**: "review the docs for this project", "check the documentation", "validate CLAUDE.md files"
- **review-tests**: "review the tests", "check test quality", "audit test coverage"

### Usage Examples

```
/init
/beadify 001-user-auth
/beadify --dry-run
/implement
/implement 002-realtime-gateway --all
/fix
/fix sam-b3i
/fix auth
/review-code src/auth/
/review-docs --create-beads
/review-tests tests/unit/
/review-spec 001-user-auth --create-beads
```

All review skills support `--create-beads` to create beads for findings (default is report-only).

## Skill Options

### beadify

- `[spec-folder]` - Specific spec folder (e.g., `001-user-auth`)
- `--dry-run` - Preview implementation plan without creating beads
- `--force` - Create beads even if duplicates detected

### implement

- `[epic-bead-id]` - Specific phase epic to implement
- `[feature-slug]` - Implement the next ready phase for that feature (e.g., `002-realtime-gateway`)
- `--all` - Continue through all unblocked phases sequentially
- `--dry-run` - Show the execution plan without making changes
- `<additional instructions>` - Guidance applied to all tasks (constraints, approach hints)

### fix

- `[bead-id]` - Specific standalone bead to fix
- `[filter]` - Work all ready standalone beads whose title contains the filter text
- `--dry-run` - Show the matched bead list without making changes
- `<additional instructions>` - Guidance applied throughout

### review-spec

- `[path]` - Path to focus the review (default: entire repo)
- `[spec-folder]` - Specific spec folder (e.g., `001-user-auth`)
- `--create-beads` - Create beads for findings (default: report only)

### review-code / review-docs / review-tests

- `[path]` - Path to review (required for review-code and review-tests)
- `--create-beads` - Create beads for findings (default: report only)

## Version Compatibility

- spec-kit: >= 1.0.0
- beads: >= 1.0.0
