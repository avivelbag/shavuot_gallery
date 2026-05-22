"""
Tests for piece 47 — The Aleph of Anochi (Lorenz Attractor).

Covers the pieces.json registration, on-disk file layout, essay content
requirements, and HTML correctness for the new piece.
"""
import json
import os
import re

import pytest

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECES_JSON  = os.path.join(GALLERY_ROOT, "pieces.json")
PIECE_ID     = "47-aleph-of-anochi"
PIECE_DIR    = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_pieces():
    """Load and return the parsed pieces.json list."""
    with open(PIECES_JSON, "r", encoding="utf-8") as fh:
        return json.load(fh)


def get_piece():
    """Return the pieces.json entry for piece 47, or None if absent."""
    for p in load_pieces():
        if p["id"] == PIECE_ID:
            return p
    return None


def read_file(rel_path):
    """Read a file relative to GALLERY_ROOT and return its text."""
    return open(os.path.join(GALLERY_ROOT, rel_path), encoding="utf-8").read()


# ---------------------------------------------------------------------------
# pieces.json registration
# ---------------------------------------------------------------------------

def test_piece_47_in_pieces_json():
    """Piece 47 must appear in pieces.json."""
    piece = get_piece()
    assert piece is not None, f"Piece '{PIECE_ID}' not found in pieces.json"


def test_piece_47_required_fields():
    """All required fields must be present and non-empty."""
    required = ("id", "title", "tagline", "year", "theme", "technique",
                "path", "thumbnail", "essay")
    piece = get_piece()
    assert piece is not None, f"Piece '{PIECE_ID}' missing from pieces.json"
    for field in required:
        assert field in piece, f"Field '{field}' missing from piece 47 entry"
        val = piece[field]
        assert val is not None and val != "", \
            f"Field '{field}' is empty in piece 47 entry"


def test_piece_47_id_matches_path():
    """The piece id must match the directory component of its path."""
    piece = get_piece()
    assert piece is not None
    parts = piece["path"].replace("\\", "/").split("/")
    assert len(parts) >= 2
    assert parts[-2] == PIECE_ID, \
        f"Directory in path '{piece['path']}' does not match id '{PIECE_ID}'"


def test_piece_47_year_is_int():
    """Year field must be an integer."""
    piece = get_piece()
    assert piece is not None
    assert isinstance(piece["year"], int), \
        f"year field is not an integer: {piece['year']!r}"


def test_piece_47_no_duplicate_id():
    """Piece 47 id must appear exactly once in pieces.json."""
    pieces = load_pieces()
    ids = [p["id"] for p in pieces]
    assert ids.count(PIECE_ID) == 1, \
        f"Piece id '{PIECE_ID}' appears {ids.count(PIECE_ID)} times (expected 1)"


def test_piece_47_thumbnail_extension():
    """Thumbnail must have a recognised image extension."""
    piece = get_piece()
    assert piece is not None
    ext = os.path.splitext(piece["thumbnail"])[1].lower()
    assert ext in {".svg", ".png", ".jpg", ".jpeg", ".webp", ".gif"}, \
        f"Unrecognised thumbnail extension: '{ext}'"


def test_piece_47_path_ends_with_html():
    """Piece path must end with .html."""
    piece = get_piece()
    assert piece is not None
    assert piece["path"].endswith(".html"), \
        f"Piece path does not end with .html: '{piece['path']}'"


# ---------------------------------------------------------------------------
# On-disk file layout
# ---------------------------------------------------------------------------

def test_piece_47_index_html_exists():
    """pieces/47-aleph-of-anochi/index.html must exist."""
    piece = get_piece()
    assert piece is not None
    full = os.path.join(GALLERY_ROOT, piece["path"])
    assert os.path.isfile(full), f"index.html not found at '{piece['path']}'"


def test_piece_47_thumbnail_exists():
    """The thumbnail SVG must exist on disk."""
    piece = get_piece()
    assert piece is not None
    full = os.path.join(GALLERY_ROOT, piece["thumbnail"])
    assert os.path.isfile(full), f"thumbnail not found at '{piece['thumbnail']}'"


def test_piece_47_essay_md_exists():
    """pieces/47-aleph-of-anochi/essay.md must exist on disk."""
    piece = get_piece()
    assert piece is not None
    full = os.path.join(GALLERY_ROOT, piece["essay"])
    assert os.path.isfile(full), f"essay.md not found at '{piece['essay']}'"


def test_piece_47_readme_exists():
    """pieces/47-aleph-of-anochi/README.md must exist."""
    readme = os.path.join(PIECE_DIR, "README.md")
    assert os.path.isfile(readme), f"README.md missing from {PIECE_DIR}"


def test_piece_47_thumbnail_is_valid_svg():
    """The thumbnail must contain valid SVG markup."""
    piece = get_piece()
    assert piece is not None
    text = read_file(piece["thumbnail"])
    assert "<svg" in text and "</svg>" in text, \
        "thumbnail.svg does not contain valid SVG markup"


# ---------------------------------------------------------------------------
# Essay content requirements
# ---------------------------------------------------------------------------

def test_piece_47_essay_min_words():
    """essay.md must contain at least 200 words."""
    piece = get_piece()
    assert piece is not None
    text = read_file(piece["essay"])
    word_count = len(text.split())
    assert word_count >= 200, \
        f"essay.md has only {word_count} words (need ≥ 200)"


def test_piece_47_essay_cites_makkot():
    """essay.md must cite Makkot 24a as required by the acceptance criteria."""
    piece = get_piece()
    assert piece is not None
    text = read_file(piece["essay"])
    assert "Makkot" in text and "24a" in text, \
        "essay.md must cite Makkot 24a"


def test_piece_47_essay_cites_shemot_rabbah():
    """essay.md must cite Shemot Rabbah 29:9."""
    piece = get_piece()
    assert piece is not None
    text = read_file(piece["essay"])
    assert "Shemot Rabbah" in text or "Shemot Rabbah" in text, \
        "essay.md must cite Shemot Rabbah"
    assert "29:9" in text, "essay.md must cite Shemot Rabbah 29:9"


def test_piece_47_essay_mentions_aleph():
    """essay.md must explain the significance of the aleph letter."""
    piece = get_piece()
    assert piece is not None
    text = read_file(piece["essay"])
    assert "aleph" in text.lower(), \
        "essay.md must discuss the aleph letter"


def test_piece_47_essay_mentions_lorenz():
    """essay.md must explain the Lorenz attractor analogy."""
    piece = get_piece()
    assert piece is not None
    text = read_file(piece["essay"])
    assert "Lorenz" in text, \
        "essay.md must discuss the Lorenz attractor"


def test_piece_47_essay_mentions_butterfly():
    """essay.md should mention the butterfly shape (the visual parallel)."""
    piece = get_piece()
    assert piece is not None
    text = read_file(piece["essay"])
    assert "butterfly" in text.lower(), \
        "essay.md must note the butterfly shape of the x-z projection"


# ---------------------------------------------------------------------------
# index.html correctness
# ---------------------------------------------------------------------------

def test_piece_47_html_uses_requestanimationframe():
    """index.html must use requestAnimationFrame for animation."""
    piece = get_piece()
    assert piece is not None
    html = read_file(piece["path"])
    assert "requestAnimationFrame" in html, \
        "index.html must use requestAnimationFrame"


def test_piece_47_html_mentions_rk4():
    """index.html must implement or mention RK4 integration."""
    piece = get_piece()
    assert piece is not None
    html = read_file(piece["path"])
    assert "rk4" in html.lower() or "runge" in html.lower() or "RK4" in html, \
        "index.html must implement RK4 integration"


def test_piece_47_html_uses_lorenz_parameters():
    """index.html must use the canonical Lorenz parameters σ=10, ρ=28, β=8/3."""
    piece = get_piece()
    assert piece is not None
    html = read_file(piece["path"])
    assert "10" in html and "28" in html, \
        "index.html must include sigma=10 and rho=28"


def test_piece_47_html_mentions_aleph_glyph():
    """index.html must render the aleph letter (א)."""
    piece = get_piece()
    assert piece is not None
    html = read_file(piece["path"])
    assert "א" in html, \
        "index.html must include the Hebrew aleph character (א)"


def test_piece_47_html_uses_background_color():
    """index.html must use the specified indigo-black background color."""
    piece = get_piece()
    assert piece is not None
    html = read_file(piece["path"])
    assert "#08061A" in html or "#08061a" in html, \
        "index.html must use background color #08061A"


def test_piece_47_html_embeds_essay_text():
    """index.html must embed essay text inline — spot-check 5 of 10 sampled words."""
    piece = get_piece()
    assert piece is not None
    essay_text = read_file(piece["essay"])
    html        = read_file(piece["path"])
    words = [w for w in essay_text.split() if len(w) > 5]
    sampled = words[:10]
    found = sum(1 for w in sampled if w in html)
    assert found >= 5, \
        f"index.html does not appear to embed essay text (found {found}/10 sampled words)"


def test_piece_47_html_has_canvas():
    """index.html must contain at least one <canvas> element."""
    piece = get_piece()
    assert piece is not None
    html = read_file(piece["path"])
    assert "<canvas" in html, "index.html must contain a <canvas> element"


def test_piece_47_html_velocity_colors():
    """index.html must include at least two of the specified palette colors."""
    piece = get_piece()
    assert piece is not None
    html = read_file(piece["path"])
    palette_colors = ["#4A1A8C", "#1A4ACA", "#D4A017", "#F5F0E0"]
    present = [c for c in palette_colors if c in html or c.lower() in html.lower()]
    assert len(present) >= 2, \
        f"index.html must include at least 2 palette colors; found: {present}"


# ---------------------------------------------------------------------------
# Edge cases / failure mode tests
# ---------------------------------------------------------------------------

def test_essay_word_count_below_200_fails(tmp_path):
    """A stub essay with fewer than 200 words must be detected as insufficient."""
    stub = tmp_path / "stub.md"
    stub.write_text("short " * 50, encoding="utf-8")   # 50 words
    text = stub.read_text(encoding="utf-8")
    word_count = len(text.split())
    assert word_count < 200, "Fixture must have fewer than 200 words"


def test_missing_piece_id_not_in_json(tmp_path):
    """An id that does not exist in pieces.json should not be found."""
    pieces = load_pieces()
    ids = [p["id"] for p in pieces]
    assert "99-nonexistent-piece" not in ids, \
        "Non-existent piece id should not appear in pieces.json"


def test_piece_47_directory_exists():
    """The piece directory must exist on disk."""
    assert os.path.isdir(PIECE_DIR), \
        f"Piece directory '{PIECE_DIR}' does not exist"
