# Component Specification Template

Use this template when creating `specs/<feature-name>/<component-name>.md` for individual components.

Component types: Services, Agents, APIs, UIs

## Template Structure

```markdown
# [Component Name] - [One-Line Purpose]

## Quick Reference

- **Files**: `src/services/component.py`, `configs/agents/component.yaml`
- **Key Decision**: [One-sentence design choice for this component]
- **Status**: Design Phase | In Progress | Complete
- **Dependencies**: [Libraries, APIs this component requires]

---

## Purpose

[1-2 paragraph description of what this component does and why it exists. Explain the WHY, not just the WHAT.]

---

## Design Overview

**[Component Type]**: `[file path or module]` (e.g., "Service Module: `src/services/vision_service.py`", "Agent Config: `configs/agents/catalog.yaml`", "React Component: `src/components/CameraCapture.tsx`")

**[Pattern]**: [Architecture pattern used] (e.g., "Singleton Pattern", "Agent with Tools", "REST API", "React Hooks", "GraphQL Resolver")

[Optionally add other high-level design notes about structure or approach]

---

## Architecture

### Dependencies

```[toml|json|yaml|package.json]
# [Config file name]
[Actual dependencies with versions]
```

### Environment Configuration

```env
# [Environment file or config]
[ENV_VAR_1]="[description or example]"
[ENV_VAR_2]="[description or example]"
```

### Shared Config Integration [Skip if standalone]

```yaml
# [Config file path]
[Relevant configuration block]
```

---

## Core [Method|Workflow|API|Interface] ✅ Decided

### `[function_name]([params]) -> [return_type]`

**Input**:
- `[param1]`: [type] - [description]
- `[param2]`: [type] - [description]

**Output**: [Prose description of returned data structure and key fields]

**[Additional Details Section]** (e.g., "Status Codes", "Confidence Levels", "Event Types"):
- `[value1]`: [When this occurs or what it means]
- `[value2]`: [When this occurs or what it means]

---

## [Implementation|Workflow] ⚠️ TBD

### [Step-by-Step Process or Key Methods]

**[Workflow Name]** ([X] steps):

1. **[Step 1]**: [Detailed description of what happens]
2. **[Step 2]**: [Detailed description of what happens]
3. **[Step 3]**: [Detailed description of what happens]
[Continue for all steps in the workflow]

### Helper Functions [Skip if none needed]

#### `[helper_function]([params])`

**Purpose**: [One sentence explaining what this does]

**Steps**:
1. [Step 1]
2. [Step 2]

Implementation details deferred to development phase.

---

## Error Handling

**Error Scenarios**:
1. **[Error Type 1]**: [How it's handled] (e.g., "HTTP 500 errors: Retry with exponential backoff")
2. **[Error Type 2]**: [How it's handled] (e.g., "Invalid input: Return error status with descriptive message")
3. **[Error Type 3]**: [How it's handled] (e.g., "Service unavailable: Graceful degradation to cached data")

**Graceful Degradation**: [How the component behaves when dependencies fail or data is incomplete]

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

---

## Performance ⚠️ TBD

**Targets**:
- **[Metric 1]**: [Target with unit] (e.g., "<2 seconds per request")
- **[Metric 2]**: [Target with unit] (e.g., "<100ms p95 latency")

**Optimization Strategies** [Skip for MVPs]:
- [Strategy 1] (e.g., "Image resizing to reduce token usage by 70%")
- [Strategy 2] (e.g., "Caching frequently accessed catalog data for 5 minutes")

**Cost** [Skip if not API-based]:
- ~$[amount] per [operation]

---

## Testing 🔄 Placeholder

### Unit Tests

**Test Cases**:
- [Test case 1]: [What to verify] (e.g., "Valid input data returns success status")
- [Test case 2]: [What to verify] (e.g., "Invalid image format returns descriptive error")
- [Test case 3]: [What to verify] (e.g., "Edge case handling for missing optional fields")

Test implementation deferred to development phase.

### Integration Tests

**Scenarios**:
- [Scenario 1]: [What to test] (e.g., "End-to-end flow with real API endpoints")
- [Scenario 2]: [What to test] (e.g., "Error handling with mocked service failures")

---

## Deployment [Skip for MVPs]

**[Deployment Notes]**: [How this component is deployed, configured, or integrated]

**[Environment Variables]**: [Production-specific configuration requirements]

**[Monitoring]**: [What metrics or logs to monitor] (e.g., "API latency, error rates, cost per request")

[Optional: Add migration notes, rollout strategy, database migrations, or infrastructure requirements]
```

## Readiness Indicators

Mark section headers with decision status:

- **✅ Decided** - Implement as written
- **⚠️ TBD** - Needs implementation decision before coding
- **🔄 Placeholder** - Fill during implementation

## Filling Guidelines

- **Quick Reference**: Always fill first - orients readers immediately
- **Purpose**: Explain *why* this component exists, not just what it does
- **Architecture**: Include actual file paths, module names, config snippets
- **Core API/Interface**: Show exact input/output structure with types
- **Workflow**: Number steps clearly, be specific about what happens
- **Error Handling**: Document specific failure modes and recovery strategies
- **Architecture Conformance**: Check applicable items before implementation
- **Performance**: Include specific numeric targets where applicable
- **Testing**: Describe test scenarios and expected behaviors (no code)

## Component-Specific Guidance

- **Service**: Python module with functions/classes (e.g., `src/services/vision_service.py`)
- **Agent**: SAM config + tools module (e.g., `configs/agents/catalog.yaml` + `src/tools/catalog_tools.py`)
- **API**: HTTP endpoints with request/response schemas
- **UI**: React components with props/state

## Example Sections

### Example Quick Reference

```markdown
## Quick Reference

- **Files**: `src/services/vision_service.py`, `src/tools/vision_tools.py`
- **Key Decision**: Using Vision API with structured prompts for reliable label extraction
- **Status**: In Progress
- **Dependencies**: anthropic>=0.18.0, pillow>=10.0.0
```

### Example Purpose

```markdown
## Purpose

Extract structured product information from photos using Vision API.

This service bridges the gap between user-captured images and the matching system. It handles image preprocessing, calls the Vision API with structured prompts, and returns normalized data that can be used for catalog lookup and inventory search.
```

### Example Error Handling

```markdown
## Error Handling

**Error Scenarios**:
1. **Vision API Errors**: Retry once with exponential backoff (1s delay), then return error status with message
2. **Invalid Image Format**: Preprocess to convert unsupported formats to JPEG, or return clear error
3. **Low Confidence Extraction**: Return results with "low" confidence flag, allow matching to proceed with partial data
4. **Catalog Lookup Failure**: Continue matching with user-provided name (bypass normalization)
5. **Inventory Search Empty**: Match without price/availability data, note in response

**Graceful Degradation**: Missing optional data (category, variant) doesn't block matching. Algorithm adjusts weights dynamically based on available fields.
```
