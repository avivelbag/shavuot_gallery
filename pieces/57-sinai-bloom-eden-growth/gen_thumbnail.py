"""Generate thumbnail.svg for 57-sinai-bloom-eden-growth.

Renders a 400×400 SVG showing concentric rings of hex cells in the floral
palette, with a mountain silhouette cut from the centre — a static snapshot
of the Eden bloom at completion.
"""
import math
import os

W, H = 400, 400
CX, CY = W // 2, H // 2
HEX_SIZE = 9  # circumradius in SVG units
SQ3 = math.sqrt(3)

PALETTE = [
    (58,  30,  106),   # #3A1E6A — deep violet
    (192, 96,  128),   # #C06080 — warm rose
    (212, 168, 32),    # #D4A820 — wheat gold
    (255, 248, 240),   # #FFF8F0 — pale cream
]
MAX_DIST = math.sqrt(CX ** 2 + CY ** 2)


def hex_to_pixel(q, r):
    """Convert axial hex coordinates to pixel centre (pointy-top orientation)."""
    x = CX + HEX_SIZE * (SQ3 * q + SQ3 * 0.5 * r)
    y = CY + HEX_SIZE * 1.5 * r
    return x, y


def lerp_palette(t):
    """Interpolate the 4-stop floral palette; t in [0, 1]."""
    t = max(0.0, min(1.0, t))
    n = len(PALETTE) - 1
    i = min(int(t * n), n - 1)
    f = t * n - i
    r1, g1, b1 = PALETTE[i]
    r2, g2, b2 = PALETTE[i + 1]
    r = round(r1 + (r2 - r1) * f)
    g = round(g1 + (g2 - g1) * f)
    b = round(b1 + (b2 - b1) * f)
    return f'#{r:02X}{g:02X}{b:02X}'


def hex_corners(cx, cy, size):
    """Return the 6 corner points of a pointy-top hexagon."""
    pts = []
    for k in range(6):
        angle = math.pi / 3 * k + math.pi / 6
        pts.append((cx + size * math.cos(angle), cy + size * math.sin(angle)))
    return pts


def pts_str(pts):
    return ' '.join(f'{x:.2f},{y:.2f}' for x, y in pts)


# Collect all hex cells within canvas bounds
cells = []
margin = HEX_SIZE
for q in range(-25, 26):
    for r in range(-25, 26):
        px, py = hex_to_pixel(q, r)
        if margin <= px <= W - margin and margin <= py <= H - margin:
            d = math.sqrt((px - CX) ** 2 + (py - CY) ** 2)
            t = d / MAX_DIST
            color = lerp_palette(t)
            # Slight inset (0.88×) leaves a small gap between cells
            corners = hex_corners(px, py, HEX_SIZE * 0.88)
            cells.append((corners, color))

lines = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">',
    f'  <rect width="{W}" height="{H}" fill="#100820"/>',
]

for corners, color in cells:
    lines.append(f'  <polygon points="{pts_str(corners)}" fill="{color}"/>')

# Mountain silhouette — dark triangle over the violet centre
mx, my = CX, CY
lines.append(
    f'  <polygon points="{mx},{my - 52} {mx - 38},{my + 12} {mx + 38},{my + 12}" fill="#100820"/>'
)

# Title bar
lines.append(
    f'  <rect x="0" y="{H - 42}" width="{W}" height="42" fill="rgba(16,8,32,0.93)"/>'
)
lines.append(
    f'  <text x="{CX}" y="{H - 15}" font-family="Georgia, serif" font-size="12" '
    f'fill="#d4a8c8" text-anchor="middle">And Sinai Was Covered in Flowers</text>'
)
lines.append('</svg>')

out_path = os.path.join(os.path.dirname(__file__), 'thumbnail.svg')
with open(out_path, 'w', encoding='utf-8') as fh:
    fh.write('\n'.join(lines) + '\n')

print(f'Wrote {len(cells)} hex cells to {out_path}')
