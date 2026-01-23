# Component Specification Template

Use this template when creating `specs/<feature-name>/<component-name>.md` for individual components.

Component types: Services, Agents, APIs, UIs

## Template Structure

```markdown
# [Component Name] - [One-Line Purpose]

## Quick Reference

- **Key Decision**: [One-sentence design choice for this component]
- **Status**: Design Phase | In Progress | Complete
- **Dependencies**: [Libraries, APIs this component requires]

---

## Purpose

[1-2 paragraph description of what this component does and why it exists. Explain the WHY, not just the WHAT.]

---

## Design Overview

**[Component Type]**: [Brief description] (e.g., "Service Module", "Agent with Tools", "REST API", "React Component")

**[Pattern]**: [Architecture pattern used] (e.g., "Singleton Pattern", "Agent with Tools", "REST API", "React Hooks", "GraphQL Resolver")

[Optionally add other high-level design notes about structure or approach]

---

## Interface ✅ Decided

[Describe the component's public interface in prose. Focus on what it accepts and what it returns, not exact signatures.]

**Inputs**:
- [Input 1]: [Description of what data is expected and any constraints]
- [Input 2]: [Description]

**Outputs**:
- [Output description]: [What the component returns and the key fields/structure]

**Key Behaviors**:
- [Behavior 1]: [When this happens or what it means]
- [Behavior 2]: [When this happens or what it means]

---

## Behavior ⚠️ TBD

[Describe what the component does at a high level. Focus on the WHAT, not the HOW.]

**Primary Workflow**:

1. **[Step 1]**: [What happens from the user/system perspective]
2. **[Step 2]**: [What happens]
3. **[Step 3]**: [What happens]

[Continue for key steps - focus on observable behavior, not implementation details]

---

## Error Handling

**Error Scenarios**:
1. **[Error Type 1]**: [How it should be handled] (e.g., "API unavailable: Retry with backoff, then graceful degradation")
2. **[Error Type 2]**: [How it should be handled]
3. **[Error Type 3]**: [How it should be handled]

**Graceful Degradation**: [How the component should behave when dependencies fail or data is incomplete]

---

## Architecture Conformance

### Agent Conformance [Skip if not an agent]
- [ ] Agent instructions describe capabilities and domain
- [ ] Agent instructions list available tools
- [ ] Agent instructions do NOT reference other agents by name
- [ ] Agent instructions do NOT prescribe orchestrator behavior

### REST API Conformance [Skip if not a REST API]
- [ ] Success responses use `{ "data": {...}, "meta": {...} }` envelope
- [ ] Error responses use `{ "error": { "code": "...", "message": "..." } }` envelope
- [ ] Pagination uses `page` (1-indexed) and `per_page` (max 100)
- [ ] Error codes follow SCREAMING_SNAKE_CASE format
- [ ] No `status` field in response envelopes

```

## Readiness Indicators

Mark section headers with decision status:

- **✅ Decided** - Implement as written
- **⚠️ TBD** - Needs implementation decision before coding
- **🔄 Placeholder** - Fill during implementation

## Filling Guidelines

- **Quick Reference**: Always fill first - orients readers immediately
- **Purpose**: Explain *why* this component exists, not just what it does
- **Design Overview**: Describe the component type and pattern at a high level
- **Interface**: Describe inputs/outputs in prose - defer exact signatures to implementation
- **Behavior**: Describe what happens from the user/system perspective, not internal details
- **Error Handling**: Document failure modes and recovery expectations
- **Architecture Conformance**: Check applicable items before implementation

## Component-Specific Guidance

- **Service**: Describe responsibilities and key operations
- **Agent**: Describe capabilities, tools, and when it should be invoked
- **API**: Describe endpoints, expected payloads, and response shapes
- **UI**: Describe user interactions and state requirements

## Example Sections

### Example Quick Reference

```markdown
## Quick Reference

- **Key Decision**: Using Vision API with structured prompts for reliable label extraction
- **Status**: In Progress
- **Dependencies**: anthropic, pillow
```

### Example Purpose

```markdown
## Purpose

Extract structured product information from photos using Vision API.

This service bridges the gap between user-captured images and the matching system. It handles the extraction of product details from images and returns normalized data that can be used for catalog lookup and inventory search.
```

### Example Error Handling

```markdown
## Error Handling

**Error Scenarios**:
1. **Vision API Errors**: Retry once with backoff, then return error status with message
2. **Invalid Image Format**: Return clear error indicating supported formats
3. **Low Confidence Extraction**: Return results with "low" confidence flag, allow matching to proceed with partial data

**Graceful Degradation**: Missing optional data (category, variant) doesn't block matching. Algorithm adjusts weights dynamically based on available fields.
```
