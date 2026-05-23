"""
Tests for piece 03-kuramoto-kol-echad (Kuramoto coupled oscillator synchronization).

Covers acceptance criteria: directory layout, index.html canvas animation,
essay content, thumbnail validity, and pieces.json registration.
"""
import json
import os

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID = "03-kuramoto-kol-echad"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")


def load_piece():
    """Return the pieces.json entry for 03-kuramoto-kol-echad, or None."""
    with open(PIECES_JSON, encoding="utf-8") as fh:
        data = json.load(fh)
    for entry in data:
        if entry["id"] == PIECE_ID:
            return entry
    return None


def read_html():
    """Return the full text of index.html."""
    return open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()


def read_essay():
    """Return the full text of essay.md."""
    return open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()


# ---------------------------------------------------------------------------
# Directory and file layout
# ---------------------------------------------------------------------------

def test_piece_directory_exists():
    assert os.path.isdir(PIECE_DIR), f"Piece directory {PIECE_DIR} does not exist"


def test_index_html_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "index.html"))


def test_essay_md_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "essay.md"))


def test_readme_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "README.md"))


def test_thumbnail_svg_exists():
    thumb = os.path.join(PIECE_DIR, "thumbnail.svg")
    assert os.path.isfile(thumb)
    text = open(thumb, encoding="utf-8").read()
    assert "<svg" in text and "</svg>" in text, "thumbnail.svg is not valid SVG"


# ---------------------------------------------------------------------------
# pieces.json registration
# ---------------------------------------------------------------------------

def test_piece_registered_in_pieces_json():
    entry = load_piece()
    assert entry is not None, f"{PIECE_ID} not found in pieces.json"


def test_piece_required_fields_present():
    entry = load_piece()
    assert entry is not None
    for field in ("id", "title", "tagline", "year", "theme", "technique", "path", "thumbnail", "essay"):
        assert field in entry, f"Field '{field}' missing from pieces.json entry"
        assert entry[field], f"Field '{field}' is empty in pieces.json entry"


def test_piece_theme_mentions_matan_torah_or_sinai():
    entry = load_piece()
    theme = entry["theme"].lower()
    assert "matan torah" in theme or "sinai" in theme or "collective" in theme, (
        f"Theme should reference Matan Torah or Sinai, got: {entry['theme']!r}"
    )


def test_piece_technique_mentions_kuramoto():
    entry = load_piece()
    assert "kuramoto" in entry["technique"].lower(), (
        f"Technique must mention Kuramoto, got: {entry['technique']!r}"
    )


def test_piece_year_is_integer():
    entry = load_piece()
    assert isinstance(entry["year"], int)


def test_piece_path_matches_id():
    entry = load_piece()
    path_parts = entry["path"].replace("\\", "/").split("/")
    dir_name = path_parts[-2]
    assert dir_name == PIECE_ID, f"path dir '{dir_name}' does not match piece id '{PIECE_ID}'"


# ---------------------------------------------------------------------------
# index.html — simulation requirements
# ---------------------------------------------------------------------------

def test_index_html_uses_requestanimationframe():
    assert "requestAnimationFrame" in read_html()


def test_index_html_has_canvas_element():
    assert "<canvas" in read_html()


def test_index_html_declares_n_300():
    """N = 300 oscillators must be declared in the simulation."""
    html = read_html()
    assert "300" in html, "N = 300 must appear in index.html"


def test_index_html_has_kuramoto_step():
    """The Kuramoto phase update function must be present."""
    html = read_html()
    assert "kuramotoStep" in html or "kuramoto" in html.lower(), (
        "Kuramoto step function not found in index.html"
    )


def test_index_html_has_order_parameter_r():
    """The order parameter r (synchrony measure) must be computed and displayed."""
    html = read_html()
    assert "r =" in html or "r=" in html, "Order parameter r not displayed in index.html"


def test_index_html_has_lorentzian_distribution():
    """Lorentzian frequency sampling via Math.tan must be present."""
    html = read_html()
    assert "Math.tan" in html, "Lorentzian distribution (Math.tan) not found in index.html"


def test_index_html_clamps_omega_to_01_30():
    """Omega must be clamped to [0.1, 3.0] to prevent extreme outliers."""
    html = read_html()
    assert "0.1" in html and "3.0" in html, (
        "Omega clamp bounds [0.1, 3.0] not found in index.html"
    )


def test_index_html_coupling_constant_reaches_30():
    """K must reach 3.0 during the coupling ramp."""
    html = read_html()
    assert "3.0" in html, "Coupling constant K = 3.0 not found in index.html"


def test_index_html_has_cycle_ramp_times():
    """Coupling ramp: 15s up, 10s hold, 5s down — at least two of these values must appear."""
    html = read_html()
    found = sum(1 for v in ("15", "25", "30") if v in html)
    assert found >= 2, "Coupling ramp timing constants (15, 25, 30) not found in index.html"


def test_index_html_uses_hsl_color():
    """Oscillator color must use HSL encoding."""
    html = read_html()
    assert "hsl(" in html or "hsl(" in html, "HSL color encoding not found in index.html"


def test_index_html_has_link_distance_80():
    """Coupling lines drawn for oscillators within 80px."""
    html = read_html()
    assert "80" in html, "Link distance 80 not found in index.html"


def test_index_html_has_euler_dt():
    """Euler integration timestep DT = 0.016 must be present."""
    html = read_html()
    assert "0.016" in html, "Euler dt = 0.016 not found in index.html"


def test_index_html_displays_k_value():
    """K value must be displayed on the canvas HUD."""
    html = read_html()
    assert "K = " in html or 'fillText(`K' in html or "fillText" in html, (
        "K value display not found in index.html"
    )


def test_index_html_gold_blend_toward_synchrony():
    """Gold color (#D4A017) or gold-blend logic must appear when r is high."""
    html = read_html()
    assert "D4A017" in html.upper() or "43" in html, (
        "Gold color (#D4A017) not found in index.html"
    )


def test_index_html_uses_float32array():
    """Float32Array buffers must be used for oscillator state."""
    assert "Float32Array" in read_html()


def test_index_html_has_mean_field_computation():
    """Mean-field computation (sx/sy sum of cos/sin) must be present."""
    html = read_html()
    assert "Math.cos" in html and "Math.sin" in html, (
        "Mean-field cos/sin summation not found in index.html"
    )


def test_index_html_phase_wraps_modulo_2pi():
    """Phase must be wrapped modulo 2π after each step."""
    html = read_html()
    assert "2 * Math.PI" in html or "2*Math.PI" in html, (
        "Phase modulo 2*PI wrap not found in index.html"
    )


# ---------------------------------------------------------------------------
# essay.md content
# ---------------------------------------------------------------------------

def test_essay_at_least_350_words():
    text = read_essay()
    word_count = len(text.split())
    assert word_count >= 350, f"Essay has only {word_count} words (need ≥ 350)"


def test_essay_cites_exodus_24_3():
    text = read_essay()
    assert "24:3" in text or "Exodus 24" in text, "Essay must cite Exodus 24:3"


def test_essay_cites_shabbat_86b():
    text = read_essay()
    assert "Shabbat 86b" in text or "86b" in text, "Essay must cite Shabbat 86b"


def test_essay_mentions_kol_echad():
    text = read_essay()
    assert "kol echad" in text.lower() or "kol-echad" in text.lower(), (
        "Essay must mention 'kol echad' (one voice)"
    )


def test_essay_mentions_600000():
    text = read_essay()
    assert "600,000" in text or "600000" in text, (
        "Essay must reference the 600,000 souls at Sinai"
    )


def test_essay_mentions_kuramoto():
    text = read_essay()
    assert "kuramoto" in text.lower() or "Kuramoto" in text, (
        "Essay must explain the Kuramoto model"
    )


def test_essay_mentions_critical_coupling():
    text = read_essay()
    assert "K_c" in text or "critical" in text.lower() or "threshold" in text.lower(), (
        "Essay must mention the critical coupling threshold"
    )


def test_essay_mentions_order_parameter():
    text = read_essay()
    assert "order parameter" in text.lower() or "r =" in text or "r = 1" in text, (
        "Essay must mention the order parameter r"
    )


def test_essay_mentions_naaseh_vnishma():
    text = read_essay()
    assert "naaseh" in text.lower() or "na'aseh" in text.lower(), (
        "Essay must mention naaseh v'nishma"
    )


def test_essay_embedded_in_html():
    """Words from essay.md must appear in index.html (embedded inline, not fetched)."""
    essay = read_essay()
    html = read_html()
    words = [w for w in essay.split() if len(w) > 6][:15]
    found = sum(1 for w in words if w in html)
    assert found >= 8, (
        f"Only {found}/15 essay words found in index.html — essay must be embedded inline"
    )


# ---------------------------------------------------------------------------
# Edge cases and failure modes
# ---------------------------------------------------------------------------

def test_no_duplicate_piece_id():
    """Piece ID must be unique across pieces.json."""
    with open(PIECES_JSON, encoding="utf-8") as fh:
        data = json.load(fh)
    ids = [e["id"] for e in data]
    assert ids.count(PIECE_ID) == 1, f"Duplicate entry for {PIECE_ID} in pieces.json"


def test_piece_path_resolves_to_file():
    entry = load_piece()
    full_path = os.path.join(GALLERY_ROOT, entry["path"])
    assert os.path.isfile(full_path), f"path '{entry['path']}' does not resolve to a file"


def test_piece_thumbnail_resolves_to_file():
    entry = load_piece()
    full_path = os.path.join(GALLERY_ROOT, entry["thumbnail"])
    assert os.path.isfile(full_path), f"thumbnail '{entry['thumbnail']}' does not resolve to a file"


def test_piece_essay_path_resolves_to_file():
    entry = load_piece()
    full_path = os.path.join(GALLERY_ROOT, entry["essay"])
    assert os.path.isfile(full_path), f"essay '{entry['essay']}' does not resolve to a file"


def test_html_has_no_runtime_fetch_of_essay():
    """index.html must not fetch essay.md at runtime — essay must be embedded inline."""
    html = read_html()
    assert "essay.md" not in html, (
        "index.html must not reference essay.md — embed the essay text directly in HTML"
    )


def test_thumbnail_has_dark_background():
    """Thumbnail must use a dark background color."""
    thumb = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert "#0a0a14" in thumb or "0a0a14" in thumb.lower(), (
        "Thumbnail must have dark background #0a0a14"
    )


def test_thumbnail_has_gold_circles():
    """Thumbnail must contain gold (#D4A017) representing synchronized oscillators."""
    thumb = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert "D4A017" in thumb.upper(), (
        "Thumbnail must contain gold circles (#D4A017) for the synchronized state"
    )


def test_thumbnail_has_rainbow_hsl_colors():
    """Thumbnail must contain hsl() colors representing asynchronous oscillators."""
    thumb = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert "hsl(" in thumb, (
        "Thumbnail must contain hsl() colors for the asynchronous (rainbow) state"
    )


def test_thumbnail_has_gradient_boundary():
    """Thumbnail must have a gradient element suggesting the phase transition."""
    thumb = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert "linearGradient" in thumb or "radialGradient" in thumb, (
        "Thumbnail must contain a gradient for the phase-transition boundary"
    )
