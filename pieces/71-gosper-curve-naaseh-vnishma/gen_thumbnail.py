"""
Generate thumbnail.svg for piece 71-gosper-curve-naaseh-vnishma.

Runs the Gosper-curve L-system to level 3 (343 segments, 344 points),
performs the turtle walk, normalises the result into a 380×380 drawing
area centred in a 400×400 SVG, and writes the SVG path.

Run from the piece directory:  python3 gen_thumbnail.py
No external dependencies required.
"""
import math
import os

RULES = {
    'A': 'A-B--B+A++AA+B-',
    'B': '+A-BB--B-A++A+B',
}
ANGLE = math.pi / 3  # 60 degrees


def expand(axiom: str, depth: int) -> str:
    """Return the L-system string after `depth` expansion steps."""
    s = axiom
    for _ in range(depth):
        s = ''.join(RULES.get(c, c) for c in s)
    return s


def turtle_walk(lsystem: str) -> list[tuple[float, float]]:
    """Convert an L-system string into a list of (x, y) waypoints.

    'A' and 'B' move forward one unit; '+' turns left by ANGLE; '-' turns right.
    """
    x, y, direction = 0.0, 0.0, 0.0
    points = [(x, y)]
    for ch in lsystem:
        if ch in ('A', 'B'):
            x += math.cos(direction)
            y += math.sin(direction)
            points.append((x, y))
        elif ch == '+':
            direction += ANGLE
        elif ch == '-':
            direction -= ANGLE
    return points


def normalise(points: list[tuple[float, float]],
              target_w: float, target_h: float,
              margin: float) -> list[tuple[float, float]]:
    """Scale and translate points so they fill (margin…W-margin, margin…H-margin)."""
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    span_x = max_x - min_x or 1.0
    span_y = max_y - min_y or 1.0
    draw_w = target_w - 2 * margin
    draw_h = target_h - 2 * margin
    scale = min(draw_w / span_x, draw_h / span_y)
    off_x = margin + (draw_w - span_x * scale) / 2 - min_x * scale
    off_y = margin + (draw_h - span_y * scale) / 2 - min_y * scale
    return [(p[0] * scale + off_x, p[1] * scale + off_y) for p in points]


def build_path_d(points: list[tuple[float, float]]) -> str:
    """Return the SVG path `d` attribute string for the waypoints."""
    parts = [f'M {points[0][0]:.2f} {points[0][1]:.2f}']
    for x, y in points[1:]:
        parts.append(f'L {x:.2f} {y:.2f}')
    return ' '.join(parts)


def main() -> None:
    lsystem = expand('A', 3)
    raw = turtle_walk(lsystem)
    scaled = normalise(raw, target_w=400, target_h=400, margin=10)
    path_d = build_path_d(scaled)

    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" '
        'width="400" height="400" viewBox="0 0 400 400">\n'
        '  <rect width="400" height="400" fill="#0A1840"/>\n'
        f'  <path d="{path_d}" stroke="#C8A020" stroke-width="1.5" '
        'fill="none" stroke-linecap="round" stroke-linejoin="round"/>\n'
        '</svg>\n'
    )

    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'thumbnail.svg')
    with open(out_path, 'w', encoding='utf-8') as fh:
        fh.write(svg)

    print(f'Written {len(raw) - 1} segments ({len(raw)} points) to {out_path}')
    print(f'SVG size: {len(svg):,} bytes')


if __name__ == '__main__':
    main()
