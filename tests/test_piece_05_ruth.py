"""
Tests for piece 05 — "Where You Go" (Ruth in the wheat field).

Validates file layout, pieces.json entry, and key content requirements from
the acceptance criteria: noise implementation, stalk bezier drawing, silhouette
figures, Hebrew text overlay, animation loop, and color palette.
"""
import json
import os
import re

import pytest

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")
PIECE_ID = "05-ruth-wheat-field"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
INDEX_HTML = os.path.join(PIECE_DIR, "index.html")
THUMBNAIL_SVG = os.path.join(PIECE_DIR, "thumbnail.svg")
README_MD = os.path.join(PIECE_DIR, "README.md")


def _load_pieces():
    with open(PIECES_JSON, "r", encoding="utf-8") as fh:
        return json.load(fh)


def _get_piece():
    for p in _load_pieces():
        if p["id"] == PIECE_ID:
            return p
    return None


def _html():
    return open(INDEX_HTML, encoding="utf-8").read()


def _svg():
    return open(THUMBNAIL_SVG, encoding="utf-8").read()


def _readme():
    return open(README_MD, encoding="utf-8").read()


# ─── File layout ────────────────────────────────────────────────────────────

def test_index_html_exists():
    assert os.path.isfile(INDEX_HTML), "pieces/05-ruth-wheat-field/index.html missing"


def test_thumbnail_svg_exists():
    assert os.path.isfile(THUMBNAIL_SVG), "pieces/05-ruth-wheat-field/thumbnail.svg missing"


def test_readme_exists():
    assert os.path.isfile(README_MD), "pieces/05-ruth-wheat-field/README.md missing"


# ─── pieces.json entry ───────────────────────────────────────────────────────

def test_piece_in_json():
    assert _get_piece() is not None, f"'{PIECE_ID}' not found in pieces.json"


def test_piece_theme():
    p = _get_piece()
    assert p is not None
    assert p["theme"] == "Book of Ruth"


def test_piece_technique_mentions_flow_field():
    p = _get_piece()
    assert p is not None
    assert "flow field" in p["technique"].lower() or "perlin" in p["technique"].lower()


def test_piece_technique_mentions_noise():
    p = _get_piece()
    assert p is not None
    assert "noise" in p["technique"].lower()


def test_piece_paths_correct():
    p = _get_piece()
    assert p is not None
    assert p["path"] == f"pieces/{PIECE_ID}/index.html"
    assert p["thumbnail"] == f"pieces/{PIECE_ID}/thumbnail.svg"


# ─── Canvas animation ────────────────────────────────────────────────────────

def test_uses_request_animation_frame():
    assert "requestAnimationFrame" in _html(), "animation must use requestAnimationFrame"


def test_canvas_element_present():
    assert "<canvas" in _html(), "index.html must contain a <canvas> element"


# ─── Noise implementation ────────────────────────────────────────────────────

def test_noise_grid_defined():
    """Inline value noise must define a grid (Float32Array or similar)."""
    html = _html()
    assert "noiseGrid" in html or "noise_grid" in html or "GRID" in html, \
        "value noise grid variable not found in index.html"


def test_bilinear_interpolation_present():
    """Noise must interpolate between grid corners (bilinear)."""
    html = _html()
    # Bilinear interpolation needs four corner samples combined.
    # We check for the characteristic v00/v10/v01/v11 pattern or similar.
    assert re.search(r"v00|v10|v01|v11|lerp|interpolat", html), \
        "bilinear interpolation not found in noise implementation"


def test_fade_function_present():
    """Smoothstep / fade curve must be present (3t^2 - 2t^3 pattern)."""
    html = _html()
    assert "fade" in html or "smoothstep" in html or "3 - 2" in html or "3-2" in html, \
        "fade/smoothstep curve not found in noise implementation"


def test_no_external_noise_library():
    """No external noise library may be imported."""
    html = _html()
    assert "simplex" not in html.lower()
    assert "perlin.js" not in html.lower()
    assert "noisejs" not in html.lower()


# ─── Wheat stalks ────────────────────────────────────────────────────────────

def test_stalk_count_around_300():
    """HTML must define ~300 stalks (within 200–400 range is acceptable)."""
    html = _html()
    m = re.search(r"STALK_COUNT\s*=\s*(\d+)", html)
    if m:
        count = int(m.group(1))
        assert 200 <= count <= 400, f"STALK_COUNT {count} not in 200-400 range"
    else:
        # Fallback: check cols*rows product if STALK_COUNT constant absent
        cols_m = re.search(r"const cols\s*=\s*(\d+)", html)
        rows_m = re.search(r"const rows\s*=\s*(\d+)", html)
        if cols_m and rows_m:
            assert 200 <= int(cols_m.group(1)) * int(rows_m.group(1)) <= 400
        else:
            pytest.fail("Could not find stalk count definition in index.html")


def test_quadratic_bezier_used_for_stalks():
    """Stalks must be drawn as quadratic bezier curves."""
    assert "quadraticCurveTo" in _html(), "stalks must use quadraticCurveTo"


def test_stalk_height_variation():
    """Stalk heights must vary (±20% means a random factor)."""
    html = _html()
    assert re.search(r"0\.[89]\d*\s*\+\s*Math\.random|Math\.random.*0\.[234]", html), \
        "stalk height ±20% variation not found"


# ─── Silhouettes ─────────────────────────────────────────────────────────────

def test_two_figures_defined():
    """Two silhouette figures must be built (Ruth and Naomi)."""
    html = _html()
    assert "naomiFig" in html or "naomi" in html.lower(), "Naomi figure not found"
    assert "ruthFig" in html or "ruth" in html.lower(), "Ruth figure not found"


def test_silhouette_color_near_black():
    """Silhouette fill must use the specified near-black colour."""
    html = _html()
    assert "#1a0f00" in html, "silhouette colour #1a0f00 not found"


def test_path2d_used_for_figures():
    """Figures must be drawn as Path2D objects."""
    assert "Path2D" in _html(), "silhouette figures must use Path2D"


# ─── Hebrew text overlay ─────────────────────────────────────────────────────

def test_hebrew_text_present():
    """Hebrew quote must appear in the HTML."""
    html = _html()
    assert "אֵלֵךְ" in html or "תֵּלְכִי" in html or "אֲשֶׁר" in html, \
        "Hebrew text not found in index.html"


def test_rtl_direction_set():
    """ctx.direction must be set to 'rtl' for correct Hebrew rendering."""
    assert "rtl" in _html(), "ctx.direction = 'rtl' not found"


def test_text_overlay_bar():
    """A translucent overlay bar must back the text (fillRect with rgba)."""
    html = _html()
    assert re.search(r"rgba\s*\(\s*0\s*,\s*0\s*,\s*0", html), \
        "translucent overlay bar (rgba(0,0,0,...)) not found"


# ─── Color palette ───────────────────────────────────────────────────────────

def test_parchment_sky_color():
    assert "#f5e6c8" in _html() or "#f5e6c8" in _svg(), \
        "parchment sky colour #f5e6c8 not found"


def test_golden_wheat_color():
    assert "#d4a017" in _html() or "#d4a017" in _svg(), \
        "golden wheat colour #d4a017 not found"


def test_dark_wheat_color():
    assert "#8b6914" in _html() or "#8b6914" in _svg(), \
        "dark wheat colour #8b6914 not found"


# ─── Thumbnail ───────────────────────────────────────────────────────────────

def test_thumbnail_is_valid_svg():
    svg = _svg()
    assert "<svg" in svg and "</svg>" in svg, "thumbnail.svg is not valid SVG"


def test_thumbnail_has_field_gradient():
    """Thumbnail must represent the golden field."""
    svg = _svg()
    assert "#d4a017" in svg or "#8b6914" in svg, \
        "thumbnail.svg missing wheat field colours"


def test_thumbnail_has_text_bar():
    """Thumbnail should include the Hebrew text or its overlay bar."""
    svg = _svg()
    assert "אֵלֵךְ" in svg or "תֵּלְכִי" in svg or "rgba(0,0,0" in svg, \
        "thumbnail.svg missing text overlay"


def test_thumbnail_has_silhouettes():
    """Thumbnail must include dark silhouette shapes."""
    svg = _svg()
    assert "#1a0f00" in svg, "thumbnail.svg missing silhouette colour #1a0f00"


# ─── README ──────────────────────────────────────────────────────────────────

def test_readme_mentions_book_of_ruth():
    text = _readme().lower()
    assert "ruth" in text, "README.md must mention the Book of Ruth theme"


def test_readme_mentions_noise_technique():
    text = _readme().lower()
    assert "noise" in text, "README.md must describe the noise technique"


def test_readme_mentions_bezier():
    text = _readme().lower()
    assert "bezier" in text or "bézier" in text, \
        "README.md must mention bezier curves"


# ─── Edge cases ──────────────────────────────────────────────────────────────

def test_no_hard_reset_setinterval():
    """Animation must not use setInterval (would cause visible resets)."""
    html = _html()
    # setInterval is acceptable for non-animation tasks, but the main loop
    # should use requestAnimationFrame. Warn if setInterval drives animation.
    assert html.count("setInterval") == 0 or "requestAnimationFrame" in html, \
        "setInterval without requestAnimationFrame may cause hard resets"


def test_html_charset_utf8():
    """HTML must declare UTF-8 to render Hebrew correctly."""
    assert 'charset="UTF-8"' in _html() or "charset=utf-8" in _html().lower(), \
        "index.html must declare UTF-8 charset for Hebrew rendering"


def test_pieces_json_no_duplicate_ids():
    pieces = _load_pieces()
    ids = [p["id"] for p in pieces]
    assert len(ids) == len(set(ids)), f"Duplicate piece IDs: {ids}"
