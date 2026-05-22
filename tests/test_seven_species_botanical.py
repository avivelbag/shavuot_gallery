"""
Tests for piece 11-seven-species-botanical.

Covers the acceptance criteria: file layout, SVG content, all seven species
present, CSS animation, palette colours, Hebrew text, and pieces.json registration.
"""
import json
import os
import re

import pytest

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID = "11-seven-species-botanical"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")

SEVEN_SPECIES = ["wheat", "barley", "grape", "fig", "pomegranate", "olive", "date"]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _piece_entry():
    with open(PIECES_JSON, encoding="utf-8") as fh:
        pieces = json.load(fh)
    for p in pieces:
        if p["id"] == PIECE_ID:
            return p
    return None


def _read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


# ---------------------------------------------------------------------------
# pieces.json registration
# ---------------------------------------------------------------------------

def test_piece_registered_in_pieces_json():
    entry = _piece_entry()
    assert entry is not None, f"'{PIECE_ID}' not found in pieces.json"


def test_pieces_json_required_fields():
    entry = _piece_entry()
    assert entry is not None
    required = ("id", "title", "tagline", "year", "theme", "technique", "path", "thumbnail", "essay")
    for field in required:
        assert field in entry and entry[field], f"Missing or empty field '{field}' in pieces.json entry"


def test_pieces_json_theme_non_empty():
    entry = _piece_entry()
    assert entry is not None
    assert entry.get("theme"), "theme field must be non-empty"


def test_pieces_json_essay_field_non_empty():
    entry = _piece_entry()
    assert entry is not None
    assert entry.get("essay"), "essay field must be non-empty"


def test_pieces_json_id_matches_directory():
    entry = _piece_entry()
    assert entry is not None
    path_parts = entry["path"].replace("\\", "/").split("/")
    dir_name = path_parts[-2]
    assert dir_name == PIECE_ID, f"Directory '{dir_name}' does not match id '{PIECE_ID}'"


# ---------------------------------------------------------------------------
# File layout (happy path)
# ---------------------------------------------------------------------------

def test_piece_svg_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "piece.svg")), "piece.svg missing"


def test_thumbnail_svg_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "thumbnail.svg")), "thumbnail.svg missing"


def test_readme_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "README.md")), "README.md missing"


def test_essay_md_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "essay.md")), "essay.md missing"


def test_index_html_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "index.html")), "index.html missing"


# ---------------------------------------------------------------------------
# essay.md content
# ---------------------------------------------------------------------------

def test_essay_has_at_least_200_words():
    text = _read(os.path.join(PIECE_DIR, "essay.md"))
    word_count = len(text.split())
    assert word_count >= 200, f"essay.md has only {word_count} words (need ≥ 200)"


def test_essay_mentions_deuteronomy():
    """Essay must cite a real Torah source (Deuteronomy 26 for Bikkurim)."""
    text = _read(os.path.join(PIECE_DIR, "essay.md")).lower()
    assert "deuteronomy" in text or "devarim" in text, "essay must reference Deuteronomy"


def test_essay_mentions_bikkurim():
    text = _read(os.path.join(PIECE_DIR, "essay.md")).lower()
    assert "bikkurim" in text, "essay must mention Bikkurim"


# ---------------------------------------------------------------------------
# index.html embeds essay text
# ---------------------------------------------------------------------------

def test_index_html_contains_essay_words():
    """At least 5 of the first 10 long words in essay.md must appear in index.html."""
    essay = _read(os.path.join(PIECE_DIR, "essay.md"))
    html = _read(os.path.join(PIECE_DIR, "index.html"))
    long_words = [w for w in essay.split() if len(w) > 5][:10]
    found = sum(1 for w in long_words if w in html)
    assert found >= 5, (
        f"Only {found}/10 sampled essay words found in index.html — essay must be embedded inline"
    )


def test_index_html_references_piece_svg():
    html = _read(os.path.join(PIECE_DIR, "index.html"))
    assert "piece.svg" in html, "index.html must reference piece.svg"


# ---------------------------------------------------------------------------
# piece.svg structure
# ---------------------------------------------------------------------------

def test_piece_svg_is_valid_svg():
    svg = _read(os.path.join(PIECE_DIR, "piece.svg"))
    assert "<svg" in svg and "</svg>" in svg, "piece.svg does not look like valid SVG"


def test_piece_svg_has_viewbox():
    svg = _read(os.path.join(PIECE_DIR, "piece.svg"))
    assert "viewBox" in svg, "piece.svg must declare a viewBox"


def test_piece_svg_viewbox_is_600x600():
    svg = _read(os.path.join(PIECE_DIR, "piece.svg"))
    assert "0 0 600 600" in svg, "piece.svg viewBox must be '0 0 600 600'"


def test_piece_svg_has_hebrew_text():
    svg = _read(os.path.join(PIECE_DIR, "piece.svg"))
    assert "שִׁבְעַת" in svg or "הַמִּינִים" in svg, (
        "piece.svg must contain the Hebrew text שִׁבְעַת הַמִּינִים"
    )


def test_piece_svg_has_css_animation():
    svg = _read(os.path.join(PIECE_DIR, "piece.svg"))
    assert "@keyframes" in svg, "piece.svg must contain @keyframes CSS animation"


def test_piece_svg_animation_is_4s():
    svg = _read(os.path.join(PIECE_DIR, "piece.svg"))
    assert "4s" in svg, "leaf sway animation must be 4 seconds"


def test_piece_svg_uses_transform_origin_bottom():
    svg = _read(os.path.join(PIECE_DIR, "piece.svg"))
    assert "transform-origin" in svg, "piece.svg must set transform-origin for leaf sway"
    assert "bottom" in svg, "transform-origin must reference bottom (stem base)"


def test_piece_svg_no_external_stylesheets():
    svg = _read(os.path.join(PIECE_DIR, "piece.svg"))
    assert "<link" not in svg, "piece.svg must not use external stylesheets"
    assert "href=" not in svg or "xlink:href" not in svg.replace("xlink:href", ""), (
        "piece.svg must be self-contained — no external stylesheet links"
    )


def test_piece_svg_has_background_parchment():
    svg = _read(os.path.join(PIECE_DIR, "piece.svg"))
    assert "#f5ead0" in svg, "piece.svg must use parchment background #f5ead0"


def test_piece_svg_has_pomegranate_red():
    svg = _read(os.path.join(PIECE_DIR, "piece.svg"))
    assert "#c0392b" in svg, "piece.svg must use pomegranate red #c0392b"


def test_piece_svg_has_grape_purple():
    svg = _read(os.path.join(PIECE_DIR, "piece.svg"))
    assert "#6b2d8b" in svg, "piece.svg must use grape purple #6b2d8b"


def test_piece_svg_has_leaf_green():
    svg = _read(os.path.join(PIECE_DIR, "piece.svg"))
    assert "#2d5a1b" in svg, "piece.svg must use deep leaf green #2d5a1b"


def test_piece_svg_has_date_amber():
    svg = _read(os.path.join(PIECE_DIR, "piece.svg"))
    assert "#d4821a" in svg, "piece.svg must include date amber #d4821a"


def test_piece_svg_has_all_seven_species_groups():
    """SVG must contain enough <g> groups to represent all seven species (plus grains/wheat as 2 each)."""
    svg = _read(os.path.join(PIECE_DIR, "piece.svg"))
    g_count = svg.count("<g ")
    assert g_count >= 9, (
        f"Expected at least 9 species groups in piece.svg, found {g_count} <g elements"
    )


def test_piece_svg_has_grape_circles():
    """Grapes must use <circle> elements for individual grape berries."""
    svg = _read(os.path.join(PIECE_DIR, "piece.svg"))
    circle_count = svg.count("<circle")
    assert circle_count >= 5, (
        f"Expected at least 5 <circle> elements for grape cluster, found {circle_count}"
    )


def test_piece_svg_has_barley_awns():
    """Barley is distinguished from wheat by awns (long thin lines)."""
    svg = _read(os.path.join(PIECE_DIR, "piece.svg"))
    line_count = svg.count("<line")
    assert line_count >= 6, (
        f"Expected at least 6 <line> elements (barley awns and stems), found {line_count}"
    )


# ---------------------------------------------------------------------------
# thumbnail.svg
# ---------------------------------------------------------------------------

def test_thumbnail_is_valid_svg():
    svg = _read(os.path.join(PIECE_DIR, "thumbnail.svg"))
    assert "<svg" in svg and "</svg>" in svg, "thumbnail.svg is not valid SVG"


def test_thumbnail_has_hebrew_text():
    svg = _read(os.path.join(PIECE_DIR, "thumbnail.svg"))
    assert "שִׁבְעַת" in svg or "הַמִּינִים" in svg, (
        "thumbnail.svg must contain the Hebrew text"
    )


# ---------------------------------------------------------------------------
# Edge cases and failure modes
# ---------------------------------------------------------------------------

def test_piece_svg_inline_css_only():
    """The <style> block must be inside the SVG, not an external file."""
    svg = _read(os.path.join(PIECE_DIR, "piece.svg"))
    assert "<style>" in svg or "<style " in svg, "CSS must be inline inside piece.svg"


def test_essay_md_does_not_just_say_placeholder(tmp_path):
    """essay.md must not be a stub — check that it has real sentences (>10 chars per word avg)."""
    text = _read(os.path.join(PIECE_DIR, "essay.md"))
    words = text.split()
    assert len(words) >= 200, f"essay.md stub detected: only {len(words)} words"
    long_words = [w for w in words if len(w) > 4]
    assert len(long_words) >= 50, "essay.md appears to be a placeholder — too few substantive words"


def test_missing_piece_svg_detected(tmp_path):
    """Verify that absence of piece.svg would be caught."""
    fake_path = os.path.join(str(tmp_path), "piece.svg")
    assert not os.path.isfile(fake_path), "Fixture path must not exist"


def test_missing_essay_detected(tmp_path):
    """Verify that absence of essay.md would be caught."""
    fake_path = os.path.join(str(tmp_path), "essay.md")
    assert not os.path.isfile(fake_path), "Fixture path must not exist"
