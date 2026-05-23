"""
Tests for piece 95-burning-ship-sinai-fire.

Verifies the required file layout, pieces.json registration, WebGL
fragment-shader correctness markers, bilingual essay content, and
the Burning Ship iteration formula presence.
"""
import json
import os
import re

import pytest

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID     = "95-burning-ship-sinai-fire"
PIECE_DIR    = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_pieces():
    """Load and return parsed pieces.json."""
    path = os.path.join(GALLERY_ROOT, "pieces.json")
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def get_piece():
    """Return the pieces.json entry for the Burning Ship piece, or None."""
    for p in load_pieces():
        if p["id"] == PIECE_ID:
            return p
    return None


def read_file(rel_path):
    """Read a file relative to the gallery root; return its text."""
    return open(os.path.join(GALLERY_ROOT, rel_path), encoding="utf-8").read()


# ---------------------------------------------------------------------------
# pieces.json registration — happy path
# ---------------------------------------------------------------------------

def test_piece_registered_in_pieces_json():
    """The Burning Ship piece must appear in pieces.json."""
    assert get_piece() is not None, f"'{PIECE_ID}' not found in pieces.json"


def test_piece_has_all_required_fields():
    """Every required pieces.json field must be present and non-empty."""
    piece = get_piece()
    assert piece is not None
    required = ("id", "title", "tagline", "year", "theme", "technique",
                "path", "thumbnail", "essay")
    for field in required:
        val = piece.get(field)
        assert val is not None and val != "", (
            f"pieces.json field '{field}' is missing or empty"
        )


def test_theme_mentions_sinai_fire():
    """Theme field must reference Sinai or fire."""
    piece = get_piece()
    assert piece is not None
    theme = piece.get("theme", "").lower()
    assert "sinai" in theme or "fire" in theme, (
        f"Expected theme to mention Sinai or fire; got: {piece['theme']!r}"
    )


def test_technique_mentions_burning_ship():
    """Technique field must mention Burning Ship."""
    piece = get_piece()
    assert piece is not None
    technique = piece.get("technique", "").lower()
    assert "burning ship" in technique, (
        f"Expected technique to mention 'Burning Ship'; got: {piece['technique']!r}"
    )


def test_year_is_integer():
    """Year must be an integer."""
    piece = get_piece()
    assert piece is not None
    assert isinstance(piece["year"], int), f"year must be int, got {piece['year']!r}"


# ---------------------------------------------------------------------------
# File layout — happy path
# ---------------------------------------------------------------------------

def test_piece_directory_exists():
    """pieces/95-burning-ship-sinai-fire/ must exist."""
    assert os.path.isdir(PIECE_DIR), f"Piece directory not found: {PIECE_DIR}"


def test_index_html_exists():
    """index.html must be present in the piece directory."""
    path = os.path.join(PIECE_DIR, "index.html")
    assert os.path.isfile(path), f"Missing: {path}"


def test_essay_md_exists():
    """essay.md must be present in the piece directory."""
    path = os.path.join(PIECE_DIR, "essay.md")
    assert os.path.isfile(path), f"Missing: {path}"


def test_thumbnail_svg_exists():
    """thumbnail.svg must be present in the piece directory."""
    path = os.path.join(PIECE_DIR, "thumbnail.svg")
    assert os.path.isfile(path), f"Missing: {path}"


def test_readme_exists():
    """README.md must be present in the piece directory."""
    path = os.path.join(PIECE_DIR, "README.md")
    assert os.path.isfile(path), f"Missing: {path}"


def test_pieces_json_path_points_to_existing_html():
    """The 'path' field in pieces.json must resolve to an existing file."""
    piece = get_piece()
    assert piece is not None
    full = os.path.join(GALLERY_ROOT, piece["path"])
    assert os.path.isfile(full), f"path '{piece['path']}' does not exist on disk"


def test_pieces_json_thumbnail_points_to_existing_file():
    """The 'thumbnail' field must resolve to an existing file."""
    piece = get_piece()
    assert piece is not None
    full = os.path.join(GALLERY_ROOT, piece["thumbnail"])
    assert os.path.isfile(full), (
        f"thumbnail '{piece['thumbnail']}' does not exist on disk"
    )


def test_pieces_json_essay_points_to_existing_file():
    """The 'essay' field must resolve to an existing file."""
    piece = get_piece()
    assert piece is not None
    full = os.path.join(GALLERY_ROOT, piece["essay"])
    assert os.path.isfile(full), (
        f"essay '{piece['essay']}' does not exist on disk"
    )


# ---------------------------------------------------------------------------
# essay.md content
# ---------------------------------------------------------------------------

def test_essay_is_substantial():
    """essay.md must have at least 300 words."""
    text = read_file(os.path.join("pieces", PIECE_ID, "essay.md"))
    count = len(text.split())
    assert count >= 300, f"essay.md has only {count} words (need ≥ 300)"


def test_essay_mentions_deuteronomy():
    """essay.md must cite Deuteronomy 4:11 or 4:12."""
    text = read_file(os.path.join("pieces", PIECE_ID, "essay.md"))
    assert re.search(r"Deuteronomy\s+4[:.]1[12]", text, re.IGNORECASE), (
        "essay.md must cite Deuteronomy 4:11 or 4:12"
    )


def test_essay_contains_hebrew_characters():
    """essay.md must contain Hebrew script (Unicode block U+0590–U+05FF)."""
    text = read_file(os.path.join("pieces", PIECE_ID, "essay.md"))
    has_hebrew = any('֐' <= ch <= '׿' for ch in text)
    assert has_hebrew, "essay.md must include Hebrew text"


def test_essay_mentions_burning_ship():
    """essay.md must name the Burning Ship fractal."""
    text = read_file(os.path.join("pieces", PIECE_ID, "essay.md"))
    assert "Burning Ship" in text, "essay.md must mention the Burning Ship fractal"


def test_essay_mentions_unconsumed():
    """essay.md must explain the interior / unconsumed core concept."""
    text = read_file(os.path.join("pieces", PIECE_ID, "essay.md"))
    lower = text.lower()
    assert "unconsumed" in lower or "interior" in lower or "bounded" in lower, (
        "essay.md must discuss the unconsumed interior of the fractal"
    )


# ---------------------------------------------------------------------------
# index.html content
# ---------------------------------------------------------------------------

def test_html_embeds_essay_text():
    """index.html must embed the essay body (not fetch essay.md at runtime)."""
    essay = read_file(os.path.join("pieces", PIECE_ID, "essay.md"))
    html  = read_file(os.path.join("pieces", PIECE_ID, "index.html"))
    words = [w for w in essay.split() if len(w) > 6][:12]
    found = sum(1 for w in words if w in html)
    assert found >= 6, (
        f"index.html does not appear to embed the essay "
        f"(only {found}/12 sampled words found in HTML)"
    )


def test_html_has_webgl_context():
    """index.html must attempt to acquire a WebGL context."""
    html = read_file(os.path.join("pieces", PIECE_ID, "index.html"))
    assert "webgl" in html.lower(), (
        "index.html must call getContext('webgl') for the WebGL renderer"
    )


def test_html_has_burning_ship_iteration():
    """Fragment shader in index.html must contain the abs() fold."""
    html = read_file(os.path.join("pieces", PIECE_ID, "index.html"))
    # The Burning Ship takes abs of z components before squaring
    assert "abs(z.x)" in html or "abs(z" in html, (
        "index.html must contain the Burning Ship abs() fold in the shader"
    )


def test_html_has_smooth_coloring():
    """index.html must use the log-based smooth coloring formula."""
    html = read_file(os.path.join("pieces", PIECE_ID, "index.html"))
    assert "log(" in html, (
        "index.html must contain the log()-based smooth escape-time formula"
    )


def test_html_uses_requestanimationframe():
    """Animation must use requestAnimationFrame."""
    html = read_file(os.path.join("pieces", PIECE_ID, "index.html"))
    assert "requestAnimationFrame" in html, (
        "index.html must use requestAnimationFrame for the render loop"
    )


def test_html_has_tanach_block():
    """index.html must include a bilingual tanach-block with Hebrew text."""
    html = read_file(os.path.join("pieces", PIECE_ID, "index.html"))
    assert "tanach-block" in html, (
        "index.html must contain a .tanach-block element for the Hebrew/English passage"
    )


def test_html_has_hebrew_text():
    """index.html must contain Hebrew characters in the bilingual block."""
    html = read_file(os.path.join("pieces", PIECE_ID, "index.html"))
    has_hebrew = any('֐' <= ch <= '׿' for ch in html)
    assert has_hebrew, "index.html must include Hebrew text in the essay panel"


def test_html_has_deuteronomy_reference():
    """index.html must cite Deuteronomy 4:11 or similar."""
    html = read_file(os.path.join("pieces", PIECE_ID, "index.html"))
    assert re.search(r"Deuteronomy\s+4[:.]1[12]", html, re.IGNORECASE) or \
           re.search(r"4:11", html), (
        "index.html must reference Deuteronomy 4:11 in the essay text"
    )


def test_html_has_canvas_2d_fallback():
    """index.html must include a Canvas 2D fallback path."""
    html = read_file(os.path.join("pieces", PIECE_ID, "index.html"))
    assert "getContext('2d')" in html or 'getContext("2d")' in html, (
        "index.html must include a Canvas 2D fallback"
    )


def test_html_fire_palette_colors_present():
    """index.html must reference the fire palette hex values."""
    html = read_file(os.path.join("pieces", PIECE_ID, "index.html"))
    # Check for at least two of the required fire palette colours
    colors = ["8B0000", "FF4500", "FFD700", "FFFAF0"]
    found = sum(1 for c in colors if c in html.upper())
    assert found >= 2, (
        f"index.html must reference fire palette colours; found only {found}/4"
    )


def test_html_has_animation_zoom():
    """index.html must define start/target viewport for the 8-second animation."""
    html = read_file(os.path.join("pieces", PIECE_ID, "index.html"))
    assert "ANIM_DURATION" in html or "8000" in html, (
        "index.html must define the 8-second animation duration"
    )


# ---------------------------------------------------------------------------
# thumbnail.svg
# ---------------------------------------------------------------------------

def test_thumbnail_is_valid_svg():
    """thumbnail.svg must open with <svg and close with </svg>."""
    text = read_file(os.path.join("pieces", PIECE_ID, "thumbnail.svg"))
    assert "<svg" in text and "</svg>" in text, (
        "thumbnail.svg does not appear to be valid SVG"
    )


def test_thumbnail_has_400x400_dimensions():
    """thumbnail.svg must declare 400×400 dimensions."""
    text = read_file(os.path.join("pieces", PIECE_ID, "thumbnail.svg"))
    assert 'width="400"' in text and 'height="400"' in text, (
        "thumbnail.svg must be 400×400 pixels"
    )


def test_thumbnail_has_hebrew_text():
    """thumbnail.svg must contain the Hebrew citation דברים ד:יא."""
    text = read_file(os.path.join("pieces", PIECE_ID, "thumbnail.svg"))
    assert "דברים" in text, (
        "thumbnail.svg must contain Hebrew text 'דברים' (Deuteronomy)"
    )


# ---------------------------------------------------------------------------
# Edge cases and failure modes
# ---------------------------------------------------------------------------

def test_piece_id_not_duplicate():
    """95-burning-ship-sinai-fire must appear exactly once in pieces.json."""
    pieces = load_pieces()
    count = sum(1 for p in pieces if p["id"] == PIECE_ID)
    assert count == 1, (
        f"'{PIECE_ID}' appears {count} times in pieces.json (expected 1)"
    )


def test_path_ends_with_html():
    """The 'path' field must end with .html."""
    piece = get_piece()
    assert piece is not None
    assert piece["path"].endswith(".html"), (
        f"path must end with .html; got: {piece['path']!r}"
    )


def test_thumbnail_extension_is_svg():
    """Thumbnail must be an SVG file."""
    piece = get_piece()
    assert piece is not None
    assert piece["thumbnail"].endswith(".svg"), (
        f"thumbnail must be .svg; got: {piece['thumbnail']!r}"
    )


def test_missing_piece_returns_none():
    """Helper get_piece returns None for a non-existent ID (sanity check)."""
    pieces = load_pieces()
    result = next((p for p in pieces if p["id"] == "00-nonexistent-piece"), None)
    assert result is None


def test_essay_does_not_mention_placeholder():
    """essay.md must not contain stub placeholder text."""
    text = read_file(os.path.join("pieces", PIECE_ID, "essay.md"))
    lower = text.lower()
    for stub in ("lorem ipsum", "placeholder", "todo", "tbd"):
        assert stub not in lower, (
            f"essay.md contains stub/placeholder text: {stub!r}"
        )
