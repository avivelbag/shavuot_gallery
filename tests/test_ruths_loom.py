"""
Tests for piece 57-ruths-loom-woven-harvest (Ruth's Loom).

Validates the piece directory layout, pieces.json registration, canvas
animation mechanics (twill rule, color assignments), essay word count,
and the essay-in-HTML embedding requirement.
"""
import json
import math
import os
import re

import pytest

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID = "57-ruths-loom-woven-harvest"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _load_piece():
    """Return the pieces.json entry for this piece, or None if absent."""
    data = json.load(open(os.path.join(GALLERY_ROOT, "pieces.json"), encoding="utf-8"))
    for p in data:
        if p["id"] == PIECE_ID:
            return p
    return None


def _html():
    return open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()


def _essay():
    return open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()


# ---------------------------------------------------------------------------
# Happy path — pieces.json registration
# ---------------------------------------------------------------------------

def test_piece_registered_in_pieces_json():
    assert _load_piece() is not None, f"{PIECE_ID} not found in pieces.json"


def test_piece_theme_is_ruth_ketzir():
    piece = _load_piece()
    assert piece is not None
    assert "Ruth" in piece["theme"] or "Ketzir" in piece["theme"], (
        "theme must reference Book of Ruth / Ketzir"
    )


def test_piece_technique_mentions_weaving():
    piece = _load_piece()
    assert piece is not None
    assert "weav" in piece["technique"].lower(), (
        "technique field must mention weaving"
    )


def test_piece_year_is_integer():
    piece = _load_piece()
    assert piece is not None
    assert isinstance(piece["year"], int)


# ---------------------------------------------------------------------------
# Happy path — file layout
# ---------------------------------------------------------------------------

def test_index_html_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "index.html"))


def test_essay_md_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "essay.md"))


def test_thumbnail_svg_exists():
    thumb_path = os.path.join(PIECE_DIR, "thumbnail.svg")
    assert os.path.isfile(thumb_path)


def test_readme_md_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "README.md"))


# ---------------------------------------------------------------------------
# Happy path — essay substance
# ---------------------------------------------------------------------------

def test_essay_exceeds_350_words():
    """Acceptance criterion: essay.md is ≥350 words."""
    text = _essay()
    assert len(text.split()) >= 350, f"Essay has only {len(text.split())} words"


def test_essay_cites_ruth_2_2():
    """Essay must reference Ruth 2:2, the core verse of the gleaning scene."""
    text = _essay()
    assert "2:2" in text, "essay.md must cite Ruth 2:2"


def test_essay_cites_ruth_2_3():
    """Essay must reference Ruth 2:3 (ויקר מקרה / providential chance)."""
    text = _essay()
    assert "2:3" in text, "essay.md must cite Ruth 2:3"


def test_essay_mentions_peah_or_leket():
    """Essay must discuss the Halakhic institution of pe'ah / leket."""
    text = _essay().lower()
    assert "pe" in text and ("leket" in text or "glean" in text), (
        "essay.md must mention pe'ah and/or leket (gleaning law)"
    )


def test_essay_mentions_megillah_13a():
    """Essay must reference Megillah 13a (Talmudic reading of ויקר מקרה)."""
    text = _essay()
    assert "Megillah" in text and "13a" in text, (
        "essay.md must cite Megillah 13a for the providential reading of Ruth 2:3"
    )


def test_essay_mentions_leviticus_19():
    """Essay must cite Leviticus 19:9-10 for pe'ah / leket legal basis."""
    text = _essay()
    assert "Leviticus" in text and "19" in text, (
        "essay.md must reference Leviticus 19 as the halakhic source for gleaning"
    )


# ---------------------------------------------------------------------------
# Happy path — canvas animation mechanics in HTML
# ---------------------------------------------------------------------------

def test_html_uses_request_animation_frame():
    assert "requestAnimationFrame" in _html()


def test_html_canvas_is_700x700():
    html = _html()
    assert 'width="700"' in html and 'height="700"' in html, (
        "canvas must be 700×700 px"
    )


def test_html_defines_cols_175_rows_175():
    """The weave grid must be 175×175 threads at 4 px each."""
    html = _html()
    assert "COLS = 175" in html or "COLS=175" in html
    assert "ROWS = 175" in html or "ROWS=175" in html


def test_html_twill_rule_present():
    """The over-2-under-1 twill rule must use (col + row) % 3."""
    html = _html()
    assert "% 3" in html, "twill modulo-3 rule must be present in JS"


def test_html_warp_gold_color():
    assert "#D4A317" in _html(), "barley gold warp color missing from HTML"


def test_html_warp_olive_color():
    assert "#556B2F" in _html(), "deep olive warp color missing from HTML"


def test_html_warp_cream_color():
    assert "#F5E6B0" in _html(), "wheat cream warp color missing from HTML"


def test_html_weft_rose_madder():
    assert "#B5302A" in _html(), "rose madder weft color missing from HTML"


def test_html_weft_linen():
    assert "#E8D9B0" in _html(), "faded linen weft color missing from HTML"


def test_html_shabbat_weft_gold():
    """Every 7th weft row must use the bright gold Shabbat color."""
    assert "#F0C040" in _html(), "Shabbat gold weft color (#F0C040) missing"


def test_html_shabbat_row_uses_modulo_7():
    """The bright gold row is triggered by r % 7 === 0."""
    html = _html()
    assert "% 7" in html, "modulo-7 Shabbat row trigger missing from JS"


def test_html_weave_duration_12_seconds():
    """The animation must be timed to ~12 seconds."""
    html = _html()
    assert "12000" in html, "12 000 ms weave duration constant missing from JS"


def test_html_sway_amplitude_2px():
    """Sway displacement amplitude must be 2 px."""
    html = _html()
    assert re.search(r"\b2\s*\*\s*Math\.sin", html), (
        "sway amplitude expression '2 * Math.sin' missing from JS"
    )


def test_html_sway_period_3s():
    """Sway period must be 3 seconds (2π/3 angular frequency)."""
    html = _html()
    assert "2 * Math.PI / 3" in html or "2*Math.PI/3" in html, (
        "sway period 3 s (2π/3) expression missing from JS"
    )


def test_html_offscreen_canvas_used():
    """The sway phase must copy from an offscreen canvas for clean compositing."""
    html = _html()
    assert "createElement('canvas')" in html or 'createElement("canvas")' in html, (
        "offscreen canvas creation missing from JS"
    )


def test_html_draws_image_strips_for_sway():
    """Column-strip drawImage must be used to implement per-column sway shift."""
    assert "drawImage" in _html()


def test_html_hebrew_inscription_present():
    """The Hebrew verse reference must appear in the HTML."""
    html = _html()
    assert "רות" in html, "Hebrew inscription with 'רות' (Ruth) missing"


def test_html_essay_embedded_substantial():
    """At least 5 of the first 10 long words from essay.md appear in index.html."""
    essay_text = _essay()
    html = _html()
    words = [w for w in essay_text.split() if len(w) > 5]
    sampled = words[:10]
    found = sum(1 for w in sampled if w in html)
    assert found >= 5, (
        f"Only {found}/10 sampled essay words found in index.html — "
        "essay text must be embedded, not fetched at runtime"
    )


# ---------------------------------------------------------------------------
# Analytical verification of twill rule
# ---------------------------------------------------------------------------

def test_twill_rule_over_two_under_one():
    """Verify the twill rule: for any 3 consecutive columns in a row,
    exactly 2 cells show weft and 1 shows warp."""
    def is_over(col, row):
        return (col + row) % 3 != 0

    for row in range(10):
        for col_start in range(0, 12, 3):
            statuses = [is_over(col_start + c, row) for c in range(3)]
            over_count = sum(statuses)
            assert over_count == 2, (
                f"Row {row} cols {col_start}–{col_start+2}: expected 2 over, got {over_count}"
            )


def test_twill_rule_diagonal_rib():
    """The diagonal rib shifts left one column per row: if (c,r) is warp,
    then (c-1, r+1) is also warp. This holds because (c-1)+(r+1) = c+r."""
    def is_warp(col, row):
        return (col + row) % 3 == 0

    for row in range(20):
        for col in range(1, 21):  # col >= 1 ensures col-1 >= 0
            if is_warp(col, row):
                assert is_warp(col - 1, row + 1), (
                    f"Diagonal rib broken at ({col},{row}) → ({col-1},{row+1})"
                )


def test_shabbat_rows():
    """Every 7th row (0, 7, 14, ...) must be the gold Shabbat row."""
    shabbat_rows = [r for r in range(175) if r % 7 == 0]
    assert 0 in shabbat_rows
    assert 7 in shabbat_rows
    assert 14 in shabbat_rows
    assert len(shabbat_rows) == 25


def test_warp_color_assignment_irregular():
    """Warp colors must not be a simple repeating sequence — sin-based assignment
    should yield the full palette and avoid long uniform runs."""
    warp_palette = ['#D4A317', '#F5E6B0', '#D4A317', '#F5E6B0', '#556B2F']
    warp = [
        warp_palette[math.floor(abs(math.sin(i * 2.3)) * len(warp_palette))]
        for i in range(175)
    ]
    unique = set(warp)
    assert '#D4A317' in unique
    assert '#F5E6B0' in unique
    assert '#556B2F' in unique
    # No run of more than 10 identical consecutive colors
    max_run = 1
    run = 1
    for i in range(1, len(warp)):
        if warp[i] == warp[i - 1]:
            run += 1
            max_run = max(max_run, run)
        else:
            run = 1
    assert max_run <= 10, f"Warp color run of {max_run} is too long — pattern feels mechanical"


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

def test_thumbnail_is_valid_svg():
    thumb = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert thumb.strip().startswith("<svg") or "<svg" in thumb[:200]
    assert "</svg>" in thumb


def test_thumbnail_contains_twill_colors():
    """Thumbnail SVG must include the key palette colors."""
    thumb = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert "#D4A317" in thumb, "barley gold missing from thumbnail"
    assert "#B5302A" in thumb or "#556B2F" in thumb, "weft/olive color missing from thumbnail"


def test_html_does_not_reference_external_assets():
    """The piece must be self-contained — no img src or script src pointing outside."""
    html = _html()
    assert "essay.md" not in html, "index.html must not fetch essay.md at runtime"
    external = re.findall(r'src=["\']https?://', html)
    assert len(external) == 0, f"External script/img src found: {external}"


def test_essay_mentions_shavuot():
    """Essay must connect the artwork to Shavuot."""
    assert "Shavuot" in _essay()


def test_essay_minimum_200_words_baseline():
    """Baseline: essay must meet the gallery-wide minimum of 200 words."""
    text = _essay()
    assert len(text.split()) >= 200


# ---------------------------------------------------------------------------
# Explicit failure modes
# ---------------------------------------------------------------------------

def test_wrong_piece_id_not_in_json():
    """A slightly wrong ID must not be in pieces.json."""
    data = json.load(open(os.path.join(GALLERY_ROOT, "pieces.json"), encoding="utf-8"))
    ids = {p["id"] for p in data}
    assert "57-ruths-loom" not in ids
    assert "ruths-loom-woven-harvest" not in ids


def test_piece_56_not_mutated():
    """Ensure the last existing piece (56-613-force-graph) is still in pieces.json."""
    data = json.load(open(os.path.join(GALLERY_ROOT, "pieces.json"), encoding="utf-8"))
    ids = {p["id"] for p in data}
    assert "56-613-force-graph" in ids


def test_twill_rule_rejects_every_cell_over():
    """The twill rule must never mark every cell in a row as over."""
    def is_over(col, row):
        return (col + row) % 3 != 0

    for row in range(175):
        warp_in_row = sum(1 for c in range(175) if not is_over(c, row))
        assert warp_in_row > 0, f"Row {row} has no warp cells — invalid twill"
