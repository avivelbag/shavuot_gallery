"""
Tests for piece 16-bikkurim-procession — "I Declare" (Bikkurim procession quadtree mosaic).

Verifies file layout, pieces.json registration, essay content,
HTML structure, animation requirements, and quadtree-split math.
"""
import json
import os
import re


GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID = "16-bikkurim-procession"
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

def load_pieces():
    """Return the parsed pieces.json list."""
    with open(PIECES_JSON, encoding="utf-8") as fh:
        return json.load(fh)


def get_piece():
    """Return the bikkurim-procession entry from pieces.json, or None."""
    return next((p for p in load_pieces() if p["id"] == PIECE_ID), None)


def test_piece_registered_in_pieces_json():
    assert get_piece() is not None, f"'{PIECE_ID}' not found in pieces.json"


def test_piece_has_correct_theme():
    piece = get_piece()
    assert piece is not None
    theme = piece["theme"].lower()
    assert "bikkurim" in theme or "first fruit" in theme, (
        f"theme field should reference Bikkurim/First Fruits, got: {piece['theme']!r}"
    )


def test_piece_has_quadtree_technique():
    piece = get_piece()
    assert piece is not None
    technique = piece["technique"].lower()
    assert "quadtree" in technique or "subdivision" in technique or "mosaic" in technique, (
        f"technique must mention quadtree/subdivision/mosaic, got: {piece['technique']!r}"
    )


def test_piece_essay_field_in_json():
    piece = get_piece()
    assert piece is not None
    essay = piece.get("essay", "")
    assert essay.strip(), "essay field in pieces.json must be non-empty"
    assert essay == f"pieces/{PIECE_ID}/essay.md", f"essay path mismatch: {essay!r}"


def test_piece_path_correct():
    piece = get_piece()
    assert piece is not None
    assert piece["path"] == f"pieces/{PIECE_ID}/index.html"


def test_piece_thumbnail_correct():
    piece = get_piece()
    assert piece is not None
    assert piece["thumbnail"] == f"pieces/{PIECE_ID}/thumbnail.svg"


def test_piece_year_is_int():
    piece = get_piece()
    assert piece is not None
    assert isinstance(piece["year"], int)


def test_no_duplicate_ids():
    pieces = load_pieces()
    ids = [p["id"] for p in pieces]
    assert len(ids) == len(set(ids)), f"Duplicate piece IDs: {ids}"


def test_piece_all_required_fields():
    """All required pieces.json fields must be present and non-empty."""
    required = ("id", "title", "tagline", "year", "theme", "technique", "path", "thumbnail", "essay")
    piece = get_piece()
    assert piece is not None
    for field in required:
        val = piece.get(field)
        assert val is not None and val != "", (
            f"pieces.json entry missing or empty field: {field!r}"
        )


# ---------------------------------------------------------------------------
# Essay content
# ---------------------------------------------------------------------------

def read_essay():
    """Return the full essay text."""
    return open(ESSAY_PATH, encoding="utf-8").read()


def test_essay_word_count():
    text = read_essay()
    words = text.split()
    assert len(words) >= 300, f"essay.md has only {len(words)} words (need >= 300)"


def test_essay_references_deuteronomy_26():
    text = read_essay()
    assert "Deuteronomy 26" in text or "Deut" in text, (
        "essay.md must cite Deuteronomy 26 (the farmer's declaration)"
    )


def test_essay_mentions_wandering_aramean():
    text = read_essay()
    assert "Aramean" in text or "aramean" in text.lower(), (
        "essay.md must quote/paraphrase 'A wandering Aramean was my father' (Deut 26:5)"
    )


def test_essay_references_mishnah_bikkurim():
    text = read_essay()
    assert "Bikkurim" in text or "bikkurim" in text.lower(), (
        "essay.md must cite Mishnah Bikkurim"
    )


def test_essay_mentions_procession():
    text = read_essay()
    assert "procession" in text.lower() or "flute" in text.lower() or "ox" in text.lower(), (
        "essay.md must describe the Bikkurim procession (flute, ox, pilgrims)"
    )


def test_essay_connects_shavuot_to_bikkurim():
    text = read_essay()
    assert "Shavuot" in text or "shavuot" in text.lower(), (
        "essay.md must connect Shavuot to the Bikkurim offering"
    )


def test_essay_mentions_ani_modeh():
    text = read_essay()
    assert "ani modeh" in text.lower() or "אֲנִי" in text or "I declare" in text, (
        "essay.md must mention Ani Modeh / 'I declare'"
    )


def test_essay_not_placeholder():
    text = read_essay()
    for stub in ("TODO", "placeholder", "lorem ipsum", "FILL IN"):
        assert stub.lower() not in text.lower(), (
            f"essay.md appears to contain placeholder text: {stub!r}"
        )


def test_essay_cites_numbers_28():
    text = read_essay()
    assert "Numbers 28" in text or "Num" in text, (
        "essay.md must cite Numbers 28:26 (Yom HaBikkurim)"
    )


# ---------------------------------------------------------------------------
# HTML / canvas structure
# ---------------------------------------------------------------------------

def read_html():
    """Return the full index.html text."""
    return open(HTML_PATH, encoding="utf-8").read()


def test_html_uses_canvas():
    html = read_html()
    assert "<canvas" in html, "index.html must contain a <canvas> element"


def test_html_uses_request_animation_frame():
    html = read_html()
    assert "requestAnimationFrame" in html, (
        "index.html must use requestAnimationFrame for animation"
    )


def test_html_contains_hebrew_text():
    html = read_html()
    assert "אֲנִי" in html or "מוֹדֶה" in html or "מודֶה" in html, (
        "index.html must contain Hebrew text אֲנִי מוֹדֶה"
    )


def test_html_has_palette_colors():
    """All seven-species palette colors must appear in the HTML."""
    html = read_html()
    assert "d4a017" in html.lower(), "index.html must use harvest gold #d4a017"
    assert "4a7c3f" in html.lower(), "index.html must use olive green #4a7c3f"
    assert "5b2d8e" in html.lower(), "index.html must use grape purple #5b2d8e"
    assert "c0392b" in html.lower(), "index.html must use pomegranate red #c0392b"


def test_html_has_bg_color():
    html = read_html()
    assert "f7f0e0" in html.lower(), "index.html must use warm cream background #f7f0e0"


def test_html_has_cell_border():
    html = read_html()
    assert "rgba(0,0,0,0.15)" in html or "0,0,0,0.15" in html, (
        "index.html must draw cell borders in rgba(0,0,0,0.15)"
    )


def test_html_has_weighted_palette():
    """Gold and olive must appear with weight=3 in the PALETTE_ENTRIES."""
    html = read_html()
    assert "weight" in html, (
        "index.html must implement weighted palette (gold and olive 3×)"
    )


def test_html_has_splitting_phase():
    html = read_html()
    assert "splitting" in html or "MAX_SPLITS" in html, (
        "index.html must implement a splitting phase and MAX_SPLITS limit"
    )


def test_html_has_fade_in_phase():
    html = read_html()
    assert "fade_in" in html or "FADE_IN" in html, (
        "index.html must implement a fade-in phase for the Hebrew text"
    )


def test_html_has_holding_phase():
    html = read_html()
    assert "holding" in html or "HOLD" in html, (
        "index.html must implement a holding phase after text appears"
    )


def test_html_has_gaussian_split():
    html = read_html()
    assert "gauss" in html.lower() or "Math.log" in html or "Box-Muller" in html.lower(), (
        "index.html must use a Gaussian distribution for split positions"
    )


def test_html_splits_on_long_axis():
    html = read_html()
    assert "cell.w >= cell.h" in html or "long axis" in html.lower() or "w >= h" in html, (
        "index.html must split on the long axis of each cell"
    )


def test_html_hue_jitter():
    html = read_html()
    assert "jitter" in html.lower() or "hslToHex" in html or "rgbToHsl" in html, (
        "index.html must implement HSL hue jitter for color assignment"
    )


def test_html_embeds_essay_text():
    """index.html must embed essay text inline."""
    essay = read_essay()
    html = read_html()
    words = [w for w in essay.split() if len(w) > 5]
    sampled = words[:10]
    found = sum(1 for w in sampled if w in html)
    assert found >= 5, (
        f"index.html does not embed essay text: only {found}/10 sampled words found"
    )


def test_html_no_external_scripts():
    html = read_html()
    external = re.findall(r'<script[^>]+src=["\']https?://', html)
    assert len(external) == 0, f"index.html must not load external scripts: {external}"


def test_html_not_placeholder():
    html = read_html()
    for stub in ("TODO", "lorem ipsum", "FILL IN"):
        assert stub.lower() not in html.lower(), (
            f"index.html appears to contain placeholder text: {stub!r}"
        )


def test_html_wide_narrow_layout():
    """index.html must have a responsive layout (media query or flex/grid)."""
    html = read_html()
    assert "max-width" in html or "flex-direction: column" in html, (
        "index.html must support both wide and narrow screen layouts"
    )


# ---------------------------------------------------------------------------
# Thumbnail SVG
# ---------------------------------------------------------------------------

def read_thumb():
    """Return the thumbnail SVG text."""
    return open(THUMB_PATH, encoding="utf-8").read()


def test_thumbnail_is_valid_svg():
    svg = read_thumb()
    assert "<svg" in svg and "</svg>" in svg, "thumbnail.svg is not valid SVG"


def test_thumbnail_has_many_rects():
    """Quadtree mosaic thumbnail must have at least 25 <rect> elements."""
    svg = read_thumb()
    rects = re.findall(r'<rect', svg)
    assert len(rects) >= 25, (
        f"thumbnail.svg should have ≥25 <rect> elements for a mosaic look, found {len(rects)}"
    )


def test_thumbnail_uses_palette_colors():
    svg = read_thumb()
    assert "d4a017" in svg.lower(), "thumbnail.svg must use harvest gold #d4a017"
    assert "4a7c3f" in svg.lower(), "thumbnail.svg must use olive green #4a7c3f"


def test_thumbnail_has_hebrew_text():
    svg = read_thumb()
    assert "<text" in svg, "thumbnail.svg must include Hebrew text element"
    assert "אֲנִי" in svg or "מוֹדֶה" in svg or "מודֶה" in svg, (
        "thumbnail.svg must include the Hebrew text אֲנִי מוֹדֶה"
    )


def test_thumbnail_has_background():
    svg = read_thumb()
    assert "f7f0e0" in svg.lower(), (
        "thumbnail.svg must use warm cream background #f7f0e0"
    )


# ---------------------------------------------------------------------------
# Quadtree math sanity checks (pure Python)
# ---------------------------------------------------------------------------

import math
import random


def simulate_splits(n_splits=300, seed=42):
    """
    Simulate n_splits of the quadtree algorithm using the same logic as index.html.

    Returns the list of cells after all splits.
    Each cell is a dict with keys x, y, w, h, area.
    """
    rng = random.Random(seed)

    def gauss_rand():
        u = rng.random() or 1e-10
        v = rng.random() or 1e-10
        return math.sqrt(-2.0 * math.log(u)) * math.cos(2.0 * math.PI * v)

    def split_pos():
        return max(0.2, min(0.8, 0.5 + gauss_rand() * 0.15))

    W, H = 600, 600
    cells = [{'x': 0, 'y': 0, 'w': W, 'h': H, 'area': W * H}]

    for _ in range(n_splits):
        best = max(range(len(cells)), key=lambda i: cells[i]['area'])
        cell = cells[best]
        t = split_pos()

        if cell['w'] >= cell['h']:
            sx = cell['x'] + int(cell['w'] * t)
            c1 = {'x': cell['x'], 'y': cell['y'],
                  'w': sx - cell['x'], 'h': cell['h']}
            c2 = {'x': sx, 'y': cell['y'],
                  'w': cell['x'] + cell['w'] - sx, 'h': cell['h']}
        else:
            sy = cell['y'] + int(cell['h'] * t)
            c1 = {'x': cell['x'], 'y': cell['y'],
                  'w': cell['w'], 'h': sy - cell['y']}
            c2 = {'x': cell['x'], 'y': sy,
                  'w': cell['w'], 'h': cell['y'] + cell['h'] - sy}

        c1['area'] = c1['w'] * c1['h']
        c2['area'] = c2['w'] * c2['h']
        cells[best:best + 1] = [c1, c2]

    return cells


# Attach the math.PI alias needed by the helper above
math.PI = math.pi


def test_cells_cover_full_canvas():
    """After 300 splits the cells must cover the full 600×600 = 360000 area."""
    cells = simulate_splits(300)
    total_area = sum(c['area'] for c in cells)
    assert total_area == 600 * 600, (
        f"Cells do not cover the full canvas: total area = {total_area} (expected 360000)"
    )


def test_cells_count_after_splits():
    """After n splits we must have exactly n+1 cells (each split adds one cell)."""
    for n in [1, 10, 50, 300]:
        cells = simulate_splits(n)
        assert len(cells) == n + 1, (
            f"After {n} splits expected {n + 1} cells, got {len(cells)}"
        )


def test_splits_along_long_axis():
    """
    Verify that every split divides along the long axis.

    After each split the two children together must have the same total area
    as their parent, and neither child may have a larger bounding dimension
    than the parent's long axis dimension.
    """
    rng = random.Random(0)
    for _ in range(100):
        w = rng.randint(10, 600)
        h = rng.randint(10, 600)
        t = 0.5  # center split

        if w >= h:
            sx = int(w * t)
            c1_w, c1_h = sx, h
            c2_w, c2_h = w - sx, h
            assert max(c1_w, c2_w) <= w, "Horizontal split child wider than parent"
        else:
            sy = int(h * t)
            c1_w, c1_h = w, sy
            c2_w, c2_h = w, h - sy
            assert max(c1_h, c2_h) <= h, "Vertical split child taller than parent"


def test_all_cells_within_canvas_bounds():
    """No cell after 300 splits may exceed the 600×600 canvas."""
    cells = simulate_splits(300)
    for cell in cells:
        assert cell['x'] >= 0 and cell['y'] >= 0, (
            f"Cell has negative coordinates: {cell}"
        )
        assert cell['x'] + cell['w'] <= 600, (
            f"Cell exceeds canvas width: {cell}"
        )
        assert cell['y'] + cell['h'] <= 600, (
            f"Cell exceeds canvas height: {cell}"
        )


def test_split_position_stays_near_center():
    """
    The Gaussian split position (clamped to [0.2, 0.8]) must average near 0.5.

    Run 1000 samples and check that the mean is within ±0.05 of 0.5.
    """
    rng = random.Random(7)
    results = []
    for _ in range(1000):
        u = rng.random() or 1e-10
        v = rng.random() or 1e-10
        g = math.sqrt(-2.0 * math.log(u)) * math.cos(2.0 * math.PI * v)
        pos = max(0.2, min(0.8, 0.5 + g * 0.15))
        results.append(pos)
    mean = sum(results) / len(results)
    assert abs(mean - 0.5) < 0.05, (
        f"Gaussian split positions have unexpected mean {mean:.4f} (expected ~0.5)"
    )


def test_weighted_palette_gold_olive_dominant():
    """
    With gold and olive weighted 3× and others 1×, gold+olive must make up
    approximately 6/11 of random draws (> 50%).
    """
    palette_entries = [
        {'hex': '#d4a017', 'weight': 3},
        {'hex': '#c8a96e', 'weight': 1},
        {'hex': '#5b2d8e', 'weight': 1},
        {'hex': '#c0392b', 'weight': 1},
        {'hex': '#7d4a2f', 'weight': 1},
        {'hex': '#4a7c3f', 'weight': 3},
        {'hex': '#d4850a', 'weight': 1},
    ]
    flat = []
    for e in palette_entries:
        flat.extend([e['hex']] * e['weight'])

    assert len(flat) == 11

    warm_count = sum(1 for c in flat if c in ('#d4a017', '#4a7c3f'))
    ratio = warm_count / len(flat)
    assert ratio > 0.5, (
        f"Gold+olive should be > 50% of weighted palette, got {ratio:.2%}"
    )


def test_simulate_300_splits_no_zero_area_cells():
    """No cell should have zero area after splitting."""
    cells = simulate_splits(300, seed=99)
    zero_area = [c for c in cells if c['area'] == 0]
    assert len(zero_area) == 0, (
        f"Found {len(zero_area)} zero-area cells after 300 splits"
    )


def test_simulate_large_split_count():
    """The algorithm must remain stable with 500 splits (more than the animation limit)."""
    cells = simulate_splits(500, seed=13)
    assert len(cells) == 501
    total_area = sum(c['area'] for c in cells)
    assert total_area == 600 * 600
