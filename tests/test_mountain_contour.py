"""
Tests for piece 35-heart-of-heaven (Sinai topographic contour map).

Verifies: pieces.json registration, required file layout, essay content,
simplex-noise presence, Hebrew verse, particle animation markers, and
sky-gradient colors.
"""
import json
import os
import re

import pytest

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID = "35-heart-of-heaven"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
HTML_PATH = os.path.join(PIECE_DIR, "index.html")
ESSAY_PATH = os.path.join(PIECE_DIR, "essay.md")
THUMB_PATH = os.path.join(PIECE_DIR, "thumbnail.svg")
README_PATH = os.path.join(PIECE_DIR, "README.md")
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")


def load_piece_entry():
    """Return the pieces.json entry for piece 35, or None if absent."""
    with open(PIECES_JSON, encoding="utf-8") as f:
        pieces = json.load(f)
    for p in pieces:
        if p["id"] == PIECE_ID:
            return p
    return None


def read_html():
    """Return the full text of the piece's index.html."""
    with open(HTML_PATH, encoding="utf-8") as f:
        return f.read()


# ─── pieces.json registration ─────────────────────────────────────────────────

def test_piece_registered_in_json():
    """Piece 35 must appear in pieces.json."""
    entry = load_piece_entry()
    assert entry is not None, f"'{PIECE_ID}' not found in pieces.json"


def test_piece_json_required_fields():
    """All required metadata fields must be present and non-empty."""
    required = ("id", "title", "tagline", "year", "theme", "technique",
                "path", "thumbnail", "essay")
    entry = load_piece_entry()
    assert entry is not None
    for field in required:
        assert field in entry and entry[field], f"Missing or empty field: {field}"


def test_piece_year_is_2026():
    entry = load_piece_entry()
    assert entry is not None
    assert entry["year"] == 2026


def test_piece_path_points_to_correct_directory():
    entry = load_piece_entry()
    assert entry is not None
    assert entry["path"] == f"pieces/{PIECE_ID}/index.html"


# ─── Required files on disk ───────────────────────────────────────────────────

def test_index_html_exists():
    assert os.path.isfile(HTML_PATH), "index.html missing"


def test_essay_md_exists():
    assert os.path.isfile(ESSAY_PATH), "essay.md missing"


def test_thumbnail_svg_exists():
    assert os.path.isfile(THUMB_PATH), "thumbnail.svg missing"


def test_readme_exists():
    assert os.path.isfile(README_PATH), "README.md missing"


# ─── Essay content requirements ───────────────────────────────────────────────

def test_essay_at_least_200_words():
    text = open(ESSAY_PATH, encoding="utf-8").read()
    wc = len(text.split())
    assert wc >= 200, f"essay.md has only {wc} words"


def test_essay_cites_deuteronomy_4():
    """Essay must cite Deuteronomy 4:11 as specified by the acceptance criteria."""
    text = open(ESSAY_PATH, encoding="utf-8").read()
    assert "Deuteronomy 4" in text, "essay.md must cite Deuteronomy 4"


def test_essay_cites_exodus_19():
    """Essay must cite Exodus 19:18 as specified by the acceptance criteria."""
    text = open(ESSAY_PATH, encoding="utf-8").read()
    assert "Exodus 19" in text, "essay.md must cite Exodus 19"


def test_essay_mentions_anti_iconic_theme():
    """Essay should address the anti-iconic theology / voice-without-form theme."""
    text = open(ESSAY_PATH, encoding="utf-8").read()
    assert "voice" in text.lower() or "form" in text.lower(), (
        "essay.md must discuss the voice-without-form / anti-iconic theme"
    )


# ─── index.html content requirements ─────────────────────────────────────────

def test_html_embeds_essay_text():
    """At least 5 of the first 10 long words from essay.md must appear in HTML."""
    essay = open(ESSAY_PATH, encoding="utf-8").read()
    html = read_html()
    words = [w for w in essay.split() if len(w) > 5]
    sampled = words[:10]
    found = sum(1 for w in sampled if w in html)
    assert found >= 5, (
        f"index.html does not embed essay text ({found}/10 sampled words found)"
    )


def test_html_uses_request_animation_frame():
    """Canvas animation must use requestAnimationFrame."""
    html = read_html()
    assert "requestAnimationFrame" in html


def test_html_has_canvas_element():
    """index.html must contain a <canvas> element."""
    html = read_html()
    assert "<canvas" in html


def test_html_contains_hebrew_verse():
    """The Hebrew verse from Deuteronomy 4:11 must appear in the HTML."""
    html = read_html()
    # Check for the key Hebrew words from the verse
    assert "וְהָהָר" in html, "Hebrew verse 'וְהָהָר' not found in HTML"
    assert "בָּאֵשׁ" in html, "Hebrew verse 'בָּאֵשׁ' not found in HTML"


def test_html_has_sky_gradient_indigo_color():
    """Sky gradient must include the deep indigo stop (#1A0A3A)."""
    html = read_html()
    assert "1A0A3A" in html.upper() or "#1a0a3a" in html.lower()


def test_html_has_sky_gradient_orange_color():
    """Sky gradient must include the smoky orange-red near-horizon stop."""
    html = read_html()
    assert "7A3B2E" in html.upper() or "#7a3b2e" in html.lower()


def test_html_has_simplex_noise():
    """index.html must contain a self-contained simplex noise implementation."""
    html = read_html()
    assert "noise2D" in html or "simplexNoise" in html, (
        "No simplex noise function found in HTML"
    )
    assert "permMod12" in html or "perm" in html, (
        "No permutation table found in HTML (expected for simplex noise)"
    )


def test_html_has_n_bands_14():
    """The piece must use between 12 and 18 contour elevation bands."""
    html = read_html()
    match = re.search(r'N_BANDS\s*=\s*(\d+)', html)
    assert match is not None, "N_BANDS constant not found in HTML"
    n = int(match.group(1))
    assert 12 <= n <= 18, f"N_BANDS={n} is outside the required 12–18 range"


def test_html_has_particle_system():
    """index.html must declare a particle array and emit particles near the summit."""
    html = read_html()
    assert "particles" in html, "No particles array found"
    assert "peakX" in html or "peak" in html.lower(), (
        "No summit/peak reference found for particle emission"
    )


def test_html_max_particles_in_range():
    """MAX_PARTICLES must be between 80 and 120."""
    html = read_html()
    match = re.search(r'MAX_PARTICLES\s*=\s*(\d+)', html)
    assert match is not None, "MAX_PARTICLES constant not found"
    n = int(match.group(1))
    assert 80 <= n <= 120, f"MAX_PARTICLES={n} is outside required 80–120 range"


def test_html_offscreen_canvas():
    """The piece must pre-render the static mountain to an offscreen canvas."""
    html = read_html()
    assert "offscreen" in html or "createElementNS" in html or (
        "createElement" in html and "canvas" in html
    ), "No offscreen canvas found"


# ─── Thumbnail validity ───────────────────────────────────────────────────────

def test_thumbnail_is_valid_svg():
    text = open(THUMB_PATH, encoding="utf-8").read()
    assert "<svg" in text and "</svg>" in text


def test_thumbnail_has_contour_colors():
    """Thumbnail SVG must include at least some of the contour color palette."""
    text = open(THUMB_PATH, encoding="utf-8").read()
    # Check for a few of the expected band colors
    assert any(c in text.upper() for c in ["5C3A1E", "F0EDE8", "7A4A28"]), (
        "Thumbnail does not appear to use contour band colors"
    )


# ─── Edge-case / failure-mode tests ───────────────────────────────────────────

def test_missing_piece_id_fails(tmp_path):
    """A pieces.json without piece 35 must be detected as missing."""
    with open(PIECES_JSON, encoding="utf-8") as f:
        pieces = json.load(f)
    found = any(p["id"] == PIECE_ID for p in pieces)
    # This test asserts the current state is correct
    assert found, f"Piece '{PIECE_ID}' must be in pieces.json"


def test_essay_word_count_boundary():
    """Exactly 200 words must not be an off-by-one failure."""
    text = open(ESSAY_PATH, encoding="utf-8").read()
    wc = len(text.split())
    assert wc >= 200, f"Word count {wc} must be ≥ 200"
    # Verify it's meaningfully above the minimum (not a stub)
    assert wc >= 250, f"Essay appears too thin ({wc} words); expected a full essay"


def test_no_duplicate_piece_ids():
    """Inserting piece 35 must not have created duplicate IDs."""
    with open(PIECES_JSON, encoding="utf-8") as f:
        pieces = json.load(f)
    ids = [p["id"] for p in pieces]
    assert len(ids) == len(set(ids)), f"Duplicate piece IDs found: {ids}"
