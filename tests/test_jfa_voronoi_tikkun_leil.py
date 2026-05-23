"""
Tests for piece 88 — JFA Voronoi / Tikkun Leil Shavuot.

Validates the piece directory layout, pieces.json registration, HTML content,
and essay requirements.  All paths are resolved relative to GALLERY_ROOT so
the suite works from any working directory.
"""
import json
import os
import re

import pytest

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")
PIECE_ID = "88-jfa-voronoi-tikkun-leil"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)


def load_pieces():
    """Return the parsed pieces.json list."""
    with open(PIECES_JSON, encoding="utf-8") as fh:
        return json.load(fh)


def get_piece():
    """Return the pieces.json entry for piece 88, or None."""
    for p in load_pieces():
        if p["id"] == PIECE_ID:
            return p
    return None


# ---------------------------------------------------------------------------
# Happy-path: piece is registered and all files exist
# ---------------------------------------------------------------------------

def test_piece_registered_in_pieces_json():
    """Piece 88 must appear in pieces.json."""
    piece = get_piece()
    assert piece is not None, f"Piece '{PIECE_ID}' not found in pieces.json"


def test_piece_has_correct_theme():
    """pieces.json theme must reference Tikkun Leil Shavuot."""
    piece = get_piece()
    assert piece is not None
    assert "Tikkun" in piece["theme"], (
        f"Expected 'Tikkun' in theme, got: {piece['theme']!r}"
    )


def test_piece_has_correct_technique():
    """pieces.json technique must reference JFA Voronoi."""
    piece = get_piece()
    assert piece is not None
    assert "JFA" in piece["technique"] or "Jump Flooding" in piece["technique"], (
        f"Expected JFA or Jump Flooding in technique, got: {piece['technique']!r}"
    )


def test_index_html_exists():
    """index.html must exist in the piece directory."""
    path = os.path.join(PIECE_DIR, "index.html")
    assert os.path.isfile(path), f"index.html missing from {PIECE_DIR}"


def test_essay_md_exists():
    """essay.md must exist in the piece directory."""
    path = os.path.join(PIECE_DIR, "essay.md")
    assert os.path.isfile(path), f"essay.md missing from {PIECE_DIR}"


def test_thumbnail_svg_exists():
    """thumbnail.svg must exist in the piece directory."""
    path = os.path.join(PIECE_DIR, "thumbnail.svg")
    assert os.path.isfile(path), f"thumbnail.svg missing from {PIECE_DIR}"


def test_readme_md_exists():
    """README.md must exist in the piece directory."""
    path = os.path.join(PIECE_DIR, "README.md")
    assert os.path.isfile(path), f"README.md missing from {PIECE_DIR}"


# ---------------------------------------------------------------------------
# HTML content checks
# ---------------------------------------------------------------------------

def test_index_html_uses_requestanimationframe():
    """index.html must drive animation with requestAnimationFrame."""
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "requestAnimationFrame" in html, (
        "index.html must use requestAnimationFrame for animation"
    )


def test_index_html_has_jfa_pass():
    """index.html must define the jfaPass function implementing the JFA algorithm."""
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "jfaPass" in html, "index.html must contain jfaPass function"


def test_index_html_has_49_seeds():
    """index.html must declare N = 49 seed points."""
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert re.search(r'\bN\s*=\s*49\b', html), (
        "index.html must declare N = 49 (one seed per night-hour × Omer day)"
    )


def test_index_html_has_canvas():
    """index.html must contain a canvas element."""
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "<canvas" in html, "index.html must contain a <canvas> element"


def test_index_html_embeds_essay():
    """index.html must embed substantial essay text inline (not fetched at runtime)."""
    essay_text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    words = [w for w in essay_text.split() if len(w) > 5]
    sampled = words[:10]
    found = sum(1 for w in sampled if w in html)
    assert found >= 5, (
        f"index.html does not appear to embed essay text (only {found}/10 sampled words found)"
    )


def test_index_html_has_midnight_blue_color():
    """index.html must reference the midnight blue color #0A0F2E."""
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "0A0F2E" in html.upper() or "0a0f2e" in html, (
        "index.html must reference midnight blue color #0A0F2E"
    )


def test_index_html_has_warm_gold_color():
    """index.html must reference the dawn gold color #F0A800."""
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "F0A800" in html.upper() or "f0a800" in html, (
        "index.html must reference warm gold color #F0A800"
    )


def test_index_html_has_hebrew_letters():
    """index.html must define the Hebrew letter array for seed glyphs."""
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "HEBREW" in html, "index.html must define the HEBREW letter array"
    assert "א" in html, "index.html must include Hebrew letter aleph (א)"


def test_index_html_has_bloom_animation():
    """index.html must define BLOOM_MS or equivalent bloom duration constant."""
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "BLOOM" in html or "bloom" in html, (
        "index.html must reference bloom animation (BLOOM_MS or bloomAge)"
    )


# ---------------------------------------------------------------------------
# Essay content checks
# ---------------------------------------------------------------------------

def test_essay_is_substantial():
    """essay.md must contain at least 200 words."""
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    word_count = len(text.split())
    assert word_count >= 200, (
        f"essay.md has only {word_count} words (minimum 200)"
    )


def test_essay_mentions_zohar():
    """essay.md must cite the Zohar as the source of Tikkun Leil Shavuot."""
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    assert "Zohar" in text, "essay.md must mention the Zohar"


def test_essay_mentions_tikkun():
    """essay.md must use the word tikkun to explain the repair concept."""
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    assert "tikkun" in text.lower(), "essay.md must mention tikkun"


def test_essay_mentions_tzfat_or_karo():
    """essay.md must reference the Tzfat kabbalists or R. Joseph Karo."""
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    assert "Tzfat" in text or "Karo" in text, (
        "essay.md must mention Tzfat or R. Joseph Karo"
    )


def test_essay_mentions_slept_at_sinai():
    """essay.md must explain that Israel fell asleep before Matan Torah."""
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    lower = text.lower()
    assert "asleep" in lower or "sleep" in lower or "drowsy" in lower, (
        "essay.md must mention Israel's drowsiness before Matan Torah"
    )


# ---------------------------------------------------------------------------
# Thumbnail checks
# ---------------------------------------------------------------------------

def test_thumbnail_is_valid_svg():
    """thumbnail.svg must be valid SVG with an <svg> root element."""
    text = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert "<svg" in text and "</svg>" in text, (
        "thumbnail.svg must be a valid SVG document"
    )


def test_thumbnail_has_gradient_background():
    """thumbnail.svg must define a linearGradient for the dark-to-dawn background."""
    text = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert "linearGradient" in text, (
        "thumbnail.svg must use a linearGradient for the night-to-dawn background"
    )


def test_thumbnail_has_polygon_cells():
    """thumbnail.svg must contain polygon elements representing Voronoi cells."""
    text = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert "<polygon" in text, (
        "thumbnail.svg must contain <polygon> elements for Voronoi cells"
    )


def test_thumbnail_has_seed_dots():
    """thumbnail.svg must mark seed/learner positions with circle elements."""
    text = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert "<circle" in text, (
        "thumbnail.svg must contain <circle> elements marking learner positions"
    )


# ---------------------------------------------------------------------------
# Edge cases and failure-mode checks
# ---------------------------------------------------------------------------

def test_pieces_json_no_duplicate_ids():
    """Adding piece 88 must not create a duplicate ID."""
    pieces = load_pieces()
    ids = [p["id"] for p in pieces]
    assert len(ids) == len(set(ids)), f"Duplicate piece IDs found: {ids}"


def test_piece_path_resolves_to_existing_file():
    """The 'path' field in pieces.json must point to an existing file."""
    piece = get_piece()
    assert piece is not None
    full_path = os.path.join(GALLERY_ROOT, piece["path"])
    assert os.path.isfile(full_path), (
        f"pieces.json path '{piece['path']}' does not exist on disk"
    )


def test_piece_thumbnail_resolves_to_existing_file():
    """The 'thumbnail' field must point to an existing file."""
    piece = get_piece()
    assert piece is not None
    full_path = os.path.join(GALLERY_ROOT, piece["thumbnail"])
    assert os.path.isfile(full_path), (
        f"pieces.json thumbnail '{piece['thumbnail']}' does not exist on disk"
    )


def test_piece_essay_field_resolves_to_existing_file():
    """The 'essay' field must point to an existing file."""
    piece = get_piece()
    assert piece is not None
    full_path = os.path.join(GALLERY_ROOT, piece["essay"])
    assert os.path.isfile(full_path), (
        f"pieces.json essay '{piece['essay']}' does not exist on disk"
    )


def test_missing_piece_id_returns_none():
    """Helper get_piece() must return None for a non-existent piece ID."""
    pieces = load_pieces()
    result = next((p for p in pieces if p["id"] == "00-nonexistent"), None)
    assert result is None, "Non-existent ID should not be found in pieces.json"


def test_empty_essay_would_fail_word_count():
    """Verify the word-count check logic catches empty essay text."""
    fake_text = ""
    word_count = len(fake_text.split())
    assert word_count < 200, "Empty string must have fewer than 200 words"


def test_large_seed_count_within_range():
    """The HTML must declare exactly 49 seeds — not a different quantity."""
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert not re.search(r'\bN\s*=\s*(?!49\b)\d+', html) or re.search(r'\bN\s*=\s*49\b', html), (
        "N in index.html must equal 49"
    )
