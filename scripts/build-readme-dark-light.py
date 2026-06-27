#!/usr/bin/env python3
import json
import xml.etree.ElementTree as ET
import pathlib


def progressbar(level: int, highest_level: int, width: int = 120,
                style: str = "rounded", fill_color: str = "5c7c8a",
                bg_color: str = "#e0e0e0") -> str:
    ET.register_namespace('', 'http://www.w3.org/2000/svg')
    bar_height = 4

    svg = ET.Element('svg', {
        'width': str(width),
        'height': str(bar_height),
        'viewBox': f'0 0 {width} {bar_height}',
        'xmlns': 'http://www.w3.org/2000/svg'
    })

    bg_rect = {
        'x': '0', 'y': '0',
        'width': str(width), 'height': str(bar_height),
        'fill': bg_color
    }

    level = max(0, min(level, highest_level))
    progress_width = (level / highest_level) * width

    active_rect = {
        'x': '0', 'y': '0',
        'width': str(progress_width), 'height': str(bar_height),
        'fill': f'#{fill_color}'
    }

    if style == "rounded":
        r = str(bar_height / 2)
        bg_rect.update({'rx': r, 'ry': r})
        active_rect.update({'rx': r, 'ry': r})

    ET.SubElement(svg, 'rect', bg_rect)
    ET.SubElement(svg, 'rect', active_rect)

    return ET.tostring(svg, encoding='unicode')


# === SETUP ===
template = open("README.template.md").read()
skills = json.load(open("parts/skills.json"))

BASE_URL = "https://readmecodegen.vercel.app/api/social-icon"
highest_level = max(map(int, skills.keys()))
accent = "5c7c8a"

# Color schemes for progress bars
LIGHT_PROGRESS_BG = "#d0d7de"
DARK_PROGRESS_BG  = "#30363d"

# Ensure assets dir and clean old SVGs
pathlib.Path("assets").mkdir(exist_ok=True)
for f in pathlib.Path("assets").glob("progress_*.svg"):
    f.unlink()

# === GENERATE TABLE ===
rows = ""

for level in range(highest_level, 0, -1):
    slugs = skills.get(str(level), [])

    # Generate two progress bar SVGs per level
    for mode, bg in [("light", LIGHT_PROGRESS_BG), ("dark", DARK_PROGRESS_BG)]:
        svg = progressbar(level, highest_level, width=100,
                         fill_color=accent, bg_color=bg)
        pathlib.Path(f"assets/progress_{level}_{mode}.svg").write_text(svg)

    # <picture> element picks the right SVG automatically
    bar = (
        f'<picture>'
        f'<source media="(prefers-color-scheme: dark)" '
        f'srcset="assets/progress_{level}_dark.svg">'
        f'<img src="assets/progress_{level}_light.svg" width="120" '
        f'alt="Level {level}">'
        f'</picture>'
    )

    # Neutral icons: light theme on a soft gray background
    # works acceptably on both white and dark pages
    icons = []
    for slug in slugs:
        icons.append(
            f'<img src="{BASE_URL}?name={slug}&size=32'
            f'&bg=%23f6f8fa&theme=light&shape=rect" '
            f'alt="{slug}" '
            f'style="height:32px;vertical-align:middle;padding:3px;'
            f'border-radius:8px;background:#f6f8fa;border:1px solid #d0d7de;" />'
        )

    cell = "<br>".join(
        " ".join(icons[i:i+5]) for i in range(0, len(icons), 5)
    ) if icons else ""

    rows += f"| {bar} | {cell} |\n"

# === BUILD README ===
if "{{SKILLS_TABLE}}" in template:
    output = template.replace("{{SKILLS_TABLE}}", rows)
else:
    output = template + "\n## Skills\n" + rows

pathlib.Path("README.md").write_text(output)
print("README.md generated successfully!")
