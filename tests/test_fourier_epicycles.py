"""
Tests for piece 29 — The Fiftieth Day (Fourier Epicycle Hebrew Calligraphy).

Verifies the piece directory layout, pieces.json entry, essay content,
and HTML structure for the Fourier epicycle animation.
"""
import json
import os
import re

import pytest

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")
PIECE_ID = "29-fiftieth-day-epicycles"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)


def load_pieces():
    """Load pieces.json and return the list."""
    with open(PIECES_JSON, "r", encoding="utf-8") as fh:
        return json.load(fh)


def get_piece():
    """Return the pieces.json entry for piece 29, or None."""
    for p in load_pieces():
        if p["id"] == PIECE_ID:
            return p
    return None


# ---------------------------------------------------------------------------
# pieces.json registration
# ---------------------------------------------------------------------------

def test_piece_29_in_json():
    """Piece 29 must be registered in pieces.json."""
    assert get_piece() is not None, f"Piece '{PIECE_ID}' not found in pieces.json"


def test_piece_29_required_fields():
    """All required fields must be present and non-empty."""
    required = ("id", "title", "tagline", "year", "theme", "technique", "path", "thumbnail", "essay")
    piece = get_piece()
    assert piece is not None
    for field in required:
        val = piece.get(field)
        assert val is not None and val != "", (
            f"Piece '{PIECE_ID}' is missing required field '{field}'"
        )


def test_piece_29_year_integer():
    piece = get_piece()
    assert piece is not None
    assert isinstance(piece["year"], int), "year must be an integer"


def test_piece_29_path_ends_html():
    piece = get_piece()
    assert piece is not None
    assert piece["path"].endswith(".html"), "path must end with .html"


def test_piece_29_id_matches_directory():
    """The id field must match the directory component of the path."""
    piece = get_piece()
    assert piece is not None
    parts = piece["path"].replace("\\", "/").split("/")
    assert parts[-2] == PIECE_ID, (
        f"Directory '{parts[-2]}' does not match id '{PIECE_ID}'"
    )


def test_no_duplicate_ids():
    """Adding piece 29 must not introduce a duplicate ID."""
    pieces = load_pieces()
    ids = [p["id"] for p in pieces]
    assert len(ids) == len(set(ids)), f"Duplicate IDs in pieces.json: {ids}"


# ---------------------------------------------------------------------------
# File layout
# ---------------------------------------------------------------------------

def test_piece_29_directory_exists():
    assert os.path.isdir(PIECE_DIR), f"Piece directory missing: {PIECE_DIR}"


def test_piece_29_index_html_exists():
    html_path = os.path.join(PIECE_DIR, "index.html")
    assert os.path.isfile(html_path), "index.html missing from piece 29 directory"


def test_piece_29_essay_md_exists():
    essay_path = os.path.join(PIECE_DIR, "essay.md")
    assert os.path.isfile(essay_path), "essay.md missing from piece 29 directory"


def test_piece_29_readme_exists():
    readme = os.path.join(PIECE_DIR, "README.md")
    assert os.path.isfile(readme), "README.md missing from piece 29 directory"


def test_piece_29_thumbnail_exists():
    piece = get_piece()
    assert piece is not None
    thumb = os.path.join(GALLERY_ROOT, piece["thumbnail"])
    assert os.path.isfile(thumb), f"Thumbnail missing: {piece['thumbnail']}"


def test_piece_29_thumbnail_is_svg():
    piece = get_piece()
    assert piece is not None
    ext = os.path.splitext(piece["thumbnail"])[1].lower()
    assert ext == ".svg", "Thumbnail must be an SVG file"
    thumb_path = os.path.join(GALLERY_ROOT, piece["thumbnail"])
    content = open(thumb_path, encoding="utf-8").read()
    assert "<svg" in content and "</svg>" in content, "thumbnail.svg is not valid SVG"


# ---------------------------------------------------------------------------
# Essay content
# ---------------------------------------------------------------------------

def test_piece_29_essay_min_words():
    """Essay must be at least 200 words."""
    essay_path = os.path.join(PIECE_DIR, "essay.md")
    text = open(essay_path, encoding="utf-8").read()
    word_count = len(text.split())
    assert word_count >= 200, (
        f"essay.md has only {word_count} words (minimum 200)"
    )


def test_piece_29_essay_mentions_leviticus():
    """Essay must cite Leviticus 23 as the source for the fifty-day count."""
    essay_path = os.path.join(PIECE_DIR, "essay.md")
    text = open(essay_path, encoding="utf-8").read()
    assert "Leviticus 23" in text or "Lev. 23" in text or "ויקרא" in text, (
        "essay.md must mention Leviticus 23 as the source for the count"
    )


def test_piece_29_essay_mentions_seven():
    """Essay must discuss the derivation from sheva (seven) / weeks."""
    essay_path = os.path.join(PIECE_DIR, "essay.md")
    text = open(essay_path, encoding="utf-8").read()
    assert "seven" in text.lower() or "sheva" in text.lower(), (
        "essay.md must discuss the festival's derivation from sheva (seven)"
    )


def test_piece_29_essay_mentions_oath():
    """Essay must explain the שבועה (oath) resonance in the word שבועות."""
    essay_path = os.path.join(PIECE_DIR, "essay.md")
    text = open(essay_path, encoding="utf-8").read()
    assert "oath" in text.lower() or "shvuah" in text.lower() or "שְׁבוּעָה" in text, (
        "essay.md must mention the covenant-oath meaning of שבועה"
    )


def test_piece_29_essay_mentions_fifty():
    """Essay must discuss the significance of fifty."""
    essay_path = os.path.join(PIECE_DIR, "essay.md")
    text = open(essay_path, encoding="utf-8").read()
    assert "fifty" in text.lower() or "50" in text, (
        "essay.md must discuss the number fifty"
    )


# ---------------------------------------------------------------------------
# HTML / animation structure
# ---------------------------------------------------------------------------

def test_piece_29_html_uses_requestanimationframe():
    """index.html must use requestAnimationFrame for the animation loop."""
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "requestAnimationFrame" in html, (
        "index.html must use requestAnimationFrame"
    )


def test_piece_29_html_has_canvas():
    """index.html must contain a <canvas> element."""
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "<canvas" in html, "index.html must contain a <canvas> element"


def test_piece_29_html_has_dft():
    """index.html must implement a DFT (Discrete Fourier Transform)."""
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "DFT" in html or "fourier" in html.lower() or "Math.PI" in html, (
        "index.html must implement a Fourier / DFT computation"
    )


def test_piece_29_html_uses_sapphire_background():
    """index.html must use the deep sapphire background color #0B1A3D."""
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "0B1A3D" in html.upper() or "0b1a3d" in html, (
        "index.html must reference the sapphire background #0B1A3D"
    )


def test_piece_29_html_embeds_essay():
    """index.html must embed essay text inline."""
    essay_text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    words = [w for w in essay_text.split() if len(w) > 5][:10]
    found = sum(1 for w in words if w in html)
    assert found >= 5, (
        f"index.html does not appear to embed essay text (only {found}/10 sampled words found)"
    )


def test_piece_29_html_hebrew_word_present():
    """index.html must contain the Hebrew word שָׁבוּעוֹת or its unvocalised form שבועות."""
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "שבועות" in html or "שָׁבוּעוֹת" in html, (
        "index.html must contain the Hebrew word שָׁבוּעוֹת"
    )


def test_piece_29_readme_mentions_epicycles():
    """README.md must mention Fourier epicycles."""
    readme = open(os.path.join(PIECE_DIR, "README.md"), encoding="utf-8").read()
    assert "epicycle" in readme.lower() or "fourier" in readme.lower(), (
        "README.md must mention Fourier epicycles"
    )


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

def test_piece_29_essay_path_matches_json():
    """The essay path in pieces.json must point to an existing file."""
    piece = get_piece()
    assert piece is not None
    essay_path = os.path.join(GALLERY_ROOT, piece["essay"])
    assert os.path.isfile(essay_path), (
        f"essay path '{piece['essay']}' in pieces.json does not exist on disk"
    )


def test_piece_29_html_path_matches_json():
    """The html path in pieces.json must point to an existing file."""
    piece = get_piece()
    assert piece is not None
    html_path = os.path.join(GALLERY_ROOT, piece["path"])
    assert os.path.isfile(html_path), (
        f"path '{piece['path']}' in pieces.json does not exist on disk"
    )


def test_piece_29_not_before_piece_25_in_json():
    """Piece 29 should come after piece 25 in pieces.json (numerical order)."""
    pieces = load_pieces()
    ids = [p["id"] for p in pieces]
    idx_25 = next((i for i, pid in enumerate(ids) if pid.startswith("25-")), None)
    idx_29 = next((i for i, pid in enumerate(ids) if pid.startswith("29-")), None)
    if idx_25 is not None and idx_29 is not None:
        assert idx_29 > idx_25, "Piece 29 should appear after piece 25 in pieces.json"
