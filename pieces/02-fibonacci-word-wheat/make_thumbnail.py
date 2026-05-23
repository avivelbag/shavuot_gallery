"""Generate thumbnail.svg for the Fibonacci word wheat piece.

Walks the Fibonacci word to depth 16 (987 segments), computes the bounding
box, and renders a 400x400 SVG with a single wheat-gold polyline on near-black.
"""

import math
import os

PHI = (1 + math.sqrt(5)) / 2


def fib_word(n):
    """Return the turn-indicator for position n (0-indexed) of the Fibonacci word.

    The Fibonacci word is defined by F(1)="1", F(2)="0", F(n)=F(n-1)+F(n-2).
    This closed form uses the Beatty-sequence property: the result is 1 when
    the corresponding character is '1' (a left-turn in the walk), and 2 when
    it is '0' (advance only, no turn).

    Args:
        n: Zero-based position in the infinite Fibonacci word.

    Returns:
        1 if the nth character is '1', 2 if it is '0'.
    """
    return math.floor((n + 2) * PHI) - math.floor((n + 1) * PHI)


def walk(length):
    """Trace the Fibonacci word fractal and return the vertex sequence.

    Starts at the origin heading right (angle 0). Each step advances one unit
    in the current heading direction. When fib_word(n) == 1 (character '1'),
    the heading turns 90 degrees counterclockwise (left turn in screen coords).

    Direction encoding: 0=right, 1=up(-y), 2=left, 3=down(+y).

    Args:
        length: Number of steps / segments to walk.

    Returns:
        List of (x, y) integer tuples with length+1 points.
    """
    dx = [1, 0, -1, 0]
    dy = [0, -1, 0, 1]
    x, y = 0, 0
    angle = 0
    points = [(x, y)]
    for n in range(length):
        x += dx[angle]
        y += dy[angle]
        points.append((x, y))
        if fib_word(n) == 1:
            angle = (angle + 1) % 4
    return points


def make_svg(points, size=400, bg="#0A0A0A", stroke="#E8C84A", stroke_width=1.2):
    """Render walk points as a square SVG polyline scaled to fill the canvas.

    Scales and centers the walk so that the full bounding box fits within the
    canvas with a 5% margin on each side.

    Args:
        points: Sequence of (x, y) pairs from walk().
        size: Output canvas dimension in pixels (square).
        bg: Background fill color string.
        stroke: Polyline stroke color string.
        stroke_width: Stroke width in output pixels.

    Returns:
        Complete SVG markup as a string.
    """
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    span_x = (max_x - min_x) or 1
    span_y = (max_y - min_y) or 1

    margin = size * 0.05
    scale = min((size - 2 * margin) / span_x, (size - 2 * margin) / span_y)
    offset_x = (size - span_x * scale) / 2 - min_x * scale
    offset_y = (size - span_y * scale) / 2 - min_y * scale

    pts = " ".join(
        f"{p[0] * scale + offset_x:.1f},{p[1] * scale + offset_y:.1f}"
        for p in points
    )

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{size}" height="{size}" viewBox="0 0 {size} {size}">\n'
        f'  <rect width="{size}" height="{size}" fill="{bg}"/>\n'
        f'  <polyline points="{pts}" fill="none" stroke="{stroke}" '
        f'stroke-width="{stroke_width}" stroke-linecap="round" '
        f'stroke-linejoin="round"/>\n'
        f'</svg>\n'
    )


if __name__ == "__main__":
    points = walk(987)
    svg = make_svg(points)
    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "thumbnail.svg")
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(svg)
    bounding = (
        min(p[0] for p in points),
        min(p[1] for p in points),
        max(p[0] for p in points),
        max(p[1] for p in points),
    )
    print(
        f"Wrote {out_path} ({len(points)} points, "
        f"bbox x={bounding[0]}..{bounding[2]} y={bounding[1]}..{bounding[3]})"
    )
