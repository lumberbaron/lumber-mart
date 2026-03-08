---
name: review-code
description: Reviews code for design issues that static analysis misses. Checks single responsibility, abstraction levels, testability, and meaningful naming. Use when asked to review code, find design problems, or improve code quality.
---

# Code Review

Review code for design and architecture issues that linters and static analysis tools miss.

> [!IMPORTANT]
> Consult [REFERENCE.md](REFERENCE.md) for the expected output format and level of detail.

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Argument Parsing

Parse `$ARGUMENTS` for:
- **Path**: Required path to review (file or directory)
- **`--create-beads`**: Create beads for findings (default: report only)

## Prerequisites

This review assumes standard tooling is already running:
- **Linters** (ESLint, golangci-lint, pylint) catch complexity, length, nesting, unused code
- **Formatters** (prettier, gofmt, black) handle style
- **Security scanners** (Semgrep, CodeQL, Bandit) catch injection, XSS, secrets
- **Type checkers** (TypeScript, mypy) catch type errors

If these aren't set up, recommend adding them before this review.

## Workflow

### Step 1 — Discover source files

Find all source files in the specified path, excluding test files, vendored/generated code, and files that are purely configuration. Record the full file list and count.

### Step 2 — Choose execution strategy

- **1–2 files → Direct mode**: Read the files, evaluate against the Design Criteria below (skip mechanical checks tools handle), then proceed to Deduplication and Bead Check.
- **3+ files → Parallel mode**: Batch files, spawn subagents, collect results, merge, then proceed to Deduplication and Bead Check.

### Parallel Review Mode

Use this mode when 3 or more source files are discovered.

#### Batching

Group files into batches based on total file count:

| Total files | Files per batch | ~Subagents |
|-------------|-----------------|------------|
| 3–10        | 1               | 3–10       |
| 11–20       | 2               | 6–10       |
| 21+         | 3               | 7–10       |

#### Spawn subagents

For each batch, use `Agent(subagent_type="general-purpose")`. **Spawn all subagents in a single message** so they run in parallel.

Each subagent prompt MUST include:

1. The file paths in its batch (instruct the subagent to read them)
2. The **Design Criteria** section from this skill — copy it verbatim into the prompt
3. The **Severity** section from this skill — copy it verbatim into the prompt
4. The **Prerequisites** note — remind the subagent to skip mechanical checks that linters/formatters/scanners handle
5. The structured output format below
6. The explicit instruction: **"Do NOT use the Bash tool. Do NOT run any shell commands. Use only Read, Grep, and Glob tools. Do NOT create beads, do NOT run `bd` commands. Return findings only."**
7. The explicit instruction: **"For every P3 finding, you MUST state a concrete consequence in the `explanation` field: 'a caller/maintainer would likely \<specific mistake\> because of this.' Omit P3 findings that lack this claim."**
8. The explicit instruction: **"For the `pattern` field, use a short, reusable label that names the underlying anti-pattern (e.g., 'module-scope side effects', 'mixed abstraction in handlers'). If two findings in your batch stem from the same root cause, they MUST use the same pattern label."**

Instruct each subagent to return findings in this exact delimited format (one block per finding):

```
---FINDING---
priority: P<1|2|3>
location: <file:line>
title: <short title>
category: <Single Responsibility|Abstraction Levels|Meaningful Naming|Testability|API Design|Error Handling Strategy>
pattern: <short label for the underlying anti-pattern, e.g. "module-scope side effects" or "mixed abstraction in handlers" — use the SAME label across findings that share the same root cause>
explanation: <what is wrong and why it matters>
fix: <concrete prescription>
done_when: <verifiable criterion>
---END---
```

If the subagent finds no issues for its batch, it should return `---NO-FINDINGS---`.

#### Collect and merge

After all subagents return:

1. Parse each subagent's structured findings
2. Combine into a single list, sorted by priority (P1 first)
3. Deduplicate: if two findings share the same `location` (file:line) AND the same `category`, keep only the one with the highest priority
4. Group findings by `pattern` label — findings from different subagents that used the same (or very similar) pattern label share a root cause and will be collapsed in the Pattern Collapsing step

#### Error fallback

If a subagent fails or returns unparseable output, review those files directly (as in direct mode) and include a note in the report: `Note: Files [list] were reviewed directly due to subagent failure.`

### Pattern Collapsing

Both direct mode and parallel mode flow into this step before bead creation.

After merging all findings, look for findings that share the **same root cause** — i.e., the same design pattern repeated across multiple files. Examples:

- Multiple files flagged for "module-level side effect blocks testability" → one pattern: "codebase initialises services at module scope instead of using injection"
- Multiple files flagged for "mixed abstraction levels" where the same kind of mixing recurs → one pattern: "business logic is interleaved with infrastructure calls throughout"

When you identify a shared root cause:

1. **Collapse** the N per-file findings into **one finding** that names the pattern, lists all affected files, and prescribes the codebase-wide fix
2. **Set severity** to the highest severity among the collapsed findings
3. **Keep separate** any findings that happen to share a category but have genuinely different root causes

This is critical: N beads for N instances of the same pattern creates noise. One bead that names the pattern and lists the affected locations is actionable.

### Deduplication and Bead Check

Before creating a bead, check if one already exists:
- Run `bd list --status=open` to see all open issues
- Run `bd list --status=closed` to see previously resolved issues
- Compare your findings against existing bead titles and descriptions
- Skip creating beads for issues that already have matching open beads
- **Skip findings where a closed bead's fix introduced the pattern you're flagging.** Use `bd show <id>` on relevant closed beads to read the description and close reason. If the current code is the intentional resolution of a prior bug, do not re-raise it.
- When in doubt, show the user the potential duplicate rather than creating

---

## Design Criteria

### Single Responsibility

Flag when a unit has multiple unrelated reasons to change:
- Functions that do X AND Y (validate AND save, fetch AND transform AND render)
- Classes with unrelated method groups (UserService with email sending and caching)
- Files with unrelated exports
- Modules mixing infrastructure with business logic

Ask: "If requirement X changes, does this code change? What about unrelated requirement Y?"

### Abstraction Levels

Flag when a function mixes high-level intent with low-level details:
- Business logic interleaved with HTTP/DB/file operations
- Algorithm steps mixed with error handling boilerplate
- Policy decisions embedded in mechanism code

Good: each function operates at one level, delegating details to helpers.

### Meaningful Naming

Linters enforce patterns; this checks *meaning*:
- Does `processData` actually explain what processing occurs?
- Does `handleRequest` distinguish itself from other handlers?
- Do similar names (`userService`, `userManager`, `userHelper`) have clear distinct roles?
- Are abbreviations obvious to someone new to the codebase?

Flag: names that pass linter rules but don't reveal intent.

### Testability

Flag architectural decisions that make testing hard:
- Direct instantiation of external services (no injection points)
- Static/global state that persists between tests
- Business logic that can only run with real I/O
- Hidden side effects (function does more than signature suggests)
- Circular dependencies between modules

Ask: "Can I test this unit in isolation with fake dependencies?"

### API Design

Flag interface issues:
- Leaky abstractions (caller must understand implementation details)
- Inconsistent patterns across similar APIs
- Missing or misleading error information
- Temporal coupling (must call A before B, but nothing enforces it)

### Error Handling Strategy

Linters catch empty catches; this checks *appropriateness*:
- Are errors handled at the right level? (not swallowed too early, not leaked too far)
- Do error messages help the *recipient* (user vs developer vs operator)?
- Is the recovery strategy sensible? (retry? fail fast? degrade gracefully?)
- Are error paths tested?

---

## Severity

- **P1**: Code that **cannot** be tested without heroic workarounds (no seam exists even with standard mocking), or security design flaws (authentication bypass, privilege escalation by design). A module-level singleton that can be mocked with `vi.mock()` or `monkey.Patch` is **not** P1 — that's testable, just inconvenient. P1 means "there is no way to isolate this code for testing" or "this design is a security vulnerability."
- **P2**: SRP violations, mixed abstractions, leaky APIs, testability friction (module-level state, hard-coded dependencies that require mocking at import time)
- **P3**: Naming or API issues where you can state a **concrete consequence** — i.e., "a caller/maintainer would likely \<specific mistake\> because of this." Do **not** raise P3 for names or patterns that are merely suboptimal without a realistic misuse or maintenance hazard.

---

## Output

You MUST produce a report following the exact structure shown in [REFERENCE.md](REFERENCE.md). When using parallel mode, the lead assembles the unified report from subagent findings. The report format is identical regardless of execution mode.

**`--create-beads` mode**: Create beads for P1/P2 issues.

Each bead description MUST be structured in three parts:

```
<file:line>

<Explanation of the problem: what is wrong and why it matters.>

Fix: <Concrete prescription of the fix. For API design issues, specify the exact
shape — parameter names, types, signatures — not just the general approach.
Example: "Change `Skill(dir string, prefix ...string)` to `Skill(dir, prefix string)`
where empty string means no prefix" rather than "remove the variadic.">

Done when: <A verifiable completion criterion that can be checked by reading the diff.
Must reference specific functions, files, or observable behaviours.
Example: "Both parseSkillFrontmatter and parseAgentFrontmatter delegate to a shared
parseFrontmatterRaw; no duplicated delimiter-scanning code remains in either function."
NOT: "The duplication is removed.">
```

```bash
bd create --type=bug --priority=<1-3> --title="Code: <specific issue>" \
  --description="<file:line>

<explanation>

Fix: <concrete prescription>

Done when: <verifiable criterion>"
```
