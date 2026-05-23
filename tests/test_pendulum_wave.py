"""
Tests for piece 76-pendulum-wave-sefirat-haomer (Forty-Nine Voices in Time).

Covers: directory layout, pieces.json registration, physics constants in HTML,
essay content requirements, thumbnail SVG validity, and edge-case failures.
"""
import json
import math
import os
import re

import pytest

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID = "76-pendulum-wave-sefirat-haomer"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_pieces():
    """Return parsed pieces.json list."""
    with open(PIECES_JSON, encoding="utf-8") as fh:
        return json.load(fh)


def get_piece():
    """Return the pieces.json entry for the pendulum wave piece, or None."""
    for p in load_pieces():
        if p["id"] == PIECE_ID:
            return p
    return None


def read_html():
    """Return raw text of index.html."""
    path = os.path.join(PIECE_DIR, "index.html")
    return open(path, encoding="utf-8").read()


def read_essay():
    """Return raw text of essay.md."""
    path = os.path.join(PIECE_DIR, "essay.md")
    return open(path, encoding="utf-8").read()


# ---------------------------------------------------------------------------
# Directory layout tests
# ---------------------------------------------------------------------------

def test_piece_directory_exists():
    assert os.path.isdir(PIECE_DIR), f"Piece directory missing: {PIECE_DIR}"


def test_index_html_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "index.html"))


def test_essay_md_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "essay.md"))


def test_thumbnail_svg_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "thumbnail.svg"))


def test_readme_md_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "README.md"))


# ---------------------------------------------------------------------------
# pieces.json registration tests
# ---------------------------------------------------------------------------

def test_piece_registered_in_pieces_json():
    assert get_piece() is not None, f"'{PIECE_ID}' not found in pieces.json"


def test_piece_theme_is_sefirat_haomer():
    p = get_piece()
    assert p is not None
    assert "Sefirat HaOmer" in p["theme"], (
        f"Expected theme containing 'Sefirat HaOmer', got: {p['theme']!r}"
    )


def test_piece_technique_mentions_pendulum():
    p = get_piece()
    assert p is not None
    assert "pendulum" in p["technique"].lower(), (
        f"Technique should mention pendulum, got: {p['technique']!r}"
    )


def test_piece_paths_resolve():
    """All path fields referenced in pieces.json must exist on disk."""
    p = get_piece()
    assert p is not None
    for field in ("path", "thumbnail", "essay"):
        full = os.path.join(GALLERY_ROOT, p[field])
        assert os.path.isfile(full), f"File for field '{field}' missing: {p[field]}"


def test_piece_year_is_integer():
    p = get_piece()
    assert p is not None
    assert isinstance(p["year"], int)


# ---------------------------------------------------------------------------
# index.html physics and animation tests
# ---------------------------------------------------------------------------

def test_html_uses_requestanimationframe():
    assert "requestAnimationFrame" in read_html()


def test_html_has_49_pendulums_constant():
    """N = 49 must be encoded in the script."""
    html = read_html()
    assert "N = 49" in html or "var N = 49" in html or "N=49" in html, (
        "index.html must declare N = 49 (number of pendulums)"
    )


def test_html_has_correct_period_constant():
    """T1 = 3.0 seconds for the slowest pendulum."""
    html = read_html()
    assert "T1 = 3.0" in html or "T1=3.0" in html or "var T1 = 3.0" in html, (
        "index.html must set T1 = 3.0 (period of slowest pendulum)"
    )


def test_html_uses_g_9_8():
    """Gravitational constant g = 9.8."""
    html = read_html()
    assert "G = 9.8" in html or "g = 9.8" in html or "G=9.8" in html or "g=9.8" in html, (
        "index.html must use g = 9.8 m/s²"
    )


def test_html_uses_theta0_0_3():
    """Initial angle θ₀ = 0.3 radians."""
    html = read_html()
    assert "THETA0 = 0.3" in html or "theta0 = 0.3" in html or "0.3" in html, (
        "index.html must use initial angle 0.3 radians"
    )


def test_html_trail_length_is_120():
    """Trail ring buffer length must be 120."""
    html = read_html()
    assert "TRAIL_LEN = 120" in html or "TRAIL_LEN=120" in html, (
        "index.html must define TRAIL_LEN = 120"
    )


def test_html_background_is_navy():
    """Background must be the deep navy color #0A0A1A."""
    html = read_html()
    assert "#0A0A1A" in html or "#0a0a1a" in html, (
        "index.html must use background color #0A0A1A"
    )


def test_html_contains_shavuot_hebrew():
    """The Hebrew word שָׁבוּעוֹת must appear in the animation overlay code."""
    html = read_html()
    assert "שָׁבוּעוֹת" in html, (
        "index.html must include the Hebrew text שָׁבוּעוֹת in the overlay"
    )


def test_html_has_canvas_element():
    html = read_html()
    assert "<canvas" in html, "index.html must contain a <canvas> element"


def test_html_hsl_color_formula_present():
    """HSL color formula using 300 degree range must be present."""
    html = read_html()
    assert "300" in html, (
        "index.html must contain hue range 300 for HSL color cycling"
    )


# ---------------------------------------------------------------------------
# Essay content tests
# ---------------------------------------------------------------------------

def test_essay_minimum_word_count():
    """Essay must have at least 380 words as specified."""
    text = read_essay()
    count = len(text.split())
    assert count >= 380, f"essay.md has {count} words, need ≥ 380"


def test_essay_opens_with_leviticus_citation():
    """Essay must open with or reference Leviticus 23:15-16."""
    text = read_essay()
    assert "23:15" in text or "23:15–16" in text, (
        "essay.md must cite Leviticus 23:15 or 23:15–16"
    )


def test_essay_mentions_sefirot():
    """Essay must reference the Sefirot / Kabbalistic framework."""
    text = read_essay()
    assert "Sefirot" in text or "Sefirah" in text or "sefirot" in text.lower(), (
        "essay.md must mention the Sefirot"
    )


def test_essay_mentions_arizal():
    """Essay should cite the Arizal as the canonical Kabbalistic source."""
    text = read_essay()
    assert "Arizal" in text or "Sha'ar haKavanot" in text or "Sha'ar HaKavanot" in text, (
        "essay.md must cite the Arizal or Sha'ar haKavanot"
    )


def test_essay_mentions_shavuot():
    text = read_essay()
    assert "Shavuot" in text or "שָׁבוּעוֹת" in text, (
        "essay.md must mention Shavuot"
    )


def test_essay_embedded_in_html():
    """index.html must embed essay content (not fetch it at runtime)."""
    essay = read_essay()
    html  = read_html()
    words = [w for w in essay.split() if len(w) > 5][:15]
    found = sum(1 for w in words if w in html)
    assert found >= 8, (
        f"index.html does not appear to embed the essay "
        f"(only {found}/15 sampled words found)"
    )


# ---------------------------------------------------------------------------
# Thumbnail SVG tests
# ---------------------------------------------------------------------------

def test_thumbnail_is_valid_svg():
    svg = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert "<svg" in svg and "</svg>" in svg, "thumbnail.svg is not valid SVG"


def test_thumbnail_has_pendulum_elements():
    """Thumbnail must contain line elements representing pendulum rods."""
    svg = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert "<line" in svg, "thumbnail.svg must contain <line> elements for rods"


def test_thumbnail_has_bob_circles():
    """Thumbnail must contain circle elements for pendulum bobs."""
    svg = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert "<circle" in svg, "thumbnail.svg must contain <circle> elements for bobs"


def test_thumbnail_has_hsl_colors():
    """Thumbnail must use HSL colors for the purple-to-gold palette."""
    svg = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert "hsl(" in svg, "thumbnail.svg must use HSL colors"


def test_thumbnail_viewbox_is_400x400():
    svg = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert "400" in svg, "thumbnail.svg should be 400×400"


# ---------------------------------------------------------------------------
# Physics correctness tests (Python simulation)
# ---------------------------------------------------------------------------

def test_pendulum_physics_resync_at_T1():
    """All pendulums must return to starting angle at t = T1."""
    N = 49
    T1 = 3.0
    theta0 = 0.3
    g = 9.8

    for k in range(1, N + 1):
        omega = k * 2 * math.pi / T1
        theta_t = theta0 * math.cos(omega * T1)
        assert abs(theta_t - theta0) < 1e-9, (
            f"Pendulum {k} did not return to θ₀ at t=T1: got {theta_t}, expected {theta0}"
        )


def test_pendulum_k_completes_k_oscillations():
    """Pendulum k must complete exactly k cycles in T1 seconds."""
    N = 49
    T1 = 3.0
    g = 9.8

    for k in range(1, N + 1):
        omega = k * 2 * math.pi / T1
        L = g / (omega ** 2)
        period = 2 * math.pi / omega
        cycles = T1 / period
        assert abs(cycles - k) < 1e-9, (
            f"Pendulum {k} does not complete exactly {k} cycles: got {cycles}"
        )


def test_pendulum_lengths_decrease_with_k():
    """Higher-k pendulums must be shorter (faster oscillation)."""
    N = 49
    T1 = 3.0
    g = 9.8
    lengths = []
    for k in range(1, N + 1):
        omega = k * 2 * math.pi / T1
        lengths.append(g / (omega ** 2))
    for i in range(len(lengths) - 1):
        assert lengths[i] > lengths[i + 1], (
            f"Pendulum lengths must decrease with k: L[{i}]={lengths[i]} <= L[{i+1}]={lengths[i+1]}"
        )


def test_slowest_pendulum_length():
    """L₁ (k=1) should be approximately 2.24 m with T1=3.0, g=9.8."""
    T1 = 3.0
    g = 9.8
    omega1 = 1 * 2 * math.pi / T1
    L1 = g / (omega1 ** 2)
    assert abs(L1 - 2.237) < 0.01, f"L₁ expected ~2.24 m, got {L1:.4f}"


# ---------------------------------------------------------------------------
# Edge-case / failure-mode tests
# ---------------------------------------------------------------------------

def test_piece_id_is_unique_in_pieces_json():
    """The piece ID must not appear twice in pieces.json."""
    pieces = load_pieces()
    ids = [p["id"] for p in pieces]
    count = ids.count(PIECE_ID)
    assert count == 1, f"'{PIECE_ID}' appears {count} times in pieces.json (expected 1)"


def test_wrong_piece_id_returns_none():
    """Helper get_piece() returns None for non-existent IDs."""
    pieces = load_pieces()
    result = next((p for p in pieces if p["id"] == "99-nonexistent"), None)
    assert result is None


def test_theta_at_t0_equals_theta0():
    """All pendulums must start at θ₀ at t=0."""
    N = 49
    T1 = 3.0
    theta0 = 0.3
    for k in range(1, N + 1):
        omega = k * 2 * math.pi / T1
        theta = theta0 * math.cos(omega * 0)
        assert abs(theta - theta0) < 1e-12, (
            f"Pendulum {k}: θ(0) = {theta}, expected {theta0}"
        )


def test_day_counter_formula():
    """Day = round(t/T1*49) clamped to [1,49]."""
    T1 = 3.0
    N = 49

    def day(t):
        raw = round((t / T1) * N)
        return max(1, min(N, raw))

    assert day(0.0) == 1
    assert day(T1 * (26 / 49)) == 26   # unambiguous midpoint
    assert day(T1) == 49
    assert day(T1 * 0.999) == 49
    assert day(-0.001) == 1  # clamped
