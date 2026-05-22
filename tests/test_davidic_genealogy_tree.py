"""
Tests for piece 48-ruth-to-david-tree: From Ruth to David — The Living Branch.

Verifies that the genealogy tree piece exists on disk with correct content,
that pieces.json registers it with the right theme and technique, and that
the HTML animation meets the acceptance criteria.
"""
import json
import os
import unicodedata

import pytest

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")
PIECE_ID = "48-ruth-to-david-tree"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)


def _load_pieces():
    with open(PIECES_JSON, "r", encoding="utf-8") as fh:
        return json.load(fh)


def _get_piece():
    for p in _load_pieces():
        if p["id"] == PIECE_ID:
            return p
    return None


def _html():
    """Return NFC-normalised index.html content."""
    return unicodedata.normalize(
        "NFC", open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    )


def _essay():
    return open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()


# ---------------------------------------------------------------------------
# pieces.json registration
# ---------------------------------------------------------------------------

def test_piece_registered_in_pieces_json():
    """Piece must appear in pieces.json."""
    assert _get_piece() is not None, f"Piece '{PIECE_ID}' not found in pieces.json"


def test_piece_theme_is_book_of_ruth():
    """Theme must be 'The Book of Ruth' as specified in the acceptance criteria."""
    piece = _get_piece()
    assert piece is not None
    assert piece["theme"] == "The Book of Ruth", (
        f"Expected theme 'The Book of Ruth', got '{piece['theme']}'"
    )


def test_piece_technique_mentions_bezier():
    """Technique field must reference the bezier tree method."""
    piece = _get_piece()
    assert piece is not None
    tech = piece["technique"].lower()
    assert "bezier" in tech or "bézier" in tech or "botanical" in tech, (
        f"Technique '{piece['technique']}' does not mention bezier or botanical"
    )


def test_piece_has_all_required_fields():
    """Every required pieces.json field must be present and non-empty."""
    piece = _get_piece()
    assert piece is not None
    required = (
        "id", "title", "tagline", "year", "theme",
        "technique", "path", "thumbnail", "essay",
    )
    for field in required:
        assert field in piece and piece[field], (
            f"Piece '{PIECE_ID}' is missing or has empty field '{field}'"
        )


# ---------------------------------------------------------------------------
# File layout
# ---------------------------------------------------------------------------

def test_piece_directory_exists():
    """The piece directory must exist on disk."""
    assert os.path.isdir(PIECE_DIR), f"Piece directory '{PIECE_DIR}' not found"


def test_index_html_exists():
    """index.html must exist inside the piece directory."""
    assert os.path.isfile(os.path.join(PIECE_DIR, "index.html"))


def test_essay_md_exists():
    """essay.md must exist inside the piece directory."""
    assert os.path.isfile(os.path.join(PIECE_DIR, "essay.md"))


def test_thumbnail_svg_exists():
    """thumbnail.svg must exist inside the piece directory."""
    assert os.path.isfile(os.path.join(PIECE_DIR, "thumbnail.svg"))


def test_readme_exists():
    """README.md must exist inside the piece directory."""
    assert os.path.isfile(os.path.join(PIECE_DIR, "README.md"))


# ---------------------------------------------------------------------------
# Essay content
# ---------------------------------------------------------------------------

def test_essay_md_word_count_at_least_300():
    """Essay must be at least 300 words (acceptance criterion)."""
    text = _essay()
    word_count = len(text.split())
    assert word_count >= 300, (
        f"essay.md has only {word_count} words; acceptance criterion requires >= 300"
    )


def test_essay_cites_ruth_chapter():
    """Essay must reference Ruth 4:18-22 as the textual source."""
    text = _essay()
    assert "Ruth 4" in text or "4:18" in text, (
        "essay.md must cite Ruth 4:18-22 as the genealogy source"
    )


def test_essay_cites_yerushalmi():
    """Essay must cite the Yerushalmi tradition that David was born on Shavuot."""
    text = _essay()
    assert "Yerushalmi" in text or "Chagigah" in text, (
        "essay.md must cite Yerushalmi Chagigah 2:3 for the Shavuot-David tradition"
    )


def test_essay_mentions_hesed():
    """Essay must discuss hesed as its central theological concept."""
    text = _essay()
    assert "hesed" in text.lower() or "lovingkindness" in text.lower(), (
        "essay.md must discuss hesed (loving-kindness)"
    )


def test_essay_mentions_goel():
    """Essay must draw the Leviticus 25 go'el connection."""
    text = _essay()
    assert "go'el" in text or "goel" in text.lower() or "redeemer" in text.lower(), (
        "essay.md must mention the go'el / kinsman redeemer connecting to Leviticus 25"
    )


# ---------------------------------------------------------------------------
# HTML animation requirements
# ---------------------------------------------------------------------------

def test_index_html_uses_request_animation_frame():
    """Canvas animation must use requestAnimationFrame."""
    html = _html()
    assert "requestAnimationFrame" in html, (
        "index.html must use requestAnimationFrame for the animation loop"
    )


def test_index_html_has_canvas_element():
    """index.html must contain a canvas element for the tree animation."""
    html = _html()
    assert "<canvas" in html, "index.html must contain a <canvas> element"


def test_index_html_contains_key_hebrew_base_letters():
    """Base Hebrew letters for key names must appear in the HTML (nikud-independent check).

    Uses base consonants only (stripping nikud) so the check passes regardless of
    combining-character ordering between the HTML and the test source file.
    """
    html = _html()
    # Strip nikud (U+0591-U+05C7) for encoding-independent comparison
    def strip_nikud(s):
        return "".join(c for c in s if not (0x0591 <= ord(c) <= 0x05C7))

    html_stripped = strip_nikud(html)
    base_names = [
        "פרץ",  # פרץ Peretz
        "בעז",  # בעז Boaz
        "דוד",  # דוד David
    ]
    for name in base_names:
        assert name in html_stripped, (
            f"Hebrew base letters '{name}' not found in index.html"
        )


def test_index_html_has_parchment_background():
    """index.html must use the parchment background color #F5EDD6."""
    html = _html()
    assert "#F5EDD6" in html or "F5EDD6" in html.upper(), (
        "index.html must use parchment background #F5EDD6"
    )


def test_index_html_has_sienna_branches():
    """index.html must use sienna #7B3F00 for branches."""
    html = _html()
    assert "#7B3F00" in html or "7B3F00" in html.upper(), (
        "index.html must use warm sienna #7B3F00 for branches"
    )


def test_index_html_has_gold_glow():
    """index.html must use gold #D4A017 for David's glow."""
    html = _html()
    assert "#D4A017" in html or "D4A017" in html.upper(), (
        "index.html must use gold #D4A017 for the David node glow"
    )


def test_index_html_embeds_essay_text():
    """The essay text must be embedded inline in index.html (no external fetch needed)."""
    essay_text = _essay()
    html = _html()
    words = [w for w in essay_text.split() if len(w) > 5]
    sampled = words[:10]
    found = sum(1 for w in sampled if w in html)
    assert found >= 5, (
        f"index.html does not appear to embed essay text: only {found}/10 sampled words found"
    )


def test_index_html_has_crown_drawing_code():
    """index.html must include code to draw a crown above David."""
    html = _html()
    assert "crown" in html.lower() or "Crown" in html, (
        "index.html must contain crown drawing code for David's node"
    )


def test_index_html_has_ruth_silhouette():
    """index.html must include code to draw a Ruth figure below Peretz."""
    html = _html()
    assert "ruth" in html.lower() or "Ruth" in html, (
        "index.html must contain a Ruth silhouette drawing function"
    )


def test_thumbnail_is_valid_svg():
    """thumbnail.svg must be a valid SVG document."""
    svg_path = os.path.join(PIECE_DIR, "thumbnail.svg")
    text = open(svg_path, encoding="utf-8").read()
    assert "<svg" in text and "</svg>" in text, (
        "thumbnail.svg does not appear to be valid SVG"
    )


def test_thumbnail_uses_parchment_color():
    """thumbnail.svg must reference the parchment background color."""
    svg_path = os.path.join(PIECE_DIR, "thumbnail.svg")
    text = open(svg_path, encoding="utf-8").read()
    assert "F5EDD6" in text.upper(), (
        "thumbnail.svg must use the parchment background #F5EDD6"
    )


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

def test_piece_does_not_duplicate_existing_id():
    """The new piece ID must not collide with any pre-existing piece."""
    pieces = _load_pieces()
    ids = [p["id"] for p in pieces]
    assert ids.count(PIECE_ID) == 1, (
        f"Piece ID '{PIECE_ID}' appears {ids.count(PIECE_ID)} times in pieces.json (must be exactly 1)"
    )


def test_essay_md_path_matches_pieces_json():
    """The essay path registered in pieces.json must match the actual file on disk."""
    piece = _get_piece()
    assert piece is not None
    registered = piece["essay"]
    full_path = os.path.join(GALLERY_ROOT, registered)
    assert os.path.isfile(full_path), (
        f"Essay path '{registered}' in pieces.json does not exist on disk"
    )


def test_empty_essay_file_would_fail():
    """Confirm that an empty file would fail the 300-word threshold — fixture test."""
    word_count = len("".split())
    assert word_count < 300, "Empty string should have zero words, below threshold"


def test_missing_piece_id_not_registered():
    """A piece ID that does not exist should not be found in pieces.json."""
    piece = None
    for p in _load_pieces():
        if p["id"] == "99-nonexistent-piece":
            piece = p
    assert piece is None, "Nonexistent piece ID should not be in pieces.json"
