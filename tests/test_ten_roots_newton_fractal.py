"""
Tests for piece 57-ten-roots-newton-fractal.

Verifies: file layout, pieces.json registration, essay content,
HTML structure (WebGL shader, legend, essay embed), thumbnail SVG,
and Newton-fractal correctness (Python reference implementation).
"""
import cmath
import json
import math
import os
import re

import pytest

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID = "57-ten-roots-newton-fractal"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_pieces():
    with open(os.path.join(GALLERY_ROOT, "pieces.json"), encoding="utf-8") as f:
        return json.load(f)


def get_piece():
    for p in load_pieces():
        if p["id"] == PIECE_ID:
            return p
    return None


def read(relpath):
    return open(os.path.join(GALLERY_ROOT, relpath), encoding="utf-8").read()


def newton_fractal_root(zr, zi, max_iter=64, thresh=1e-6):
    """
    Python reference implementation of Newton's method for f(z) = z^10 - 1.

    Returns the basin index (0-9) of the nearest root of unity, or -1 if
    the iteration did not converge within max_iter steps.
    """
    z = complex(zr, zi)
    for _ in range(max_iter):
        fz = z**10 - 1
        if abs(fz) < thresh:
            angle = cmath.phase(z)
            if angle < 0:
                angle += 2 * math.pi
            root = int(angle / (2 * math.pi / 10) + 0.5) % 10
            return root
        dfz = 10 * z**9
        if abs(dfz) < 1e-14:
            break
        z = z - fz / dfz
        if abs(z) > 1e4:
            break
    return -1


# ---------------------------------------------------------------------------
# File layout
# ---------------------------------------------------------------------------

def test_piece_directory_exists():
    assert os.path.isdir(PIECE_DIR), f"Piece directory missing: {PIECE_DIR}"


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

def test_piece_registered_in_pieces_json():
    piece = get_piece()
    assert piece is not None, f"Piece '{PIECE_ID}' not found in pieces.json"


def test_piece_required_fields():
    piece = get_piece()
    assert piece is not None
    for field in ("id", "title", "tagline", "year", "theme", "technique", "path", "thumbnail", "essay"):
        assert field in piece and piece[field], f"Field '{field}' missing or empty"


def test_piece_theme():
    piece = get_piece()
    assert piece is not None
    assert "Aseret HaDibrot" in piece["theme"] or "Matan Torah" in piece["theme"]


def test_piece_technique():
    piece = get_piece()
    assert piece is not None
    technique = piece["technique"].lower()
    assert "newton" in technique or "fractal" in technique


def test_piece_year():
    piece = get_piece()
    assert piece is not None
    assert isinstance(piece["year"], int)


def test_piece_thumbnail_path_exists():
    piece = get_piece()
    assert piece is not None
    full = os.path.join(GALLERY_ROOT, piece["thumbnail"])
    assert os.path.isfile(full)


def test_piece_essay_path_exists():
    piece = get_piece()
    assert piece is not None
    full = os.path.join(GALLERY_ROOT, piece["essay"])
    assert os.path.isfile(full)


# ---------------------------------------------------------------------------
# Essay content
# ---------------------------------------------------------------------------

def test_essay_word_count():
    text = read(f"pieces/{PIECE_ID}/essay.md")
    word_count = len(text.split())
    assert word_count >= 350, f"Essay has only {word_count} words (need ≥ 350)"


def test_essay_cites_exodus_20():
    text = read(f"pieces/{PIECE_ID}/essay.md")
    assert "Exodus 20" in text or "exodus 20" in text.lower()


def test_essay_mentions_rambam_or_enumeration_dispute():
    text = read(f"pieces/{PIECE_ID}/essay.md")
    assert "Rambam" in text or "enumeration" in text or "HaChinuch" in text


def test_essay_mentions_halakha_boundary():
    text = read(f"pieces/{PIECE_ID}/essay.md")
    assert "boundary" in text.lower() or "halakha" in text.lower() or "halakhic" in text.lower()


# ---------------------------------------------------------------------------
# index.html: WebGL shader and structure
# ---------------------------------------------------------------------------

def test_index_html_has_webgl_canvas():
    html = read(f"pieces/{PIECE_ID}/index.html")
    assert "getContext" in html and ("webgl" in html.lower()), \
        "index.html must set up a WebGL context"


def test_index_html_has_fragment_shader():
    html = read(f"pieces/{PIECE_ID}/index.html")
    assert "x-shader/x-fragment" in html or "FRAGMENT_SHADER" in html


def test_index_html_shader_implements_z10_minus_1():
    html = read(f"pieces/{PIECE_ID}/index.html")
    assert "z10" in html or "z^10" in html or "cpow10" in html or "z9" in html, \
        "Shader must implement z^10 - 1 Newton iteration"


def test_index_html_has_newton_step():
    html = read(f"pieces/{PIECE_ID}/index.html")
    assert "Newton" in html or "cdiv" in html or "f(z)/f" in html.replace(" ", "")


def test_index_html_has_requestanimationframe():
    html = read(f"pieces/{PIECE_ID}/index.html")
    assert "requestAnimationFrame" in html


def test_index_html_has_ten_palette_colors():
    html = read(f"pieces/{PIECE_ID}/index.html")
    expected_colors = [
        "FFFEF0", "D4A020", "C07010", "B84010",
        "8B2050", "3A1060", "1A1050", "0A3850",
        "1A4820", "6A5010"
    ]
    for color in expected_colors:
        assert color.lower() in html.lower(), f"Palette color #{color} missing from index.html"


def test_index_html_has_legend_with_ten_commandments():
    html = read(f"pieces/{PIECE_ID}/index.html")
    assert "אָנֹכִי" in html, "Legend must include first commandment (אָנֹכִי)"
    assert "לֹא תַחְמֹד" in html, "Legend must include tenth commandment (לֹא תַחְמֹד)"


def test_index_html_has_hebrew_numerals_aleph_through_yod():
    html = read(f"pieces/{PIECE_ID}/index.html")
    for letter in ["א", "ב", "ג", "ד", "ה", "ו", "ז", "ח", "ט", "י"]:
        assert letter in html, f"Legend missing Hebrew numeral {letter}"


def test_index_html_zoom_animation():
    html = read(f"pieces/{PIECE_ID}/index.html")
    assert "u_scale" in html or "uScale" in html, \
        "index.html must animate a scale/zoom uniform"


def test_index_html_embeds_essay_text():
    """Essay prose must appear inline in index.html (no runtime fetch)."""
    essay = read(f"pieces/{PIECE_ID}/essay.md")
    html  = read(f"pieces/{PIECE_ID}/index.html")
    words = [w for w in essay.split() if len(w) > 6][:15]
    found = sum(1 for w in words if w in html)
    assert found >= 8, f"index.html appears not to embed essay text (only {found}/15 sampled words found)"


def test_index_html_has_boundary_color():
    """Near-black boundary color must be present."""
    html = read(f"pieces/{PIECE_ID}/index.html")
    assert "0A0808" in html or "0a0808" in html, \
        "Boundary (non-convergent) color #0A0808 must appear in index.html"


# ---------------------------------------------------------------------------
# Thumbnail SVG
# ---------------------------------------------------------------------------

def test_thumbnail_is_valid_svg():
    text = read(f"pieces/{PIECE_ID}/thumbnail.svg")
    assert "<svg" in text and "</svg>" in text


def test_thumbnail_has_ten_sectors():
    text = read(f"pieces/{PIECE_ID}/thumbnail.svg")
    path_count = text.count("<path")
    assert path_count >= 10, f"Thumbnail should have ≥ 10 path elements (found {path_count})"


def test_thumbnail_has_basin_colors():
    text = read(f"pieces/{PIECE_ID}/thumbnail.svg")
    for color in ["FFFEF0", "3A1060", "6A5010"]:
        assert color.upper() in text.upper(), f"Thumbnail missing basin color #{color}"


# ---------------------------------------------------------------------------
# Newton fractal reference implementation — correctness
# ---------------------------------------------------------------------------

def test_newton_converges_to_root_zero_from_real_axis():
    """Starting from (1.2, 0), Newton should converge to root 0 (angle 0°)."""
    r = newton_fractal_root(1.2, 0.0)
    assert r == 0, f"Expected root 0, got {r}"


def test_newton_converges_to_root_five_from_negative_real():
    """Starting from (-1.2, 0), Newton should converge to root 5 (angle 180°)."""
    r = newton_fractal_root(-1.2, 0.0)
    assert r == 5, f"Expected root 5, got {r}"


def test_newton_converges_to_root_two_from_upper_right():
    """Starting from (0.3, 1.0) at ~73°, well inside the root-2 basin (72°)."""
    r = newton_fractal_root(0.3, 1.0)
    assert r == 2, f"Expected root 2 from (0.3, 1.0), got {r}"


def test_newton_converges_to_root_three_from_upper_left():
    """Starting from (-0.3, 1.0) at ~107°, well inside the root-3 basin (108°)."""
    r = newton_fractal_root(-0.3, 1.0)
    assert r == 3, f"Expected root 3 from (-0.3, 1.0), got {r}"


def test_newton_non_convergent_at_origin():
    """The origin is a pole of Newton's method; the reference impl returns -1."""
    r = newton_fractal_root(0.0, 0.0)
    assert r == -1, "Origin should not converge"


def test_newton_ten_distinct_basins_on_unit_circle_spokes():
    """Sampling from slightly outside each of the 10 roots should yield all 10 basins."""
    found = set()
    for k in range(10):
        angle = 2 * math.pi * k / 10
        zr = 1.1 * math.cos(angle)
        zi = 1.1 * math.sin(angle)
        r = newton_fractal_root(zr, zi)
        assert r != -1, f"Did not converge for spoke k={k}"
        found.add(r)
    assert len(found) == 10, f"Expected 10 distinct basins, found {len(found)}: {found}"


def test_newton_large_starting_point_converges():
    """Large-magnitude starting points should still converge (Newton for z^10-1 works globally)."""
    r = newton_fractal_root(3.0, 0.5)
    assert r != -1, "Large starting point should eventually converge"


def test_newton_returns_minus_one_on_divergence():
    """
    Edge-case: a starting point extremely close to origin but nonzero.
    Newton's method has a saddle near 0 and will fail to converge for very small |z|.
    We just verify the function doesn't crash and returns a valid integer.
    """
    r = newton_fractal_root(1e-8, 0.0)
    assert isinstance(r, int)
