---
description: Initialize a git repository with spec-kit and beads configuration. Works for both new and existing repositories.
---

# Initialize Repository with Spec-Kit and Beads

Initialize the current repository with spec-kit (specify) and beads configuration for Claude.

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Argument Parsing

Parse `$ARGUMENTS` for:
- `--no-commit` - Initialize without prompting to commit

## Outline

### 1. Check Prerequisites

Verify required tools and environment:

```bash
git rev-parse --is-inside-work-tree
command -v specify
command -v bd
```

> [!CAUTION]
> - ERROR if not a git repository → Instruct user to run `git init` first
> - ERROR if `specify` not found → Instruct user to install spec-kit
> - ERROR if `bd` not found → Instruct user to install beads

### 2. Initialize Spec-Kit

Determine the shell script type based on platform:
- **macOS/Linux/WSL2** (`uname` returns Darwin or Linux): use `--script sh`
- **Windows** (no uname or returns Windows): use `--script ps`

```bash
# macOS/Linux
specify init . --ai claude --script sh --force

# Windows
specify init . --ai claude --script ps --force
```

> [!NOTE]
> This command requires network access. If sandbox blocks it, retry with sandbox disabled.

### 3. Initialize Beads

```bash
bd init --quiet
bd setup claude
```

Both commands are idempotent.

### 4. Merge AGENTS.md into CLAUDE.md

The `bd setup claude` command creates an `AGENTS.md` file with beads workflow instructions.

If `AGENTS.md` exists:
1. Check if CLAUDE.md already contains beads content (grep for "bd ready")
2. If not found, append AGENTS.md content to CLAUDE.md
3. Delete AGENTS.md

```bash
# Example approach
if [ -f AGENTS.md ]; then
  if ! grep -q "bd ready" CLAUDE.md 2>/dev/null; then
    cat AGENTS.md >> CLAUDE.md
  fi
  rm AGENTS.md
fi
```

### 5. Report and Prompt for Commit

Report what was set up:

```
Repository initialized with spec-kit and beads.

Files created/modified:
- .specify/ (spec-kit configuration)
- .beads/ (beads configuration)
- CLAUDE.md (updated with beads workflow)
```

Unless `--no-commit` was specified, ask the user if they want to commit these changes. If yes:

```bash
git add -A
git commit -m "Initialize spec-kit and beads"
```

## Error Handling

- If prerequisite checks fail, stop and report clearly
- If `specify init` fails due to sandbox, instruct to retry with sandbox disabled
- If commit fails with "nothing to commit", repo was likely already initialized
