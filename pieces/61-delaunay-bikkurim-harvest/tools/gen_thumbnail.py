"""
Generate thumbnail.svg for piece 61-delaunay-bikkurim-harvest.

Produces a 400×400 SVG with ~80 Delaunay triangles in the seven-species
palette, a sky zone at the top, and a thin horizontal separator line at 80%
height.  Uses scipy.spatial.Delaunay when available; falls back to a
pure-Python Bowyer-Watson implementation otherwise.

Run from anywhere — the output path is resolved relative to this file's
parent directory.
"""
import math
import os
import random

SEED = 42
W, H = 400, 400
TARGET_PTS = 42  # yields ~80 triangles (2n − hull ≈ 80)
SKY_FRAC = 0.20  # upper 20 % → sky

SPECIES = [
    ("#D4A020", "חִיטָּה"),   # wheat
    ("#B8860B", "שְׂעֹרָה"),  # barley
    ("#6A2080", "גֶּפֶן"),    # grapes
    ("#7A4010", "תְּאֵנָה"),  # figs
    ("#A01828", "רִמּוֹן"),   # pomegranates
    ("#4A6020", "זַיִת"),     # olives
    ("#8B4513", "תָּמָר"),    # dates
]
SKY_COLOR = "#8BBFCE"
EARTH_COLOR = "#8B4030"
HORIZON_LINE = "#5A3010"


def darken(hex_color: str, amount: float = 0.22) -> str:
    """Return hex_color darkened by amount (0–1)."""
    r = int(hex_color[1:3], 16)
    g = int(hex_color[3:5], 16)
    b = int(hex_color[5:7], 16)
    r = max(0, int(r * (1 - amount)))
    g = max(0, int(g * (1 - amount)))
    b = max(0, int(b * (1 - amount)))
    return f"#{r:02x}{g:02x}{b:02x}"


def tri_color(cx: float, cy: float) -> str:
    """Return fill color for a triangle centroid at (cx, cy)."""
    if cy < H * SKY_FRAC:
        return SKY_COLOR
    if cy > H * 0.92:
        return EARTH_COLOR
    h = abs(math.sin(cx * 0.017 + cy * 0.031) * 7919) % 7
    return SPECIES[int(h)][0]


# ---------------------------------------------------------------------------
# Point generation: simple rejection sampling with min-distance check
# ---------------------------------------------------------------------------

def generate_points(seed: int = SEED) -> list[tuple[float, float]]:
    """Generate ~TARGET_PTS points with weighted density (denser in field zone)."""
    rng = random.Random(seed)
    pts: list[tuple[float, float]] = []

    # Corner anchors so the triangulation covers the canvas
    for x in (0.0, W / 2, float(W)):
        for y in (0.0, H / 2, float(H)):
            pts.append((x, y))

    min_sky = 55.0    # sparser sky zone
    min_field = 35.0  # denser field zone

    def too_close(px: float, py: float) -> bool:
        em = min_sky if py < H * SKY_FRAC else min_field
        for qx, qy in pts:
            if (px - qx) ** 2 + (py - qy) ** 2 < em * em:
                return True
        return False

    attempts = 0
    while len(pts) < TARGET_PTS + 9 and attempts < 20000:
        attempts += 1
        px = rng.uniform(0, W)
        py = rng.uniform(0, H)
        if not too_close(px, py):
            pts.append((px, py))

    return pts


# ---------------------------------------------------------------------------
# Pure-Python Bowyer-Watson Delaunay triangulation
# ---------------------------------------------------------------------------

def _in_circumcircle(
    ax: float, ay: float,
    bx: float, by: float,
    cx: float, cy: float,
    px: float, py: float,
) -> bool:
    """Return True if (px, py) lies strictly inside the circumcircle of abc.

    Works for both CW and CCW triangles: uses orientation-aware sign flip.
    """
    d = ax - px
    e = ay - py
    f = bx - px
    g = by - py
    h = cx - px
    k = cy - py
    det = (d * d + e * e) * (f * k - h * g) \
        - (f * f + g * g) * (d * k - h * e) \
        + (h * h + k * k) * (d * g - f * e)
    cross = (bx - ax) * (cy - ay) - (cx - ax) * (by - ay)
    return cross * det > 0


def bowyer_watson(pts: list[tuple[float, float]]) -> list[tuple[int, int, int]]:
    """Incremental Bowyer-Watson Delaunay triangulation.

    Returns a list of triangles as (i, j, k) index triples into pts.
    """
    n = len(pts)
    M = 1e8
    # Super-triangle vertices appended at indices n, n+1, n+2
    all_pts = list(pts) + [(W / 2, -M), (W / 2 + 2 * M, 2 * M), (W / 2 - 2 * M, 2 * M)]
    # Each triangle is a list [a, b, c] of indices into all_pts
    tris: list[list[int]] = [[n, n + 1, n + 2]]

    for i in range(n):
        px, py = pts[i]

        # Find triangles whose circumcircle contains pts[i]
        bad_idx: set[int] = set()
        for j, t in enumerate(tris):
            a, b, c = t
            if _in_circumcircle(
                all_pts[a][0], all_pts[a][1],
                all_pts[b][0], all_pts[b][1],
                all_pts[c][0], all_pts[c][1],
                px, py,
            ):
                bad_idx.add(j)

        # Boundary edges: appear in exactly one bad triangle
        edge_count: dict[str, int] = {}
        edge_dir: dict[str, tuple[int, int]] = {}
        for j in bad_idx:
            a, b, c = tris[j]
            for u, v in ((a, b), (b, c), (c, a)):
                key = f"{min(u,v)},{max(u,v)}"
                edge_count[key] = edge_count.get(key, 0) + 1
                if key not in edge_dir:
                    edge_dir[key] = (u, v)

        # Remove bad triangles (keep indices that are not in bad_idx)
        tris = [t for j, t in enumerate(tris) if j not in bad_idx]

        # Add new triangles from boundary edges to new point i
        for key, cnt in edge_count.items():
            if cnt == 1:
                u, v = edge_dir[key]
                tris.append([u, v, i])

    # Keep only triangles that do not touch super-triangle vertices
    result = []
    for t in tris:
        if t[0] < n and t[1] < n and t[2] < n:
            result.append((t[0], t[1], t[2]))
    return result


# ---------------------------------------------------------------------------
# SVG generation
# ---------------------------------------------------------------------------

def build_svg(pts: list[tuple[float, float]], tris: list[tuple[int, int, int]]) -> str:
    """Build the thumbnail SVG string from points and triangle index list."""
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg"'
        f' width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        "  <defs>",
        '    <filter id="tex" x="0%" y="0%" width="100%" height="100%">',
        '      <feTurbulence type="fractalNoise" baseFrequency="0.9"'
        ' numOctaves="3" stitchTiles="stitch" result="n"/>',
        '      <feBlend in="SourceGraphic" in2="n" mode="multiply"/>',
        "    </filter>",
        "  </defs>",
        f'  <rect width="{W}" height="{H}" fill="#e8dfc8"/>',
    ]

    for a, b, c in tris:
        ax, ay = pts[a]
        bx, by = pts[b]
        cx, cy = pts[c]
        centx = (ax + bx + cx) / 3
        centy = (ay + by + cy) / 3
        fill = tri_color(centx, centy)
        stroke = darken(fill)
        pts_str = f"{ax:.1f},{ay:.1f} {bx:.1f},{by:.1f} {cx:.1f},{cy:.1f}"
        lines.append(
            f'  <polygon points="{pts_str}"'
            f' fill="{fill}" stroke="{stroke}" stroke-width="0.8"/>'
        )

    # Horizon separator at 80 % height
    sep_y = int(H * 0.80)
    lines.append(
        f'  <line x1="0" y1="{sep_y}" x2="{W}" y2="{sep_y}"'
        f' stroke="{HORIZON_LINE}" stroke-width="1.2" opacity="0.5"/>'
    )

    # Parchment texture overlay
    lines.append(
        f'  <rect width="{W}" height="{H}" fill="white" opacity="0.06"'
        ' filter="url(#tex)"/>'
    )

    lines.append("</svg>")
    return "\n".join(lines)


def main() -> None:
    """Generate the thumbnail and write it next to this script's parent dir."""
    pts = generate_points(SEED)

    try:
        from scipy.spatial import Delaunay as ScipyDelaunay  # type: ignore
        import numpy as np  # type: ignore
        arr = np.array(pts)
        d = ScipyDelaunay(arr)
        tris = [(int(t[0]), int(t[1]), int(t[2])) for t in d.simplices]
    except ImportError:
        tris = bowyer_watson(pts)

    svg = build_svg(pts, tris)

    out_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out_path = os.path.join(out_dir, "thumbnail.svg")
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(svg)
    print(f"Written {len(tris)} triangles → {out_path}")


if __name__ == "__main__":
    main()
