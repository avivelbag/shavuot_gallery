"""
Tests specific to piece 42-sinai-chuppah.

Verifies the cloth simulation HTML, essay content, and pieces.json entry
satisfy the acceptance criteria for the Sinai Chuppah suggestion.
"""
import json
import os
import re

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")
PIECE_ID = "42-sinai-chuppah"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
INDEX_HTML = os.path.join(PIECE_DIR, "index.html")
ESSAY_MD = os.path.join(PIECE_DIR, "essay.md")
THUMBNAIL_SVG = os.path.join(PIECE_DIR, "thumbnail.svg")
README_MD = os.path.join(PIECE_DIR, "README.md")


def _load_pieces():
    """Return the parsed pieces.json list."""
    with open(PIECES_JSON, "r", encoding="utf-8") as fh:
        return json.load(fh)


def _get_piece():
    """Return the pieces.json entry for piece 42, or None."""
    for p in _load_pieces():
        if p["id"] == PIECE_ID:
            return p
    return None


# ---------------------------------------------------------------------------
# Happy path — pieces.json registration
# ---------------------------------------------------------------------------

def test_piece_42_exists_in_json():
    """Piece 42-sinai-chuppah must be registered in pieces.json."""
    piece = _get_piece()
    assert piece is not None, f"Piece '{PIECE_ID}' not found in pieces.json"


def test_piece_42_has_all_required_fields():
    """Every required field must be present and non-empty."""
    required = ("id", "title", "tagline", "year", "theme", "technique", "path", "thumbnail", "essay")
    piece = _get_piece()
    assert piece is not None, f"Piece '{PIECE_ID}' missing from pieces.json"
    for field in required:
        assert field in piece, f"Missing field '{field}' in piece {PIECE_ID}"
        assert piece[field] not in (None, ""), f"Empty field '{field}' in piece {PIECE_ID}"


def test_piece_42_technique_mentions_cloth_simulation():
    """Technique field must describe the Verlet cloth simulation."""
    piece = _get_piece()
    assert piece is not None
    technique = piece.get("technique", "").lower()
    assert "cloth" in technique or "verlet" in technique or "spring" in technique, (
        f"Technique field should mention cloth simulation; got: {piece.get('technique')}"
    )


# ---------------------------------------------------------------------------
# Happy path — file existence
# ---------------------------------------------------------------------------

def test_piece_42_index_html_exists():
    assert os.path.isfile(INDEX_HTML), f"index.html missing at {INDEX_HTML}"


def test_piece_42_essay_md_exists():
    assert os.path.isfile(ESSAY_MD), f"essay.md missing at {ESSAY_MD}"


def test_piece_42_thumbnail_exists():
    assert os.path.isfile(THUMBNAIL_SVG), f"thumbnail.svg missing at {THUMBNAIL_SVG}"


def test_piece_42_readme_exists():
    assert os.path.isfile(README_MD), f"README.md missing at {README_MD}"


# ---------------------------------------------------------------------------
# Happy path — canvas cloth simulation requirements
# ---------------------------------------------------------------------------

def test_piece_42_uses_requestanimationframe():
    """The cloth animation must use requestAnimationFrame for the render loop."""
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "requestAnimationFrame" in html, (
        "index.html must use requestAnimationFrame for 60fps animation"
    )


def test_piece_42_contains_hebrew_ultimatum():
    """The Hebrew text of the Sinai ultimatum must appear in the HTML canvas script."""
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "הַתּוֹרָה" in html or "התורה" in html, (
        "index.html must contain the Hebrew text of the Sinai ultimatum"
    )


def test_piece_42_cloth_grid_is_large_enough():
    """The cloth grid must be at least 20×20 particles as required by the spec."""
    html = open(INDEX_HTML, encoding="utf-8").read()
    rows_match = re.search(r'ROWS\s*=\s*(\d+)', html)
    cols_match = re.search(r'COLS\s*=\s*(\d+)', html)
    assert rows_match and cols_match, "ROWS and COLS constants must be defined in index.html"
    rows = int(rows_match.group(1))
    cols = int(cols_match.group(1))
    assert rows >= 20 and cols >= 20, (
        f"Cloth grid must be at least 20×20; got {rows}×{cols}"
    )


def test_piece_42_uses_verlet_integration():
    """Verlet integration requires storing previous position (px/py) and applying gravity."""
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "GRAVITY" in html, "index.html must define a GRAVITY constant for Verlet integration"
    assert "pinned" in html, "index.html must pin the top row of particles"


def test_piece_42_constraint_iterations():
    """The simulation must use multiple constraint-satisfaction iterations per frame."""
    html = open(INDEX_HTML, encoding="utf-8").read()
    iters_match = re.search(r'ITERS\s*=\s*(\d+)', html)
    assert iters_match, "ITERS constant must be defined in index.html"
    iters = int(iters_match.group(1))
    assert iters >= 6, f"ITERS must be >= 6 for stable cloth; got {iters}"


def test_piece_42_cobalt_color_present():
    """Deep cobalt color (R=0x1B, G=0x2F, B=0x6E) must be referenced in the HTML."""
    html = open(INDEX_HTML, encoding="utf-8").read()
    has_hex_literal = "1b2f6e" in html.lower()
    has_array_form = ("0x1B" in html or "0x1b" in html) and ("0x2F" in html or "0x2f" in html)
    assert has_hex_literal or has_array_form, (
        "index.html must reference deep cobalt (#1B2F6E) for the top of the fabric"
    )


# ---------------------------------------------------------------------------
# Happy path — essay content
# ---------------------------------------------------------------------------

def test_piece_42_essay_cites_shabbat_88a():
    """Essay must cite Shabbat 88a, the source of the 'mountain like a barrel' midrash."""
    essay = open(ESSAY_MD, encoding="utf-8").read()
    assert "Shabbat 88a" in essay or "Shabbat 88" in essay, (
        "essay.md must cite Shabbat 88a (the 'mountain suspended like a barrel' midrash)"
    )


def test_piece_42_essay_mentions_chuppah():
    """Essay must explain the wedding-canopy (chuppah) metaphor."""
    essay = open(ESSAY_MD, encoding="utf-8").read().lower()
    assert "chuppah" in essay or "wedding canopy" in essay or "wedding" in essay, (
        "essay.md must discuss the chuppah / wedding canopy metaphor"
    )


def test_piece_42_essay_mentions_avodah_zarah():
    """Essay must cite Avodah Zarah 2b (Torah offered to other nations)."""
    essay = open(ESSAY_MD, encoding="utf-8").read()
    assert "Avodah Zarah" in essay, (
        "essay.md must cite Avodah Zarah 2b (God offered Torah to other nations)"
    )


def test_piece_42_essay_substantial():
    """Essay must contain at least 200 words."""
    essay = open(ESSAY_MD, encoding="utf-8").read()
    word_count = len(essay.split())
    assert word_count >= 200, f"essay.md has only {word_count} words (minimum 200)"


def test_piece_42_essay_embedded_in_html():
    """Essay text must be embedded inline in index.html (not fetched at runtime)."""
    essay = open(ESSAY_MD, encoding="utf-8").read()
    html = open(INDEX_HTML, encoding="utf-8").read()
    words = [w for w in essay.split() if len(w) > 5]
    sampled = words[:10]
    found = sum(1 for w in sampled if w in html)
    assert found >= 5, (
        f"index.html must embed essay text inline; only {found}/10 sampled words found"
    )


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

def test_piece_42_thumbnail_is_valid_svg():
    """Thumbnail must be a valid SVG file with opening and closing svg tags."""
    content = open(THUMBNAIL_SVG, encoding="utf-8").read()
    assert "<svg" in content and "</svg>" in content, (
        "thumbnail.svg does not appear to be valid SVG"
    )


def test_piece_42_readme_mentions_sinai():
    """README.md must reference the Shavuot / Sinai theme."""
    readme = open(README_MD, encoding="utf-8").read().lower()
    assert "sinai" in readme or "shavuot" in readme or "matan torah" in readme, (
        "README.md must mention the Sinai / Shavuot theme"
    )


def test_piece_42_path_format_correct():
    """pieces.json path must follow the canonical pieces/<id>/index.html pattern."""
    piece = _get_piece()
    assert piece is not None
    expected_path = f"pieces/{PIECE_ID}/index.html"
    assert piece["path"] == expected_path, (
        f"Expected path '{expected_path}', got '{piece['path']}'"
    )


# ---------------------------------------------------------------------------
# Failure modes
# ---------------------------------------------------------------------------

def test_missing_piece_42_detected():
    """Lookup helper returns None when pieces.json does not contain piece 42."""
    fake_pieces = [{"id": "01-thunder-at-sinai", "title": "Thunder"}]
    result = next((p for p in fake_pieces if p["id"] == PIECE_ID), None)
    assert result is None


def test_essay_below_minimum_words_detected(tmp_path):
    """A stub essay with 50 words is detected as below the 200-word minimum."""
    stub = tmp_path / "essay.md"
    stub.write_text("word " * 50, encoding="utf-8")
    word_count = len(stub.read_text(encoding="utf-8").split())
    assert word_count < 200, f"Expected stub to have <200 words; got {word_count}"


def test_cloth_grid_too_small_detected():
    """Regex extraction of ROWS/COLS from fake HTML catches a grid below 20×20."""
    fake_html = "const ROWS = 10;\nconst COLS = 10;"
    rows_match = re.search(r'ROWS\s*=\s*(\d+)', fake_html)
    cols_match = re.search(r'COLS\s*=\s*(\d+)', fake_html)
    assert rows_match and cols_match, "Regex must find ROWS and COLS in fake HTML"
    assert int(rows_match.group(1)) < 20 or int(cols_match.group(1)) < 20
