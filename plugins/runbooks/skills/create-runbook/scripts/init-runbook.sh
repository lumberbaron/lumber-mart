#!/usr/bin/env bash
# Initialize a new runbook file from the standard template.
#
# Usage: init-runbook.sh <runbook-name> [target-directory]
#
# Creates <target-directory>/<runbook-name>.md from the runbook template.
#
# The runbook name must be lowercase letters, digits, and hyphens only,
# with no leading/trailing/consecutive hyphens, and max 64 characters.
#
# If target-directory is omitted, defaults to the current directory.
#
# Outputs JSON with RUNBOOK_FILE and RUNBOOK_DIR paths on success.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TEMPLATE="$SCRIPT_DIR/../assets/runbook-template.md"

usage() {
  echo "Usage: $(basename "$0") <runbook-name> [target-directory]"
  echo ""
  echo "Creates a new runbook file from the standard template."
  echo ""
  echo "Runbook name rules:"
  echo "  - Lowercase letters (a-z), digits (0-9), and hyphens (-) only"
  echo "  - No leading, trailing, or consecutive hyphens"
  echo "  - Maximum 64 characters"
  echo ""
  echo "Examples:"
  echo "  $(basename "$0") deploy-api-production"
  echo "  $(basename "$0") rotate-db-credentials docs/ops"
}

if [ $# -lt 1 ] || [ $# -gt 2 ]; then
  usage
  exit 1
fi

RUNBOOK_NAME="$1"
TARGET_DIR="${2:-.}"

# Validate runbook name
if [ ${#RUNBOOK_NAME} -gt 64 ]; then
  echo "Error: Runbook name exceeds 64 characters (${#RUNBOOK_NAME})."
  exit 1
fi

if ! echo "$RUNBOOK_NAME" | grep -qE '^[a-z0-9-]+$'; then
  echo "Error: Runbook name must contain only lowercase letters, digits, and hyphens."
  echo "  Got: $RUNBOOK_NAME"
  exit 1
fi

if echo "$RUNBOOK_NAME" | grep -qE '(^-|-$|--)'; then
  echo "Error: Runbook name cannot start/end with a hyphen or contain consecutive hyphens."
  echo "  Got: $RUNBOOK_NAME"
  exit 1
fi

if [ ! -f "$TEMPLATE" ]; then
  echo "Error: Template not found at $TEMPLATE"
  exit 1
fi

RUNBOOK_FILE="$TARGET_DIR/$RUNBOOK_NAME.md"

if [ -e "$RUNBOOK_FILE" ]; then
  echo "Error: $RUNBOOK_FILE already exists."
  exit 1
fi

# Create target directory if needed
mkdir -p "$TARGET_DIR"

# Copy template
cp "$TEMPLATE" "$RUNBOOK_FILE"

# Output JSON with paths
RUNBOOK_FILE_ABS="$(cd "$(dirname "$RUNBOOK_FILE")" && pwd)/$(basename "$RUNBOOK_FILE")"
RUNBOOK_DIR_ABS="$(cd "$TARGET_DIR" && pwd)"

jq -n --arg f "$RUNBOOK_FILE_ABS" --arg d "$RUNBOOK_DIR_ABS" '{RUNBOOK_FILE: $f, RUNBOOK_DIR: $d}'
