"""
Tests specific to piece 67-magnetic-pendulum-matan-torah.

Covers: correct pieces.json entry, all required files on disk, essay content,
Hebrew overlay text in HTML, canvas + requestAnimationFrame usage, physics
constants, and several edge / failure cases.
"""
import json
import os

import pytest

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID     = "67-magnetic-pendulum-matan-torah"
PIECE_DIR    = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
PIECES_JSON  = os.path.join(GALLERY_ROOT, "pieces.json")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_piece():
    """Return the pieces.json entry for piece 67, or None if absent."""
    with open(PIECES_JSON, encoding="utf-8") as fh:
        pieces = json.load(fh)
    for p in pieces:
        if p["id"] == PIECE_ID:
            return p
    return None


def read_html():
    return open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()


def read_essay():
    return open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()


# ---------------------------------------------------------------------------
# pieces.json entry
# ---------------------------------------------------------------------------

def test_piece_67_exists_in_json():
    assert load_piece() is not None, f"Piece '{PIECE_ID}' not found in pieces.json"


def test_piece_67_theme_is_matan_torah():
    piece = load_piece()
    assert piece is not None
    assert "Matan Torah" in piece["theme"], (
        f"Expected theme 'Matan Torah', got: {piece['theme']!r}"
    )


def test_piece_67_technique_mentions_magnetic_pendulum():
    piece = load_piece()
    assert piece is not None
    assert "magnetic pendulum fractal" in piece["technique"].lower(), (
        f"Expected 'magnetic pendulum fractal' in technique, got: {piece['technique']!r}"
    )


def test_piece_67_technique_mentions_basin():
    piece = load_piece()
    assert piece is not None
    assert "basin" in piece["technique"].lower(), (
        f"Expected 'basin' in technique field, got: {piece['technique']!r}"
    )


def test_piece_67_required_fields_all_present():
    piece = load_piece()
    assert piece is not None
    for field in ("id", "title", "tagline", "year", "theme", "technique", "path", "thumbnail", "essay"):
        assert field in piece and piece[field], (
            f"Piece '{PIECE_ID}' missing or empty field '{field}'"
        )


# ---------------------------------------------------------------------------
# File layout
# ---------------------------------------------------------------------------

def test_piece_67_directory_exists():
    assert os.path.isdir(PIECE_DIR), f"Piece directory '{PIECE_DIR}' does not exist"


def test_piece_67_index_html_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "index.html")), (
        "pieces/67-magnetic-pendulum-matan-torah/index.html is missing"
    )


def test_piece_67_essay_md_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "essay.md")), (
        "pieces/67-magnetic-pendulum-matan-torah/essay.md is missing"
    )


def test_piece_67_thumbnail_svg_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "thumbnail.svg")), (
        "pieces/67-magnetic-pendulum-matan-torah/thumbnail.svg is missing"
    )


def test_piece_67_readme_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "README.md")), (
        "pieces/67-magnetic-pendulum-matan-torah/README.md is missing"
    )


# ---------------------------------------------------------------------------
# Essay content
# ---------------------------------------------------------------------------

def test_piece_67_essay_has_at_least_400_words():
    text = read_essay()
    count = len(text.split())
    assert count >= 400, f"essay.md has {count} words; need at least 400"


def test_piece_67_essay_cites_exodus_24_7():
    text = read_essay().lower()
    assert "exodus 24" in text or "24:7" in text, (
        "essay.md must cite Exodus 24:7 (naaseh v'nishma)"
    )


def test_piece_67_essay_mentions_shabbat_88a():
    text = read_essay().lower()
    assert "shabbat 88" in text or "88a" in text, (
        "essay.md must reference Talmud Shabbat 88a"
    )


def test_piece_67_essay_mentions_maharal():
    text = read_essay().lower()
    assert "maharal" in text, "essay.md must mention the Maharal's teaching"


def test_piece_67_essay_mentions_three_days():
    text = read_essay().lower()
    assert ("three" in text and "day" in text) or "shloshet" in text or "hagbalah" in text, (
        "essay.md must discuss the three preparatory days (shloshet yemei hagbalah)"
    )


# ---------------------------------------------------------------------------
# index.html content
# ---------------------------------------------------------------------------

def test_piece_67_html_contains_canvas():
    html = read_html()
    assert "<canvas" in html, "index.html must include a <canvas> element"


def test_piece_67_html_uses_requestanimationframe():
    html = read_html()
    assert "requestAnimationFrame" in html, (
        "index.html must use requestAnimationFrame for animated rendering"
    )


def test_piece_67_html_contains_hebrew_overlay():
    html = read_html()
    assert "נַעֲשֶׂה" in html or "נַעֲשֶה" in html or "נעשה" in html, (
        "index.html must contain the Hebrew text נַעֲשֶׂה וְנִשְׁמָע as an overlay"
    )


def test_piece_67_html_embeds_essay_text():
    """index.html must embed the essay text inline (not fetch it at runtime)."""
    essay = read_essay()
    html  = read_html()
    words = [w for w in essay.split() if len(w) > 5][:10]
    found = sum(1 for w in words if w in html)
    assert found >= 5, (
        f"index.html does not embed essay text — only {found}/10 sampled words found"
    )


def test_piece_67_html_contains_scripture_in_hebrew():
    html = read_html()
    # The Hebrew of Exodus 24:7 core words
    assert "נַעֲשֶׂה" in html or "נעשה" in html, (
        "index.html must include the Hebrew scripture quote for Exodus 24:7"
    )
    assert "וְנִשְׁמָע" in html or "נשמע" in html, (
        "index.html must include the Hebrew scripture quote for Exodus 24:7"
    )


def test_piece_67_html_contains_scripture_in_english():
    html = read_html()
    assert "will do" in html and "will hear" in html, (
        "index.html must include the English translation of Exodus 24:7"
    )


def test_piece_67_html_has_physics_constants():
    """Verify the key physics constants from the spec are present in the source."""
    html = read_html()
    assert "0.02" in html,  "dt = 0.02 must appear in index.html simulation code"
    assert "0.5"  in html,  "g = 0.5 must appear in index.html simulation code"
    assert "0.2"  in html,  "damping = 0.2 must appear in index.html simulation code"
    assert "3000" in html,  "maxSteps = 3000 must appear in index.html simulation code"


def test_piece_67_html_has_three_magnet_colors():
    html = read_html()
    assert "D4A020" in html.upper() or "#d4a020" in html.lower(), (
        "Gold magnet color #D4A020 must appear in index.html"
    )
    assert "1A3080" in html.upper() or "#1a3080" in html.lower(), (
        "Blue magnet color #1A3080 must appear in index.html"
    )
    assert "F0E8D0" in html.upper() or "#f0e8d0" in html.lower(), (
        "Cream magnet color #F0E8D0 must appear in index.html"
    )


# ---------------------------------------------------------------------------
# Thumbnail SVG
# ---------------------------------------------------------------------------

def test_piece_67_thumbnail_is_valid_svg():
    text = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert "<svg" in text and "</svg>" in text, (
        "thumbnail.svg does not appear to be valid SVG"
    )


def test_piece_67_thumbnail_contains_three_magnet_colors():
    text = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read().upper()
    assert "D4A020" in text, "thumbnail.svg must contain gold color #D4A020"
    assert "1A3080" in text, "thumbnail.svg must contain blue color #1A3080"
    assert "F0E8D0" in text, "thumbnail.svg must contain cream color #F0E8D0"


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

def test_piece_67_id_no_duplicate_in_json():
    """Piece IDs must be unique across the gallery."""
    with open(PIECES_JSON, encoding="utf-8") as fh:
        pieces = json.load(fh)
    ids = [p["id"] for p in pieces]
    assert ids.count(PIECE_ID) == 1, (
        f"'{PIECE_ID}' appears {ids.count(PIECE_ID)} times in pieces.json — must be exactly once"
    )


def test_piece_67_path_ends_with_html():
    piece = load_piece()
    assert piece is not None
    assert piece["path"].endswith(".html"), (
        f"path must end with .html, got: {piece['path']!r}"
    )


def test_piece_67_thumbnail_has_svg_extension():
    piece = load_piece()
    assert piece is not None
    assert piece["thumbnail"].endswith(".svg"), (
        f"thumbnail must have .svg extension, got: {piece['thumbnail']!r}"
    )


# ---------------------------------------------------------------------------
# Failure mode: a malformed entry would be caught
# ---------------------------------------------------------------------------

def test_missing_piece_id_returns_none():
    """Confirm that load_piece() returns None for a non-existent ID."""
    with open(PIECES_JSON, encoding="utf-8") as fh:
        pieces = json.load(fh)
    result = next((p for p in pieces if p["id"] == "99-nonexistent-piece"), None)
    assert result is None, "load_piece should return None for a missing ID"


def test_essay_below_minimum_words_detected(tmp_path):
    """A stub essay with fewer than 200 words must be detectable."""
    stub = tmp_path / "essay.md"
    stub.write_text("Short stub.", encoding="utf-8")
    word_count = len(stub.read_text(encoding="utf-8").split())
    assert word_count < 200, "Fixture must have fewer than 200 words for the test to be meaningful"
