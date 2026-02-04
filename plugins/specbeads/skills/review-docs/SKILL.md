---
name: sb-review-docs
description: Review documentation (README.md and CLAUDE.md) for quality, completeness, and consistency. Use when asked to review docs, check documentation, validate README files, or audit CLAUDE.md coverage.
---

# Documentation Review

Review documentation in the specified path (default: entire repository).

> [!IMPORTANT]
> Consult `REFERENCE.md` in this skill directory for the expected output format and level of detail.

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Argument Parsing

Parse `$ARGUMENTS` for:
- **Path**: Optional path to review (default: repo root, reviews all docs)
- **`--create-beads`**: Create beads for findings (default: report only)

## Workflow

1. Run deterministic validation script for structural issues
2. Find all README and CLAUDE.md files in scope
3. Evaluate against quality criteria
4. Check for existing beads: `bd list --status=open`
5. For each issue found, skip if a bead already exists with matching file/issue
6. Create beads only for new issues

### Deterministic Validation

Before manual review, run the validation script for CLAUDE.md structural issues:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/review-docs/scripts/validate-claude-md.py $0 --json
```

Parse the JSON output and include structural issues (missing tables, missing references, index drift) in your findings. The script checks:
- Presence of markdown tables with required columns
- Whether referenced files/directories exist
- Index drift (files not indexed, or index entries pointing to missing files)

### Deduplication

Before creating a bead, check if one already exists:
- Run `bd list --status=open` to see all open issues
- Compare your findings against existing bead titles and descriptions
- Skip creating beads for issues that already have matching open beads
- When in doubt, show the user the potential duplicate rather than creating

## Quality Criteria

### Structure (Progressive Disclosure)

README.md files belong at **component boundaries** — the repo root plus the top-level directory of each major component (e.g., `frontend/`, `backend/`, `infra/`, `docs/`). Most subdirectories within a component should not have their own README. If a directory only needs a brief description and a pointer to its files, a CLAUDE.md index is sufficient.

**Root README.md**:
- Project purpose (why it exists)
- What it does (brief overview)
- Quick start instructions
- Links to component docs
- NO deep architectural details

**Component READMEs** (top-level component dirs only):
- Component's purpose in detail
- Architectural decisions
- Component-specific setup
- Internal APIs/interfaces

Do **not** flag missing READMEs in nested subdirectories (e.g., `src/utils/`, `lib/internal/`). Navigation within a component is handled by CLAUDE.md.

### Content Quality

- **Concise**: No unnecessary words or redundancy
- **Clear**: Jargon explained, unambiguous
- **Accurate**: Examples work, paths exist, commands valid
- **Complete**: Prerequisites listed, all steps included
- **Consistent**: Uniform terminology and formatting

Content Quality applies primarily to README prose. For CLAUDE.md, focus on accuracy (index entries point to real files) and consistency (uniform table format).

### Hidden Knowledge

Good docs surface things newcomers can't discover on their own. Flag when these are missing:

**Prerequisites & Environment**:
- System dependencies (e.g., "requires Docker 20+", "needs libssl-dev on Linux")
- Required tool versions (node, python, go, etc.)
- Required accounts or API keys (with signup links, not the keys themselves)
- Environment variables with example values (use `YOUR_API_KEY` placeholders)

**Platform Differences**:
- OS-specific instructions when behavior differs (Mac vs Linux vs Windows)
- Architecture notes if relevant (ARM vs x86)

**Gotchas & Failure Modes**:
- Common setup errors and fixes ("If you see X, run Y")
- Non-obvious side effects ("This command also resets the database")
- Known limitations or unsupported scenarios

**Magic Values**:
- Default ports, timeouts, limits that aren't obvious from code
- Config file locations that vary by platform
- Implicit ordering dependencies ("Run A before B")

### Quick Start Quality

The quick start should let someone succeed in minutes, not hours. Evaluate:

**Copy-Pasteable Commands**:
- Commands can be copied and run verbatim (no unexplained `<placeholders>`)
- If placeholders are needed, explain how to get the real value
- Shell-specific syntax noted if it matters (bash vs zsh vs fish)

**Expected Output**:
- Show what success looks like ("You should see: ...")
- Include sample output for key commands
- Note how to verify it worked

**Minimal Path**:
- Doesn't require reading other sections first
- Optional features clearly marked as optional
- "Hello world" possible before diving into configuration

**First-Run Troubleshooting**:
- Top 2-3 things that go wrong on first run
- One-liner fixes for each
- Link to more detailed troubleshooting if it exists

### CLAUDE.md Navigation Index

CLAUDE.md files provide progressive disclosure via tabular indexes, pointing readers to the right file at the right time. README.md holds invisible knowledge (architecture, design decisions, invariants); CLAUDE.md holds navigation.

> CLAUDE.md conventions inspired by solatis/claude-config (MIT).

**Coverage** — Non-trivial directories should have a CLAUDE.md. Skip generated dirs, vendored deps, stubs (`.gitkeep` only), `.git`, `node_modules`, `__pycache__`, `dist`, `build`, and similar.

**Tabular index format** — Each CLAUDE.md must contain at least one markdown table with columns: `File` (or `Directory`), `What`, `When to read`. Entries should use:
- Backtick-wrapped file/directory names (e.g., `` `src/` ``)
- Noun-based "What" descriptions (e.g., "Entry point", "Test utilities")
- Action-verb "When to read" triggers (e.g., "Adding a new route", "Debugging test failures")

**Content separation (subdirectory CLAUDE.md only)** — Subdirectory CLAUDE.md files should contain only:
- A one-sentence overview of the directory's purpose
- One or more tabular indexes

They should **not** contain architecture explanations, design decisions, invariants, or multi-paragraph prose. That content belongs in README.md.

**Root CLAUDE.md is exempt** — The root CLAUDE.md may additionally contain operational sections (Build, Test, Lint commands), agent instruction sections (e.g., beads workflow, tool configuration), and other project-wide guidance. This is expected and should not be flagged.

**Index drift** — Flag when:
- A file or subdirectory exists in the directory but is missing from the CLAUDE.md index (excluding dotfiles, generated artifacts, and files covered by glob patterns in the index)
- An index entry references a file or directory that does not exist
- A CLAUDE.md index links to a README that doesn't exist, or a README references a component whose CLAUDE.md is missing

## Checklist

### Structure & Navigation
- [ ] Root README has: purpose, overview, quick start
- [ ] Root README links to component docs
- [ ] Each major component root has a README (not nested subdirs)
- [ ] Progressive disclosure maintained
- [ ] Non-trivial directories have CLAUDE.md files
- [ ] Each CLAUDE.md has a tabular index (`File`/`Directory`, `What`, `When to read`)
- [ ] Subdirectory CLAUDE.md files contain only overview + index (no architecture prose)
- [ ] CLAUDE.md indexes are in sync with actual directory contents (no drift)

### Content Quality
- [ ] No outdated references (paths, commands)
- [ ] Code examples syntactically correct
- [ ] Referenced files/commands exist
- [ ] Consistent terminology
- [ ] No duplicate information

### Hidden Knowledge
- [ ] Prerequisites documented (system deps, tool versions)
- [ ] Required env vars listed with example values
- [ ] Platform-specific instructions where behavior differs
- [ ] Common errors and fixes documented
- [ ] Magic values (ports, timeouts, defaults) explained

### Quick Start
- [ ] Commands are copy-pasteable (no unexplained placeholders)
- [ ] Expected output shown for key steps
- [ ] Minimal path to first success (no detours)
- [ ] First-run troubleshooting for common failures

## Output

You MUST produce a report following the exact structure shown in `REFERENCE.md`.

**Severity guide**:
- **P1** — Security-relevant: docs omit auth steps, expose secrets in examples, or give dangerous command examples
- **P2** — Broken: code examples that error, paths/commands that don't exist, quick start fails on copy-paste, index entries pointing to missing files
- **P3** — Stale or incomplete: outdated references, missing prerequisites, missing env var docs, missing CLAUDE.md coverage, index drift, no expected output shown
- **P4** — Polish: formatting inconsistencies, verbose wording, missing "When to read" triggers, missing platform-specific notes

**`--create-beads` mode**:

- Errors/inconsistencies → bug beads:
  ```bash
  bd create --type=bug --priority=<1-3> --title="Docs: <issue>" --description="<file and explanation>"
  ```

- Missing content → task beads:
  ```bash
  bd create --type=task --priority=<2-4> --title="Docs: <what to add>" --description="<what's needed and why>"
  ```
