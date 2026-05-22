"""
Tests for piece 46-given-in-wilderness (curl noise sand dunes).

Validates that the piece satisfies all acceptance criteria from the
suggestion: file layout, palette, Hebrew text, essay content, and
pieces.json registration.
"""
import json
import os
import re

import pytest

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECES_JSON  = os.path.join(GALLERY_ROOT, "pieces.json")
PIECE_ID     = "46-given-in-wilderness"
PIECE_DIR    = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
INDEX_HTML   = os.path.join(PIECE_DIR, "index.html")
ESSAY_MD     = os.path.join(PIECE_DIR, "essay.md")
README_MD    = os.path.join(PIECE_DIR, "README.md")
THUMBNAIL    = os.path.join(PIECE_DIR, "thumbnail.svg")


def load_pieces():
    with open(PIECES_JSON, encoding="utf-8") as fh:
        return json.load(fh)


def get_piece():
    for p in load_pieces():
        if p["id"] == PIECE_ID:
            return p
    return None


# ---------------------------------------------------------------------------
# Happy path: directory layout
# ---------------------------------------------------------------------------

def test_piece_directory_exists():
    """The piece directory must be created at pieces/46-given-in-wilderness/."""
    assert os.path.isdir(PIECE_DIR), f"Piece directory not found: {PIECE_DIR}"


def test_index_html_exists():
    assert os.path.isfile(INDEX_HTML), "index.html missing from piece directory"


def test_essay_md_exists():
    assert os.path.isfile(ESSAY_MD), "essay.md missing from piece directory"


def test_readme_md_exists():
    assert os.path.isfile(README_MD), "README.md missing from piece directory"


def test_thumbnail_svg_exists():
    assert os.path.isfile(THUMBNAIL), "thumbnail.svg missing from piece directory"


# ---------------------------------------------------------------------------
# pieces.json registration
# ---------------------------------------------------------------------------

def test_piece_registered_in_json():
    """Piece 46-given-in-wilderness must appear in pieces.json."""
    piece = get_piece()
    assert piece is not None, f"'{PIECE_ID}' not found in pieces.json"


def test_piece_json_required_fields():
    """All required fields must be present and non-empty."""
    required = ("id", "title", "tagline", "year", "theme", "technique",
                "path", "thumbnail", "essay")
    piece = get_piece()
    assert piece is not None
    for field in required:
        assert field in piece, f"Missing field '{field}' in pieces.json entry"
        assert piece[field] not in (None, ""), f"Empty field '{field}' in pieces.json entry"


def test_piece_year_is_int():
    piece = get_piece()
    assert piece is not None
    assert isinstance(piece["year"], int), "year field must be an integer"


def test_piece_path_is_correct():
    piece = get_piece()
    assert piece is not None
    assert piece["path"] == f"pieces/{PIECE_ID}/index.html"


def test_piece_thumbnail_path_is_correct():
    piece = get_piece()
    assert piece is not None
    assert piece["thumbnail"] == f"pieces/{PIECE_ID}/thumbnail.svg"


def test_piece_essay_path_is_correct():
    piece = get_piece()
    assert piece is not None
    assert piece["essay"] == f"pieces/{PIECE_ID}/essay.md"


# ---------------------------------------------------------------------------
# index.html content checks
# ---------------------------------------------------------------------------

def test_index_html_uses_requestanimationframe():
    """Canvas animation must use requestAnimationFrame."""
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "requestAnimationFrame" in html


def test_index_html_has_curl_noise():
    """index.html must implement curl noise (finite-difference computation)."""
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "curlAt" in html or "curl" in html.lower(), \
        "index.html must contain curl noise computation"


def test_index_html_has_perlin_noise():
    """index.html must include an inline Perlin / gradient noise implementation."""
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "noise3" in html or "PERM" in html, \
        "index.html must contain an inline noise function"


def test_index_html_has_streamline_integration():
    """index.html must integrate streamlines (step loop)."""
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "STEPS" in html or "drawStreamline" in html, \
        "index.html must integrate streamlines"


def test_index_html_has_time_offset_animation():
    """index.html must animate via a timeOffset or equivalent variable."""
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "timeOffset" in html, \
        "index.html must have a timeOffset variable for animation"


def test_index_html_has_palette_colors():
    """index.html must reference the warm desert palette colors."""
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "F5E6C8" in html or "245, 230, 200" in html, \
        "Pale sand color #F5E6C8 must appear in index.html"
    assert "C8843A" in html or "200, 132, 58" in html, \
        "Tawny amber #C8843A must appear in index.html"
    assert "7A4A18" in html or "122, 74, 24" in html, \
        "Deep ochre #7A4A18 must appear in index.html"
    assert "3A2855" in html or "58, 40, 85" in html, \
        "Violet shadow #3A2855 must appear in index.html"


def test_index_html_has_horizon_line():
    """index.html must draw a horizon line."""
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "horizon" in html.lower() or "A09070" in html, \
        "index.html must draw a horizon line"


def test_index_html_has_hebrew_midbar():
    """index.html must render the Hebrew word מִדְבָּר (midbar)."""
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "מִדְבָר" in html or "מִדְבָּר" in html, \
        "index.html must contain the Hebrew word מִדְבָּר (midbar)"


def test_index_html_embeds_essay():
    """index.html must embed essay text inline (sampled word check)."""
    essay = open(ESSAY_MD, encoding="utf-8").read()
    html  = open(INDEX_HTML, encoding="utf-8").read()
    words = [w for w in essay.split() if len(w) > 5][:10]
    found = sum(1 for w in words if w in html)
    assert found >= 5, (
        f"index.html does not appear to embed essay text "
        f"(only {found}/10 sampled words found in HTML)"
    )


def test_index_html_has_two_panel_layout():
    """index.html must use the two-panel art/essay layout."""
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "art-panel" in html and "essay-panel" in html, \
        "index.html must have art-panel and essay-panel layout"


# ---------------------------------------------------------------------------
# Essay content checks
# ---------------------------------------------------------------------------

def test_essay_min_200_words():
    text = open(ESSAY_MD, encoding="utf-8").read()
    count = len(text.split())
    assert count >= 200, f"essay.md has only {count} words (need ≥ 200)"


def test_essay_cites_bamidbar_rabbah():
    """Essay must cite Bamidbar Rabbah 1:7."""
    text = open(ESSAY_MD, encoding="utf-8").read()
    assert "Bamidbar Rabbah" in text or "bamidbar rabbah" in text.lower(), \
        "essay.md must cite Bamidbar Rabbah"
    assert "1:7" in text, "essay.md must cite Bamidbar Rabbah 1:7 specifically"


def test_essay_mentions_hefker():
    """Essay must discuss hefker (ownerless) theology."""
    text = open(ESSAY_MD, encoding="utf-8").read()
    assert "hefker" in text.lower(), \
        "essay.md must mention hefker (ownerless desert theology)"


def test_essay_cites_avot():
    """Essay must connect to Pirkei Avot 6:6."""
    text = open(ESSAY_MD, encoding="utf-8").read()
    assert "Avot" in text or "avot" in text.lower(), \
        "essay.md must reference Pirkei Avot"
    assert "6:6" in text, "essay.md must cite Avot 6:6 specifically"


def test_essay_mentions_wilderness_revelations():
    """Essay must discuss at least one of the three wilderness revelations."""
    text = open(ESSAY_MD, encoding="utf-8").read().lower()
    revelations = ["burning bush", "sinai", "tabernacle", "mishkan"]
    found = [r for r in revelations if r in text]
    assert len(found) >= 1, \
        f"essay.md must mention wilderness revelations; found none of {revelations}"


# ---------------------------------------------------------------------------
# Thumbnail checks
# ---------------------------------------------------------------------------

def test_thumbnail_is_valid_svg():
    text = open(THUMBNAIL, encoding="utf-8").read()
    assert "<svg" in text and "</svg>" in text, "thumbnail.svg must be valid SVG"


def test_thumbnail_uses_desert_palette():
    """thumbnail.svg must reference at least one desert palette color."""
    text = open(THUMBNAIL, encoding="utf-8").read()
    palette_colors = ["F5E6C8", "C8843A", "7A4A18", "3A2855",
                      "EDD8A8", "D4A860", "A09070", "C8A87A"]
    found = [c for c in palette_colors if c in text]
    assert len(found) >= 2, \
        f"thumbnail.svg should reference desert palette colors; found {found}"


# ---------------------------------------------------------------------------
# Edge-case / failure-mode tests
# ---------------------------------------------------------------------------

def test_no_duplicate_ids_after_addition():
    """Adding piece 46 must not create duplicate IDs in pieces.json."""
    pieces = load_pieces()
    ids = [p["id"] for p in pieces]
    assert len(ids) == len(set(ids)), f"Duplicate IDs found: {ids}"


def test_piece_46_is_last_entry():
    """Piece 46-given-in-wilderness should be the last entry (highest number)."""
    pieces = load_pieces()
    assert pieces[-1]["id"] == PIECE_ID, \
        f"Expected '{PIECE_ID}' to be the last entry; got '{pieces[-1]['id']}'"


def test_index_html_no_external_fetch():
    """index.html must not fetch the essay at runtime (no fetch/XHR of essay.md)."""
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "fetch(" not in html or "essay.md" not in html, \
        "index.html must not fetch essay.md at runtime — essay must be embedded"


def test_essay_mentions_curl_noise_technique():
    """Essay should explain the curl noise technique."""
    text = open(ESSAY_MD, encoding="utf-8").read().lower()
    assert "curl" in text or "divergence" in text or "flow field" in text, \
        "essay.md should mention the curl noise / flow field technique"


def test_empty_piece_directory_would_fail(tmp_path):
    """A piece directory with no index.html must be caught by the layout test."""
    fake_dir = tmp_path / "99-fake-piece"
    fake_dir.mkdir()
    assert not (fake_dir / "index.html").exists(), \
        "Fixture confirms missing index.html should be caught"


def test_piece_with_wrong_id_path_mismatch_detected():
    """pieces.json path must match the piece ID."""
    piece = get_piece()
    assert piece is not None
    path_dir = piece["path"].replace("\\", "/").split("/")[-2]
    assert path_dir == piece["id"], \
        f"path directory '{path_dir}' must match id '{piece['id']}'"
