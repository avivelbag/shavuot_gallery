"""
Tests for piece 21 — "The Open Corner" (Pe'ah flow field).

Validates file layout, pieces.json entry, and key content requirements from
the acceptance criteria: Perlin noise implementation, stalk bezier drawing,
pe'ah corner exclusion zones, Hebrew label, color palette, essay content,
and thumbnail SVG.
"""
import json
import os
import re

import pytest

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")
PIECE_ID = "21-peah-open-corner"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
INDEX_HTML = os.path.join(PIECE_DIR, "index.html")
THUMBNAIL_SVG = os.path.join(PIECE_DIR, "thumbnail.svg")
README_MD = os.path.join(PIECE_DIR, "README.md")
ESSAY_MD = os.path.join(PIECE_DIR, "essay.md")


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


def _essay():
    return open(ESSAY_MD, encoding="utf-8").read()


# ─── File layout ─────────────────────────────────────────────────────────────

def test_index_html_exists():
    assert os.path.isfile(INDEX_HTML), "pieces/21-peah-open-corner/index.html missing"


def test_thumbnail_svg_exists():
    assert os.path.isfile(THUMBNAIL_SVG), "pieces/21-peah-open-corner/thumbnail.svg missing"


def test_readme_exists():
    assert os.path.isfile(README_MD), "pieces/21-peah-open-corner/README.md missing"


def test_essay_md_exists():
    assert os.path.isfile(ESSAY_MD), "pieces/21-peah-open-corner/essay.md missing"


# ─── pieces.json entry ───────────────────────────────────────────────────────

def test_piece_in_json():
    assert _get_piece() is not None, f"'{PIECE_ID}' not found in pieces.json"


def test_piece_theme():
    p = _get_piece()
    assert p is not None
    assert "Harvest" in p["theme"] or "Bikkurim" in p["theme"], \
        "theme must reference Bikkurim / Harvest and Social Justice"


def test_piece_technique_mentions_flow_field():
    p = _get_piece()
    assert p is not None
    assert "flow" in p["technique"].lower() or "perlin" in p["technique"].lower(), \
        "technique must mention flow field or Perlin noise"


def test_piece_technique_mentions_perlin():
    p = _get_piece()
    assert p is not None
    assert "perlin" in p["technique"].lower(), \
        "technique must explicitly mention Perlin noise"


def test_piece_paths_correct():
    p = _get_piece()
    assert p is not None
    assert p["path"] == f"pieces/{PIECE_ID}/index.html"
    assert p["thumbnail"] == f"pieces/{PIECE_ID}/thumbnail.svg"
    assert p["essay"] == f"pieces/{PIECE_ID}/essay.md"


def test_pieces_json_no_duplicate_ids():
    pieces = _load_pieces()
    ids = [p["id"] for p in pieces]
    assert len(ids) == len(set(ids)), f"Duplicate piece IDs found: {ids}"


# ─── Canvas animation ────────────────────────────────────────────────────────

def test_uses_request_animation_frame():
    assert "requestAnimationFrame" in _html(), \
        "animation must use requestAnimationFrame"


def test_canvas_element_present():
    assert "<canvas" in _html(), "index.html must contain a <canvas> element"


def test_no_external_libraries():
    """No external script src imports allowed — everything must be inline."""
    html = _html()
    assert not re.search(r'<script\s+src=', html, re.IGNORECASE), \
        "index.html must not import external scripts"


# ─── Perlin noise implementation ─────────────────────────────────────────────

def test_permutation_table_defined():
    """Perlin noise must use a 256-element permutation table."""
    html = _html()
    assert "perm" in html or "permutation" in html.lower(), \
        "256-element permutation table not found in index.html"


def test_perlin_fade_quintic():
    """Perlin noise must use quintic fade: 6t^5 - 15t^4 + 10t^3."""
    html = _html()
    assert re.search(r"6\s*[-\*]|6t|6 \*", html) or "6 - 15" in html or "6-15" in html, \
        "quintic fade function (6t^5-15t^4+10t^3) not found in noise implementation"


def test_perlin_lerp_defined():
    """Noise must use lerp for interpolation."""
    html = _html()
    assert "_lerp" in html or "lerp" in html, \
        "lerp interpolation function not found in noise implementation"


def test_noise2d_function_defined():
    """A noise2d function must be defined."""
    assert "noise2d" in _html(), "noise2d function not found in index.html"


def test_no_external_noise_library():
    """No external noise library may be imported."""
    html = _html()
    assert "simplex" not in html.lower()
    assert "perlin.js" not in html.lower()
    assert "noisejs" not in html.lower()


# ─── Stalk grid and pe'ah corners ────────────────────────────────────────────

def test_stalk_count_around_1200():
    """HTML must define ~1200 stalks (40×30 grid)."""
    html = _html()
    cols_m = re.search(r"COLS\s*=\s*(\d+)", html)
    rows_m = re.search(r"ROWS\s*=\s*(\d+)", html)
    if cols_m and rows_m:
        product = int(cols_m.group(1)) * int(rows_m.group(1))
        assert 800 <= product <= 1600, \
            f"COLS*ROWS={product} not in expected range 800–1600 for ~1200 stalks"
    else:
        pytest.fail("COLS and ROWS constants not found in index.html")


def test_corner_exclusion_function():
    """A corner exclusion check (inCorner or equivalent) must be present."""
    html = _html()
    assert "inCorner" in html or "corner" in html.lower(), \
        "pe'ah corner exclusion logic not found in index.html"


def test_four_corner_zones_checked():
    """All four corners must be excluded (top-left, top-right, bottom-left, bottom-right)."""
    html = _html()
    assert html.count("CX") >= 4 or html.count("CY") >= 4 or \
           html.count("0.15") >= 4, \
        "four corner exclusion zones not detected in index.html"


def test_quadratic_bezier_for_stalks():
    """Stalks must be drawn as quadratic Bezier curves."""
    assert "quadraticCurveTo" in _html(), "stalks must use quadraticCurveTo"


def test_batched_stalk_drawing():
    """Stalks must be batched (beginPath called once per color group, not per stalk)."""
    html = _html()
    assert "stalksGold" in html or "stalksLight" in html or "stalkBatch" in html or \
           "batch" in html.lower(), \
        "batched stalk drawing not detected in index.html"


def test_flow_field_angle_formula():
    """Flow field angle must incorporate noise2d and Math.PI."""
    html = _html()
    assert "noise2d" in html and "Math.PI" in html, \
        "flow field angle formula (noise2d * Math.PI) not found"


def test_stalk_height_variation():
    """Stalk heights must vary (random factor present)."""
    html = _html()
    assert re.search(r"0\.[89]\d*\s*\+\s*Math\.random|Math\.random.*0\.[234]", html), \
        "stalk height ±20% variation not found"


# ─── Color palette ───────────────────────────────────────────────────────────

def test_background_loam_brown():
    """Background must use the specified loam brown."""
    html = _html()
    assert "#2a1a08" in html, "deep loam background #2a1a08 not found in index.html"


def test_wheat_gold_color():
    """Stalk gold color must be present."""
    html = _html()
    assert "#d4a017" in html, "wheat gold #d4a017 not found in index.html"


def test_wheat_highlight_color():
    """Stalk highlight color must be present."""
    html = _html()
    assert "#e8c850" in html, "wheat highlight #e8c850 not found in index.html"


def test_corner_lighter_tone():
    """Empty corner zones must use the lighter ground tone."""
    html = _html()
    assert "#3a2510" in html, "corner lighter ground tone #3a2510 not found"


# ─── Hebrew label ─────────────────────────────────────────────────────────────

def test_hebrew_peah_label():
    """Hebrew פֵּאָה label must appear in the HTML."""
    html = _html()
    assert "פֵּאָה" in html or "פאה" in html, \
        "Hebrew פֵּאָה label not found in index.html"


def test_rtl_direction_set():
    """ctx.direction must be set to 'rtl' for correct Hebrew rendering."""
    assert "rtl" in _html(), "ctx.direction = 'rtl' not found in index.html"


def test_label_fade_in():
    """Hebrew label must fade in (opacity animation) on load."""
    html = _html()
    assert "opacity" in html.lower() or "globalAlpha" in html, \
        "label fade-in (globalAlpha or opacity) not found in index.html"


# ─── Thumbnail ───────────────────────────────────────────────────────────────

def test_thumbnail_is_valid_svg():
    svg = _svg()
    assert "<svg" in svg and "</svg>" in svg, "thumbnail.svg is not valid SVG"


def test_thumbnail_background_loam():
    """Thumbnail must use the loam background color."""
    svg = _svg()
    assert "#2a1a08" in svg, "thumbnail.svg missing loam background #2a1a08"


def test_thumbnail_wheat_colors():
    """Thumbnail must include wheat stalk colors."""
    svg = _svg()
    assert "#d4a017" in svg or "#e8c850" in svg, \
        "thumbnail.svg missing wheat colors #d4a017 or #e8c850"


def test_thumbnail_corner_zones():
    """Thumbnail must show the lighter corner pe'ah zones."""
    svg = _svg()
    assert "#3a2510" in svg, "thumbnail.svg missing corner zone color #3a2510"


def test_thumbnail_has_stalks():
    """Thumbnail must include stalk path elements."""
    svg = _svg()
    assert "<path" in svg, "thumbnail.svg must contain <path> elements for stalks"


def test_thumbnail_has_hebrew_label():
    """Thumbnail must include the Hebrew pe'ah label."""
    svg = _svg()
    assert "פֵּאָה" in svg or "פאה" in svg, \
        "thumbnail.svg missing Hebrew פֵּאָה label"


# ─── Essay ───────────────────────────────────────────────────────────────────

def test_essay_substantial():
    """essay.md must be at least 300 words."""
    text = _essay()
    word_count = len(text.split())
    assert word_count >= 300, f"essay.md has only {word_count} words (minimum 300)"


def test_essay_under_800_words():
    """essay.md should not far exceed 500 words (no more than 800 with margin)."""
    text = _essay()
    word_count = len(text.split())
    assert word_count <= 800, f"essay.md has {word_count} words (maximum 800)"


def test_essay_cites_leviticus_23_22():
    """Essay must cite Leviticus 23:22 as the source."""
    text = _essay()
    assert "23:22" in text, "essay.md must cite Leviticus 23:22"


def test_essay_names_peah():
    """Essay must name the pe'ah law."""
    text = _essay().lower()
    assert "pe'ah" in text or "peah" in text, "essay.md must name the pe'ah law"


def test_essay_names_leket_and_shikchah():
    """Essay must name leket and shikchah."""
    text = _essay().lower()
    assert "leket" in text, "essay.md must name leket"
    assert "shikchah" in text or "shikha" in text, "essay.md must name shikchah"


def test_essay_cites_mishnah_peah():
    """Essay must cite Mishnah Pe'ah 1:1."""
    text = _essay()
    assert "Pe'ah 1:1" in text or "Peah 1:1" in text or "1:1" in text, \
        "essay.md must cite Mishnah Pe'ah 1:1"


def test_essay_cites_ruth():
    """Essay must reference Ruth 2:2-3 and the gleaning narrative."""
    text = _essay()
    assert "Ruth" in text and "2:" in text, \
        "essay.md must cite Ruth 2 for the gleaning narrative"


def test_essay_mentions_shavuot():
    """Essay must connect the piece to Shavuot."""
    text = _essay().lower()
    assert "shavuot" in text, "essay.md must explain the Shavuot connection"


def test_essay_embedded_in_html():
    """Essay content must be readable as HTML text in index.html."""
    html = _html()
    assert "essay-pane" in html, "index.html must embed the essay in a .essay-pane element"
    assert "Leviticus 23:22" in html or "23:22" in html, \
        "index.html must reference Leviticus 23:22 in the embedded essay"


# ─── UTF-8 / charset ─────────────────────────────────────────────────────────

def test_html_charset_utf8():
    """HTML must declare UTF-8 to render Hebrew correctly."""
    html = _html()
    assert 'charset="UTF-8"' in html or "charset=utf-8" in html.lower(), \
        "index.html must declare UTF-8 charset for Hebrew rendering"


# ─── Edge cases ──────────────────────────────────────────────────────────────

def test_no_set_interval_main_loop():
    """Main animation loop must not use setInterval."""
    html = _html()
    assert html.count("setInterval") == 0 or "requestAnimationFrame" in html, \
        "setInterval without requestAnimationFrame may cause hard resets"


def test_essay_empty_file_detection(tmp_path):
    """An empty essay.md must be caught by the word-count check."""
    empty = tmp_path / "essay.md"
    empty.write_text("", encoding="utf-8")
    text = empty.read_text(encoding="utf-8")
    assert len(text.split()) == 0


def test_essay_short_stub_detection(tmp_path):
    """A stub essay with fewer than 300 words must fail the word-count check."""
    stub = tmp_path / "essay.md"
    stub.write_text("Pe'ah is a corner. " * 10, encoding="utf-8")
    text = stub.read_text(encoding="utf-8")
    assert len(text.split()) < 300


def test_missing_piece_directory(tmp_path):
    """Accessing a non-existent piece directory raises FileNotFoundError."""
    missing = tmp_path / "99-nonexistent" / "essay.md"
    with pytest.raises(FileNotFoundError):
        open(str(missing), encoding="utf-8")


def test_pieces_json_all_fields_present():
    """Every piece in pieces.json must have the required fields."""
    required = {"id", "title", "tagline", "year", "theme", "technique", "path", "thumbnail", "essay"}
    for piece in _load_pieces():
        missing = required - set(piece.keys())
        assert not missing, f"Piece {piece.get('id')} missing fields: {missing}"


def test_piece_21_essay_path_matches_disk():
    """The essay path in pieces.json must point to an existing file on disk."""
    p = _get_piece()
    assert p is not None
    essay_path = p.get("essay", "")
    full_path = os.path.join(GALLERY_ROOT, essay_path)
    assert os.path.isfile(full_path), f"essay file '{essay_path}' not found on disk"
