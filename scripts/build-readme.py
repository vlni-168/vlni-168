#!/usr/bin/env python3
import json
import xml.etree.ElementTree as ET
import base64

def progressbar(level: int, highest_level: int, width: int = 120, style: str = "rounded",
                fill_color: str = "4ecdc4") -> str:
    ET.register_namespace('', 'http://w3.org')
    bar_height = 4

    svg = ET.Element('svg', {
        'width': str(width),
        'height': str(bar_height),
        'viewBox': f'0 0 {width} {bar_height}',
        'xmlns': 'http://www.w3.org/2000/svg'
    })

    # Hintergrund (grau)
    bg_rect_attrs = {
        'x': '0', 'y': '0',
        'width': str(width), 'height': str(bar_height),
        'fill': '#e0e0e0'
    }

    # Fortschritt berechnen
    level = max(0, min(level, highest_level))
    progress_width = (level / highest_level) * width

    # Fortschrittsbalken (einfarbig)
    active_rect_attrs = {
        'x': '0', 'y': '0',
        'width': str(progress_width), 'height': str(bar_height),
        'fill': f'#{fill_color}'
    }

    # Rundung optional
    if style == "rounded":
        radius = str(bar_height / 2)
        bg_rect_attrs.update({'rx': radius, 'ry': radius})
        active_rect_attrs.update({'rx': radius, 'ry': radius})

    ET.SubElement(svg, 'rect', bg_rect_attrs)
    ET.SubElement(svg, 'rect', active_rect_attrs)

    return ET.tostring(svg, encoding='utf-8', method='xml').decode('utf-8')


template = open("README.template.md").read()
skills = json.load(open("parts/skills.json"))

BASE_URL = "https://readmecodegen.vercel.app/api/social-icon"
highest_level = 5

rows = "| Level | Skills |\n| ----- | ------ |\n"

for level in range(highest_level, 0, -1):
    slugs = skills.get(str(level), [])

    svg_code = progressbar(level=level, highest_level=5, width=120)
    clean_svg = "".join(svg_code.splitlines()).strip()

    encoded_svg = base64.b64encode(clean_svg.encode('utf-8')).decode('utf-8')

    # ✅ FIX: echtes <img>, kein HTML-escaping
    level_bar = f'<img src="data:image/svg+xml;base64,{encoded_svg}" alt="Level {level}" width="120" style="vertical-align: middle;" />'

    icons = []
    for slug in slugs:
        icon_url = f"{BASE_URL}?name={slug}&theme=dark&size=40&bg=transparent"
        icons.append(
            f'<img src="{icon_url}" alt="{slug}" height="32" style="display:inline-block; vertical-align: middle;" />'
        )

    cell = "<br>".join(
        " ".join(icons[i:i+5]) for i in range(0, len(icons), 5)
    ) if icons else ""

    rows += f"| {level_bar} | {cell} |\n"

if "{{SKILLS_TABLE}}" in template:
    output = template.replace("{{SKILLS_TABLE}}", rows)
else:
    output = template + "\n## Skills\n" + rows

with open("README.md", "w") as f:
    f.write(output)

print("README.md generated successfully!")
