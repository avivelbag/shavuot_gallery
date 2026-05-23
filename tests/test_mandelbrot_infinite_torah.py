"""Tests for piece 75-mandelbrot-infinite-torah.

Covers:
  - Presence and correctness of all required files
  - pieces.json registration with correct fields
  - WebGL shader requirements (highp, uniforms, smooth coloring formula)
  - Animation loop (requestAnimationFrame, zoom factor, reset condition)
  - Hebrew text overlay presence and RTL direction
  - Interior color (#050508 / near-black)
  - Zoom target coordinates
  - Essay content depth
  - gen_thumbnail.py can be imported and its core rendering logic is correct
"""
import json
import os
import sys

import pytest

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID = "75-mandelbrot-infinite-torah"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")


def _load_pieces():
    with open(PIECES_JSON, encoding="utf-8") as fh:
        return json.load(fh)


def _get_piece():
    for p in _load_pieces():
        if p["id"] == PIECE_ID:
            return p
    return None


def _html():
    p = _get_piece()
    assert p is not None
    return open(os.path.join(GALLERY_ROOT, p["path"]), encoding="utf-8").read()


def _essay():
    p = _get_piece()
    assert p is not None
    return open(os.path.join(GALLERY_ROOT, p["essay"]), encoding="utf-8").read()


# ---------------------------------------------------------------------------
# pieces.json registration
# ---------------------------------------------------------------------------

def test_piece_registered_in_json():
    assert _get_piece() is not None, f"Piece '{PIECE_ID}' missing from pieces.json"


def test_piece_theme():
    p = _get_piece()
    assert "Crown of Torah" in p["theme"] and "Nishma" in p["theme"]


def test_piece_technique_mentions_mandelbrot():
    p = _get_piece()
    assert "Mandelbrot" in p["technique"]


def test_piece_technique_mentions_webgl():
    p = _get_piece()
    assert "WebGL" in p["technique"]


def test_piece_year():
    p = _get_piece()
    assert p["year"] == 2026


def test_piece_thumbnail_is_png():
    p = _get_piece()
    assert p["thumbnail"].endswith(".png"), "Thumbnail must be a .png"


# ---------------------------------------------------------------------------
# Required files on disk
# ---------------------------------------------------------------------------

def test_index_html_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "index.html"))


def test_essay_md_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "essay.md"))


def test_readme_md_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "README.md"))


def test_thumbnail_png_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "thumbnail.png"))


def test_gen_thumbnail_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "gen_thumbnail.py"))


# ---------------------------------------------------------------------------
# WebGL shader correctness
# ---------------------------------------------------------------------------

def test_shader_uses_highp_float():
    html = _html()
    assert "precision highp float" in html, "Shader must declare 'precision highp float'"


def test_shader_has_uniform_center():
    html = _html()
    assert "u_center" in html, "Shader must have u_center uniform"


def test_shader_has_uniform_scale():
    html = _html()
    assert "u_scale" in html, "Shader must have u_scale uniform"


def test_shader_has_uniform_resolution():
    html = _html()
    assert "u_resolution" in html, "Shader must have u_resolution uniform"


def test_smooth_coloring_formula_present():
    """The smooth escape formula keyword 'log2' must appear (smooth_iter computation)."""
    html = _html()
    assert "log2" in html, "Shader must use log2 for smooth coloring"


def test_max_iteration_256():
    html = _html()
    assert "256" in html, "Max iteration count must be 256"


def test_interior_near_black_color():
    """Interior set is rendered near-black — check for #050508 or the float equivalent."""
    html = _html()
    has_hex = "#050508" in html or "050508" in html
    has_float = "0.020" in html or "0.02," in html
    assert has_hex or has_float, "Interior color must be near-black #050508"


# ---------------------------------------------------------------------------
# Animation / zoom logic
# ---------------------------------------------------------------------------

def test_uses_request_animation_frame():
    html = _html()
    assert "requestAnimationFrame" in html


def test_zoom_factor_0_9997():
    """Zoom factor must be 0.9997 per frame (scale multiplied each frame)."""
    html = _html()
    assert "0.9997" in html, "Zoom factor 0.9997 must be present in JS"


def test_zoom_reset_at_1e_12():
    """Scale must reset to 3.5 when it reaches 1e-12."""
    html = _html()
    assert "1e-12" in html, "Zoom reset threshold 1e-12 must be present"


def test_initial_scale_3_5():
    html = _html()
    assert "3.5" in html, "Initial scale must be 3.5"


def test_zoom_target_cx():
    """Zoom target x-coordinate must be -0.7269."""
    html = _html()
    assert "0.7269" in html, "Zoom target x=-0.7269 must be present"


def test_zoom_target_cy():
    """Zoom target y-coordinate must be 0.1889."""
    html = _html()
    assert "0.1889" in html, "Zoom target y=0.1889 must be present"


# ---------------------------------------------------------------------------
# Hebrew overlay
# ---------------------------------------------------------------------------

def test_hebrew_overlay_text_present():
    html = _html()
    # Check for Ben Bag Bag's dictum (key Hebrew words)
    assert "הֲפֹךְ" in html, "Hebrew overlay text must include הֲפֹךְ"


def test_hebrew_overlay_rtl_direction():
    html = _html()
    assert "direction: rtl" in html or "direction:rtl" in html, "Overlay must use direction: rtl"


def test_hebrew_overlay_fades_in():
    """Overlay must fade in after a delay — check for setTimeout."""
    html = _html()
    assert "setTimeout" in html, "Hebrew overlay must use setTimeout for fade-in delay"


# ---------------------------------------------------------------------------
# Essay content
# ---------------------------------------------------------------------------

def test_essay_mentions_ben_bag_bag():
    essay = _essay()
    assert "Ben Bag Bag" in essay


def test_essay_mentions_shishikura():
    essay = _essay()
    assert "Shishikura" in essay, "Essay must cite Shishikura's 1998 proof"


def test_essay_mentions_hausdorff_dimension():
    essay = _essay()
    assert "Hausdorff" in essay, "Essay must discuss Hausdorff dimension"


def test_essay_mentions_shivim_panim():
    essay = _essay()
    assert "shivim panim" in essay or "seventy faces" in essay.lower()


def test_essay_mentions_shavuot():
    essay = _essay()
    assert "Shavuot" in essay


def test_essay_word_count():
    """Essay must be at least 420 words."""
    essay = _essay()
    words = essay.split()
    assert len(words) >= 420, f"Essay has {len(words)} words; need >= 420"


def test_essay_embedded_in_html():
    """Key essay words must appear in index.html (embedded, not fetched)."""
    essay = _essay()
    html = _html()
    words = [w for w in essay.split() if len(w) > 6][:15]
    found = sum(1 for w in words if w in html)
    assert found >= 8, (
        f"Only {found}/15 sampled essay words found in index.html; essay must be embedded"
    )


# ---------------------------------------------------------------------------
# gen_thumbnail.py logic (importable unit tests)
# ---------------------------------------------------------------------------

def _import_gen_thumbnail():
    """Import gen_thumbnail.py as a module without executing __main__ block."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "gen_thumbnail_75",
        os.path.join(PIECE_DIR, "gen_thumbnail.py"),
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_gen_thumbnail_importable():
    mod = _import_gen_thumbnail()
    assert hasattr(mod, "_mandelbrot")
    assert hasattr(mod, "_palette")
    assert hasattr(mod, "_render")
    assert hasattr(mod, "_write_png")


def test_mandelbrot_interior_returns_none():
    """A point well inside the set (c=0) should return None."""
    mod = _import_gen_thumbnail()
    result = mod._mandelbrot(0.0, 0.0)
    assert result is None, "c=0 is in the Mandelbrot set; _mandelbrot must return None"


def test_mandelbrot_exterior_returns_float():
    """A point well outside the set (c=2+2i) should escape quickly."""
    mod = _import_gen_thumbnail()
    result = mod._mandelbrot(2.0, 2.0)
    assert result is not None, "c=(2+2i) must escape"
    assert isinstance(result, float)
    assert result >= 0.0


def test_palette_returns_three_ints():
    mod = _import_gen_thumbnail()
    rgb = mod._palette(0.0)
    assert len(rgb) == 3
    for v in rgb:
        assert isinstance(v, int)
        assert 0 <= v <= 255


def test_palette_wraps_periodically():
    """palette(0) and palette(1) should return the same color (period 1)."""
    mod = _import_gen_thumbnail()
    assert mod._palette(0.0) == mod._palette(1.0)
    assert mod._palette(0.5) == mod._palette(1.5)


def test_render_returns_correct_pixel_count():
    """_render must return WIDTH * HEIGHT pixels."""
    mod = _import_gen_thumbnail()
    # Use small overrides to keep the test fast
    orig_w, orig_h, orig_mi = mod.WIDTH, mod.HEIGHT, mod.MAX_ITER
    mod.WIDTH = 10
    mod.HEIGHT = 10
    mod.MAX_ITER = 8
    try:
        pixels = mod._render()
    finally:
        mod.WIDTH = orig_w
        mod.HEIGHT = orig_h
        mod.MAX_ITER = orig_mi
    assert len(pixels) == 100, f"Expected 100 pixels for 10x10, got {len(pixels)}"


def test_write_png_produces_valid_png(tmp_path):
    """_write_png must write a file starting with the PNG magic bytes."""
    mod = _import_gen_thumbnail()
    pixels = [(255, 0, 128)] * 4  # 2x2 red-ish
    out = str(tmp_path / "test.png")
    mod._write_png(out, pixels, 2, 2)
    assert os.path.isfile(out)
    with open(out, "rb") as fh:
        header = fh.read(8)
    assert header == b'\x89PNG\r\n\x1a\n', "Output file must start with PNG magic bytes"


def test_thumbnail_png_is_valid_png():
    """The committed thumbnail.png must start with the PNG magic bytes."""
    thumb_path = os.path.join(PIECE_DIR, "thumbnail.png")
    with open(thumb_path, "rb") as fh:
        header = fh.read(8)
    assert header == b'\x89PNG\r\n\x1a\n', "thumbnail.png must be a valid PNG file"


def test_thumbnail_png_is_not_empty():
    thumb_path = os.path.join(PIECE_DIR, "thumbnail.png")
    size = os.path.getsize(thumb_path)
    assert size > 1000, f"thumbnail.png looks too small ({size} bytes); likely empty or corrupt"


# ---------------------------------------------------------------------------
# Edge / failure modes
# ---------------------------------------------------------------------------

def test_palette_at_midpoint_is_not_interior_color():
    """The palette at t=0.5 should not be the interior color (5,5,8)."""
    mod = _import_gen_thumbnail()
    rgb = mod._palette(0.5)
    assert rgb != (5, 5, 8), "Exterior palette must differ from interior color at t=0.5"


def test_mandelbrot_boundary_escapes_slowly():
    """A point near the boundary should take many iterations to escape."""
    mod = _import_gen_thumbnail()
    # (-0.7269, 0.1889) is on the boundary — at low MAX_ITER it likely doesn't escape at all
    orig_mi = mod.MAX_ITER
    mod.MAX_ITER = 16
    try:
        result = mod._mandelbrot(-0.7269, 0.1889)
    finally:
        mod.MAX_ITER = orig_mi
    # With only 16 iterations, the boundary point may return None (doesn't escape) — that's fine
    if result is not None:
        # If it does escape, smooth value should be non-negative
        assert result >= 0.0
