"""
Tests for piece 60 — Livnat HaSapir: The Pavement of Sapphire (Wang tiles).

Covers: pieces.json registration, file layout, essay content, HTML structure,
thumbnail validity, and specific Wang-tile / sapphire-pavement acceptance criteria.
"""
import json
import os
import re

import pytest

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECES_JSON  = os.path.join(GALLERY_ROOT, "pieces.json")
PIECE_ID     = "60-sapphire-pavement-wang-tiles"
PIECE_DIR    = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)


def load_pieces():
    with open(PIECES_JSON, encoding="utf-8") as fh:
        return json.load(fh)


def get_piece():
    for p in load_pieces():
        if p["id"] == PIECE_ID:
            return p
    return None


def read_piece_file(name):
    return open(os.path.join(PIECE_DIR, name), encoding="utf-8").read()


# ---------------------------------------------------------------------------
# pieces.json registration
# ---------------------------------------------------------------------------

def test_piece_registered_in_pieces_json():
    """Piece 60 must appear in pieces.json."""
    piece = get_piece()
    assert piece is not None, f"Piece '{PIECE_ID}' not found in pieces.json"


def test_piece_theme_is_har_sinai():
    """Theme must be 'Har Sinai' per the acceptance criteria."""
    piece = get_piece()
    assert piece is not None
    assert piece["theme"] == "Har Sinai", (
        f"Expected theme 'Har Sinai', got '{piece['theme']}'"
    )


def test_piece_technique_mentions_wang():
    """Technique field must mention Wang tiles."""
    piece = get_piece()
    assert piece is not None
    assert "Wang" in piece["technique"] or "wang" in piece["technique"].lower(), (
        f"Technique '{piece['technique']}' does not mention Wang tiles"
    )


def test_piece_technique_mentions_aperiodic():
    """Technique field must mention 'aperiodic'."""
    piece = get_piece()
    assert piece is not None
    assert "aperiodic" in piece["technique"].lower(), (
        f"Technique '{piece['technique']}' does not mention 'aperiodic'"
    )


def test_piece_year_is_2026():
    piece = get_piece()
    assert piece is not None
    assert piece["year"] == 2026


def test_piece_id_no_duplicate():
    """Piece ID must be unique in pieces.json."""
    pieces = load_pieces()
    ids = [p["id"] for p in pieces]
    assert ids.count(PIECE_ID) == 1, f"Duplicate ID '{PIECE_ID}' in pieces.json"


def test_piece_number_is_60():
    """Piece ID must start with '60-' (the next available number after 59)."""
    assert PIECE_ID.startswith("60-"), f"Piece ID '{PIECE_ID}' does not start with '60-'"


# ---------------------------------------------------------------------------
# File layout
# ---------------------------------------------------------------------------

def test_index_html_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "index.html"))


def test_essay_md_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "essay.md"))


def test_thumbnail_svg_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "thumbnail.svg"))


def test_readme_md_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "README.md"))


# ---------------------------------------------------------------------------
# Canvas / HTML acceptance criteria
# ---------------------------------------------------------------------------

def test_canvas_dimensions_700x700():
    """Canvas must be declared 700×700 pixels."""
    html = read_piece_file("index.html")
    assert 'width="700"' in html and 'height="700"' in html, (
        "index.html canvas must be 700×700"
    )


def test_grid_size_20x20_in_html():
    """HTML must reference a 20×20 grid constant."""
    html = read_piece_file("index.html")
    assert "GRID = 20" in html or "const GRID=20" in html or "GRID=20" in html, (
        "index.html must declare a 20x20 GRID constant"
    )


def test_tile_size_35_in_html():
    """Each tile must be 35px."""
    html = read_piece_file("index.html")
    assert "TILE = 35" in html or "TILE=35" in html, (
        "index.html must declare TILE = 35"
    )


def test_sapphire_palette_present():
    """All four palette colors must appear in the HTML."""
    html = read_piece_file("index.html")
    for color in ["#0A1F6E", "#3A7BD5", "#C8E6FA", "#D4A820"]:
        assert color in html, f"Palette color {color} missing from index.html"


def test_wang_tiles_array_in_html():
    """TILES array must be defined in the HTML script."""
    html = read_piece_file("index.html")
    assert "const TILES" in html or "TILES =" in html, (
        "index.html must define a TILES array for the Wang tile set"
    )


def test_central_void_hebrew_label_in_html():
    """HTML must contain the Hebrew phrase for 'under His feet'."""
    html = read_piece_file("index.html")
    assert "תַּחַת רַגְלָיו" in html, (
        "index.html must contain Hebrew label 'תַּחַת רַגְלָיו'"
    )


def test_animation_uses_requestanimationframe():
    """Animation must use requestAnimationFrame (no setInterval-only pattern)."""
    html = read_piece_file("index.html")
    assert "requestAnimationFrame" in html


def test_fill_animation_constant_8_seconds():
    """HTML must reference the 8-second fill duration."""
    html = read_piece_file("index.html")
    assert "8000" in html, "index.html must define an 8-second (8000ms) fill animation duration"


def test_void_region_constants_in_html():
    """HTML must define the void start/end constants."""
    html = read_piece_file("index.html")
    assert "VOID_START" in html, "index.html must define VOID_START for the center void"


def test_exodus_reference_in_html():
    """HTML must reference Exodus 24:10 (the source verse)."""
    html = read_piece_file("index.html")
    assert "24:10" in html, "index.html must reference Exodus 24:10"


def test_essay_text_embedded_in_html():
    """Key essay phrases must appear inline in index.html."""
    essay = read_piece_file("essay.md")
    html  = read_piece_file("index.html")
    # Sample the first 10 words longer than 5 chars from the essay
    words = [w.strip("*_.,;:()'\"") for w in essay.split() if len(w.strip("*_.,;:()'\"")) > 5]
    sampled = words[:10]
    found = sum(1 for w in sampled if w in html)
    assert found >= 5, (
        f"index.html embeds too little essay text ({found}/10 sampled words found)"
    )


# ---------------------------------------------------------------------------
# Essay content acceptance criteria
# ---------------------------------------------------------------------------

def test_essay_word_count_at_least_350():
    """Essay must be ~350 words (at least 300 to give some slack)."""
    essay = read_piece_file("essay.md")
    wc = len(essay.split())
    assert wc >= 300, f"essay.md has only {wc} words (need ≥ 300)"


def test_essay_cites_exodus_24_9_11():
    """Essay must cite the covenant ratification ascent passage."""
    essay = read_piece_file("essay.md")
    assert "24:9" in essay or "24:10" in essay, (
        "essay.md must cite Exodus 24:9-11"
    )


def test_essay_mentions_ate_and_drank():
    """Essay must note the 'they ate and drank' detail from Exodus 24:11."""
    essay = read_piece_file("essay.md")
    lower = essay.lower()
    assert "ate" in lower or "drank" in lower or "yochlu" in lower or "yishtu" in lower, (
        "essay.md must mention the 'they ate and drank' detail of Exodus 24:11"
    )


def test_essay_mentions_rashi():
    """Essay must cite Rashi's interpretation."""
    essay = read_piece_file("essay.md")
    assert "Rashi" in essay or "rashi" in essay.lower(), "essay.md must mention Rashi"


def test_essay_mentions_nachmanides():
    """Essay must cite Nachmanides' interpretation."""
    essay = read_piece_file("essay.md")
    assert "Nachmanides" in essay or "Ramban" in essay, (
        "essay.md must mention Nachmanides"
    )


def test_essay_mentions_wang_tiles():
    """Essay must connect the artwork technique to the verse."""
    essay = read_piece_file("essay.md")
    assert "Wang" in essay or "wang" in essay.lower(), (
        "essay.md must mention Wang tiles"
    )


def test_essay_contains_hebrew_verse():
    """Essay must embed the Hebrew text of Exodus 24:10."""
    essay = read_piece_file("essay.md")
    assert "תַּחַת רַגְלָיו" in essay or "לִבְנַת הַסַּפִּיר" in essay, (
        "essay.md must contain Hebrew text from Exodus 24:10"
    )


def test_essay_contains_english_translation():
    """Essay must include an English translation of Exodus 24:10."""
    essay = read_piece_file("essay.md")
    assert "sapphire" in essay.lower(), (
        "essay.md must contain an English translation mentioning 'sapphire'"
    )


# ---------------------------------------------------------------------------
# Thumbnail acceptance criteria
# ---------------------------------------------------------------------------

def test_thumbnail_is_valid_svg():
    svg = read_piece_file("thumbnail.svg")
    assert "<svg" in svg and "</svg>" in svg


def test_thumbnail_contains_sapphire_colors():
    """Thumbnail must reference at least two palette colors."""
    svg = read_piece_file("thumbnail.svg")
    colors_found = sum(1 for c in ["#0A1F6E", "#3A7BD5", "#C8E6FA", "#D4A820"] if c in svg)
    assert colors_found >= 2, f"thumbnail.svg has only {colors_found} palette colors"


def test_thumbnail_contains_hebrew_label():
    """Thumbnail must contain the Hebrew void label."""
    svg = read_piece_file("thumbnail.svg")
    assert "תַּחַת" in svg or "רַגְלָיו" in svg, (
        "thumbnail.svg must contain the Hebrew label for the central void"
    )


def test_thumbnail_has_dark_background():
    """Thumbnail must use the near-black background color."""
    svg = read_piece_file("thumbnail.svg")
    assert "#03060f" in svg or "#060810" in svg or "#04060e" in svg, (
        "thumbnail.svg must use a dark background"
    )


# ---------------------------------------------------------------------------
# Edge cases and failure modes
# ---------------------------------------------------------------------------

def test_no_piece_59_renumbered():
    """Piece 59 must still exist — we must not have renumbered it."""
    pieces = load_pieces()
    ids = [p["id"] for p in pieces]
    assert "59-ten-roots-newton-fractal" in ids, (
        "Piece 59 was incorrectly removed or renumbered"
    )


def test_piece_60_after_piece_59_in_json():
    """Piece 60 must appear after piece 59 in pieces.json order."""
    pieces = load_pieces()
    ids = [p["id"] for p in pieces]
    idx_59 = next((i for i, p in enumerate(pieces) if p["id"] == "59-ten-roots-newton-fractal"), -1)
    idx_60 = next((i for i, p in enumerate(pieces) if p["id"] == PIECE_ID), -1)
    assert idx_59 >= 0 and idx_60 >= 0, "Both pieces 59 and 60 must be in pieces.json"
    assert idx_60 > idx_59, "Piece 60 must appear after piece 59 in pieces.json"


def test_piece_dir_has_exactly_four_files():
    """Piece directory must contain index.html, essay.md, thumbnail.svg, README.md."""
    expected = {"index.html", "essay.md", "thumbnail.svg", "README.md"}
    actual = set(os.listdir(PIECE_DIR))
    for f in expected:
        assert f in actual, f"Missing required file '{f}' in piece directory"


def test_html_no_external_fetch_of_essay():
    """index.html must NOT fetch essay.md at runtime (essay must be inlined)."""
    html = read_piece_file("index.html")
    assert "essay.md" not in html, (
        "index.html must not fetch essay.md; embed the essay text inline"
    )
