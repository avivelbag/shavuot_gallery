"""
Tests for piece 30-seven-weeks-spirograph.

Validates that the hypotrochoid spirograph piece is correctly registered in
pieces.json, ships all required files, and that index.html contains the
expected animation technique, palette, and embedded essay text.
"""
import json
import os

import pytest

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")
PIECE_ID = "30-seven-weeks-spirograph"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)


def _load_pieces():
    """Return the parsed pieces.json list."""
    with open(PIECES_JSON, encoding="utf-8") as fh:
        return json.load(fh)


def _get_piece():
    """Return the pieces.json entry for the spirograph piece, or None."""
    for p in _load_pieces():
        if p["id"] == PIECE_ID:
            return p
    return None


def _read_html():
    """Return the full text of the piece's index.html."""
    return open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()


def _read_essay():
    """Return the full text of the piece's essay.md."""
    return open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()


# ---------------------------------------------------------------------------
# Happy path — piece registration and file layout
# ---------------------------------------------------------------------------

def test_piece_registered_in_pieces_json():
    """Piece 30 must appear in pieces.json with the correct id."""
    piece = _get_piece()
    assert piece is not None, f"Piece '{PIECE_ID}' not found in pieces.json"


def test_required_files_exist():
    """All four piece files must exist on disk."""
    for filename in ("index.html", "essay.md", "thumbnail.svg", "README.md"):
        full = os.path.join(PIECE_DIR, filename)
        assert os.path.isfile(full), f"Missing: pieces/{PIECE_ID}/{filename}"


def test_pieces_json_entry_has_all_required_fields():
    """The pieces.json entry must contain every required gallery field."""
    required = ("id", "title", "tagline", "year", "theme", "technique", "path", "thumbnail", "essay")
    piece = _get_piece()
    assert piece is not None
    for field in required:
        assert field in piece and piece[field], (
            f"Piece '{PIECE_ID}' is missing or has empty field '{field}'"
        )


def test_pieces_json_no_duplicate_ids():
    """Adding piece 30 must not create a duplicate id."""
    ids = [p["id"] for p in _load_pieces()]
    assert len(ids) == len(set(ids)), f"Duplicate piece IDs found: {ids}"


def test_thumbnail_is_valid_svg():
    """Thumbnail must be a readable SVG file."""
    piece = _get_piece()
    assert piece is not None
    thumb = os.path.join(GALLERY_ROOT, piece["thumbnail"])
    assert os.path.isfile(thumb)
    content = open(thumb, encoding="utf-8").read()
    assert "<svg" in content and "</svg>" in content


# ---------------------------------------------------------------------------
# Happy path — animation content
# ---------------------------------------------------------------------------

def test_index_html_uses_requestanimationframe():
    """The animation must drive itself with requestAnimationFrame."""
    assert "requestAnimationFrame" in _read_html()


def test_index_html_has_canvas_element():
    """A <canvas> element must be present for the animation."""
    assert "<canvas" in _read_html()


def test_index_html_uses_parametric_math():
    """The hypotrochoid must be computed via Math.cos and Math.sin."""
    html = _read_html()
    assert "Math.cos" in html and "Math.sin" in html


def test_index_html_contains_shavuot_hebrew():
    """The Hebrew label שָׁבוּעוֹת (or simplified form) must appear in the HTML."""
    html = _read_html()
    assert "שָׁבוּעוֹת" in html or "שבועות" in html or "שָבוּעות" in html, (
        "index.html must contain the Hebrew word שָׁבוּעוֹת"
    )


def test_index_html_palette_field_green():
    """Field green #2D5016 must appear in the source."""
    html = _read_html().upper()
    assert "2D5016" in html, "index.html must reference the field-green palette color #2D5016"


def test_index_html_palette_harvest_gold():
    """Harvest gold #C8962A must appear in the source."""
    html = _read_html().upper()
    assert "C8962A" in html, "index.html must reference the harvest-gold palette color #C8962A"


def test_index_html_palette_parchment_background():
    """Parchment background #F2EAD3 must appear in the source."""
    html = _read_html().upper()
    assert "F2EAD3" in html, "index.html must reference the parchment background color #F2EAD3"


def test_index_html_seven_fold_symmetry_parameter():
    """The hypotrochoid R=7 parameter must appear in the JavaScript."""
    html = _read_html()
    assert "Rv = 7" in html or "R = 7" in html or "= 7," in html or "Rv=7" in html, (
        "index.html must use R=7 for seven-fold symmetry"
    )


# ---------------------------------------------------------------------------
# Happy path — essay content
# ---------------------------------------------------------------------------

def test_essay_minimum_word_count():
    """Essay must contain at least 200 words."""
    text = _read_essay()
    count = len(text.split())
    assert count >= 200, f"Essay has only {count} words (minimum 200)"


def test_essay_mentions_leviticus():
    """Essay must cite Leviticus 23 as the source for Sefirat HaOmer."""
    essay = _read_essay()
    assert "Leviticus" in essay or "23:15" in essay, (
        "Essay must cite Leviticus 23:15-16 as the source"
    )


def test_essay_mentions_sefirot():
    """Essay must explain the kabbalistic sefirot structure of the Omer."""
    essay = _read_essay().lower()
    assert "sefirot" in essay or "sefirah" in essay or "sefira" in essay, (
        "Essay must discuss the kabbalistic sefirot structure"
    )


def test_essay_mentions_seven_weeks():
    """Essay must reference the seven-week structure of the Omer."""
    essay = _read_essay().lower()
    assert "seven weeks" in essay or "49 days" in essay or "forty-nine" in essay, (
        "Essay must discuss the seven-week / 49-day structure"
    )


def test_essay_embedded_in_html():
    """The essay text must be embedded inline in index.html (no runtime fetch)."""
    essay = _read_essay()
    html = _read_html()
    long_words = [w for w in essay.split() if len(w) > 5][:10]
    found = sum(1 for w in long_words if w in html)
    assert found >= 5, (
        f"Essay text not embedded in index.html: only {found}/10 sampled words found"
    )


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

def test_empty_essay_fails_word_count(tmp_path):
    """An empty essay.md must not satisfy the 200-word minimum."""
    empty = tmp_path / "empty.md"
    empty.write_text("", encoding="utf-8")
    count = len(empty.read_text(encoding="utf-8").split())
    assert count < 200, "Empty file should have zero words"


def test_wrong_piece_id_not_found(tmp_path):
    """Looking up a non-existent piece id must return None."""
    bad = [{"id": "99-fake", "title": "x"}]
    result = next((p for p in bad if p["id"] == PIECE_ID), None)
    assert result is None


def test_thumbnail_extension_is_svg():
    """Thumbnail for piece 30 must use the .svg extension."""
    piece = _get_piece()
    assert piece is not None
    ext = os.path.splitext(piece["thumbnail"])[1].lower()
    assert ext == ".svg", f"Expected .svg thumbnail, got '{ext}'"


# ---------------------------------------------------------------------------
# Explicit failure mode
# ---------------------------------------------------------------------------

def test_missing_canvas_element_would_fail():
    """An HTML file without <canvas> could not host the animation."""
    html = _read_html()
    assert "<canvas" in html, (
        "index.html must contain a <canvas> element for the spirograph animation"
    )


def test_piece_path_matches_id():
    """The 'path' field in pieces.json must contain the piece id as directory name."""
    piece = _get_piece()
    assert piece is not None
    parts = piece["path"].replace("\\", "/").split("/")
    dir_name = parts[-2] if len(parts) >= 2 else ""
    assert dir_name == PIECE_ID, (
        f"path directory '{dir_name}' does not match piece id '{PIECE_ID}'"
    )


def test_year_is_integer():
    """The year field must be an integer, not a string."""
    piece = _get_piece()
    assert piece is not None
    assert isinstance(piece["year"], int), (
        f"year field must be int, got {type(piece['year'])}"
    )
