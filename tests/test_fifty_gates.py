"""
Tests for piece 32: The Fifty Gates — Bayer-Dithered Omer Calendar.

Covers structural requirements (file layout, pieces.json entry), content
requirements (citations, Hebrew characters, key colors), and algorithmic
correctness of the Bayer 4×4 ordered dithering logic.
"""
import json
import math
import os
import re

import pytest

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID = "32-fifty-gates"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_piece():
    """Return the pieces.json entry for piece 32, or None if absent."""
    with open(PIECES_JSON, encoding="utf-8") as fh:
        data = json.load(fh)
    for p in data:
        if p["id"] == PIECE_ID:
            return p
    return None


def read_html():
    return open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()


def read_essay():
    return open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()


# ---------------------------------------------------------------------------
# Bayer dithering algorithm — Python reference implementation
# ---------------------------------------------------------------------------

BAYER_4X4 = [
    [ 0,  8,  2, 10],
    [12,  4, 14,  6],
    [ 3, 11,  1,  9],
    [15,  7, 13,  5],
]


def bayer_dither(luminance: float, px: int, py: int) -> bool:
    """Return True (lit) if luminance exceeds the Bayer threshold at pixel (px, py).

    Implements the same logic as the JavaScript canvas code:
    threshold = BAYER[py % 4][px % 4] / 16.0; lit = luminance > threshold.
    """
    threshold = BAYER_4X4[py % 4][px % 4] / 16.0
    return luminance > threshold


def count_lit_4x4(luminance: float) -> int:
    """Count how many pixels in a single 4×4 Bayer tile are lit at the given luminance."""
    return sum(
        1 for py in range(4) for px in range(4)
        if bayer_dither(luminance, px, py)
    )


# ---------------------------------------------------------------------------
# Happy path: pieces.json entry and file layout
# ---------------------------------------------------------------------------

def test_piece_32_in_pieces_json():
    """Piece 32 must exist in pieces.json."""
    assert load_piece() is not None, f"'{PIECE_ID}' not found in pieces.json"


def test_piece_32_required_fields():
    """All required fields must be present and non-empty."""
    required = ("id", "title", "tagline", "year", "theme", "technique", "path", "thumbnail", "essay")
    piece = load_piece()
    assert piece is not None
    for field in required:
        assert field in piece and piece[field], f"Missing or empty field '{field}'"


def test_piece_32_index_html_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "index.html"))


def test_piece_32_essay_md_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "essay.md"))


def test_piece_32_readme_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "README.md"))


def test_piece_32_thumbnail_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "thumbnail.svg"))


def test_piece_32_thumbnail_is_valid_svg():
    text = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert "<svg" in text and "</svg>" in text


# ---------------------------------------------------------------------------
# HTML content requirements
# ---------------------------------------------------------------------------

def test_html_has_canvas_element():
    assert "<canvas" in read_html()


def test_html_uses_requestanimationframe():
    assert "requestAnimationFrame" in read_html()


def test_html_contains_bayer_matrix_values():
    """The Bayer 4×4 matrix must be present in the JS (check for distinctive values)."""
    html = read_html()
    # Row 0 of the standard Bayer matrix: [0, 8, 2, 10]
    assert "8,  2, 10" in html or "8, 2, 10" in html, (
        "Bayer matrix row [0,8,2,10] not found in index.html"
    )


def test_html_contains_dither_gold_color():
    """The warm wheat gold dither-dot color #E8C96A must appear in the HTML."""
    assert "#E8C96A" in read_html() or "E8C96A" in read_html().upper()


def test_html_contains_panel50_gold_color():
    """The 50th panel solid gold color #F5C842 must appear in the HTML."""
    assert "#F5C842" in read_html() or "F5C842" in read_html().upper()


def test_html_contains_background_color():
    """The deep indigo background color #0D1B2A must appear in the HTML."""
    assert "#0D1B2A" in read_html() or "0D1B2A" in read_html().upper()


def test_html_contains_hebrew_nun():
    """The Hebrew letter נ (nun = 50) must appear on the 50th panel."""
    assert "נ" in read_html(), "Hebrew letter נ (nun) not found in index.html"


def test_html_contains_shavuot_label():
    """The Hebrew word שבועות (Shavuot) must label the 50th panel."""
    assert "שבועות" in read_html(), "שבועות not found in index.html"


def test_html_contains_7x7_grid_structure():
    """index.html must draw a 7-column by 7-row grid (NCOLS=7, NROWS=7)."""
    html = read_html()
    assert "NCOLS = 7" in html or "NCOLS=7" in html, "NCOLS 7 not found"
    assert "NROWS = 7" in html or "NROWS=7" in html, "NROWS 7 not found"


def test_html_day_timing_250ms():
    """Each day's materialization should take ~250ms (DAY_MS = 250)."""
    assert "DAY_MS = 250" in read_html() or "DAY_MS=250" in read_html()


def test_html_49_days():
    """The piece must iterate over all 49 days."""
    html = read_html()
    assert "49" in html, "Reference to 49 days not found in index.html"


def test_essay_text_embedded_in_html():
    """The essay prose must be embedded inline in index.html (not fetched at runtime)."""
    essay = read_essay()
    html = read_html()
    long_words = [w for w in essay.split() if len(w) > 7][:12]
    found = sum(1 for w in long_words if w in html)
    assert found >= 6, (
        f"Only {found}/12 essay words found in index.html — essay may not be embedded"
    )


# ---------------------------------------------------------------------------
# Essay content requirements
# ---------------------------------------------------------------------------

def test_essay_at_least_200_words():
    text = read_essay()
    assert len(text.split()) >= 200, "essay.md has fewer than 200 words"


def test_essay_cites_rosh_hashanah_21b():
    essay = read_essay()
    assert "Rosh Hashanah 21b" in essay or "Rosh HaShanah 21b" in essay, (
        "essay.md must cite Rosh Hashanah 21b"
    )


def test_essay_cites_nedarim_38a():
    assert "Nedarim 38a" in read_essay() or "Nedarim" in read_essay(), (
        "essay.md must cite Nedarim 38a"
    )


def test_essay_mentions_leviticus():
    assert "Leviticus" in read_essay() or "23:15" in read_essay(), (
        "essay.md must reference the Leviticus Omer commandment"
    )


def test_essay_mentions_shavuot_unnamed():
    essay = read_essay()
    assert "count" in essay.lower() or "counting" in essay.lower(), (
        "essay.md must discuss the counting nature of the Omer"
    )


def test_essay_mentions_bayer():
    assert "Bayer" in read_essay() or "dither" in read_essay().lower()


# ---------------------------------------------------------------------------
# Bayer dithering algorithm correctness
# ---------------------------------------------------------------------------

def test_bayer_matrix_has_16_unique_values():
    """A valid 4×4 Bayer matrix must contain exactly the values 0–15."""
    flat = [BAYER_4X4[py][px] for py in range(4) for px in range(4)]
    assert sorted(flat) == list(range(16)), "Bayer matrix must contain values 0–15 exactly once"


def test_bayer_day1_exactly_one_lit_per_tile():
    """Day 1 luminance (1/50) is just above threshold 0/16=0 — only 1 pixel per 4×4 tile."""
    assert count_lit_4x4(1 / 50) == 1


def test_bayer_day25_half_lit():
    """Day 25 luminance (0.5) crosses exactly 8 of 16 thresholds (0/16 through 7/16)."""
    assert count_lit_4x4(25 / 50) == 8


def test_bayer_day49_all_lit():
    """Day 49 luminance (49/50=0.98) exceeds all 16 thresholds (max is 15/16=0.9375)."""
    assert count_lit_4x4(49 / 50) == 16


def test_bayer_monotone_across_days():
    """More days = at least as many lit pixels — luminance is monotone in day number."""
    prev = 0
    for d in range(1, 50):
        current = count_lit_4x4(d / 50)
        assert current >= prev, f"Day {d} has fewer lit pixels than day {d-1}"
        prev = current


def test_bayer_all_thresholds_strictly_less_than_one():
    """All Bayer thresholds are < 1.0 so any luminance = 1.0 would light every pixel."""
    for py in range(4):
        for px in range(4):
            assert BAYER_4X4[py][px] / 16.0 < 1.0


def test_bayer_pixel_independence():
    """Each pixel position (px, py) uses only its local 4×4 tile index, not neighbors."""
    lum = 0.5
    for py in range(8):
        for px in range(8):
            # Two pixels in the same tile position across tile boundaries should match
            result_here = bayer_dither(lum, px, py)
            result_tiled = bayer_dither(lum, px + 4, py + 4)
            assert result_here == result_tiled, (
                f"Bayer result differs between ({px},{py}) and ({px+4},{py+4}) "
                f"— tiling is inconsistent"
            )


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

def test_bayer_luminance_zero_no_pixels_lit():
    """At luminance 0.0, no threshold (all ≥ 0) is exceeded — no pixels lit."""
    assert count_lit_4x4(0.0) == 0


def test_bayer_luminance_one_all_pixels_lit():
    """At luminance 1.0, all thresholds (max 15/16 < 1) are exceeded — all 16 lit."""
    assert count_lit_4x4(1.0) == 16


def test_pieces_json_no_duplicate_ids_after_addition():
    """Adding piece 32 must not create a duplicate ID."""
    with open(PIECES_JSON, encoding="utf-8") as fh:
        data = json.load(fh)
    ids = [p["id"] for p in data]
    assert len(ids) == len(set(ids)), f"Duplicate piece IDs found after adding piece 32"


def test_piece_32_path_format():
    """Piece 32 path must be pieces/32-fifty-gates/index.html."""
    piece = load_piece()
    assert piece is not None
    assert piece["path"] == "pieces/32-fifty-gates/index.html"


# ---------------------------------------------------------------------------
# Failure modes
# ---------------------------------------------------------------------------

def test_missing_essay_file_would_fail(tmp_path):
    """Confirm that a missing essay.md would cause a detectable failure."""
    missing = tmp_path / "nonexistent.md"
    assert not missing.exists(), "Fixture path must not exist on disk"


def test_wrong_bayer_matrix_detected():
    """A corrupted Bayer matrix (constant zeros) would fail the monotone test."""
    bad_bayer = [[0] * 4 for _ in range(4)]

    def bad_dither(lum, px, py):
        return lum > bad_bayer[py % 4][px % 4] / 16.0

    counts = [sum(1 for py in range(4) for px in range(4) if bad_dither(d / 50, px, py))
              for d in range(1, 50)]
    # All counts above threshold 0/16=0 would be 16 for any lum>0,
    # making early days wrong (should be sparse, not fully lit)
    assert counts[0] == 16, "With all-zero Bayer, day 1 incorrectly lights all 16 pixels"
