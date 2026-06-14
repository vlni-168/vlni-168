#!/usr/bin/env bash
set -euo pipefail

ICON_URL="https://cdn.simpleicons.org"

{
  echo "| Level | Skills |"
  echo "| ----- | ------ |"

  for level in 5 4 3 2 1; do
    slugs=$(jq -r ".\"$level\" // [] | .[]" parts/skills.json 2>/dev/null || true)
    if [ -z "$slugs" ]; then
      echo "| $level | |"
    else
      icons=""
      while IFS= read -r slug; do
        icons+="<img src=\"$ICON_URL/$slug\" style=\"background: #f0f0f0; border-radius: 4px; padding: 4px;\" /> "
      done <<< "$slugs"
      echo "| $level | ${icons% } |"
    fi
  done
} > /tmp/skills-table.md

perl -p -i -e 'open(TABLE, "/tmp/skills-table.md"); local $/; $table = <TABLE>; close TABLE; s/<!-- SKILLS_TABLE -->/$table/' README.template.md
cp README.template.md README.md
