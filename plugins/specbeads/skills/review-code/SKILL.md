---
name: sb-review-code
description: Review code for design issues that static analysis misses. Checks single responsibility, abstraction levels, testability, and meaningful naming. Use when asked to review code, find design problems, or improve code quality.
---

# Code Review

Review code for design and architecture issues that linters and static analysis tools miss.

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
3. Check for existing beads: `bd list --status=open`
4. For each issue found, skip if a bead already exists with matching file/issue
5. Create beads only for new critical/major issues

### Deduplication

Before creating a bead, check if one already exists:
- Run `bd list --status=open` to see all open issues
- Compare your findings against existing bead titles and descriptions
- Skip creating beads for issues that already have matching open beads
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

- **Critical** (P1): Architectural issues blocking testability, security design flaws
- **Major** (P2): SRP violations, mixed abstractions, leaky APIs
- **Minor** (P3): Naming unclear but functional, minor API inconsistencies

---

## Output Format

For each issue: file:line, severity, specific problem, and concrete fix.

**Default mode**: List issues in a table:

| Severity | File:Line | Issue | Fix |
|----------|-----------|-------|-----|
| major | auth.go:42 | `processUser` validates, transforms, AND persists | Extract to `validateUser`, `transformUser`, `saveUser` |
| major | api/handler.ts:15 | HTTP parsing mixed with business logic | Move validation rules to domain layer |
| minor | user.ts:55 | `handleUser` doesn't distinguish from other handlers | Rename: `createUserFromSignup` |

**`--create-beads` mode**: Create beads for critical/major issues:
```bash
bd create --type=bug --priority=<1-3> --title="Code: <specific issue>" --description="<file:line, explanation, and suggested fix>"
```
