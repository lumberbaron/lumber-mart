---
name: spec
description: Generate and maintain feature specifications for non-trivial features. Use this skill when implementing multi-component features, new agents/services, architectural changes, or public-facing APIs that require documentation. Also use when updating existing spec'd components after implementation changes.
---

# Spec

## Overview

Generate consistent, comprehensive feature specifications in the `specs/` directory. Specifications document architecture, design decisions, and implementation details for non-trivial features before and during development.

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
- Performance characteristics change significantly
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

| Template | Lines | Purpose | When to Use |
|----------|-------|---------|-------------|
| `story_template.md` | ~100 | Lightweight feature story | Initial proposals, small features (1-2 components) |
| `architecture_template.md` | ~250 | System design | Multi-component features, new services, architectural changes |
| `component_template.md` | ~180 | Single component deep-dive | Individual agents, services, APIs, UIs |

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

**Conditional Sections:**
- Technology Stack (skip if using existing stack)
- Cost Analysis (skip for MVPs)
- Load Testing (skip for MVPs)

### Component Spec (component_template.md)

**Required Sections:**
- Quick Reference
- Purpose
- Design Overview
- Core API/Interface
- Error Handling
- Architecture Conformance (applicable items only)

**Conditional Sections:**
- Shared Config Integration (skip if standalone)
- Helper Functions (skip if none needed)
- Optimization Strategies (skip for MVPs)
- Cost (skip if not API-based)
- Deployment (skip for MVPs)

---

## Readiness Indicators

Mark section headers with decision status to communicate readiness:

- **✅ Decided** - Implement as written, no further decisions needed
- **⚠️ TBD** - Needs implementation decision before coding
- **🔄 Placeholder** - Fill during implementation, structure is placeholder

Example usage:
```markdown
## Core API ✅ Decided
[API is finalized, implement as documented]

## Performance Targets ⚠️ TBD
[Needs benchmarking before finalizing]

## Testing 🔄 Placeholder
[Test cases to be defined during implementation]
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
   - **Quick Reference**: Files, Key Decision, Status, Dependencies
   - **Purpose**: 1-2 paragraphs explaining what and why
   - **Design Overview**: Component type, file paths, architecture pattern
   - **Architecture**: Dependencies, environment config, integration setup
   - **Core API/Interface**: Input/output structure with types
   - **Implementation/Workflow**: Step-by-step process (numbered steps)
   - **Error Handling**: Specific scenarios with recovery strategies
   - **Architecture Conformance**: Check applicable items
   - **Performance**: Targets, optimization strategies, cost (conditional)
   - **Testing**: Unit and integration test approaches (placeholder)
   - **Deployment**: Configuration, monitoring (conditional)

4. Component-specific guidance:
   - **Services**: Include module path, singleton pattern if applicable
   - **Agents**: Include SAM config path, tools module, workflow steps
   - **APIs**: Include endpoints, request/response schemas, authentication
   - **UIs**: Include component structure, props/state, hooks, styling

### Step 6: Link Components

Ensure proper navigation:
- User stories index links to overview: `[Feature Overview](feature-name/overview.md)`
- Overview links to components: `[Component](component-name.md)`
- Components link back to overview: `[Overview](overview.md)`

Use relative markdown links throughout. Full user story details live in overview.md; user-stories.md is a lightweight index.

### Step 7: Fill in Specifics

Replace template placeholders with actual values:

**From codebase exploration:**
- Real file paths and module names
- Actual dependency versions
- Current configuration patterns
- Existing environment variables

**From requirements:**
- Specific performance targets (e.g., "<6s end-to-end", ">90% accuracy")
- Cost estimates based on API pricing
- Timeline with phases matching project plan

**Keep specs focused on requirements:**
- Document WHAT to build and WHY (design decisions with rationale)
- Defer HOW to implementation time (exact code, API shapes, test fixtures)
- Use prose descriptions, not code blocks, for workflows
- Specify measurable success criteria

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
- Technology Stack
- Architecture Conformance checklist

**New features** → Update:
- Key Features list
- Success Criteria
- Implementation/Workflow steps
- Testing sections

**Performance changes** → Update:
- Performance Targets
- Cost Analysis
- Optimization Strategies

**API changes** → Update:
- Core API/Interface section
- Request/Response schemas
- Integration examples

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
- Check that timeline and status reflect current reality
- Verify code examples match actual implementation
- Confirm success criteria are still achievable/relevant

---

## Best Practices

### Spec Quality

- **Be specific**: Use concrete numbers, not vague terms (">90% accuracy" not "high accuracy")
- **Requirements over implementation**: Describe behaviors and constraints; defer code to implementation
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
- User story index template is smallest (~0.5k tokens)
- Story template is lightweight (~1k tokens)
- Component template is medium (~1.5k tokens)
- Architecture template is largest (~2k tokens)

### Portability

Specs are self-contained documentation:
- No assumptions about existing specs directory
- Templates work for any project
- All necessary structure embedded in references

### Spec-First Development

Work should conform to specs. If implementation requirements differ from documented design, update the spec first, then implement the change.
