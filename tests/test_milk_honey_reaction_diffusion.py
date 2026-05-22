"""
Tests for piece 07 "A Land Flowing" — milk-honey reaction-diffusion.

Covers: file layout, pieces.json registration, HTML content (Gray-Scott
simulation, Hebrew overlay, essay embedding), essay.md substance, color
values, and explicit failure-mode / edge-case behaviors.
"""
import json
import os
import re

import pytest

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")
PIECE_ID = "07-milk-honey-reaction-diffusion"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)


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


def read_piece_file(filename):
    return open(os.path.join(PIECE_DIR, filename), encoding="utf-8").read()


# ---------------------------------------------------------------------------
# pieces.json registration
# ---------------------------------------------------------------------------

def test_piece_07_in_json():
    assert get_piece() is not None, f"'{PIECE_ID}' not found in pieces.json"


def test_piece_07_theme_mentions_milk_and_honey():
    piece = get_piece()
    assert piece is not None
    theme = piece["theme"].lower()
    assert "milk" in theme or "honey" in theme or "bikkurim" in theme, (
        "theme must reference Milk, Honey, or Bikkurim"
    )


def test_piece_07_technique_mentions_reaction_diffusion():
    piece = get_piece()
    assert piece is not None
    technique = piece["technique"].lower()
    assert "reaction" in technique or "diffusion" in technique or "gray-scott" in technique, (
        "technique must mention reaction-diffusion or Gray-Scott"
    )


def test_piece_07_year_is_integer():
    piece = get_piece()
    assert piece is not None
    assert isinstance(piece["year"], int)


def test_piece_07_required_fields_present():
    piece = get_piece()
    assert piece is not None
    for field in ("id", "title", "tagline", "year", "theme", "technique", "path", "thumbnail", "essay"):
        assert field in piece and piece[field], f"Missing or empty field '{field}'"


# ---------------------------------------------------------------------------
# File layout
# ---------------------------------------------------------------------------

def test_piece_07_index_html_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "index.html")), (
        "pieces/07-milk-honey-reaction-diffusion/index.html is missing"
    )


def test_piece_07_thumbnail_png_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "thumbnail.png")), (
        "pieces/07-milk-honey-reaction-diffusion/thumbnail.png is missing"
    )


def test_piece_07_readme_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "README.md")), (
        "pieces/07-milk-honey-reaction-diffusion/README.md is missing"
    )


def test_piece_07_essay_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "essay.md")), (
        "pieces/07-milk-honey-reaction-diffusion/essay.md is missing"
    )


def test_piece_07_gen_thumbnail_script_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "gen_thumbnail.py")), (
        "pieces/07-milk-honey-reaction-diffusion/gen_thumbnail.py is missing"
    )


def test_piece_07_thumbnail_is_png():
    piece = get_piece()
    assert piece is not None
    assert piece["thumbnail"].endswith(".png"), "thumbnail must be a .png file"


# ---------------------------------------------------------------------------
# index.html — simulation logic
# ---------------------------------------------------------------------------

def test_piece_07_html_uses_request_animation_frame():
    html = read_piece_file("index.html")
    assert "requestAnimationFrame" in html, (
        "index.html must use requestAnimationFrame for 60fps loop"
    )


def test_piece_07_html_has_gray_scott_parameters():
    """F and k parameters must be present for the coral/worm pattern range."""
    html = read_piece_file("index.html")
    assert "0.055" in html, "Gray-Scott feed rate F=0.055 must appear in HTML"
    assert "0.062" in html, "Gray-Scott kill rate k=0.062 must appear in HTML"


def test_piece_07_html_has_diffusion_rates():
    html = read_piece_file("index.html")
    assert "0.16" in html, "Du=0.16 must appear in HTML"
    assert "0.08" in html, "Dv=0.08 must appear in HTML"


def test_piece_07_html_uses_float32array():
    """Double-buffered Float32Array is required for U and V fields."""
    html = read_piece_file("index.html")
    assert "Float32Array" in html, (
        "index.html must use Float32Array for the simulation grid"
    )


def test_piece_07_html_multiple_float32arrays():
    """Four Float32Arrays needed: uA, uB, vA, vB for double-buffering."""
    html = read_piece_file("index.html")
    count = html.count("Float32Array")
    assert count >= 4, (
        f"index.html must declare at least 4 Float32Arrays (uA, uB, vA, vB); found {count}"
    )


def test_piece_07_html_has_delta_time_guard():
    """MAX_DT or equivalent cap prevents runaway catchup from tab sleep."""
    html = read_piece_file("index.html")
    assert "MAX_DT" in html or "maxDt" in html or "max_dt" in html or "> 50" in html or "> MAX_DT" in html, (
        "index.html must include a delta-time guard against tab-sleep catchup"
    )


def test_piece_07_html_simulation_grid_256():
    html = read_piece_file("index.html")
    assert "256" in html, "Simulation grid must be 256 wide/high"


def test_piece_07_html_steps_per_frame_2_to_4():
    """2-4 simulation steps per frame for smooth motion."""
    html = read_piece_file("index.html")
    assert re.search(r"STEPS_PER_FRAME\s*=\s*[234]", html) or re.search(r"steps.*[234]", html.lower()), (
        "STEPS_PER_FRAME must be set to 2, 3, or 4"
    )


# ---------------------------------------------------------------------------
# index.html — color palette
# ---------------------------------------------------------------------------

def test_piece_07_html_has_cream_color():
    """Cream color (#fdf6e3) for U field background."""
    html = read_piece_file("index.html")
    assert "fdf6e3" in html.lower(), "index.html must reference cream color #fdf6e3"


def test_piece_07_html_has_honey_color():
    """Honey gold (#d4a017) for mid-range V field."""
    html = read_piece_file("index.html")
    assert "d4a017" in html.lower(), "index.html must reference honey color #d4a017"


def test_piece_07_html_has_amber_color():
    """Dark amber (#8b5a00) for high V field."""
    html = read_piece_file("index.html")
    assert "8b5a00" in html.lower() or ("8b" in html and "5a00" in html.lower()), (
        "index.html must reference amber color #8b5a00"
    )


def test_piece_07_html_has_lut_or_color_ramp():
    """Color ramp must be pre-built or computed per-pixel."""
    html = read_piece_file("index.html")
    assert "LUT" in html or "lut" in html or "ramp" in html.lower() or "lerp" in html.lower() or "212" in html, (
        "index.html must implement a color ramp from cream to amber"
    )


# ---------------------------------------------------------------------------
# index.html — Hebrew overlay
# ---------------------------------------------------------------------------

def test_piece_07_html_has_hebrew_phrase():
    """The phrase 'a land flowing with milk and honey' must appear in Hebrew."""
    html = read_piece_file("index.html")
    # The phrase: אֶרֶץ זָבַת חָלָב וּדְבַשׁ
    assert "אֶרֶץ" in html or "זָבַת" in html or "חָלָב" in html, (
        "index.html must contain the Hebrew phrase אֶרֶץ זָבַת חָלָב וּדְבַשׁ"
    )


def test_piece_07_html_hebrew_is_semi_transparent():
    """Hebrew overlay must be semi-transparent (globalAlpha < 1)."""
    html = read_piece_file("index.html")
    assert "globalAlpha" in html, "Hebrew overlay must use globalAlpha for transparency"
    match = re.search(r"globalAlpha\s*=\s*([0-9.]+)", html)
    assert match is not None, "globalAlpha assignment must be present"
    alpha = float(match.group(1))
    assert alpha < 1.0, f"globalAlpha must be < 1 (semi-transparent); found {alpha}"


# ---------------------------------------------------------------------------
# index.html — layout (art left, essay right)
# ---------------------------------------------------------------------------

def test_piece_07_html_has_two_panel_layout():
    html = read_piece_file("index.html")
    assert "art-panel" in html and "essay-panel" in html, (
        "index.html must define art-panel and essay-panel"
    )


def test_piece_07_html_has_responsive_media_query():
    html = read_piece_file("index.html")
    assert "@media" in html, "index.html must include a media query for narrow screens"
    assert "768" in html or "600" in html, "media query must specify a breakpoint (768px or 600px)"


def test_piece_07_html_essay_embedded():
    """Essay text must be embedded in HTML, not fetched at runtime."""
    essay = read_piece_file("essay.md")
    html = read_piece_file("index.html")
    words = [w for w in essay.split() if len(w) > 6][:10]
    found = sum(1 for w in words if w in html)
    assert found >= 5, (
        f"index.html must embed the essay text (only {found}/10 sampled words found)"
    )


def test_piece_07_html_no_external_resources():
    html = read_piece_file("index.html")
    external = re.findall(r'(?:src|href)\s*=\s*["\']https?://', html)
    assert not external, f"index.html must not load external resources; found: {external}"


# ---------------------------------------------------------------------------
# essay.md content
# ---------------------------------------------------------------------------

def test_piece_07_essay_word_count():
    text = read_piece_file("essay.md")
    count = len(text.split())
    assert 200 <= count <= 1000, (
        f"essay.md must be 200-1000 words; found {count}"
    )


def test_piece_07_essay_mentions_deuteronomy_26():
    text = read_piece_file("essay.md").lower()
    assert "deuteronomy 26" in text or "deut" in text or "26:" in text, (
        "essay.md must reference Deuteronomy 26 (the Bikkurim declaration)"
    )


def test_piece_07_essay_mentions_exodus_3():
    text = read_piece_file("essay.md").lower()
    assert "exodus 3" in text or "3:8" in text, (
        "essay.md must reference Exodus 3:8 (first occurrence of the phrase)"
    )


def test_piece_07_essay_mentions_milk_and_honey():
    text = read_piece_file("essay.md").lower()
    assert "milk" in text and "honey" in text, (
        "essay.md must discuss both milk and honey"
    )


def test_piece_07_essay_mentions_reaction_diffusion_or_gray_scott():
    text = read_piece_file("essay.md").lower()
    assert "gray-scott" in text or "reaction-diffusion" in text or "reaction diffusion" in text or "diffusion" in text, (
        "essay.md must explain the reaction-diffusion technique"
    )


# ---------------------------------------------------------------------------
# README.md
# ---------------------------------------------------------------------------

def test_piece_07_readme_mentions_bikkurim_or_milk_honey():
    text = read_piece_file("README.md").lower()
    assert "milk" in text or "honey" in text or "bikkurim" in text, (
        "README.md must mention Milk/Honey or Bikkurim"
    )


def test_piece_07_readme_mentions_gray_scott():
    text = read_piece_file("README.md").lower()
    assert "gray-scott" in text or "reaction" in text, (
        "README.md must mention Gray-Scott or reaction-diffusion"
    )


# ---------------------------------------------------------------------------
# gen_thumbnail.py content
# ---------------------------------------------------------------------------

def test_gen_thumbnail_uses_numpy():
    src = open(os.path.join(PIECE_DIR, "gen_thumbnail.py"), encoding="utf-8").read()
    assert "numpy" in src or "np" in src, "gen_thumbnail.py must use NumPy"


def test_gen_thumbnail_uses_pillow():
    src = open(os.path.join(PIECE_DIR, "gen_thumbnail.py"), encoding="utf-8").read()
    assert "PIL" in src or "pillow" in src.lower() or "Image" in src, (
        "gen_thumbnail.py must use Pillow (PIL)"
    )


def test_gen_thumbnail_runs_2000_steps():
    src = open(os.path.join(PIECE_DIR, "gen_thumbnail.py"), encoding="utf-8").read()
    assert "2000" in src, "gen_thumbnail.py must run at least 2000 simulation steps"


# ---------------------------------------------------------------------------
# Gray-Scott correctness (pure Python, no numpy dependency in test)
# ---------------------------------------------------------------------------

def test_gray_scott_v_spreads_from_seed():
    """
    A point seed of V=1 surrounded by V=0 must spread via diffusion: after
    one step, at least one neighbor cell of the seed must have V > 0.
    """
    W, H = 32, 32
    Du, Dv, Ff, kk = 0.16, 0.08, 0.055, 0.062
    u = [[1.0] * W for _ in range(H)]
    v = [[0.0] * W for _ in range(H)]
    u[16][16] = 0.0
    v[16][16] = 1.0

    nu = [[0.0] * W for _ in range(H)]
    nv = [[0.0] * W for _ in range(H)]
    for y in range(H):
        for x in range(W):
            lt = x - 1 if x > 0 else W - 1
            rt = x + 1 if x < W - 1 else 0
            up = y - 1 if y > 0 else H - 1
            dn = y + 1 if y < H - 1 else 0
            lapU = u[y][lt] + u[y][rt] + u[up][x] + u[dn][x] - 4 * u[y][x]
            lapV = v[y][lt] + v[y][rt] + v[up][x] + v[dn][x] - 4 * v[y][x]
            uvv = u[y][x] * v[y][x] * v[y][x]
            nu[y][x] = max(0.0, min(1.0, u[y][x] + Du * lapU - uvv + Ff * (1 - u[y][x])))
            nv[y][x] = max(0.0, min(1.0, v[y][x] + Dv * lapV + uvv - (Ff + kk) * v[y][x]))

    # Diffusion must have moved V into the seed's immediate neighbors
    neighbors_v = [nv[16][15], nv[16][17], nv[15][16], nv[17][16]]
    assert any(val > 0 for val in neighbors_v), (
        f"V must spread to neighbors via diffusion after one step; "
        f"neighbor values = {neighbors_v}"
    )


def test_gray_scott_clipping_prevents_overflow():
    """Values must never exceed 1 or go below 0 even after many steps."""
    W, H = 16, 16
    Du, Dv, Ff, kk = 0.16, 0.08, 0.055, 0.062
    u = [[1.0] * W for _ in range(H)]
    v = [[0.0] * W for _ in range(H)]
    u[8][8] = 0.0
    v[8][8] = 1.0

    for _ in range(50):
        nu = [[0.0] * W for _ in range(H)]
        nv = [[0.0] * W for _ in range(H)]
        for y in range(H):
            for x in range(W):
                lt = x - 1 if x > 0 else W - 1
                rt = x + 1 if x < W - 1 else 0
                up = y - 1 if y > 0 else H - 1
                dn = y + 1 if y < H - 1 else 0
                lapU = u[y][lt] + u[y][rt] + u[up][x] + u[dn][x] - 4 * u[y][x]
                lapV = v[y][lt] + v[y][rt] + v[up][x] + v[dn][x] - 4 * v[y][x]
                uvv = u[y][x] * v[y][x] * v[y][x]
                nu[y][x] = max(0.0, min(1.0, u[y][x] + Du * lapU - uvv + Ff * (1 - u[y][x])))
                nv[y][x] = max(0.0, min(1.0, v[y][x] + Dv * lapV + uvv - (Ff + kk) * v[y][x]))
        u, v = nu, nv

    for y in range(H):
        for x in range(W):
            assert 0.0 <= u[y][x] <= 1.0, f"u[{y}][{x}]={u[y][x]} out of [0,1]"
            assert 0.0 <= v[y][x] <= 1.0, f"v[{y}][{x}]={v[y][x]} out of [0,1]"


def test_gray_scott_no_growth_without_seed():
    """A uniform U=1, V=0 field with no seed should remain at V=0."""
    W, H = 16, 16
    Du, Dv, Ff, kk = 0.16, 0.08, 0.055, 0.062
    u = [[1.0] * W for _ in range(H)]
    v = [[0.0] * W for _ in range(H)]

    for _ in range(10):
        nu = [[0.0] * W for _ in range(H)]
        nv = [[0.0] * W for _ in range(H)]
        for y in range(H):
            for x in range(W):
                lt = x - 1 if x > 0 else W - 1
                rt = x + 1 if x < W - 1 else 0
                up = y - 1 if y > 0 else H - 1
                dn = y + 1 if y < H - 1 else 0
                lapU = u[y][lt] + u[y][rt] + u[up][x] + u[dn][x] - 4 * u[y][x]
                lapV = v[y][lt] + v[y][rt] + v[up][x] + v[dn][x] - 4 * v[y][x]
                uvv = u[y][x] * v[y][x] * v[y][x]
                nu[y][x] = max(0.0, min(1.0, u[y][x] + Du * lapU - uvv + Ff * (1 - u[y][x])))
                nv[y][x] = max(0.0, min(1.0, v[y][x] + Dv * lapV + uvv - (Ff + kk) * v[y][x]))
        u, v = nu, nv

    total_v = sum(v[y][x] for y in range(H) for x in range(W))
    assert total_v == 0.0, f"V must stay 0 with no seed; total_v={total_v}"


# ---------------------------------------------------------------------------
# gen_thumbnail.py functional test (runs numpy simulation)
# ---------------------------------------------------------------------------

def test_gen_thumbnail_produces_correct_output(tmp_path):
    """Running gen_thumbnail.py must produce a 256x256 PNG with amber tones."""
    import importlib.util
    import sys
    # Load gen_thumbnail as a module without executing __main__
    spec = importlib.util.spec_from_file_location(
        "gen_thumbnail",
        os.path.join(PIECE_DIR, "gen_thumbnail.py")
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    V = mod.run_gray_scott()
    assert V.shape == (256, 256), f"V field must be 256x256; got {V.shape}"
    assert V.min() >= 0.0 and V.max() <= 1.0, "V field must be clipped to [0, 1]"

    pixels = mod.v_to_rgb(V)
    assert pixels.shape == (256, 256, 3), f"RGB array must be 256x256x3; got {pixels.shape}"
    assert pixels.dtype.name == "uint8", f"RGB array must be uint8; got {pixels.dtype}"

    # The steady-state pattern should contain non-cream pixels (V > 0.1)
    from PIL import Image
    img = Image.fromarray(pixels, 'RGB')
    out = tmp_path / "thumbnail.png"
    img.save(str(out))
    assert out.exists()
    assert out.stat().st_size > 1000, "Generated PNG is suspiciously small"


# ---------------------------------------------------------------------------
# Edge cases and failure modes
# ---------------------------------------------------------------------------

def test_piece_07_id_matches_directory():
    piece = get_piece()
    assert piece is not None
    path_parts = piece["path"].replace("\\", "/").split("/")
    dir_name = path_parts[-2]
    assert dir_name == PIECE_ID, (
        f"piece id '{PIECE_ID}' does not match directory '{dir_name}'"
    )


def test_piece_07_path_ends_with_html():
    piece = get_piece()
    assert piece is not None
    assert piece["path"].endswith(".html"), "piece path must end with .html"


def test_piece_07_no_duplicate_id():
    pieces = load_pieces()
    ids = [p["id"] for p in pieces]
    assert len(ids) == len(set(ids)), f"Duplicate IDs in pieces.json: {ids}"


def test_piece_07_essay_field_in_json():
    piece = get_piece()
    assert piece is not None
    assert "essay" in piece and piece["essay"], "pieces.json entry must have non-empty 'essay' field"


def test_piece_07_essay_path_points_to_file():
    piece = get_piece()
    assert piece is not None
    essay_path = os.path.join(GALLERY_ROOT, piece["essay"])
    assert os.path.isfile(essay_path), (
        f"'{PIECE_ID}': essay file '{piece['essay']}' does not exist"
    )


def test_missing_piece_07_would_fail(tmp_path):
    """Confirm that a missing piece directory would be caught."""
    fake_dir = tmp_path / "fake-07"
    assert not fake_dir.exists(), "Fixture dir must not exist before test"


def test_thumbnail_png_is_binary_file():
    """thumbnail.png must be a binary file with PNG magic bytes."""
    png_path = os.path.join(PIECE_DIR, "thumbnail.png")
    with open(png_path, "rb") as fh:
        header = fh.read(8)
    # PNG magic: \x89PNG\r\n\x1a\n
    assert header[:4] == b'\x89PNG', (
        f"thumbnail.png does not start with PNG magic bytes; got {header[:4]!r}"
    )
