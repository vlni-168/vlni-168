#!/bin/bash

TEMPLATE="README.template.md"
JSON_FILE="parts/skills.json"
OUTPUT="README.md"

if [ ! -f "$TEMPLATE" ] || [ ! -f "$JSON_FILE" ]; then
    echo "Error: Template or JSON missing!"
    exit 1
fi

TABLE_CONTENT="| Level | Skills |\n| ----- | ------ |\n"

for level in {5..1}; do
    skills=$(jq -r --arg lvl "$level" '.[$lvl] | if . then .[] else empty end' "$JSON_FILE")
    
    ROW_ICONS=""
    for skill in $skills; do
        ROW_ICONS="$ROW_ICONS <img src=\"https://simpleicons.org\" style=\"background: #f0f0f0; border-radius: 4px; padding: 4px;\" />"
    done
    TABLE_CONTENT="${TABLE_CONTENT}| $level |$ROW_ICONS |\n"
done

if grep -q "{{SKILLS_TABLE}}" "$TEMPLATE"; then
    awk -v r="$TABLE_CONTENT" '{gsub(/\{\{SKILLS_TABLE\}\}/,r)}1' "$TEMPLATE" > "$OUTPUT"
else
    cat "$TEMPLATE" > "$OUTPUT"
    echo -e "\n## Skills\n$TABLE_CONTENT" >> "$OUTPUT"
fi

echo "README.md generated sucessfully!"
