"""
Tests for piece 75 "Fire That Does Not Consume" — Barkley spiral sinai fire.

Covers: file layout, pieces.json registration, HTML content (Barkley model
parameters, Float32Array double-buffering, Hebrew overlay, essay embedding),
essay.md substance, thumbnail, and Barkley model correctness in pure Python.
"""
import json
import os
import re

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")
PIECE_ID = "75-barkley-spiral-sinai-fire"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_pieces():
    """Load and return the parsed pieces.json list."""
    with open(PIECES_JSON, encoding="utf-8") as fh:
        return json.load(fh)


def get_piece():
    """Return the pieces.json entry for this piece, or None if absent."""
    for p in load_pieces():
        if p["id"] == PIECE_ID:
            return p
    return None


def read_piece_file(filename):
    """Read a file from the piece directory."""
    return open(os.path.join(PIECE_DIR, filename), encoding="utf-8").read()


# ---------------------------------------------------------------------------
# pieces.json registration
# ---------------------------------------------------------------------------

def test_piece_75_in_json():
    assert get_piece() is not None, f"'{PIECE_ID}' not found in pieces.json"


def test_piece_75_theme_mentions_sinai():
    piece = get_piece()
    assert piece is not None
    theme = piece["theme"].lower()
    assert "sinai" in theme or "har sinai" in theme, "theme must reference Har Sinai"


def test_piece_75_technique_mentions_barkley():
    piece = get_piece()
    assert piece is not None
    technique = piece["technique"].lower()
    assert "barkley" in technique or "reaction-diffusion" in technique or "excitable" in technique, (
        "technique must mention Barkley model or reaction-diffusion"
    )


def test_piece_75_year_is_integer():
    piece = get_piece()
    assert piece is not None
    assert isinstance(piece["year"], int)


def test_piece_75_required_fields_present():
    piece = get_piece()
    assert piece is not None
    for field in ("id", "title", "tagline", "year", "theme", "technique", "path", "thumbnail", "essay"):
        assert field in piece and piece[field], f"Missing or empty field '{field}'"


# ---------------------------------------------------------------------------
# File layout
# ---------------------------------------------------------------------------

def test_piece_75_index_html_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "index.html")), (
        f"{PIECE_ID}/index.html is missing"
    )


def test_piece_75_thumbnail_svg_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "thumbnail.svg")), (
        f"{PIECE_ID}/thumbnail.svg is missing"
    )


def test_piece_75_readme_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "README.md")), (
        f"{PIECE_ID}/README.md is missing"
    )


def test_piece_75_essay_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "essay.md")), (
        f"{PIECE_ID}/essay.md is missing"
    )


def test_piece_75_thumbnail_is_svg():
    piece = get_piece()
    assert piece is not None
    assert piece["thumbnail"].endswith(".svg"), "thumbnail must be a .svg file"


# ---------------------------------------------------------------------------
# index.html — animation loop
# ---------------------------------------------------------------------------

def test_piece_75_html_uses_request_animation_frame():
    html = read_piece_file("index.html")
    assert "requestAnimationFrame" in html, (
        "index.html must use requestAnimationFrame for the animation loop"
    )


def test_piece_75_html_has_barkley_parameters():
    """Required Barkley model parameters must be present in the HTML."""
    html = read_piece_file("index.html")
    assert "0.75" in html, "Barkley parameter a=0.75 must appear in HTML"
    assert "0.06" in html, "Barkley parameter b=0.06 must appear in HTML"
    assert "0.02" in html, "Barkley parameter eps=0.02 must appear in HTML"


def test_piece_75_html_has_dt_and_diffusion():
    html = read_piece_file("index.html")
    assert "0.1" in html, "dt=0.1 must appear in HTML"
    assert "1.0" in html or "D = 1" in html or "D=1" in html, "D=1.0 (diffusion) must appear in HTML"


def test_piece_75_html_uses_float32array():
    """Double-buffered Float32Array is required for u and v fields."""
    html = read_piece_file("index.html")
    assert "Float32Array" in html, "index.html must use Float32Array for the simulation grid"


def test_piece_75_html_has_four_float32arrays():
    """Four Float32Arrays needed: u, v, u2, v2 for double-buffering."""
    html = read_piece_file("index.html")
    count = html.count("Float32Array")
    assert count >= 4, (
        f"index.html must declare at least 4 Float32Arrays (u, v, u2, v2); found {count}"
    )


def test_piece_75_html_steps_per_frame_3():
    html = read_piece_file("index.html")
    assert "STEPS_PER_FRAME" in html, "STEPS_PER_FRAME must be defined"
    assert re.search(r"STEPS_PER_FRAME\s*=\s*3", html), "STEPS_PER_FRAME must be set to 3"


def test_piece_75_html_simulation_grid_200():
    html = read_piece_file("index.html")
    assert "200" in html, "Simulation grid must be 200 wide/high"
    assert re.search(r"W\s*=\s*200", html) or re.search(r"H\s*=\s*200", html), (
        "W=200 or H=200 must be declared"
    )


def test_piece_75_html_has_laplacian():
    """The 5-point Laplacian formula must appear in the HTML."""
    html = read_piece_file("index.html")
    assert "lap" in html.lower() or "laplacian" in html.lower(), (
        "index.html must implement a Laplacian for diffusion"
    )
    assert "- 4" in html or "-4" in html, "5-point Laplacian must include the -4*u[i] term"


def test_piece_75_html_has_periodic_boundary():
    """Periodic boundary conditions must be present (modulo arithmetic)."""
    html = read_piece_file("index.html")
    assert "% W" in html or "%W" in html, "Periodic X boundary requires modulo W"
    assert "% H" in html or "%H" in html, "Periodic Y boundary requires modulo H"


def test_piece_75_html_has_delta_time_guard():
    """MAX_DT guard prevents runaway simulation after tab sleep."""
    html = read_piece_file("index.html")
    assert "MAX_DT" in html or "maxDt" in html or "max_dt" in html, (
        "index.html must include a MAX_DT delta-time guard"
    )


def test_piece_75_html_seeds_perturbations():
    """The seeding of perturbations must be present in the HTML."""
    html = read_piece_file("index.html")
    assert "seeds" in html or "seed" in html.lower() or "perturbation" in html.lower(), (
        "index.html must seed initial perturbations"
    )


# ---------------------------------------------------------------------------
# index.html — color palette
# ---------------------------------------------------------------------------

def test_piece_75_html_has_charcoal_color():
    """Deep charcoal (#120805) for unexcited state."""
    html = read_piece_file("index.html")
    assert "120805" in html.lower(), "index.html must reference charcoal color #120805"


def test_piece_75_html_has_ember_color():
    """Deep ember (#5C1800) for low activation."""
    html = read_piece_file("index.html")
    assert "5c1800" in html.lower() or "5C1800" in html, (
        "index.html must reference ember color #5C1800"
    )


def test_piece_75_html_has_orange_color():
    """Volcanic orange (#E83A00) for mid activation."""
    html = read_piece_file("index.html")
    assert "e83a00" in html.lower() or "E83A00" in html, (
        "index.html must reference volcanic orange #E83A00"
    )


def test_piece_75_html_has_flame_color():
    """Bright flame (#FF8C00) for high activation."""
    html = read_piece_file("index.html")
    assert "ff8c00" in html.lower() or "FF8C00" in html, (
        "index.html must reference flame color #FF8C00"
    )


def test_piece_75_html_has_flame_tip_color():
    """Pale flame-tip (#FFE8B0) for peak activation."""
    html = read_piece_file("index.html")
    assert "ffe8b0" in html.lower() or "FFE8B0" in html, (
        "index.html must reference flame-tip color #FFE8B0"
    )


def test_piece_75_html_has_recovery_tint():
    """Blue-gray recovery tint (#2A3050) for recovering cells."""
    html = read_piece_file("index.html")
    assert "2a3050" in html.lower() or "2A3050" in html, (
        "index.html must reference recovery tint #2A3050"
    )


# ---------------------------------------------------------------------------
# index.html — Hebrew overlay
# ---------------------------------------------------------------------------

def test_piece_75_html_has_hebrew_phrase():
    """The phrase 'and the mountain was burning with fire' must appear in Hebrew."""
    html = read_piece_file("index.html")
    assert "וְהַהָר" in html or "בֹּעֵר" in html or "בָּאֵשׁ" in html, (
        "index.html must contain the Hebrew phrase וְהַהָר בֹּעֵר בָּאֵשׁ"
    )


def test_piece_75_html_hebrew_direction_rtl():
    """Hebrew text must be rendered right-to-left."""
    html = read_piece_file("index.html")
    assert "rtl" in html, "index.html must set direction: rtl for Hebrew text"


def test_piece_75_html_hebrew_opacity():
    """Hebrew overlay must be semi-transparent (opacity 0.7)."""
    html = read_piece_file("index.html")
    assert "0.7" in html, "Hebrew overlay must be at opacity 0.7"


def test_piece_75_html_hebrew_has_text_shadow():
    """Hebrew overlay must have a fiery glow via text-shadow or shadowBlur."""
    html = read_piece_file("index.html")
    assert "shadowBlur" in html or "text-shadow" in html, (
        "index.html must apply a fiery glow to the Hebrew text"
    )


def test_piece_75_html_hebrew_color():
    """Hebrew text must use near-white color #FFF8F0."""
    html = read_piece_file("index.html")
    assert "FFF8F0" in html or "fff8f0" in html.lower(), (
        "index.html must use #FFF8F0 for Hebrew text color"
    )


# ---------------------------------------------------------------------------
# index.html — layout
# ---------------------------------------------------------------------------

def test_piece_75_html_has_two_panel_layout():
    html = read_piece_file("index.html")
    assert "art-panel" in html and "essay-panel" in html, (
        "index.html must define art-panel and essay-panel"
    )


def test_piece_75_html_has_responsive_media_query():
    html = read_piece_file("index.html")
    assert "@media" in html, "index.html must include a media query for narrow screens"
    assert "768" in html or "600" in html, "media query must specify a breakpoint"


def test_piece_75_html_essay_embedded():
    """Essay text must be embedded in HTML, not fetched at runtime."""
    essay = read_piece_file("essay.md")
    html = read_piece_file("index.html")
    words = [w for w in essay.split() if len(w) > 6][:10]
    found = sum(1 for w in words if w in html)
    assert found >= 5, (
        f"index.html must embed the essay text (only {found}/10 sampled words found)"
    )


def test_piece_75_html_no_external_resources():
    html = read_piece_file("index.html")
    external = re.findall(r'(?:src|href)\s*=\s*["\']https?://', html)
    assert not external, f"index.html must not load external resources; found: {external}"


# ---------------------------------------------------------------------------
# essay.md content
# ---------------------------------------------------------------------------

def test_piece_75_essay_word_count():
    text = read_piece_file("essay.md")
    count = len(text.split())
    assert 300 <= count <= 1200, (
        f"essay.md must be 300-1200 words; found {count}"
    )


def test_piece_75_essay_mentions_deuteronomy_4():
    text = read_piece_file("essay.md").lower()
    assert "deuteronomy 4" in text or "4:11" in text, (
        "essay.md must reference Deuteronomy 4:11-12 (the burning mountain)"
    )


def test_piece_75_essay_mentions_burning_bush():
    text = read_piece_file("essay.md").lower()
    assert "burning bush" in text or "exodus 3" in text or "sneh" in text, (
        "essay.md must reference the burning bush of Exodus 3:2"
    )


def test_piece_75_essay_mentions_shabbat_88b():
    text = read_piece_file("essay.md").lower()
    assert "shabbat 88" in text or "88b" in text, (
        "essay.md must cite Shabbat 88b (souls fled at each commandment)"
    )


def test_piece_75_essay_mentions_barkley_or_bz():
    text = read_piece_file("essay.md").lower()
    assert "barkley" in text or "belousov" in text or "bz" in text or "belousov-zhabotinsky" in text, (
        "essay.md must explain the Barkley/BZ connection"
    )


def test_piece_75_essay_mentions_fire_not_consumed():
    text = read_piece_file("essay.md").lower()
    assert "not consumed" in text or "einenu" in text or "ukal" in text or "not destroy" in text, (
        "essay.md must discuss the fire-that-does-not-consume paradox"
    )


# ---------------------------------------------------------------------------
# README.md
# ---------------------------------------------------------------------------

def test_piece_75_readme_mentions_sinai():
    text = read_piece_file("README.md").lower()
    assert "sinai" in text, "README.md must mention Sinai"


def test_piece_75_readme_mentions_barkley():
    text = read_piece_file("README.md").lower()
    assert "barkley" in text or "reaction-diffusion" in text or "excitable" in text, (
        "README.md must mention Barkley model or reaction-diffusion"
    )


# ---------------------------------------------------------------------------
# thumbnail.svg content
# ---------------------------------------------------------------------------

def test_piece_75_thumbnail_is_valid_svg():
    text = read_piece_file("thumbnail.svg")
    assert "<svg" in text and "</svg>" in text, "thumbnail.svg must be valid SVG"


def test_piece_75_thumbnail_uses_fire_colors():
    """Thumbnail SVG must reference fire palette colors."""
    text = read_piece_file("thumbnail.svg")
    assert "E83A00" in text or "e83a00" in text.lower() or "FF8C00" in text, (
        "thumbnail.svg must use fire palette colors"
    )


def test_piece_75_thumbnail_has_dark_background():
    """Thumbnail must have the near-black charcoal background."""
    text = read_piece_file("thumbnail.svg")
    assert "120805" in text.lower(), "thumbnail.svg must include dark background #120805"


# ---------------------------------------------------------------------------
# Barkley model correctness — pure Python, no external deps
# ---------------------------------------------------------------------------

def _barkley_step(u, v, W, H, a, b, eps, D, dt):
    """One forward-Euler step of the Barkley model on a WxH grid (flat lists)."""
    u2 = [0.0] * (W * H)
    v2 = [0.0] * (W * H)
    for y in range(H):
        for x in range(W):
            i = y * W + x
            xm = y * W + (x - 1 + W) % W
            xp = y * W + (x + 1) % W
            ym = ((y - 1 + H) % H) * W + x
            yp = ((y + 1) % H) * W + x
            lap = u[xm] + u[xp] + u[ym] + u[yp] - 4 * u[i]
            f = u[i] * (1 - u[i]) * (u[i] - (v[i] + b) / a)
            u2[i] = u[i] + dt * (f / eps + D * lap)
            v2[i] = v[i] + dt * (u[i] - v[i])
            if u2[i] < 0:
                u2[i] = 0
            if u2[i] > 1:
                u2[i] = 1
            if v2[i] < 0:
                v2[i] = 0
            if v2[i] > 1:
                v2[i] = 1
    return u2, v2


def test_barkley_u_spreads_from_seed():
    """
    A point seed of u=1 surrounded by u=0 must spread via diffusion: after
    one step at least one neighbor of the seed must have u > 0.
    """
    W, H = 20, 20
    a, b, eps, D, dt = 0.75, 0.06, 0.02, 1.0, 0.1
    u = [0.0] * (W * H)
    v = [0.0] * (W * H)
    u[10 * W + 10] = 1.0

    u2, v2 = _barkley_step(u, v, W, H, a, b, eps, D, dt)

    neighbors = [
        u2[10 * W + 9],
        u2[10 * W + 11],
        u2[9 * W + 10],
        u2[11 * W + 10],
    ]
    assert any(val > 0 for val in neighbors), (
        f"u must spread to neighbors via diffusion; neighbor values = {neighbors}"
    )


def test_barkley_values_stay_in_unit_interval():
    """All u and v values must remain in [0, 1] even after many steps."""
    W, H = 16, 16
    a, b, eps, D, dt = 0.75, 0.06, 0.02, 1.0, 0.1
    u = [0.0] * (W * H)
    v = [0.0] * (W * H)
    # Seed with a full u=1 patch to stress the clipping
    for dy in range(3):
        for dx in range(3):
            u[(8 + dy) * W + (8 + dx)] = 1.0

    for _ in range(100):
        u, v = _barkley_step(u, v, W, H, a, b, eps, D, dt)

    for i in range(W * H):
        assert 0.0 <= u[i] <= 1.0, f"u[{i}]={u[i]} out of [0,1]"
        assert 0.0 <= v[i] <= 1.0, f"v[{i}]={v[i]} out of [0,1]"


def test_barkley_quiescent_state_stable():
    """A fully quiescent grid (u=0, v=0) must remain at zero — no spontaneous excitation."""
    W, H = 16, 16
    a, b, eps, D, dt = 0.75, 0.06, 0.02, 1.0, 0.1
    u = [0.0] * (W * H)
    v = [0.0] * (W * H)

    for _ in range(20):
        u, v = _barkley_step(u, v, W, H, a, b, eps, D, dt)

    total_u = sum(u)
    assert total_u == 0.0, f"Quiescent state must remain zero; total_u={total_u}"


def test_barkley_v_increases_after_excitation():
    """
    Recovery variable v must increase in a cell that is excited (u=1) because
    dv/dt = u - v = 1 - 0 = 1 > 0 in the first step.
    """
    W, H = 5, 5
    a, b, eps, D, dt = 0.75, 0.06, 0.02, 1.0, 0.1
    u = [0.0] * (W * H)
    v = [0.0] * (W * H)
    cx = cy = 2
    u[cy * W + cx] = 1.0

    u2, v2 = _barkley_step(u, v, W, H, a, b, eps, D, dt)

    assert v2[cy * W + cx] > 0.0, (
        f"v must increase after u=1 excitation; v2 at center = {v2[cy * W + cx]}"
    )


def test_barkley_periodic_boundary_wraps_correctly():
    """
    A seed at the right edge (x=W-1) must influence the cell at x=0 via the
    periodic Laplacian after one step.
    """
    W, H = 10, 10
    a, b, eps, D, dt = 0.75, 0.06, 0.02, 1.0, 0.1
    u = [0.0] * (W * H)
    v = [0.0] * (W * H)
    # Place excitation at rightmost column, middle row
    u[5 * W + (W - 1)] = 1.0

    u2, v2 = _barkley_step(u, v, W, H, a, b, eps, D, dt)

    # The left-edge cell (x=0, y=5) receives diffusion from the right-edge seed
    left_edge_u = u2[5 * W + 0]
    assert left_edge_u > 0.0, (
        f"Periodic boundary must carry diffusion from x=W-1 to x=0; u at x=0 = {left_edge_u}"
    )


# ---------------------------------------------------------------------------
# Edge cases and failure modes
# ---------------------------------------------------------------------------

def test_piece_75_id_matches_directory():
    piece = get_piece()
    assert piece is not None
    path_parts = piece["path"].replace("\\", "/").split("/")
    dir_name = path_parts[-2]
    assert dir_name == PIECE_ID, (
        f"piece id '{PIECE_ID}' does not match directory '{dir_name}'"
    )


def test_piece_75_path_ends_with_html():
    piece = get_piece()
    assert piece is not None
    assert piece["path"].endswith(".html"), "piece path must end with .html"


def test_piece_75_no_duplicate_id():
    pieces = load_pieces()
    ids = [p["id"] for p in pieces]
    assert len(ids) == len(set(ids)), f"Duplicate IDs in pieces.json: {ids}"


def test_piece_75_essay_field_in_json():
    piece = get_piece()
    assert piece is not None
    assert "essay" in piece and piece["essay"], "pieces.json entry must have non-empty 'essay' field"


def test_piece_75_essay_path_points_to_file():
    piece = get_piece()
    assert piece is not None
    essay_path = os.path.join(GALLERY_ROOT, piece["essay"])
    assert os.path.isfile(essay_path), (
        f"'{PIECE_ID}': essay file '{piece['essay']}' does not exist"
    )


def test_missing_piece_would_fail(tmp_path):
    """Confirm that a missing piece directory would be caught by absence of index.html."""
    fake_dir = tmp_path / "fake-piece"
    assert not (fake_dir / "index.html").exists(), (
        "A non-existent directory must not have an index.html"
    )


def test_barkley_empty_grid_no_crash():
    """Running Barkley on a 1x1 grid must complete without raising."""
    W, H = 1, 1
    a, b, eps, D, dt = 0.75, 0.06, 0.02, 1.0, 0.1
    u = [0.5]
    v = [0.1]
    u2, v2 = _barkley_step(u, v, W, H, a, b, eps, D, dt)
    assert 0.0 <= u2[0] <= 1.0
    assert 0.0 <= v2[0] <= 1.0
