# Example Output

This reference shows the expected format and level of detail for a code review report.

---

## Example Report

```
---
Code Review for src/order

| Priority | Location | Issue | Fix |
|----------|----------|-------|-----|
| P2 | src/order/service.go:87 | OrderService validates, prices, AND persists | Split into validateOrder, priceOrder, saveOrder |
| P2 | src/order/handler.go:23 | HTTP parsing mixed with discount business logic | Move discount rules to domain layer |
| P1 | src/order/repo.go:14 | Direct DB connection with no injection point | Accept a db interface parameter |
| P3 | src/order/handler.go:61 | `processOrder` doesn't distinguish from other handlers | Rename to `handleCheckout` |

4 files reviewed, 4 issues found.

## Findings

### 1. OrderService has three unrelated reasons to change
**Location:** src/order/service.go:87

PlaceOrder validates input, calculates pricing with discount rules, and writes to the database in one 90-line function. A pricing policy change forces edits to the same function as a validation rule change. Extract validateOrder, priceOrder, and saveOrder so each has a single reason to change.

### 2. HTTP handler embeds discount business logic
**Location:** src/order/handler.go:23

The handler parses the HTTP request, then inline-calculates volume discounts before calling the service. Discount rules belong in the domain layer so they can be tested without an HTTP context and reused from other entry points (CLI, queue consumer).

### 3. Repository directly instantiates database connection
**Location:** src/order/repo.go:14

NewOrderRepo calls sql.Open internally, making it impossible to test with a fake database or swap drivers. Accept a *sql.DB (or an interface) as a parameter so callers control the connection lifecycle.

### 4. Handler name doesn't reveal intent
**Location:** src/order/handler.go:61

`processOrder` is indistinguishable from `handleOrder` or `doOrder`. Since this handler specifically processes checkout submissions, rename to `handleCheckout` to convey the specific action.

---
To create beads for these findings, re-run with --create-beads
```

---

## Format Rules

### Issue table: Priority / Location / Issue / Fix

```
| Priority | Location | Issue | Fix |
|----------|----------|-------|-----|
| P2 | src/order/service.go:87 | OrderService validates, prices, AND persists | Split into three focused functions |
```

### Only show issues found — no passing rows

Do not include items that passed review. End with "N files reviewed, M issues found."

### Findings section: Use H3 headers with Location and explanation

```
### 1. OrderService has three unrelated reasons to change
**Location:** src/order/service.go:87

Explanation of the design problem and rationale for the fix.
```

### No Summary table

Do not include a Summary table counting issues — the Findings section already lists them.

### NEVER use ASCII box-drawing characters

Do not use `─`, `│`, `┌`, `┐`, `└`, `┘`, `├`, `┤`, `┬`, `┴`, `┼` or similar characters for tables or separators.

### Priority maps to bead creation

P1/P2/P3 map directly to `--priority=1`, `--priority=2`, `--priority=3` in bead creation commands.
