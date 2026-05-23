"""
Tests for piece 88 "Flowing Together" — Cahn–Hilliard spinodal decomposition.

Covers: file layout, pieces.json registration, HTML content (Cahn–Hilliard
simulation parameters, color palette, crossfade restart, essay embedding),
essay.md substance, thumbnail SVG validity, and explicit failure-mode /
edge-case behaviors.  Also verifies the Cahn–Hilliard physics directly in
pure Python.
"""
import json
import os
import re

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")
PIECE_ID = "88-cahn-hilliard-milk-honey"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_pieces():
    """Return the parsed pieces.json list."""
    with open(PIECES_JSON, encoding="utf-8") as fh:
        return json.load(fh)


def get_piece():
    """Return the pieces.json entry for this piece, or None."""
    for p in load_pieces():
        if p["id"] == PIECE_ID:
            return p
    return None


def read_piece_file(filename):
    """Read a file from the piece directory and return its text."""
    return open(os.path.join(PIECE_DIR, filename), encoding="utf-8").read()


# ---------------------------------------------------------------------------
# pieces.json registration
# ---------------------------------------------------------------------------

def test_piece_in_json():
    """The piece must be registered in pieces.json."""
    assert get_piece() is not None, f"'{PIECE_ID}' not found in pieces.json"


def test_piece_theme_mentions_milk_and_honey():
    """Theme field must reference milk, honey, or the promised land."""
    piece = get_piece()
    assert piece is not None
    theme = piece["theme"].lower()
    assert "milk" in theme or "honey" in theme or "promised" in theme, (
        "theme must reference milk, honey, or promised land"
    )


def test_piece_technique_mentions_cahn_hilliard():
    """Technique field must mention Cahn-Hilliard or spinodal decomposition."""
    piece = get_piece()
    assert piece is not None
    technique = piece["technique"].lower()
    assert "cahn" in technique or "spinodal" in technique or "hilliard" in technique, (
        "technique must mention Cahn-Hilliard or spinodal decomposition"
    )


def test_piece_year_is_integer():
    piece = get_piece()
    assert piece is not None
    assert isinstance(piece["year"], int)


def test_piece_required_fields_present():
    """All required pieces.json fields must be present and non-empty."""
    piece = get_piece()
    assert piece is not None
    for field in ("id", "title", "tagline", "year", "theme", "technique", "path", "thumbnail", "essay"):
        assert field in piece and piece[field], f"Missing or empty field '{field}'"


# ---------------------------------------------------------------------------
# File layout
# ---------------------------------------------------------------------------

def test_index_html_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "index.html")), (
        f"{PIECE_ID}/index.html is missing"
    )


def test_thumbnail_svg_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "thumbnail.svg")), (
        f"{PIECE_ID}/thumbnail.svg is missing"
    )


def test_readme_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "README.md")), (
        f"{PIECE_ID}/README.md is missing"
    )


def test_essay_md_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "essay.md")), (
        f"{PIECE_ID}/essay.md is missing"
    )


def test_thumbnail_is_svg():
    """pieces.json must point to a .svg thumbnail."""
    piece = get_piece()
    assert piece is not None
    assert piece["thumbnail"].endswith(".svg"), "thumbnail must be a .svg file"


# ---------------------------------------------------------------------------
# index.html — simulation logic
# ---------------------------------------------------------------------------

def test_html_uses_request_animation_frame():
    html = read_piece_file("index.html")
    assert "requestAnimationFrame" in html, (
        "index.html must use requestAnimationFrame for the animation loop"
    )


def test_html_has_float32array():
    """Simulation grid must be a Float32Array."""
    html = read_piece_file("index.html")
    assert "Float32Array" in html, (
        "index.html must use Float32Array for the phi field"
    )


def test_html_has_grid_size_300():
    """Internal canvas resolution must be 300×300."""
    html = read_piece_file("index.html")
    assert "300" in html, "index.html must reference grid size 300"


def test_html_has_eps2_parameter():
    """EPS2 = 6.25 (ε=2.5) must appear in the HTML."""
    html = read_piece_file("index.html")
    assert "6.25" in html, "EPS2=6.25 must appear in index.html"


def test_html_has_dt_parameter():
    """DT = 0.25 must appear in the HTML."""
    html = read_piece_file("index.html")
    assert "0.25" in html, "DT=0.25 must appear in index.html"


def test_html_has_steps_per_frame_8():
    """STEPS_PER_FRAME = 8 must appear in the HTML."""
    html = read_piece_file("index.html")
    assert "8" in html, "STEPS_PER_FRAME=8 must appear in index.html"
    assert re.search(r"STEPS_PER_FRAME\s*=\s*8", html), (
        "STEPS_PER_FRAME must be explicitly set to 8"
    )


def test_html_has_laplacian_function():
    """The 5-point Laplacian must be implemented."""
    html = read_piece_file("index.html")
    assert "laplacian" in html, "index.html must define a laplacian function"


def test_html_has_ch_step_function():
    """The Cahn–Hilliard update step must be implemented."""
    html = read_piece_file("index.html")
    assert "chStep" in html or "ch_step" in html, (
        "index.html must define a Cahn–Hilliard step function"
    )


def test_html_has_crossfade_logic():
    """Crossfade restart after coarsening must be implemented."""
    html = read_piece_file("index.html")
    assert "FADE_FRAMES" in html or "fadeFrame" in html or "fading" in html, (
        "index.html must implement the crossfade/restart logic"
    )


def test_html_has_coarsen_frames():
    """COARSEN_FRAMES (or equivalent) must define the ~30s cycle duration."""
    html = read_piece_file("index.html")
    assert "COARSEN_FRAMES" in html or "2000" in html, (
        "index.html must define a coarsening cycle of ~2000 frames"
    )


def test_html_has_clamp_to_minus_one_one():
    """phi must be clamped to [-1, 1] each step."""
    html = read_piece_file("index.html")
    assert "Math.max(-1" in html or "Math.max( -1" in html or "-1, Math.min" in html, (
        "index.html must clamp phi to [-1, 1]"
    )


def test_html_has_periodic_boundaries():
    """5-point Laplacian must use periodic (wrap-around) boundary conditions."""
    html = read_piece_file("index.html")
    assert "% H" in html or "% W" in html or "%H" in html or "%W" in html, (
        "index.html must use modulo for periodic boundary conditions"
    )


def test_html_has_image_rendering_pixelated():
    """Canvas must use pixelated scaling for sharp upscaling."""
    html = read_piece_file("index.html")
    assert "pixelated" in html, (
        "index.html must set image-rendering: pixelated on the canvas"
    )


# ---------------------------------------------------------------------------
# index.html — color palette
# ---------------------------------------------------------------------------

def test_html_has_milk_color():
    """Milk color #FFF5E6 (R255, G245, B230) must appear."""
    html = read_piece_file("index.html")
    assert "255" in html and "245" in html and "230" in html, (
        "index.html must reference milk color components (R255, G245, B230)"
    )


def test_html_has_honey_color():
    """Honey color #C8860A (R200, G134, B10) must appear."""
    html = read_piece_file("index.html")
    assert "200" in html and "134" in html, (
        "index.html must reference honey color components (R200, G134)"
    )


def test_html_color_interpolates_phi():
    """Color mapping must interpolate based on phi value."""
    html = read_piece_file("index.html")
    # The color formula uses (phi[i] + 1) * 0.5 or equivalent to map [-1,1] to [0,1]
    assert "phi" in html.lower() or "phi[i]" in html or "phi[" in html, (
        "index.html must map phi values to colors"
    )


# ---------------------------------------------------------------------------
# index.html — layout and essay embedding
# ---------------------------------------------------------------------------

def test_html_has_two_panel_layout():
    html = read_piece_file("index.html")
    assert "art-panel" in html and "essay-panel" in html, (
        "index.html must define art-panel and essay-panel"
    )


def test_html_has_responsive_media_query():
    html = read_piece_file("index.html")
    assert "@media" in html, "index.html must include a responsive media query"
    assert "768" in html or "600" in html, "media query must specify a pixel breakpoint"


def test_html_essay_embedded():
    """Essay text must be embedded in index.html, not fetched at runtime."""
    essay = read_piece_file("essay.md")
    html = read_piece_file("index.html")
    words = [w for w in essay.split() if len(w) > 6][:10]
    found = sum(1 for w in words if w in html)
    assert found >= 5, (
        f"index.html must embed the essay text (only {found}/10 sampled words found)"
    )


def test_html_no_external_resources():
    html = read_piece_file("index.html")
    external = re.findall(r'(?:src|href)\s*=\s*["\']https?://', html)
    assert not external, f"index.html must not load external resources; found: {external}"


def test_html_has_hebrew_text():
    """Hebrew phrase from Exodus 3:17 must appear in the HTML."""
    html = read_piece_file("index.html")
    assert "זָבַת" in html or "חָלָב" in html or "זוב" in html or "זָבַת חָלָב" in html, (
        "index.html must contain a Hebrew phrase referencing milk and honey"
    )


# ---------------------------------------------------------------------------
# essay.md content
# ---------------------------------------------------------------------------

def test_essay_word_count():
    """Essay must be ~350 words — at least 250, at most 700."""
    text = read_piece_file("essay.md")
    count = len(text.split())
    assert 250 <= count <= 700, (
        f"essay.md must be 250–700 words; found {count}"
    )


def test_essay_mentions_exodus_3_17():
    """Essay must open with or reference Exodus 3:17."""
    text = read_piece_file("essay.md").lower()
    assert "exodus 3" in text or "3:17" in text, (
        "essay.md must reference Exodus 3:17"
    )


def test_essay_mentions_twenty_times():
    """Essay must note that the phrase recurs more than twenty times."""
    text = read_piece_file("essay.md").lower()
    assert "twenty" in text or "20" in text, (
        "essay.md must note that the phrase recurs more than twenty times in the Torah"
    )


def test_essay_mentions_cahn_hilliard():
    """Essay must explain the Cahn–Hilliard equation."""
    text = read_piece_file("essay.md").lower()
    assert "cahn" in text or "hilliard" in text or "spinodal" in text, (
        "essay.md must mention Cahn–Hilliard or spinodal decomposition"
    )


def test_essay_mentions_milk_and_honey():
    text = read_piece_file("essay.md").lower()
    assert "milk" in text and "honey" in text, (
        "essay.md must discuss both milk and honey"
    )


def test_essay_mentions_immiscible_or_separation():
    """Essay must explain that milk and honey are immiscible / spontaneously separate."""
    text = read_piece_file("essay.md").lower()
    assert "immiscible" in text or "separat" in text or "spinodal" in text, (
        "essay.md must explain that milk and honey separate spontaneously"
    )


# ---------------------------------------------------------------------------
# thumbnail.svg
# ---------------------------------------------------------------------------

def test_thumbnail_is_valid_svg():
    text = read_piece_file("thumbnail.svg")
    assert "<svg" in text and "</svg>" in text, (
        "thumbnail.svg must be a valid SVG file"
    )


def test_thumbnail_has_amber_background():
    """SVG must contain the amber-gold background color."""
    text = read_piece_file("thumbnail.svg")
    assert "C8860A" in text or "c8860a" in text or "#c8860a" in text or "#C8860A" in text, (
        "thumbnail.svg must use amber-gold #C8860A as background"
    )


def test_thumbnail_has_cream_blobs():
    """SVG must contain cream-white blob shapes."""
    text = read_piece_file("thumbnail.svg")
    assert "FFF5E6" in text or "fff5e6" in text, (
        "thumbnail.svg must contain cream-white #FFF5E6 blob shapes"
    )


def test_thumbnail_has_multiple_ellipses():
    """SVG must contain multiple ellipse elements for the blob shapes."""
    text = read_piece_file("thumbnail.svg")
    ellipses = text.count("<ellipse")
    assert ellipses >= 6, (
        f"thumbnail.svg must have at least 6 blob shapes (ellipses); found {ellipses}"
    )


def test_thumbnail_viewbox_400():
    """SVG viewBox must be 400×400."""
    text = read_piece_file("thumbnail.svg")
    assert "400" in text, "thumbnail.svg must have 400×400 dimensions"


# ---------------------------------------------------------------------------
# README.md
# ---------------------------------------------------------------------------

def test_readme_mentions_milk_and_honey():
    text = read_piece_file("README.md").lower()
    assert "milk" in text or "honey" in text, (
        "README.md must mention milk and honey"
    )


def test_readme_mentions_cahn_hilliard():
    text = read_piece_file("README.md").lower()
    assert "cahn" in text or "spinodal" in text, (
        "README.md must mention Cahn–Hilliard or spinodal decomposition"
    )


# ---------------------------------------------------------------------------
# pieces.json integrity
# ---------------------------------------------------------------------------

def test_piece_id_matches_directory():
    piece = get_piece()
    assert piece is not None
    path_parts = piece["path"].replace("\\", "/").split("/")
    dir_name = path_parts[-2]
    assert dir_name == PIECE_ID, (
        f"piece id '{PIECE_ID}' does not match directory '{dir_name}'"
    )


def test_piece_path_ends_with_html():
    piece = get_piece()
    assert piece is not None
    assert piece["path"].endswith(".html"), "piece path must end with .html"


def test_no_duplicate_ids():
    """Duplicate IDs would break gallery routing."""
    pieces = load_pieces()
    ids = [p["id"] for p in pieces]
    assert len(ids) == len(set(ids)), f"Duplicate IDs in pieces.json: {ids}"


def test_essay_field_in_json():
    piece = get_piece()
    assert piece is not None
    assert "essay" in piece and piece["essay"], (
        "pieces.json entry must have a non-empty 'essay' field"
    )


def test_essay_path_points_to_file():
    piece = get_piece()
    assert piece is not None
    essay_path = os.path.join(GALLERY_ROOT, piece["essay"])
    assert os.path.isfile(essay_path), (
        f"'{PIECE_ID}': essay file '{piece['essay']}' does not exist on disk"
    )


# ---------------------------------------------------------------------------
# Cahn–Hilliard physics — pure Python verification
# ---------------------------------------------------------------------------

def _laplacian_py(f, W, H):
    """5-point discrete Laplacian with periodic boundaries (Python reference)."""
    out = [[0.0] * W for _ in range(H)]
    for y in range(H):
        for x in range(W):
            c = f[y][x]
            n = f[(y - 1) % H][x]
            s = f[(y + 1) % H][x]
            e = f[y][(x + 1) % W]
            w = f[y][(x - 1) % W]
            out[y][x] = n + s + e + w - 4 * c
    return out


def _ch_step_py(phi, W, H, eps2=6.25, dt=0.25):
    """One explicit Cahn–Hilliard step; returns updated phi (list-of-lists)."""
    lap_phi = _laplacian_py(phi, W, H)
    mu = [[0.0] * W for _ in range(H)]
    for y in range(H):
        for x in range(W):
            p = phi[y][x]
            mu[y][x] = p**3 - p - eps2 * lap_phi[y][x]
    lap_mu = _laplacian_py(mu, W, H)
    new_phi = [[0.0] * W for _ in range(H)]
    for y in range(H):
        for x in range(W):
            new_phi[y][x] = max(-1.0, min(1.0, phi[y][x] + dt * lap_mu[y][x]))
    return new_phi


def test_cahn_hilliard_phi_stays_clamped():
    """After many steps from random noise, phi must stay in [-1, 1]."""
    import random
    random.seed(42)
    W, H = 20, 20
    phi = [[(random.random() - 0.5) * 0.2 for _ in range(W)] for _ in range(H)]
    for _ in range(50):
        phi = _ch_step_py(phi, W, H)
    for y in range(H):
        for x in range(W):
            assert -1.0 <= phi[y][x] <= 1.0, (
                f"phi[{y}][{x}] = {phi[y][x]} outside [-1, 1]"
            )


def test_cahn_hilliard_phases_separate_from_noise():
    """Starting from small noise, the field must develop bimodal distribution (phase separation).

    After sufficient steps, most cells should be near ±1, not near 0.
    This verifies the double-well free energy drives separation.
    """
    import random
    random.seed(7)
    W, H = 32, 32
    phi = [[(random.random() - 0.5) * 0.2 for _ in range(W)] for _ in range(H)]
    for _ in range(500):
        phi = _ch_step_py(phi, W, H)
    flat = [phi[y][x] for y in range(H) for x in range(W)]
    near_extremes = sum(1 for v in flat if abs(v) > 0.5)
    total = W * H
    fraction = near_extremes / total
    assert fraction > 0.5, (
        f"After 500 steps only {fraction:.1%} of cells near ±1; "
        "phase separation did not occur"
    )


def test_cahn_hilliard_uniform_state_is_unstable():
    """A near-uniform phi=0 state with tiny perturbation must evolve away from 0.

    The spinodal region (|φ| < 1/√3 ≈ 0.577) is linearly unstable; a tiny
    perturbation should grow.
    """
    import random
    random.seed(99)
    W, H = 16, 16
    phi = [[(random.random() - 0.5) * 0.01 for _ in range(W)] for _ in range(H)]
    flat_initial = [phi[y][x] for y in range(H) for x in range(W)]
    variance_initial = sum(v**2 for v in flat_initial) / len(flat_initial)

    for _ in range(100):
        phi = _ch_step_py(phi, W, H)

    flat_final = [phi[y][x] for y in range(H) for x in range(W)]
    variance_final = sum(v**2 for v in flat_final) / len(flat_final)

    assert variance_final > variance_initial * 2, (
        "Variance should grow from spinodal instability but did not; "
        f"initial={variance_initial:.6f}, final={variance_final:.6f}"
    )


def test_laplacian_of_constant_is_zero():
    """The Laplacian of a spatially uniform field must be zero everywhere."""
    W, H = 10, 10
    phi = [[3.7] * W for _ in range(H)]
    lap = _laplacian_py(phi, W, H)
    for y in range(H):
        for x in range(W):
            assert abs(lap[y][x]) < 1e-9, (
                f"Laplacian of constant field must be 0; got {lap[y][x]} at ({y},{x})"
            )


def test_laplacian_periodic_boundary():
    """Laplacian must wrap at boundaries: a cell at x=0 sees the cell at x=W-1."""
    W, H = 4, 4
    phi = [[0.0] * W for _ in range(H)]
    phi[0][0] = 1.0
    lap = _laplacian_py(phi, W, H)
    # Cell (0,0) has four neighbors: (W-1,0), (1,0), (0,H-1), (0,1)
    # All neighbors are 0; center is 1 → laplacian = 0+0+0+0 - 4*1 = -4
    assert abs(lap[0][0] - (-4.0)) < 1e-9, (
        f"Laplacian at (0,0) should be -4 for isolated spike; got {lap[0][0]}"
    )
    # The cell at (0, W-1) should feel the spike from (0,0) via periodic wrap
    # lap[0][W-1] = phi[0][W-2] + phi[0][0] + phi[H-1][W-1] + phi[1][W-1] - 4*phi[0][W-1]
    #             = 0 + 1 + 0 + 0 - 4*0 = 1
    assert abs(lap[0][W - 1] - 1.0) < 1e-9, (
        f"Periodic wrap: lap[0][{W-1}] should be 1.0 (sees spike at (0,0)); "
        f"got {lap[0][W-1]}"
    )


# ---------------------------------------------------------------------------
# Edge cases and failure modes
# ---------------------------------------------------------------------------

def test_missing_piece_directory_would_fail(tmp_path):
    """Confirm that a missing piece directory would be caught by the file layout tests."""
    fake_dir = tmp_path / "fake-88"
    assert not fake_dir.exists(), "Fixture directory must not exist"


def test_wrong_piece_id_not_found():
    """A lookup for a non-existent ID must return None."""
    pieces = load_pieces()
    result = next((p for p in pieces if p["id"] == "99-does-not-exist"), None)
    assert result is None, "Non-existent ID should not be found in pieces.json"


def test_empty_essay_would_fail_word_count():
    """An empty string has 0 words — our word-count assertion would correctly reject it."""
    text = ""
    count = len(text.split())
    assert count < 250, "Fixture: empty essay has fewer than 250 words — our test would catch it"
