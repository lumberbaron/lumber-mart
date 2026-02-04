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
| FR-001 | System shall authenticate users via email and password | ✅ PASS | src/auth/login.ts:28 - LoginService.authenticate() validates credentials against bcrypt hash |
| FR-002 | System shall enforce password complexity (min 8 chars, 1 uppercase, 1 number) | ✅ PASS | src/auth/validation.ts:15 - passwordSchema uses zod regex validation |
| FR-003 | System shall lock accounts after 5 failed login attempts | ⚠️ PARTIAL | src/auth/login.ts:45 - Tracks attempts but threshold is hardcoded to 3, not 5 |
| FR-004 | System shall support password reset via email with 24-hour token expiry | ❌ GAP | Token generation exists but expiry check not implemented |
| FR-005 | System shall log all authentication events to audit trail | ✅ PASS | src/auth/audit.ts:12 - AuditLogger.logAuthEvent() called on login/logout/reset |
| FR-006 | System shall support optional TOTP-based 2FA | ❌ GAP | No 2FA implementation found |
| FR-007 | Removed | — | — |


### Acceptance Criteria Coverage

| User Story | Scenario | Status | Notes |
|------------|----------|--------|-------|
| US1-1 | User enters valid credentials and is redirected to dashboard | ✅ | Redirect handled in login.ts:67 |
| US1-2 | User enters invalid password and sees error message | ✅ | Error displayed via AuthError component |
| US1-3 | User exceeds login attempts and account is locked | ⚠️ | Works but uses wrong threshold (3 vs 5) |
| US2-1 | User requests password reset and receives email within 5 minutes | ✅ | Email queued via SendGrid integration |
| US2-2 | User clicks expired reset link and sees appropriate error | ❌ | No expiry validation - accepts any valid token |
| US3-1 | User enables 2FA and must enter code on subsequent logins | ❌ | 2FA not implemented |

---
## 4.2 Architecture Consistency (plan.md)

| Plan Declaration | Status | Evidence |
|------------------|--------|----------|
| Use bcrypt for password hashing with cost factor 12 | ✅ PASS | src/auth/hash.ts:8 - bcrypt.hash(password, 12) |
| Store sessions in Redis with 7-day TTL | ✅ PASS | src/auth/session.ts:22 - redis.setex(key, 604800, data) |
| Authentication middleware in src/middleware/auth.ts | ✅ PASS | File exists with verifyToken() and requireAuth() |
| Use Passport.js for OAuth providers | ⚠️ PARTIAL | Passport configured but only Google implemented, plan mentions GitHub and Microsoft |
| Rate limiting via express-rate-limit at 100 req/min | ❌ GAP | No rate limiting middleware found |

---
## 4.3 Constitution Alignment

| Principle | Status | Notes |
|-----------|--------|-------|
| I. All API endpoints must validate input before processing | ✅ PASS | Zod schemas validate all auth endpoints |
| II. Secrets must never appear in logs or error messages | ✅ PASS | Audit logger redacts password fields |
| III. All database queries must use parameterized statements | ✅ PASS | Prisma ORM handles parameterization |
| IV. Public endpoints must be rate-limited | ❌ GAP | Login endpoint has no rate limiting |
| V. Authentication tokens must be cryptographically signed | ✅ PASS | JWT signed with RS256 algorithm |

---
## Summary

| Category | Issues Found |
|----------|--------------|
| Specification conformance | 4 |
| Architecture consistency | 2 |
| Constitution alignment | 1 |
| **Total** | **7** |

---
## Findings

| # | Ref | Title | Explanation |
|---|-----|-------|-------------|
| 1 | FR-003 / US1-3 | Login attempt threshold mismatch | Spec requires lockout after 5 failed attempts, but implementation uses hardcoded threshold of 3 in login.ts:45. Causes premature lockouts. |
| 2 | FR-004 / US2-2 | Password reset token expiry not enforced | Spec requires 24-hour token expiry. Tokens generated with expiry (reset.ts:31) but verification (reset.ts:58) only checks validity, not expiration. |
| 3 | FR-006 / US3-1 | TOTP-based 2FA not implemented | Spec lists optional TOTP 2FA as requirement. No implementation exists - no DB fields, no QR generation, no verification endpoints. |
| 4 | Plan | OAuth providers incomplete | Plan specifies Passport.js for Google, GitHub, Microsoft. Only Google implemented. GitHub and Microsoft strategy files missing. |
| 5 | Plan | Rate limiting missing | Plan requires express-rate-limit at 100 req/min. No rate limiting middleware configured. Also violates Constitution IV. |
| 6 | Constitution IV | Public endpoints unprotected | /auth/login and /auth/reset accessible without rate limiting, vulnerable to brute force attacks. |

---
To create beads for these findings, re-run with --create-beads
```

---

## Wrong Formats (Do Not Use)

The following formats are **WRONG**. Never produce output like this.

### WRONG: Key-value pairs with horizontal lines

```
FR: FR-001
Requirement: System shall authenticate users via email and password
Status: ✅ PASS
Evidence: src/auth/login.ts:28 - LoginService.authenticate() validates credentials
────────────────────────────────────────
FR: FR-002
Requirement: System shall enforce password complexity
Status: ⚠️ PARTIAL
Evidence: src/auth/validation.ts:15 - passwordSchema uses zod regex
────────────────────────────────────────
```

### WRONG: ASCII box-drawing tables

```
┌───────────────────────────────────────┬─────────┬────────────────────────────┐
│              Principle                │ Status  │           Notes            │
├───────────────────────────────────────┼─────────┼────────────────────────────┤
│ I. All API endpoints must validate    │ ✅ PASS │ Zod schemas validate all   │
├───────────────────────────────────────┼─────────┼────────────────────────────┤
│ II. Secrets must never appear in logs │ ✅ PASS │ Audit logger redacts       │
└───────────────────────────────────────┴─────────┴────────────────────────────┘
```

### CORRECT: Markdown pipe-delimited tables only

```
| FR | Requirement | Status | Evidence |
|----|-------------|--------|----------|
| FR-001 | System shall authenticate users via email and password | ✅ PASS | src/auth/login.ts:28 - LoginService.authenticate() validates credentials |
| FR-002 | System shall enforce password complexity | ⚠️ PARTIAL | src/auth/validation.ts:15 - passwordSchema uses zod regex |
```

Use this format for ALL tabular data in the report.
