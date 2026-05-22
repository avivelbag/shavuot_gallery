#!/usr/bin/env python3
"""Generate thumbnail.svg for the Rose of Sharon rhodonea piece."""
import math
import os


def rhodonea_points(cx, cy, R, k, n=2000, rotation=0.0):
    """Compute (x, y) points for a rhodonea curve r = cos(k*t).

    Uses a universal period of 2*pi*12 so all rational k values with
    denominators in {1, 2, 3, 4, 6} close exactly.
    """
    period = 2 * math.pi * 12
    points = []
    for i in range(n + 1):
        t = period * i / n
        r = R * math.cos(k * t)
        x = cx + r * math.cos(t + rotation)
        y = cy + r * math.sin(t + rotation)
        points.append((x, y))
    return points


def points_to_path(points):
    """Convert a list of (x, y) tuples to an SVG path d-string."""
    parts = []
    for i, (x, y) in enumerate(points):
        cmd = "M" if i == 0 else "L"
        parts.append(f"{cmd} {x:.1f},{y:.1f}")
    parts.append("Z")
    return " ".join(parts)


def main():
    W, H = 600, 600
    cx, cy = W / 2, H / 2
    R = 240

    curves = [
        (3,         "#E8A0A0", 0.55, 0.0),
        (5 / 2,     "#D4A843", 0.50, math.pi / 10),
        (7 / 3,     "#FDF6E3", 0.45, math.pi / 6),
        (4 / 3,     "#9B4060", 0.55, math.pi / 4),
        (8 / 3,     "#C07090", 0.45, math.pi / 8),
    ]

    path_elements = []
    for k, color, opacity, rotation in curves:
        pts = rhodonea_points(cx, cy, R, k, rotation=rotation)
        d = points_to_path(pts)
        path_elements.append(
            f'  <path d="{d}" fill="none" stroke="{color}" '
            f'stroke-width="1.5" opacity="{opacity}" filter="url(#glow)"/>'
        )

    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'viewBox="0 0 {W} {H}">\n'
        "  <defs>\n"
        "    <filter id=\"glow\" x=\"-20%\" y=\"-20%\" width=\"140%\" height=\"140%\">\n"
        "      <feGaussianBlur stdDeviation=\"3\" result=\"blur\"/>\n"
        "      <feMerge><feMergeNode in=\"blur\"/>"
        "<feMergeNode in=\"SourceGraphic\"/></feMerge>\n"
        "    </filter>\n"
        "  </defs>\n"
        f'  <rect width="{W}" height="{H}" fill="#1A1035"/>\n'
        + "\n".join(path_elements)
        + "\n</svg>\n"
    )

    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "thumbnail.svg")
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(svg)
    print(f"Written {out_path}")


if __name__ == "__main__":
    main()
