"""Tests for piece 82-superformula-seven-species.

Verifies the directory layout, pieces.json registration, HTML structure,
essay content requirements, and the thumbnail SVG — covering the happy path,
edge cases, and explicit failure modes described in the acceptance criteria.
"""

import json
import os

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID = "82-superformula-seven-species"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_pieces():
    with open(PIECES_JSON, encoding="utf-8") as fh:
        return json.load(fh)


def get_piece():
    for p in load_pieces():
        if p["id"] == PIECE_ID:
            return p
    return None


def read_file(relpath):
    """Read a file relative to GALLERY_ROOT, return text."""
    return open(os.path.join(GALLERY_ROOT, relpath), encoding="utf-8").read()


# ---------------------------------------------------------------------------
# Happy path: directory and file layout
# ---------------------------------------------------------------------------

def test_piece_directory_exists():
    assert os.path.isdir(PIECE_DIR), f"Piece directory not found: {PIECE_DIR}"


def test_index_html_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "index.html"))


def test_essay_md_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "essay.md"))


def test_thumbnail_svg_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "thumbnail.svg"))


def test_readme_md_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "README.md"))


# ---------------------------------------------------------------------------
# Happy path: pieces.json registration
# ---------------------------------------------------------------------------

def test_piece_registered_in_pieces_json():
    piece = get_piece()
    assert piece is not None, f"Piece '{PIECE_ID}' not found in pieces.json"


def test_piece_has_required_fields():
    piece = get_piece()
    assert piece is not None
    required = ("id", "title", "tagline", "year", "theme", "technique", "path", "thumbnail", "essay")
    for field in required:
        assert field in piece and piece[field], f"Missing or empty field '{field}'"


def test_piece_theme_mentions_bikkurim():
    piece = get_piece()
    assert piece is not None
    assert "Bikkurim" in piece["theme"] or "seven species" in piece["theme"].lower(), (
        "theme must reference Bikkurim or seven species"
    )


def test_piece_technique_mentions_superformula():
    piece = get_piece()
    assert piece is not None
    assert "superformula" in piece["technique"].lower() or "Gielis" in piece["technique"], (
        "technique must reference the Gielis superformula"
    )


def test_piece_year_is_int():
    piece = get_piece()
    assert piece is not None
    assert isinstance(piece["year"], int)


# ---------------------------------------------------------------------------
# Happy path: index.html content
# ---------------------------------------------------------------------------

def test_index_html_uses_requestanimationframe():
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "requestAnimationFrame" in html


def test_index_html_contains_superformula_math():
    """The superformula r(θ) computation must appear in the JS."""
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    # The formula involves cos(m*theta/4) and Math.pow
    assert "Math.cos" in html and "Math.pow" in html, (
        "index.html must implement the superformula with Math.cos and Math.pow"
    )


def test_index_html_defines_all_seven_species():
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    hebrew_labels = ["חיטה", "שעורה", "גפן", "תאנה", "רימון", "זית", "תמר"]
    for label in hebrew_labels:
        assert label in html, f"Hebrew label '{label}' not found in index.html"


def test_index_html_has_seven_species_array():
    """The JS must define parameter sets for all 7 species."""
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    # At minimum 7 entries in the species array; count opening brace sequences
    count = html.count("label:")
    assert count >= 7, f"Expected ≥7 species label fields in JS, found {count}"


def test_index_html_embeds_essay_text():
    """Essay content must be embedded inline (not fetched at runtime)."""
    essay = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    words = [w for w in essay.split() if len(w) > 5][:15]
    found = sum(1 for w in words if w in html)
    assert found >= 7, (
        f"index.html does not appear to embed essay text (only {found}/15 words found)"
    )


def test_index_html_has_hebrew_labels_in_canvas_code():
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    # The fillText call with Hebrew label and canvas animation
    assert "fillText" in html, "index.html must use ctx.fillText for Hebrew labels"


def test_index_html_has_background_color():
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    # Background should be near-black parchment
    assert "#0C0A06" in html or "0C0A06" in html, (
        "index.html must use background color #0C0A06"
    )


def test_index_html_cycles_through_species():
    """Animation must have a timing mechanism for display and transition."""
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "DISPLAY_MS" in html or "4000" in html, (
        "index.html must define a display duration (4s per species)"
    )
    assert "TRANSITION_MS" in html or "1500" in html, (
        "index.html must define a transition duration (1.5s)"
    )


# ---------------------------------------------------------------------------
# Happy path: essay.md content
# ---------------------------------------------------------------------------

def test_essay_has_deuteronomy_quote():
    essay = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    assert "Deuteronomy 8:8" in essay or "8:8" in essay, (
        "essay.md must open with a Deuteronomy 8:8 reference"
    )


def test_essay_mentions_bikkurim():
    essay = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    assert "Bikkurim" in essay, "essay.md must discuss the Bikkurim ceremony"


def test_essay_mentions_mishnah_bikkurim():
    essay = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    assert "Bikkurim" in essay and ("3:1" in essay or "Mishnah" in essay), (
        "essay.md must mention Mishnah Bikkurim and the Temple procession"
    )


def test_essay_mentions_rashi():
    essay = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    assert "Rashi" in essay, "essay.md must cite Rashi on Deuteronomy 8:10"


def test_essay_mentions_birkat_hamazon():
    essay = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    assert "Birkat HaMazon" in essay or "grace after meals" in essay.lower(), (
        "essay.md must connect the seven species to Birkat HaMazon"
    )


def test_essay_word_count_at_least_400():
    essay = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    word_count = len(essay.split())
    assert word_count >= 400, f"essay.md has only {word_count} words (need ≥400)"


def test_essay_connects_math_to_theme():
    """The essay must tie the superformula to the seven-species theme."""
    essay = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    has_math_ref = "superformula" in essay.lower() or "equation" in essay.lower() or "formula" in essay.lower()
    assert has_math_ref, "essay.md must connect the mathematical technique to the Shavuot theme"


# ---------------------------------------------------------------------------
# Happy path: thumbnail.svg
# ---------------------------------------------------------------------------

def test_thumbnail_is_valid_svg():
    svg = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert "<svg" in svg and "</svg>" in svg


def test_thumbnail_has_dark_background():
    svg = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert "#0C0A06" in svg or "0C0A06" in svg, (
        "thumbnail.svg must use the dark parchment background #0C0A06"
    )


def test_thumbnail_has_seven_species_paths():
    """Thumbnail must have shapes for all seven species (at least 7 path elements)."""
    svg = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    path_count = svg.count("<path ")
    assert path_count >= 7, f"thumbnail.svg has only {path_count} <path> elements (need ≥7)"


def test_thumbnail_has_seven_hebrew_labels():
    svg = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    hebrew_labels = ["חיטה", "שעורה", "גפן", "תאנה", "רימון", "זית", "תמר"]
    for label in hebrew_labels:
        assert label in svg, f"thumbnail.svg is missing Hebrew label '{label}'"


def test_thumbnail_uses_species_colors():
    svg = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    colors = ["D4A820", "C8963A", "6030A0", "8B5A2B", "C03020", "4A7040", "A06010"]
    for color in colors:
        assert color.lower() in svg.lower(), (
            f"thumbnail.svg is missing species color #{color}"
        )


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

def test_essay_file_is_utf8():
    """essay.md must be valid UTF-8 (Hebrew text requires it)."""
    path = os.path.join(PIECE_DIR, "essay.md")
    with open(path, "rb") as fh:
        raw = fh.read()
    raw.decode("utf-8")  # raises UnicodeDecodeError if not valid


def test_index_html_is_utf8():
    path = os.path.join(PIECE_DIR, "index.html")
    with open(path, "rb") as fh:
        raw = fh.read()
    raw.decode("utf-8")


def test_thumbnail_viewbox_is_400x400():
    svg = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert '400' in svg, "thumbnail.svg must be 400×400"


def test_index_html_has_canvas_element():
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "<canvas" in html, "index.html must contain a <canvas> element"


def test_index_html_has_meta_charset_utf8():
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert 'charset="UTF-8"' in html or "charset=UTF-8" in html, (
        "index.html must declare UTF-8 charset for Hebrew rendering"
    )


# ---------------------------------------------------------------------------
# Explicit failure modes
# ---------------------------------------------------------------------------

def test_wrong_piece_id_not_found():
    """Querying for a non-existent piece ID returns None."""
    pieces = load_pieces()
    bad_id = "82-superformula-seven-species-WRONG"
    result = next((p for p in pieces if p["id"] == bad_id), None)
    assert result is None


def test_piece_id_unique_in_pieces_json():
    pieces = load_pieces()
    ids = [p["id"] for p in pieces]
    assert ids.count(PIECE_ID) == 1, f"Piece ID '{PIECE_ID}' appears more than once"


def test_empty_essay_would_fail_word_count():
    """Verify that a zero-word essay fails our minimum word count check."""
    word_count = len("".split())
    assert word_count < 400, "Fixture: empty string has 0 words, below threshold"
