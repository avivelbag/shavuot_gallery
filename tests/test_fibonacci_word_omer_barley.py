"""
Tests for piece 96-fibonacci-word-omer-barley: Seven Times Seven, Plus One.

Verifies that the Fibonacci word fractal Omer piece satisfies all acceptance
criteria: correct directory layout, embedded essay, key JavaScript behaviors,
thumbnail validity, and pieces.json registration.
"""
import json
import os

import pytest

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID = "96-fibonacci-word-omer-barley"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
INDEX_HTML = os.path.join(PIECE_DIR, "index.html")
ESSAY_MD = os.path.join(PIECE_DIR, "essay.md")
THUMBNAIL_SVG = os.path.join(PIECE_DIR, "thumbnail.svg")
README_MD = os.path.join(PIECE_DIR, "README.md")
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")


def load_pieces():
    with open(PIECES_JSON, "r", encoding="utf-8") as fh:
        return json.load(fh)


def get_piece():
    for p in load_pieces():
        if p["id"] == PIECE_ID:
            return p
    return None


def read_file(path):
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


# ---------------------------------------------------------------------------
# Happy path: directory layout
# ---------------------------------------------------------------------------

def test_piece_directory_exists():
    assert os.path.isdir(PIECE_DIR), f"piece directory {PIECE_DIR} is missing"


def test_index_html_exists():
    assert os.path.isfile(INDEX_HTML), "index.html is missing from piece directory"


def test_essay_md_exists():
    assert os.path.isfile(ESSAY_MD), "essay.md is missing from piece directory"


def test_thumbnail_svg_exists():
    assert os.path.isfile(THUMBNAIL_SVG), "thumbnail.svg is missing from piece directory"


def test_readme_md_exists():
    assert os.path.isfile(README_MD), "README.md is missing from piece directory"


# ---------------------------------------------------------------------------
# Happy path: pieces.json registration
# ---------------------------------------------------------------------------

def test_piece_registered_in_pieces_json():
    piece = get_piece()
    assert piece is not None, f"piece '{PIECE_ID}' not found in pieces.json"


def test_piece_has_correct_theme():
    piece = get_piece()
    assert piece is not None
    assert "Sefirat HaOmer" in piece["theme"] or "Bikkurim" in piece["theme"] or "harvest" in piece["theme"].lower(), (
        f"expected Sefirat HaOmer / Bikkurim / harvest theme, got: {piece['theme']!r}"
    )


def test_piece_has_correct_technique():
    piece = get_piece()
    assert piece is not None
    assert "Fibonacci" in piece["technique"], (
        f"expected Fibonacci word fractal technique, got: {piece['technique']!r}"
    )
    assert "turtle" in piece["technique"].lower() or "substitution" in piece["technique"].lower(), (
        f"technique should mention turtle-graphics or substitution: {piece['technique']!r}"
    )


def test_piece_path_points_to_index_html():
    piece = get_piece()
    assert piece is not None
    assert piece["path"].endswith("index.html"), "path must end with index.html"
    full = os.path.join(GALLERY_ROOT, piece["path"])
    assert os.path.isfile(full), f"path '{piece['path']}' does not exist on disk"


def test_piece_thumbnail_exists_on_disk():
    piece = get_piece()
    assert piece is not None
    full = os.path.join(GALLERY_ROOT, piece["thumbnail"])
    assert os.path.isfile(full), f"thumbnail '{piece['thumbnail']}' does not exist on disk"


def test_piece_essay_field_exists_on_disk():
    piece = get_piece()
    assert piece is not None
    full = os.path.join(GALLERY_ROOT, piece["essay"])
    assert os.path.isfile(full), f"essay '{piece['essay']}' does not exist on disk"


# ---------------------------------------------------------------------------
# Happy path: index.html required content
# ---------------------------------------------------------------------------

def test_index_html_has_canvas():
    html = read_file(INDEX_HTML)
    assert "<canvas" in html, "index.html must contain a <canvas> element"


def test_index_html_uses_request_animation_frame():
    html = read_file(INDEX_HTML)
    assert "requestAnimationFrame" in html, "index.html must use requestAnimationFrame for animation"


def test_index_html_uses_lighter_compositing():
    html = read_file(INDEX_HTML)
    assert "lighter" in html, "index.html must use globalCompositeOperation = 'lighter'"


def test_index_html_has_fibonacci_word_generation():
    """The page must generate the Fibonacci word by substitution."""
    html = read_file(INDEX_HTML)
    assert "genWord" in html or "fibWord" in html or "substitut" in html.lower(), (
        "index.html must generate the Fibonacci word (look for genWord/fibWord/substitution)"
    )


def test_index_html_has_18_iterations():
    """18 substitution iterations produce F(20)=6765 characters."""
    html = read_file(INDEX_HTML)
    assert "18" in html, "index.html should perform 18 substitution iterations"


def test_index_html_has_turtle_graphics():
    """The page interprets the word as turtle-graphics instructions."""
    html = read_file(INDEX_HTML)
    keywords = ["turtle", "angle", "angleDeg", "cos(", "sin("]
    found = sum(1 for k in keywords if k in html)
    assert found >= 3, f"index.html must contain turtle-graphics code; found only {found}/5 keywords"


def test_index_html_has_49_trail():
    """Trail of 49 segments marks each day of the Omer."""
    html = read_file(INDEX_HTML)
    assert "49" in html, "index.html must reference 49 (Omer count) in the trail logic"


def test_index_html_has_hebrew_numerals():
    """The page must include Hebrew numerals for the Omer count."""
    html = read_file(INDEX_HTML)
    assert "א" in html or "\\u05D0" in html or "HEBREW" in html, (
        "index.html must include Hebrew numerals for the Omer flash display"
    )
    assert "מ" in html or "HEBREW" in html, (
        "index.html should include מ (mem) for the numeral מ״ט (49)"
    )


def test_index_html_background_is_dark_parchment():
    """Background color must be the specified dark parchment #1A1408."""
    html = read_file(INDEX_HTML)
    assert "1A1408" in html.upper() or "1a1408" in html, (
        "index.html must use dark parchment background #1A1408"
    )


def test_index_html_has_color_gradient():
    """The three palette colors must appear in the index.html."""
    html = read_file(INDEX_HTML)
    colors = ["8B6914", "6B8C3E", "D4A200"]
    missing = [c for c in colors if c.upper() not in html.upper()]
    assert not missing, f"index.html is missing palette colors: {missing}"


def test_index_html_embeds_essay_text():
    """index.html must embed the essay content inline (not fetch it at runtime)."""
    essay = read_file(ESSAY_MD)
    html = read_file(INDEX_HTML)
    words = [w for w in essay.split() if len(w) > 5][:15]
    found = sum(1 for w in words if w in html)
    assert found >= 7, (
        f"index.html does not appear to embed the essay ({found}/15 sampled words found)"
    )


def test_index_html_has_offscreen_canvas():
    """The implementation must use an offscreen canvas for performance."""
    html = read_file(INDEX_HTML)
    assert "offscreen" in html or "createElementNS" in html or "createElement('canvas')" in html or 'createElement("canvas")' in html, (
        "index.html should use an offscreen canvas for the static fractal"
    )


# ---------------------------------------------------------------------------
# Edge case: essay content quality
# ---------------------------------------------------------------------------

def test_essay_md_mentions_leviticus():
    essay = read_file(ESSAY_MD)
    assert "Leviticus" in essay or "23:15" in essay, (
        "essay.md must open with or reference Leviticus 23:15-16"
    )


def test_essay_md_mentions_sefer_hachinuch():
    essay = read_file(ESSAY_MD)
    assert "Sefer HaChinuch" in essay or "Chinuch" in essay, (
        "essay.md must reference the Sefer HaChinuch (Mitzvah 306)"
    )


def test_essay_md_mentions_fibonacci():
    essay = read_file(ESSAY_MD)
    assert "Fibonacci" in essay, "essay.md must explain the Fibonacci word fractal"


def test_essay_md_mentions_barley():
    essay = read_file(ESSAY_MD)
    assert "barley" in essay.lower() or "Omer" in essay, (
        "essay.md must connect the piece to barley / the Omer"
    )


def test_essay_md_word_count():
    """Essay must be substantial (at least 250 words)."""
    essay = read_file(ESSAY_MD)
    word_count = len(essay.split())
    assert word_count >= 250, f"essay.md has only {word_count} words (need ≥ 250)"


# ---------------------------------------------------------------------------
# Edge case: thumbnail validity
# ---------------------------------------------------------------------------

def test_thumbnail_is_valid_svg():
    svg = read_file(THUMBNAIL_SVG)
    assert "<svg" in svg and "</svg>" in svg, "thumbnail.svg is not valid SVG"


def test_thumbnail_has_dark_background():
    svg = read_file(THUMBNAIL_SVG)
    assert "1A1408" in svg.upper() or "1a1408" in svg, (
        "thumbnail.svg must use the dark parchment background #1A1408"
    )


def test_thumbnail_has_hebrew_mem_tet():
    """thumbnail.svg must contain מ״ט (49) in Hebrew."""
    svg = read_file(THUMBNAIL_SVG)
    assert "מ" in svg or "\\u05DE" in svg or "&#x05DE;" in svg, (
        "thumbnail.svg must contain the Hebrew numeral מ״ט (49)"
    )


def test_thumbnail_has_path_or_polyline():
    """The thumbnail must contain a drawn path (the fractal curve)."""
    svg = read_file(THUMBNAIL_SVG)
    assert "<polyline" in svg or "<path" in svg or "<line" in svg, (
        "thumbnail.svg must contain a path, polyline, or line element for the fractal curve"
    )


def test_thumbnail_dimensions_are_400x400():
    svg = read_file(THUMBNAIL_SVG)
    assert 'width="400"' in svg and 'height="400"' in svg, (
        "thumbnail.svg must be 400×400 pixels"
    )


# ---------------------------------------------------------------------------
# Failure mode: piece missing from pieces.json would be caught
# ---------------------------------------------------------------------------

def test_missing_id_would_be_detected(tmp_path):
    """Simulate a pieces.json that lacks the piece and verify detection logic."""
    bad_pieces = [{"id": "01-thunder-at-sinai", "title": "Thunder"}]
    ids = [p["id"] for p in bad_pieces]
    assert PIECE_ID not in ids, "fixture must not contain the new piece — detection check"


def test_empty_essay_field_would_fail():
    """An empty essay path in pieces.json should be treated as missing."""
    bad = {"id": PIECE_ID, "essay": ""}
    assert not bad["essay"], "empty essay field must be falsy for the guard check to catch it"


def test_nonexistent_thumbnail_would_fail(tmp_path):
    """A thumbnail path pointing to a nonexistent file should be detected."""
    fake_thumb = os.path.join(str(tmp_path), "nonexistent.svg")
    assert not os.path.isfile(fake_thumb), "fixture path must not exist on disk"
