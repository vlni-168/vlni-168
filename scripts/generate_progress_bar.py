import xml.etree.ElementTree as ET

def progressbar(level: int, highest_level: int, width: int = 120, style: str = "rounded", 
                start_color: str = "ff6b6b", end_color: str = "4ecdc4")
    bar_height = 4

    svg = ET.Element('svg', {
        'width': str(width),
        'height': str(bar_height),
        'viewBox': f'0 0 {width} {bar_height}',
        'xmlns': 'http://w3.org'
    })

    defs = ET.SubElement(svg, 'defs')
    linear_gradient = ET.SubElement(defs, 'linearGradient', {
        'id': 'progressGrad',
        'x1': '0%', 'y1': '0%', 'x2': '100%', 'y2': '0%'
    })
    ET.SubElement(linear_gradient, 'stop', {'offset': '0%', 'stop-color': f'#{start_color}'})
    ET.SubElement(linear_gradient, 'stop', {'offset': '100%', 'stop-color': f'#{end_color}'})

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
        'fill': 'url(#progressGrad)'
    }

    if style == "rounded":
        radius = str(bar_height / 2)
        bg_rect_attrs.update({'rx': radius, 'ry': radius})
        active_rect_attrs.update({'rx': radius, 'ry': radius})

    ET.SubElement(svg, 'rect', bg_rect_attrs)
    ET.SubElement(svg, 'rect', active_rect_attrs)

    return ET.tostring(svg, encoding='utf-8').decode('utf-8')
