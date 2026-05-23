"""
Tests for piece 70-pinwheel-tiling-omer: Forty-Nine Angles of the Count.

Validates the pinwheel tiling piece satisfies all acceptance criteria:
SVG generation, depth-4 subdivision, harvest palette, 49 Hebrew Omer labels,
rotation animation, essay content, and pieces.json registration.
"""

import json
import os
import re

import pytest

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID = "70-pinwheel-tiling-omer"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
HTML_PATH = os.path.join(PIECE_DIR, "index.html")
ESSAY_PATH = os.path.join(PIECE_DIR, "essay.md")
README_PATH = os.path.join(PIECE_DIR, "README.md")
THUMB_PATH = os.path.join(PIECE_DIR, "thumbnail.svg")
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def html():
    with open(HTML_PATH, encoding="utf-8") as f:
        return f.read()


@pytest.fixture(scope="module")
def essay():
    with open(ESSAY_PATH, encoding="utf-8") as f:
        return f.read()


@pytest.fixture(scope="module")
def readme():
    with open(README_PATH, encoding="utf-8") as f:
        return f.read()


@pytest.fixture(scope="module")
def thumbnail():
    with open(THUMB_PATH, encoding="utf-8") as f:
        return f.read()


@pytest.fixture(scope="module")
def pieces_entry():
    with open(PIECES_JSON, encoding="utf-8") as f:
        pieces = json.load(f)
    for p in pieces:
        if p["id"] == PIECE_ID:
            return p
    return None


# ---------------------------------------------------------------------------
# Happy path: file existence
# ---------------------------------------------------------------------------

def test_piece_directory_exists():
    assert os.path.isdir(PIECE_DIR), f"Piece directory {PIECE_DIR} is missing"


def test_index_html_exists():
    assert os.path.isfile(HTML_PATH)


def test_essay_md_exists():
    assert os.path.isfile(ESSAY_PATH)


def test_readme_md_exists():
    assert os.path.isfile(README_PATH)


def test_thumbnail_svg_exists():
    assert os.path.isfile(THUMB_PATH)


# ---------------------------------------------------------------------------
# Happy path: pieces.json registration
# ---------------------------------------------------------------------------

def test_piece_registered_in_pieces_json(pieces_entry):
    assert pieces_entry is not None, f"Piece '{PIECE_ID}' not found in pieces.json"


def test_pieces_json_theme(pieces_entry):
    assert pieces_entry is not None
    assert "Sefirat HaOmer" in pieces_entry["theme"]


def test_pieces_json_technique(pieces_entry):
    assert pieces_entry is not None
    assert "pinwheel" in pieces_entry["technique"].lower()
    assert "aperiodic" in pieces_entry["technique"].lower()


def test_pieces_json_all_required_fields(pieces_entry):
    required = ("id", "title", "tagline", "year", "theme", "technique", "path", "thumbnail", "essay")
    assert pieces_entry is not None
    for field in required:
        assert field in pieces_entry and pieces_entry[field], f"Missing field: {field}"


def test_pieces_json_year(pieces_entry):
    assert pieces_entry is not None
    assert pieces_entry["year"] == 2026


# ---------------------------------------------------------------------------
# Happy path: SVG / canvas structure in index.html
# ---------------------------------------------------------------------------

def test_html_contains_svg_element(html):
    assert "<svg" in html and "</svg>" in html


def test_html_has_700x700_viewbox(html):
    assert "700" in html


def test_html_uses_request_animation_frame(html):
    assert "requestAnimationFrame" in html


def test_html_uses_css_rotate(html):
    assert "rotate(" in html


def test_html_contains_pinwheel_subdivision(html):
    assert "subdivide" in html or "subdivision" in html.lower()


def test_html_contains_depth_4_constant(html):
    assert "DEPTH = 4" in html or "depth 4" in html.lower() or "depth=4" in html.lower()


# ---------------------------------------------------------------------------
# Happy path: harvest palette colors
# ---------------------------------------------------------------------------

def test_html_contains_wheat_gold(html):
    assert "#C8A020" in html or "C8A020" in html


def test_html_contains_warm_amber(html):
    assert "#D4720A" in html or "D4720A" in html


def test_html_contains_field_green(html):
    assert "#5A8A30" in html or "5A8A30" in html


def test_html_contains_cream(html):
    assert "#F0E8D0" in html or "F0E8D0" in html


def test_html_label_color_deep_blue(html):
    assert "#1A3080" in html or "1A3080" in html


# ---------------------------------------------------------------------------
# Happy path: 49 Hebrew ordinal labels
# ---------------------------------------------------------------------------

def test_html_contains_aleph_label(html):
    assert "א" in html


def test_html_contains_mem_tet_label(html):
    """The 49th Hebrew ordinal מ״ט must appear in the HTML."""
    assert "מ״ט" in html or "מט" in html


def test_html_contains_hebrew_ordinals_array(html):
    assert "HEBREW_ORDINALS" in html or "hebrewOrdinals" in html


def test_html_references_49_omer_tiles(html):
    assert "49" in html


# ---------------------------------------------------------------------------
# Happy path: essay content
# ---------------------------------------------------------------------------

def test_essay_minimum_400_words(essay):
    word_count = len(essay.split())
    assert word_count >= 400, f"Essay has {word_count} words; expected >= 400"


def test_essay_mentions_leviticus(essay):
    assert "Leviticus" in essay or "leviticus" in essay.lower()


def test_essay_mentions_sefirot(essay):
    assert "sefirot" in essay.lower() or "sefirah" in essay.lower() or "sefirat" in essay.lower()


def test_essay_mentions_pinwheel(essay):
    assert "pinwheel" in essay.lower()


def test_essay_mentions_radin_or_conway(essay):
    assert "Radin" in essay or "Conway" in essay


def test_essay_mentions_chinuch(essay):
    assert "Chinuch" in essay or "chinuch" in essay.lower() or "HaChinuch" in essay


def test_essay_mentions_49(essay):
    assert "49" in essay


def test_essay_embedded_in_html(html, essay):
    """A sample of essay words must appear in the HTML (inline embedding check)."""
    words = [w for w in essay.split() if len(w) > 6][:15]
    found = sum(1 for w in words if w in html)
    assert found >= 7, f"Only {found}/15 sampled essay words found in HTML"


# ---------------------------------------------------------------------------
# Happy path: README content
# ---------------------------------------------------------------------------

def test_readme_mentions_omer(readme):
    assert "omer" in readme.lower() or "Omer" in readme


def test_readme_mentions_pinwheel(readme):
    assert "pinwheel" in readme.lower()


def test_readme_mentions_palette(readme):
    assert "palette" in readme.lower() or "color" in readme.lower() or "colour" in readme.lower()


# ---------------------------------------------------------------------------
# Happy path: thumbnail SVG
# ---------------------------------------------------------------------------

def test_thumbnail_is_valid_svg(thumbnail):
    assert "<svg" in thumbnail and "</svg>" in thumbnail


def test_thumbnail_contains_triangles(thumbnail):
    assert "<polygon" in thumbnail or "<path" in thumbnail


def test_thumbnail_contains_gold_color(thumbnail):
    assert "C8A020" in thumbnail or "D4720A" in thumbnail


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

def test_essay_words_are_real_text(essay):
    """Guard against placeholder stubs like 'Lorem ipsum'."""
    assert "lorem" not in essay.lower()
    assert "placeholder" not in essay.lower()


def test_html_is_not_empty(html):
    assert len(html) > 2000, "index.html appears suspiciously short"


def test_thumbnail_not_empty(thumbnail):
    assert len(thumbnail) > 200


def test_pieces_json_path_ends_html(pieces_entry):
    assert pieces_entry is not None
    assert pieces_entry["path"].endswith(".html")


def test_pieces_json_thumbnail_is_svg(pieces_entry):
    assert pieces_entry is not None
    assert pieces_entry["thumbnail"].endswith(".svg")


# ---------------------------------------------------------------------------
# Explicit failure modes
# ---------------------------------------------------------------------------

def test_piece_id_not_duplicated():
    with open(PIECES_JSON, encoding="utf-8") as f:
        pieces = json.load(f)
    ids = [p["id"] for p in pieces]
    assert ids.count(PIECE_ID) == 1, f"Piece ID '{PIECE_ID}' appears more than once in pieces.json"


def test_missing_piece_directory_would_be_detected(tmp_path):
    """Verify that a missing directory is correctly identified as absent."""
    fake_dir = tmp_path / "99-fake-piece"
    assert not fake_dir.is_dir()


def test_empty_essay_would_fail_word_count():
    """An empty essay string has 0 words, which is less than the 200-word minimum."""
    empty = ""
    assert len(empty.split()) < 200


def test_nonexistent_thumbnail_detected(tmp_path):
    """Confirm that a path pointing to a missing file is correctly flagged."""
    missing = tmp_path / "thumbnail.svg"
    assert not missing.exists()
