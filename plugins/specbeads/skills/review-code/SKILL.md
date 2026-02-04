---
name: sb-review-code
description: Review code for quality, security, and readability. Checks function size, naming, single responsibility, testability, concurrency, and security. Use when asked to review code, find bugs, audit code, check for issues, or improve code quality.
---

# Code Review

Review code in the specified path for quality, security, and readability issues.

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Argument Parsing

Parse `$ARGUMENTS` for:
- **Path**: Required path to review (file or directory)
- **`--create-beads`**: Create beads for findings (default: report only)

## Workflow

1. Read/explore code in the specified path
2. Evaluate against quality criteria below
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

## Quality Criteria

### Function Size & Complexity

| Smell | Threshold | Refactoring |
|-------|-----------|-------------|
| Long function | > 20 lines | Extract method per logical block |
| Too many parameters | > 3 params | Parameter object or builder |
| High cyclomatic complexity | > 10 paths | Split functions, use polymorphism |
| Deep nesting | > 3 levels | Guard clauses, early returns, extract |
| Mixed abstraction levels | High + low together | Extract low-level to helpers |
| Flag arguments | Boolean changes behavior | Split into two functions |

### Single Responsibility

Flag when a unit has multiple unrelated reasons to change:
- Functions that do X AND Y (validate AND save)
- Classes with unrelated method groups
- Files with unrelated exports

### Naming

| Element | Look For |
|---------|----------|
| Functions | Verbs: `calculateTotal` not `process` |
| Booleans | Predicates: `isValid` not `flag` |
| Variables | Intent: `userCount` not `n` |
| Constants | Meaning: `MAX_RETRIES` not `THREE` |

Flag: generic names (`handle`, `data`, `tmp`), abbreviations, redundant context.

### Code Organization

- Functions read top-to-bottom (high-level first, helpers below)
- Related functions grouped together
- Public API separated from implementation
- One abstraction level per function

### Duplication

| Type | Fix |
|------|-----|
| Identical blocks | Extract to shared function |
| Same pattern, different data | Extract with parameters |
| Same idea, different impl | Unify approach |

Rule of three: refactor on third occurrence.

### Testability

Flag code that's hard to test:
- Direct instantiation of external services (no injection)
- Static/global state access
- Business logic mixed with I/O
- Hidden side effects
- Large setup requirements

---

## Concurrency

| Issue | Severity |
|-------|----------|
| Shared mutable state without sync | Critical |
| Inconsistent lock ordering | Critical |
| Concurrent map/slice access (Go) | Critical |
| Thread/goroutine leaks | Major |
| Unbuffered channel blocking | Major |

---

## Error Handling

| Issue | Fix |
|-------|-----|
| `catch {}` or `_ = err` | Log, wrap, or propagate |
| Ignored return values | Check all errors |
| Stack traces in user errors | Sanitize messages |
| `throw new Error("failed")` | Specific error types |

---

## Resource Management

| Issue | Fix |
|-------|-----|
| Unclosed files/connections | `defer`/`finally`/`with`/RAII |
| Missing cleanup | Add in same scope as acquisition |
| DB connections not returned | Use pooling with proper release |

---

## Security

| Issue | Severity |
|-------|----------|
| String concat in SQL/commands | Critical |
| Unescaped output (XSS) | Critical |
| Hardcoded secrets | Critical |
| Missing input validation at boundaries | Major |
| Unsanitized deserialization | Major |
| Path traversal | Major |

---

## Severity

- **Critical** (P1): Security vulnerabilities, data corruption, race conditions
- **Major** (P2): SRP violations, testability blockers, error handling gaps, functions > 50 lines
- **Minor** (P3): Style issues, naming nitpicks, minor duplication

---

## Output Format

For each issue: file:line, severity, specific problem, and concrete fix.

**Default mode**: List issues in a table:

| Severity | File:Line | Issue | Fix |
|----------|-----------|-------|-----|
| major | auth.go:142 | `processUser` is 87 lines, 5 nesting levels | Extract validation (145-160), transform (165-190), persist (195-220) |
| major | user.ts:55 | Generic name `handle` | Rename: `createUserAccount` |
| minor | config.go:12 | Magic number `86400` | Extract: `SECONDS_PER_DAY` |

**`--create-beads` mode**: Create beads for critical/major issues:
```bash
bd create --type=bug --priority=<1-3> --title="Code: <specific issue>" --description="<file:line, explanation, and suggested fix>"
```
