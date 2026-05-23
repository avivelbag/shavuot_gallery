"""
Tests for piece 91-spectre-monotile-aleph.

Covers: pieces.json registration, file layout, HTML content requirements,
essay word count, SVG thumbnail validity, and edge cases.
"""
import json
import os

import pytest

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID = "91-spectre-monotile-aleph"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)


def load_pieces():
    with open(os.path.join(GALLERY_ROOT, "pieces.json"), encoding="utf-8") as f:
        return json.load(f)


def get_piece():
    for p in load_pieces():
        if p["id"] == PIECE_ID:
            return p
    return None


# ---------------------------------------------------------------------------
# pieces.json registration
# ---------------------------------------------------------------------------

def test_piece_registered_in_json():
    """The spectre piece must appear in pieces.json."""
    assert get_piece() is not None, f"Piece '{PIECE_ID}' not found in pieces.json"


def test_piece_theme():
    p = get_piece()
    assert p is not None
    theme = p.get("theme", "")
    assert "Aleph" in theme or "Anochi" in theme or "Matan Torah" in theme, (
        f"Theme should reference Aleph/Anochi/Matan Torah, got: {theme!r}"
    )


def test_piece_technique():
    p = get_piece()
    assert p is not None
    tech = p.get("technique", "")
    assert "spectre" in tech.lower() or "monotile" in tech.lower() or "substitution" in tech.lower(), (
        f"Technique should mention spectre/monotile/substitution, got: {tech!r}"
    )


def test_piece_year():
    p = get_piece()
    assert p is not None
    assert p["year"] == 2026


def test_no_duplicate_id():
    pieces = load_pieces()
    ids = [p["id"] for p in pieces]
    assert ids.count(PIECE_ID) == 1, "Duplicate piece ID found"


# ---------------------------------------------------------------------------
# File layout
# ---------------------------------------------------------------------------

def test_index_html_exists():
    path = os.path.join(PIECE_DIR, "index.html")
    assert os.path.isfile(path), "index.html is missing"


def test_essay_md_exists():
    path = os.path.join(PIECE_DIR, "essay.md")
    assert os.path.isfile(path), "essay.md is missing"


def test_thumbnail_svg_exists():
    path = os.path.join(PIECE_DIR, "thumbnail.svg")
    assert os.path.isfile(path), "thumbnail.svg is missing"


def test_readme_exists():
    path = os.path.join(PIECE_DIR, "README.md")
    assert os.path.isfile(path), "README.md is missing"


# ---------------------------------------------------------------------------
# Essay content
# ---------------------------------------------------------------------------

def test_essay_minimum_words():
    path = os.path.join(PIECE_DIR, "essay.md")
    text = open(path, encoding="utf-8").read()
    words = len(text.split())
    assert words >= 400, f"Essay has only {words} words (need ≥ 400)"


def test_essay_mentions_makkot():
    """Essay must cite Makkot 24a as required by acceptance criteria."""
    path = os.path.join(PIECE_DIR, "essay.md")
    text = open(path, encoding="utf-8").read()
    assert "Makkot" in text or "24a" in text, "Essay must cite Makkot 24a"


def test_essay_mentions_aleph():
    path = os.path.join(PIECE_DIR, "essay.md")
    text = open(path, encoding="utf-8").read()
    assert "Aleph" in text or "aleph" in text or "א" in text, "Essay must mention the Aleph"


def test_essay_mentions_spectre():
    path = os.path.join(PIECE_DIR, "essay.md")
    text = open(path, encoding="utf-8").read()
    assert "spectre" in text.lower() or "aperiodic" in text.lower(), (
        "Essay must explain the spectre tile"
    )


def test_essay_mentions_baal_shem_tov_or_chasidic():
    path = os.path.join(PIECE_DIR, "essay.md")
    text = open(path, encoding="utf-8").read().lower()
    assert "baal shem tov" in text or "chasidic" in text or "zoharic" in text or "kabbalistic" in text, (
        "Essay must reference the Chasidic/Zoharic tradition of the silent Aleph"
    )


# ---------------------------------------------------------------------------
# HTML content
# ---------------------------------------------------------------------------

def test_html_has_canvas():
    path = os.path.join(PIECE_DIR, "index.html")
    html = open(path, encoding="utf-8").read()
    assert "<canvas" in html, "index.html must include a <canvas> element"


def test_html_uses_requestanimationframe():
    path = os.path.join(PIECE_DIR, "index.html")
    html = open(path, encoding="utf-8").read()
    assert "requestAnimationFrame" in html, (
        "index.html must use requestAnimationFrame for animation"
    )


def test_html_references_gold_color():
    """The flame-gold palette color must appear in the HTML."""
    path = os.path.join(PIECE_DIR, "index.html")
    html = open(path, encoding="utf-8").read().lower()
    assert "d4a017" in html, "index.html must use flame gold #D4A017"


def test_html_references_lapis_color():
    """Deep lapis must appear in the palette."""
    path = os.path.join(PIECE_DIR, "index.html")
    html = open(path, encoding="utf-8").read().lower()
    assert "1b2a6b" in html, "index.html must use deep lapis #1B2A6B"


def test_html_contains_aleph_character():
    """The Hebrew Aleph glyph must be drawn in the canvas script."""
    path = os.path.join(PIECE_DIR, "index.html")
    html = open(path, encoding="utf-8").read()
    assert "א" in html, "index.html must contain the Hebrew Aleph character (א)"


def test_html_embeds_essay_content():
    """Essay text must be embedded in index.html (no runtime fetch)."""
    essay_path = os.path.join(PIECE_DIR, "essay.md")
    html_path = os.path.join(PIECE_DIR, "index.html")
    essay = open(essay_path, encoding="utf-8").read()
    html = open(html_path, encoding="utf-8").read()
    long_words = [w for w in essay.split() if len(w) > 6][:12]
    found = sum(1 for w in long_words if w in html)
    assert found >= 6, (
        f"index.html does not embed essay text ({found}/{len(long_words)} words found)"
    )


def test_html_has_spectre_polygon():
    """HTML must define the spectre polygon (14 vertices)."""
    path = os.path.join(PIECE_DIR, "index.html")
    html = open(path, encoding="utf-8").read()
    # The spectre vertex list should appear — check for the characteristic coords
    assert "SPECTRE_UNIT" in html or "spectreVerts" in html or "SPECTRE_VERTS" in html, (
        "index.html must define the spectre polygon vertices"
    )


def test_html_has_pulse_animation():
    """HTML must implement the 4-second pulse animation."""
    path = os.path.join(PIECE_DIR, "index.html")
    html = open(path, encoding="utf-8").read()
    assert "4000" in html or "CYCLE" in html, (
        "index.html must implement 4-second pulse cycle"
    )


def test_html_has_substitution_logic():
    """HTML must implement substitution (collectTiles or equivalent)."""
    path = os.path.join(PIECE_DIR, "index.html")
    html = open(path, encoding="utf-8").read()
    assert "collectTiles" in html or "CHILDREN" in html or "substitut" in html.lower(), (
        "index.html must implement the substitution rule"
    )


# ---------------------------------------------------------------------------
# Thumbnail SVG
# ---------------------------------------------------------------------------

def test_thumbnail_is_valid_svg():
    path = os.path.join(PIECE_DIR, "thumbnail.svg")
    text = open(path, encoding="utf-8").read()
    assert "<svg" in text and "</svg>" in text, "thumbnail.svg is not valid SVG"


def test_thumbnail_has_correct_dimensions():
    path = os.path.join(PIECE_DIR, "thumbnail.svg")
    text = open(path, encoding="utf-8").read()
    assert 'width="400"' in text and 'height="400"' in text, (
        "thumbnail.svg must be 400×400"
    )


def test_thumbnail_has_dark_background():
    path = os.path.join(PIECE_DIR, "thumbnail.svg")
    text = open(path, encoding="utf-8").read().lower()
    assert "0a0a14" in text or "#0a0a14" in text or "rect" in text, (
        "thumbnail.svg must have a dark background"
    )


def test_thumbnail_has_aleph():
    path = os.path.join(PIECE_DIR, "thumbnail.svg")
    text = open(path, encoding="utf-8").read()
    assert "א" in text or "text" in text.lower(), (
        "thumbnail.svg should include the Aleph glyph"
    )


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

def test_missing_piece_returns_none():
    """Querying a non-existent piece ID returns None."""
    pieces = load_pieces()
    result = next((p for p in pieces if p["id"] == "999-does-not-exist"), None)
    assert result is None


def test_essay_not_empty():
    """essay.md must have non-trivial content (not a placeholder)."""
    path = os.path.join(PIECE_DIR, "essay.md")
    text = open(path, encoding="utf-8").read().strip()
    assert len(text) > 500, f"essay.md appears to be a placeholder ({len(text)} chars)"


def test_readme_mentions_spectre():
    path = os.path.join(PIECE_DIR, "README.md")
    text = open(path, encoding="utf-8").read().lower()
    assert "spectre" in text or "monotile" in text or "aperiodic" in text, (
        "README.md should describe the spectre monotile technique"
    )


def test_readme_mentions_sinai_or_aleph():
    path = os.path.join(PIECE_DIR, "README.md")
    text = open(path, encoding="utf-8").read().lower()
    assert "sinai" in text or "aleph" in text or "anochi" in text or "matan torah" in text.lower(), (
        "README.md should mention the Shavuot theme"
    )
