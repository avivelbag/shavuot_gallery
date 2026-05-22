"""
Tests for piece 12-omer-spiral — Forty-Nine Fires (Sefirat HaOmer).

Verifies file layout, pieces.json registration, essay content,
HTML structure, and canvas animation requirements.
"""
import json
import math
import os
import re

import pytest

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID = "12-omer-spiral"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
HTML_PATH = os.path.join(PIECE_DIR, "index.html")
ESSAY_PATH = os.path.join(PIECE_DIR, "essay.md")
THUMB_PATH = os.path.join(PIECE_DIR, "thumbnail.svg")
README_PATH = os.path.join(PIECE_DIR, "README.md")
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")


# ---------------------------------------------------------------------------
# File layout
# ---------------------------------------------------------------------------

def test_piece_directory_exists():
    assert os.path.isdir(PIECE_DIR), f"Directory {PIECE_DIR} does not exist"


def test_index_html_exists():
    assert os.path.isfile(HTML_PATH), "index.html is missing"


def test_thumbnail_svg_exists():
    assert os.path.isfile(THUMB_PATH), "thumbnail.svg is missing"


def test_readme_exists():
    assert os.path.isfile(README_PATH), "README.md is missing"


def test_essay_md_exists():
    assert os.path.isfile(ESSAY_PATH), "essay.md is missing"


# ---------------------------------------------------------------------------
# pieces.json registration
# ---------------------------------------------------------------------------

def load_pieces():
    """Return the parsed pieces.json list."""
    with open(PIECES_JSON, encoding="utf-8") as fh:
        return json.load(fh)


def get_piece():
    """Return the omer-spiral entry from pieces.json, or None."""
    return next((p for p in load_pieces() if p["id"] == PIECE_ID), None)


def test_piece_registered_in_pieces_json():
    assert get_piece() is not None, f"'{PIECE_ID}' not found in pieces.json"


def test_piece_has_correct_theme():
    piece = get_piece()
    assert piece is not None
    assert "Omer" in piece["theme"] or "omer" in piece["theme"].lower(), (
        f"theme field should reference Omer, got: {piece['theme']!r}"
    )


def test_piece_essay_field_in_json():
    piece = get_piece()
    assert piece is not None
    essay = piece.get("essay", "")
    assert essay and essay.strip(), "essay field in pieces.json must be non-empty"
    assert essay == f"pieces/{PIECE_ID}/essay.md", (
        f"essay path mismatch: {essay!r}"
    )


def test_piece_path_correct():
    piece = get_piece()
    assert piece is not None
    assert piece["path"] == f"pieces/{PIECE_ID}/index.html"


def test_piece_thumbnail_correct():
    piece = get_piece()
    assert piece is not None
    assert piece["thumbnail"] == f"pieces/{PIECE_ID}/thumbnail.svg"


def test_piece_year_is_int():
    piece = get_piece()
    assert piece is not None
    assert isinstance(piece["year"], int)


def test_no_duplicate_ids():
    pieces = load_pieces()
    ids = [p["id"] for p in pieces]
    assert len(ids) == len(set(ids)), f"Duplicate piece IDs: {ids}"


# ---------------------------------------------------------------------------
# Essay content
# ---------------------------------------------------------------------------

def read_essay():
    return open(ESSAY_PATH, encoding="utf-8").read()


def test_essay_word_count():
    text = read_essay()
    words = text.split()
    assert len(words) >= 200, f"essay.md has only {len(words)} words (need ≥ 200)"


def test_essay_references_leviticus():
    text = read_essay()
    assert "Leviticus" in text or "leviticus" in text, (
        "essay.md must reference Leviticus (the biblical source)"
    )


def test_essay_references_sefirah():
    text = read_essay()
    assert "Omer" in text or "omer" in text or "sefirat" in text.lower(), (
        "essay.md must mention the Omer or Sefirat HaOmer"
    )


def test_essay_mentions_49_or_forty_nine():
    text = read_essay()
    assert "49" in text or "forty-nine" in text.lower() or "forty nine" in text.lower(), (
        "essay.md must mention the 49-day count"
    )


# ---------------------------------------------------------------------------
# HTML / canvas structure
# ---------------------------------------------------------------------------

def read_html():
    return open(HTML_PATH, encoding="utf-8").read()


def test_html_uses_canvas():
    html = read_html()
    assert "<canvas" in html, "index.html must contain a <canvas> element"


def test_html_uses_request_animation_frame():
    html = read_html()
    assert "requestAnimationFrame" in html, (
        "index.html must use requestAnimationFrame for animation"
    )


def test_html_has_49_dots_constant():
    html = read_html()
    assert "49" in html or "N = 49" in html or "const N" in html, (
        "index.html must define the 49-dot count"
    )


def test_html_has_hebrew_labels():
    html = read_html()
    assert "יום" in html, "index.html must contain Hebrew day labels (יום)"


def test_html_embeds_essay_text():
    essay = read_essay()
    html = read_html()
    words = [w for w in essay.split() if len(w) > 5]
    sampled = words[:10]
    found = sum(1 for w in sampled if w in html)
    assert found >= 5, (
        f"index.html does not embed essay text: only {found}/10 sampled words found"
    )


def test_html_has_archimedean_spiral_math():
    html = read_html()
    has_spiral = (
        "ANG_STEP" in html or "angStep" in html or
        "ang_step" in html or "STEP" in html or
        "Math.PI" in html
    )
    assert has_spiral, "index.html must implement spiral positioning (Math.PI / angular step)"


def test_html_crown_element():
    html = read_html()
    assert "crown" in html.lower() or "Crown" in html, (
        "index.html must reference a crown element for Shavuot"
    )


def test_html_no_external_scripts():
    html = read_html()
    external = re.findall(r'<script[^>]+src=["\']https?://', html)
    assert len(external) == 0, f"index.html must not load external scripts: {external}"


# ---------------------------------------------------------------------------
# Thumbnail SVG
# ---------------------------------------------------------------------------

def read_thumb():
    return open(THUMB_PATH, encoding="utf-8").read()


def test_thumbnail_is_valid_svg():
    svg = read_thumb()
    assert "<svg" in svg and "</svg>" in svg, "thumbnail.svg is not valid SVG"


def test_thumbnail_has_dots():
    svg = read_thumb()
    circles = re.findall(r'<circle', svg)
    assert len(circles) >= 49, (
        f"thumbnail.svg should have at least 49 circle elements, found {len(circles)}"
    )


def test_thumbnail_has_crown():
    svg = read_thumb()
    circles = re.findall(r'<circle', svg)
    assert len(circles) >= 50, (
        "thumbnail.svg should have a crown element (50th circle), "
        f"found only {len(circles)} circles"
    )


# ---------------------------------------------------------------------------
# Edge cases and failure modes
# ---------------------------------------------------------------------------

def test_essay_not_placeholder():
    text = read_essay()
    for stub in ("TODO", "placeholder", "lorem ipsum", "FILL IN"):
        assert stub.lower() not in text.lower(), (
            f"essay.md appears to contain placeholder text: {stub!r}"
        )


def test_html_not_placeholder():
    html = read_html()
    for stub in ("TODO", "lorem ipsum", "FILL IN"):
        assert stub.lower() not in html.lower(), (
            f"index.html appears to contain placeholder text: {stub!r}"
        )


def test_hebrew_numeral_generation():
    """Verify the Hebrew numeral JS logic handles day 15 and 16 correctly (special cases)."""
    html = read_html()
    assert "ט״ו" in html, "Hebrew numeral for day 15 (ט״ו) must appear in index.html"
    assert "ט״ז" in html, "Hebrew numeral for day 16 (ט״ז) must appear in index.html"


def test_piece_all_required_fields():
    """All required pieces.json fields must be present and non-empty."""
    required = ("id", "title", "tagline", "year", "theme", "technique", "path", "thumbnail", "essay")
    piece = get_piece()
    assert piece is not None
    for field in required:
        val = piece.get(field)
        assert val is not None and val != "", (
            f"pieces.json entry missing or empty field: {field!r}"
        )


def test_spiral_math_approximation():
    """Sanity-check the Archimedean spiral: 49 points at 7 per revolution stays within canvas bounds."""
    A, B = 12, 4.6
    ang_step = 2 * math.pi / 7
    cx, cy = 280, 280  # center of 560×560 canvas
    for i in range(49):
        theta = i * ang_step
        r = A + B * theta
        x = cx + r * math.cos(theta - math.pi / 2)
        y = cy + r * math.sin(theta - math.pi / 2)
        assert 0 <= x <= 560, f"Dot {i} x={x:.1f} out of 560px canvas"
        assert 0 <= y <= 560, f"Dot {i} y={y:.1f} out of 560px canvas"
