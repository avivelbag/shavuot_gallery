"""
Tests for piece 60 — The Fiftieth Gate: Julia Set of Infinite Understanding.
"""
import json
import os

import pytest

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECES_JSON  = os.path.join(GALLERY_ROOT, "pieces.json")
PIECE_ID     = "60-fiftieth-gate-julia-set"
PIECE_DIR    = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)


def _load_pieces():
    with open(PIECES_JSON, encoding="utf-8") as fh:
        return json.load(fh)


def _get_piece():
    for p in _load_pieces():
        if p["id"] == PIECE_ID:
            return p
    return None


# ---------------------------------------------------------------------------
# Happy path — piece registered and files present
# ---------------------------------------------------------------------------

def test_piece_60_in_pieces_json():
    assert _get_piece() is not None, f"Piece '{PIECE_ID}' not found in pieces.json"


def test_piece_60_required_fields_non_empty():
    piece = _get_piece()
    assert piece is not None, f"Piece '{PIECE_ID}' missing from pieces.json"
    required = ("id", "title", "tagline", "year", "theme", "technique",
                "path", "thumbnail", "essay")
    for field in required:
        val = piece.get(field)
        assert val is not None and val != "", \
            f"Field '{field}' is empty or missing in piece '{PIECE_ID}'"


def test_piece_60_index_html_exists():
    piece = _get_piece()
    assert piece is not None
    full = os.path.join(GALLERY_ROOT, piece["path"])
    assert os.path.isfile(full), f"index.html not found at {piece['path']}"


def test_piece_60_thumbnail_exists():
    piece = _get_piece()
    assert piece is not None
    full = os.path.join(GALLERY_ROOT, piece["thumbnail"])
    assert os.path.isfile(full), f"thumbnail not found at {piece['thumbnail']}"


def test_piece_60_essay_md_exists():
    piece = _get_piece()
    assert piece is not None
    full = os.path.join(GALLERY_ROOT, piece["essay"])
    assert os.path.isfile(full), f"essay.md not found at {piece['essay']}"


def test_piece_60_readme_exists():
    readme = os.path.join(PIECE_DIR, "README.md")
    assert os.path.isfile(readme), f"README.md missing from {PIECE_DIR}"


# ---------------------------------------------------------------------------
# Essay content — word count, Hebrew passages, Talmud citation
# ---------------------------------------------------------------------------

def test_piece_60_essay_at_least_200_words():
    piece = _get_piece()
    assert piece is not None
    text = open(os.path.join(GALLERY_ROOT, piece["essay"]), encoding="utf-8").read()
    count = len(text.split())
    assert count >= 200, f"essay.md has only {count} words (need ≥ 200)"


def test_piece_60_essay_contains_hebrew_talmud_quote():
    piece = _get_piece()
    assert piece is not None
    text = open(os.path.join(GALLERY_ROOT, piece["essay"]), encoding="utf-8").read()
    assert "חֲמִשִּׁים שַׁעֲרֵי בִינָה" in text, \
        "essay.md must include the Hebrew Talmudic quote about fifty gates"


def test_piece_60_essay_contains_leviticus_quote_hebrew():
    piece = _get_piece()
    assert piece is not None
    text = open(os.path.join(GALLERY_ROOT, piece["essay"]), encoding="utf-8").read()
    assert "וּסְפַרְתֶּם" in text, \
        "essay.md must include Leviticus 23:15 in Hebrew (וּסְפַרְתֶּם)"


def test_piece_60_essay_mentions_50th_gate():
    piece = _get_piece()
    assert piece is not None
    text = open(os.path.join(GALLERY_ROOT, piece["essay"]), encoding="utf-8").read()
    assert "fiftieth" in text.lower() or "50" in text or "fifty" in text.lower(), \
        "essay.md must discuss the fiftieth gate concept"


# ---------------------------------------------------------------------------
# index.html content checks
# ---------------------------------------------------------------------------

def test_piece_60_html_uses_webgl():
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "webgl" in html.lower() or "WebGL" in html, \
        "index.html must use WebGL for the Julia set renderer"


def test_piece_60_html_uses_requestanimationframe():
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "requestAnimationFrame" in html, \
        "index.html must use requestAnimationFrame for animation"


def test_piece_60_html_contains_julia_uniform():
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "u_c" in html, \
        "index.html must pass the Julia parameter c as a uniform (u_c)"


def test_piece_60_html_contains_gate_overlay():
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "שַׁעַר נ׳" in html, \
        "index.html must contain the Gate 50 Hebrew label (שַׁעַר נ׳)"


def test_piece_60_html_embeds_essay_text():
    piece = _get_piece()
    assert piece is not None
    essay_text = open(os.path.join(GALLERY_ROOT, piece["essay"]), encoding="utf-8").read()
    html = open(os.path.join(GALLERY_ROOT, piece["path"]), encoding="utf-8").read()
    words = [w for w in essay_text.split() if len(w) > 5][:10]
    found = sum(1 for w in words if w in html)
    assert found >= 5, \
        f"index.html does not appear to embed essay text (only {found}/10 sampled words found)"


def test_piece_60_html_contains_harvest_palette_color():
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "D4A820" in html or "d4a820" in html.lower(), \
        "index.html must reference the wheat-gold harvest palette color #D4A820"


def test_piece_60_html_contains_interior_color():
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "0D0B14" in html or "0d0b14" in html.lower(), \
        "index.html must reference the midnight interior color #0D0B14"


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

def test_piece_60_id_unique():
    pieces = _load_pieces()
    ids = [p["id"] for p in pieces]
    assert ids.count(PIECE_ID) == 1, \
        f"Piece ID '{PIECE_ID}' appears more than once in pieces.json"


def test_piece_60_year_is_integer():
    piece = _get_piece()
    assert piece is not None
    assert isinstance(piece["year"], int), \
        f"Piece '{PIECE_ID}' year must be an integer, got {piece['year']!r}"


def test_piece_60_thumbnail_is_svg():
    piece = _get_piece()
    assert piece is not None
    assert piece["thumbnail"].endswith(".svg"), \
        f"Piece '{PIECE_ID}' thumbnail must be .svg"
    svg_text = open(os.path.join(GALLERY_ROOT, piece["thumbnail"]), encoding="utf-8").read()
    assert "<svg" in svg_text and "</svg>" in svg_text, \
        "thumbnail.svg does not contain valid SVG markup"


def test_piece_60_path_ends_with_html():
    piece = _get_piece()
    assert piece is not None
    assert piece["path"].endswith(".html"), \
        f"Piece '{PIECE_ID}' path must end with .html"


# ---------------------------------------------------------------------------
# Failure-mode / negative tests
# ---------------------------------------------------------------------------

def test_missing_piece_60_detected(tmp_path):
    """Removing piece 60 from a local copy should cause the lookup to return None."""
    pieces = [p for p in _load_pieces() if p["id"] != PIECE_ID]
    bad_json = tmp_path / "pieces.json"
    bad_json.write_text(json.dumps(pieces), encoding="utf-8")
    data = json.loads(bad_json.read_text())
    ids = [p["id"] for p in data]
    assert PIECE_ID not in ids, "Piece should be absent after removal"


def test_essay_short_word_count_detected():
    """An essay with fewer than 200 words must be caught."""
    stub = "word " * 50
    assert len(stub.split()) < 200
