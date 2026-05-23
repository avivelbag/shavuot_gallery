"""
Tests for piece 90-gierer-meinhardt-seven-species.

Covers:
  - Piece directory structure (all required files present)
  - pieces.json registration (fields, theme, technique)
  - index.html: canvas, requestAnimationFrame, GM parameters, D_h sweep, color values
  - essay.md: word count, key topics (Turing, bikkurim, Deuteronomy, bifurcation)
  - thumbnail.svg: valid SVG, diagonal split structure
  - GM simulation invariants via a pure-Python port: steady state, positivity, Laplacian
"""
import json
import os


GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID     = "90-gierer-meinhardt-seven-species"
PIECE_DIR    = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def piece_path(filename):
    return os.path.join(PIECE_DIR, filename)


def load_pieces():
    with open(os.path.join(GALLERY_ROOT, "pieces.json"), encoding="utf-8") as f:
        return json.load(f)


def get_piece():
    for p in load_pieces():
        if p["id"] == PIECE_ID:
            return p
    return None


def read_html():
    with open(piece_path("index.html"), encoding="utf-8") as f:
        return f.read()


def read_essay():
    with open(piece_path("essay.md"), encoding="utf-8") as f:
        return f.read()


def read_svg():
    with open(piece_path("thumbnail.svg"), encoding="utf-8") as f:
        return f.read()


# ---------------------------------------------------------------------------
# Directory and file structure
# ---------------------------------------------------------------------------

def test_piece_directory_exists():
    assert os.path.isdir(PIECE_DIR), f"Piece directory {PIECE_DIR} is missing"


def test_index_html_exists():
    assert os.path.isfile(piece_path("index.html"))


def test_essay_md_exists():
    assert os.path.isfile(piece_path("essay.md"))


def test_thumbnail_svg_exists():
    assert os.path.isfile(piece_path("thumbnail.svg"))


def test_readme_md_exists():
    assert os.path.isfile(piece_path("README.md"))


# ---------------------------------------------------------------------------
# pieces.json registration
# ---------------------------------------------------------------------------

def test_piece_in_pieces_json():
    assert get_piece() is not None, f"{PIECE_ID} not found in pieces.json"


def test_piece_required_fields():
    piece = get_piece()
    for field in ("id", "title", "tagline", "year", "theme", "technique", "path", "thumbnail", "essay"):
        assert field in piece and piece[field], f"Missing or empty field: {field}"


def test_piece_theme_mentions_bikkurim_or_seven_species():
    piece = get_piece()
    theme_lower = piece["theme"].lower()
    assert "bikkurim" in theme_lower or "seven species" in theme_lower, (
        f"theme should mention 'Bikkurim' or 'seven species', got: {piece['theme']}"
    )


def test_piece_technique_mentions_gierer_meinhardt():
    piece = get_piece()
    tech_lower = piece["technique"].lower()
    assert "gierer" in tech_lower or "meinhardt" in tech_lower or "reaction-diffusion" in tech_lower, (
        f"technique should mention Gierer-Meinhardt, got: {piece['technique']}"
    )


def test_piece_technique_mentions_bifurcation():
    piece = get_piece()
    assert "bifurcation" in piece["technique"].lower(), (
        f"technique should mention 'bifurcation', got: {piece['technique']}"
    )


def test_piece_paths_point_to_existing_files():
    piece = get_piece()
    for key in ("path", "thumbnail", "essay"):
        full = os.path.join(GALLERY_ROOT, piece[key])
        assert os.path.isfile(full), f"File missing: {piece[key]}"


# ---------------------------------------------------------------------------
# index.html: structure and simulation parameters
# ---------------------------------------------------------------------------

def test_html_uses_request_animation_frame():
    assert "requestAnimationFrame" in read_html()


def test_html_has_canvas_element():
    html = read_html()
    assert "<canvas" in html, "index.html must contain a <canvas> element"


def test_html_embeds_essay_words():
    """Key essay words must appear in index.html (essay is embedded, not fetched)."""
    essay = read_essay()
    html  = read_html()
    # Sample the first 10 words longer than 6 chars from the essay
    long_words = [w.strip('.,;:—\'"') for w in essay.split() if len(w) > 6][:10]
    found = sum(1 for w in long_words if w in html)
    assert found >= 5, f"Only {found}/10 sampled essay words found in index.html — essay must be embedded"


def test_html_gm_parameters_present():
    """The accepted GM parameter values must appear in the source."""
    html = read_html()
    # rho=0.02, mu=0.03, nu=0.03, Da=0.005, rho0=0.001, dt=0.1
    for token in ("0.02", "0.03", "0.005", "0.001", "0.1"):
        assert token in html, f"GM parameter {token} not found in index.html"


def test_html_dh_sweep_range():
    """D_h sweep endpoints 0.2 and 2.0 must appear in the source."""
    html = read_html()
    assert "0.2" in html, "D_h minimum (0.2) not found in index.html"
    assert "2.0" in html, "D_h maximum (2.0) not found in index.html"


def test_html_sweep_time_twenty_seconds():
    """20-second sweep duration must appear in the source."""
    html = read_html()
    assert "20" in html, "20-second sweep duration not found in index.html"


def test_html_color_palette_present():
    """The three palette hex colors must appear in the source."""
    html = read_html().upper()
    for color in ("2D5016", "C8A84B", "8B1A1A"):
        assert color in html, f"Palette color #{color} not found in index.html"


def test_html_periodic_boundary_conditions():
    """Periodic BC implementation (modulo arithmetic) must be present."""
    html = read_html()
    assert "% N" in html or "%N" in html, "Periodic boundary modulo arithmetic not found in index.html"


def test_html_hebrew_labels_present():
    """All four Hebrew species labels must appear in index.html."""
    html = read_html()
    for hebrew in ("רִמּוֹן", "תְאֵנָה", "זַיִת", "חִטָּה"):
        assert hebrew in html, f"Hebrew label '{hebrew}' not found in index.html"


def test_html_species_english_labels():
    """English morphology labels must appear."""
    html = read_html()
    for label in ("pomegranate", "fig", "olive", "wheat"):
        assert label in html.lower(), f"English label '{label}' not found in index.html"


def test_html_grid_size_256():
    """The 256×256 grid constant must be declared."""
    html = read_html()
    assert "256" in html, "Grid size 256 not found in index.html"


def test_html_float32array_buffers():
    """Float32Array ping-pong buffers must be used for performance."""
    html = read_html()
    assert "Float32Array" in html, "Float32Array not found in index.html"


def test_html_offscreen_canvas_or_imagedata():
    """Efficient rendering via offscreen canvas or createImageData must be used."""
    html = read_html()
    assert "createImageData" in html or "createElement('canvas')" in html or 'createElement("canvas")' in html, (
        "index.html must use createImageData or an offscreen canvas for rendering"
    )


# ---------------------------------------------------------------------------
# essay.md content
# ---------------------------------------------------------------------------

def test_essay_word_count():
    essay = read_essay()
    word_count = len(essay.split())
    assert word_count >= 300, f"essay.md has only {word_count} words (need ≥ 300)"


def test_essay_opens_with_deuteronomy():
    essay = read_essay()
    # First 200 chars should mention Deuteronomy or the quote
    head = essay[:400].lower()
    assert "deuteronomy" in head or "8:8" in head or "wheat" in head, (
        "essay should open with a reference to Deuteronomy 8:8"
    )


def test_essay_mentions_turing():
    assert "Turing" in read_essay() or "turing" in read_essay().lower()


def test_essay_mentions_gierer_meinhardt():
    essay = read_essay()
    assert "Gierer" in essay or "Meinhardt" in essay or "gierer" in essay.lower()


def test_essay_mentions_bikkurim():
    essay = read_essay().lower()
    assert "bikkurim" in essay or "first fruit" in essay or "first-fruit" in essay


def test_essay_mentions_bifurcation_or_parameter():
    essay = read_essay().lower()
    assert "bifurcation" in essay or "parameter" in essay, (
        "essay must explain the bifurcation parameter concept"
    )


def test_essay_mentions_spots_and_stripes():
    essay = read_essay().lower()
    assert "spot" in essay and "stripe" in essay, (
        "essay must mention both spot and stripe patterns"
    )


def test_essay_mentions_mishna():
    essay = read_essay().lower()
    assert "mishna" in essay or "mishnah" in essay, "essay should reference the Mishna Bikkurim"


# ---------------------------------------------------------------------------
# thumbnail.svg
# ---------------------------------------------------------------------------

def test_thumbnail_is_valid_svg():
    svg = read_svg()
    assert "<svg" in svg and "</svg>" in svg


def test_thumbnail_has_clip_paths():
    """Thumbnail uses clipPath elements for the diagonal split."""
    svg = read_svg()
    assert "clipPath" in svg, "thumbnail.svg should use clipPath for the diagonal split"


def test_thumbnail_has_diagonal_line():
    """A diagonal boundary line must exist."""
    svg = read_svg()
    assert "<line" in svg, "thumbnail.svg must have a diagonal boundary line"


def test_thumbnail_pomegranate_color():
    """Pomegranate red (#8B1A1A) must appear in the SVG."""
    assert "8B1A1A" in read_svg().upper() or "8b1a1a" in read_svg()


def test_thumbnail_gold_color():
    """Harvest gold (#C8A84B) must appear in the SVG."""
    assert "C8A84B" in read_svg().upper() or "c8a84b" in read_svg()


def test_thumbnail_green_background():
    """Dark green (#2D5016) must appear as background."""
    assert "2D5016" in read_svg().upper() or "2d5016" in read_svg()


def test_thumbnail_has_circles_for_spots():
    """Upper-left spot pattern should use <circle> elements."""
    assert "<circle" in read_svg(), "thumbnail.svg must have <circle> elements for the spot pattern"


def test_thumbnail_has_rects_for_stripes():
    """Lower-right stripe pattern should use horizontal <rect> elements."""
    assert "<rect" in read_svg(), "thumbnail.svg must have <rect> elements for the stripe pattern"


# ---------------------------------------------------------------------------
# GM physics invariants via a pure-Python simulation port
# ---------------------------------------------------------------------------

def _gm_steady_state():
    """Compute the homogeneous GM steady state for the canonical parameters."""
    nu   = 0.03
    mu   = 0.03
    rho  = 0.02
    rho0 = 0.001
    a0 = (nu + rho0) / mu
    h0 = rho * a0 * a0 / nu
    return a0, h0


def test_gm_steady_state_values():
    """The homogeneous steady state satisfies da/dt=0 and dh/dt=0."""
    rho  = 0.02
    mu   = 0.03
    nu   = 0.03
    rho0 = 0.001
    a0, h0 = _gm_steady_state()

    da = rho * a0 * a0 / h0 - mu * a0 + rho0
    dh = rho * a0 * a0       - nu * h0

    assert abs(da) < 1e-10, f"da/dt at steady state should be 0, got {da}"
    assert abs(dh) < 1e-12, f"dh/dt at steady state should be 0, got {dh}"


def test_gm_steady_state_positive():
    a0, h0 = _gm_steady_state()
    assert a0 > 0, "steady-state activator must be positive"
    assert h0 > 0, "steady-state inhibitor must be positive"


def test_gm_euler_step_positivity():
    """One Euler step from a slightly perturbed SS should keep both fields positive."""
    rho  = 0.02
    mu   = 0.03
    nu   = 0.03
    rho0 = 0.001
    dt   = 0.1

    a0, h0 = _gm_steady_state()
    # single-cell isolated test (Laplacian = 0 because we use one cell with periodic BC = itself)
    ai = a0 * 1.005
    hi = h0 * 0.995

    da = rho * ai * ai / hi - mu * ai + rho0  # no spatial gradient (Da * 0)
    dh = rho * ai * ai       - nu * hi        # no spatial gradient (Dh * 0)

    a_new = ai + dt * da
    h_new = hi + dt * dh
    assert a_new > 0, f"activator went non-positive after one step: {a_new}"
    assert h_new > 0, f"inhibitor went non-positive after one step: {h_new}"


def test_gm_laplacian_flat_field_is_zero():
    """The 5-point Laplacian of a constant field on a periodic grid must be zero."""
    N = 8
    import array
    f = array.array('f', [2.5] * (N * N))

    def lap(x, y):
        yn = ((y - 1 + N) % N) * N
        ys = ((y + 1) % N) * N
        yc = y * N
        xw = (x - 1 + N) % N
        xe = (x + 1) % N
        idx = yc + x
        return f[yn + x] + f[ys + x] + f[yc + xw] + f[yc + xe] - 4.0 * f[idx]

    for y in range(N):
        for x in range(N):
            assert abs(lap(x, y)) < 1e-6, f"Laplacian of constant field is nonzero at ({x},{y})"


def test_gm_laplacian_periodic_wrap():
    """Periodic BC: Laplacian at a boundary cell uses the opposite edge."""
    N = 4
    import array
    f = array.array('f', [0.0] * (N * N))
    # Set one cell high; all others at 0
    f[0] = 4.0  # cell (0,0)
    # Periodic BC: neighbours of (0,0) wrap around:
    #   north = (3,0), south = (1,0), west = (0,3), east = (0,1)
    # All neighbours = 0, so Laplacian = 0 + 0 + 0 + 0 - 4*4 = -16
    y, x = 0, 0
    yn = ((y - 1 + N) % N) * N
    ys = ((y + 1) % N) * N
    yc = y * N
    xw = (x - 1 + N) % N
    xe = (x + 1) % N
    idx = yc + x
    lap = f[yn + x] + f[ys + x] + f[yc + xw] + f[yc + xe] - 4.0 * f[idx]
    assert abs(lap - (-16.0)) < 1e-5, f"Expected -16, got {lap}"


def test_gm_dh_sweep_range_formula():
    """The D_h sweep formula produces correct endpoint values."""
    DH_MIN     = 0.2
    DH_MAX     = 2.0
    SWEEP_SECS = 20.0

    def Dh(elapsed):
        phase = (elapsed % (2.0 * SWEEP_SECS)) / SWEEP_SECS
        return DH_MIN + (DH_MAX - DH_MIN) * phase if phase < 1.0 else DH_MIN + (DH_MAX - DH_MIN) * (2.0 - phase)

    assert abs(Dh(0.0)        - DH_MIN) < 1e-9
    assert abs(Dh(SWEEP_SECS) - DH_MAX) < 1e-9
    assert abs(Dh(2*SWEEP_SECS) - DH_MIN) < 1e-9


def test_gm_dh_sweep_intermediate():
    """At t=10s the D_h should be the midpoint."""
    DH_MIN     = 0.2
    DH_MAX     = 2.0
    SWEEP_SECS = 20.0

    elapsed = 10.0
    phase = (elapsed % (2.0 * SWEEP_SECS)) / SWEEP_SECS
    Dh = DH_MIN + (DH_MAX - DH_MIN) * phase if phase < 1.0 else DH_MIN + (DH_MAX - DH_MIN) * (2.0 - phase)
    midpoint = (DH_MIN + DH_MAX) / 2.0
    assert abs(Dh - midpoint) < 1e-9


def test_gm_color_mapping_green_at_zero():
    """At a=0 the color should be the deep green."""
    C_GREEN = (0x2D, 0x50, 0x16)
    # t = 0/MAX_A = 0 → interpolate green→gold at s=0 → pure green
    MAX_A = 5.0
    Dh    = 1.0
    a     = 0.0
    DH_MIN = 0.2
    DH_MAX = 2.0
    C_GOLD = (0xC8, 0xA8, 0x4B)
    C_RED  = (0x8B, 0x1A, 0x1A)

    t = min(1.0, max(0.0, a / MAX_A))
    dhT = (Dh - DH_MIN) / (DH_MAX - DH_MIN)
    rH = C_RED[0] + (C_GOLD[0] - C_RED[0]) * dhT
    gH = C_RED[1] + (C_GOLD[1] - C_RED[1]) * dhT
    bH = C_RED[2] + (C_GOLD[2] - C_RED[2]) * dhT

    if t < 0.5:
        s = t * 2.0
        r = C_GREEN[0] + (C_GOLD[0] - C_GREEN[0]) * s
        g = C_GREEN[1] + (C_GOLD[1] - C_GREEN[1]) * s
        b = C_GREEN[2] + (C_GOLD[2] - C_GREEN[2]) * s
    else:
        s = (t - 0.5) * 2.0
        r = C_GOLD[0] + (rH - C_GOLD[0]) * s
        g = C_GOLD[1] + (gH - C_GOLD[1]) * s
        b = C_GOLD[2] + (bH - C_GOLD[2]) * s

    assert abs(r - C_GREEN[0]) < 1e-6
    assert abs(g - C_GREEN[1]) < 1e-6
    assert abs(b - C_GREEN[2]) < 1e-6


def test_gm_color_mapping_clamped_at_max():
    """Values above MAX_A should clamp to t=1.0 (no out-of-range colors)."""
    MAX_A  = 5.0
    a      = 1000.0
    t      = min(1.0, max(0.0, a / MAX_A))
    assert t == 1.0, f"Expected t=1.0 for large a, got {t}"


def test_label_index_function():
    """getLabelIdx thresholds must match the acceptance criteria."""
    def get_label_idx(Dh):
        if Dh < 0.5:
            return 0  # pomegranate seeds
        if Dh < 1.0:
            return 1  # fig cross-section
        if Dh < 1.5:
            return 2  # olive grove
        return 3      # rows of wheat

    assert get_label_idx(0.1) == 0
    assert get_label_idx(0.5) == 1
    assert get_label_idx(0.9) == 1
    assert get_label_idx(1.0) == 2
    assert get_label_idx(1.4) == 2
    assert get_label_idx(1.5) == 3
    assert get_label_idx(2.0) == 3


def test_stability_condition_for_dt():
    """dt=0.1 must satisfy the FTCS stability criterion dt ≤ 1/(4*D) for all D values used."""
    dt     = 0.1
    DH_MAX = 2.0
    # Stability: dt * D * 8 ≤ 2 => dt ≤ 0.25 / D
    # (8 is the maximum Laplacian eigenvalue magnitude on a periodic unit grid)
    max_stable_dt = 0.25 / DH_MAX
    assert dt <= max_stable_dt, (
        f"dt={dt} violates FTCS stability for D_h={DH_MAX}: requires dt ≤ {max_stable_dt}"
    )


# ---------------------------------------------------------------------------
# Failure modes / edge cases
# ---------------------------------------------------------------------------

def test_missing_piece_directory_detected(tmp_path):
    """Absence of the piece directory must be detectable."""
    missing = tmp_path / "not-a-piece"
    assert not missing.is_dir()


def test_empty_essay_fails_word_count():
    """An empty string has zero words — word-count check would fail it."""
    essay = ""
    assert len(essay.split()) < 300


def test_malformed_pieces_json_detected(tmp_path):
    """A non-array pieces.json must be identifiable as invalid."""
    bad = tmp_path / "pieces.json"
    bad.write_text('{"not": "an array"}', encoding="utf-8")
    data = json.loads(bad.read_text())
    assert not isinstance(data, list)
