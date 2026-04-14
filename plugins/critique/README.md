# critique

A Claude Code plugin providing review skills for code, tests, and documentation. Produces structured findings reports that surface design, coverage, and doc-structure issues that linters and static analysis miss.

## Overview

Three focused review skills, each operating on a path you specify:

- **review-code** — design issues (single responsibility, abstraction levels, testability, meaningful naming, API design, error handling strategy)
- **review-tests** — test completeness, usefulness, coverage gaps, output validation, isolation, readability
- **review-docs** — README and CLAUDE.md quality, progressive disclosure, enumeration completeness, index drift, `.claude/rules/` validation

Each skill produces a structured findings report with P1/P2/P3 (and P4 for docs) severities, specific file:line locations, explanations, and concrete fixes.

## Installation

Add this plugin to your Claude Code plugins directory or reference it in your project's `.claude/settings.json`.

## Skills

| Skill | Description | Model-Invocable |
|-------|-------------|-----------------|
| `/review-code` | Review code for design issues | Yes |
| `/review-tests` | Review tests for quality and coverage gaps | Yes |
| `/review-docs` | Review README and CLAUDE.md files | Yes |

### Natural Language Triggers

- **review-code**: "review the code in api/", "check this code for design issues", "audit this module"
- **review-tests**: "review the tests", "check test quality", "audit test coverage"
- **review-docs**: "review the docs for this project", "check the documentation", "validate CLAUDE.md files"

### Usage Examples

```
/review-code src/auth/
/review-tests tests/unit/
/review-docs
/review-docs backend/
```

## Output

Each skill produces a report with:

- Header: `N files reviewed, M issues found (severity breakdown)`
- One finding per issue with H3 header, priority tag, location, explanation, and concrete fix

No tables, no passing rows — only actionable findings.

## Using with beads

Critique is intentionally bead-agnostic. To file findings as beads, install the companion plugin **specbeads** and run `/raise-beads` after a review. It reads the review output from conversation context, deduplicates against existing open/closed beads, and creates bug/task beads with structured descriptions.

```
/review-code src/auth/
/raise-beads
```

In environments that don't use beads, the review report is the deliverable — read it directly, or ask Claude to act on specific findings.

## Prerequisites

- `python3` (for `review-docs` structural validation script)

No other tooling required. The review skills assume you already run linters, formatters, security scanners, and type checkers separately — critique focuses on issues those tools cannot detect.
