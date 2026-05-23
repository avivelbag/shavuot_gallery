"""
Tests for the Rule 110 / Oral Torah piece (92-rule110-oral-torah).

Covers:
- Rule 110 algorithm correctness
- Piece directory structure and required files
- index.html content requirements
- Essay content
- Thumbnail SVG validity
- pieces.json registration
- Edge cases and failure modes
"""
import json
import os
import re

import pytest

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID = "92-rule110-oral-torah"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
INDEX_HTML = os.path.join(PIECE_DIR, "index.html")
ESSAY_MD = os.path.join(PIECE_DIR, "essay.md")
THUMBNAIL_SVG = os.path.join(PIECE_DIR, "thumbnail.svg")
README_MD = os.path.join(PIECE_DIR, "README.md")
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")


# ---------------------------------------------------------------------------
# Rule 110 algorithm (pure Python mirror of the JS implementation)
# ---------------------------------------------------------------------------

RULE = 110


def next_cell(left, center, right):
    """Apply Rule 110 to a 3-cell neighborhood."""
    idx = (left << 2) | (center << 1) | right
    return (RULE >> idx) & 1


def compute_rule110(initial_row, num_generations):
    """
    Compute num_generations steps of Rule 110 starting from initial_row.

    Returns a list of rows (each a list of ints), including the initial row
    as generation 0.
    """
    W = len(initial_row)
    rows = [list(initial_row)]
    for _ in range(num_generations):
        prev = rows[-1]
        curr = [
            next_cell(prev[(c - 1) % W], prev[c], prev[(c + 1) % W])
            for c in range(W)
        ]
        rows.append(curr)
    return rows


# ---------------------------------------------------------------------------
# Rule 110 correctness tests
# ---------------------------------------------------------------------------

def test_rule110_all_zeros_stays_zero():
    """000 -> 0: an all-zero row stays all-zero."""
    row = [0] * 20
    result = compute_rule110(row, 5)
    for gen in result:
        assert all(c == 0 for c in gen), "All-zero row should remain all-zero"


def test_rule110_single_cell_known_output():
    """
    Rule 110 starting from a single center cell produces a known first few
    generations.  Verified against the canonical Rule 110 table:
      gen 0: ...010...
      gen 1: ...011...  (neighbors 0,1,0 -> idx 2 -> bit 2 of 110 = 1;
                          neighbors 0,0,1 -> idx 1 -> bit 1 of 110 = 1)
    """
    W = 11
    row0 = [0] * W
    row0[W // 2] = 1
    rows = compute_rule110(row0, 3)

    assert rows[0][W // 2] == 1
    assert all(rows[0][c] == 0 for c in range(W) if c != W // 2)

    center = W // 2
    # neighborhood at center: (0,1,0)=idx 2 -> bit 2 of 110 = 1
    assert rows[1][center] == 1
    # neighborhood at center-1: (0,0,1)=idx 1 -> bit 1 of 110 = 1
    assert rows[1][center - 1] == 1
    # neighborhood at center+1: (1,0,0)=idx 4 -> bit 4 of 110 = 0
    assert rows[1][center + 1] == 0


def test_rule110_neighborhood_table():
    """Every entry in the Rule 110 lookup table is correct."""
    expected = {
        (0, 0, 0): 0,
        (0, 0, 1): 1,
        (0, 1, 0): 1,
        (0, 1, 1): 1,
        (1, 0, 0): 0,
        (1, 0, 1): 1,
        (1, 1, 0): 1,
        (1, 1, 1): 0,
    }
    for (l, c, r), expected_out in expected.items():
        assert next_cell(l, c, r) == expected_out, (
            f"next_cell({l},{c},{r}) = {next_cell(l,c,r)}, expected {expected_out}"
        )


def test_rule110_nontrivial_growth():
    """After 50 generations, the pattern has grown beyond the seed column."""
    W = 200
    row0 = [0] * W
    row0[W // 2] = 1
    rows = compute_rule110(row0, 50)
    final = rows[-1]
    on_cells = sum(final)
    assert on_cells > 5, "Rule 110 from single seed should produce many ON cells after 50 generations"


def test_rule110_does_not_have_simple_period():
    """Rule 110 should NOT be a simple all-zeros or all-ones periodic attractor."""
    W = 100
    row0 = [0] * W
    row0[W // 2] = 1
    rows = compute_rule110(row0, 100)
    final = rows[-1]
    assert not all(c == 0 for c in final), "Rule 110 should not collapse to all zeros"
    assert not all(c == 1 for c in final), "Rule 110 should not collapse to all ones"


def test_rule110_wrap_around_boundary():
    """Boundary cells wrap around (periodic boundary conditions)."""
    W = 10
    row0 = [0] * W
    row0[0] = 1
    rows = compute_rule110(row0, 1)
    left_of_0 = row0[W - 1]
    center_0 = row0[0]
    right_of_0 = row0[1]
    expected = next_cell(left_of_0, center_0, right_of_0)
    assert rows[1][0] == expected


# ---------------------------------------------------------------------------
# Directory structure and file existence
# ---------------------------------------------------------------------------

def test_piece_directory_exists():
    assert os.path.isdir(PIECE_DIR), f"Piece directory not found: {PIECE_DIR}"


def test_index_html_exists():
    assert os.path.isfile(INDEX_HTML), "index.html missing from piece directory"


def test_essay_md_exists():
    assert os.path.isfile(ESSAY_MD), "essay.md missing from piece directory"


def test_thumbnail_svg_exists():
    assert os.path.isfile(THUMBNAIL_SVG), "thumbnail.svg missing from piece directory"


def test_readme_md_exists():
    assert os.path.isfile(README_MD), "README.md missing from piece directory"


# ---------------------------------------------------------------------------
# index.html content tests
# ---------------------------------------------------------------------------

def _load_html():
    return open(INDEX_HTML, encoding="utf-8").read()


def test_index_html_has_canvas():
    html = _load_html()
    assert "<canvas" in html, "index.html must contain a <canvas> element"


def test_index_html_uses_rule_110():
    html = _load_html()
    assert "110" in html, "index.html must reference Rule 110"


def test_index_html_has_on_color_indigo():
    """ON cells must use #1C1864 (deep indigo)."""
    html = _load_html()
    assert "1C1864" in html or "1c1864" in html, (
        "index.html must reference the indigo ON-cell color #1C1864"
    )


def test_index_html_has_off_color_parchment():
    """OFF cells must use #F5EDD6 (warm parchment)."""
    html = _load_html()
    assert "F5EDD6" in html or "f5edd6" in html, (
        "index.html must reference the parchment OFF-cell color #F5EDD6"
    )


def test_index_html_has_dor_ldor_overlay():
    """The Hebrew dor l'dor text must appear in the HTML."""
    html = _load_html()
    assert "דּוֹר" in html or "דּוֹר" in html or "דור" in html, (
        "index.html must contain the Hebrew dor l'dor overlay text"
    )


def test_index_html_overlay_color_gold():
    """Overlay must use gold color #C8941A."""
    html = _load_html()
    assert "C8941A" in html or "c8941a" in html, (
        "index.html must reference the gold overlay color #C8941A"
    )


def test_index_html_has_setinterval_or_raf():
    """Animation must use setInterval or requestAnimationFrame."""
    html = _load_html()
    assert "setInterval" in html or "requestAnimationFrame" in html, (
        "index.html must use setInterval or requestAnimationFrame for animation"
    )


def test_index_html_has_cell_size_4():
    """Cell size must be 4 pixels."""
    html = _load_html()
    assert "CELL_SIZE = 4" in html or "cellSize = 4" in html or "CELL_SIZE=4" in html, (
        "index.html must define cellSize = 4"
    )


def test_index_html_has_ring_buffer():
    """The ring buffer pattern (head pointer) must be present."""
    html = _load_html()
    assert "head" in html, "index.html must implement a ring buffer with a 'head' pointer"


def test_index_html_embeds_essay_words():
    """At least 5 of the first 10 long essay words must appear in the HTML."""
    essay_text = open(ESSAY_MD, encoding="utf-8").read()
    html = _load_html()
    words = [w for w in essay_text.split() if len(w) > 5][:10]
    found = sum(1 for w in words if w in html)
    assert found >= 5, (
        f"index.html must embed essay text; only {found}/10 sampled words found"
    )


# ---------------------------------------------------------------------------
# Essay content tests
# ---------------------------------------------------------------------------

def test_essay_min_word_count():
    text = open(ESSAY_MD, encoding="utf-8").read()
    word_count = len(text.split())
    assert word_count >= 400, f"Essay has {word_count} words; must have at least 400"


def test_essay_mentions_oral_torah():
    text = open(ESSAY_MD, encoding="utf-8").read().lower()
    assert "oral torah" in text, "Essay must mention the Oral Torah"


def test_essay_mentions_written_torah():
    text = open(ESSAY_MD, encoding="utf-8").read().lower()
    assert "written torah" in text or "she-bikhsav" in text or "bikhsav" in text, (
        "Essay must mention the Written Torah"
    )


def test_essay_mentions_turing_complete():
    text = open(ESSAY_MD, encoding="utf-8").read().lower()
    assert "turing" in text, "Essay must mention Turing-completeness"


def test_essay_mentions_sinai_source():
    text = open(ESSAY_MD, encoding="utf-8").read()
    assert "Peah" in text or "Avot" in text or "Sinai" in text, (
        "Essay must cite a rabbinic source relating to Sinai / Oral Torah"
    )


def test_essay_mentions_wolfram_or_cook():
    text = open(ESSAY_MD, encoding="utf-8").read()
    assert "Wolfram" in text or "Cook" in text, (
        "Essay must mention Wolfram or Cook in connection with Rule 110 universality"
    )


# ---------------------------------------------------------------------------
# Thumbnail SVG tests
# ---------------------------------------------------------------------------

def test_thumbnail_is_valid_svg():
    text = open(THUMBNAIL_SVG, encoding="utf-8").read()
    assert "<svg" in text and "</svg>" in text, "thumbnail.svg does not look like valid SVG"


def test_thumbnail_has_viewbox_400():
    text = open(THUMBNAIL_SVG, encoding="utf-8").read()
    assert "400" in text, "thumbnail.svg must be 400×400"


def test_thumbnail_has_indigo_cells():
    text = open(THUMBNAIL_SVG, encoding="utf-8").read().lower()
    assert "1c1864" in text, "thumbnail.svg must use the indigo ON-cell color #1C1864"


def test_thumbnail_has_parchment_background():
    text = open(THUMBNAIL_SVG, encoding="utf-8").read().lower()
    assert "f5edd6" in text, "thumbnail.svg must use the parchment background #F5EDD6"


def test_thumbnail_has_hebrew_tav():
    text = open(THUMBNAIL_SVG, encoding="utf-8").read()
    assert "ת" in text or "05EA" in text or "#x05EA" in text or "05ea" in text, (
        "thumbnail.svg must contain the Hebrew letter tav (ת)"
    )


def test_thumbnail_has_on_cells():
    text = open(THUMBNAIL_SVG, encoding="utf-8").read()
    rect_count = text.count("<rect")
    assert rect_count >= 10, f"thumbnail.svg should have many rect elements; found {rect_count}"


# ---------------------------------------------------------------------------
# pieces.json registration tests
# ---------------------------------------------------------------------------

def _load_pieces():
    with open(PIECES_JSON, encoding="utf-8") as fh:
        return json.load(fh)


def _get_piece():
    for p in _load_pieces():
        if p["id"] == PIECE_ID:
            return p
    return None


def test_piece_in_pieces_json():
    assert _get_piece() is not None, f"'{PIECE_ID}' not found in pieces.json"


def test_piece_theme_is_oral_torah():
    piece = _get_piece()
    assert piece is not None
    theme = piece.get("theme", "")
    assert "Oral Torah" in theme or "Matan Torah" in theme, (
        f"piece theme must reference Oral Torah or Matan Torah; got '{theme}'"
    )


def test_piece_technique_is_rule110():
    piece = _get_piece()
    assert piece is not None
    technique = piece.get("technique", "")
    assert "110" in technique or "Rule 110" in technique, (
        f"piece technique must reference Rule 110; got '{technique}'"
    )


def test_piece_path_points_to_existing_file():
    piece = _get_piece()
    assert piece is not None
    full_path = os.path.join(GALLERY_ROOT, piece["path"])
    assert os.path.isfile(full_path), f"piece path '{piece['path']}' does not exist"


def test_piece_thumbnail_points_to_existing_file():
    piece = _get_piece()
    assert piece is not None
    full_path = os.path.join(GALLERY_ROOT, piece["thumbnail"])
    assert os.path.isfile(full_path), f"piece thumbnail '{piece['thumbnail']}' does not exist"


def test_piece_essay_points_to_existing_file():
    piece = _get_piece()
    assert piece is not None
    full_path = os.path.join(GALLERY_ROOT, piece["essay"])
    assert os.path.isfile(full_path), f"piece essay '{piece['essay']}' does not exist"


# ---------------------------------------------------------------------------
# Edge cases and failure modes
# ---------------------------------------------------------------------------

def test_rule110_empty_grid_returns_empty_rows():
    """An empty 0-cell row produces empty-row generations without error."""
    rows = compute_rule110([], 1)
    assert len(rows) == 2
    assert rows[0] == []
    assert rows[1] == []


def test_rule110_single_cell_grid():
    """A 1-wide grid wraps: left = right = center. Pattern known from table."""
    row = [1]
    rows = compute_rule110(row, 3)
    assert rows[0] == [1]
    assert rows[1] == [next_cell(1, 1, 1)]


def test_rule110_large_grid_does_not_hang():
    """Computing 200 generations on a 500-wide grid should complete quickly."""
    W = 500
    row0 = [0] * W
    row0[W // 2] = 1
    rows = compute_rule110(row0, 200)
    assert len(rows) == 201
    assert len(rows[-1]) == W


def test_rule110_on_count_grows_then_stabilizes():
    """After many generations, Rule 110 should have a non-trivial density."""
    W = 200
    row0 = [0] * W
    row0[W // 2] = 1
    rows = compute_rule110(row0, 150)
    final_on = sum(rows[-1])
    assert 5 < final_on < W, (
        f"After 150 generations, ON count {final_on} should be between 5 and {W}"
    )


def test_no_duplicate_piece_ids():
    """Adding our piece must not create a duplicate ID."""
    pieces = _load_pieces()
    ids = [p["id"] for p in pieces]
    assert len(ids) == len(set(ids)), f"Duplicate piece IDs found after adding {PIECE_ID}"


def test_piece_year_is_2026():
    piece = _get_piece()
    assert piece is not None
    assert piece["year"] == 2026
