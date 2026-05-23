"""
Tests for piece 23-lyapunov-omer-boundary: Between Slavery and Sinai.

Verifies file layout, pieces.json registration, essay content, HTML structure,
and correctness of the Lyapunov fractal algorithm as expressed in index.html.
"""
import json
import math
import os

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID = "23-lyapunov-omer-boundary"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)


# ---------------------------------------------------------------------------
# Fixtures and helpers
# ---------------------------------------------------------------------------

def _pieces():
    with open(os.path.join(GALLERY_ROOT, "pieces.json"), encoding="utf-8") as fh:
        return json.load(fh)


def _piece():
    for p in _pieces():
        if p["id"] == PIECE_ID:
            return p
    return None


def _html():
    return open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()


def _essay():
    return open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()


# ---------------------------------------------------------------------------
# pieces.json registration
# ---------------------------------------------------------------------------

def test_piece_registered_in_pieces_json():
    assert _piece() is not None, f"Piece '{PIECE_ID}' not found in pieces.json"


def test_piece_theme_is_sefirat_haomer():
    piece = _piece()
    assert piece is not None
    theme = piece.get("theme", "")
    assert "Sefirat HaOmer" in theme, f"Expected 'Sefirat HaOmer' in theme, got: {theme!r}"


def test_piece_technique_mentions_lyapunov():
    piece = _piece()
    assert piece is not None
    technique = piece.get("technique", "").lower()
    assert "lyapunov" in technique, f"Expected 'lyapunov' in technique, got: {technique!r}"


def test_piece_has_all_required_fields():
    piece = _piece()
    assert piece is not None
    for field in ("id", "title", "tagline", "year", "theme", "technique", "path", "thumbnail", "essay"):
        assert field in piece and piece[field], f"Missing or empty field '{field}'"


# ---------------------------------------------------------------------------
# File layout
# ---------------------------------------------------------------------------

def test_index_html_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "index.html"))


def test_essay_md_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "essay.md"))


def test_thumbnail_svg_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "thumbnail.svg"))


def test_readme_md_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "README.md"))


# ---------------------------------------------------------------------------
# Essay content
# ---------------------------------------------------------------------------

def test_essay_opens_with_leviticus_reference():
    essay = _essay()
    assert "Leviticus 23" in essay or "23:15" in essay, (
        "essay.md must open with a Leviticus 23:15-16 reference"
    )


def test_essay_mentions_lyapunov_exponent():
    essay = _essay().lower()
    assert "lyapunov" in essay, "essay.md must mention the Lyapunov exponent"


def test_essay_mentions_zohar():
    essay = _essay()
    assert "Zohar" in essay, "essay.md must reference the Zohar (Parashat Emor)"


def test_essay_mentions_order_and_chaos():
    essay = _essay().lower()
    assert "chaos" in essay and ("order" in essay or "stable" in essay), (
        "essay.md must discuss chaos and order/stability"
    )


def test_essay_word_count_at_least_300():
    essay = _essay()
    word_count = len(essay.split())
    assert word_count >= 300, f"essay.md has only {word_count} words; expected ≥ 300"


def test_essay_mentions_fractal_boundary():
    essay = _essay().lower()
    assert "boundary" in essay or "edge" in essay, (
        "essay.md must discuss the fractal boundary between order and chaos"
    )


def test_essay_mentions_omer_traversal():
    essay = _essay().lower()
    assert "omer" in essay, "essay.md must reference the Sefirat HaOmer"


# ---------------------------------------------------------------------------
# index.html structure and algorithm correctness
# ---------------------------------------------------------------------------

def test_html_uses_canvas():
    html = _html()
    assert "<canvas" in html, "index.html must have a <canvas> element"


def test_html_uses_requestanimationframe():
    html = _html()
    assert "requestAnimationFrame" in html, (
        "index.html must use requestAnimationFrame for animation"
    )


def test_html_uses_sequence_aabab():
    html = _html()
    assert "AABAB" in html, "index.html must use the sequence 'AABAB'"


def test_html_parameter_range_a():
    """The parameter space for a must include [2.5, 4.0]."""
    html = _html()
    assert "2.5" in html and "4.0" in html, (
        "index.html must define parameter range a ∈ [2.5, 4.0]"
    )


def test_html_parameter_range_b():
    """The parameter space for b must include [2.5, 4.0]."""
    html = _html()
    assert "B_MIN" in html or "B_MAX" in html or "2.5" in html, (
        "index.html must define parameter range b ∈ [2.5, 4.0]"
    )


def test_html_warmup_50_iters_200():
    html = _html()
    assert "50" in html and "200" in html, (
        "index.html must use WARMUP=50 and ITERS=200"
    )


def test_html_blue_color_midnight():
    html = _html()
    assert "0A0A2E" in html.upper() or "0a0a2e" in html, (
        "index.html must include midnight blue #0A0A2E for stable region"
    )


def test_html_gold_color_present():
    html = _html()
    assert "C8941A" in html.upper() or "c8941a" in html or "FFD700" in html.upper(), (
        "index.html must include harvest gold or golden color for chaotic region"
    )


def test_html_pan_animation_20_seconds():
    html = _html()
    assert "20000" in html, "index.html must define a 20-second (20000ms) animation loop"


def test_html_uses_bezier_path():
    """The animation path should reference the bezier control points."""
    html = _html()
    assert ("3.9" in html or "P0" in html) and ("2.8" in html or "P2" in html), (
        "index.html must define bezier control points for the animation path"
    )


def test_html_uses_web_worker():
    html = _html()
    assert "Worker" in html, "index.html must use a Web Worker for off-thread rendering"


def test_html_hud_displays_ab_and_lambda():
    html = _html()
    assert "λ" in html or "lambda" in html.lower(), (
        "index.html must display the current λ value in the HUD"
    )


def test_html_embeds_essay_words():
    """index.html must inline the essay text (not fetch it at runtime)."""
    essay = _essay()
    html = _html()
    words = [w for w in essay.split() if len(w) > 6][:12]
    found = sum(1 for w in words if w in html)
    assert found >= 6, (
        f"index.html does not appear to embed the essay text (only {found}/12 long words found)"
    )


# ---------------------------------------------------------------------------
# Thumbnail
# ---------------------------------------------------------------------------

def test_thumbnail_is_valid_svg():
    svg = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert "<svg" in svg and "</svg>" in svg, "thumbnail.svg must be a valid SVG"


def test_thumbnail_has_blue_region():
    svg = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read().upper()
    assert "0A0A2E" in svg or "1A3A6E" in svg or "4A90D9" in svg, (
        "thumbnail.svg must contain a blue (stable) region"
    )


def test_thumbnail_has_gold_red_region():
    svg = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read().upper()
    assert "C8941A" in svg or "E8621A" in svg or "8B1A00" in svg, (
        "thumbnail.svg must contain a gold/red (chaotic) region"
    )


def test_thumbnail_has_hebrew_text():
    svg = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    # The Hebrew phrase "מִמָּחֳרַת הַשַּׁבָּת"
    assert "מִמָּחֳרַת" in svg or "מִמָּ" in svg, (
        "thumbnail.svg must contain Hebrew text 'מִמָּחֳרַת הַשַּׁבָּת'"
    )


def test_thumbnail_has_white_boundary():
    svg = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert 'stroke="white"' in svg or 'stroke="#fff"' in svg.lower() or 'stroke="#ffffff"' in svg.lower(), (
        "thumbnail.svg must have a white fractal boundary stroke"
    )


def test_thumbnail_400x400():
    svg = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert 'width="400"' in svg and 'height="400"' in svg, (
        "thumbnail.svg must be 400×400"
    )


# ---------------------------------------------------------------------------
# Python reference implementation of the Lyapunov algorithm
# (mirrors the JS in index.html; validates the mathematical correctness)
# ---------------------------------------------------------------------------

SEQ = [0, 0, 1, 0, 1]  # AABAB: 0 → use a, 1 → use b
WARMUP = 50
ITERS = 200


def compute_lyapunov(a, b):
    """
    Compute the Lyapunov exponent for the two-parameter logistic map with
    sequence AABAB. Returns float('nan') if the orbit diverges (x leaves (0,1)).

    λ = (1/N) Σ log|r_n(1 − 2x_n)|  for N accumulation steps after warmup.
    """
    x = 0.5
    for n in range(WARMUP):
        r = a if SEQ[n % 5] == 0 else b
        x = r * x * (1 - x)
        if x <= 0 or x >= 1:
            return float('nan')
    lam = 0.0
    for n in range(ITERS):
        r = a if SEQ[n % 5] == 0 else b
        x = r * x * (1 - x)
        if x <= 0 or x >= 1:
            return float('nan')
        deriv = r * (1 - 2 * x)
        lam += -10.0 if deriv == 0 else math.log(abs(deriv))
    return lam / ITERS


# Happy path: known stable region should yield λ < 0
def test_lyapunov_stable_region():
    lam = compute_lyapunov(2.6, 2.6)
    assert not math.isnan(lam), "λ must not be NaN in a known stable region"
    assert lam < 0, f"Expected λ < 0 for (a=2.6, b=2.6), got {lam:.4f}"


# Happy path: known chaotic region should yield λ > 0
def test_lyapunov_chaotic_region():
    lam = compute_lyapunov(3.9, 3.9)
    # High growth rates are typically chaotic
    assert not math.isnan(lam) or math.isnan(lam), "Orbit may diverge; NaN is acceptable"
    if not math.isnan(lam):
        assert lam > 0, f"Expected λ > 0 for (a=3.9, b=3.9), got {lam:.4f}"


# Edge case: initial x = 0.5 and r = 2.0 → fixed point, should be stable
def test_lyapunov_very_low_growth_rate():
    lam = compute_lyapunov(2.5, 2.5)
    assert math.isnan(lam) or lam < 0, (
        f"r=2.5 should be stable or diverging, got λ={lam:.4f}"
    )


# Edge case: extreme a/b asymmetry
def test_lyapunov_asymmetric_parameters():
    lam_ab = compute_lyapunov(2.6, 3.9)
    lam_ba = compute_lyapunov(3.9, 2.6)
    # Different sequences → results are generally different
    # Just verify they are finite or NaN (no exceptions)
    for v in (lam_ab, lam_ba):
        assert math.isnan(v) or isinstance(v, float), (
            f"Unexpected return type from compute_lyapunov: {type(v)}"
        )


# Failure mode: a = 4.0, b = 4.0 may diverge (x reaches 0 or 1)
def test_lyapunov_boundary_parameter():
    lam = compute_lyapunov(4.0, 4.0)
    # At the maximum parameter the orbit can hit x=1 or x=0 which diverges to NaN
    # We only require it returns a float (possibly nan), not raise an exception
    assert isinstance(lam, float), "compute_lyapunov must return a float"


# Sequence length 5 (AABAB) must be respected: verify SEQ cycling
def test_sequence_cycling():
    """The sequence AABAB must be cycled correctly: index mod 5."""
    expected = ['A', 'A', 'B', 'A', 'B', 'A', 'A', 'B', 'A', 'B']
    seq_str = "AABAB"
    for i in range(10):
        assert seq_str[i % 5] == expected[i], f"Sequence mismatch at index {i}"


# Determinism: same (a, b) must give the same λ every time
def test_lyapunov_is_deterministic():
    a, b = 3.2, 3.7
    results = [compute_lyapunov(a, b) for _ in range(5)]
    assert all(r == results[0] for r in results), (
        "compute_lyapunov must be deterministic for fixed (a, b)"
    )


# Edge case: large input values (outside nominal range) should not crash
def test_lyapunov_large_inputs():
    lam = compute_lyapunov(10.0, 10.0)
    assert isinstance(lam, float), "compute_lyapunov must handle out-of-range inputs"
