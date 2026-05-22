"""
Tests for piece 69 — differential growth / Bikkurim.

Validates that all required files exist, pieces.json is updated correctly,
the simulation code is syntactically present, and the essay meets word-count
requirements.
"""
import json
import os

import pytest

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID = "69-differential-growth-bikkurim"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")


def load_piece():
    with open(PIECES_JSON, encoding="utf-8") as fh:
        pieces = json.load(fh)
    for p in pieces:
        if p["id"] == PIECE_ID:
            return p
    return None


# ---------------------------------------------------------------------------
# File presence
# ---------------------------------------------------------------------------

def test_piece_directory_exists():
    assert os.path.isdir(PIECE_DIR), f"Piece directory {PIECE_DIR} is missing"


def test_index_html_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "index.html"))


def test_essay_md_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "essay.md"))


def test_thumbnail_svg_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "thumbnail.svg"))


def test_readme_md_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "README.md"))


# ---------------------------------------------------------------------------
# pieces.json registration
# ---------------------------------------------------------------------------

def test_piece_registered_in_pieces_json():
    piece = load_piece()
    assert piece is not None, f"Piece '{PIECE_ID}' not found in pieces.json"


def test_theme_is_bikkurim():
    piece = load_piece()
    assert piece is not None
    assert "Bikkurim" in piece["theme"], (
        f"Expected 'Bikkurim' in theme, got: {piece['theme']!r}"
    )


def test_technique_mentions_differential_growth():
    piece = load_piece()
    assert piece is not None
    assert "differential growth" in piece["technique"].lower(), (
        f"Expected 'differential growth' in technique, got: {piece['technique']!r}"
    )


def test_pieces_json_paths_are_consistent():
    """id, path directory, thumbnail directory, and essay directory must all agree."""
    piece = load_piece()
    assert piece is not None
    for field in ("path", "thumbnail", "essay"):
        assert PIECE_ID in piece[field], (
            f"Field '{field}' does not reference the piece id '{PIECE_ID}': {piece[field]!r}"
        )


# ---------------------------------------------------------------------------
# index.html — simulation requirements
# ---------------------------------------------------------------------------

def _html():
    with open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8") as fh:
        return fh.read()


def test_canvas_is_700x700():
    html = _html()
    assert "700" in html, "Canvas size 700 not found in index.html"


def test_uses_request_animation_frame():
    assert "requestAnimationFrame" in _html()


def test_has_repulsion_radius_constant():
    html = _html()
    assert "REPULSION_RADIUS" in html, "REPULSION_RADIUS constant not found in index.html"


def test_has_spring_cohesion():
    html = _html()
    assert "SPRING_K" in html, "SPRING_K cohesion constant not found in index.html"


def test_has_node_insertion_logic():
    """splice is used to insert midpoint nodes at long edges."""
    assert "splice" in _html()


def test_has_restart_threshold():
    assert "RESTART_THRESHOLD" in _html()


def test_has_beginpath_closepath_fill():
    html = _html()
    assert "beginPath" in html
    assert "closePath" in html
    assert "fill()" in html


def test_background_is_field_green():
    assert "0A2010" in _html()


def test_has_harvest_gold_fill_color():
    assert "C8A020" in _html()


def test_has_amber_color():
    """Ripening color D4600A or its numeric components must appear."""
    html = _html()
    assert "D4600A" in html or "d4600a" in html or "D4600A".lower() in html.lower()


def test_has_hebrew_text():
    html = _html()
    assert "רֵאשִׁית" in html or "בִּכּוּרֵי" in html, (
        "Hebrew Exodus 23:19 text not found in index.html"
    )


def test_essay_embedded_in_html():
    """The essay must be embedded directly in index.html (no runtime fetch)."""
    html = _html()
    essay = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    words = [w for w in essay.split() if len(w) > 6][:10]
    found = sum(1 for w in words if w in html)
    assert found >= 5, (
        f"Only {found}/10 essay words found in index.html; essay does not appear embedded"
    )


# ---------------------------------------------------------------------------
# essay.md — content requirements
# ---------------------------------------------------------------------------

def test_essay_word_count():
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    count = len(text.split())
    assert count >= 400, f"Essay has {count} words; need at least 400"


def test_essay_mentions_deuteronomy():
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    assert "Deuteronomy" in text


def test_essay_mentions_seven_species():
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    lower = text.lower()
    assert "seven species" in lower or "shivat haminim" in lower or "shivat" in lower


def test_essay_mentions_mishnah_bikkurim():
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    assert "Mishnah" in text or "Bikkurim" in text


# ---------------------------------------------------------------------------
# thumbnail.svg
# ---------------------------------------------------------------------------

def test_thumbnail_is_valid_svg():
    text = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert "<svg" in text and "</svg>" in text


def test_thumbnail_has_green_background():
    text = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert "0A2010" in text


def test_thumbnail_has_gold_fill():
    text = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert "C8A020" in text


def test_thumbnail_has_polygon_or_path():
    text = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert "<polygon" in text or "<path" in text


# ---------------------------------------------------------------------------
# Edge cases and failure modes
# ---------------------------------------------------------------------------

def test_no_duplicate_id_in_pieces_json():
    with open(PIECES_JSON, encoding="utf-8") as fh:
        pieces = json.load(fh)
    ids = [p["id"] for p in pieces]
    assert ids.count(PIECE_ID) == 1, f"Duplicate entry for '{PIECE_ID}' in pieces.json"


def test_index_html_no_external_fetch():
    """The piece must be self-contained — no fetch() or XMLHttpRequest calls."""
    html = _html()
    assert "fetch(" not in html, "index.html must not use fetch() — piece must be self-contained"
    assert "XMLHttpRequest" not in html


def test_empty_nodes_does_not_crash_draw_function():
    """The drawFrame guard (nodes.length >= 2) prevents crashes with no nodes."""
    html = _html()
    assert "nodes.length" in html, "No guard on nodes.length found in index.html"


def test_essay_does_not_contain_placeholder_text():
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read().lower()
    for placeholder in ("lorem ipsum", "todo", "placeholder", "tbd"):
        assert placeholder not in text, f"Placeholder text '{placeholder}' found in essay.md"
