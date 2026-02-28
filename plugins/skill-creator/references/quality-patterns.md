# Quality Patterns

Patterns for organizing skill content, structuring workflows, formatting output, writing scripts, and avoiding common mistakes.

## Progressive Disclosure Patterns

### Pattern 1: High-Level Guide with References

Keep SKILL.md lean by linking to reference files for advanced or variant-specific content:

```markdown
# PDF Processing

## Quick Start
Extract text with pdfplumber:
[code example]

## Advanced Features
- **Form filling**: See [references/forms.md](references/forms.md)
- **API reference**: See [references/api.md](references/api.md)
- **Examples**: See [references/examples.md](references/examples.md)
```

Claude loads each reference only when needed.

### Pattern 2: Domain-Specific Organization

For skills spanning multiple domains or frameworks, organize by variant so Claude only loads the relevant one:

```
bigquery-skill/
├── SKILL.md (overview and navigation)
└── references/
    ├── finance.md (revenue, billing metrics)
    ├── sales.md (opportunities, pipeline)
    └── product.md (API usage, features)
```

When a user asks about sales metrics, Claude reads only `sales.md`.

Similarly for multi-framework skills:

```
cloud-deploy/
├── SKILL.md (workflow + provider selection)
└── references/
    ├── aws.md
    ├── gcp.md
    └── azure.md
```

### Pattern 3: Conditional Details

Show basic content inline, link to advanced content:

```markdown
# DOCX Processing

## Creating Documents
Use docx-js for new documents. See [references/docx-js.md](references/docx-js.md).

## Editing Documents
For simple edits, modify the XML directly.

**For tracked changes**: See [references/redlining.md](references/redlining.md)
```

## Workflow Patterns

### Sequential Workflows

For multi-step processes, provide a clear overview before the detailed steps:

```markdown
Filling a PDF form involves these steps:

1. Analyze the form (run analyze_form.py)
2. Create field mapping (edit fields.json)
3. Validate mapping (run validate_fields.py)
4. Fill the form (run fill_form.py)
5. Verify output (run verify_output.py)
```

Then expand each step below the overview.

### Conditional Workflows

For tasks with branching logic, guide through decision points:

```markdown
1. Determine the modification type:
   **Creating new content?** → Follow "Creation workflow" below
   **Editing existing content?** → Follow "Editing workflow" below

2. Creation workflow: [steps]
3. Editing workflow: [steps]
```

### Feedback Loop Workflows

For iterative processes, make the loop explicit:

```markdown
1. Generate initial output
2. Validate against requirements
3. If validation fails:
   - Identify the gap
   - Adjust the approach
   - Return to step 1
4. When validation passes, finalize output
```

Specify the maximum number of iterations and what to do if the loop doesn't converge.

## Output Patterns

### Template Pattern

For skills that produce structured output, provide a template. Match strictness to needs.

**Strict** (API responses, data formats):

```markdown
## Report Structure
ALWAYS use this exact template:

# [Analysis Title]
## Executive Summary
[One-paragraph overview]
## Key Findings
- Finding 1 with data
- Finding 2 with data
## Recommendations
1. Specific recommendation
2. Specific recommendation
```

**Flexible** (adaptive content):

```markdown
## Report Structure
Sensible default — adapt as needed:

# [Analysis Title]
## Executive Summary
[Overview]
## Key Findings
[Adapt sections based on discoveries]
## Recommendations
[Tailor to context]
```

### Examples Pattern

When output quality depends on style, provide input/output pairs:

```markdown
## Commit Message Format

**Example 1:**
Input: Added user authentication with JWT tokens
Output:
feat(auth): implement JWT-based authentication

Add login endpoint and token validation middleware

**Example 2:**
Input: Fixed bug where dates displayed incorrectly
Output:
fix(reports): correct date formatting in timezone conversion

Use UTC timestamps consistently across report generation
```

Examples convey style more effectively than descriptions alone.

## Executable Code Best Practices

### Solve Complete Problems

Scripts should solve the complete problem they address. Avoid:

- Placeholder logic ("TODO: implement actual logic")
- Magic numbers without explanation
- "Adjust as needed" stubs that defer the real work to Claude

### Verifiable Intermediate Outputs

Where possible, scripts should produce intermediate outputs that Claude can inspect to verify correctness before proceeding:

```python
# Good: Produces a validation report Claude can check
def validate_mapping(mapping):
    report = check_all_fields(mapping)
    print(json.dumps(report, indent=2))
    return report
```

### Utility Scripts

Keep scripts focused on a single task. A script that does one thing well is more reusable than a Swiss Army knife. Name scripts after what they do: `rotate_pdf.py`, `validate_fields.py`, `extract_schema.py`.

## Anti-Patterns

### Windows-Style Paths

Never use backslashes in file paths within skill content. Skills run in Unix-like environments. Use forward slashes (`references/api.md`), not backslashes (`references\api.md`).

### Too Many Options Without Guidance

Don't present a long list of options without helping Claude choose:

```markdown
# Bad: List without selection guidance
Supports: React, Vue, Svelte, Angular, Solid, Preact, Qwik, Lit, Alpine...

# Good: Opinionated with fallback
Default to React. If the user specifies another framework, adapt accordingly.
```

### Over-Explaining What Claude Already Knows

Don't explain general programming concepts, common libraries, or standard practices. Claude already knows these. Focus on what's specific to *this* skill.

```markdown
# Bad: Teaching Claude what JSON is
JSON (JavaScript Object Notation) is a lightweight data format...

# Good: Telling Claude the specific schema
Output must match this schema: { "status": "pass"|"fail", "findings": [...] }
```

### Extraneous Files

Don't create files that exist for organizational aesthetics rather than functional need. Every file must directly support the skill's purpose. Common offenders:

- README.md inside a skill directory
- CHANGELOG.md
- CONTRIBUTING.md
- Empty placeholder files

### Nested References

Keep references one level deep from SKILL.md. A reference file should never link to another reference file as required reading — this creates a context-loading chain that's hard for Claude to navigate efficiently.

```
# Good: Flat references
SKILL.md → references/patterns.md
SKILL.md → references/api.md

# Bad: Nested chain
SKILL.md → references/overview.md → references/details.md → references/edge-cases.md
```
