#!/usr/bin/env python3
import json
import xml.etree.ElementTree as ET

def progressbar(level: int, highest_level: int, width: int = 120, style: str = "rounded",
                fill_color: str = "5c7c8a") -> str:
    ET.register_namespace('', 'http://www.w3.org/2000/svg')
    bar_height = 4

    svg = ET.Element('svg', {
        'width': str(width),
        'height': str(bar_height),
        'viewBox': f'0 0 {width} {bar_height}',
        'xmlns': 'http://www.w3.org/2000/svg'
    })

    bg_rect_attrs = {
        'x': '0', 'y': '0',
        'width': str(width), 'height': str(bar_height),
        'fill': '#e0e0e0'
    }

    level = max(0, min(level, highest_level))
    progress_width = (level / highest_level) * width

    active_rect_attrs = {
        'x': '0', 'y': '0',
        'width': str(progress_width), 'height': str(bar_height),
        'fill': f'#{fill_color}'
    }

    if style == "rounded":
        radius = str(bar_height / 2)
        bg_rect_attrs.update({'rx': radius, 'ry': radius})
        active_rect_attrs.update({'rx': radius, 'ry': radius})

    ET.SubElement(svg, 'rect', bg_rect_attrs)
    ET.SubElement(svg, 'rect', active_rect_attrs)

    return ET.tostring(svg, encoding='unicode')
# === SETUP ===
template = open("README.template.md").read()
skills = json.load(open("parts/skills.json"))

BASE_URL = "https://readmecodegen.vercel.app/api/social-icon"
highest_level = 5

try:
    open("assets/.keep", "x").close()
except FileExistsError:
    pass
except FileNotFoundError:
    import pathlib
    pathlib.Path("assets").mkdir(parents=True, exist_ok=True)
    open("assets/.keep", "w").close()

rows = "| Level | Skills |\n| ----- | ------ |\n"

# === GENERATE ===
for level in range(highest_level, 0, -1):
    slugs = skills.get(str(level), [])

    svg_code = progressbar(level=level, highest_level=highest_level, width=100)
    svg_path = f"assets/progress_{level}.svg"

    with open(svg_path, "w") as f:
        f.write(svg_code)

    level_bar = f'<img src="{svg_path}" width="120" alt="Level {level}" />'

    icons = []
    for slug in slugs:
        icon_url = f"{BASE_URL}?name={slug}&theme=dark&size=40&bg=transparent"
        icons.append(
            f'<img src="{icon_url}" alt="{slug}" height="32" />'
        )

    cell = "<br>".join(
        " ".join(icons[i:i+5]) for i in range(0, len(icons), 5)
    ) if icons else ""

    rows += f"| {level_bar} | {cell} |\n"

# === README BUILD ===
if "{{SKILLS_TABLE}}" in template:
    output = template.replace("{{SKILLS_TABLE}}", rows)
else:
    output = template + "\n## Skills\n" + rows

with open("README.md", "w") as f:
    f.write(output)

print("README.md generated successfully!")
