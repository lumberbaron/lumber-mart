# Example Output

This reference shows the expected format and level of detail for a tests review report.

---

## Example Report

```
---
Tests Review for tests/order

| Priority | Location | Issue | Fix |
|----------|----------|-------|-----|
| P1 | tests/order/service_test.go:34 | Shared DB connection mutated across tests | Use per-test setup with t.Cleanup |
| P2 | tests/order/service_test.go:78 | Asserts no error but never checks return value | Assert expected order fields |
| P2 | tests/order/handler_test.go:12 | Test name "TestHandler" doesn't describe scenario | Rename to TestCheckout_AppliesVolumeDiscount |
| P3 | tests/order/repo_test.go:55 | Happy path only — no test for duplicate order ID | Add conflict/duplicate test case |

3 files reviewed, 4 issues found.

## Findings

### 1. Shared mutable state between test cases
**Location:** tests/order/service_test.go:34

A package-level `testDB` variable is opened in TestMain and reused across all tests without resetting state. Tests pass individually but fail when run together because earlier tests leave rows that affect later assertions. Use per-test setup with t.Cleanup to guarantee isolation.

### 2. Assertion checks error only, ignores result
**Location:** tests/order/service_test.go:78

TestPlaceOrder calls PlaceOrder and asserts `err == nil` but never inspects the returned order. If the function silently returns a zero-value order, this test still passes. Assert on expected fields (ID, total, status) to catch real regressions.

### 3. Test name doesn't communicate intent
**Location:** tests/order/handler_test.go:12

"TestHandler" gives no indication of what scenario is being verified. When this test fails in CI, the developer must read the test body to understand what broke. Rename to TestCheckout_AppliesVolumeDiscount to make failures self-describing.

### 4. Missing edge case for duplicate order
**Location:** tests/order/repo_test.go:55

Only the happy path (create new order) is tested. There is no test for what happens when an order with the same ID already exists. Add a test that inserts a duplicate and asserts the expected conflict error.

---
To create beads for these findings, re-run with --create-beads
```

---

## Format Rules

### Issue table: Priority / Location / Issue / Fix

```
| Priority | Location | Issue | Fix |
|----------|----------|-------|-----|
| P1 | tests/order/service_test.go:34 | Shared DB connection mutated across tests | Use per-test setup with t.Cleanup |
```

### Only show issues found — no passing rows

Do not include items that passed review. End with "N files reviewed, M issues found."

### Findings section: Use H3 headers with Location and explanation

```
### 1. Shared mutable state between test cases
**Location:** tests/order/service_test.go:34

Explanation of the test quality problem and rationale for the fix.
```

### No Summary table

Do not include a Summary table counting issues — the Findings section already lists them.

### NEVER use ASCII box-drawing characters

Do not use `─`, `│`, `┌`, `┐`, `└`, `┘`, `├`, `┤`, `┬`, `┴`, `┼` or similar characters for tables or separators.

### Priority maps to bead creation

P1/P2/P3 map directly to `--priority=1`, `--priority=2`, `--priority=3` in bead creation commands.
