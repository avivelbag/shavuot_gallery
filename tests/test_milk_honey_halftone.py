"""
Tests for piece 52-milk-and-honey (Halftone Drip).

Validates that the piece is correctly registered in pieces.json, all required
files are present on disk, and the index.html implements the specified
canvas 2D halftone technique with the correct palette and animation.
"""
import json
import os

import pytest

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")
PIECE_ID = "52-milk-and-honey"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)


def load_pieces():
    """Load pieces.json and return the list."""
    with open(PIECES_JSON, encoding="utf-8") as fh:
        return json.load(fh)


def get_piece():
    """Return the pieces.json entry for piece 52, or None if absent."""
    for p in load_pieces():
        if p["id"] == PIECE_ID:
            return p
    return None


def read_file(rel_path):
    """Read a file relative to GALLERY_ROOT."""
    return open(os.path.join(GALLERY_ROOT, rel_path), encoding="utf-8").read()


# ---------------------------------------------------------------------------
# Registration in pieces.json
# ---------------------------------------------------------------------------

def test_piece_52_in_pieces_json():
    """Piece 52-milk-and-honey must appear in pieces.json."""
    assert get_piece() is not None, f"Piece '{PIECE_ID}' not found in pieces.json"


def test_piece_52_required_fields():
    """All required fields must be present and non-empty."""
    piece = get_piece()
    if piece is None:
        pytest.skip("Piece not registered")
    for field in ("id", "title", "tagline", "year", "theme", "technique", "path", "thumbnail", "essay"):
        assert field in piece and piece[field], f"Field '{field}' missing or empty"


def test_piece_52_year_is_int():
    piece = get_piece()
    if piece is None:
        pytest.skip("Piece not registered")
    assert isinstance(piece["year"], int), "year must be an integer"


def test_piece_52_path_format():
    """Path must point to pieces/52-milk-and-honey/index.html."""
    piece = get_piece()
    if piece is None:
        pytest.skip("Piece not registered")
    assert piece["path"] == "pieces/52-milk-and-honey/index.html"


def test_piece_52_technique_is_halftone():
    """Technique field must mention halftone dot-screen to distinguish from other pieces."""
    piece = get_piece()
    if piece is None:
        pytest.skip("Piece not registered")
    assert "halftone" in piece["technique"].lower(), (
        "Technique must mention halftone to distinguish from piece 07 (reaction-diffusion)"
    )


def test_piece_52_is_not_reaction_diffusion():
    """Must not be registered as reaction-diffusion (that is piece 07)."""
    piece = get_piece()
    if piece is None:
        pytest.skip("Piece not registered")
    assert "reaction" not in piece["technique"].lower(), (
        "Piece 52 must not use reaction-diffusion technique (already used by piece 07)"
    )


# ---------------------------------------------------------------------------
# Files on disk
# ---------------------------------------------------------------------------

def test_index_html_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "index.html")), \
        "pieces/52-milk-and-honey/index.html must exist"


def test_essay_md_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "essay.md")), \
        "pieces/52-milk-and-honey/essay.md must exist"


def test_thumbnail_exists():
    piece = get_piece()
    if piece is None:
        pytest.skip("Piece not registered")
    thumb = os.path.join(GALLERY_ROOT, piece["thumbnail"])
    assert os.path.isfile(thumb), f"Thumbnail '{piece['thumbnail']}' does not exist"


def test_readme_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "README.md")), \
        "pieces/52-milk-and-honey/README.md must exist"


def test_thumbnail_is_svg_or_png():
    piece = get_piece()
    if piece is None:
        pytest.skip("Piece not registered")
    ext = os.path.splitext(piece["thumbnail"])[1].lower()
    assert ext in (".svg", ".png"), f"Thumbnail extension {ext!r} is not .svg or .png"


def test_thumbnail_svg_is_valid():
    """If thumbnail is SVG, it must contain svg tags and a rect for the background."""
    piece = get_piece()
    if piece is None:
        pytest.skip("Piece not registered")
    thumb_path = os.path.join(GALLERY_ROOT, piece["thumbnail"])
    if not thumb_path.endswith(".svg"):
        pytest.skip("Thumbnail is not SVG")
    text = open(thumb_path, encoding="utf-8").read()
    assert "<svg" in text and "</svg>" in text, "thumbnail.svg must be valid SVG"
    assert "<circle" in text, "thumbnail.svg must contain halftone circles"


# ---------------------------------------------------------------------------
# index.html — canvas technique
# ---------------------------------------------------------------------------

def _html():
    return read_file("pieces/52-milk-and-honey/index.html")


def test_uses_requestanimationframe():
    """Animation loop must use requestAnimationFrame."""
    assert "requestAnimationFrame" in _html()


def test_uses_canvas_arc():
    """Halftone dots must be drawn with ctx.arc (not CSS or SVG filters)."""
    assert "ctx.arc" in _html(), "Halftone dots must use ctx.arc()"


def test_no_css_filter():
    """Must not use CSS filter property for halftone effect."""
    html = _html()
    assert "filter:" not in html and "filter :" not in html, \
        "index.html must not use CSS filter for halftone"


def test_cream_background_color():
    """Background must be cream #FFF8E7."""
    assert "#FFF8E7" in _html() or "#fff8e7" in _html().lower()


def test_honey_color_present():
    """Honey amber color #C97B00 must appear in the animation code."""
    html = _html()
    assert "C97B00" in html or "c97b00" in html.lower(), \
        "index.html must contain honey color #C97B00"


def test_honey_color_range():
    """Brighter honey color #E8A020 must also appear (color lerp range)."""
    html = _html()
    assert "E8A020" in html or "e8a020" in html.lower(), \
        "index.html must contain #E8A020 (bright end of honey color range)"


def test_milk_color_present():
    """Milk dot color must appear in the animation code."""
    html = _html()
    assert (
        "D0D8F0" in html or "d0d8f0" in html.lower() or
        "208,216,240" in html or "208, 216, 240" in html
    ), "index.html must contain milk dot color D0D8F0 / rgb(208,216,240)"


def test_drip_speed_constant():
    """Drip speed of ~30 px/s must be encoded in the animation constants."""
    html = _html()
    assert "30" in html, "index.html must encode drip speed of 30 px/s"


def test_sine_wave_for_drip_front():
    """Drip front must use Math.sin for the sinusoidal shape."""
    assert "Math.sin" in _html(), "Drip front must use Math.sin for sinusoidal variation"


def test_two_layer_variable_names():
    """Code must contain variables for both honey and milk density."""
    html = _html()
    assert ("hd" in html or "honey" in html.lower()) and \
           ("md" in html or "milk" in html.lower()), \
        "index.html must name density variables for both honey and milk layers"


def test_canvas_element_present():
    assert '<canvas' in _html(), "index.html must contain a <canvas> element"


def test_essay_panel_present():
    """Essay must be in a readable panel, not just hidden."""
    assert "essay" in _html().lower(), "index.html must contain an essay panel"


# ---------------------------------------------------------------------------
# essay.md — content requirements
# ---------------------------------------------------------------------------

def _essay():
    return read_file("pieces/52-milk-and-honey/essay.md")


def test_essay_word_count():
    """Essay must have at least 200 words."""
    words = _essay().split()
    assert len(words) >= 200, f"Essay has only {len(words)} words (need ≥ 200)"


def test_essay_cites_exodus_3():
    """Essay must cite Exodus 3:8 (the promise of the Land)."""
    essay = _essay()
    assert "Exodus 3" in essay or "Exodus 3:8" in essay, \
        "essay.md must cite Exodus 3:8"


def test_essay_cites_deuteronomy_26():
    """Essay must cite Deuteronomy 26 (the Bikkurim declaration)."""
    assert "Deuteronomy 26" in _essay(), "essay.md must cite Deuteronomy 26"


def test_essay_cites_deuteronomy_32():
    """Essay must cite Deuteronomy 32:13 (honey from the rock)."""
    assert "Deuteronomy 32" in _essay(), "essay.md must cite Deuteronomy 32:13"


def test_essay_mentions_bikkurim():
    """Essay must discuss the Bikkurim / first fruits context."""
    essay = _essay().lower()
    assert "bikkurim" in essay or "first fruits" in essay, \
        "essay.md must discuss Bikkurim / first fruits"


def test_essay_mentions_dairy_custom():
    """Essay must mention the Shavuot dairy custom."""
    essay = _essay().lower()
    assert "dairy" in essay or "cheese" in essay or "milk" in essay, \
        "essay.md must mention the dairy food custom on Shavuot"


def test_essay_mentions_two_substances():
    """Essay must discuss both milk and honey as distinct substances."""
    essay = _essay().lower()
    assert "milk" in essay and "honey" in essay, \
        "essay.md must discuss both milk and honey"


def test_essay_embedded_in_html():
    """Key words from essay.md must appear in index.html (embedded, not fetched)."""
    essay_words = [w for w in _essay().split() if len(w) > 6][:15]
    html = _html()
    found = sum(1 for w in essay_words if w in html)
    assert found >= 7, (
        f"Only {found}/15 essay words found in index.html; "
        "essay text must be embedded in the HTML"
    )


# ---------------------------------------------------------------------------
# README
# ---------------------------------------------------------------------------

def test_readme_mentions_bikkurim():
    readme = read_file("pieces/52-milk-and-honey/README.md").lower()
    assert "bikkurim" in readme or "milk" in readme, \
        "README.md must mention the Bikkurim or milk/honey theme"


def test_readme_mentions_technique():
    readme = read_file("pieces/52-milk-and-honey/README.md").lower()
    assert "halftone" in readme or "canvas" in readme, \
        "README.md must mention the halftone/canvas technique"


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

def test_no_duplicate_id_52():
    """Piece id 52-milk-and-honey must appear exactly once in pieces.json."""
    pieces = load_pieces()
    matches = [p for p in pieces if p["id"] == PIECE_ID]
    assert len(matches) == 1, f"Expected exactly one entry for '{PIECE_ID}', found {len(matches)}"


def test_pieces_json_still_valid_array():
    """Adding piece 52 must not corrupt pieces.json."""
    pieces = load_pieces()
    assert isinstance(pieces, list) and len(pieces) > 0


def test_animation_resets_drip():
    """The animation code must contain logic to reset dripY to 0 for the cycle."""
    html = _html()
    assert "dripY = 0" in html or "drip_y = 0" in html or "dripY=0" in html, \
        "index.html must reset the drip position to restart the cycle"


def test_fade_phase_present():
    """The animation must implement a fade phase before reset."""
    html = _html()
    assert "fading" in html or "fade" in html.lower(), \
        "index.html must implement a fade-out phase before cycle reset"
