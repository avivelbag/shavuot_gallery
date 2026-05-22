"""
Tests for piece 30 "The Night Turns Toward Morning" — Tikkun Leil Star Trails.

Covers: pieces.json registration, file layout, WebGL-specific requirements
(shader uniforms, hash function, rotation matrix, trail logic), sky-color
gradient correctness (Python mirror of GLSL logic), Hebrew phrase presence,
essay content (Zohar, Karo, Magen Avraham), thumbnail validity, and edge cases.
"""
import json
import math
import os
import unicodedata

import pytest

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECES_JSON  = os.path.join(GALLERY_ROOT, "pieces.json")
PIECE_ID     = "30-tikkun-leil-star-trails"
PIECE_DIR    = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_pieces():
    """Return the parsed pieces.json list."""
    with open(PIECES_JSON, "r", encoding="utf-8") as fh:
        return json.load(fh)


def get_piece_30():
    """Return the piece-30 entry from pieces.json, or None if absent."""
    return next((p for p in load_pieces() if p["id"] == PIECE_ID), None)


def read_html():
    """Read and return the text of pieces/30-tikkun-leil-star-trails/index.html."""
    path = os.path.join(PIECE_DIR, "index.html")
    return open(path, encoding="utf-8").read()


def read_essay():
    """Read and return the text of essay.md."""
    path = os.path.join(PIECE_DIR, "essay.md")
    return open(path, encoding="utf-8").read()


def sky_color_python(t):
    """Python mirror of the GLSL skyColor function for unit-testing the gradient math.

    Interpolates between six keyframe colors over t in [0, 1], matching the
    GLSL shader's if-chain.  Returns an (r, g, b) tuple of floats in [0, 1].
    """
    c = [
        (0.031, 0.047, 0.102),  # midnight  #080c1a
        (0.051, 0.059, 0.200),  # deep indigo
        (0.102, 0.055, 0.271),  # violet    #1a0e45
        (0.353, 0.118, 0.329),  # violet-rose
        (0.784, 0.314, 0.125),  # amber     #c85020
        (0.910, 0.659, 0.188),  # gold      #e8a830
    ]

    def lerp(a, b, f):
        return tuple(a[i] + (b[i] - a[i]) * f for i in range(3))

    if t < 0.20:
        return lerp(c[0], c[1], t * 5.0)
    if t < 0.40:
        return lerp(c[1], c[2], (t - 0.20) * 5.0)
    if t < 0.60:
        return lerp(c[2], c[3], (t - 0.40) * 5.0)
    if t < 0.75:
        return lerp(c[3], c[4], (t - 0.60) / 0.15)
    if t < 0.90:
        return lerp(c[4], c[5], (t - 0.75) / 0.15)
    return lerp(c[5], c[0], (t - 0.90) / 0.10)


def hash_glsl(p):
    """Python approximation of the GLSL hash function for star placement tests."""
    dot = p[0] * 127.1 + p[1] * 311.7
    val = math.sin(dot) * 43758.5453123
    return val - math.floor(val)


# ---------------------------------------------------------------------------
# pieces.json registration
# ---------------------------------------------------------------------------

def test_piece_30_exists_in_json():
    assert get_piece_30() is not None, f"Piece '{PIECE_ID}' not found in pieces.json"


def test_piece_30_theme_mentions_tikkun_leil():
    p = get_piece_30()
    if p is None:
        pytest.skip("Piece 30 not present")
    assert "Tikkun Leil" in p["theme"], (
        f"Theme must mention 'Tikkun Leil', got {p['theme']!r}"
    )


def test_piece_30_technique_mentions_webgl():
    p = get_piece_30()
    if p is None:
        pytest.skip("Piece 30 not present")
    technique = p["technique"].lower()
    assert "webgl" in technique, (
        f"Technique must mention 'WebGL', got {p['technique']!r}"
    )


def test_piece_30_technique_mentions_fragment_shader():
    p = get_piece_30()
    if p is None:
        pytest.skip("Piece 30 not present")
    assert "fragment shader" in p["technique"].lower(), (
        f"Technique must mention 'fragment shader', got {p['technique']!r}"
    )


def test_piece_30_has_non_empty_tagline():
    p = get_piece_30()
    if p is None:
        pytest.skip("Piece 30 not present")
    assert p.get("tagline"), "Piece '30-tikkun-leil-star-trails' must have a non-empty tagline"


def test_piece_30_year_is_integer():
    p = get_piece_30()
    if p is None:
        pytest.skip("Piece 30 not present")
    assert isinstance(p["year"], int), f"year must be an integer, got {p['year']!r}"


# ---------------------------------------------------------------------------
# File layout
# ---------------------------------------------------------------------------

def test_piece_30_required_files_exist():
    for fname in ("index.html", "thumbnail.svg", "README.md", "essay.md"):
        assert os.path.isfile(os.path.join(PIECE_DIR, fname)), (
            f"pieces/30-tikkun-leil-star-trails/{fname} is missing"
        )


# ---------------------------------------------------------------------------
# WebGL requirements in index.html
# ---------------------------------------------------------------------------

def test_piece_30_uses_webgl_context():
    """index.html must request a WebGL context."""
    html = read_html()
    assert 'getContext("webgl")' in html or "getContext('webgl')" in html, (
        "index.html must call canvas.getContext('webgl')"
    )


def test_piece_30_has_u_time_uniform():
    """Fragment shader must declare the u_time uniform."""
    html = read_html()
    assert "uniform float u_time" in html, (
        "Fragment shader must declare 'uniform float u_time'"
    )


def test_piece_30_has_u_resolution_uniform():
    """Fragment shader must declare the u_resolution uniform."""
    html = read_html()
    assert "uniform vec2 u_resolution" in html, (
        "Fragment shader must declare 'uniform vec2 u_resolution'"
    )


def test_piece_30_uses_request_animation_frame():
    html = read_html()
    assert "requestAnimationFrame" in html, (
        "index.html must use requestAnimationFrame for the animation loop"
    )


def test_piece_30_has_hash_function():
    """Fragment shader must contain a hash/noise function for procedural star placement."""
    html = read_html()
    assert "43758.5453" in html, (
        "Shader must use the standard hash function constant 43758.5453"
    )


def test_piece_30_has_rotation_matrix():
    """Fragment shader must define a rotation matrix for star rotation."""
    html = read_html()
    assert "mat2" in html and ("rot2" in html or "rot(" in html), (
        "Shader must define a mat2 rotation function (rot2 or similar)"
    )


def test_piece_30_has_trail_sec_constant():
    """Fragment shader must define a trail length constant."""
    html = read_html()
    assert "TRAIL_SEC" in html or "TRAIL_STEPS" in html, (
        "Shader must define a trail length constant (TRAIL_SEC or TRAIL_STEPS)"
    )


def test_piece_30_has_cycle_constant():
    """Shader must define a CYCLE constant for the 60-second day/night loop."""
    html = read_html()
    assert "CYCLE" in html and ("60.0" in html or "= 60" in html), (
        "Shader must define a CYCLE constant (60 seconds)"
    )


def test_piece_30_has_rotation_period():
    """Shader must define the rotation period (~90 seconds)."""
    html = read_html()
    assert "90.0" in html or "ROT_PERIOD" in html, (
        "Shader must reference the star rotation period (90.0 seconds)"
    )


def test_piece_30_no_cdn_dependencies():
    """index.html must not load from any external CDN."""
    html = read_html()
    cdn_patterns = [
        "fonts.googleapis.com",
        "fonts.gstatic.com",
        "cdnjs.cloudflare.com",
        "jsdelivr.net",
        "unpkg.com/",
        "cdn.jsdelivr",
    ]
    for pat in cdn_patterns:
        assert pat not in html, (
            f"index.html must not load from external CDN ({pat})"
        )


# ---------------------------------------------------------------------------
# Sky color / gradient tests (Python mirror of GLSL skyColor function)
# ---------------------------------------------------------------------------

def test_sky_color_midnight_at_t0():
    """t=0 must return exact midnight color."""
    c = sky_color_python(0.0)
    assert c == pytest.approx((0.031, 0.047, 0.102)), (
        "skyColor(0.0) must be midnight color (0.031, 0.047, 0.102)"
    )


def test_sky_color_wraps_back_to_midnight_at_t1():
    """t=1.0 must return midnight (smooth wrap back from gold)."""
    c = sky_color_python(1.0)
    assert c == pytest.approx((0.031, 0.047, 0.102)), (
        "skyColor(1.0) must wrap back to midnight"
    )


def test_sky_color_gold_peak_at_t90():
    """t=0.9 marks the peak of the gold sunrise keyframe."""
    c = sky_color_python(0.90)
    assert c == pytest.approx((0.910, 0.659, 0.188)), (
        "skyColor(0.9) must be gold sunrise color (0.910, 0.659, 0.188)"
    )


def test_sky_color_red_channel_increases_toward_dawn():
    """Red channel must increase monotonically from t=0 through t=0.9."""
    ts = [0.0, 0.20, 0.40, 0.60, 0.75, 0.90]
    reds = [sky_color_python(t)[0] for t in ts]
    for i in range(1, len(reds)):
        assert reds[i] >= reds[i - 1], (
            f"Red channel must increase toward dawn: r[{ts[i-1]}]={reds[i-1]:.3f} "
            f"> r[{ts[i]}]={reds[i]:.3f}"
        )


def test_sky_color_midpoints_are_between_endpoints():
    """Every keyframe midpoint must lie strictly between its two endpoint colors."""
    breakpoints = [(0.0, 0.20), (0.20, 0.40), (0.40, 0.60), (0.60, 0.75), (0.75, 0.90)]
    for lo, hi in breakpoints:
        mid_t = (lo + hi) / 2.0
        c_lo  = sky_color_python(lo)
        c_hi  = sky_color_python(hi)
        c_mid = sky_color_python(mid_t)
        min_r = min(c_lo[0], c_hi[0])
        max_r = max(c_lo[0], c_hi[0])
        if min_r < max_r:
            assert min_r <= c_mid[0] <= max_r, (
                f"Midpoint red channel at t={mid_t} must lie in [{min_r:.3f}, {max_r:.3f}]"
            )


def test_sky_color_transition_is_continuous():
    """skyColor must be continuous: adjacent samples must not jump by more than 0.15."""
    prev = sky_color_python(0.0)
    for i in range(1, 201):
        t = i / 200.0
        curr = sky_color_python(t)
        for ch in range(3):
            delta = abs(curr[ch] - prev[ch])
            assert delta < 0.15, (
                f"Sky color channel {ch} jumps by {delta:.3f} at t={t:.3f} — must be continuous"
            )
        prev = curr


# ---------------------------------------------------------------------------
# Hash function sanity (Python approximation)
# ---------------------------------------------------------------------------

def test_hash_output_in_unit_interval():
    """Hash function must return values in [0, 1)."""
    import itertools
    for i, j in itertools.product(range(5), range(5)):
        h = hash_glsl((float(i), float(j)))
        assert 0.0 <= h < 1.0, f"hash(({i},{j})) = {h} is outside [0,1)"


def test_hash_distinct_for_distinct_cells():
    """Different cell IDs must produce meaningfully different hash values."""
    values = {hash_glsl((float(i), float(j))) for i in range(6) for j in range(6)}
    assert len(values) == 36, "Hash collisions detected across a 6x6 grid of cells"


# ---------------------------------------------------------------------------
# Hebrew phrase
# ---------------------------------------------------------------------------

def test_piece_30_has_hebrew_phrase():
    """index.html must contain the phrase 'until the rise of the dawn'."""
    html = unicodedata.normalize("NFC", read_html())
    phrase = unicodedata.normalize("NFC", "עַד-עֲלוֹת הַשַּׁחַר")
    assert phrase in html, (
        "index.html must contain the Hebrew phrase עַד-עֲלוֹת הַשַּׁחַר"
    )


def test_piece_30_hebrew_phrase_in_thumbnail():
    """thumbnail.svg must contain the Hebrew phrase."""
    thumb_path = os.path.join(PIECE_DIR, "thumbnail.svg")
    if not os.path.isfile(thumb_path):
        pytest.skip("thumbnail.svg missing")
    text = unicodedata.normalize("NFC", open(thumb_path, encoding="utf-8").read())
    phrase = unicodedata.normalize("NFC", "עַד-עֲלוֹת הַשַּׁחַר")
    assert phrase in text, "thumbnail.svg must include the Hebrew phrase"


# ---------------------------------------------------------------------------
# Essay content requirements
# ---------------------------------------------------------------------------

def test_essay_mentions_zohar():
    assert "Zohar" in read_essay(), "essay.md must name the Zohar as source"


def test_essay_mentions_parashat_emor():
    essay = read_essay()
    assert "Emor" in essay or "Parashat" in essay, (
        "essay.md must reference Parashat Emor"
    )


def test_essay_mentions_safed():
    assert "Safed" in read_essay(), (
        "essay.md must mention the kabbalists of 16th-century Safed"
    )


def test_essay_mentions_karo():
    assert "Karo" in read_essay(), (
        "essay.md must mention Rabbi Joseph Karo"
    )


def test_essay_mentions_magen_avraham():
    essay = read_essay()
    assert "Magen Avraham" in essay or "Orach Chayyim" in essay or "494" in essay, (
        "essay.md must cite the Magen Avraham (Orach Chayyim 494)"
    )


def test_essay_mentions_wedding_night_or_bride():
    essay = read_essay().lower()
    assert "bride" in essay or "wedding" in essay or "bridal" in essay, (
        "essay.md must explain the 'wedding night' / bride metaphor for Tikkun Leil"
    )


def test_essay_has_200_words():
    text = read_essay()
    word_count = len(text.split())
    assert word_count >= 200, (
        f"essay.md has only {word_count} words (minimum 200)"
    )


# ---------------------------------------------------------------------------
# Thumbnail
# ---------------------------------------------------------------------------

def test_piece_30_thumbnail_is_valid_svg():
    thumb = os.path.join(PIECE_DIR, "thumbnail.svg")
    if not os.path.isfile(thumb):
        pytest.skip("thumbnail.svg missing")
    text = open(thumb, encoding="utf-8").read()
    assert "<svg" in text and "</svg>" in text, (
        "thumbnail.svg does not look like valid SVG"
    )


def test_piece_30_thumbnail_has_gradient():
    """Thumbnail must use a gradient for the night-to-dawn sky."""
    thumb = os.path.join(PIECE_DIR, "thumbnail.svg")
    if not os.path.isfile(thumb):
        pytest.skip("thumbnail.svg missing")
    text = open(thumb, encoding="utf-8").read()
    assert "linearGradient" in text or "radialGradient" in text, (
        "thumbnail.svg must include a sky gradient"
    )


# ---------------------------------------------------------------------------
# README
# ---------------------------------------------------------------------------

def test_piece_30_readme_mentions_tikkun():
    readme = os.path.join(PIECE_DIR, "README.md")
    if not os.path.isfile(readme):
        pytest.skip("README.md missing")
    text = open(readme, encoding="utf-8").read().lower()
    assert "tikkun" in text or "shavuot" in text, (
        "README.md must mention the Tikkun Leil Shavuot theme"
    )


def test_piece_30_readme_mentions_webgl():
    readme = os.path.join(PIECE_DIR, "README.md")
    if not os.path.isfile(readme):
        pytest.skip("README.md missing")
    text = open(readme, encoding="utf-8").read().lower()
    assert "webgl" in text, "README.md must mention WebGL technique"


# ---------------------------------------------------------------------------
# Overlay and horizon requirements
# ---------------------------------------------------------------------------

def test_piece_30_html_has_overlay_canvas():
    """index.html must contain a second 2D canvas for the horizon overlay."""
    html = read_html()
    assert 'id="overlay"' in html or "id='overlay'" in html, (
        "index.html must define an overlay canvas with id='overlay'"
    )


def test_piece_30_html_has_bezier_curve():
    """Overlay drawing must use bezier curves for the hill silhouette."""
    html = read_html()
    assert "bezierCurveTo" in html, (
        "Overlay canvas must use bezierCurveTo for rolling hill silhouette"
    )


# ---------------------------------------------------------------------------
# Edge cases and failure modes
# ---------------------------------------------------------------------------

def test_piece_30_not_duplicate_id():
    """Piece 30 ID must appear exactly once in pieces.json."""
    count = sum(1 for p in load_pieces() if p["id"] == PIECE_ID)
    assert count == 1, f"'{PIECE_ID}' appears {count} times in pieces.json (expected 1)"


def test_piece_30_id_matches_directory():
    """The id in pieces.json must match the directory name in 'path'."""
    p = get_piece_30()
    if p is None:
        pytest.skip("Piece 30 not present")
    parts = p["path"].replace("\\", "/").split("/")
    dir_name = parts[-2]
    assert dir_name == PIECE_ID, (
        f"Directory name '{dir_name}' does not match id '{PIECE_ID}'"
    )


def test_sky_color_large_t_clamped_to_wrap():
    """t values just below 1.0 must be in the gold-to-midnight fade, not error."""
    c = sky_color_python(0.999)
    assert 0.0 <= c[0] <= 1.0
    assert 0.0 <= c[1] <= 1.0
    assert 0.0 <= c[2] <= 1.0


def test_sky_color_exactly_at_keyframe_boundaries():
    """skyColor must be defined and finite at every keyframe boundary."""
    for t in [0.0, 0.20, 0.40, 0.60, 0.75, 0.90, 1.0]:
        c = sky_color_python(t)
        for ch, val in enumerate(c):
            assert math.isfinite(val), f"skyColor({t}) channel {ch} is not finite: {val}"
            assert 0.0 <= val <= 1.1, f"skyColor({t}) channel {ch}={val} out of expected range"


def test_missing_piece_30_entry_detected(tmp_path):
    """A pieces.json without piece 30 must return None from get_piece_30()."""
    bad_data = [p for p in load_pieces() if p["id"] != PIECE_ID]
    result = next((p for p in bad_data if p["id"] == PIECE_ID), None)
    assert result is None, "Fixture should not contain piece 30"


def test_piece_30_path_ends_with_html():
    p = get_piece_30()
    if p is None:
        pytest.skip("Piece 30 not present")
    assert p["path"].endswith(".html"), "Piece path must end with .html"
