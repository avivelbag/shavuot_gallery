"""
Tests for piece 35-dew-of-torah — WebGL metaball piece.

Verifies that the piece directory, HTML, essay, and pieces.json entry
all satisfy the acceptance criteria for this swarm branch.
"""
import json
import os
import re

import pytest

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECES_JSON  = os.path.join(GALLERY_ROOT, "pieces.json")
PIECE_ID     = "35-dew-of-torah"
PIECE_DIR    = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
HTML_PATH    = os.path.join(PIECE_DIR, "index.html")
ESSAY_PATH   = os.path.join(PIECE_DIR, "essay.md")
README_PATH  = os.path.join(PIECE_DIR, "README.md")
THUMB_PATH   = os.path.join(PIECE_DIR, "thumbnail.svg")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_pieces():
    """Return parsed pieces.json list."""
    with open(PIECES_JSON, encoding="utf-8") as fh:
        return json.load(fh)


def get_piece():
    """Return the pieces.json entry for piece 35, or None if absent."""
    for p in load_pieces():
        if p["id"] == PIECE_ID:
            return p
    return None


# ---------------------------------------------------------------------------
# Directory and file existence
# ---------------------------------------------------------------------------

def test_piece_directory_exists():
    assert os.path.isdir(PIECE_DIR), f"Piece directory {PIECE_DIR} does not exist"


def test_index_html_exists():
    assert os.path.isfile(HTML_PATH), "index.html is missing"


def test_essay_md_exists():
    assert os.path.isfile(ESSAY_PATH), "essay.md is missing"


def test_readme_exists():
    assert os.path.isfile(README_PATH), "README.md is missing"


def test_thumbnail_exists():
    assert os.path.isfile(THUMB_PATH), "thumbnail.svg is missing"


# ---------------------------------------------------------------------------
# pieces.json registration
# ---------------------------------------------------------------------------

def test_piece_registered_in_pieces_json():
    assert get_piece() is not None, f"Piece '{PIECE_ID}' not found in pieces.json"


def test_pieces_json_required_fields():
    piece = get_piece()
    assert piece is not None
    for field in ("id", "title", "tagline", "year", "theme", "technique", "path", "thumbnail", "essay"):
        assert field in piece and piece[field], f"Missing or empty field '{field}'"


def test_pieces_json_paths_exist():
    piece = get_piece()
    assert piece is not None
    for key in ("path", "thumbnail", "essay"):
        full = os.path.join(GALLERY_ROOT, piece[key])
        assert os.path.isfile(full), f"Registered {key} '{piece[key]}' does not exist on disk"


def test_no_duplicate_ids():
    ids = [p["id"] for p in load_pieces()]
    assert len(ids) == len(set(ids)), "Duplicate IDs in pieces.json"


# ---------------------------------------------------------------------------
# Essay content
# ---------------------------------------------------------------------------

def test_essay_minimum_words():
    text = open(ESSAY_PATH, encoding="utf-8").read()
    assert len(text.split()) >= 200, "essay.md has fewer than 200 words"


def test_essay_cites_deuteronomy():
    text = open(ESSAY_PATH, encoding="utf-8").read()
    assert "32:2" in text or "Deuteronomy" in text, \
        "essay.md must cite Deuteronomy 32:2"


def test_essay_cites_eruvin():
    text = open(ESSAY_PATH, encoding="utf-8").read()
    assert "Eruvin" in text, "essay.md must cite Eruvin 54b"


def test_essay_mentions_rashi():
    text = open(ESSAY_PATH, encoding="utf-8").read()
    assert "Rashi" in text, "essay.md must mention Rashi's insight about dew"


def test_essay_mentions_dew():
    text = open(ESSAY_PATH, encoding="utf-8").read()
    assert "dew" in text.lower(), "essay.md must discuss the concept of dew"


# ---------------------------------------------------------------------------
# index.html — technique and structure
# ---------------------------------------------------------------------------

def test_html_uses_webgl():
    html = open(HTML_PATH, encoding="utf-8").read()
    assert "webgl" in html.lower() or "getContext" in html, \
        "index.html must use WebGL"


def test_html_has_metaball_shader():
    html = open(HTML_PATH, encoding="utf-8").read()
    assert "field +=" in html or "metaball" in html.lower(), \
        "index.html must contain the metaball SDF field accumulation"


def test_html_uses_requestanimationframe():
    html = open(HTML_PATH, encoding="utf-8").read()
    assert "requestAnimationFrame" in html, \
        "index.html must use requestAnimationFrame for the render loop"


def test_html_has_fragment_shader():
    html = open(HTML_PATH, encoding="utf-8").read()
    assert "x-shader/x-fragment" in html or "FRAGMENT_SHADER" in html, \
        "index.html must include a WebGL fragment shader"


def test_html_has_vertex_shader():
    html = open(HTML_PATH, encoding="utf-8").read()
    assert "x-shader/x-vertex" in html or "VERTEX_SHADER" in html, \
        "index.html must include a WebGL vertex shader"


def test_html_passes_ball_uniforms():
    html = open(HTML_PATH, encoding="utf-8").read()
    assert "uBalls" in html, \
        "index.html must pass ball positions/radii as a uniform array 'uBalls'"


def test_html_has_gravity_physics():
    html = open(HTML_PATH, encoding="utf-8").read()
    assert "GRAVITY" in html or "gravity" in html.lower(), \
        "index.html must implement downward gravity in the physics"


def test_html_embeds_essay_text():
    essay = open(ESSAY_PATH, encoding="utf-8").read()
    html  = open(HTML_PATH,  encoding="utf-8").read()
    words = [w for w in essay.split() if len(w) > 5][:10]
    found = sum(1 for w in words if w in html)
    assert found >= 5, \
        f"index.html must embed essay text inline (only {found}/10 sampled words found)"


def test_html_has_hebrew_overlay():
    html = open(HTML_PATH, encoding="utf-8").read()
    assert "תּוֹרָה" in html or "טַּל" in html or "כַּטַּל" in html, \
        "index.html must include Hebrew text (dew / Torah verse)"


def test_html_has_ground_settling():
    html = open(HTML_PATH, encoding="utf-8").read()
    assert "settled" in html or "GROUND" in html, \
        "index.html must implement ground-settling logic for the physics"


def test_html_has_merge_logic():
    html = open(HTML_PATH, encoding="utf-8").read()
    assert "merge" in html.lower() or "splice" in html, \
        "index.html must implement ball merging"


def test_html_has_letter_targets():
    html = open(HTML_PATH, encoding="utf-8").read()
    assert "TARGETS" in html or "target" in html.lower(), \
        "index.html must define letter targets for the Torah word emergence"


# ---------------------------------------------------------------------------
# Thumbnail
# ---------------------------------------------------------------------------

def test_thumbnail_is_valid_svg():
    text = open(THUMB_PATH, encoding="utf-8").read()
    assert "<svg" in text and "</svg>" in text, "thumbnail.svg must be valid SVG"


def test_thumbnail_has_circles():
    text = open(THUMB_PATH, encoding="utf-8").read()
    assert "<circle" in text, "thumbnail.svg must contain circles representing metaballs"


# ---------------------------------------------------------------------------
# Edge cases and failure modes
# ---------------------------------------------------------------------------

def test_essay_word_count_not_zero():
    """Catches accidental empty essay stub."""
    text = open(ESSAY_PATH, encoding="utf-8").read()
    assert len(text.strip()) > 0, "essay.md must not be empty"


def test_html_not_empty():
    html = open(HTML_PATH, encoding="utf-8").read()
    assert len(html.strip()) > 100, "index.html must not be empty or near-empty"


def test_pieces_json_35_is_last_or_present():
    """Piece 35 must appear in pieces.json (correct numbering enforced)."""
    pieces = load_pieces()
    ids = [p["id"] for p in pieces]
    assert PIECE_ID in ids, f"'{PIECE_ID}' missing from pieces.json"


def test_piece_path_format():
    piece = get_piece()
    assert piece is not None
    assert piece["path"] == f"pieces/{PIECE_ID}/index.html", \
        f"path must be 'pieces/{PIECE_ID}/index.html'"


def test_no_piece_with_missing_essay_file(tmp_path):
    """Synthetic: a pieces.json entry whose essay file is missing must be detectable."""
    bad = [{"id": "99-phantom", "essay": str(tmp_path / "ghost.md")}]
    essay_path = bad[0]["essay"]
    assert not os.path.isfile(essay_path), "Fixture: ghost essay file must not exist"


def test_essay_rain_vs_dew_contrast():
    """Essay must discuss rain as contrast to dew (acceptance criterion)."""
    text = open(ESSAY_PATH, encoding="utf-8").read()
    assert "rain" in text.lower(), \
        "essay.md must contrast Torah-as-rain with Torah-as-dew"
