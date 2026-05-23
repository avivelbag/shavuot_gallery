"""Generate thumbnail.svg for the p6m wallpaper-group piece.

Draws the p6m tiling (12 fundamental-domain triangles per hexagonal tile,
alternating ivory / field-green, with a gold wheat-ear stroke in each domain)
using only stdlib xml.etree.ElementTree.  Run from this directory:

    python3 gen_thumbnail.py
"""
import math
import xml.etree.ElementTree as ET

GOLD = "#D4A830"
GREEN = "#2A6020"
IVORY = "#F5EDD8"
W = H = 400
R = 40          # hex circumradius (center → vertex)
SQRT3 = math.sqrt(3)
DX = R * SQRT3  # horizontal distance between same-row hex centres
DY = R * 1.5    # vertical distance between row centres


def hex_vertices(cx, cy):
    """Return 6 (x,y) vertices of a flat-top regular hexagon."""
    return [
        (cx + R * math.cos(k * math.pi / 3),
         cy + R * math.sin(k * math.pi / 3))
        for k in range(6)
    ]


def pts(*coords):
    """Format a sequence of (x,y) pairs as an SVG points string."""
    return " ".join(f"{x:.2f},{y:.2f}" for x, y in coords)


def draw_hex_background(svg, cx, cy):
    """Fill the 12 fundamental-domain triangles of one hex tile."""
    verts = hex_vertices(cx, cy)
    for k in range(6):
        v1 = verts[k]
        v2 = verts[(k + 1) % 6]
        # midpoint of the edge between v1 and v2
        vm = ((v1[0] + v2[0]) / 2, (v1[1] + v2[1]) / 2)
        center = (cx, cy)

        # Two sub-triangles per equilateral-triangle sector
        for i, (va, vb) in enumerate(((v1, vm), (vm, v2))):
            idx = 2 * k + i
            color = GREEN if idx % 2 == 0 else IVORY
            ET.SubElement(svg, "polygon", {
                "points": pts(center, va, vb),
                "fill": color,
                "stroke": "none",
            })


def draw_domain_motif(svg, cx, cy, angle, flip):
    """Stroke a tiny wheat-ear motif for one fundamental domain.

    The motif is drawn in the local coordinate frame defined by:
      translate(cx, cy) → rotate(angle) → [scale(-1,1) if flip]
    The stem runs roughly from the centre outward; two pairs of grain
    ellipses flank it.
    """
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    sign = -1 if flip else 1

    def local_to_world(lx, ly):
        """Apply local transform: scale-if-flip → rotate → translate."""
        sx = sign * lx
        wx = cx + sx * cos_a - ly * sin_a
        wy = cy + sx * sin_a + ly * cos_a
        return wx, wy

    # Stem: two anchor points in local space (x-axis is the main axis)
    p_inner = local_to_world(R * 0.15, 0)
    p_outer = local_to_world(R * 0.70, 0)

    # Draw stem as a path element
    d = f"M {p_inner[0]:.2f},{p_inner[1]:.2f} L {p_outer[0]:.2f},{p_outer[1]:.2f}"
    ET.SubElement(svg, "path", {
        "d": d,
        "stroke": GOLD,
        "stroke-width": "1.5",
        "fill": "none",
        "stroke-linecap": "round",
    })

    # Grain ellipses: two pairs flanking the stem
    for i in range(2):
        lx = R * (0.30 + i * 0.20)  # position along stem axis
        for side in (-1, 1):
            ly = side * R * 0.10     # perpendicular offset
            wx, wy = local_to_world(lx, ly)
            # Ellipse axes in world space (we approximate with a small circle)
            ET.SubElement(svg, "ellipse", {
                "cx": f"{wx:.2f}",
                "cy": f"{wy:.2f}",
                "rx": f"{R * 0.07:.2f}",
                "ry": f"{R * 0.035:.2f}",
                "transform": f"rotate({math.degrees(angle + math.atan2(ly, lx)):.1f} {wx:.2f} {wy:.2f})",
                "fill": GOLD,
                "stroke": "none",
            })


def draw_hex(svg, cx, cy):
    """Draw one complete hexagonal tile: background triangles + motifs."""
    draw_hex_background(svg, cx, cy)
    for rot in range(6):
        angle = rot * math.pi / 3
        for flip in range(2):
            draw_domain_motif(svg, cx, cy, angle, bool(flip))


def main():
    svg = ET.Element("svg", {
        "xmlns": "http://www.w3.org/2000/svg",
        "width": str(W),
        "height": str(H),
        "viewBox": f"0 0 {W} {H}",
    })
    ET.SubElement(svg, "rect", {"width": str(W), "height": str(H), "fill": IVORY})

    for row in range(-2, 9):
        for col in range(-1, 8):
            cx = col * DX + (row % 2) * DX / 2
            cy = row * DY
            draw_hex(svg, cx, cy)

    tree = ET.ElementTree(svg)
    ET.indent(tree, space="  ")
    tree.write("thumbnail.svg", encoding="unicode", xml_declaration=False)
    print("thumbnail.svg written.")


if __name__ == "__main__":
    main()
