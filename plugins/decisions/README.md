# decisions

Architectural Decision Record (ADR) creation and maintenance tooling for Claude Code.

## Overview

ADRs capture the *why* behind significant architectural choices — constraints, trade-offs, rejected alternatives — and act as the policy layer above specs. A spec describes *what* to build; the ADR it cites describes *which constraints shaped it*. When decisions live only in Slack threads or a reviewer's memory, future agents re-litigate settled questions or quietly drift from intent. This plugin produces structured, version-controlled ADRs that agents can read and honor.

The output is MADR-style (Markdown Architecture Decision Records) with rich frontmatter so ADRs form a navigable graph: `supersedes`, `superseded-by`, `related`, and `governs` (linking to spec files the ADR constrains).

## Skills

| Skill | Description | Model-Invocable |
|-------|-------------|-----------------|
| `/decisions:create-adr` | Create a new ADR from a standard MADR template, researching context from the codebase and registering it in the project's CLAUDE.md | Yes |

## Usage

```
/decisions:create-adr use Postgres for the event store instead of DynamoDB
/decisions:create-adr adopt trunk-based development with short-lived feature flags
/decisions:create-adr replace the custom retry wrapper with Temporal workflows
```

If you drop the argument, the skill will ask what decision you want to record.

## Template Structure

Every ADR follows MADR conventions:

- **Frontmatter** — `id`, `title`, `status`, `date`, `deciders`, `supersedes`, `superseded-by`, `related`, `governs`, `tags`
- **Context and Problem Statement** — forces in play, constraints, the problem
- **Decision Drivers** — the criteria that matter
- **Considered Options** — options under evaluation, with one-line summaries
- **Decision Outcome** — which option won, and why against the drivers
- **Consequences** — positive, negative, and risks accepted
- **Pros and Cons of the Options** — per-option analysis
- **Implementation Notes** — how the decision cascades into specs/code
- **References** — links to discussions, PRs, specs

## ADR Directory Convention

The skill looks for an existing ADR directory in this order:

1. `docs/adr/` (if it exists)
2. `docs/decisions/` (if it exists)
3. `docs/adrs/` (if it exists)
4. Asks the user, defaulting to `docs/adr/`

## The `governs:` frontmatter field

This is the bridge between ADRs and specs. Populate `governs:` with paths to spec files, `spec.md`/`plan.md` artifacts, or feature directories the ADR constrains. Downstream tooling (and future agents) can walk the relationship in either direction: given a spec, find the ADRs that govern it; given an ADR, find the specs it shapes.

## Registration in CLAUDE.md

The skill appends (or updates) an `## Architectural Decisions` section in the project's root `CLAUDE.md`, listing each ADR with a one-line "when this applies" description. This is how future Claude Code sessions discover and honor prior decisions — if an ADR isn't registered, agents won't see it.

## Bundled Resources

### Scripts

| Script | Language | Purpose |
|--------|----------|---------|
| `init-adr.sh` | Bash | Create an ADR file from the MADR template with auto-numbered ID and today's date |

### Assets

| File | Purpose |
|------|---------|
| `adr-template.md` | MADR-format ADR template with all sections and frontmatter |
