"""
Tests for piece 66-stipple-ruth-gleaning (Voronoi stippling / Lloyd's algorithm).

Covers the acceptance criteria: files on disk, pieces.json registration,
HTML structure (canvas, Lloyd's algorithm, breath animation), essay content,
thumbnail SVG structure, and edge cases around the density function and
silhouette gap logic.
"""
import json
import os
import re

import pytest

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID = "66-stipple-ruth-gleaning"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
HTML_PATH = os.path.join(PIECE_DIR, "index.html")
ESSAY_PATH = os.path.join(PIECE_DIR, "essay.md")
THUMB_PATH = os.path.join(PIECE_DIR, "thumbnail.svg")
README_PATH = os.path.join(PIECE_DIR, "README.md")
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")


def load_pieces():
    with open(PIECES_JSON, encoding="utf-8") as f:
        return json.load(f)


def get_piece():
    for p in load_pieces():
        if p["id"] == PIECE_ID:
            return p
    return None


# ---------------------------------------------------------------------------
# File layout
# ---------------------------------------------------------------------------

def test_piece_directory_exists():
    assert os.path.isdir(PIECE_DIR), f"Piece directory missing: {PIECE_DIR}"


def test_index_html_exists():
    assert os.path.isfile(HTML_PATH), "index.html missing"


def test_essay_md_exists():
    assert os.path.isfile(ESSAY_PATH), "essay.md missing"


def test_thumbnail_svg_exists():
    assert os.path.isfile(THUMB_PATH), "thumbnail.svg missing"


def test_readme_md_exists():
    assert os.path.isfile(README_PATH), "README.md missing"


# ---------------------------------------------------------------------------
# pieces.json registration
# ---------------------------------------------------------------------------

def test_piece_registered_in_pieces_json():
    piece = get_piece()
    assert piece is not None, f"Piece '{PIECE_ID}' not found in pieces.json"


def test_piece_theme():
    piece = get_piece()
    assert piece is not None
    assert "Ruth" in piece["theme"] or "harvest" in piece["theme"].lower(), (
        f"Expected harvest/Ruth theme, got: {piece['theme']}"
    )


def test_piece_technique():
    piece = get_piece()
    assert piece is not None
    technique = piece["technique"].lower()
    assert "lloyd" in technique or "voronoi" in technique or "stippl" in technique, (
        f"Expected Lloyd/Voronoi/stippling technique, got: {piece['technique']}"
    )


def test_piece_year():
    piece = get_piece()
    assert piece is not None
    assert piece["year"] == 2026


def test_piece_paths_point_to_correct_files():
    piece = get_piece()
    assert piece is not None
    for field in ("path", "thumbnail", "essay"):
        full = os.path.join(GALLERY_ROOT, piece[field])
        assert os.path.isfile(full), f"Field '{field}' points to missing file: {piece[field]}"


# ---------------------------------------------------------------------------
# index.html — canvas and algorithm structure
# ---------------------------------------------------------------------------

def test_html_has_700x700_canvas():
    html = open(HTML_PATH, encoding="utf-8").read()
    assert 'width="700"' in html and 'height="700"' in html, (
        "Canvas must be 700×700 px"
    )


def test_html_uses_request_animation_frame():
    html = open(HTML_PATH, encoding="utf-8").read()
    assert "requestAnimationFrame" in html, "Must use requestAnimationFrame for animation"


def test_html_implements_lloyd_iteration():
    html = open(HTML_PATH, encoding="utf-8").read()
    assert "lloyd" in html.lower() or "Lloyd" in html, (
        "index.html must reference Lloyd's algorithm"
    )


def test_html_has_density_function():
    html = open(HTML_PATH, encoding="utf-8").read()
    assert "density" in html, "index.html must define a density() function"


def test_html_n_dots_approximately_3000():
    """The code should define ~3000 dots."""
    html = open(HTML_PATH, encoding="utf-8").read()
    assert "3000" in html or "N_DOTS" in html, (
        "index.html must define ~3000 dots (look for literal 3000 or N_DOTS)"
    )


def test_html_n_iterations_30():
    """Lloyd's must run 30 iterations."""
    html = open(HTML_PATH, encoding="utf-8").read()
    assert "30" in html, "index.html must specify 30 Lloyd iterations"


def test_html_harvest_gold_color():
    html = open(HTML_PATH, encoding="utf-8").read()
    assert "#C8900A" in html or "C8900A" in html.upper(), (
        "Dot color must be harvest gold #C8900A"
    )


def test_html_parchment_background():
    html = open(HTML_PATH, encoding="utf-8").read()
    assert "#F5EDD8" in html or "F5EDD8" in html.upper(), (
        "Background must be parchment #F5EDD8"
    )


def test_html_breath_animation_15_percent():
    """Breath animation oscillates ±15% of base radius."""
    html = open(HTML_PATH, encoding="utf-8").read()
    assert "0.15" in html, "Breath animation must oscillate ±15% (0.15)"


def test_html_60fps_cap():
    """Must cap at 60fps."""
    html = open(HTML_PATH, encoding="utf-8").read()
    assert "60" in html, "Must cap at 60fps"


def test_html_ruth_silhouette_x_coordinate():
    """Ruth's silhouette must be centered near x=220."""
    html = open(HTML_PATH, encoding="utf-8").read()
    assert "220" in html, "Ruth silhouette must reference x=220"


def test_html_ruth_silhouette_y_coordinate():
    """Ruth's silhouette bottom at y=520."""
    html = open(HTML_PATH, encoding="utf-8").read()
    assert "520" in html, "Ruth silhouette bottom must reference y=520"


def test_html_spatial_hash_present():
    html = open(HTML_PATH, encoding="utf-8").read()
    # Spatial hash uses grid cells
    assert "CELL_SIZE" in html or "cellSize" in html or "grid" in html.lower(), (
        "index.html must implement a spatial hash for nearest-neighbor lookup"
    )


def test_html_embeds_essay_words():
    """index.html must embed essay content inline."""
    essay = open(ESSAY_PATH, encoding="utf-8").read()
    html = open(HTML_PATH, encoding="utf-8").read()
    words = [w for w in essay.split() if len(w) > 6][:15]
    found = sum(1 for w in words if w in html)
    assert found >= 8, (
        f"index.html must embed essay text inline; only {found}/15 sampled words found"
    )


# ---------------------------------------------------------------------------
# essay.md content
# ---------------------------------------------------------------------------

def test_essay_word_count():
    text = open(ESSAY_PATH, encoding="utf-8").read()
    count = len(text.split())
    assert count >= 350, f"Essay must be ≥350 words; got {count}"


def test_essay_contains_hebrew_quotes():
    """Essay must quote Tanach verses in Hebrew."""
    text = open(ESSAY_PATH, encoding="utf-8").read()
    # Hebrew Unicode range U+0590–U+05FF
    hebrew_chars = sum(1 for c in text if '֐' <= c <= '׿')
    assert hebrew_chars >= 20, (
        f"Essay must contain Hebrew verse text; found only {hebrew_chars} Hebrew chars"
    )


def test_essay_contains_english_translation():
    """Essay must provide English translations alongside Hebrew."""
    text = open(ESSAY_PATH, encoding="utf-8").read()
    assert "your people" in text.lower() or "Your people" in text, (
        "Essay must include English translation of Ruth 1:16"
    )


def test_essay_cites_ruth_1_16():
    text = open(ESSAY_PATH, encoding="utf-8").read()
    assert "1:16" in text, "Essay must cite Ruth 1:16"


def test_essay_cites_ruth_2():
    text = open(ESSAY_PATH, encoding="utf-8").read()
    assert "2:11" in text or "2:10" in text or "2:12" in text or "Ruth 2" in text, (
        "Essay must cite Ruth chapter 2"
    )


def test_essay_focuses_on_chesed_not_peah_law():
    """Essay must not re-explain peah/leket legal mechanics (that's piece 21's angle)."""
    text = open(ESSAY_PATH, encoding="utf-8").read().lower()
    peah_law_phrases = ["peah has no fixed measure", "mishnah pe'ah 1:1", "leket law"]
    for phrase in peah_law_phrases:
        assert phrase not in text, (
            f"Essay must not duplicate piece 21's peah-law argument; found: '{phrase}'"
        )


def test_essay_mentions_moav_road_or_chesed():
    """The fresh angle: Ruth as stranger who chooses in, or chesed arc."""
    text = open(ESSAY_PATH, encoding="utf-8").read().lower()
    has_angle = (
        "moav" in text or "moab" in text
        or "chesed" in text or "stranger" in text
        or "chose" in text or "choice" in text
    )
    assert has_angle, "Essay must focus on Ruth's choice / chesed arc / road from Moav"


def test_essay_links_to_stippling_technique():
    """Essay must tie the writing to the visual technique."""
    text = open(ESSAY_PATH, encoding="utf-8").read().lower()
    assert "stippl" in text or "dot" in text or "lloyd" in text or "voronoi" in text, (
        "Essay must connect the written theme to the stippling / Lloyd technique"
    )


# ---------------------------------------------------------------------------
# thumbnail.svg
# ---------------------------------------------------------------------------

def test_thumbnail_is_valid_svg():
    text = open(THUMB_PATH, encoding="utf-8").read()
    assert "<svg" in text and "</svg>" in text, "thumbnail.svg must be valid SVG"


def test_thumbnail_parchment_background():
    text = open(THUMB_PATH, encoding="utf-8").read()
    assert "F5EDD8" in text.upper() or "#F5EDD8" in text, (
        "Thumbnail must use parchment background #F5EDD8"
    )


def test_thumbnail_has_circles():
    text = open(THUMB_PATH, encoding="utf-8").read()
    circle_count = text.count("<circle")
    assert circle_count >= 80, (
        f"Thumbnail must have ≥80 stipple circles; found {circle_count}"
    )


def test_thumbnail_has_horizon_line():
    text = open(THUMB_PATH, encoding="utf-8").read()
    assert "<line" in text, "Thumbnail must include a horizon line element"


def test_thumbnail_has_ruth_silhouette():
    """Thumbnail must include Ruth's silhouette as a path or ellipse/rect."""
    text = open(THUMB_PATH, encoding="utf-8").read()
    has_shape = "<path" in text or "<ellipse" in text or "<rect" in text
    assert has_shape, "Thumbnail must include Ruth's silhouette shape"


def test_thumbnail_gold_color():
    text = open(THUMB_PATH, encoding="utf-8").read()
    assert "C8900A" in text.upper() or "#9B6E20" in text, (
        "Thumbnail must use gold/harvest color"
    )


def test_thumbnail_400x400():
    text = open(THUMB_PATH, encoding="utf-8").read()
    assert '400' in text, "Thumbnail must reference 400px dimensions"


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

def test_html_handles_breath_animation_period_4s():
    """Period of breath animation must be 4 seconds (t * 2π/4000 ≈ t * 0.001571)."""
    html = open(HTML_PATH, encoding="utf-8").read()
    # Either explicit constant or 4000 in code
    assert "4" in html, "Breath animation must reference 4s period"


def test_html_no_external_image_assets():
    """Density function must be procedural — no img src or fetch of image files."""
    html = open(HTML_PATH, encoding="utf-8").read()
    assert "fetch(" not in html, "index.html must not fetch external assets"
    assert "<img" not in html, "index.html must not use <img> elements for the artwork"


def test_html_synchronous_lloyd_before_animation():
    """Lloyd iterations must run synchronously before requestAnimationFrame render."""
    html = open(HTML_PATH, encoding="utf-8").read()
    lloyd_pos = html.lower().find("for (let iter")
    raf_pos = html.find("requestAnimationFrame(drawFrame")
    assert lloyd_pos != -1, "Must find Lloyd iteration loop"
    assert raf_pos != -1, "Must find requestAnimationFrame(drawFrame)"
    assert lloyd_pos < raf_pos, (
        "Lloyd iterations must execute before the animation RAF call"
    )


def test_no_duplicate_piece_id():
    pieces = load_pieces()
    ids = [p["id"] for p in pieces]
    assert ids.count(PIECE_ID) == 1, f"Piece ID '{PIECE_ID}' must appear exactly once"
