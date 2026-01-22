# Story Specification Template

Use this template when creating `specs/<feature-name>/overview.md` for initial proposals or smaller features.

## Template Structure

```markdown
# [Feature Name] - Feature Story

## Quick Reference

- **Files**: `path/to/main.py`, `configs/agent.yaml`
- **Key Decision**: [One-sentence architectural choice]
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

---

## Problem Statement

[Describe the problem this feature solves:]
- Current pain point 1
- Current pain point 2
- Current pain point 3

[One sentence explaining why the current state is insufficient]

---

## Solution

[Describe the solution approach in 3-5 numbered points:]

1. [High-level approach - what the system does]
2. [Key technology or methodology used]
3. [How it integrates with existing system]

**Key Insight**: [One sentence capturing the core insight that makes this solution work]

---

## Success Criteria ✅ Decided

- [ ] [Measurable criterion 1] (e.g., "Response time <2 seconds")
- [ ] [Measurable criterion 2] (e.g., "Accuracy >90%")
- [ ] [Measurable criterion 3] (e.g., "Works on mobile and desktop")

---

## Implementation Approach ⚠️ TBD

[High-level description of how this will be built:]

**Components Involved**:
- [Component 1]: [What it does for this feature]
- [Component 2]: [What it does for this feature]

**Key Steps**:
1. [Step 1]
2. [Step 2]
3. [Step 3]

---

## Open Questions

- [ ] [Question 1 that needs resolution]
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
- **User Story**: Full details here (user need, use case, key features) - this is the authoritative source
- **Problem Statement**: 3-5 bullet points showing user pain
- **Solution**: Keep high-level, defer details to implementation
- **Success Criteria**: Must be measurable and testable

## When to Use This Template

Use story_template.md for:
- Initial feature proposals
- Small features (1-2 components)
- Features that don't require deep architectural decisions
- Exploratory specs before committing to full architecture

For multi-component features or architectural changes, use architecture_template.md instead.
