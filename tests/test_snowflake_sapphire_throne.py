"""
Tests for piece 83-snowflake-sapphire-throne: The Essence of a Sapphire Brick.

Validates the directory layout, pieces.json registration, essay content,
and HTML implementation requirements for the Gravner-Griffeath snowflake piece.
"""
import json
import os
import re

import pytest

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID = "83-snowflake-sapphire-throne"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
HTML_PATH = os.path.join(PIECE_DIR, "index.html")
ESSAY_PATH = os.path.join(PIECE_DIR, "essay.md")
THUMB_PATH = os.path.join(PIECE_DIR, "thumbnail.svg")
README_PATH = os.path.join(PIECE_DIR, "README.md")
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")


def load_pieces():
    """Return the parsed pieces.json list."""
    with open(PIECES_JSON, "r", encoding="utf-8") as fh:
        return json.load(fh)


def get_piece():
    """Return the pieces.json entry for this piece, or None if absent."""
    for p in load_pieces():
        if p["id"] == PIECE_ID:
            return p
    return None


# ---------------------------------------------------------------------------
# File layout
# ---------------------------------------------------------------------------

def test_piece_directory_exists():
    """The piece directory must exist on disk."""
    assert os.path.isdir(PIECE_DIR), f"Missing directory: {PIECE_DIR}"


def test_index_html_exists():
    assert os.path.isfile(HTML_PATH), f"Missing: {HTML_PATH}"


def test_essay_md_exists():
    assert os.path.isfile(ESSAY_PATH), f"Missing: {ESSAY_PATH}"


def test_thumbnail_svg_exists():
    assert os.path.isfile(THUMB_PATH), f"Missing: {THUMB_PATH}"


def test_readme_exists():
    assert os.path.isfile(README_PATH), f"Missing: {README_PATH}"


# ---------------------------------------------------------------------------
# pieces.json registration
# ---------------------------------------------------------------------------

def test_piece_registered_in_pieces_json():
    """The piece must appear in pieces.json."""
    assert get_piece() is not None, f"'{PIECE_ID}' not found in pieces.json"


def test_pieces_json_required_fields():
    """All required fields must be present and non-empty."""
    piece = get_piece()
    assert piece is not None
    for field in ("id", "title", "tagline", "year", "theme", "technique", "path", "thumbnail", "essay"):
        assert piece.get(field), f"pieces.json entry missing or empty field: '{field}'"


def test_pieces_json_theme_mentions_sinai():
    """Theme must reference Sinai / sapphire pavement."""
    piece = get_piece()
    assert piece is not None
    theme = piece["theme"].lower()
    assert "sinai" in theme or "sapphire" in theme, (
        f"Theme '{piece['theme']}' does not mention Sinai or sapphire pavement"
    )


def test_pieces_json_technique_mentions_automaton():
    """Technique must mention the cellular automaton."""
    piece = get_piece()
    assert piece is not None
    technique = piece["technique"].lower()
    assert "automaton" in technique or "gravner" in technique or "crystal" in technique, (
        f"Technique '{piece['technique']}' does not mention the Gravner-Griffeath automaton"
    )


def test_pieces_json_year_is_integer():
    piece = get_piece()
    assert piece is not None
    assert isinstance(piece["year"], int), f"year must be int, got {type(piece['year'])}"


def test_no_duplicate_piece_ids():
    """Adding this piece must not introduce a duplicate ID."""
    pieces = load_pieces()
    ids = [p["id"] for p in pieces]
    assert len(ids) == len(set(ids)), f"Duplicate IDs found after adding {PIECE_ID}"


# ---------------------------------------------------------------------------
# essay.md content
# ---------------------------------------------------------------------------

def test_essay_at_least_300_words():
    """Essay must be substantial — at least 300 words."""
    text = open(ESSAY_PATH, encoding="utf-8").read()
    word_count = len(text.split())
    assert word_count >= 300, f"Essay has only {word_count} words (need ≥ 300)"


def test_essay_cites_exodus_24_10():
    """Essay must cite Exodus 24:10 (or the Hebrew שמות כד:י)."""
    text = open(ESSAY_PATH, encoding="utf-8").read()
    assert "24:10" in text or "כד:י" in text, (
        "Essay must cite Exodus 24:10 (שמות כד:י)"
    )


def test_essay_mentions_tablets():
    """Essay must discuss the Talmudic tradition about the Tablets."""
    text = open(ESSAY_PATH, encoding="utf-8").read().lower()
    assert "tablet" in text or "luchot" in text or "לוחות" in text, (
        "Essay must mention the Tablets of the Law"
    )


def test_essay_mentions_megillah_or_berachot():
    """Essay must name Megillah 29a or Berachot 55a."""
    text = open(ESSAY_PATH, encoding="utf-8").read()
    assert "Megillah" in text or "Berachot" in text or "מגילה" in text or "ברכות" in text, (
        "Essay must cite Talmudic sources Megillah 29a or Berachot 55a"
    )


def test_essay_mentions_sforno():
    """Essay must reference the Sforno's commentary."""
    text = open(ESSAY_PATH, encoding="utf-8").read()
    assert "Sforno" in text or "sforno" in text.lower(), (
        "Essay must mention the Sforno commentary on Exodus 24:10"
    )


def test_essay_mentions_bereshit_rabbah():
    """Essay must reference Bereshit Rabbah 1:1 (pre-cosmic Torah)."""
    text = open(ESSAY_PATH, encoding="utf-8").read()
    assert "Bereshit Rabbah" in text or "בראשית רבה" in text, (
        "Essay must cite Bereshit Rabbah 1:1 for the pre-cosmic Torah tradition"
    )


# ---------------------------------------------------------------------------
# index.html implementation
# ---------------------------------------------------------------------------

def test_html_uses_request_animation_frame():
    """The animation must use requestAnimationFrame."""
    html = open(HTML_PATH, encoding="utf-8").read()
    assert "requestAnimationFrame" in html, "index.html must use requestAnimationFrame"


def test_html_has_canvas_element():
    html = open(HTML_PATH, encoding="utf-8").read()
    assert "<canvas" in html, "index.html must contain a <canvas> element"


def test_html_has_hex_grid_constants():
    """COLS and ROWS (300) must appear in the simulation code."""
    html = open(HTML_PATH, encoding="utf-8").read()
    assert "300" in html, "index.html must define a 300-wide hex grid"
    assert "COLS" in html or "cols" in html.lower(), "index.html must define COLS"


def test_html_implements_diffusion():
    """The simulation must reference ALPHA (diffusion coefficient)."""
    html = open(HTML_PATH, encoding="utf-8").read()
    assert "ALPHA" in html or "alpha" in html.lower(), (
        "index.html must define a diffusion coefficient ALPHA"
    )


def test_html_implements_freeze_threshold():
    """The simulation must reference THETA (freeze threshold)."""
    html = open(HTML_PATH, encoding="utf-8").read()
    assert "THETA" in html or "theta" in html.lower(), (
        "index.html must define a freeze threshold THETA"
    )


def test_html_embeds_sapphire_palette():
    """The sapphire color palette values must appear in the HTML."""
    html = open(HTML_PATH, encoding="utf-8").read()
    assert "0A2060" in html.upper() or "#0a2060" in html.lower(), (
        "index.html must include the deep sapphire color #0A2060"
    )
    assert "D8EEFF" in html.upper() or "#d8eeff" in html.lower(), (
        "index.html must include the crystal white color #D8EEFF"
    )


def test_html_embeds_essay_text():
    """index.html must embed the essay text inline (no runtime fetch)."""
    essay_text = open(ESSAY_PATH, encoding="utf-8").read()
    html = open(HTML_PATH, encoding="utf-8").read()
    # Sample the first 10 words > 5 chars from the essay
    long_words = [w for w in essay_text.split() if len(w) > 5][:10]
    found = sum(1 for w in long_words if w in html)
    assert found >= 5, (
        f"index.html embeds only {found}/10 sampled essay words — essay must be inline"
    )


def test_html_has_hebrew_quote():
    """index.html must include the Hebrew text of Exodus 24:10."""
    html = open(HTML_PATH, encoding="utf-8").read()
    assert "רַגְלָיו" in html or "ספיר" in html or "סַפִּיר" in html, (
        "index.html must include Hebrew text from Exodus 24:10 (sapphire pavement)"
    )


def test_html_has_rtl_attribute():
    """Hebrew passages must use dir='rtl'."""
    html = open(HTML_PATH, encoding="utf-8").read()
    assert 'dir="rtl"' in html or "dir='rtl'" in html, (
        "index.html must set dir='rtl' for Hebrew passages"
    )


def test_html_has_dark_background():
    """Background color must be the specified near-black."""
    html = open(HTML_PATH, encoding="utf-8").read()
    assert "030508" in html.upper() or "#030508" in html.lower(), (
        "index.html must use background color #030508"
    )


def test_html_steps_per_frame():
    """The simulation should run multiple steps per animation frame."""
    html = open(HTML_PATH, encoding="utf-8").read()
    assert "STEPS_PER_FRAME" in html or "stepsPerFrame" in html or "10" in html, (
        "index.html should define steps per animation frame (target: 10)"
    )


# ---------------------------------------------------------------------------
# Thumbnail SVG
# ---------------------------------------------------------------------------

def test_thumbnail_is_valid_svg():
    """thumbnail.svg must be a valid SVG file."""
    text = open(THUMB_PATH, encoding="utf-8").read()
    assert "<svg" in text and "</svg>" in text, "thumbnail.svg is not valid SVG"


def test_thumbnail_has_gradient():
    """Thumbnail must use SVG linearGradient for the sapphire-to-white arm colors."""
    text = open(THUMB_PATH, encoding="utf-8").read()
    assert "linearGradient" in text, "thumbnail.svg must use SVG linearGradient"


def test_thumbnail_has_dark_background():
    text = open(THUMB_PATH, encoding="utf-8").read()
    assert "030508" in text.upper() or "#030508" in text.lower(), (
        "thumbnail.svg must have the dark background color #030508"
    )


def test_thumbnail_has_six_arms():
    """Thumbnail must depict a 6-pointed snowflake (at least 6 lines/paths for arms)."""
    text = open(THUMB_PATH, encoding="utf-8").read()
    arm_count = text.count("<line") + text.count("<path")
    assert arm_count >= 6, (
        f"thumbnail.svg has only {arm_count} line/path elements — need at least 6 for six arms"
    )


# ---------------------------------------------------------------------------
# README
# ---------------------------------------------------------------------------

def test_readme_mentions_sinai():
    text = open(README_PATH, encoding="utf-8").read().lower()
    assert "sinai" in text or "sapphire" in text, (
        "README.md must mention the Sinai / sapphire pavement theme"
    )


def test_readme_mentions_gravner_griffeath():
    text = open(README_PATH, encoding="utf-8").read().lower()
    assert "gravner" in text or "griffeath" in text or "automaton" in text, (
        "README.md must mention the Gravner-Griffeath automaton technique"
    )


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

def test_piece_path_resolves_to_existing_file():
    """The path registered in pieces.json must resolve to an existing file."""
    piece = get_piece()
    assert piece is not None
    full_path = os.path.join(GALLERY_ROOT, piece["path"])
    assert os.path.isfile(full_path), f"Registered path '{piece['path']}' does not exist on disk"


def test_thumbnail_path_resolves_to_existing_file():
    piece = get_piece()
    assert piece is not None
    full_path = os.path.join(GALLERY_ROOT, piece["thumbnail"])
    assert os.path.isfile(full_path), f"Registered thumbnail '{piece['thumbnail']}' does not exist"


def test_essay_path_resolves_to_existing_file():
    piece = get_piece()
    assert piece is not None
    full_path = os.path.join(GALLERY_ROOT, piece["essay"])
    assert os.path.isfile(full_path), f"Registered essay '{piece['essay']}' does not exist"


def test_piece_not_present_returns_none():
    """Helper: looking up a non-existent ID returns None (no crash)."""
    pieces = load_pieces()
    result = next((p for p in pieces if p["id"] == "99-does-not-exist"), None)
    assert result is None


def test_empty_piece_id_absent_from_pieces_json():
    """No entry should have an empty id."""
    pieces = load_pieces()
    for piece in pieces:
        assert piece.get("id", "").strip() != "", "A piece has an empty 'id' field"
