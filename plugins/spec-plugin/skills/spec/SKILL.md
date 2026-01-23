---
name: spec
description: Generate and maintain feature specifications for non-trivial features. Use this skill when implementing multi-component features, new agents/services, architectural changes, or public-facing APIs that require documentation. Also use when updating existing spec'd components after implementation changes.
---

# Spec

## Overview

Generate consistent, comprehensive feature specifications. Specifications document architecture, design decisions, and implementation details for non-trivial features before and during development.

Unless instructed otherwise, specs are always stored in the specs/ directory.

## When to Use This Skill

**Generate specs for:**
- Multi-component implementations (>2 files with different responsibilities)
- New agents or services in the architecture
- Features requiring architectural decisions
- Public-facing APIs or interfaces
- Features with complex workflows or state management

**Update specs when:**
- Implementation changes affect documented architecture
- New components are added to spec'd features
- API contracts are modified

---

## Spec Type Decision Tree

Choose the right template based on feature complexity:

```
Is this a multi-component feature (3+ components)?
├── YES → Use architecture_template.md
│         (System design, data flow, conformance)
└── NO
    │
    Is this a new agent, service, or API?
    ├── YES → Use architecture_template.md + component_template.md
    │         (Architecture overview + detailed component spec)
    └── NO
        │
        Is this an initial proposal or small feature?
        ├── YES → Use story_template.md
        │         (Lightweight, ~100 lines)
        └── NO
            │
            Is this a single component deep-dive?
            └── YES → Use component_template.md
                      (Detailed single component spec)
```

### Template Summary

| Template | Purpose | When to Use |
|----------|---------|-------------|
| `story_template.md` | Lightweight feature story | Initial proposals, small features (1-2 components) |
| `architecture_template.md` | System design | Multi-component features, new services, architectural changes |
| `component_template.md` | Single component spec | Individual agents, services, APIs, UIs |

---

## Section Guidance by Spec Type

### Story Spec (story_template.md)

**Required Sections:**
- Quick Reference
- User Story (full: user need, use case, key features)
- Problem Statement
- Solution
- Success Criteria

**Optional Sections:**
- Implementation Approach (if known)
- Open Questions

### Architecture Spec (architecture_template.md)

**Required Sections:**
- Quick Reference
- User Story (full: user need, use case, key features, success criteria)
- Problem Statement
- Solution
- System Architecture (ASCII diagram)
- Component Specifications (with links)
- Data Flow
- Design Decisions
- Architecture Conformance (checklist)
- Security & Privacy

**Optional Sections:**
- Open Questions

### Component Spec (component_template.md)

**Required Sections:**
- Quick Reference
- Purpose
- Design Overview
- Interface (prose-based, not signatures)
- Behavior (what happens, not how)
- Error Handling
- Architecture Conformance (applicable items only)

---

## Readiness Indicators

Mark section headers with decision status to communicate readiness:

- **✅ Decided** - Implement as written, no further decisions needed
- **⚠️ TBD** - Needs implementation decision before coding
- **🔄 Placeholder** - Fill during implementation, structure is placeholder

Example usage:
```markdown
## Interface ✅ Decided
[Interface is finalized, implement as documented]

## Behavior ⚠️ TBD
[Needs clarification before implementation]

## Error Handling 🔄 Placeholder
[Error scenarios to be defined during implementation]
```

---

## Workflow Decision Tree

**For new features:**
1. Determine spec type using the decision tree above
2. Read the appropriate template(s) from `references/`
3. Follow the "Generating New Specs" workflow below

**For updates to existing features:**
1. Read the existing spec file(s) to understand current documentation
2. Follow the "Updating Existing Specs" workflow below

---

## Generating New Specs

### Step 1: Explore the Codebase

Gather information needed to fill templates:

**Architecture Understanding:**
- Identify affected systems, agents, services, or components
- Understand existing patterns (agent configurations, service modules, API endpoints)
- Note file paths and module names
- Review similar existing features for consistency

**Technical Details:**
- Dependencies from `pyproject.toml`, `package.json`, or other config files
- Database schemas and models
- API request/response formats
- Configuration patterns (YAML structure, environment variables)

**Requirements Clarification:**
- User story and acceptance criteria
- Performance requirements (response time, accuracy, throughput)
- Security constraints
- Integration points with existing systems

### Step 2: Create Directory Structure

```bash
mkdir -p specs/<feature-name>
```

### Step 3: Update User Stories Index

1. Read `specs/user-stories.md` to understand existing format
2. Read `references/user_story_template.md` for index entry structure
3. Add lightweight entry to "Active Stories" section:
   - Epic, Status, Priority
   - User Need (one-line summary)
   - Link to full spec: `[Feature Overview](feature-name/overview.md)`

Full user story details (use case, key features, success criteria) belong in `overview.md`, not the index.

### Step 4: Generate Overview (Story or Architecture)

**For story specs:**
1. Read `references/story_template.md`
2. Create `specs/<feature-name>/overview.md`
3. Fill required sections: Quick Reference, User Story link, Problem Statement, Solution, Success Criteria

**For architecture specs:**
1. Read `references/architecture_template.md`
2. Create `specs/<feature-name>/overview.md`
3. Fill all required sections including System Architecture diagram, Component Specifications, Data Flow, Design Decisions, and Architecture Conformance checklist

### Step 5: Generate Component Specs

For each major component (service, agent, API, UI):

1. Read `references/component_template.md` for structure
2. Create `specs/<feature-name>/<component-name>.md`
3. Fill in sections:
   - **Quick Reference**: Key Decision, Status, Dependencies
   - **Purpose**: 1-2 paragraphs explaining what and why
   - **Design Overview**: Component type, architecture pattern
   - **Interface**: Inputs/outputs in prose (defer exact signatures to implementation)
   - **Behavior**: What happens from user/system perspective (numbered steps)
   - **Error Handling**: Failure modes and recovery expectations
   - **Architecture Conformance**: Check applicable items

4. Component-specific guidance:
   - **Services**: Describe responsibilities and key operations
   - **Agents**: Describe capabilities, tools, and when invoked
   - **APIs**: Describe endpoints, expected payloads, and response shapes
   - **UIs**: Describe user interactions and state requirements

### Step 6: Link Components

Ensure proper navigation:
- User stories index links to overview: `[Feature Overview](feature-name/overview.md)`
- Overview links to components: `[Component](component-name.md)`
- Components link back to overview: `[Overview](overview.md)`

Use relative markdown links throughout. Full user story details live in overview.md; user-stories.md is a lightweight index.

### Step 7: Fill in Specifics

Replace template placeholders with actual values:

**From codebase exploration:**
- Existing patterns and conventions to follow
- Integration points with other systems
- Constraints from current architecture

**From requirements:**
- Security and privacy requirements
- Success criteria that can be measured

**Keep specs focused on requirements, not implementation:**
- Document WHAT to build and WHY (design decisions with rationale)
- Defer HOW to implementation time (exact code, file paths, API signatures, test fixtures)
- Use prose descriptions for interfaces and workflows, not code blocks or signatures
- Specify measurable success criteria
- Describe behaviors from user/system perspective, not internal implementation details
- Omit exact versions, file paths, and configuration details—these are implementation decisions

---

## Updating Existing Specs

### Step 1: Identify Scope

**Read the existing spec** to understand:
- Current structure and sections
- What's changing vs staying the same
- Links to other specs that may need updates

**Determine update type:**
- **Minor update**: Single section change (new field, performance tweak, additional endpoint)
- **Major update**: Multiple sections or architectural changes
- **Regeneration needed**: Complete redesign or tech stack change (use "Generating New Specs" workflow instead)

### Step 2: Update Affected Sections

**Architecture changes** → Update:
- System Architecture diagram
- Data Flow steps
- Component Specifications list
- Architecture Conformance checklist

**New features** → Update:
- Key Features list
- Success Criteria
- Behavior steps

**API changes** → Update:
- Interface section
- Behavior section

### Step 3: Preserve Structure

While updating:
- Keep section headers intact
- Maintain existing formatting conventions
- Preserve unchanged content verbatim
- Update links if file names or structure changes
- Update readiness indicators (✅ ⚠️ 🔄) as decisions are made

### Step 4: Verify Consistency

After updates:
- Ensure all links still work
- Check that status reflects current reality
- Confirm success criteria are still achievable/relevant

---

## Best Practices

### Spec Quality

- **Be specific**: Use concrete numbers, not vague terms (">90% accuracy" not "high accuracy")
- **Requirements over implementation**: Describe WHAT and WHY; defer HOW to implementation
  - Use prose, not code blocks or function signatures
  - Omit file paths, exact versions, and configuration details
  - Focus on observable behaviors, not internal mechanics
- **Document decisions**: Explain why, not just what was chosen
- **Stay current**: Update specs when implementation diverges
- **Link generously**: Connect related specs and components
- **Progressive disclosure**: Full details in overview.md; user-stories.md is a scannable index

### Progressive Disclosure

**Principle**: Information should be organized so readers can find what they need at the appropriate depth without wading through unnecessary detail.

**Applied to specs**:

| Level | File | Purpose | Detail Level |
|-------|------|---------|--------------|
| 1 | `user-stories.md` | Scan all features | One-line summaries, links |
| 2 | `overview.md` | Understand a feature | Full user story, architecture, decisions |
| 3 | `<component>.md` | Implement a component | API details, error handling, tests |

**Key rules**:
- Index files (user-stories.md) link to details, never duplicate them
- Full context lives where it's needed (overview.md has the complete user story)
- Deeper specs link back to parent for navigation

**Applied to templates**:
- Load only the template needed for current task
- Story template is lightest (initial proposals)
- Component template is focused (single component requirements)
- Architecture template is most comprehensive (system design)

### Portability

Specs are self-contained documentation:
- No assumptions about existing specs directory
- Templates work for any project
- All necessary structure embedded in references

### Spec-First Development

Work should conform to specs. If implementation requirements differ from documented design, update the spec first, then implement the change.
