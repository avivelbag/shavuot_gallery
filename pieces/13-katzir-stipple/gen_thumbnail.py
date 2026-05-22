"""
Generate thumbnail.svg for piece 13-katzir-stipple.

Produces a 400x400 SVG approximating the stipple wheat-sheaf effect using
small circles distributed within sheaf-shaped regions and a background gradient.
Run from the piece directory: python3 gen_thumbnail.py
"""
import math
import random
import os

random.seed(42)

W, H = 400, 400

# Sheaf region: three rough elliptical columns representing the three sheaves
sheaf_regions = [
    # (cx, top_y, bottom_y, rx_top, rx_bottom) — left sheaf
    {'cx': 162, 'cy_top': 55, 'cy_bot': 370, 'rx': 22, 'tilt': -0.18},
    # center sheaf
    {'cx': 200, 'cy_top': 38, 'cy_bot': 378, 'rx': 20, 'tilt': 0.0},
    # right sheaf
    {'cx': 238, 'cy_top': 58, 'cy_bot': 368, 'rx': 22, 'tilt': 0.15},
]

bind_cx, bind_cy, bind_rx, bind_ry = 200, 255, 26, 16


def in_sheaf_region(x, y):
    """Return True if (x,y) is within any sheaf column or the bind ellipse."""
    for s in sheaf_regions:
        t = (y - s['cy_top']) / max(1, s['cy_bot'] - s['cy_top'])
        if not (0 <= t <= 1):
            continue
        cx = s['cx'] + s['tilt'] * (y - (s['cy_top'] + s['cy_bot']) / 2)
        rx = s['rx'] * (1 + 0.5 * abs(t - 0.5))
        if abs(x - cx) <= rx:
            return True
    dx = (x - bind_cx) / bind_rx
    dy = (y - bind_cy) / bind_ry
    if dx * dx + dy * dy <= 1:
        return True
    return False


def density(x, y, in_sh):
    if in_sh:
        dist = math.hypot(x - 200, y - 255) / 200
        return max(0.15, min(1.0, 0.9 - dist * 0.4))
    else:
        sky = max(0, 1 - y / H)
        return sky * 0.05


def dot_color(x, y, in_sh):
    if in_sh:
        t = (y - 38) / 340
        if t < 0.3:
            return '#b87a30'
        elif t < 0.6:
            return '#7a3010'
        else:
            return '#6b2800'
    else:
        sky_t = 1 - y / H
        if sky_t > 0.6:
            return '#a8c8e0'
        elif sky_t > 0.3:
            return '#c8d8b0'
        return '#d4b860'


circles = []
attempts = 0
while len(circles) < 500 and attempts < 50000:
    attempts += 1
    x = random.uniform(10, W - 10)
    y = random.uniform(10, H - 40)
    in_sh = in_sheaf_region(x, y)
    d = density(x, y, in_sh)
    if random.random() > d:
        continue
    r = 1.2 if in_sh else 0.8
    color = dot_color(x, y, in_sh)
    circles.append((x, y, r, color))

# Build SVG
lines = []
lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
lines.append(f'  <defs>')
lines.append(f'    <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">')
lines.append(f'      <stop offset="0%" stop-color="#c8dce8"/>')
lines.append(f'      <stop offset="35%" stop-color="#e8c870"/>')
lines.append(f'      <stop offset="100%" stop-color="#f5c842"/>')
lines.append(f'    </linearGradient>')
lines.append(f'  </defs>')
lines.append(f'  <rect width="{W}" height="{H}" fill="url(#bg)"/>')

for (x, y, r, color) in circles:
    lines.append(f'  <circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{color}"/>')

# Hebrew label
lines.append(f'  <text x="{W//2}" y="{H - 18}" text-anchor="middle" font-family="Arial, sans-serif" font-size="22" font-weight="bold" fill="rgba(60,20,0,0.82)">&#x05D7;&#x05B7;&#x05D2; &#x05D4;&#x05B7;&#x05E7;&#x05B8;&#x05E6;&#x05B4;&#x05D9;&#x05E8;</text>')
lines.append('</svg>')

svg_content = '\n'.join(lines)

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'thumbnail.svg')
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(svg_content)

print(f"Written {len(circles)} dots to {out_path} ({len(svg_content)} bytes)")
