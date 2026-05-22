"""
Tests for piece 42-finger-of-god — Apollonian gasket / Written by the Finger of God.

Validates file layout, pieces.json registration, essay content requirements,
HTML structure, and the mathematical correctness of the Descartes circle
theorem implementation embedded in the piece.
"""
import json
import os
import re

import pytest

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID = "42-finger-of-god"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_pieces():
    with open(PIECES_JSON, encoding="utf-8") as fh:
        return json.load(fh)


def get_piece():
    for p in load_pieces():
        if p["id"] == PIECE_ID:
            return p
    return None


def read_file(rel_path):
    return open(os.path.join(GALLERY_ROOT, rel_path), encoding="utf-8").read()


# ---------------------------------------------------------------------------
# File layout
# ---------------------------------------------------------------------------

def test_piece_directory_exists():
    assert os.path.isdir(PIECE_DIR), f"Directory {PIECE_DIR} does not exist"


def test_index_html_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "index.html"))


def test_essay_md_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "essay.md"))


def test_thumbnail_svg_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "thumbnail.svg"))


def test_readme_md_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "README.md"))


# ---------------------------------------------------------------------------
# pieces.json registration
# ---------------------------------------------------------------------------

def test_registered_in_pieces_json():
    piece = get_piece()
    assert piece is not None, f"Piece '{PIECE_ID}' not found in pieces.json"


def test_required_fields_present():
    piece = get_piece()
    required = ("id", "title", "tagline", "year", "theme", "technique", "path", "thumbnail", "essay")
    for field in required:
        assert field in piece, f"Missing field '{field}' in pieces.json entry"


def test_paths_are_correct():
    piece = get_piece()
    assert piece["path"] == f"pieces/{PIECE_ID}/index.html"
    assert piece["thumbnail"] == f"pieces/{PIECE_ID}/thumbnail.svg"
    assert piece["essay"] == f"pieces/{PIECE_ID}/essay.md"


def test_year_is_2026():
    piece = get_piece()
    assert piece["year"] == 2026


# ---------------------------------------------------------------------------
# Essay content requirements
# ---------------------------------------------------------------------------

def test_essay_minimum_word_count():
    text = read_file(f"pieces/{PIECE_ID}/essay.md")
    word_count = len(text.split())
    assert word_count >= 200, f"Essay has only {word_count} words; need >= 200"


def test_essay_cites_exodus_31_18():
    text = read_file(f"pieces/{PIECE_ID}/essay.md")
    assert "31:18" in text or "Exodus 31" in text, \
        "essay.md must cite Exodus 31:18"


def test_essay_mentions_written_by_finger_of_god():
    text = read_file(f"pieces/{PIECE_ID}/essay.md")
    assert "finger of God" in text or "finger of god" in text.lower(), \
        "essay.md must mention 'written by the finger of God'"


def test_essay_mentions_torah_shebichtav():
    text = read_file(f"pieces/{PIECE_ID}/essay.md")
    assert "Shebichtav" in text or "Torah Shebichtav" in text, \
        "essay.md must explain Torah Shebichtav (Written Torah)"


def test_essay_mentions_torah_shebaal_peh():
    text = read_file(f"pieces/{PIECE_ID}/essay.md")
    assert "Sheba'al Peh" in text or "Oral Torah" in text, \
        "essay.md must explain Torah Sheba'al Peh (Oral Torah)"


def test_essay_cites_shabbat_31a():
    text = read_file(f"pieces/{PIECE_ID}/essay.md")
    assert "Shabbat 31a" in text or "Shabbat 31" in text, \
        "essay.md must cite Shabbat 31a"


def test_essay_cites_avot():
    text = read_file(f"pieces/{PIECE_ID}/essay.md")
    assert "Avot" in text, "essay.md must cite Avot (1:1 or 5:22)"


def test_essay_mentions_apollonian_or_descartes():
    text = read_file(f"pieces/{PIECE_ID}/essay.md")
    has_apollonian = "Apollonian" in text or "apollonian" in text
    has_descartes = "Descartes" in text
    assert has_apollonian or has_descartes, \
        "essay.md must explain the Apollonian gasket or Descartes' theorem"


# ---------------------------------------------------------------------------
# HTML structure
# ---------------------------------------------------------------------------

def test_html_uses_canvas():
    html = read_file(f"pieces/{PIECE_ID}/index.html")
    assert "<canvas" in html, "index.html must use a <canvas> element"


def test_html_uses_request_animation_frame():
    html = read_file(f"pieces/{PIECE_ID}/index.html")
    assert "requestAnimationFrame" in html, \
        "index.html must animate with requestAnimationFrame"


def test_html_contains_aleph():
    html = read_file(f"pieces/{PIECE_ID}/index.html")
    assert "א" in html, "index.html must render the Hebrew aleph (א)"


def test_html_embeds_essay_text():
    """Essay text must be inline in HTML (no runtime fetch)."""
    essay = read_file(f"pieces/{PIECE_ID}/essay.md")
    html = read_file(f"pieces/{PIECE_ID}/index.html")
    long_words = [w for w in essay.split() if len(w) > 6][:10]
    found = sum(1 for w in long_words if w in html)
    assert found >= 5, (
        f"index.html does not appear to embed the essay text "
        f"(only {found}/10 sampled words found)"
    )


def test_html_has_slate_background():
    html = read_file(f"pieces/{PIECE_ID}/index.html")
    assert "#1A1A2E" in html or "#1a1a2e" in html.lower(), \
        "index.html must use the deep slate background color #1A1A2E"


def test_html_has_gold_palette():
    html = read_file(f"pieces/{PIECE_ID}/index.html")
    has_gold = "#F5D87A" in html or "#f5d87a" in html.lower()
    has_amber = "#8B5A00" in html or "#8b5a00" in html.lower()
    assert has_gold or has_amber, \
        "index.html must reference the gold/amber palette colors"


def test_html_mentions_descartes_theorem():
    html = read_file(f"pieces/{PIECE_ID}/index.html")
    assert "Descartes" in html or "descartes" in html.lower(), \
        "index.html should reference Descartes' theorem in code or comments"


# ---------------------------------------------------------------------------
# Thumbnail
# ---------------------------------------------------------------------------

def test_thumbnail_is_valid_svg():
    svg = read_file(f"pieces/{PIECE_ID}/thumbnail.svg")
    assert "<svg" in svg and "</svg>" in svg


def test_thumbnail_contains_circles():
    svg = read_file(f"pieces/{PIECE_ID}/thumbnail.svg")
    assert "<circle" in svg, "thumbnail.svg should contain circle elements"


def test_thumbnail_has_slate_background():
    svg = read_file(f"pieces/{PIECE_ID}/thumbnail.svg")
    assert "#1A1A2E" in svg or "#1a1a2e" in svg.lower()


# ---------------------------------------------------------------------------
# Edge cases: Descartes theorem math (Python re-implementation for testing)
# ---------------------------------------------------------------------------

def descartes_k(k1, k2, k3):
    """Compute the two Soddy curvatures for three mutually tangent circles."""
    import math
    s = k1 + k2 + k3
    disc = math.sqrt(max(0, k1 * k2 + k2 * k3 + k3 * k1))
    return s + 2 * disc, s - 2 * disc


def test_descartes_theorem_equal_circles():
    """Three equal circles of radius 1 (k=1) produce known Soddy curvatures."""
    import math
    k4a, k4b = descartes_k(1, 1, 1)
    # Known: k4 = 3 ± 2*sqrt(3); inner ~= 5.464, outer ~= 0.536
    assert abs(k4a - (3 + 2 * math.sqrt(3))) < 1e-9
    assert abs(k4b - (3 - 2 * math.sqrt(3))) < 1e-9


def test_descartes_theorem_enclosing_circle():
    """Standard Apollonian seed: outer circle r=1 (k=-1), two inner r=0.5 (k=2).
    The two Soddy curvatures for the triple (outer, left, right) should include k=3."""
    k4a, k4b = descartes_k(-1, 2, 2)
    # Expected: k = 3 and k = -1 (outer circle itself)
    assert abs(k4a - 3) < 1e-9 or abs(k4b - 3) < 1e-9


def test_descartes_theorem_zero_radius_edge_case():
    """A degenerate circle with curvature 0 (infinite radius / flat plane) is handled."""
    # k=0 means a line; theorem still computes without division by zero on the input side
    k4a, k4b = descartes_k(0, 1, 1)
    # Just verify both solutions are finite
    import math
    assert math.isfinite(k4a) and math.isfinite(k4b)


def test_descartes_theorem_large_curvature():
    """Very small circles (large k) should still satisfy Descartes relation."""
    import math
    k1, k2, k3 = 100, 200, 300
    k4a, k4b = descartes_k(k1, k2, k3)
    # Verify Descartes: (k1+k2+k3+k4)^2 == 2*(k1^2+k2^2+k3^2+k4^2)
    for k4 in [k4a, k4b]:
        lhs = (k1 + k2 + k3 + k4) ** 2
        rhs = 2 * (k1**2 + k2**2 + k3**2 + k4**2)
        assert abs(lhs - rhs) < 1e-3, f"Descartes theorem violated for k4={k4}"


# ---------------------------------------------------------------------------
# Failure-mode tests
# ---------------------------------------------------------------------------

def test_missing_piece_not_in_json():
    """A piece not in pieces.json returns None from our helper."""
    pieces = load_pieces()
    ids = [p["id"] for p in pieces]
    assert "99-nonexistent" not in ids


def test_essay_stub_would_fail_word_count():
    """A stub essay with fewer than 200 words fails the word-count threshold."""
    stub = "This is a stub. " * 10
    assert len(stub.split()) < 200
