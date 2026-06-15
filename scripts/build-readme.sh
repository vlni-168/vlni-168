#!/bin/bash

TEMPLATE="README.template.md"
JSON_FILE="parts/skills.json"
OUTPUT="README.md"

if [ ! -f "$TEMPLATE" ] || [ ! -f "$JSON_FILE" ]; then
    echo "Error: Template or JSON missing!"
    exit 1
fi

TABLE_CONTENT=$(printf "| Level | Skills |\n| ----- | ------ |\n")

for level in {5..1}; do
    skills=$(jq -r --arg lvl "$level" '.[$lvl] | if . then .[] else empty end' "$JSON_FILE")

    ROW_ICONS=""
    for skill in $skills; do
        ROW_ICONS="$ROW_ICONS <img src=\"https://cdn.simpleicons.org/$skill\" style=\"background: #f0f0f0; border-radius: 4px; padding: 4px;\" height=\"32\" />"
    done
    TABLE_CONTENT="${TABLE_CONTENT}$(printf "| $level |$ROW_ICONS |\n")"
done

if grep -q "{{SKILLS_TABLE}}" "$TEMPLATE"; then
    export TABLE_CONTENT
    perl -0777 -pe 's/\{\{SKILLS_TABLE\}\}/$ENV{TABLE_CONTENT}/g' "$TEMPLATE" > "$OUTPUT"
else
    cat "$TEMPLATE" > "$OUTPUT"
    printf "\n## Skills\n$TABLE_CONTENT" >> "$OUTPUT"
fi

echo "README.md generated successfully!"
