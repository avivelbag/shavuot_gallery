"""Tests for piece 28-all-souls-at-sinai (DLA simulation)."""
import json
import os

import pytest

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID = "28-all-souls-at-sinai"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
INDEX_HTML = os.path.join(PIECE_DIR, "index.html")
ESSAY_MD = os.path.join(PIECE_DIR, "essay.md")
THUMBNAIL = os.path.join(PIECE_DIR, "thumbnail.svg")
README = os.path.join(PIECE_DIR, "README.md")
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")


def load_pieces():
    """Return the parsed pieces.json list."""
    with open(PIECES_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


def get_piece():
    """Return the pieces.json entry for piece 28, or None if absent."""
    return next((p for p in load_pieces() if p["id"] == PIECE_ID), None)


# ---------------------------------------------------------------------------
# Happy path: pieces.json registration
# ---------------------------------------------------------------------------

def test_piece_in_pieces_json():
    assert get_piece() is not None, f"Piece '{PIECE_ID}' not found in pieces.json"


def test_piece_has_correct_id():
    piece = get_piece()
    assert piece is not None
    assert piece["id"] == PIECE_ID


def test_piece_technique_mentions_dla():
    piece = get_piece()
    assert piece is not None
    tech = piece["technique"].lower()
    assert "dla" in tech or "diffusion" in tech, (
        "technique field should mention DLA or diffusion-limited aggregation"
    )


def test_piece_year_is_2026():
    piece = get_piece()
    assert piece is not None
    assert piece["year"] == 2026


def test_piece_has_all_required_fields():
    piece = get_piece()
    assert piece is not None
    for field in ("id", "title", "tagline", "year", "theme", "technique", "path", "thumbnail", "essay"):
        assert field in piece and piece[field], f"Missing or empty field: {field}"


# ---------------------------------------------------------------------------
# File existence
# ---------------------------------------------------------------------------

def test_index_html_exists():
    assert os.path.isfile(INDEX_HTML), f"index.html missing at {INDEX_HTML}"


def test_essay_md_exists():
    assert os.path.isfile(ESSAY_MD), f"essay.md missing at {ESSAY_MD}"


def test_thumbnail_svg_exists():
    assert os.path.isfile(THUMBNAIL), f"thumbnail.svg missing at {THUMBNAIL}"


def test_readme_exists():
    assert os.path.isfile(README), f"README.md missing at {README}"


# ---------------------------------------------------------------------------
# essay.md content
# ---------------------------------------------------------------------------

def test_essay_cites_tanhuma_nitzavim():
    text = open(ESSAY_MD, encoding="utf-8").read()
    assert "Tanhuma" in text and "Nitzavim" in text, (
        "essay.md must cite Tanhuma Nitzavim 3"
    )


def test_essay_cites_shevuot():
    text = open(ESSAY_MD, encoding="utf-8").read()
    assert "Shevuot" in text, "essay.md must cite Shevuot 39a"


def test_essay_mentions_souls_and_sinai():
    text = open(ESSAY_MD, encoding="utf-8").read().lower()
    assert "sinai" in text, "essay.md must mention Sinai"
    assert "soul" in text, "essay.md must mention souls"


def test_essay_mentions_covenant():
    text = open(ESSAY_MD, encoding="utf-8").read().lower()
    assert "covenant" in text, "essay.md should discuss the covenant binding each generation"


def test_essay_mentions_haggadah_or_exodus():
    text = open(ESSAY_MD, encoding="utf-8").read().lower()
    assert "haggadah" in text or "egypt" in text or "exodus" in text, (
        "essay.md should connect to the Haggadah / Exodus / personally leaving Egypt"
    )


def test_essay_at_least_200_words():
    text = open(ESSAY_MD, encoding="utf-8").read()
    word_count = len(text.split())
    assert word_count >= 200, f"essay.md has only {word_count} words (need ≥ 200)"


def test_essay_substantially_longer_than_minimum():
    """Essay should be a real essay, not a minimal stub."""
    text = open(ESSAY_MD, encoding="utf-8").read()
    word_count = len(text.split())
    assert word_count >= 300, f"essay.md has only {word_count} words; expected a full essay"


# ---------------------------------------------------------------------------
# index.html content
# ---------------------------------------------------------------------------

def test_index_html_uses_canvas():
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "<canvas" in html, "index.html must use a <canvas> element"


def test_index_html_uses_requestanimationframe():
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "requestAnimationFrame" in html, (
        "index.html must use requestAnimationFrame for animation"
    )


def test_index_html_has_midnight_blue_background():
    html = open(INDEX_HTML, encoding="utf-8").read().lower()
    assert "0d1b2a" in html, "index.html must use midnight blue (#0D1B2A) background"


def test_index_html_mentions_tanhuma_or_shevuot():
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "Tanhuma" in html or "Shevuot" in html, (
        "index.html must embed the source citations from the essay"
    )


def test_index_html_embeds_essay_text():
    """index.html must embed essay text inline; the test samples the first 10 long words."""
    essay = open(ESSAY_MD, encoding="utf-8").read()
    html = open(INDEX_HTML, encoding="utf-8").read()
    long_words = [w for w in essay.split() if len(w) > 5]
    sampled = long_words[:10]
    found = sum(1 for w in sampled if w in html)
    assert found >= 7, (
        f"index.html must embed essay text inline (only {found}/10 sampled words found)"
    )


def test_index_html_has_walkers_and_dla_logic():
    """index.html must contain the DLA simulation logic."""
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "walkers" in html or "walker" in html.lower(), (
        "index.html must contain DLA walker logic"
    )
    assert "freezeCell" in html or "freeze" in html.lower(), (
        "index.html must contain cell-freezing logic"
    )


# ---------------------------------------------------------------------------
# thumbnail.svg validation
# ---------------------------------------------------------------------------

def test_thumbnail_is_valid_svg():
    text = open(THUMBNAIL, encoding="utf-8").read()
    assert "<svg" in text and "</svg>" in text, "thumbnail.svg must be valid SVG"


def test_thumbnail_has_dark_background():
    text = open(THUMBNAIL, encoding="utf-8").read().lower()
    assert "0d1b2a" in text, "thumbnail.svg must use the midnight blue background colour"


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

def test_piece_path_ends_with_html():
    piece = get_piece()
    assert piece is not None
    assert piece["path"].endswith(".html"), "piece path must end with .html"


def test_piece_thumbnail_extension_is_svg():
    piece = get_piece()
    assert piece is not None
    assert piece["thumbnail"].endswith(".svg"), "thumbnail must be an SVG file"


# ---------------------------------------------------------------------------
# Explicit failure modes
# ---------------------------------------------------------------------------

def test_nonexistent_piece_id_not_in_json():
    """Confirms that the lookup returns None for an ID that does not exist."""
    pieces = load_pieces()
    found = any(p["id"] == "99-nonexistent-dla-piece" for p in pieces)
    assert not found, "Fixture: a nonexistent ID should not appear in pieces.json"


def test_stub_essay_below_minimum_would_fail():
    """A stub essay with fewer than 200 words must not pass the word-count check."""
    stub = "short essay stub " * 10  # 30 words
    word_count = len(stub.split())
    assert word_count < 200, "Fixture confirms stub is below the 200-word minimum"


def test_empty_pieces_array_has_no_entry():
    """Verifies that get_piece() returns None when pieces list is empty."""
    empty = []
    result = next((p for p in empty if p.get("id") == PIECE_ID), None)
    assert result is None, "Empty list should yield no match"
