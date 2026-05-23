"""
Tests specific to piece 95-quantum-walk-forty-nine-gates.

Covers: happy path (all required files present, pieces.json registration),
essay content requirements (Hebrew text, Talmud citation, word count),
HTML requirements (canvas, requestAnimationFrame, absorbing boundary mention,
Grover coin mention), thumbnail SVG validity, and edge/failure cases.
"""
import json
import os

import pytest

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID = "95-quantum-walk-forty-nine-gates"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")


def _load_piece():
    with open(PIECES_JSON, encoding="utf-8") as f:
        pieces = json.load(f)
    for p in pieces:
        if p["id"] == PIECE_ID:
            return p
    return None


def _read(rel):
    return open(os.path.join(GALLERY_ROOT, rel), encoding="utf-8").read()


# ---------------------------------------------------------------------------
# Happy path — registration and file layout
# ---------------------------------------------------------------------------

def test_piece_registered_in_pieces_json():
    """Piece must appear in pieces.json with the correct id."""
    piece = _load_piece()
    assert piece is not None, f"'{PIECE_ID}' not found in pieces.json"


def test_piece_has_all_required_fields():
    """All nine required fields must be present and non-empty."""
    required = ("id", "title", "tagline", "year", "theme", "technique", "path", "thumbnail", "essay")
    piece = _load_piece()
    assert piece is not None
    for field in required:
        assert field in piece and piece[field], f"Field '{field}' missing or empty"


def test_piece_theme_and_technique():
    """Theme and technique must match the acceptance criteria."""
    piece = _load_piece()
    assert piece is not None
    assert "49 gates" in piece["theme"].lower() or "sefirat" in piece["theme"].lower(), \
        f"Unexpected theme: {piece['theme']!r}"
    assert "quantum walk" in piece["technique"].lower(), \
        f"Unexpected technique: {piece['technique']!r}"


def test_index_html_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "index.html")), "index.html missing"


def test_essay_md_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "essay.md")), "essay.md missing"


def test_thumbnail_svg_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "thumbnail.svg")), "thumbnail.svg missing"


def test_readme_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "README.md")), "README.md missing"


# ---------------------------------------------------------------------------
# Essay content requirements
# ---------------------------------------------------------------------------

def test_essay_word_count():
    """essay.md must have at least 200 words."""
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    wc = len(text.split())
    assert wc >= 200, f"essay.md has only {wc} words"


def test_essay_has_talmud_rosh_hashanah_reference():
    """Essay must cite Rosh Hashanah 21b — the fifty gates teaching."""
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    assert "Rosh Hashanah" in text or "21b" in text, \
        "essay.md must cite Talmud Rosh Hashanah 21b"


def test_essay_has_leviticus_reference():
    """Essay must cite Leviticus 23 on the Omer count."""
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    assert "Leviticus" in text or "23:15" in text, \
        "essay.md must cite Leviticus 23:15–16 on counting the Omer"


def test_essay_has_hebrew_text():
    """Essay must contain Hebrew characters (bilingual block requirement)."""
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    has_hebrew = any('א' <= ch <= 'ת' for ch in text)
    assert has_hebrew, "essay.md must contain Hebrew text"


def test_essay_mentions_quantum_walk():
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read().lower()
    assert "quantum walk" in text, "essay.md must explain the quantum walk"


def test_essay_mentions_absorbing_boundary():
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read().lower()
    assert "absorb" in text or "boundary" in text or "drain" in text, \
        "essay.md must describe the absorbing boundary at the 50th gate"


# ---------------------------------------------------------------------------
# HTML requirements
# ---------------------------------------------------------------------------

def test_html_has_canvas():
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "<canvas" in html, "index.html must contain a <canvas> element"


def test_html_uses_request_animation_frame():
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "requestAnimationFrame" in html, "index.html must use requestAnimationFrame"


def test_html_has_float64array():
    """State arrays must be Float64Array as specified."""
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "Float64Array" in html, "index.html must use Float64Array for quantum state"


def test_html_has_grover_coin():
    """Grover coin implementation must be present."""
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read().lower()
    assert "grover" in html or "0.5" in html, \
        "index.html must implement the Grover coin"


def test_html_has_absorbing_boundary_code():
    """The absorbing boundary at (48,48) must be implemented in JS."""
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "48, 48" in html or "(48,48)" in html or "idx(48" in html, \
        "index.html must zero out amplitude at position (48,48)"


def test_html_has_hebrew_text():
    """index.html must contain Hebrew characters (embedded essay requirement)."""
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    has_hebrew = any('א' <= ch <= 'ת' for ch in html)
    assert has_hebrew, "index.html must embed Hebrew text"


def test_html_has_shavuot_label():
    """The Shavuot end-of-cycle label must be in the HTML."""
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "שבועות" in html, "index.html must display 'שבועות' at cycle end"


def test_html_embeds_essay_words():
    """index.html must embed substantive words from essay.md."""
    essay = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    long_words = [w for w in essay.split() if len(w) > 5][:10]
    found = sum(1 for w in long_words if w in html)
    assert found >= 5, \
        f"index.html embeds only {found}/10 sampled essay words; essay not embedded"


def test_html_has_bilingual_talmud_block():
    """index.html must contain the Hebrew Talmud passage."""
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "שַׁעֲרֵי בִינָה" in html or "חֲמִשִּׁים" in html, \
        "index.html must contain the Hebrew text of Rosh Hashanah 21b"


def test_html_mentions_forty_nine_grid():
    """index.html must reference the 49×49 grid dimension."""
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "49" in html, "index.html must reference the 49×49 grid"


# ---------------------------------------------------------------------------
# Thumbnail
# ---------------------------------------------------------------------------

def test_thumbnail_is_valid_svg():
    text = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert "<svg" in text and "</svg>" in text, "thumbnail.svg is not valid SVG"


def test_thumbnail_has_correct_dimensions():
    text = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert 'width="400"' in text and 'height="400"' in text, \
        "thumbnail.svg must be 400×400"


def test_thumbnail_has_caption():
    """Thumbnail must have the Hebrew caption שערי בינה."""
    text = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert "שַׁעֲרֵי בִינָה" in text or "שערי" in text, \
        "thumbnail.svg must contain the Hebrew caption שערי בינה"


def test_thumbnail_has_fiftieth_gate_cell():
    """Thumbnail must have the white-bordered 50th gate cell."""
    text = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert "50" in text or 'stroke="white"' in text, \
        "thumbnail.svg must mark the 50th gate cell"


# ---------------------------------------------------------------------------
# Edge cases and failure modes
# ---------------------------------------------------------------------------

def test_piece_year_is_integer():
    piece = _load_piece()
    assert piece is not None
    assert isinstance(piece["year"], int), f"year must be int, got {type(piece['year'])}"


def test_piece_path_ends_with_html():
    piece = _load_piece()
    assert piece is not None
    assert piece["path"].endswith(".html"), "path must end with .html"


def test_no_duplicate_id():
    """Our new piece id must not duplicate any existing entry."""
    with open(PIECES_JSON, encoding="utf-8") as f:
        pieces = json.load(f)
    ids = [p["id"] for p in pieces]
    assert ids.count(PIECE_ID) == 1, f"Duplicate id '{PIECE_ID}' in pieces.json"


def test_readme_mentions_shavuot_theme():
    """README must mention the quantum walk or the 50th gate theme."""
    text = open(os.path.join(PIECE_DIR, "README.md"), encoding="utf-8").read().lower()
    assert "quantum walk" in text or "fiftieth gate" in text or "50" in text, \
        "README.md must mention the quantum walk or 50th gate"


def test_missing_piece_returns_none():
    """Helper _load_piece must return None for a nonexistent id."""
    with open(PIECES_JSON, encoding="utf-8") as f:
        pieces = json.load(f)
    result = next((p for p in pieces if p["id"] == "99-nonexistent-piece"), None)
    assert result is None
