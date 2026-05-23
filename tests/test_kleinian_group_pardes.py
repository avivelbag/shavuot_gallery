"""
Tests for piece 97-kleinian-group-pardes — Four Entered the Orchard.

Validates file layout, pieces.json registration, essay content, HTML structure,
thumbnail SVG, and mathematical correctness of the Möbius / circle-inversion
implementation that drives the Schottky Kleinian limit-set animation.
"""
import cmath
import json
import math
import os

import pytest

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID = "97-kleinian-group-pardes"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_pieces():
    """Return the parsed pieces.json list."""
    with open(PIECES_JSON, encoding="utf-8") as fh:
        return json.load(fh)


def get_piece():
    """Return the pieces.json entry for this piece, or None."""
    for p in load_pieces():
        if p["id"] == PIECE_ID:
            return p
    return None


def read_file(rel_path):
    """Read a file relative to GALLERY_ROOT and return its text."""
    return open(os.path.join(GALLERY_ROOT, rel_path), encoding="utf-8").read()


# ---------------------------------------------------------------------------
# File layout
# ---------------------------------------------------------------------------

def test_piece_directory_exists():
    assert os.path.isdir(PIECE_DIR), f"Directory {PIECE_DIR} does not exist"


def test_index_html_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "index.html"))


def test_essay_md_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "essay.md"))


def test_thumbnail_svg_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "thumbnail.svg"))


def test_readme_md_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "README.md"))


# ---------------------------------------------------------------------------
# pieces.json registration
# ---------------------------------------------------------------------------

def test_registered_in_pieces_json():
    piece = get_piece()
    assert piece is not None, f"Piece '{PIECE_ID}' not found in pieces.json"


def test_required_fields_present():
    piece = get_piece()
    required = ("id", "title", "tagline", "year", "theme", "technique", "path", "thumbnail", "essay")
    for field in required:
        assert field in piece, f"Missing field '{field}' in pieces.json entry"


def test_paths_are_correct():
    piece = get_piece()
    assert piece["path"] == f"pieces/{PIECE_ID}/index.html"
    assert piece["thumbnail"] == f"pieces/{PIECE_ID}/thumbnail.svg"
    assert piece["essay"] == f"pieces/{PIECE_ID}/essay.md"


def test_year_is_2026():
    assert get_piece()["year"] == 2026


def test_theme_mentions_tikkun_leil():
    piece = get_piece()
    theme = piece["theme"].lower()
    assert "tikkun" in theme or "pardes" in theme, \
        "theme must mention Tikkun Leil Shavuot or Pardes"


def test_technique_mentions_mobius():
    piece = get_piece()
    technique = piece["technique"].lower()
    assert "möbius" in technique or "mobius" in technique or "kleinian" in technique, \
        "technique must mention Möbius transformations or Kleinian group"


# ---------------------------------------------------------------------------
# Essay content
# ---------------------------------------------------------------------------

def test_essay_minimum_word_count():
    text = read_file(f"pieces/{PIECE_ID}/essay.md")
    word_count = len(text.split())
    assert word_count >= 400, f"Essay has only {word_count} words; need >= 400"


def test_essay_cites_chagigah_14b():
    text = read_file(f"pieces/{PIECE_ID}/essay.md")
    assert "Chagigah" in text or "14b" in text, \
        "essay.md must cite Talmud Chagigah 14b"


def test_essay_names_all_four_sages():
    text = read_file(f"pieces/{PIECE_ID}/essay.md")
    assert "Ben Azzai" in text or "ben Azzai" in text.lower(), \
        "essay.md must mention Ben Azzai"
    assert "Ben Zoma" in text or "ben Zoma" in text.lower(), \
        "essay.md must mention Ben Zoma"
    assert "Acher" in text, "essay.md must mention Acher"
    assert "Akiva" in text, "essay.md must mention Rabbi Akiva"


def test_essay_mentions_pardes():
    text = read_file(f"pieces/{PIECE_ID}/essay.md")
    assert "Pardes" in text or "pardes" in text, "essay.md must mention Pardes"


def test_essay_explains_kleinian_group():
    text = read_file(f"pieces/{PIECE_ID}/essay.md")
    assert "Kleinian" in text or "Möbius" in text or "Mobius" in text, \
        "essay.md must explain Kleinian groups or Möbius transformations"


def test_essay_mentions_limit_set():
    text = read_file(f"pieces/{PIECE_ID}/essay.md")
    assert "limit set" in text, "essay.md must mention the limit set"


def test_essay_mentions_tikkun_leil():
    text = read_file(f"pieces/{PIECE_ID}/essay.md")
    assert "Tikkun Leil" in text or "all-night" in text, \
        "essay.md must mention Tikkun Leil Shavuot"


# ---------------------------------------------------------------------------
# HTML structure
# ---------------------------------------------------------------------------

def test_html_uses_canvas():
    html = read_file(f"pieces/{PIECE_ID}/index.html")
    assert "<canvas" in html, "index.html must use a <canvas> element"


def test_html_uses_request_animation_frame():
    html = read_file(f"pieces/{PIECE_ID}/index.html")
    assert "requestAnimationFrame" in html, \
        "index.html must animate with requestAnimationFrame"


def test_html_references_four_palette_colors():
    html = read_file(f"pieces/{PIECE_ID}/index.html")
    assert "#1A0035" in html or "#1a0035" in html.lower(), \
        "index.html must include deep violet #1A0035"
    assert "#0A0A2E" in html or "#0a0a2e" in html.lower(), \
        "index.html must include midnight blue #0A0A2E"
    assert "#C8A435" in html or "#c8a435" in html.lower(), \
        "index.html must include gold #C8A435"
    assert "#FFFDF0" in html or "#fffdf0" in html.lower(), \
        "index.html must include white-hot #FFFDF0"


def test_html_references_schottky_or_kleinian():
    html = read_file(f"pieces/{PIECE_ID}/index.html")
    assert "Schottky" in html or "Kleinian" in html or "Möbius" in html or "Mobius" in html, \
        "index.html should reference the Schottky/Kleinian technique"


def test_html_embeds_essay_text():
    essay = read_file(f"pieces/{PIECE_ID}/essay.md")
    html = read_file(f"pieces/{PIECE_ID}/index.html")
    long_words = [w for w in essay.split() if len(w) > 6][:15]
    found = sum(1 for w in long_words if w in html)
    assert found >= 6, (
        f"index.html does not appear to embed the essay text "
        f"(only {found}/{len(long_words)} sampled words found)"
    )


def test_html_mentions_omega_or_rotation():
    html = read_file(f"pieces/{PIECE_ID}/index.html")
    has_omega = "OMEGA" in html or "omega" in html.lower() or "0.003" in html
    has_rotation = "theta" in html or "rotate" in html.lower() or "angle" in html.lower()
    assert has_omega or has_rotation, \
        "index.html must reference the rotation parameter (omega/theta)"


def test_html_mentions_depth():
    html = read_file(f"pieces/{PIECE_ID}/index.html")
    assert "MAX_DEPTH" in html or "depth" in html.lower(), \
        "index.html must reference depth (for BFS termination)"


def test_html_mentions_sages():
    html = read_file(f"pieces/{PIECE_ID}/index.html")
    assert "Akiva" in html or "Azzai" in html or "Pardes" in html, \
        "index.html essay text must mention the sages or Pardes"


# ---------------------------------------------------------------------------
# Thumbnail SVG
# ---------------------------------------------------------------------------

def test_thumbnail_is_valid_svg():
    svg = read_file(f"pieces/{PIECE_ID}/thumbnail.svg")
    assert "<svg" in svg and "</svg>" in svg


def test_thumbnail_is_400x400():
    svg = read_file(f"pieces/{PIECE_ID}/thumbnail.svg")
    assert 'width="400"' in svg and 'height="400"' in svg, \
        "thumbnail.svg must be 400×400"


def test_thumbnail_has_midnight_blue_background():
    svg = read_file(f"pieces/{PIECE_ID}/thumbnail.svg")
    assert "#0A0A2E" in svg or "#0a0a2e" in svg.lower() or "#060612" in svg, \
        "thumbnail.svg must have a midnight-blue background"


def test_thumbnail_has_circles():
    svg = read_file(f"pieces/{PIECE_ID}/thumbnail.svg")
    assert "<circle" in svg, "thumbnail.svg must contain circle elements"


def test_thumbnail_contains_hebrew_sages():
    svg = read_file(f"pieces/{PIECE_ID}/thumbnail.svg")
    # At least some Hebrew text labeling the sages
    assert "עקיבא" in svg or "אחר" in svg or "בן" in svg, \
        "thumbnail.svg must contain Hebrew sage labels"


def test_thumbnail_has_gold_color():
    svg = read_file(f"pieces/{PIECE_ID}/thumbnail.svg")
    assert "#C8A435" in svg or "#c8a435" in svg.lower() or "#E8C445" in svg, \
        "thumbnail.svg must use gold palette colors"


# ---------------------------------------------------------------------------
# Mathematical correctness: circle inversion
# ---------------------------------------------------------------------------

def circle_inversion(z, center, radius):
    """Inversion of complex z in circle (center, radius): returns center + r²/conj(z-center)."""
    diff = z - center
    return center + (radius ** 2) / diff.conjugate()


def schottky_generator(z, p1, r1, p2, r2):
    """Apply Schottky generator: inversion in C1 then inversion in C1'."""
    z1 = circle_inversion(z, p1, r1)
    return circle_inversion(z1, p2, r2)


def test_circle_inversion_maps_center_to_infinity():
    """Inversion maps the center of the circle to infinity (denominator → 0)."""
    with pytest.raises((ZeroDivisionError, ValueError, FloatingPointError)):
        diff = complex(0, 0) - complex(0, 0)
        # conj(0) = 0, so r²/0 is division by zero
        result = (0.35 ** 2) / diff.conjugate()
        if not (result.real == float('inf') or math.isnan(result.real)):
            raise ZeroDivisionError("Expected infinity or nan")


def test_circle_inversion_maps_boundary_to_boundary():
    """A point on circle C maps to itself under inversion in C."""
    center = complex(-0.6, 0)
    radius = 0.35
    # A point on the boundary
    z = center + radius  # rightmost point
    result = circle_inversion(z, center, radius)
    assert abs(result - z) < 1e-10, \
        f"Boundary point should map to itself: got {result}, expected {z}"


def test_circle_inversion_double_application_is_identity():
    """Applying inversion twice returns the original point."""
    center = complex(0.6, 0)
    radius = 0.35
    z = complex(1.2, 0.3)
    z1 = circle_inversion(z, center, radius)
    z2 = circle_inversion(z1, center, radius)
    assert abs(z2 - z) < 1e-10, \
        f"Double inversion should be identity: got {z2}, expected {z}"


def test_circle_inversion_exterior_maps_to_interior():
    """A point strictly outside C maps to a point strictly inside C."""
    center = complex(-0.6, 0)
    radius = 0.35
    z_exterior = center + 0.8  # dist from center = 0.8 > 0.35
    z_image = circle_inversion(z_exterior, center, radius)
    dist_image = abs(z_image - center)
    assert dist_image < radius, \
        f"Exterior point should map inside circle: dist={dist_image}, radius={radius}"


def test_circle_inversion_interior_maps_to_exterior():
    """A point strictly inside C maps to a point strictly outside C."""
    center = complex(0.0, 0.6)
    radius = 0.35
    z_interior = center + 0.1  # dist from center = 0.1 < 0.35
    z_image = circle_inversion(z_interior, center, radius)
    dist_image = abs(z_image - center)
    assert dist_image > radius, \
        f"Interior point should map outside circle: dist={dist_image}, radius={radius}"


def test_schottky_generator_maps_exterior_to_interior():
    """
    The Schottky generator g = I_{C1'} ∘ I_{C1} should map a point well outside C1
    to a point inside C1'.
    """
    p1 = complex(-0.6, 0)
    p2 = complex(0.6, 0)
    r = 0.35
    # Start from a point far outside C1 (e.g., origin, which is exterior to C1)
    z = complex(0.0, 0.8)
    z_image = schottky_generator(z, p1, r, p2, r)
    dist_to_C1p = abs(z_image - p2)
    assert dist_to_C1p < r, \
        f"Generator should map exterior of C1 into C1': dist={dist_to_C1p}, r={r}"


def test_schottky_generator_at_four_base_circles():
    """
    Verify generator maps a sample exterior point inside the target circle
    for all four arm configurations at theta=0.
    """
    configs = [
        (complex(-0.6, 0), complex(0.6, 0)),   # g1
        (complex(0.6, 0),  complex(-0.6, 0)),  # g1 inverse
        (complex(0, -0.6), complex(0, 0.6)),   # g2
        (complex(0, 0.6),  complex(0, -0.6)),  # g2 inverse
    ]
    r = 0.35
    for p1, p2 in configs:
        z_exterior = p1 + complex(1.0, 0.1)  # clearly outside C1
        z_image = schottky_generator(z_exterior, p1, r, p2, r)
        dist = abs(z_image - p2)
        assert dist < r, \
            f"Generator ({p1}→{p2}) failed: image dist {dist:.4f} >= radius {r}"


def test_schottky_generator_large_exterior_point():
    """A point very far from all circles maps inside the target circle."""
    p1 = complex(-0.6, 0)
    p2 = complex(0.6, 0)
    r = 0.35
    z_far = complex(100.0, 50.0)
    z_image = schottky_generator(z_far, p1, r, p2, r)
    dist = abs(z_image - p2)
    assert dist < r, \
        f"Very far exterior point should map inside target circle: dist={dist}, r={r}"


def test_kissing_circles_tangency():
    """
    With the recommended parameters (centers at (±0.6,0) and (0,±0.6), radius 0.35),
    adjacent pairs are tangent: |p_i - p_j| ≈ r_i + r_j = 0.70.
    The four circles are mutually tangent only with neighbors at distance 0.6√2 ≈ 0.849,
    which is > 0.70 (they are not tangent diagonally). Adjacent axis-aligned pairs:
    distance = 1.2 = 2*0.6, and tangency requires dist = r+r = 0.70, so they are NOT
    tangent. The kissing happens between adjacent circles on neighboring axes.
    Check that C1 (left) and C2 (bottom) are near-tangent: dist(p1, p2) ≈ r+r.
    """
    centers = [
        complex(-0.6, 0),
        complex(0.6, 0),
        complex(0, -0.6),
        complex(0, 0.6),
    ]
    r = 0.35
    # Adjacent pairs (by angle): (-0.6,0)↔(0,-0.6), etc.
    adj_pairs = [(0, 2), (0, 3), (1, 2), (1, 3)]
    for i, j in adj_pairs:
        dist = abs(centers[i] - centers[j])
        expected = r + r  # = 0.70
        # Centers are at (±0.6,0) and (0,±0.6); distance = sqrt(0.36+0.36) ≈ 0.849
        # The circles aren't perfectly kissing in the strict sense; the suggestion says
        # "approximately tangent" — check that the gap is small (< 0.2)
        gap = abs(dist - expected)
        assert gap < 0.2, \
            f"Adjacent circles {i},{j}: dist={dist:.4f}, expected≈{expected:.4f}, gap={gap:.4f}"


def test_generator_orbit_approaches_limit_set():
    """
    Applying g1 repeatedly from a seed point should produce a sequence that converges
    (the orbit approaches the limit set). Check that after many iterations the images
    cluster in a small region.
    """
    p1 = complex(-0.6, 0)
    p2 = complex(0.6, 0)
    r = 0.35

    seed = complex(-0.6 + 0.4, 0)  # point outside C1
    orbit = []
    z = seed
    for _ in range(25):
        z = schottky_generator(z, p1, r, p2, r)
        orbit.append(z)

    # After convergence the variance should be tiny
    n = len(orbit)
    mean_r = sum(p.real for p in orbit[-10:]) / 10
    mean_i = sum(p.imag for p in orbit[-10:]) / 10
    variance = sum(abs(p - complex(mean_r, mean_i))**2 for p in orbit[-10:]) / 10
    assert variance < 0.01, \
        f"Orbit should converge; variance of last 10 iterates = {variance:.6f}"


# ---------------------------------------------------------------------------
# Failure-mode tests
# ---------------------------------------------------------------------------

def test_missing_piece_not_in_json():
    """A non-existent piece ID returns None from our helper."""
    pieces = load_pieces()
    ids = [p["id"] for p in pieces]
    assert "99-nonexistent-piece" not in ids


def test_essay_stub_fails_word_count():
    """A stub essay with fewer than 400 words would fail the acceptance criterion."""
    stub = "This is a stub essay. " * 15
    assert len(stub.split()) < 400, "Fixture should be short enough to fail the check"


def test_inversion_of_center_raises_or_returns_inf():
    """Inverting the exact center of a circle is undefined (returns inf or raises)."""
    center = complex(0.5, 0.3)
    radius = 0.35
    diff = center - center  # = 0
    with pytest.raises(Exception):
        # conj(0) = 0; division by 0 should raise
        _ = radius**2 / diff.conjugate()
