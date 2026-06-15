#!/usr/bin/env python3
import json

template = open("README.template.md").read()
skills = json.load(open("parts/skills.json"))

rows = "| Level | Skills |\n| ----- | ------ |\n"
for level in range(5, 0, -1):
    icons = ""
    for slug in skills.get(str(level), []):
        icons += f' <img src="https://cdn.simpleicons.org/{slug}" style="background: #f0f0f0; border-radius: 4px; padding: 4px;" height="32" />'
    rows += f"| {level} |{icons} |\n"

if "{{SKILLS_TABLE}}" in template:
    output = template.replace("{{SKILLS_TABLE}}", rows)
else:
    output = template + "\n## Skills\n" + rows

with open("README.md", "w") as f:
    f.write(output)

print("README.md generated successfully!")
