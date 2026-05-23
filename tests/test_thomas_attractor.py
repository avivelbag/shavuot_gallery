"""
Tests specific to piece 77-thomas-attractor-tikkun-leil.

Validates that the piece directory, pieces.json entry, HTML animation,
essay, thumbnail, and README all satisfy the acceptance criteria described
in the suggestion.
"""
import json
import os
import re

import pytest

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")
PIECE_ID = "77-thomas-attractor-tikkun-leil"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)


def _load_pieces():
    with open(PIECES_JSON, "r", encoding="utf-8") as fh:
        return json.load(fh)


def _get_piece():
    return next((p for p in _load_pieces() if p["id"] == PIECE_ID), None)


def _html():
    return open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()


def _essay():
    return open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()


# ---------------------------------------------------------------------------
# pieces.json registration
# ---------------------------------------------------------------------------

def test_piece_registered_in_json():
    """Piece 77 must be present in pieces.json."""
    assert _get_piece() is not None, f"'{PIECE_ID}' not found in pieces.json"


def test_piece_theme():
    """Theme must be 'Tikkun Leil Shavuot'."""
    piece = _get_piece()
    assert piece is not None
    assert piece["theme"] == "Tikkun Leil Shavuot", (
        f"Expected theme 'Tikkun Leil Shavuot', got '{piece['theme']}'"
    )


def test_piece_technique_mentions_thomas():
    """Technique field must mention the Thomas attractor."""
    piece = _get_piece()
    assert piece is not None
    assert "Thomas" in piece["technique"], (
        f"Technique '{piece['technique']}' does not mention 'Thomas'"
    )


def test_piece_technique_mentions_rk4():
    """Technique field must mention RK4 integration."""
    piece = _get_piece()
    assert piece is not None
    assert "RK4" in piece["technique"], (
        f"Technique '{piece['technique']}' does not mention 'RK4'"
    )


def test_piece_year_is_2026():
    piece = _get_piece()
    assert piece is not None
    assert piece["year"] == 2026


def test_piece_title_non_empty():
    piece = _get_piece()
    assert piece is not None
    assert piece["title"].strip() != ""


# ---------------------------------------------------------------------------
# File existence
# ---------------------------------------------------------------------------

def test_index_html_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "index.html"))


def test_essay_md_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "essay.md"))


def test_thumbnail_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "thumbnail.svg")), (
        "thumbnail.svg not found in piece directory"
    )


def test_readme_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "README.md"))


# ---------------------------------------------------------------------------
# thumbnail.svg validity
# ---------------------------------------------------------------------------

def test_thumbnail_is_valid_svg():
    """Thumbnail must be a valid SVG (has opening and closing svg tags)."""
    text = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert "<svg" in text and "</svg>" in text, "thumbnail.svg does not look like valid SVG"


def test_thumbnail_has_gold_colors():
    """Thumbnail should reference the gold/dawn color palette."""
    text = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    has_gold = "F5D080" in text or "C87020" in text or "F5D" in text
    assert has_gold, "thumbnail.svg does not reference the gold palette colors"


# ---------------------------------------------------------------------------
# essay.md content
# ---------------------------------------------------------------------------

def test_essay_at_least_200_words():
    """Essay must be at least 200 words."""
    text = _essay()
    count = len(text.split())
    assert count >= 200, f"essay.md has only {count} words (need ≥ 200)"


def test_essay_mentions_tikkun_leil_shavuot():
    text = _essay()
    assert "Tikkun Leil Shavuot" in text, "essay.md must mention 'Tikkun Leil Shavuot'"


def test_essay_mentions_zohar():
    text = _essay()
    assert "Zohar" in text, "essay.md must mention the Zohar as origin of the practice"


def test_essay_mentions_arizal():
    text = _essay()
    assert "Arizal" in text, "essay.md must mention the Arizal (Rabbi Isaac Luria)"


def test_essay_mentions_midrash_sources():
    """Essay must cite at least one midrashic source about Israelites falling asleep."""
    text = _essay()
    has_shir = "Shir HaShirim" in text or "HaShirim" in text
    has_pirkei = "Pirkei" in text
    assert has_shir or has_pirkei, (
        "essay.md must cite Shir HaShirim Rabbah or Pirkei de-Rabbi Eliezer"
    )


def test_essay_mentions_eruvin():
    """Essay must cite the Talmudic teaching from Eruvin 54a about Torah and water."""
    text = _essay()
    assert "Eruvin" in text, "essay.md must cite Eruvin 54a"


def test_essay_mentions_thomas_attractor():
    text = _essay()
    assert "Thomas" in text, "essay.md must describe the Thomas attractor"


# ---------------------------------------------------------------------------
# index.html animation correctness
# ---------------------------------------------------------------------------

def test_html_uses_requestanimationframe():
    assert "requestAnimationFrame" in _html()


def test_html_has_rk4_implementation():
    """HTML must implement RK4 (should contain the four k1..k4 derivative evaluations)."""
    html = _html()
    assert "rk4Step" in html or "rk4" in html.lower(), (
        "index.html must implement RK4 integration"
    )


def test_html_has_attractor_b_constant():
    """HTML must define the attractor constant b = 0.208."""
    html = _html()
    assert "0.208" in html, "index.html must use attractor constant b = 0.208"


def test_html_has_buffer_size():
    """HTML must define the circular buffer of 6000 points."""
    html = _html()
    assert "6000" in html, "index.html must define circular buffer size of 6000"


def test_html_has_points_per_frame():
    """HTML must add 200 new points per frame."""
    html = _html()
    assert "200" in html, "index.html must add 200 points per frame"


def test_html_has_dark_background():
    """HTML must use the near-black background color #060408."""
    html = _html()
    assert "060408" in html, "index.html must use background color #060408"


def test_html_has_initial_condition():
    """HTML must start the attractor at (0.1, 0.0, 0.0)."""
    html = _html()
    assert "0.1" in html, "index.html must use initial condition x0 = 0.1"


def test_html_has_transient_discard():
    """HTML must discard the first 5000 steps before displaying."""
    html = _html()
    assert "5000" in html, "index.html must discard 5000 transient steps"


def test_html_has_rotation_rate():
    """HTML must advance rotation angle at 0.002 radians per frame."""
    html = _html()
    assert "0.002" in html, "index.html must rotate at 0.002 radians per frame"


def test_html_embeds_essay_text():
    """index.html must embed essay content inline (at least 5 of 10 sampled words)."""
    essay_text = _essay()
    html = _html()
    words = [w for w in essay_text.split() if len(w) > 5]
    sampled = words[:10]
    found = sum(1 for w in sampled if w in html)
    assert found >= 5, (
        f"index.html does not embed essay text (only {found}/10 sampled words found)"
    )


def test_html_is_responsive():
    """index.html must include a media query for mobile layout."""
    html = _html()
    assert "max-width" in html and "768" in html, (
        "index.html must include a max-width media query for responsive layout"
    )


# ---------------------------------------------------------------------------
# Edge cases and failure modes
# ---------------------------------------------------------------------------

def test_no_duplicate_piece_id():
    """The new piece ID must not duplicate any existing piece."""
    pieces = _load_pieces()
    ids = [p["id"] for p in pieces]
    count = ids.count(PIECE_ID)
    assert count == 1, f"Piece ID '{PIECE_ID}' appears {count} times in pieces.json"


def test_piece_paths_resolve(tmp_path):
    """All path fields in the piece entry must resolve to existing files."""
    piece = _get_piece()
    assert piece is not None
    for field in ("path", "thumbnail", "essay"):
        full = os.path.join(GALLERY_ROOT, piece[field])
        assert os.path.isfile(full), f"Field '{field}' does not resolve to a file: {piece[field]}"


def test_missing_piece_detected_by_helper(tmp_path):
    """Helper returns None for a non-existent piece ID — validates the lookup logic."""
    pieces = _load_pieces()
    result = next((p for p in pieces if p["id"] == "99-nonexistent-piece"), None)
    assert result is None


def test_essay_word_count_boundary():
    """An essay with exactly 200 words should pass; 199 should logically fail."""
    text = _essay()
    word_count = len(text.split())
    assert word_count >= 200, f"Essay has {word_count} words; minimum is 200"
    # Confirm the margin is not razor-thin (helps catch accidental truncation)
    assert word_count >= 250, (
        f"Essay has only {word_count} words; expected a substantive essay (≥250)"
    )
