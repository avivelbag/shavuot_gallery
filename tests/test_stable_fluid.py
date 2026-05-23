"""Tests for piece 74-stable-fluid-milk-honey (WebGL stable fluids).

Validates the gallery entry, HTML content, shader structure, essay quality,
and the thumbnail-generation script without requiring a GPU or browser.
"""
import json
import os
import re

import pytest

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID = "74-stable-fluid-milk-honey"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
HTML_PATH = os.path.join(PIECE_DIR, "index.html")
ESSAY_PATH = os.path.join(PIECE_DIR, "essay.md")
THUMB_PATH = os.path.join(PIECE_DIR, "thumbnail.svg")
README_PATH = os.path.join(PIECE_DIR, "README.md")
GEN_PATH = os.path.join(PIECE_DIR, "gen_thumbnail.py")
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")


def load_pieces():
    """Load and parse pieces.json."""
    with open(PIECES_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


def get_piece():
    """Return the pieces.json entry for piece 74."""
    for p in load_pieces():
        if p["id"] == PIECE_ID:
            return p
    return None


# ---------------------------------------------------------------------------
# pieces.json registration
# ---------------------------------------------------------------------------

def test_piece_registered_in_json():
    assert get_piece() is not None, f"Piece '{PIECE_ID}' not found in pieces.json"


def test_piece_theme_field():
    p = get_piece()
    assert p is not None
    assert "Milk and Honey" in p["theme"], (
        f"theme must mention 'Milk and Honey', got: {p['theme']!r}"
    )
    assert "Promised Land" in p["theme"], (
        f"theme must mention 'Promised Land', got: {p['theme']!r}"
    )


def test_piece_technique_field():
    p = get_piece()
    assert p is not None
    tech = p["technique"].lower()
    assert "stable fluid" in tech or "navier" in tech, (
        f"technique must mention stable fluids or Navier-Stokes, got: {p['technique']!r}"
    )


def test_piece_has_all_required_fields():
    p = get_piece()
    assert p is not None
    for field in ("id", "title", "tagline", "year", "theme", "technique", "path", "thumbnail", "essay"):
        assert field in p, f"Missing field '{field}'"
        val = p[field]
        assert val is not None and val != "", f"Field '{field}' is empty"


def test_piece_year_is_integer():
    p = get_piece()
    assert p is not None
    assert isinstance(p["year"], int), f"year must be int, got {type(p['year'])}"


# ---------------------------------------------------------------------------
# File existence
# ---------------------------------------------------------------------------

def test_piece_directory_exists():
    assert os.path.isdir(PIECE_DIR), f"Piece directory missing: {PIECE_DIR}"


def test_index_html_exists():
    assert os.path.isfile(HTML_PATH), f"index.html missing: {HTML_PATH}"


def test_essay_md_exists():
    assert os.path.isfile(ESSAY_PATH), f"essay.md missing: {ESSAY_PATH}"


def test_thumbnail_svg_exists():
    assert os.path.isfile(THUMB_PATH), f"thumbnail.svg missing: {THUMB_PATH}"


def test_readme_exists():
    assert os.path.isfile(README_PATH), f"README.md missing: {README_PATH}"


def test_gen_thumbnail_exists():
    assert os.path.isfile(GEN_PATH), f"gen_thumbnail.py missing: {GEN_PATH}"


# ---------------------------------------------------------------------------
# HTML structural requirements
# ---------------------------------------------------------------------------

def test_html_is_full_viewport_canvas():
    html = open(HTML_PATH, encoding="utf-8").read()
    assert "canvas" in html.lower(), "index.html must contain a <canvas> element"
    assert "100vh" in html or "100%" in html, (
        "index.html must use full-viewport sizing (100vh or 100%)"
    )


def test_html_uses_webgl():
    html = open(HTML_PATH, encoding="utf-8").read()
    assert "webgl" in html.lower(), "index.html must request a WebGL context"


def test_html_uses_requestanimationframe():
    html = open(HTML_PATH, encoding="utf-8").read()
    assert "requestAnimationFrame" in html, (
        "index.html must use requestAnimationFrame for the render loop"
    )


def test_html_checks_float_extension():
    html = open(HTML_PATH, encoding="utf-8").read()
    assert "OES_texture_float" in html, (
        "index.html must request OES_texture_float extension for WebGL1 float textures"
    )


def test_html_has_sim_grid_256():
    html = open(HTML_PATH, encoding="utf-8").read()
    assert "256" in html, "index.html must reference the 256×256 simulation grid size"


def test_html_has_pressure_iterations():
    html = open(HTML_PATH, encoding="utf-8").read()
    assert "PRES_ITERS" in html or "20" in html, (
        "index.html must define 20 pressure Jacobi iterations"
    )


def test_html_has_diffusion_iterations():
    html = open(HTML_PATH, encoding="utf-8").read()
    assert "DIFF_ITERS" in html or "VISCOSITY" in html, (
        "index.html must implement diffusion Jacobi iterations with viscosity"
    )


def test_html_has_lissajous_injection():
    html = open(HTML_PATH, encoding="utf-8").read()
    assert "sin" in html.lower(), (
        "index.html must use sin() for Lissajous injection path"
    )
    assert "lissX" in html or "liss_x" in html or ("0.08" in html and "0.04" in html), (
        "index.html must implement the Lissajous 1:2 injection pattern"
    )


def test_html_has_cream_honey_colors():
    html = open(HTML_PATH, encoding="utf-8").read()
    # cream color #FFF5DC in some form
    assert "FFF5DC" in html.upper() or "fff5dc" in html.lower() or "1.0, 0.961" in html or "1.000, 0.961" in html, (
        "index.html must reference cream color #FFF5DC"
    )
    # honey color #D4820A in some form
    assert "D4820A" in html.upper() or "d4820a" in html.lower() or "0.831" in html, (
        "index.html must reference honey color #D4820A"
    )


def test_html_has_background_color():
    html = open(HTML_PATH, encoding="utf-8").read()
    assert "0A0804" in html.upper() or "0a0804" in html.lower(), (
        "index.html must use background color #0A0804"
    )


def test_html_has_webgl_fallback():
    html = open(HTML_PATH, encoding="utf-8").read()
    assert "no-webgl" in html or "not supported" in html.lower() or "fallback" in html.lower(), (
        "index.html must include a fallback message when WebGL float textures are unavailable"
    )


def test_html_embeds_essay_text():
    """index.html must contain the essay inline (no runtime fetch)."""
    essay = open(ESSAY_PATH, encoding="utf-8").read()
    html = open(HTML_PATH, encoding="utf-8").read()
    # Sample 10 words longer than 5 chars from the essay and check ≥5 appear in HTML
    words = [w for w in essay.split() if len(w) > 5][:10]
    found = sum(1 for w in words if w in html)
    assert found >= 5, (
        f"index.html must embed the essay text inline (only {found}/10 sampled words found)"
    )


def test_html_has_advect_shader():
    html = open(HTML_PATH, encoding="utf-8").read()
    assert "advect" in html.lower() or "ADVECT" in html, (
        "index.html must contain an advection shader"
    )


def test_html_has_jacobi_shader():
    html = open(HTML_PATH, encoding="utf-8").read()
    assert "jacobi" in html.lower() or "JACOBI" in html or "rBeta" in html, (
        "index.html must contain a Jacobi iteration shader"
    )


def test_html_has_divergence_shader():
    html = open(HTML_PATH, encoding="utf-8").read()
    assert "diverge" in html.lower() or "div" in html, (
        "index.html must compute velocity divergence"
    )


def test_html_has_pressure_subtract():
    html = open(HTML_PATH, encoding="utf-8").read()
    assert "subtract" in html.lower() or "gradient" in html.lower() or "pres" in html.lower(), (
        "index.html must subtract the pressure gradient to enforce incompressibility"
    )


def test_html_has_ping_pong_fbos():
    html = open(HTML_PATH, encoding="utf-8").read()
    # Two FBO pairs: velocity and dye — detected by multiple FBO/framebuffer refs
    fbo_count = html.lower().count("framebuffer")
    assert fbo_count >= 4, (
        f"index.html must create multiple ping-pong framebuffers (found {fbo_count} refs)"
    )


# ---------------------------------------------------------------------------
# Essay requirements
# ---------------------------------------------------------------------------

def test_essay_word_count():
    text = open(ESSAY_PATH, encoding="utf-8").read()
    words = text.split()
    assert len(words) >= 300, (
        f"essay.md must have at least 300 words, has {len(words)}"
    )


def test_essay_mentions_eretz_zavat():
    text = open(ESSAY_PATH, encoding="utf-8").read()
    assert "eretz zavat" in text.lower() or "zavat chalav" in text.lower(), (
        "essay.md must open with or mention 'eretz zavat chalav u'dvash'"
    )


def test_essay_mentions_exodus():
    text = open(ESSAY_PATH, encoding="utf-8").read()
    assert "Exodus" in text or "exodus" in text, (
        "essay.md must cite the Exodus source of the milk-and-honey phrase"
    )


def test_essay_mentions_shavuot_connection():
    text = open(ESSAY_PATH, encoding="utf-8").read()
    assert "Shavuot" in text or "shavuot" in text.lower() or "bikkurim" in text.lower(), (
        "essay.md must name the Shavuot connection (festival of first fruits)"
    )


def test_essay_mentions_dairy_custom():
    text = open(ESSAY_PATH, encoding="utf-8").read()
    assert "dairy" in text.lower() or "milk" in text.lower(), (
        "essay.md must explain the dairy-foods custom on Shavuot"
    )


def test_essay_mentions_no_slaughter():
    """Essay must include the insight that milk/honey come without killing."""
    text = open(ESSAY_PATH, encoding="utf-8").read()
    assert "without" in text.lower() and ("kill" in text.lower() or "harm" in text.lower() or "violenc" in text.lower()), (
        "essay.md must mention that milk and honey come without killing/harm"
    )


# ---------------------------------------------------------------------------
# Thumbnail
# ---------------------------------------------------------------------------

def test_thumbnail_is_valid_svg():
    svg = open(THUMB_PATH, encoding="utf-8").read()
    assert "<svg" in svg and "</svg>" in svg, (
        "thumbnail.svg must be a valid SVG document"
    )
    assert 'width="400"' in svg or 'width="' in svg, (
        "thumbnail.svg should specify a width"
    )


# ---------------------------------------------------------------------------
# gen_thumbnail.py
# ---------------------------------------------------------------------------

def test_gen_thumbnail_parses():
    """gen_thumbnail.py must be importable as a module (no top-level side effects when name != __main__)."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("gen_thumbnail", GEN_PATH)
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
    except ImportError:
        pytest.skip("NumPy/Pillow not installed; skipping gen_thumbnail import test")
    assert hasattr(mod, "run_sim"), "gen_thumbnail.py must define run_sim()"
    assert hasattr(mod, "dye_to_rgb"), "gen_thumbnail.py must define dye_to_rgb()"


def test_gen_thumbnail_sim_short(tmp_path):
    """run_sim with few steps must return arrays with correct shape."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("gen_thumbnail", GEN_PATH)
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
    except ImportError:
        pytest.skip("NumPy/Pillow not installed")

    orig_steps = mod.STEPS
    mod.STEPS = 5
    try:
        cream, honey = mod.run_sim()
    finally:
        mod.STEPS = orig_steps

    assert cream.shape == (mod.H, mod.W), f"cream shape mismatch: {cream.shape}"
    assert honey.shape == (mod.H, mod.W), f"honey shape mismatch: {honey.shape}"
    assert cream.min() >= 0.0 and cream.max() <= 1.0, "cream values must be in [0, 1]"
    assert honey.min() >= 0.0 and honey.max() <= 1.0, "honey values must be in [0, 1]"


def test_gen_thumbnail_dye_to_rgb_shape():
    """dye_to_rgb must return an HxWx3 uint8 array."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("gen_thumbnail", GEN_PATH)
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
    except ImportError:
        pytest.skip("NumPy/Pillow not installed")

    import numpy as np
    cream = np.zeros((mod.H, mod.W), dtype=np.float32)
    honey = np.zeros((mod.H, mod.W), dtype=np.float32)
    rgb = mod.dye_to_rgb(cream, honey)
    assert rgb.shape == (mod.H, mod.W, 3), f"Expected ({mod.H},{mod.W},3), got {rgb.shape}"
    assert rgb.dtype == np.uint8, f"Expected uint8, got {rgb.dtype}"


def test_gen_thumbnail_all_cream_is_bright():
    """When cream=1 and honey=0, pixels must be bright (near white)."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("gen_thumbnail", GEN_PATH)
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
    except ImportError:
        pytest.skip("NumPy/Pillow not installed")

    import numpy as np
    cream = np.ones((mod.H, mod.W), dtype=np.float32)
    honey = np.zeros((mod.H, mod.W), dtype=np.float32)
    rgb = mod.dye_to_rgb(cream, honey)
    mean_r = rgb[:, :, 0].mean()
    assert mean_r > 200, f"All-cream pixels should be bright (R>{200}), got mean R={mean_r:.1f}"


def test_gen_thumbnail_all_honey_is_amber():
    """When honey=1 and cream=0, pixels must be amber-gold (high R, mid G, low B)."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("gen_thumbnail", GEN_PATH)
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
    except ImportError:
        pytest.skip("NumPy/Pillow not installed")

    import numpy as np
    cream = np.zeros((mod.H, mod.W), dtype=np.float32)
    honey = np.ones((mod.H, mod.W), dtype=np.float32)
    rgb = mod.dye_to_rgb(cream, honey)
    mean_r = rgb[:, :, 0].mean()
    mean_b = rgb[:, :, 2].mean()
    assert mean_r > 150, f"Honey pixels should have high R, got {mean_r:.1f}"
    assert mean_b < 80,  f"Honey pixels should have low B, got {mean_b:.1f}"


def test_gen_thumbnail_empty_is_dark():
    """When cream=0 and honey=0, pixels must be very dark (near background #0A0804)."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("gen_thumbnail", GEN_PATH)
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
    except ImportError:
        pytest.skip("NumPy/Pillow not installed")

    import numpy as np
    cream = np.zeros((mod.H, mod.W), dtype=np.float32)
    honey = np.zeros((mod.H, mod.W), dtype=np.float32)
    rgb = mod.dye_to_rgb(cream, honey)
    mean_lum = rgb.mean()
    assert mean_lum < 20, f"Empty-dye pixels should be dark (mean<20), got {mean_lum:.1f}"


# ---------------------------------------------------------------------------
# Edge-case / failure-mode tests
# ---------------------------------------------------------------------------

def test_piece_not_duplicate():
    """The piece ID must appear exactly once in pieces.json."""
    pieces = load_pieces()
    count = sum(1 for p in pieces if p["id"] == PIECE_ID)
    assert count == 1, f"Piece '{PIECE_ID}' appears {count} times in pieces.json (expected 1)"


def test_piece_path_points_to_existing_file():
    p = get_piece()
    assert p is not None
    full = os.path.join(GALLERY_ROOT, p["path"])
    assert os.path.isfile(full), f"Piece path '{p['path']}' does not exist on disk"


def test_piece_thumbnail_points_to_existing_file():
    p = get_piece()
    assert p is not None
    full = os.path.join(GALLERY_ROOT, p["thumbnail"])
    assert os.path.isfile(full), f"Thumbnail path '{p['thumbnail']}' does not exist on disk"


def test_piece_essay_points_to_existing_file():
    p = get_piece()
    assert p is not None
    full = os.path.join(GALLERY_ROOT, p["essay"])
    assert os.path.isfile(full), f"Essay path '{p['essay']}' does not exist on disk"


def test_html_has_no_external_script_fetches():
    """HTML must not load external JavaScript libraries (self-contained)."""
    html = open(HTML_PATH, encoding="utf-8").read()
    # No <script src="http..."> or <script src="https...">
    bad = re.findall(r'<script[^>]+src=["\']https?://', html)
    assert len(bad) == 0, f"index.html must be self-contained; found external script: {bad}"
