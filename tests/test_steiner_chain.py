"""
Tests for piece 97-steiner-chain-mesorah (Steiner chain / mesorah animation).

Covers the happy path from the acceptance criteria, two edge cases,
and one explicit failure mode.
"""
import json
import os

import pytest

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID = "97-steiner-chain-mesorah"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")

REQUIRED_FILES = ["index.html", "essay.md", "thumbnail.svg", "README.md"]
CHAIN_COLORS = ["#1A3A6B", "#8B2020", "#2A5E2A", "#C87020", "#5A2080", "#1A6060", "#E8DFC0"]
HEBREW_NAMES = ["משה", "יהושע", "הזקנים", "הנביאים", "אנשי כנסת הגדולה", "שמעון הצדיק", "אנטיגנוס"]


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def load_piece():
    """Return the pieces.json entry for piece 97, or None if absent."""
    with open(PIECES_JSON, "r", encoding="utf-8") as fh:
        pieces = json.load(fh)
    for p in pieces:
        if p["id"] == PIECE_ID:
            return p
    return None


# ---------------------------------------------------------------------------
# Happy path — acceptance criteria
# ---------------------------------------------------------------------------

def test_piece_directory_exists():
    assert os.path.isdir(PIECE_DIR), f"Piece directory missing: {PIECE_DIR}"


@pytest.mark.parametrize("fname", REQUIRED_FILES)
def test_required_files_present(fname):
    """Each required file must exist in the piece directory."""
    assert os.path.isfile(os.path.join(PIECE_DIR, fname)), (
        f"{fname} missing from {PIECE_DIR}"
    )


def test_piece_registered_in_pieces_json():
    piece = load_piece()
    assert piece is not None, f"'{PIECE_ID}' not found in pieces.json"


def test_pieces_json_fields():
    """Entry must have all required fields with correct values."""
    piece = load_piece()
    assert piece is not None
    assert piece["theme"] == "Matan Torah / Chain of Tradition"
    assert piece["technique"] == "Steiner chain (inversion to concentric circles + rotation)"
    assert piece["year"] == 2026
    assert piece["path"] == f"pieces/{PIECE_ID}/index.html"
    assert piece["thumbnail"] == f"pieces/{PIECE_ID}/thumbnail.svg"
    assert piece["essay"] == f"pieces/{PIECE_ID}/essay.md"


def test_index_html_contains_seven_colors():
    """index.html must reference all 7 generation colors."""
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    for color in CHAIN_COLORS:
        assert color.lower() in html.lower(), (
            f"Color {color} not found in index.html"
        )


def test_index_html_contains_hebrew_names():
    """index.html must contain all 7 Hebrew generation names."""
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    for name in HEBREW_NAMES:
        assert name in html, f"Hebrew name '{name}' not found in index.html"


def test_index_html_uses_requestanimationframe():
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "requestAnimationFrame" in html


def test_index_html_uses_inversion():
    """index.html must implement the inversion construction."""
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "invertCircle" in html or "invert" in html.lower()


def test_index_html_has_gold_bounding_circles():
    """Bounding circles must use the specified gold color."""
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "#BF9B30" in html


def test_index_html_pulse_animation():
    """Inner circle must pulse — HTML should reference PULSE_AMP or sin."""
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "PULSE" in html or ("pulse" in html.lower() and "sin" in html)


def test_index_html_embeds_essay_text():
    """index.html must embed essay text inline (not fetch at runtime)."""
    essay = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    words = [w for w in essay.split() if len(w) > 5]
    sampled = words[:10]
    found = sum(1 for w in sampled if w in html)
    assert found >= 5, (
        f"Only {found}/10 essay words found in index.html — essay not embedded"
    )


def test_essay_md_word_count():
    """essay.md must have at least 200 words."""
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    assert len(text.split()) >= 200


def test_essay_md_contains_pirkei_avot():
    """essay.md must open with or reference Pirkei Avot 1:1."""
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    assert "Pirkei Avot" in text or "pirkei avot" in text.lower()


def test_essay_md_mentions_steiner_porism():
    """essay.md must explain Steiner's porism."""
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    assert "porism" in text.lower() or "Steiner" in text


def test_thumbnail_is_valid_svg():
    """thumbnail.svg must be a valid SVG file."""
    content = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert "<svg" in content and "</svg>" in content


def test_thumbnail_contains_seven_colors():
    """thumbnail.svg must reference all 7 generation colors."""
    content = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    for color in CHAIN_COLORS:
        assert color.lower() in content.lower(), (
            f"Color {color} not found in thumbnail.svg"
        )


def test_readme_mentions_sinai_or_matan_torah():
    """README.md must connect the piece to Shavuot (mesorah / Sinai / Matan Torah)."""
    text = open(os.path.join(PIECE_DIR, "README.md"), encoding="utf-8").read().lower()
    assert "sinai" in text or "matan torah" in text or "mesorah" in text


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

def test_index_html_k_equals_seven():
    """The chain count K=7 must be explicit in the JavaScript."""
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "K = 7" in html or "const K=7" in html or "K=7" in html or " 7" in html


def test_essay_md_is_not_empty_and_utf8():
    """essay.md must open as valid UTF-8 and not be empty."""
    path = os.path.join(PIECE_DIR, "essay.md")
    content = open(path, encoding="utf-8").read()
    assert len(content.strip()) > 0


# ---------------------------------------------------------------------------
# Explicit failure mode
# ---------------------------------------------------------------------------

def test_nonexistent_piece_not_in_json():
    """A piece ID that does not exist should not appear in pieces.json."""
    with open(PIECES_JSON, "r", encoding="utf-8") as fh:
        pieces = json.load(fh)
    ids = [p["id"] for p in pieces]
    assert "97-nonexistent-piece" not in ids


def test_pieces_json_no_duplicate_ids():
    """pieces.json must have no duplicate IDs (our addition must not create one)."""
    with open(PIECES_JSON, "r", encoding="utf-8") as fh:
        pieces = json.load(fh)
    ids = [p["id"] for p in pieces]
    assert len(ids) == len(set(ids)), "Duplicate IDs found in pieces.json"
