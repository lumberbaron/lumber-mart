#!/usr/bin/env bash
# Initialize a new skill directory with a SKILL.md template.
#
# Usage: init-skill.sh <skill-name> [parent-directory]
#
# Creates <parent-directory>/<skill-name>/ with:
#   - SKILL.md (frontmatter + template body)
#   - scripts/ directory
#   - references/ directory
#
# The skill name must be lowercase letters, digits, and hyphens only,
# with no leading/trailing/consecutive hyphens, and max 64 characters.
#
# If parent-directory is omitted, defaults to the current directory.

set -euo pipefail

usage() {
  echo "Usage: $(basename "$0") <skill-name> [parent-directory]"
  echo ""
  echo "Creates a new skill directory with a SKILL.md template."
  echo ""
  echo "Skill name rules:"
  echo "  - Lowercase letters (a-z), digits (0-9), and hyphens (-) only"
  echo "  - No leading, trailing, or consecutive hyphens"
  echo "  - Maximum 64 characters"
  echo "  - Gerund form recommended (e.g., creating-skills, reviewing-code)"
  echo ""
  echo "Examples:"
  echo "  $(basename "$0") reviewing-code"
  echo "  $(basename "$0") generating-reports /path/to/skills"
}

if [ $# -lt 1 ] || [ $# -gt 2 ]; then
  usage
  exit 1
fi

SKILL_NAME="$1"
PARENT_DIR="${2:-.}"

# Validate skill name
if [ ${#SKILL_NAME} -gt 64 ]; then
  echo "Error: Skill name exceeds 64 characters (${#SKILL_NAME})."
  exit 1
fi

if ! echo "$SKILL_NAME" | grep -qE '^[a-z0-9-]+$'; then
  echo "Error: Skill name must contain only lowercase letters, digits, and hyphens."
  echo "  Got: $SKILL_NAME"
  exit 1
fi

if echo "$SKILL_NAME" | grep -qE '(^-|-$|--)'; then
  echo "Error: Skill name cannot start/end with a hyphen or contain consecutive hyphens."
  echo "  Got: $SKILL_NAME"
  exit 1
fi

SKILL_DIR="$PARENT_DIR/$SKILL_NAME"

if [ -e "$SKILL_DIR" ]; then
  echo "Error: $SKILL_DIR already exists."
  exit 1
fi

# Create directories
mkdir -p "$SKILL_DIR/scripts" "$SKILL_DIR/references"

# Generate title from skill name (hyphen-separated words to Title Case)
SKILL_TITLE=$(echo "$SKILL_NAME" | sed 's/-/ /g' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) substr($i,2)} 1')

# Write SKILL.md
cat > "$SKILL_DIR/SKILL.md" << SKILLEOF
---
name: $SKILL_NAME
description: TODO — Write a third-person description of what this skill does and when to use it. Include trigger phrases. Example: "Guides [task] with [capabilities]. Use when [trigger 1], [trigger 2], or [trigger 3]."
---

# $SKILL_TITLE

## Overview

TODO: 1-2 sentences explaining what this skill enables.

## User Input

\`\`\`text
\$ARGUMENTS
\`\`\`

Consider the user input above before proceeding (if not empty).

## Workflow

### Step 1: TODO

TODO: Describe the first step.

### Step 2: TODO

TODO: Describe the next step.
SKILLEOF

echo "Created $SKILL_DIR/"
echo "  SKILL.md    — Edit frontmatter and body"
echo "  scripts/    — Add executable scripts"
echo "  references/ — Add reference documentation"
