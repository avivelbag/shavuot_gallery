"""
Tests for piece 56-613-force-graph: force-directed network of the 613 mitzvot.

Validates:
- pieces.json registration with correct fields
- All required files present on disk
- essay.md content quality (Makkot 23b citation, 248/365 mention)
- index.html embeds essay text and canvas/requestAnimationFrame usage
- thumbnail.svg is valid SVG
- Node count assertions (248 positive + 365 negative = 613) via HTML source scan
"""

import json
import os
import re

import pytest

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")
PIECE_ID = "56-613-force-graph"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)


def load_pieces():
    """Return parsed pieces.json."""
    with open(PIECES_JSON, encoding="utf-8") as f:
        return json.load(f)


def get_piece():
    """Return the pieces.json entry for piece 56, or None."""
    for p in load_pieces():
        if p["id"] == PIECE_ID:
            return p
    return None


# ---------------------------------------------------------------------------
# Happy path: pieces.json registration
# ---------------------------------------------------------------------------

def test_piece_56_in_pieces_json():
    """Piece 56-613-force-graph must appear in pieces.json."""
    assert get_piece() is not None, f"'{PIECE_ID}' not found in pieces.json"


def test_piece_56_required_fields():
    """All required fields must be present and non-empty."""
    p = get_piece()
    assert p is not None
    for field in ("id", "title", "tagline", "year", "theme", "technique", "path", "thumbnail", "essay"):
        assert field in p and p[field], f"Missing or empty field '{field}' in piece 56"


def test_piece_56_theme_is_matan_torah():
    """Theme must reference Matan Torah / Torah and mitzvot."""
    p = get_piece()
    assert p is not None
    assert "Matan Torah" in p["theme"] or "mitzvot" in p["theme"].lower(), (
        f"Expected Matan Torah theme, got: {p['theme']}"
    )


def test_piece_56_technique_is_force_directed():
    """Technique must mention force-directed graph."""
    p = get_piece()
    assert p is not None
    assert "force" in p["technique"].lower(), (
        f"Expected force-directed technique, got: {p['technique']}"
    )


def test_piece_56_year_is_int():
    p = get_piece()
    assert p is not None
    assert isinstance(p["year"], int)


# ---------------------------------------------------------------------------
# File existence
# ---------------------------------------------------------------------------

def test_piece_56_index_html_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "index.html"))


def test_piece_56_essay_md_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "essay.md"))


def test_piece_56_readme_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "README.md"))


def test_piece_56_thumbnail_exists():
    p = get_piece()
    assert p is not None
    full = os.path.join(GALLERY_ROOT, p["thumbnail"])
    assert os.path.isfile(full), f"Thumbnail not found: {p['thumbnail']}"


# ---------------------------------------------------------------------------
# essay.md content
# ---------------------------------------------------------------------------

def _essay_text():
    return open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()


def test_piece_56_essay_min_words():
    """essay.md must contain at least 200 words."""
    text = _essay_text()
    assert len(text.split()) >= 200, f"Essay too short: {len(text.split())} words"


def test_piece_56_essay_cites_makkot_23b():
    """essay.md must cite Makkot 23b (the source of the 613 figure)."""
    text = _essay_text()
    assert "Makkot 23b" in text or "מכות כג" in text, (
        "essay.md must cite Talmud Bavli Makkot 23b"
    )


def test_piece_56_essay_mentions_248_and_365():
    """essay.md must mention both 248 (positive) and 365 (negative) commandments."""
    text = _essay_text()
    assert "248" in text, "essay.md must mention 248 positive commandments"
    assert "365" in text, "essay.md must mention 365 negative commandments"


def test_piece_56_essay_mentions_maimonides():
    """essay.md must discuss Maimonides / Sefer HaMitzvot."""
    text = _essay_text()
    assert "Maimonides" in text or "Mishneh Torah" in text or "Sefer HaMitzvot" in text, (
        "essay.md must discuss Maimonides and his enumeration"
    )


def test_piece_56_essay_contains_hebrew_quote():
    """essay.md must contain the Hebrew passage from Makkot 23b (Rabbi Simlai's teaching)."""
    text = _essay_text()
    # Look for Hebrew characters in the essay
    hebrew_chars = [c for c in text if 'א' <= c <= 'ת']
    assert len(hebrew_chars) >= 20, (
        "essay.md must include the Hebrew text of Rabbi Simlai's teaching"
    )


# ---------------------------------------------------------------------------
# index.html content
# ---------------------------------------------------------------------------

def _html_text():
    return open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()


def test_piece_56_html_uses_canvas():
    """index.html must use an HTML canvas element for the force-directed graph."""
    html = _html_text()
    assert "<canvas" in html, "index.html must contain a <canvas> element"


def test_piece_56_html_uses_requestanimationframe():
    """index.html must use requestAnimationFrame for the simulation loop."""
    html = _html_text()
    assert "requestAnimationFrame" in html, "index.html must use requestAnimationFrame"


def test_piece_56_html_embeds_essay():
    """index.html must embed essay text inline — at least 5 of the first 10 long words."""
    essay_text = _essay_text()
    html = _html_text()
    words = [w for w in essay_text.split() if len(w) > 5]
    sampled = words[:10]
    found = sum(1 for w in sampled if w in html)
    assert found >= 5, (
        f"index.html does not appear to embed essay text (only {found}/10 sampled words found)"
    )


def test_piece_56_html_has_hebrew_legend():
    """index.html must display the Hebrew legend for positive/negative commandments."""
    html = _html_text()
    # Check for the abbreviations used in the legend
    assert "רמ״ח" in html or "רמח" in html or "248" in html, (
        "index.html must show the 248 (רמ״ח) label in the legend"
    )
    assert "שס״ה" in html or "שסה" in html or "365" in html, (
        "index.html must show the 365 (שס״ה) label in the legend"
    )


def test_piece_56_html_has_gold_color():
    """index.html must use the harvest gold color (#D4A820) for positive commandments."""
    html = _html_text()
    assert "#D4A820" in html or "D4A820" in html.upper(), (
        "index.html must use harvest gold (#D4A820) for positive commandments"
    )


def test_piece_56_html_has_violet_color():
    """index.html must use deep violet (#4A1E8A) for negative commandments."""
    html = _html_text()
    assert "#4A1E8A" in html or "4A1E8A" in html.upper(), (
        "index.html must use deep violet (#4A1E8A) for negative commandments"
    )


def test_piece_56_html_has_tooltip():
    """index.html must implement hover tooltip functionality."""
    html = _html_text()
    assert "tooltip" in html.lower() or "mousemove" in html, (
        "index.html must implement mousemove hover/tooltip for nodes"
    )


def test_piece_56_html_has_14_books():
    """index.html JS data must reference 14 books (Maimonides' Mishneh Torah)."""
    html = _html_text()
    # The book data array should appear in the JS
    assert 'BOOKS' in html, "index.html must define a BOOKS array for Maimonidean structure"
    # Check that book 14 appears
    assert '"Shoftim' in html or "Shoftim" in html, (
        "index.html must include Book 14 (Shoftim/Judges) in node data"
    )


def test_piece_56_html_node_counts_sum_to_613():
    """The BOOKS array in index.html must encode exactly 248 positive + 365 negative = 613 nodes."""
    html = _html_text()
    # Extract all book entries like [bookNum, "Name", posCount, negCount]
    pattern = r'\[\s*(\d+)\s*,\s*"[^"]*"\s*,\s*(\d+)\s*,\s*(\d+)\s*\]'
    matches = re.findall(pattern, html)
    assert len(matches) == 14, f"Expected 14 book entries, found {len(matches)}"
    total_pos = sum(int(m[1]) for m in matches)
    total_neg = sum(int(m[2]) for m in matches)
    assert total_pos == 248, f"Expected 248 positive commandments, got {total_pos}"
    assert total_neg == 365, f"Expected 365 negative commandments, got {total_neg}"
    assert total_pos + total_neg == 613, f"Total must be 613, got {total_pos + total_neg}"


def test_piece_56_html_has_stabilization_frames():
    """index.html must run the simulation for a fixed number of frames before stabilizing."""
    html = _html_text()
    assert "STABILIZE_FRAMES" in html or "stabilize" in html.lower() or "120" in html, (
        "index.html must include a stabilization frame count for the simulation"
    )


def test_piece_56_html_has_ambient_drift():
    """index.html must implement ambient drift after stabilization."""
    html = _html_text()
    assert "drift" in html.lower() or "stabilized" in html, (
        "index.html must implement ambient drift after layout stabilizes"
    )


# ---------------------------------------------------------------------------
# thumbnail.svg content
# ---------------------------------------------------------------------------

def _thumb_text():
    p = get_piece()
    assert p is not None
    return open(os.path.join(GALLERY_ROOT, p["thumbnail"]), encoding="utf-8").read()


def test_piece_56_thumbnail_is_valid_svg():
    """thumbnail.svg must be valid SVG."""
    text = _thumb_text()
    assert "<svg" in text and "</svg>" in text, "thumbnail.svg must be valid SVG"


def test_piece_56_thumbnail_has_gold_nodes():
    """thumbnail.svg must contain gold (#D4A820) elements for positive commandments."""
    text = _thumb_text()
    assert "D4A820" in text.upper(), "thumbnail.svg must contain gold color #D4A820"


def test_piece_56_thumbnail_has_violet_nodes():
    """thumbnail.svg must contain violet elements for negative commandments."""
    text = _thumb_text()
    assert "4A1E8A" in text.upper() or "6B30C8" in text.upper(), (
        "thumbnail.svg must contain violet color for negative commandments"
    )


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

def test_piece_56_no_duplicate_ids():
    """pieces.json must not have duplicate IDs (including the new piece)."""
    pieces = load_pieces()
    ids = [p["id"] for p in pieces]
    assert len(ids) == len(set(ids)), f"Duplicate IDs found: {[i for i in ids if ids.count(i) > 1]}"


def test_essay_non_empty_path_in_pieces_json():
    """The essay field in pieces.json must be a non-empty string path."""
    p = get_piece()
    assert p is not None
    essay = p.get("essay", "")
    assert essay and essay.strip(), "essay field in pieces.json must not be empty"
    assert essay.endswith(".md"), "essay field must point to a .md file"


def test_piece_56_html_does_not_fetch_essay_externally():
    """index.html must not dynamically fetch essay.md (it must be embedded)."""
    html = _html_text()
    # If the essay is fetched at runtime, the test_index_html_contains_essay_text would fail,
    # but we also check here that there's no obvious fetch of essay.md
    assert 'fetch("essay.md")' not in html and "fetch('essay.md')" not in html, (
        "index.html must not dynamically fetch essay.md — essay text must be inline"
    )


def test_piece_56_piece_dir_contains_expected_files():
    """The piece directory must contain exactly the expected files."""
    required = {"index.html", "essay.md", "README.md", "thumbnail.svg"}
    present = set(os.listdir(PIECE_DIR))
    for f in required:
        assert f in present, f"Missing required file: {f}"
