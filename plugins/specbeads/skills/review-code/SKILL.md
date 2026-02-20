---
name: review-code
description: Review code for design issues that static analysis misses. Checks single responsibility, abstraction levels, testability, and meaningful naming. Use when asked to review code, find design problems, or improve code quality.
---

# Code Review

Review code for design and architecture issues that linters and static analysis tools miss.

> [!IMPORTANT]
> Consult `REFERENCE.md` in this skill directory for the expected output format and level of detail.

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

1. Read/explore code in the specified path
2. Evaluate against design criteria below (skip mechanical checks tools handle)
3. Check for existing beads: `bd list --status=open` and `bd list --status=closed`
4. For each issue found, skip if a bead already exists (open or closed) with matching file/issue
5. For closed beads, check whether the current code **is the fix** — if so, do not re-raise
6. Create beads only for new P1/P2 issues

### Deduplication

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

- **P1**: Architectural issues blocking testability, security design flaws
- **P2**: SRP violations, mixed abstractions, leaky APIs
- **P3**: Naming unclear but functional, minor API inconsistencies

---

## Output

You MUST produce a report following the exact structure shown in `REFERENCE.md`.

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
