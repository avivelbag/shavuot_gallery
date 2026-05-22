"""
Tests for piece 54-unfurling-scroll-ruth.

Verifies the piece directory, pieces.json registration, and
HTML/essay content requirements described in the acceptance criteria.
"""
import json
import os

import pytest

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID = "54-unfurling-scroll-ruth"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
INDEX_HTML = os.path.join(PIECE_DIR, "index.html")
ESSAY_MD = os.path.join(PIECE_DIR, "essay.md")
THUMBNAIL = os.path.join(PIECE_DIR, "thumbnail.svg")
README = os.path.join(PIECE_DIR, "README.md")
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")


def _load_piece():
    """Return the pieces.json entry for this piece, or None."""
    with open(PIECES_JSON, encoding="utf-8") as fh:
        pieces = json.load(fh)
    for p in pieces:
        if p["id"] == PIECE_ID:
            return p
    return None


# ── Happy path ────────────────────────────────────────────────────────────────

def test_piece_directory_exists():
    assert os.path.isdir(PIECE_DIR), f"Piece directory {PIECE_DIR} does not exist"


def test_index_html_exists():
    assert os.path.isfile(INDEX_HTML), "index.html missing from piece directory"


def test_essay_md_exists():
    assert os.path.isfile(ESSAY_MD), "essay.md missing from piece directory"


def test_thumbnail_svg_exists():
    assert os.path.isfile(THUMBNAIL), "thumbnail.svg missing from piece directory"


def test_readme_exists():
    assert os.path.isfile(README), "README.md missing from piece directory"


def test_pieces_json_has_entry():
    piece = _load_piece()
    assert piece is not None, f"No entry for '{PIECE_ID}' in pieces.json"


def test_pieces_json_theme_is_book_of_ruth():
    piece = _load_piece()
    assert piece is not None
    assert "Ruth" in piece["theme"], (
        f"Expected theme to mention 'Ruth', got: {piece['theme']!r}"
    )


def test_pieces_json_technique_mentions_canvas():
    piece = _load_piece()
    assert piece is not None
    tech = piece["technique"].lower()
    assert "canvas" in tech, (
        f"Expected technique to mention 'canvas', got: {piece['technique']!r}"
    )


def test_pieces_json_technique_mentions_stroke_animation():
    piece = _load_piece()
    assert piece is not None
    tech = piece["technique"].lower()
    assert "stroke" in tech or "calligraph" in tech, (
        f"Expected technique to mention stroke animation or calligraphy, got: {piece['technique']!r}"
    )


# ── index.html content ────────────────────────────────────────────────────────

def test_index_html_uses_requestanimationframe():
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "requestAnimationFrame" in html, (
        "index.html must use requestAnimationFrame for animation"
    )


def test_index_html_has_canvas_element():
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "<canvas" in html, "index.html must contain a <canvas> element"


def test_index_html_uses_bezier_curves():
    """The piece must use bezierCurveTo for calligraphic stroke rendering."""
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "bezierCurveTo" in html, (
        "index.html must use bezierCurveTo for Hebrew letter stroke animation"
    )


def test_index_html_uses_parchment_color():
    """The parchment cream color #FFF8DC must be present."""
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "FFF8DC" in html, "index.html must use parchment cream color #FFF8DC"


def test_index_html_uses_ink_color():
    """The ink near-black color #1A0A00 must be present."""
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "1A0A00" in html, "index.html must use ink near-black color #1A0A00"


def test_index_html_uses_rod_brown():
    """The wooden rod color #8B5E3C must be present."""
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "8B5E3C" in html, "index.html must use wooden rod color #8B5E3C"


def test_index_html_uses_gold():
    """The scroll shadow gold #C9A84C must be present for the breathing glow."""
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "C9A84C" in html, "index.html must use deep gold color #C9A84C for glow"


def test_index_html_has_hebrew_verse():
    """The Hebrew text of Ruth 1:16 must appear in the HTML."""
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "עַמֵּךְ" in html or "עמך" in html, (
        "index.html must contain the Hebrew text of Ruth 1:16"
    )


def test_index_html_embeds_essay_text():
    """index.html must embed essay content inline — not rely on a runtime fetch."""
    essay = open(ESSAY_MD, encoding="utf-8").read()
    html = open(INDEX_HTML, encoding="utf-8").read()
    words = [w for w in essay.split() if len(w) > 6][:10]
    found = sum(1 for w in words if w in html)
    assert found >= 5, (
        f"index.html appears not to embed essay text (only {found}/10 sampled words found)"
    )


def test_index_html_has_radial_gradient():
    """Rods must be rendered with radial gradients."""
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "createRadialGradient" in html, (
        "index.html must use createRadialGradient for the wooden rod look"
    )


def test_index_html_has_shadow_blur():
    """Breathing animation must use shadowBlur."""
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "shadowBlur" in html, (
        "index.html must use shadowBlur for the post-reveal breathing glow"
    )


# ── essay.md content ──────────────────────────────────────────────────────────

def test_essay_has_minimum_word_count():
    text = open(ESSAY_MD, encoding="utf-8").read()
    word_count = len(text.split())
    assert word_count >= 200, (
        f"essay.md has only {word_count} words (minimum 200)"
    )


def test_essay_cites_ruth_1_16():
    text = open(ESSAY_MD, encoding="utf-8").read()
    assert "1:16" in text, "essay.md must cite Ruth 1:16"


def test_essay_mentions_shavuot():
    text = open(ESSAY_MD, encoding="utf-8").read().lower()
    assert "shavuot" in text, "essay.md must mention Shavuot"


def test_essay_mentions_megillah_or_scroll():
    text = open(ESSAY_MD, encoding="utf-8").read().lower()
    assert "megillah" in text or "scroll" in text, (
        "essay.md must mention the megillah or scroll form"
    )


def test_essay_mentions_soloveitchik_or_sinai():
    text = open(ESSAY_MD, encoding="utf-8").read()
    assert "Soloveitchik" in text or "Sinai" in text, (
        "essay.md must mention Soloveitchik or the Sinai covenant parallel"
    )


def test_essay_mentions_talmud_yerushalmi():
    text = open(ESSAY_MD, encoding="utf-8").read()
    assert "Yerushalmi" in text or "Talmud" in text, (
        "essay.md must cite the Talmud Yerushalmi custom of reading Ruth on Shavuot"
    )


# ── thumbnail.svg ─────────────────────────────────────────────────────────────

def test_thumbnail_is_valid_svg():
    text = open(THUMBNAIL, encoding="utf-8").read()
    assert "<svg" in text and "</svg>" in text, (
        "thumbnail.svg does not look like valid SVG"
    )


def test_thumbnail_contains_scroll_elements():
    """Thumbnail should depict a scroll — rectangles for rods and parchment."""
    text = open(THUMBNAIL, encoding="utf-8").read()
    assert "<rect" in text, (
        "thumbnail.svg should contain <rect> elements for the scroll rods/parchment"
    )


# ── Edge cases ────────────────────────────────────────────────────────────────

def test_pieces_json_no_duplicate_ids():
    """Adding this piece must not introduce a duplicate ID."""
    with open(PIECES_JSON, encoding="utf-8") as fh:
        pieces = json.load(fh)
    ids = [p["id"] for p in pieces]
    assert len(ids) == len(set(ids)), f"Duplicate IDs after adding piece: {PIECE_ID}"


def test_index_html_has_no_external_font_link():
    """The piece must have no external font dependency (no @import or <link> for fonts)."""
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "fonts.googleapis" not in html, (
        "index.html must not load fonts from Google Fonts — glyphs are pre-computed bezier paths"
    )


def test_essay_mentions_harvest():
    """Essay must connect Ruth's story to the harvest / agricultural context."""
    text = open(ESSAY_MD, encoding="utf-8").read().lower()
    assert "harvest" in text or "barley" in text or "wheat" in text, (
        "essay.md must mention the harvest context of Ruth and Shavuot"
    )
