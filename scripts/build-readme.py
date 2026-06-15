#!/usr/bin/env python3
import json

template = open("README.template.md").read()
skills = json.load(open("parts/skills.json"))

rows = "| Level | Skills |\n| ----- | ------ |\n"
for level in range(5, 0, -1):
    slugs = skills.get(str(level), [])
    icons = []
    for slug in slugs:
        icons.append(
            f'<img src="https://cdn.simpleicons.org/{slug}" '
            f'width="32" height="32" '
            f'style="display: inline-block; background: #f0f0f0; '
            f'border-radius: 4px; padding: 4px; vertical-align: middle;" />'
        )
    # Wrap after every 5 icons, spaces between
    cell = "<br>".join(
        " ".join(icons[i:i+5]) for i in range(0, len(icons), 5)
    ) if icons else ""
    rows += f"| {level} | {cell} |\n"

if "{{SKILLS_TABLE}}" in template:
    output = template.replace("{{SKILLS_TABLE}}", rows)
else:
    output = template + "\n## Skills\n" + rows

with open("README.md", "w") as f:
    f.write(output)

print("README.md generated successfully!")
