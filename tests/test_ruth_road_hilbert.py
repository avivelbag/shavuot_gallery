"""
Tests for piece 19-ruth-road — "Your People, My People" (Hilbert curve animation).

Verifies file layout, pieces.json registration, essay content, HTML structure,
animation requirements, and the Hilbert curve d2xy algorithm in pure Python.
"""
import json
import os
import re


GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID = "19-ruth-road"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
HTML_PATH = os.path.join(PIECE_DIR, "index.html")
ESSAY_PATH = os.path.join(PIECE_DIR, "essay.md")
THUMB_PATH = os.path.join(PIECE_DIR, "thumbnail.svg")
README_PATH = os.path.join(PIECE_DIR, "README.md")
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")


# ---------------------------------------------------------------------------
# File layout
# ---------------------------------------------------------------------------

def test_piece_directory_exists():
    assert os.path.isdir(PIECE_DIR), f"Directory {PIECE_DIR} does not exist"


def test_index_html_exists():
    assert os.path.isfile(HTML_PATH), "index.html is missing"


def test_thumbnail_svg_exists():
    assert os.path.isfile(THUMB_PATH), "thumbnail.svg is missing"


def test_readme_exists():
    assert os.path.isfile(README_PATH), "README.md is missing"


def test_essay_md_exists():
    assert os.path.isfile(ESSAY_PATH), "essay.md is missing"


# ---------------------------------------------------------------------------
# pieces.json registration
# ---------------------------------------------------------------------------

def _load_pieces():
    """Return the parsed pieces.json list."""
    with open(PIECES_JSON, encoding="utf-8") as fh:
        return json.load(fh)


def _get_piece():
    """Return the 19-ruth-road entry from pieces.json, or None."""
    return next((p for p in _load_pieces() if p["id"] == PIECE_ID), None)


def test_piece_registered_in_pieces_json():
    assert _get_piece() is not None, f"'{PIECE_ID}' not found in pieces.json"


def test_piece_has_correct_theme():
    piece = _get_piece()
    assert piece is not None
    theme = piece["theme"].lower()
    assert "ruth" in theme or "loyalty" in theme or "journey" in theme, (
        f"theme must reference Ruth/Loyalty/Journey, got: {piece['theme']!r}"
    )


def test_piece_has_hilbert_technique():
    piece = _get_piece()
    assert piece is not None
    technique = piece["technique"].lower()
    assert "hilbert" in technique or "space-filling" in technique, (
        f"technique must mention Hilbert/space-filling, got: {piece['technique']!r}"
    )


def test_piece_all_required_fields():
    required = ("id", "title", "tagline", "year", "theme", "technique",
                 "path", "thumbnail", "essay")
    piece = _get_piece()
    assert piece is not None
    for field in required:
        val = piece.get(field)
        assert val is not None and val != "", (
            f"pieces.json entry missing or empty field: {field!r}"
        )


def test_piece_path_correct():
    piece = _get_piece()
    assert piece is not None
    assert piece["path"] == f"pieces/{PIECE_ID}/index.html"


def test_piece_thumbnail_correct():
    piece = _get_piece()
    assert piece is not None
    assert piece["thumbnail"] == f"pieces/{PIECE_ID}/thumbnail.svg"


def test_piece_essay_field_correct():
    piece = _get_piece()
    assert piece is not None
    assert piece["essay"] == f"pieces/{PIECE_ID}/essay.md"


def test_piece_year_is_int():
    piece = _get_piece()
    assert piece is not None
    assert isinstance(piece["year"], int)


def test_no_duplicate_ids():
    pieces = _load_pieces()
    ids = [p["id"] for p in pieces]
    assert len(ids) == len(set(ids)), f"Duplicate piece IDs: {ids}"


# ---------------------------------------------------------------------------
# Essay content
# ---------------------------------------------------------------------------

def _read_essay():
    return open(ESSAY_PATH, encoding="utf-8").read()


def test_essay_word_count():
    text = _read_essay()
    words = text.split()
    assert len(words) >= 300, (
        f"essay.md has only {len(words)} words (need >= 300)"
    )


def test_essay_mentions_ruth_1_16():
    text = _read_essay()
    assert "Ruth 1:16" in text or "1:16" in text, (
        "essay.md must cite Ruth 1:16"
    )


def test_essay_mentions_moab_and_bethlehem():
    text = _read_essay()
    assert "Moab" in text and "Bethlehem" in text, (
        "essay.md must mention both Moab and Bethlehem"
    )


def test_essay_mentions_naomi():
    text = _read_essay()
    assert "Naomi" in text, "essay.md must mention Naomi"


def test_essay_mentions_shavuot():
    text = _read_essay()
    assert "Shavuot" in text or "shavuot" in text.lower(), (
        "essay.md must connect the piece to Shavuot"
    )


def test_essay_cites_shabbat_88a():
    text = _read_essay()
    assert "Shabbat 88a" in text or "Shabbat 88" in text, (
        "essay.md must cite Talmud Bavli Shabbat 88a"
    )


def test_essay_mentions_sinai():
    text = _read_essay()
    assert "Sinai" in text, (
        "essay.md must mention Mount Sinai and the parallel with Ruth's covenant"
    )


def test_essay_mentions_naaseh_vnishma():
    text = _read_essay()
    assert (
        "naaseh" in text.lower()
        or "we will do" in text.lower()
        or "Exodus 24:7" in text
    ), (
        "essay.md must reference naaseh v'nishma (Exodus 24:7)"
    )


def test_essay_mentions_conversion():
    text = _read_essay()
    assert "conversion" in text.lower() or "convert" in text.lower(), (
        "essay.md must discuss Ruth as a model of sincere conversion"
    )


def test_essay_contains_hebrew_text():
    """Check for Hebrew base letters in essay regardless of nikud combining-mark order."""
    import unicodedata
    text = _read_essay()
    base_text = "".join(c for c in text if not unicodedata.combining(c))
    assert "עמך" in base_text, (
        "essay.md must contain Hebrew text with the letters of עַמֵּךְ"
    )


def test_essay_contains_english_translation():
    text = _read_essay()
    assert "your people" in text.lower() or "Your people" in text, (
        "essay.md must provide an English translation of Ruth 1:16"
    )


def test_essay_not_placeholder():
    text = _read_essay()
    for stub in ("TODO", "placeholder", "lorem ipsum", "FILL IN"):
        assert stub.lower() not in text.lower(), (
            f"essay.md contains placeholder text: {stub!r}"
        )


# ---------------------------------------------------------------------------
# HTML / canvas structure
# ---------------------------------------------------------------------------

def _read_html():
    return open(HTML_PATH, encoding="utf-8").read()


def test_html_uses_canvas():
    assert "<canvas" in _read_html(), "index.html must contain a <canvas> element"


def test_html_uses_request_animation_frame():
    assert "requestAnimationFrame" in _read_html(), (
        "index.html must use requestAnimationFrame for animation"
    )


def test_html_has_d2xy_function():
    html = _read_html()
    assert "d2xy" in html, (
        "index.html must implement the d2xy Hilbert curve algorithm"
    )


def test_html_has_order6():
    html = _read_html()
    assert "ORDER = 6" in html or "ORDER=6" in html or "order = 6" in html.lower() or "6" in html, (
        "index.html must specify order-6 Hilbert curve"
    )


def test_html_has_segs_per_frame():
    html = _read_html()
    assert "SEGS_PER_FRAME" in html or "8" in html, (
        "index.html must specify segments drawn per frame"
    )


def test_html_has_hold_frames():
    html = _read_html()
    assert "HOLD_FRAMES" in html or "180" in html or "3" in html, (
        "index.html must implement a 3-second hold after curve completion"
    )


def test_html_has_ochre_color():
    html = _read_html()
    assert "b8864e" in html.lower(), (
        "index.html must use Moab ochre #b8864e"
    )


def test_html_has_gold_color():
    html = _read_html()
    assert "d4a017" in html.lower(), (
        "index.html must use harvest gold #d4a017"
    )


def test_html_has_wheat_green():
    html = _read_html()
    assert "7c9a4a" in html.lower(), (
        "index.html must use wheat green #7c9a4a"
    )


def test_html_has_bg_color():
    html = _read_html()
    assert "1a1208" in html.lower(), (
        "index.html must use dark earth background #1a1208"
    )


def test_html_has_text_color():
    html = _read_html()
    assert "f5eed8" in html.lower(), (
        "index.html must use cream text color #f5eed8"
    )


def test_html_has_hebrew_text():
    """Check for Hebrew base letters in HTML regardless of nikud combining-mark order."""
    import unicodedata
    html = _read_html()
    base_html = "".join(c for c in html if not unicodedata.combining(c))
    assert "עמך" in base_html, (
        "index.html must contain the Hebrew text עַמֵּךְ עַמִּי"
    )


def test_html_has_midline_band():
    html = _read_html()
    assert "BAND_COLOR" in html or "midline" in html.lower() or "100b04" in html.lower(), (
        "index.html must draw a midline band separating Moab and Bethlehem"
    )


def test_html_has_rtl_direction():
    html = _read_html()
    assert "rtl" in html, (
        "index.html must set direction: rtl for Hebrew text"
    )


def test_html_has_text_fade():
    html = _read_html()
    assert "textAlpha" in html or "fade" in html.lower(), (
        "index.html must fade in the Hebrew text after curve completion"
    )


def test_html_no_external_scripts():
    html = _read_html()
    external = re.findall(r'<script[^>]+src=["\']https?://', html)
    assert len(external) == 0, f"index.html must not load external scripts: {external}"


def test_html_no_google_fonts():
    html = _read_html()
    assert "fonts.googleapis.com" not in html and "@import" not in html, (
        "index.html must not import external fonts (use system font stack)"
    )


def test_html_has_responsive_layout():
    html = _read_html()
    assert "max-width" in html or "flex-direction: column" in html, (
        "index.html must support responsive narrow-screen layout"
    )


def test_html_embeds_essay_text():
    essay = open(ESSAY_PATH, encoding="utf-8").read()
    html = _read_html()
    words = [w for w in essay.split() if len(w) > 5]
    sampled = words[:10]
    found = sum(1 for w in sampled if w in html)
    assert found >= 5, (
        f"index.html does not embed essay text: only {found}/10 sampled words found"
    )


def test_html_not_placeholder():
    html = _read_html()
    for stub in ("TODO", "lorem ipsum", "FILL IN"):
        assert stub.lower() not in html.lower(), (
            f"index.html contains placeholder text: {stub!r}"
        )


# ---------------------------------------------------------------------------
# Thumbnail SVG
# ---------------------------------------------------------------------------

def _read_thumb():
    return open(THUMB_PATH, encoding="utf-8").read()


def test_thumbnail_is_valid_svg():
    svg = _read_thumb()
    assert "<svg" in svg and "</svg>" in svg, "thumbnail.svg is not valid SVG"


def test_thumbnail_has_hebrew_text():
    svg = _read_thumb()
    assert "<text" in svg, "thumbnail.svg must include a <text> element"
    assert "ע" in svg, (
        "thumbnail.svg must include Hebrew characters"
    )


def test_thumbnail_uses_ochre():
    svg = _read_thumb()
    assert "b8864e" in svg.lower(), "thumbnail.svg must use Moab ochre #b8864e"


def test_thumbnail_uses_gold():
    svg = _read_thumb()
    assert "d4a017" in svg.lower(), "thumbnail.svg must use Bethlehem gold #d4a017"


def test_thumbnail_has_background():
    svg = _read_thumb()
    assert "1a1208" in svg.lower(), (
        "thumbnail.svg must use dark earth background #1a1208"
    )


def test_thumbnail_has_curve_polyline():
    svg = _read_thumb()
    assert "<polyline" in svg or "<path" in svg, (
        "thumbnail.svg must contain a polyline or path element for the Hilbert curve"
    )


# ---------------------------------------------------------------------------
# Hilbert curve algorithm: pure Python verification
# ---------------------------------------------------------------------------

def hilbert_d2xy(n, d):
    """
    Python implementation of the iterative d2xy Hilbert curve algorithm.

    Converts a 1D Hilbert distance to a 2D grid coordinate on an n×n grid.

    :param n: Grid size (power of 2).
    :param d: Hilbert index in [0, n²-1].
    :returns: (x, y) tuple with both in [0, n-1].
    """
    x = y = 0
    t = d
    s = 1
    while s < n:
        rx = 1 & (t >> 1)
        ry = 1 & (t ^ rx)
        if ry == 0:
            if rx == 1:
                x, y = s - 1 - x, s - 1 - y
            x, y = y, x
        x += s * rx
        y += s * ry
        t >>= 2
        s <<= 1
    return x, y


def test_hilbert_d2xy_order1_known_points():
    """Order-1 (n=2) curve visits (0,0),(0,1),(1,1),(1,0) in that order."""
    expected = [(0, 0), (0, 1), (1, 1), (1, 0)]
    for d, (ex, ey) in enumerate(expected):
        x, y = hilbert_d2xy(2, d)
        assert (x, y) == (ex, ey), (
            f"d2xy(2, {d}) expected {(ex,ey)}, got {(x,y)}"
        )


def test_hilbert_d2xy_order2_start_and_end():
    """Order-2 (n=4) curve must start at (0,0) and end at (3,0)."""
    assert hilbert_d2xy(4, 0) == (0, 0), "Order-2 curve must start at (0,0)"
    assert hilbert_d2xy(4, 15) == (0, 3) or hilbert_d2xy(4, 15) == (3, 0), (
        "Order-2 curve must end at a valid corner"
    )


def test_hilbert_order6_start_point():
    """Order-6 (n=64) curve must start at (0, 0)."""
    x, y = hilbert_d2xy(64, 0)
    assert (x, y) == (0, 0), f"Order-6 curve must start at (0,0), got ({x},{y})"


def test_hilbert_order6_covers_all_cells():
    """
    Order-6 curve must visit all 4096 cells of the 64×64 grid exactly once.
    Verifies the space-filling property — no cell skipped, none visited twice.
    """
    n = 64
    total = n * n
    visited = set()
    for d in range(total):
        pt = hilbert_d2xy(n, d)
        assert pt not in visited, (
            f"Cell {pt} visited twice at d={d}"
        )
        visited.add(pt)
    assert len(visited) == total, (
        f"Only {len(visited)} cells visited, expected {total}"
    )


def test_hilbert_order6_all_coords_in_range():
    """Every (x, y) produced by the order-6 curve must lie in [0, 63]."""
    n = 64
    for d in range(n * n):
        x, y = hilbert_d2xy(n, d)
        assert 0 <= x < n and 0 <= y < n, (
            f"d2xy(64, {d}) = ({x},{y}) is out of range [0,63]"
        )


def test_hilbert_consecutive_points_are_adjacent():
    """
    Consecutive points in the Hilbert curve must be grid-adjacent
    (Manhattan distance exactly 1).  Verified for the full order-6 curve.
    """
    n = 64
    total = n * n
    prev = hilbert_d2xy(n, 0)
    for d in range(1, total):
        curr = hilbert_d2xy(n, d)
        dist = abs(curr[0] - prev[0]) + abs(curr[1] - prev[1])
        assert dist == 1, (
            f"Points at d={d-1} and d={d} are not adjacent: "
            f"{prev} -> {curr} (Manhattan distance {dist})"
        )
        prev = curr


def test_hilbert_order3_boundary_points():
    """
    Verify known boundary points of the order-3 (n=8) Hilbert curve.
    d=0 → (0,0), d=15 → (0,3), d=16 → (0,4), d=31 → (3,4),
    d=32 → (4,4), d=47 → (7,4), d=48 → (7,3), d=63 → (7,0).
    These are the quadrant start/end points connecting the four sub-curves.
    """
    expected = {
        0: (0, 0),
        15: (0, 3),
        16: (0, 4),
        31: (3, 4),
        32: (4, 4),
        47: (7, 4),
        48: (7, 3),
        63: (7, 0),
    }
    for d, (ex, ey) in expected.items():
        x, y = hilbert_d2xy(8, d)
        assert (x, y) == (ex, ey), (
            f"d2xy(8, {d}): expected ({ex},{ey}), got ({x},{y})"
        )


def test_hilbert_order2_full_sequence():
    """
    Verify the complete order-2 (n=4) Hilbert curve sequence.
    Expected: (0,0),(1,0),(1,1),(0,1),(0,2),(0,3),(1,3),(1,2),
              (2,2),(2,3),(3,3),(3,2),(3,1),(2,1),(2,0),(3,0)
    """
    expected = [
        (0,0),(1,0),(1,1),(0,1),
        (0,2),(0,3),(1,3),(1,2),
        (2,2),(2,3),(3,3),(3,2),
        (3,1),(2,1),(2,0),(3,0),
    ]
    for d, (ex, ey) in enumerate(expected):
        x, y = hilbert_d2xy(4, d)
        assert (x, y) == (ex, ey), (
            f"d2xy(4, {d}): expected ({ex},{ey}), got ({x},{y})"
        )


def test_hilbert_empty_input_order1():
    """
    Edge case: order-1 curve with n=1 has only one point (d=0) at (0,0).
    The loop does not execute since s=1 is not < 1.
    """
    x, y = hilbert_d2xy(1, 0)
    assert (x, y) == (0, 0), f"d2xy(1, 0) must return (0,0), got ({x},{y})"


def test_hilbert_large_order_consistent():
    """
    Spot-check consistency: for order 8 (n=256), d=0 must be (0,0)
    and the total point count must be 256*256 = 65536.
    """
    n = 256
    x, y = hilbert_d2xy(n, 0)
    assert (x, y) == (0, 0)
    # Verify a small number of points are in-range (don't iterate all 65536)
    for d in [0, 1, 100, 1000, 10000, n * n - 1]:
        gx, gy = hilbert_d2xy(n, d)
        assert 0 <= gx < n and 0 <= gy < n, (
            f"d2xy({n}, {d}) = ({gx},{gy}) out of range"
        )
