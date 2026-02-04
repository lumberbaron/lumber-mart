# Example Output

This reference shows the expected format and level of detail for a spec review report.

---

## Example Report

```
---
Spec Review for specs/003-user-authentication

Documents Reviewed
- spec.md: Yes
- plan.md: Yes
- constitution.md: Yes

---
## 4.1 Specification Conformance Analysis

### Functional Requirements vs Implementation

| FR | Requirement | Status | Evidence |
|----|-------------|--------|----------|
| FR-003 | System shall lock accounts after 5 failed login attempts | ⚠️ PARTIAL | src/auth/login.ts:45 |
| FR-004 | System shall support password reset via email with 24-hour token expiry | ❌ GAP | src/auth/reset.ts:31 |
| FR-006 | System shall support optional TOTP-based 2FA | ❌ GAP | — |

4 passed, not shown.

### Acceptance Criteria Coverage

| User Story | Scenario | Status | Evidence |
|------------|----------|--------|----------|
| US1-3 | User exceeds login attempts and account is locked | ⚠️ PARTIAL | src/auth/login.ts:45 |
| US2-2 | User clicks expired reset link and sees appropriate error | ❌ GAP | src/auth/reset.ts:58 |
| US3-1 | User enables 2FA and must enter code on subsequent logins | ❌ GAP | — |

3 passed, not shown.

---
## 4.2 Architecture Consistency (plan.md)

| Plan Declaration | Status | Evidence |
|------------------|--------|----------|
| Use Passport.js for OAuth providers | ⚠️ PARTIAL | src/auth/passport.ts:12 |
| Rate limiting via express-rate-limit at 100 req/min | ❌ GAP | — |

3 passed, not shown.

---
## 4.3 Constitution Alignment

| Principle | Status | Evidence |
|-----------|--------|----------|
| IV. Public endpoints must be rate-limited | ❌ GAP | src/routes/auth.ts:8 |

4 passed, not shown.

---
## Findings

### 1. Login attempt threshold mismatch
**Ref:** FR-003 / US1-3

Spec requires lockout after 5 failed attempts, but implementation uses hardcoded threshold of 3 in login.ts:45. Causes premature lockouts.

### 2. Password reset token expiry not enforced
**Ref:** FR-004 / US2-2

Spec requires 24-hour token expiry. Tokens generated with expiry (reset.ts:31) but verification (reset.ts:58) only checks validity, not expiration.

### 3. TOTP-based 2FA not implemented
**Ref:** FR-006 / US3-1

Spec lists optional TOTP 2FA as requirement. No implementation exists - no DB fields, no QR generation, no verification endpoints.

### 4. OAuth providers incomplete
**Ref:** Plan

Plan specifies Passport.js for Google, GitHub, Microsoft. Only Google implemented. GitHub and Microsoft strategy files missing.

### 5. Rate limiting missing
**Ref:** Plan

Plan requires express-rate-limit at 100 req/min. No rate limiting middleware configured. Also violates Constitution IV.

### 6. Public endpoints unprotected
**Ref:** Constitution IV

/auth/login and /auth/reset accessible without rate limiting, vulnerable to brute force attacks.

---
To create beads for these findings, re-run with --create-beads
```

---

## Format Rules

### Validation tables: Only show non-passing items

- Show only ⚠️ PARTIAL and ❌ GAP rows
- End each table with "N passed, not shown."
- Evidence column is just `file:line` (or `—` if no specific location)

```
| FR | Requirement | Status | Evidence |
|----|-------------|--------|----------|
| FR-003 | System shall lock accounts after 5 failed attempts | ⚠️ PARTIAL | src/auth/login.ts:45 |
| FR-006 | System shall support optional TOTP-based 2FA | ❌ GAP | — |

2 passed, not shown.
```

### Findings section: Use H3 headers with Ref and explanation

```
### 1. Login attempt threshold mismatch
**Ref:** FR-003 / US1-3

Spec requires lockout after 5 failed attempts, but implementation uses hardcoded threshold of 3.
```

### No Summary table

Do not include a Summary table counting issues—the Findings section already lists them.

### NEVER use ASCII box-drawing characters

Do not use `─`, `│`, `┌`, `┐`, `└`, `┘`, `├`, `┤`, `┬`, `┴`, `┼` or similar characters for tables or separators.
