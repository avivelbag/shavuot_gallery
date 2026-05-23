"""
Tests for piece 92-saw-sefirat-haomer: Forty-Nine Steps That Do Not Return.

Covers the acceptance criteria from the suggestion:
  - Piece directory and all required files exist.
  - pieces.json entry has the correct fields (theme, technique, id).
  - index.html embeds the SAW animation with required constants and features.
  - essay.md is substantial and contains key thematic content.
  - thumbnail.svg is valid SVG with the required visual elements.
"""
import json
import os
import re

import pytest

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID = "92-saw-sefirat-haomer"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_pieces():
    """Return parsed pieces.json list."""
    with open(PIECES_JSON, encoding="utf-8") as fh:
        return json.load(fh)


def get_piece():
    """Return the pieces.json entry for this piece, or None."""
    return next((p for p in load_pieces() if p["id"] == PIECE_ID), None)


def read_file(rel_path):
    """Read a file relative to GALLERY_ROOT and return its text."""
    return open(os.path.join(GALLERY_ROOT, rel_path), encoding="utf-8").read()


# ---------------------------------------------------------------------------
# Happy path: file layout
# ---------------------------------------------------------------------------

def test_piece_directory_exists():
    assert os.path.isdir(PIECE_DIR), f"Piece directory missing: {PIECE_DIR}"


def test_index_html_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "index.html")), "index.html missing"


def test_essay_md_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "essay.md")), "essay.md missing"


def test_thumbnail_svg_exists():
    path = os.path.join(PIECE_DIR, "thumbnail.svg")
    assert os.path.isfile(path), "thumbnail.svg missing"


def test_readme_md_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "README.md")), "README.md missing"


# ---------------------------------------------------------------------------
# Happy path: pieces.json registration
# ---------------------------------------------------------------------------

def test_piece_in_pieces_json():
    assert get_piece() is not None, f"'{PIECE_ID}' not found in pieces.json"


def test_pieces_json_theme():
    piece = get_piece()
    assert piece is not None
    assert "Sefirat HaOmer" in piece["theme"], (
        f"theme must mention 'Sefirat HaOmer', got: {piece['theme']!r}"
    )


def test_pieces_json_technique():
    piece = get_piece()
    assert piece is not None
    tech = piece["technique"].lower()
    assert "self-avoiding" in tech or "saw" in tech, (
        f"technique must mention 'self-avoiding' or 'SAW', got: {piece['technique']!r}"
    )


def test_pieces_json_paths_exist():
    piece = get_piece()
    assert piece is not None
    for field in ("path", "thumbnail", "essay"):
        full = os.path.join(GALLERY_ROOT, piece[field])
        assert os.path.isfile(full), f"'{field}' file missing: {piece[field]}"


def test_pieces_json_year_is_int():
    piece = get_piece()
    assert piece is not None
    assert isinstance(piece["year"], int), "year must be an integer"


def test_pieces_json_no_duplicate_ids():
    pieces = load_pieces()
    ids = [p["id"] for p in pieces]
    assert len(ids) == len(set(ids)), "Duplicate piece IDs in pieces.json"


# ---------------------------------------------------------------------------
# Happy path: index.html animation requirements
# ---------------------------------------------------------------------------

def test_index_html_has_step_interval_constant():
    html = read_file(f"pieces/{PIECE_ID}/index.html")
    assert "STEP_INTERVAL_MS" in html, "index.html must define STEP_INTERVAL_MS constant"


def test_index_html_step_interval_is_1000():
    html = read_file(f"pieces/{PIECE_ID}/index.html")
    assert re.search(r'STEP_INTERVAL_MS\s*=\s*1000', html), (
        "STEP_INTERVAL_MS must be set to 1000"
    )


def test_index_html_total_steps_49():
    html = read_file(f"pieces/{PIECE_ID}/index.html")
    assert re.search(r'TOTAL_STEPS\s*=\s*49', html), (
        "index.html must define TOTAL_STEPS = 49"
    )


def test_index_html_uses_canvas():
    html = read_file(f"pieces/{PIECE_ID}/index.html")
    assert "<canvas" in html, "index.html must contain a <canvas> element"


def test_index_html_navy_background():
    html = read_file(f"pieces/{PIECE_ID}/index.html")
    assert "#0D1B2A" in html or "#0d1b2a" in html.lower(), (
        "index.html must use navy background #0D1B2A"
    )


def test_index_html_has_backtracking_dfs():
    html = read_file(f"pieces/{PIECE_ID}/index.html")
    assert "dfs" in html or "DFS" in html, (
        "index.html must implement a depth-first search (dfs) backtracking SAW generator"
    )


def test_index_html_has_hebrew_day_labels():
    html = read_file(f"pieces/{PIECE_ID}/index.html")
    assert "יום א" in html or "HEBREW_DAYS" in html, (
        "index.html must define Hebrew day labels"
    )


def test_index_html_has_yom_hamishim():
    html = read_file(f"pieces/{PIECE_ID}/index.html")
    assert "יום חמישים" in html, (
        "index.html must display 'יום חמישים' on completion"
    )


def test_index_html_wheat_gold_color():
    html = read_file(f"pieces/{PIECE_ID}/index.html")
    assert "#D4A017" in html or "#d4a017" in html.lower(), (
        "index.html must use wheat gold #D4A017 for path segments"
    )


def test_index_html_uses_request_animation_frame():
    html = read_file(f"pieces/{PIECE_ID}/index.html")
    assert "requestAnimationFrame" in html, (
        "index.html must use requestAnimationFrame for animation"
    )


def test_index_html_has_glow_effect():
    html = read_file(f"pieces/{PIECE_ID}/index.html")
    assert "shadowBlur" in html or "shadow" in html.lower(), (
        "index.html must implement a glow effect for the path head"
    )


def test_index_html_embeds_essay_words():
    """Key essay words must appear in the HTML (not fetched at runtime)."""
    essay = read_file(f"pieces/{PIECE_ID}/essay.md")
    html = read_file(f"pieces/{PIECE_ID}/index.html")
    words = [w for w in essay.split() if len(w) > 6][:10]
    found = sum(1 for w in words if w in html)
    assert found >= 5, (
        f"index.html must embed essay text inline (only {found}/10 sampled words found)"
    )


# ---------------------------------------------------------------------------
# Happy path: essay.md content
# ---------------------------------------------------------------------------

def test_essay_word_count():
    essay = read_file(f"pieces/{PIECE_ID}/essay.md")
    count = len(essay.split())
    assert count >= 300, f"essay.md has only {count} words (expected ≥ 300)"


def test_essay_contains_leviticus_reference():
    essay = read_file(f"pieces/{PIECE_ID}/essay.md")
    lower = essay.lower()
    assert "leviticus" in lower or "23:15" in essay, (
        "essay.md must reference Leviticus 23:15-16"
    )


def test_essay_contains_self_avoiding_walk():
    essay = read_file(f"pieces/{PIECE_ID}/essay.md")
    lower = essay.lower()
    assert "self-avoiding" in lower, "essay.md must mention the self-avoiding walk"


def test_essay_contains_shulchan_aruch():
    essay = read_file(f"pieces/{PIECE_ID}/essay.md")
    assert "Shulchan Aruch" in essay or "Orach Chaim" in essay, (
        "essay.md must reference the Shulchan Aruch ruling on missed days"
    )


def test_essay_contains_sefirot():
    essay = read_file(f"pieces/{PIECE_ID}/essay.md")
    lower = essay.lower()
    assert "sefirot" in lower or "sefir" in lower, (
        "essay.md must mention Kabbalistic sefirot tradition"
    )


# ---------------------------------------------------------------------------
# Happy path: thumbnail.svg
# ---------------------------------------------------------------------------

def test_thumbnail_is_valid_svg():
    svg = read_file(f"pieces/{PIECE_ID}/thumbnail.svg")
    assert "<svg" in svg and "</svg>" in svg, "thumbnail.svg must be valid SVG"


def test_thumbnail_has_navy_background():
    svg = read_file(f"pieces/{PIECE_ID}/thumbnail.svg")
    assert "#0D1B2A" in svg or "#0d1b2a" in svg.lower(), (
        "thumbnail.svg must include navy background #0D1B2A"
    )


def test_thumbnail_has_polyline_path():
    svg = read_file(f"pieces/{PIECE_ID}/thumbnail.svg")
    assert "<polyline" in svg, "thumbnail.svg must contain a <polyline> for the SAW path"


def test_thumbnail_has_hebrew_labels():
    svg = read_file(f"pieces/{PIECE_ID}/thumbnail.svg")
    assert "מ״ט" in svg or "נ" in svg, (
        "thumbnail.svg must include Hebrew numerals (מ״ט and/or נ)"
    )


def test_thumbnail_400x400():
    svg = read_file(f"pieces/{PIECE_ID}/thumbnail.svg")
    assert 'width="400"' in svg and 'height="400"' in svg, (
        "thumbnail.svg must be 400x400"
    )


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

def test_index_html_has_cell_size_constant():
    """CELL constant should be defined so the lattice is configurable."""
    html = read_file(f"pieces/{PIECE_ID}/index.html")
    assert re.search(r'CELL\s*=\s*\d+', html), (
        "index.html must define a CELL size constant for the lattice grid"
    )


def test_essay_contains_polymer_reference():
    """The polymer physics connection must be in the essay."""
    essay = read_file(f"pieces/{PIECE_ID}/essay.md")
    lower = essay.lower()
    assert "polymer" in lower or "molecule" in lower, (
        "essay.md must explain the polymer physics connection to SAWs"
    )


def test_pieces_json_tagline_non_empty():
    piece = get_piece()
    assert piece is not None
    assert piece.get("tagline", "").strip(), "tagline must be non-empty"


# ---------------------------------------------------------------------------
# Failure modes
# ---------------------------------------------------------------------------

def test_missing_piece_id_not_in_other_entry():
    """No other piece should claim the 92-saw-sefirat-haomer directory."""
    pieces = load_pieces()
    others = [p for p in pieces if p["id"] != PIECE_ID]
    for p in others:
        assert "92-saw-sefirat-haomer" not in p.get("path", ""), (
            f"Another piece '{p['id']}' incorrectly references the saw directory"
        )


def test_essay_does_not_exceed_reasonable_length():
    """Essay should not be a stub (< 100 words) but also not pathologically large."""
    essay = read_file(f"pieces/{PIECE_ID}/essay.md")
    count = len(essay.split())
    assert 100 <= count <= 3000, (
        f"essay.md word count ({count}) is outside expected range [100, 3000]"
    )


def test_index_html_canvas_has_id():
    """The canvas element must have an id so JS can reference it."""
    html = read_file(f"pieces/{PIECE_ID}/index.html")
    assert re.search(r'<canvas[^>]+id\s*=', html), (
        "The <canvas> element must have an id attribute"
    )
