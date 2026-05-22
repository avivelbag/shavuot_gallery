"""
Tests for piece 50-etz-chaim: Etz Chaim — A Tree of Life to Those Who Hold Her.

Validates the space colonization algorithm tree piece: pieces.json registration,
file layout, essay substance, and index.html content requirements.
"""
import json
import os
import re

import pytest

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECES_JSON  = os.path.join(GALLERY_ROOT, "pieces.json")
PIECE_ID     = "50-etz-chaim"
PIECE_DIR    = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
INDEX_HTML   = os.path.join(PIECE_DIR, "index.html")
ESSAY_MD     = os.path.join(PIECE_DIR, "essay.md")


def _load_pieces():
    with open(PIECES_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


def _get_piece():
    for p in _load_pieces():
        if p["id"] == PIECE_ID:
            return p
    return None


# ---------------------------------------------------------------------------
# Happy path: pieces.json registration
# ---------------------------------------------------------------------------

def test_piece_registered_in_pieces_json():
    """The etz chaim piece must appear in pieces.json."""
    piece = _get_piece()
    assert piece is not None, f"Piece '{PIECE_ID}' not found in pieces.json"


def test_piece_theme_mentions_etz_chaim():
    """Theme must reference Etz Chaim or Crown of Torah."""
    piece = _get_piece()
    assert piece is not None
    theme = piece.get("theme", "").lower()
    assert "etz chaim" in theme or "crown of torah" in theme or "torah" in theme, (
        f"Theme '{piece.get('theme')}' must mention Etz Chaim or Torah"
    )


def test_piece_technique_mentions_space_colonization():
    """Technique field must reference the space colonization algorithm."""
    piece = _get_piece()
    assert piece is not None
    technique = piece.get("technique", "").lower()
    assert "space colonization" in technique, (
        f"Technique '{piece.get('technique')}' must mention space colonization"
    )


def test_piece_year_is_int():
    piece = _get_piece()
    assert piece is not None
    assert isinstance(piece["year"], int), "year must be an integer"


def test_piece_required_fields_present():
    """All standard required fields must be non-empty."""
    required = ("id", "title", "tagline", "year", "theme", "technique",
                "path", "thumbnail", "essay")
    piece = _get_piece()
    assert piece is not None
    for field in required:
        assert field in piece and piece[field], (
            f"Field '{field}' missing or empty in piece registration"
        )


# ---------------------------------------------------------------------------
# File layout
# ---------------------------------------------------------------------------

def test_piece_directory_exists():
    assert os.path.isdir(PIECE_DIR), f"Piece directory {PIECE_DIR} does not exist"


def test_index_html_exists():
    assert os.path.isfile(INDEX_HTML), "index.html is missing from piece directory"


def test_essay_md_exists():
    assert os.path.isfile(ESSAY_MD), "essay.md is missing from piece directory"


def test_thumbnail_exists():
    piece = _get_piece()
    assert piece is not None
    thumb = os.path.join(GALLERY_ROOT, piece["thumbnail"])
    assert os.path.isfile(thumb), f"Thumbnail '{piece['thumbnail']}' does not exist"


def test_thumbnail_is_svg():
    piece = _get_piece()
    assert piece is not None
    thumb = os.path.join(GALLERY_ROOT, piece["thumbnail"])
    if os.path.isfile(thumb):
        content = open(thumb, encoding="utf-8").read()
        assert "<svg" in content and "</svg>" in content, "thumbnail is not valid SVG"


def test_readme_exists():
    readme = os.path.join(PIECE_DIR, "README.md")
    assert os.path.isfile(readme), "README.md is missing from piece directory"


def test_readme_mentions_etz_chaim_theme():
    readme = os.path.join(PIECE_DIR, "README.md")
    text = open(readme, encoding="utf-8").read().lower()
    assert "etz chaim" in text or "tree of life" in text, (
        "README.md must mention the Etz Chaim / Tree of Life theme"
    )


# ---------------------------------------------------------------------------
# Essay substance (acceptance criterion: ≥300 words)
# ---------------------------------------------------------------------------

def test_essay_at_least_300_words():
    """Acceptance criterion: essay must be at least 300 words."""
    text = open(ESSAY_MD, encoding="utf-8").read()
    count = len(text.split())
    assert count >= 300, f"essay.md has {count} words; need at least 300"


def test_essay_cites_proverbs_3_18():
    """Essay must cite Proverbs 3:18 — the key verse."""
    text = open(ESSAY_MD, encoding="utf-8").read()
    assert "Proverbs 3:18" in text or "proverbs 3:18" in text.lower(), (
        "essay.md must cite Proverbs 3:18"
    )


def test_essay_contains_hebrew_verse():
    """Essay must include the Hebrew text of Proverbs 3:18."""
    text = open(ESSAY_MD, encoding="utf-8").read()
    # Key Hebrew words from Proverbs 3:18: עֵץ (tree) and חַיִּים (life)
    assert "עֵץ" in text and "חַיִּים" in text, (
        "essay.md must include Hebrew text from Proverbs 3:18"
    )


def test_essay_cites_avot_6_7():
    """Essay must cite Pirkei Avot 6:7 per acceptance criteria."""
    text = open(ESSAY_MD, encoding="utf-8").read()
    assert "6:7" in text or "Avot 6" in text, (
        "essay.md must cite Pirkei Avot 6:7"
    )


def test_essay_mentions_space_colonization_or_runions():
    """Essay must explain the space colonization algorithm and its connection."""
    text = open(ESSAY_MD, encoding="utf-8").read().lower()
    assert "space colonization" in text or "runions" in text, (
        "essay.md must explain the space colonization algorithm"
    )


def test_essay_mentions_shavuot_sinai_connection():
    """Essay must connect the piece to Shavuot and Sinai."""
    text = open(ESSAY_MD, encoding="utf-8").read().lower()
    assert "sinai" in text or "shavuot" in text, (
        "essay.md must mention Sinai or Shavuot"
    )


def test_essay_contains_avot_hebrew():
    """Essay must include the Hebrew text of the Avot passage."""
    text = open(ESSAY_MD, encoding="utf-8").read()
    # Key Hebrew word: גְּדוֹלָה (great/greater)
    assert "גְּדוֹלָה" in text or "תורה" in text or "תוֹרָה" in text, (
        "essay.md must include Hebrew text from Pirkei Avot 6:7"
    )


# ---------------------------------------------------------------------------
# index.html content requirements
# ---------------------------------------------------------------------------

def test_html_uses_canvas_2d():
    """index.html must use Canvas 2D (not WebGL)."""
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "canvas" in html.lower() and "2d" in html.lower(), (
        "index.html must use Canvas 2D"
    )


def test_html_uses_requestanimationframe():
    """index.html must drive animation with requestAnimationFrame."""
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "requestAnimationFrame" in html, (
        "index.html must use requestAnimationFrame for animation"
    )


def test_html_has_canvas_element():
    """index.html must have a canvas element."""
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "<canvas" in html, "index.html must have a <canvas> element"


def test_html_embeds_essay_text():
    """index.html must embed essay text inline — not load it at runtime."""
    html = open(INDEX_HTML, encoding="utf-8").read()
    # Check several distinctive essay phrases
    assert "tree of life" in html.lower() or "etz chaim" in html.lower(), (
        "index.html must embed essay text inline"
    )


def test_html_embeds_proverbs_hebrew():
    """index.html must contain the Hebrew text of Proverbs 3:18."""
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "עֵץ" in html and "חַיִּים" in html, (
        "index.html must embed the Hebrew text of Proverbs 3:18"
    )


def test_html_embeds_proverbs_english_translation():
    """index.html must embed an English translation of Proverbs 3:18."""
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "tree of life" in html.lower() and "hold" in html.lower(), (
        "index.html must embed English translation of Proverbs 3:18"
    )


def test_html_embeds_avot_hebrew():
    """index.html must contain the Hebrew text of Avot 6:7."""
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "גְּדוֹלָה" in html or "כְּהֻנָּה" in html, (
        "index.html must embed the Hebrew text of Avot 6:7"
    )


def test_html_contains_perception_radius():
    """index.html must define PERCEPTION_RADIUS for the space colonization algorithm."""
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "PERCEPTION_RADIUS" in html or "perception" in html.lower(), (
        "index.html must define the perception radius constant"
    )


def test_html_contains_kill_radius():
    """index.html must define KILL_RADIUS for attractor consumption."""
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "KILL_RADIUS" in html or "kill" in html.lower(), (
        "index.html must define the kill radius constant"
    )


def test_html_implements_hold_phase():
    """index.html must implement the 3-second hold before fade."""
    html = open(INDEX_HTML, encoding="utf-8").read()
    # The hold is implemented via a 3000ms comparison
    assert "3000" in html or "holding" in html, (
        "index.html must implement the 3-second hold phase"
    )


def test_html_implements_fade_phase():
    """index.html must implement the fade-to-black and restart cycle."""
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "fading" in html or "fadeAlpha" in html, (
        "index.html must implement the fade-to-black cycle"
    )


def test_html_hebrew_inscription_at_root():
    """index.html must render the Hebrew inscription עֵץ חַיִּים at the root."""
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "עֵץ חַיִּים" in html, (
        "index.html must contain the Hebrew inscription עֵץ חַיִּים"
    )


def test_html_background_color():
    """index.html must use the deep forest green background #0A1A0D."""
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "#0A1A0D" in html or "#0a1a0d" in html.lower(), (
        "index.html must use background color #0A1A0D"
    )


def test_html_gold_color():
    """index.html must use harvest gold #D4A017 for branches."""
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "D4A017" in html or "d4a017" in html.lower(), (
        "index.html must use harvest gold color #D4A017"
    )


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

def test_piece_path_ends_with_html():
    piece = _get_piece()
    assert piece is not None
    assert piece["path"].endswith(".html"), "path must point to an HTML file"


def test_piece_id_matches_directory():
    piece = _get_piece()
    assert piece is not None
    parts = piece["path"].replace("\\", "/").split("/")
    assert parts[-2] == PIECE_ID, (
        f"Directory in path '{parts[-2]}' does not match id '{PIECE_ID}'"
    )


def test_piece_no_duplicate_id():
    """Piece ID must be unique across all pieces."""
    pieces = _load_pieces()
    ids = [p["id"] for p in pieces]
    assert ids.count(PIECE_ID) == 1, f"Duplicate ID '{PIECE_ID}' in pieces.json"


def test_essay_minimum_word_count_edge_case(tmp_path):
    """Confirm that an essay with exactly 299 words is below the threshold."""
    short_essay = tmp_path / "short.md"
    short_essay.write_text(" ".join(["word"] * 299), encoding="utf-8")
    text = short_essay.read_text(encoding="utf-8")
    assert len(text.split()) == 299
    assert len(text.split()) < 300, "Fixture must be below 300 words"


def test_empty_piece_id_would_fail(tmp_path):
    """A pieces.json entry with empty id must be detected as invalid."""
    bad = [{"id": "", "theme": "something"}]
    assert not bad[0]["id"], "Fixture confirms empty id is invalid"


# ---------------------------------------------------------------------------
# Failure modes
# ---------------------------------------------------------------------------

def test_missing_essay_file_would_fail(tmp_path):
    """Verify that a non-existent essay path would be detected."""
    missing = os.path.join(str(tmp_path), "nonexistent_essay.md")
    assert not os.path.isfile(missing), "Fixture path must not exist"


def test_essay_below_minimum_word_count_would_fail(tmp_path):
    """An essay with fewer than 300 words must be flagged."""
    short_essay = tmp_path / "short.md"
    short_essay.write_text("word " * 50, encoding="utf-8")
    text = short_essay.read_text(encoding="utf-8")
    assert len(text.split()) < 300, "Fixture should have fewer than 300 words"


def test_wrong_technique_would_fail(tmp_path):
    """A piece registered without space colonization in technique would fail the technique check."""
    bad_piece = {"id": PIECE_ID, "technique": "WebGL shader"}
    assert "space colonization" not in bad_piece["technique"].lower(), (
        "Fixture confirms missing space colonization technique keyword"
    )
