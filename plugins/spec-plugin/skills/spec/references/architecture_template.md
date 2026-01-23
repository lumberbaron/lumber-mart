# Architecture Specification Template

Use this template when creating `specs/<feature-name>/overview.md` for multi-component features, new services, or architectural changes.

## Template Structure

```markdown
# [Feature Name] - Architecture Overview

## Quick Reference

- **Key Decision**: [One-sentence architectural choice, e.g., "Using event-driven architecture for loose coupling"]
- **Status**: Design Phase | In Progress | Complete
- **Dependencies**: [Libraries, APIs, services required]

---

## User Story

**User Need**: As a [user type], I want to [action] so that [benefit].

**Use Case**: [Detailed scenario describing when and how the user would use this feature. Include context, steps, and expected outcomes. 2-3 sentences that tell a concrete story.]

**Key Features**:
- [Feature bullet 1]
- [Feature bullet 2]
- [Feature bullet 3]

**Success Criteria**:
- [Measurable criterion 1] (e.g., "Photo to recommendation in <6 seconds")
- [Measurable criterion 2] (e.g., "Vision accuracy >90% on clear labels")
- [Measurable criterion 3] (e.g., "Works on iOS Safari 14+ and Chrome 90+")

---

## Problem Statement

[Describe the problem this feature solves. Include:]
- Current pain points (bullet list, 3-5 items)
- Why existing solutions don't work
- User context and constraints

---

## Solution

[Describe the solution approach. Include:]

1. [High-level approach - what the system does]
2. [Key technology or methodology used]
3. [How it integrates with existing system]
4. [What makes this solution effective]

**Key Insight**: [One sentence capturing the core insight that makes this solution work]

---

## System Architecture

```
[ASCII/text-based system diagram showing:]
- User-facing components (Mobile, Web, API)
- Backend services and agents
- External integrations (APIs, databases)
- Data flow arrows
- Communication protocols (HTTP, SSE, GraphQL, etc.)

Example structure:
┌─────────────────┐
│   Frontend      │
│   Component     │
└────────┬────────┘
         │ HTTP POST
         ↓
┌─────────────────┐
│   Backend       │
│   Service       │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│   Database      │
└─────────────────┘
```

---

## Component Specifications

### 1. [Component Name](component-file.md)
**Purpose**: [One-line description]
**Key Responsibilities**: [What this component does]

### 2. [Component Name](component-file.md)
**Purpose**: [One-line description]
**Key Responsibilities**: [What this component does]

[Repeat for each major component]

---

## Data Flow

### [Primary Workflow Name]

**End-to-End Flow**:

1. **[Step 1 Name]**: [What happens, where, and why]
2. **[Step 2 Name]**: [What happens, where, and why]
3. **[Step 3 Name]**: [What happens, where, and why]

[Continue for 5-8 steps covering the complete user journey]

---

## Design Decisions

### [Decision 1 Title] ✅ Decided

**Options Considered**:
- **[Option A]**: [Brief description]
- **[Option B]**: [Brief description]
- **[Option C]**: [Brief description]

**Choice**: [Chosen option]

**Rationale**: [Why this option was chosen. Include pros/cons, technical constraints, or user needs that drove the decision]

### [Decision 2 Title] ⚠️ TBD

[Same structure as above - repeat for 2-4 major decisions]

---

## Architecture Conformance

### Agent Conformance [Skip if no agents]
- [ ] Agent instructions describe capabilities and domain
- [ ] Agent instructions list available tools
- [ ] Agent instructions do NOT reference other agents by name
- [ ] Agent instructions do NOT prescribe orchestrator behavior
- [ ] Orchestrator uses capability discovery (no hardcoded routing)
- [ ] Domain tools owned by agents, not orchestrator

### REST API Conformance [Skip if no REST API]
- [ ] Success responses use `{ "data": {...}, "meta": {...} }` envelope
- [ ] Error responses use `{ "error": { "code": "...", "message": "..." } }` envelope
- [ ] Pagination uses `page` (1-indexed) and `per_page` (max 100)
- [ ] Error codes follow SCREAMING_SNAKE_CASE format
- [ ] No `status` field in response envelopes

---

## Security & Privacy

**Data Protection**:
- [Security measure 1] (e.g., "No image logging - photos deleted after processing")
- [Security measure 2] (e.g., "HTTPS-only communication")
- [Security measure 3] (e.g., "Session isolation per user")

**Authentication**: [How users are authenticated, if applicable]

**Rate Limiting**: [If applicable]

---

## Open Questions

- [ ] [Question 1 that needs resolution before implementation]
- [ ] [Question 2 that needs resolution]

[Remove this section when all questions are resolved]
```

## Readiness Indicators

Mark section headers with decision status:

- **✅ Decided** - Implement as written
- **⚠️ TBD** - Needs implementation decision before coding
- **🔄 Placeholder** - Fill during implementation

## Filling Guidelines

- **Quick Reference**: Always fill first - orients readers immediately
- **User Story**: Full details here (user need, use case, features, criteria) - this is the authoritative source
- **Problem Statement**: Keep concise but specific (3-5 bullet points)
- **System Architecture**: Use ASCII art, show data flow clearly
- **Data Flow**: Describe operations in prose; save code for implementation
- **Design Decisions**: Document rationale and trade-offs, not just the choice
- **Architecture Conformance**: Check all applicable items before implementation
- **Security & Privacy**: Document requirements, not implementation details

## When to Use This Template

Use architecture_template.md for:
- Multi-component features (3+ components)
- New agents or services
- Features requiring system design decisions
- Cross-cutting concerns (auth, caching, monitoring)

For simpler features, use story_template.md instead.
