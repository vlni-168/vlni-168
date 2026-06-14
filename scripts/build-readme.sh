#!/usr/bin/env bash
set -euo pipefail

ICON_URL="https://cdn.simpleicons.org"

# Generate the skills table
{
  echo "<style>"
  echo "  .skill-icon { background: #f0f0f0; border-radius: 4px; padding: 4px; }"
  echo "</style>"
  echo ""
  echo "| Level | Skills |"
  echo "| ----- | ------ |"

  # Read JSON and build rows
  for level in 5 4 3 2 1; do
    slugs=$(jq -r ".\"$level\" // [] | .[]" parts/skills.json 2>/dev/null || true)
    if [ -z "$slugs" ]; then
      echo "| $level | |"
    else
      icons=""
      while IFS= read -r slug; do
        icons+="<img class=\"skill-icon\" src=\"$ICON_URL/$slug\" /> "
      done <<< "$slugs"
      echo "| $level | ${icons% } |"
    fi
  done
} > /tmp/skills-table.md

# Inject into template
perl -p -i -e 'open(TABLE, "/tmp/skills-table.md"); local $/; $table = <TABLE>; close TABLE; s/<!-- SKILLS_TABLE -->/$table/' README.template.md

# Overwrite README.md
cp README.template.md README.md
