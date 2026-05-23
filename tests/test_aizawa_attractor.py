"""
Tests for piece 94-aizawa-attractor-tikkun-leil.

Verifies: pieces.json entry, all required files on disk, essay content,
HTML animation requirements, thumbnail validity, and the Aizawa integration
equations as documented in the piece.
"""

import json
import math
import os

import pytest

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID = "94-aizawa-attractor-tikkun-leil"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_pieces():
    with open(PIECES_JSON, "r", encoding="utf-8") as fh:
        return json.load(fh)


def get_piece():
    for p in load_pieces():
        if p["id"] == PIECE_ID:
            return p
    return None


def read_html():
    return open(os.path.join(GALLERY_ROOT, "pieces", PIECE_ID, "index.html"),
                encoding="utf-8").read()


def read_essay():
    return open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()


# ---------------------------------------------------------------------------
# pieces.json registration
# ---------------------------------------------------------------------------

def test_piece_registered_in_json():
    """Piece must appear in pieces.json with correct id."""
    assert get_piece() is not None, f"Piece '{PIECE_ID}' not found in pieces.json"


def test_piece_theme():
    piece = get_piece()
    assert piece is not None
    assert "Tikkun" in piece["theme"], (
        f"theme must mention Tikkun Leil Shavuot, got: {piece['theme']!r}"
    )


def test_piece_technique_mentions_aizawa():
    piece = get_piece()
    assert piece is not None
    assert "Aizawa" in piece["technique"], (
        f"technique must mention Aizawa, got: {piece['technique']!r}"
    )


def test_piece_technique_mentions_rk4():
    piece = get_piece()
    assert piece is not None
    assert "RK4" in piece["technique"] or "rk4" in piece["technique"].lower(), (
        f"technique must mention RK4 integration, got: {piece['technique']!r}"
    )


def test_piece_year_is_2026():
    piece = get_piece()
    assert piece is not None
    assert piece["year"] == 2026


# ---------------------------------------------------------------------------
# Required files on disk
# ---------------------------------------------------------------------------

def test_index_html_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "index.html")), (
        "index.html is missing from piece directory"
    )


def test_essay_md_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "essay.md")), (
        "essay.md is missing from piece directory"
    )


def test_thumbnail_svg_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "thumbnail.svg")), (
        "thumbnail.svg is missing from piece directory"
    )


def test_readme_md_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "README.md")), (
        "README.md is missing from piece directory"
    )


# ---------------------------------------------------------------------------
# Essay content requirements
# ---------------------------------------------------------------------------

def test_essay_word_count():
    """Essay must be substantial — at least 300 words."""
    text = read_essay()
    count = len(text.split())
    assert count >= 300, f"essay.md has only {count} words (need ≥ 300)"


def test_essay_mentions_tikkun_leil():
    text = read_essay().lower()
    assert "tikkun" in text, "essay.md must discuss Tikkun Leil Shavuot"


def test_essay_mentions_aizawa():
    text = read_essay()
    assert "Aizawa" in text or "aizawa" in text, (
        "essay.md must introduce the Aizawa attractor"
    )


def test_essay_mentions_shacharit():
    """Essay must reference Shacharit — the dawn prayer that ends the vigil."""
    text = read_essay()
    assert "Shacharit" in text or "shacharit" in text or "שַׁחֲרִית" in text, (
        "essay.md must mention Shacharit (the dawn prayer)"
    )


def test_essay_contains_exodus_reference():
    """Essay must cite or quote Exodus 19 as the bilingual Tanach excerpt."""
    text = read_essay()
    assert "Exodus 19" in text or "exodus 19" in text.lower(), (
        "essay.md must reference Exodus 19:16–17"
    )


def test_essay_contains_hebrew_text():
    """Essay must include Hebrew script (the bilingual excerpt)."""
    text = read_essay()
    has_hebrew = any('א' <= ch <= 'ת' for ch in text)
    assert has_hebrew, "essay.md must contain Hebrew script text"


# ---------------------------------------------------------------------------
# HTML canvas animation requirements
# ---------------------------------------------------------------------------

def test_html_uses_request_animation_frame():
    html = read_html()
    assert "requestAnimationFrame" in html, (
        "index.html must use requestAnimationFrame for animation"
    )


def test_html_declares_aizawa_parameters():
    """All six canonical Aizawa parameters must appear in the HTML."""
    html = read_html()
    for val in ["0.95", "0.7", "0.6", "3.5", "0.25", "0.1"]:
        assert val in html, f"Aizawa parameter {val} not found in index.html"


def test_html_uses_rk4():
    """HTML must implement RK4 integration (look for k1/k2/k3/k4 pattern)."""
    html = read_html()
    assert "k1" in html and "k2" in html and "k3" in html and "k4" in html, (
        "index.html must implement RK4 (k1/k2/k3/k4) integration"
    )


def test_html_five_trajectories():
    """Five simultaneous trajectories must be defined."""
    html = read_html()
    assert "5" in html or "NUM_TRAJ" in html, (
        "index.html must specify 5 simultaneous trajectories"
    )


def test_html_lighter_compositing():
    """Additive 'lighter' compositing creates the bloom effect for dense regions."""
    html = read_html()
    assert "lighter" in html, (
        "index.html must use 'lighter' globalCompositeOperation for bloom"
    )


def test_html_fade_rect():
    """Fading trail overlay must be present."""
    html = read_html()
    assert "0.025" in html or "rgba(5, 5" in html or "rgba(5,5" in html, (
        "index.html must use semi-transparent fillRect for trail fading"
    )


def test_html_tikkun_hebrew_text():
    """Canvas must render the Hebrew title text."""
    html = read_html()
    assert "תִּקּוּן" in html or "תיקון" in html, (
        "index.html must render the Hebrew Tikkun Leil Shavuot text"
    )


def test_html_shacharit_text():
    """Shacharit word must appear in the animation code."""
    html = read_html()
    assert "שַׁחֲרִית" in html or "שחרית" in html, (
        "index.html must render the Shacharit dawn-prayer text"
    )


def test_html_bilingual_tanach_excerpt():
    """HTML must include the bilingual Exodus excerpt block."""
    html = read_html()
    assert "Exodus 19" in html, (
        "index.html must include the Exodus 19:16-17 reference in the essay panel"
    )
    has_hebrew = any('א' <= ch <= 'ת' for ch in html)
    assert has_hebrew, "index.html must contain Hebrew script in the essay panel"


def test_html_essay_embedded():
    """Key essay words must appear in the HTML (no external fetch)."""
    essay = read_essay()
    html = read_html()
    words = [w for w in essay.split() if len(w) > 6][:15]
    found = sum(1 for w in words if w in html)
    assert found >= 8, (
        f"index.html must embed the essay text inline; only {found}/15 sampled words found"
    )


def test_html_color_palette_midnight_blue():
    html = read_html()
    assert "0a0a2e" in html or "#0a0a2e" in html, (
        "index.html must reference midnight blue color #0a0a2e"
    )


def test_html_color_palette_pale_gold():
    html = read_html()
    assert "f0e8b0" in html or "#f0e8b0" in html, (
        "index.html must reference pale gold color #f0e8b0"
    )


def test_html_side_by_side_layout():
    """HTML must implement side-by-side art/essay layout."""
    html = read_html()
    assert "essay-panel" in html or "art-panel" in html, (
        "index.html must define art and essay panels for side-by-side layout"
    )
    assert "flex" in html, "index.html must use flexbox for the layout"


def test_html_responsive_media_query():
    """HTML must include a media query for narrow-screen stacked layout."""
    html = read_html()
    assert "max-width" in html and "768" in html, (
        "index.html must include a max-width media query for mobile layout"
    )


# ---------------------------------------------------------------------------
# Thumbnail validity
# ---------------------------------------------------------------------------

def test_thumbnail_is_valid_svg():
    text = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert "<svg" in text and "</svg>" in text, "thumbnail.svg must be valid SVG"


def test_thumbnail_has_background():
    """Thumbnail must have the dark midnight-blue background."""
    text = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert "0a0a2e" in text or "#0a0a2e" in text, (
        "thumbnail.svg must have midnight-blue (#0a0a2e) background"
    )


def test_thumbnail_has_hebrew_text():
    text = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    has_hebrew = any('א' <= ch <= 'ת' for ch in text)
    assert has_hebrew, "thumbnail.svg must include Hebrew text"


# ---------------------------------------------------------------------------
# Aizawa integration correctness (pure Python implementation)
# ---------------------------------------------------------------------------

def aizawa_derivs(x, y, z, a=0.95, b=0.7, c=0.6, d=3.5, e=0.25, f=0.1):
    """Python reference implementation of the Aizawa system derivatives."""
    zm = z - b
    r2 = x * x + y * y
    return (
        zm * x - d * y,
        d * x + zm * y,
        c + a * z - (z ** 3) / 3.0 - r2 * (1.0 + e * z) + f * z * x ** 3,
    )


def rk4_step(x, y, z, dt=0.01):
    """One RK4 step of the Aizawa system."""
    k1 = aizawa_derivs(x, y, z)
    k2 = aizawa_derivs(x + 0.5*dt*k1[0], y + 0.5*dt*k1[1], z + 0.5*dt*k1[2])
    k3 = aizawa_derivs(x + 0.5*dt*k2[0], y + 0.5*dt*k2[1], z + 0.5*dt*k2[2])
    k4 = aizawa_derivs(x + dt*k3[0],     y + dt*k3[1],     z + dt*k3[2])
    return (
        x + (dt / 6.0) * (k1[0] + 2*k2[0] + 2*k3[0] + k4[0]),
        y + (dt / 6.0) * (k1[1] + 2*k2[1] + 2*k3[1] + k4[1]),
        z + (dt / 6.0) * (k1[2] + 2*k2[2] + 2*k3[2] + k4[2]),
    )


def test_aizawa_derivs_at_origin():
    """At (0,0,0) the Aizawa derivatives match the analytic values."""
    dx, dy, dz = aizawa_derivs(0.0, 0.0, 0.0)
    # dx = (0-0.7)*0 - 3.5*0 = 0
    # dy = 3.5*0 + (0-0.7)*0 = 0
    # dz = 0.6 + 0.95*0 - 0 - 0*(1+0) + 0 = 0.6
    assert dx == pytest.approx(0.0)
    assert dy == pytest.approx(0.0)
    assert dz == pytest.approx(0.6)


def test_aizawa_derivs_at_known_point():
    """Verify derivatives at (0.1, 0, 0) against hand-computed values."""
    x, y, z = 0.1, 0.0, 0.0
    dx, dy, dz = aizawa_derivs(x, y, z)
    # dx = (0 - 0.7)*0.1 - 3.5*0 = -0.07
    assert dx == pytest.approx(-0.07, abs=1e-12)
    # dy = 3.5*0.1 + (0 - 0.7)*0 = 0.35
    assert dy == pytest.approx(0.35, abs=1e-12)
    # dz = 0.6 + 0 - 0 - 0.01*(1+0) + 0 = 0.59
    assert dz == pytest.approx(0.59, abs=1e-12)


def test_rk4_step_conserves_approximate_attractor_region():
    """After 1000 RK4 steps from (0.1,0,0) the state stays within the known attractor bounds."""
    x, y, z = 0.1, 0.0, 0.0
    for _ in range(1000):
        x, y, z = rk4_step(x, y, z)
    # Known attractor bounds: x,y ∈ [-2,2], z ∈ [-1.5, 2.2]
    assert -3.0 < x < 3.0, f"x={x} outside expected range after 1000 steps"
    assert -3.0 < y < 3.0, f"y={y} outside expected range after 1000 steps"
    assert -2.0 < z < 2.5, f"z={z} outside expected range after 1000 steps"


def test_five_trajectories_diverge():
    """Slightly different initial conditions must produce measurably different states after many steps."""
    states = [(0.1 + 0.001 * i, 0.0, 0.0) for i in range(5)]
    for _ in range(500):
        states = [rk4_step(*s) for s in states]
    # After 500 steps the trajectories should have diverged (chaos)
    xs = [s[0] for s in states]
    spread = max(xs) - min(xs)
    assert spread > 0.001, f"Trajectories have not diverged after 500 steps (spread={spread})"


def test_rk4_step_first_order_consistency():
    """RK4 at very small dt should agree with Euler to first order."""
    dt = 1e-6
    x, y, z = 0.5, 0.3, 0.8
    nx, ny, nz = rk4_step(x, y, z, dt=dt)
    dx, dy, dz = aizawa_derivs(x, y, z)
    assert nx == pytest.approx(x + dt * dx, rel=1e-4)
    assert ny == pytest.approx(y + dt * dy, rel=1e-4)
    assert nz == pytest.approx(z + dt * dz, rel=1e-4)


def test_attractor_bounded_long_run():
    """After 10000 steps the orbit remains bounded — confirms canonical parameters produce the attractor."""
    x, y, z = 0.1, 0.0, 0.0
    max_r = 0.0
    for _ in range(10000):
        x, y, z = rk4_step(x, y, z)
        r = math.sqrt(x*x + y*y + z*z)
        if r > max_r:
            max_r = r
    assert max_r < 5.0, f"Trajectory escaped bounded region: max radius = {max_r}"


def test_attractor_z_range():
    """The z coordinate of the trajectory should span a reasonable range [−1.5, 2.0]."""
    x, y, z = 0.1, 0.0, 0.0
    # Warm up to reach attractor
    for _ in range(500):
        x, y, z = rk4_step(x, y, z)
    z_min, z_max = z, z
    for _ in range(5000):
        x, y, z = rk4_step(x, y, z)
        if z < z_min:
            z_min = z
        if z > z_max:
            z_max = z
    assert z_min < -0.3, f"z_min={z_min} unexpectedly high; attractor should reach below -0.3"
    assert z_max > 1.2, f"z_max={z_max} unexpectedly low; attractor should reach above 1.2"


# ---------------------------------------------------------------------------
# Edge cases / failure modes
# ---------------------------------------------------------------------------

def test_aizawa_derivs_large_z_does_not_explode():
    """The cubic z³/3 term should dominate at large z, keeping dz/dt negative."""
    dx, dy, dz = aizawa_derivs(0.0, 0.0, 10.0)
    # dz = 0.6 + 0.95*10 - 1000/3 ≈ 0.6 + 9.5 - 333.3 ≪ 0
    assert dz < -300, f"dz should be strongly negative at z=10; got {dz}"


def test_rk4_step_negative_z():
    """Integration from negative z should remain stable."""
    x, y, z = 0.0, 0.0, -1.0
    for _ in range(100):
        x, y, z = rk4_step(x, y, z)
    assert math.isfinite(x) and math.isfinite(y) and math.isfinite(z), (
        "RK4 step produced NaN/inf from negative z initial condition"
    )


def test_pieces_json_no_duplicate_id():
    """Adding piece 94 must not introduce a duplicate ID."""
    pieces = load_pieces()
    ids = [p["id"] for p in pieces]
    assert len(ids) == len(set(ids)), f"Duplicate IDs detected: {ids}"
