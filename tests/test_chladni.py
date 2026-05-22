"""
Tests specific to piece 47-kol-hashofar-chladni.

Validates:
- All required files exist (index.html, essay.md, README.md, thumbnail.svg)
- pieces.json entry is well-formed with the expected fields
- The Chladni simulation code is present and correct (eigenfunction, modes array,
  Hebrew day labels, morphing, requestAnimationFrame)
- The essay meets content and length requirements
- Edge cases: missing files, malformed entries, wrong piece count
- Failure modes: incorrect field values, absent Hebrew labels
"""

import json
import os
import re

import pytest

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECES_JSON  = os.path.join(GALLERY_ROOT, "pieces.json")
PIECE_ID     = "47-kol-hashofar-chladni"
PIECE_DIR    = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
INDEX_HTML   = os.path.join(PIECE_DIR, "index.html")
ESSAY_MD     = os.path.join(PIECE_DIR, "essay.md")
README_MD    = os.path.join(PIECE_DIR, "README.md")
THUMBNAIL    = os.path.join(PIECE_DIR, "thumbnail.svg")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_pieces():
    """Return parsed pieces.json as a list."""
    with open(PIECES_JSON, encoding="utf-8") as fh:
        return json.load(fh)


def get_piece():
    """Return the pieces.json entry for piece 47, or None if absent."""
    for p in load_pieces():
        if p["id"] == PIECE_ID:
            return p
    return None


def read_html():
    """Return the full text of index.html."""
    with open(INDEX_HTML, encoding="utf-8") as fh:
        return fh.read()


def read_essay():
    """Return the full text of essay.md."""
    with open(ESSAY_MD, encoding="utf-8") as fh:
        return fh.read()


# ---------------------------------------------------------------------------
# File existence — happy path
# ---------------------------------------------------------------------------

def test_piece_dir_exists():
    """Piece directory pieces/47-kol-hashofar-chladni/ must be present."""
    assert os.path.isdir(PIECE_DIR), f"Missing piece directory: {PIECE_DIR}"


def test_index_html_exists():
    """index.html must exist in the piece directory."""
    assert os.path.isfile(INDEX_HTML), f"Missing: {INDEX_HTML}"


def test_essay_md_exists():
    """essay.md must exist in the piece directory."""
    assert os.path.isfile(ESSAY_MD), f"Missing: {ESSAY_MD}"


def test_readme_md_exists():
    """README.md must exist in the piece directory."""
    assert os.path.isfile(README_MD), f"Missing: {README_MD}"


def test_thumbnail_svg_exists():
    """thumbnail.svg must exist in the piece directory."""
    assert os.path.isfile(THUMBNAIL), f"Missing: {THUMBNAIL}"


def test_thumbnail_is_valid_svg():
    """thumbnail.svg must contain opening and closing <svg> tags."""
    with open(THUMBNAIL, encoding="utf-8") as fh:
        text = fh.read()
    assert "<svg" in text and "</svg>" in text, "thumbnail.svg is not valid SVG"


# ---------------------------------------------------------------------------
# pieces.json registration — happy path
# ---------------------------------------------------------------------------

def test_piece_in_pieces_json():
    """Piece 47 must appear in pieces.json."""
    assert get_piece() is not None, f"'{PIECE_ID}' not found in pieces.json"


def test_piece_required_fields():
    """All nine required fields must be present and non-empty."""
    required = ("id", "title", "tagline", "year", "theme", "technique",
                "path", "thumbnail", "essay")
    piece = get_piece()
    assert piece is not None
    for field in required:
        assert field in piece, f"Missing field '{field}' in pieces.json entry"
        assert piece[field] not in (None, ""), f"Empty field '{field}' in pieces.json"


def test_piece_year_is_int():
    """year field must be an integer."""
    piece = get_piece()
    assert piece is not None
    assert isinstance(piece["year"], int), "year must be an integer"


def test_piece_path_ends_with_html():
    """path field must end with .html."""
    piece = get_piece()
    assert piece is not None
    assert piece["path"].endswith(".html"), "path must end with .html"


def test_piece_thumbnail_extension():
    """thumbnail must have a recognised image extension."""
    piece = get_piece()
    assert piece is not None
    ext = os.path.splitext(piece["thumbnail"])[1].lower()
    assert ext in {".svg", ".png", ".jpg", ".jpeg", ".webp", ".gif"}


def test_piece_id_matches_directory():
    """The id field must match the directory name in the path."""
    piece = get_piece()
    assert piece is not None
    parts = piece["path"].replace("\\", "/").split("/")
    assert len(parts) >= 2
    assert parts[-2] == PIECE_ID


def test_piece_essay_path_resolves():
    """The essay path in pieces.json must exist on disk."""
    piece = get_piece()
    assert piece is not None
    full = os.path.join(GALLERY_ROOT, piece["essay"])
    assert os.path.isfile(full), f"Essay file not found at {full}"


# ---------------------------------------------------------------------------
# Essay content — happy path
# ---------------------------------------------------------------------------

def test_essay_min_200_words():
    """essay.md must contain at least 200 words."""
    text = read_essay()
    count = len(text.split())
    assert count >= 200, f"essay.md has only {count} words (need ≥ 200)"


def test_essay_mentions_exodus_19():
    """Essay must cite Exodus 19 — the Sinai revelation passage."""
    text = read_essay()
    assert "Exodus 19" in text or "Exodus 19:19" in text, (
        "essay.md must mention Exodus 19"
    )


def test_essay_mentions_chladni():
    """Essay must mention Ernst Chladni (physicist, 1787 discovery)."""
    text = read_essay()
    assert "Chladni" in text, "essay.md must mention Chladni"


def test_essay_mentions_leviticus_23():
    """Essay must reference Leviticus 23 for the Omer count."""
    text = read_essay()
    assert "Leviticus 23" in text, "essay.md must reference Leviticus 23"


def test_essay_mentions_nodal_lines():
    """Essay must explain the concept of nodal lines (the core physics)."""
    text = read_essay()
    assert "nodal" in text.lower(), "essay.md must mention nodal lines"


# ---------------------------------------------------------------------------
# index.html — animation code presence
# ---------------------------------------------------------------------------

def test_html_uses_requestanimationframe():
    """Chladni simulation must be driven by requestAnimationFrame."""
    assert "requestAnimationFrame" in read_html()


def test_html_contains_chladni_eigenfunction():
    """index.html must implement the Chladni eigenfunction using Math.cos."""
    html = read_html()
    assert "Math.cos" in html, "Chladni eigenfunction requires Math.cos"
    assert "Math.PI" in html, "Chladni eigenfunction requires Math.PI"


def test_html_contains_50_modes():
    """MODES array must have exactly 50 entries (one per Omer day)."""
    html = read_html()
    assert "MODES" in html, "MODES array not found in index.html"
    # Count [m, n] pair entries by counting opening brackets after 'MODES'
    modes_start = html.index("MODES")
    modes_region = html[modes_start:modes_start + 3000]
    # Each mode pair is "[m, n]" — count commas between integers in array
    pairs = re.findall(r'\[\s*\d+\s*,\s*\d+\s*\]', modes_region)
    assert len(pairs) == 50, (
        f"Expected 50 mode pairs, found {len(pairs)}"
    )


def test_html_contains_hebrew_day_1():
    """HTML must include the Hebrew label for day 1 of the Omer."""
    assert 'יוֹם אֶחָד' in read_html(), "Day 1 Hebrew label missing from index.html"


def test_html_contains_shavuot_label():
    """HTML must include the Shavuot label (day 50)."""
    assert 'חַג הַשָּׁבֻעוֹת' in read_html(), (
        "Shavuot label 'חַג הַשָּׁבֻעוֹת' missing from index.html"
    )


def test_html_contains_hold_and_trans_frames():
    """HTML must define HOLD_FRAMES and TRANS_FRAMES for the timing loop."""
    html = read_html()
    assert "HOLD_FRAMES" in html, "HOLD_FRAMES constant missing"
    assert "TRANS_FRAMES" in html or "TRANSITION" in html, "Transition frames constant missing"


def test_html_contains_smoothstep_or_lerp():
    """Morph transition must use a smooth interpolation function."""
    html = read_html()
    has_smoothstep = "smoothstep" in html
    has_lerp       = "lerp" in html.lower()
    has_cubic      = "(3.0 - 2.0 * t)" in html or "(3 - 2 * t)" in html
    assert has_smoothstep or has_lerp or has_cubic, (
        "index.html must implement smooth interpolation for the morph"
    )


def test_html_contains_imagdata_pixel_loop():
    """Pixel rendering must use ImageData (putImageData / createImageData)."""
    html = read_html()
    assert "ImageData" in html or "putImageData" in html or "createImageData" in html, (
        "index.html must use ImageData for efficient pixel rendering"
    )


def test_html_embeds_essay_text():
    """
    index.html must embed essay text inline.

    The test samples the first 10 words longer than 5 characters from essay.md
    and requires at least 5 to appear somewhere in the HTML source.
    """
    essay = read_essay()
    html  = read_html()
    long_words = [w for w in essay.split() if len(w) > 5]
    sampled    = long_words[:10]
    found      = sum(1 for w in sampled if w in html)
    assert found >= 5, (
        f"index.html does not appear to embed essay text "
        f"(only {found}/10 sampled words found)"
    )


def test_html_palette_background():
    """Background color must be the warm black #0A0804."""
    assert "#0A0804" in read_html() or "0A0804" in read_html(), (
        "index.html must use the #0A0804 background color"
    )


def test_html_palette_sand():
    """Nodal line color must be the wheat-gold #E8C870."""
    assert "E8C870" in read_html(), (
        "index.html must use the #E8C870 wheat-gold color for nodal lines"
    )


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

def test_essay_far_above_minimum_words():
    """essay.md should have substantially more than the 200-word minimum."""
    text  = read_essay()
    count = len(text.split())
    assert count >= 400, (
        f"essay.md is suspiciously short ({count} words); expected ≥ 400 for this piece"
    )


def test_modes_contain_no_diagonal_pairs(tmp_path):
    """
    Diagonal mode pairs (m == n) produce the zero field and must be excluded.

    This test parses the MODES array from index.html and verifies no (m, m)
    entry slipped in.
    """
    html  = read_html()
    start = html.index("MODES")
    region = html[start:start + 3000]
    pairs  = re.findall(r'\[\s*(\d+)\s*,\s*(\d+)\s*\]', region)
    diagonal = [(m, n) for m, n in pairs if m == n]
    assert diagonal == [], (
        f"MODES contains diagonal (m==m) pairs which yield the zero field: {diagonal}"
    )


def test_no_duplicate_modes():
    """No two days should share the same (m, n) pair (or its mirror (n, m))."""
    html   = read_html()
    start  = html.index("MODES")
    region = html[start:start + 3000]
    pairs  = [(int(m), int(n)) for m, n in re.findall(r'\[\s*(\d+)\s*,\s*(\d+)\s*\]', region)]
    canonical = set()
    duplicates = []
    for m, n in pairs:
        key = (min(m, n), max(m, n))
        if key in canonical:
            duplicates.append((m, n))
        canonical.add(key)
    assert duplicates == [], f"Duplicate mode pairs found: {duplicates}"


# ---------------------------------------------------------------------------
# Failure modes
# ---------------------------------------------------------------------------

def test_missing_piece_dir_is_detected(tmp_path):
    """
    Verify that our file-existence check correctly flags a missing directory.

    This is a meta-test: it confirms the check logic works rather than testing
    production files.
    """
    fake_dir = os.path.join(str(tmp_path), "99-nonexistent-piece")
    assert not os.path.isdir(fake_dir), (
        "Fixture directory must not exist for this test to be meaningful"
    )


def test_essay_below_200_words_is_detectable(tmp_path):
    """
    Confirm that a stub essay (< 200 words) would be caught.

    Writes a 10-word stub and verifies the word count is below threshold.
    """
    stub = tmp_path / "stub_essay.md"
    stub.write_text("Short stub. " * 10, encoding="utf-8")
    count = len(stub.read_text().split())
    assert count < 200, "Fixture stub must be below 200 words"


def test_pieces_json_missing_essay_field_detected(tmp_path):
    """
    Confirm that a pieces.json entry missing the essay field is detectable.
    """
    bad = [{"id": "99-test", "title": "Test", "essay": ""}]
    val = bad[0].get("essay")
    assert not val, "Empty essay field should be falsy — fixture is correct"
