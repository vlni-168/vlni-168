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

# Color schemes per mode
LIGHT_PROGRESS_BG = "#d0d7de"   # visible against a white page
DARK_PROGRESS_BG  = "#30363d"   # GitHub dark mode surface
LIGHT_ICON_BG     = "f0f0f0"    # subtle gray badge
DARK_ICON_BG      = accent      # colored badge

# Ensure assets dir and clean old SVGs
pathlib.Path("assets").mkdir(exist_ok=True)
for f in pathlib.Path("assets").glob("progress_*.svg"):
    f.unlink()

# === CSS for light/dark mode ===
# Default: light visible (fallback for browsers without media-query support)
# Dark mode: swaps visibility
style_block = """<style>
.skills-dark { display: none; }
.skills-light { display: inline; }
@media (prefers-color-scheme: dark) {
  .skills-dark { display: inline; }
  .skills-light { display: none; }
}
</style>"""

# === GENERATE TABLE ===
rows = ""

for level in range(highest_level, 0, -1):
    slugs = skills.get(str(level), [])

    # Two progress bar SVGs (one per color scheme)
    for mode, bg in [("light", LIGHT_PROGRESS_BG), ("dark", DARK_PROGRESS_BG)]:
        svg = progressbar(level, highest_level, width=100,
                         fill_color=accent, bg_color=bg)
        pathlib.Path(f"assets/progress_{level}_{mode}.svg").write_text(svg)

    bar_light = f'<img src="assets/progress_{level}_light.svg" width="120" alt="Level {level}" />'
    bar_dark  = f'<img src="assets/progress_{level}_dark.svg" width="120" alt="Level {level}" />'

    # Two icon sets (theme + bg differ per mode)
    def build_icons(theme, bg_hex):
        parts = []
        for slug in slugs:
            parts.append(
                f'<img src="{BASE_URL}?name={slug}&size=32&bg=%23{bg_hex}'
                f'&theme={theme}&shape=rect" alt="{slug}"'
                f' style="height:32px;vertical-align:middle;padding:3px;border-radius:8px;" />'
            )
        if not parts:
            return ""
        return "<br>".join(" ".join(parts[i:i+5]) for i in range(0, len(parts), 5))

    icons_light = build_icons("light", LIGHT_ICON_BG)
    icons_dark  = build_icons("dark",  DARK_ICON_BG)

    rows += (
        f'| <span class="skills-light">{bar_light}</span>'
        f'<span class="skills-dark">{bar_dark}</span>'
        f' | <span class="skills-light">{icons_light}</span>'
        f'<span class="skills-dark">{icons_dark}</span> |\n'
    )

# === BUILD README ===
skills_section = style_block + "\n\n" + rows

if "{{SKILLS_TABLE}}" in template:
    output = template.replace("{{SKILLS_TABLE}}", skills_section)
else:
    output = template + "\n## Skills\n" + skills_section

pathlib.Path("README.md").write_text(output)
print("README.md generated successfully!")
