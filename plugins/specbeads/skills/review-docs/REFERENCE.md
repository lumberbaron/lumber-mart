# Example Output

This reference shows the expected format and level of detail for a documentation review report.

---

## Example Report

```
---
Documentation Review for .

| Priority | Location | Issue | Fix |
|----------|----------|-------|-----|
| P1 | README.md:45 | Quick start runs `make seed` which drops and recreates DB | Add warning or use non-destructive seed command |
| P2 | docs/api.md:23 | curl example uses deleted /v1/users endpoint | Update to /v2/users with new auth header |
| P3 | backend/CLAUDE.md | Missing entry for migrations/ directory | Add migrations/ row to index table |
| P3 | README.md:12 | No expected output shown after docker compose up | Add "You should see: ..." block |
| P4 | frontend/README.md:8 | "Setup" and "Installation" used interchangeably | Standardize on "Setup" throughout |

8 files reviewed, 5 issues found.

## Findings

### 1. Quick start seed command is destructive
**Location:** README.md:45

The quick start instructs users to run `make seed`, which drops all tables before recreating them. A new contributor following these steps on a shared dev database would destroy existing test data. Either add a prominent warning or change to `make seed-safe` which inserts only missing rows.

### 2. API example references deleted endpoint
**Location:** docs/api.md:23

The curl example calls `POST /v1/users` which was removed in the v2 migration. Running the example as-is returns a 404. Update to `POST /v2/users` and include the required `Authorization: Bearer` header that v2 requires.

### 3. CLAUDE.md index missing migrations directory
**Location:** backend/CLAUDE.md

The backend/migrations/ directory contains 12 migration files but has no entry in the CLAUDE.md index table. Add a row: `migrations/` | SQL migration files | Changing database schema.

### 4. No expected output after main setup step
**Location:** README.md:12

After `docker compose up`, the reader has no way to verify success. Add a "You should see:" block showing the expected startup log lines so newcomers can distinguish success from a silent failure.

### 5. Inconsistent terminology for setup section
**Location:** frontend/README.md:8

The frontend README uses "Installation" in its heading but the root README links to it as "Setup". Standardize on "Setup" to match the root README's terminology.

---
To create beads for these findings, re-run with --create-beads
```

---

## Format Rules

### Issue table: Priority / Location / Issue / Fix

```
| Priority | Location | Issue | Fix |
|----------|----------|-------|-----|
| P2 | docs/api.md:23 | curl example uses deleted /v1/users endpoint | Update to /v2/users with new auth header |
```

### Only show issues found — no passing rows

Do not include items that passed review. End with "N files reviewed, M issues found."

### Findings section: Use H3 headers with Location and explanation

```
### 1. Quick start seed command is destructive
**Location:** README.md:45

Explanation of the documentation problem and rationale for the fix.
```

### No Summary table

Do not include a Summary table counting issues — the Findings section already lists them.

### NEVER use ASCII box-drawing characters

Do not use `─`, `│`, `┌`, `┐`, `└`, `┘`, `├`, `┤`, `┬`, `┴`, `┼` or similar characters for tables or separators.

### Priority maps to bead creation

P1/P2/P3/P4 map directly to `--priority=1` through `--priority=4` in bead creation commands. P4 is available for polish-level issues specific to documentation reviews.
