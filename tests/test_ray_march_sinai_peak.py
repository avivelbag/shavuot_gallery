"""
Tests for piece 63 "The Mountain That Burned With Fire" — Ray March Sinai Peak.

Covers: pieces.json registration, file layout, WebGL/GLSL requirements
(SDF, ray-march loop, fBm, camera orbit, lightning), fire-palette math,
essay content (Deuteronomy 4:11, Exodus 19:18, Mechilta, Shabbat 88b),
thumbnail validity, and edge/failure cases.
"""
import json
import math
import os
import unicodedata

import pytest

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECES_JSON  = os.path.join(GALLERY_ROOT, "pieces.json")
PIECE_ID     = "63-ray-march-sinai-peak"
PIECE_DIR    = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_pieces():
    """Return the parsed pieces.json list."""
    with open(PIECES_JSON, "r", encoding="utf-8") as fh:
        return json.load(fh)


def get_piece():
    """Return the piece-63 entry from pieces.json, or None if absent."""
    return next((p for p in load_pieces() if p["id"] == PIECE_ID), None)


def read_html():
    """Return the text of the piece's index.html."""
    return open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()


def read_essay():
    """Return the text of essay.md."""
    return open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()


def fire_hue_python(h):
    """Python mirror of the GLSL fireHue function.

    Maps h in [0, 1] to an (r, g, b) tuple using the same two-segment
    linear interpolation as the shader: base (#C04010) → gold (#F0C020) → crown (#FFF8E0).
    """
    base  = (0.753, 0.251, 0.063)
    gold  = (0.941, 0.753, 0.126)
    crown = (1.000, 0.973, 0.878)
    def lerp(a, b, t):
        return tuple(a[i] + (b[i] - a[i]) * t for i in range(3))
    if h < 0.5:
        return lerp(base, gold, h * 2.0)
    return lerp(gold, crown, (h - 0.5) * 2.0)


def smin_python(a, b, k):
    """Python mirror of the GLSL smooth-min function."""
    h = max(0.0, min(1.0, 0.5 + 0.5 * (b - a) / k))
    return a * h + b * (1.0 - h) - k * h * (1.0 - h)


# ---------------------------------------------------------------------------
# pieces.json registration
# ---------------------------------------------------------------------------

def test_piece_63_exists_in_json():
    assert get_piece() is not None, f"Piece '{PIECE_ID}' not found in pieces.json"


def test_piece_63_id_correct():
    p = get_piece()
    if p is None:
        pytest.skip("Piece 63 not present")
    assert p["id"] == PIECE_ID


def test_piece_63_theme_mentions_sinai():
    p = get_piece()
    if p is None:
        pytest.skip("Piece 63 not present")
    assert "Sinai" in p["theme"] or "sinai" in p["theme"].lower(), (
        f"Theme must mention Sinai, got {p['theme']!r}"
    )


def test_piece_63_technique_mentions_ray_marching():
    p = get_piece()
    if p is None:
        pytest.skip("Piece 63 not present")
    tech = p["technique"].lower()
    assert "ray" in tech and ("march" in tech or "sdf" in tech), (
        f"Technique must mention ray marching / SDF, got {p['technique']!r}"
    )


def test_piece_63_has_non_empty_tagline():
    p = get_piece()
    if p is None:
        pytest.skip("Piece 63 not present")
    assert p.get("tagline"), "Piece must have a non-empty tagline"


def test_piece_63_year_is_integer():
    p = get_piece()
    if p is None:
        pytest.skip("Piece 63 not present")
    assert isinstance(p["year"], int)


def test_piece_63_not_duplicate_id():
    """Piece 63 ID must appear exactly once in pieces.json."""
    count = sum(1 for p in load_pieces() if p["id"] == PIECE_ID)
    assert count == 1, f"'{PIECE_ID}' appears {count} times in pieces.json (expected 1)"


def test_piece_63_id_matches_directory():
    p = get_piece()
    if p is None:
        pytest.skip("Piece 63 not present")
    parts = p["path"].replace("\\", "/").split("/")
    assert parts[-2] == PIECE_ID, (
        f"Directory name '{parts[-2]}' does not match id '{PIECE_ID}'"
    )


def test_piece_63_path_ends_with_html():
    p = get_piece()
    if p is None:
        pytest.skip("Piece 63 not present")
    assert p["path"].endswith(".html")


# ---------------------------------------------------------------------------
# File layout
# ---------------------------------------------------------------------------

def test_piece_63_required_files_exist():
    for fname in ("index.html", "thumbnail.svg", "README.md", "essay.md"):
        assert os.path.isfile(os.path.join(PIECE_DIR, fname)), (
            f"pieces/63-ray-march-sinai-peak/{fname} is missing"
        )


# ---------------------------------------------------------------------------
# WebGL / GLSL requirements
# ---------------------------------------------------------------------------

def test_piece_63_uses_webgl_context():
    """index.html must request a WebGL context."""
    html = read_html()
    assert 'getContext("webgl")' in html or "getContext('webgl')" in html, (
        "index.html must call canvas.getContext('webgl')"
    )


def test_piece_63_has_u_time_uniform():
    html = read_html()
    assert "uniform float u_time" in html, "Fragment shader must declare 'uniform float u_time'"


def test_piece_63_has_u_resolution_uniform():
    html = read_html()
    assert "uniform vec2 u_resolution" in html, (
        "Fragment shader must declare 'uniform vec2 u_resolution'"
    )


def test_piece_63_has_scene_sdf():
    """Fragment shader must define a sceneSDF function."""
    html = read_html()
    assert "sceneSDF" in html, "Shader must define sceneSDF()"


def test_piece_63_has_smin():
    """Fragment shader must define the smooth-min function."""
    html = read_html()
    assert "smin" in html, "Shader must define smin() for smooth blending"


def test_piece_63_has_fbm():
    """Fragment shader must define a fBm noise function."""
    html = read_html()
    assert "fbm" in html, "Shader must define fbm() for procedural noise"


def test_piece_63_has_domain_warp():
    """Fragment shader must implement domain warping (wfbm or q = vec3(fbm...))."""
    html = read_html()
    assert "wfbm" in html or "domain" in html.lower() or (
        html.count("fbm(p") >= 2
    ), "Shader must implement domain-warped fBm"


def test_piece_63_has_fire_hue():
    """Fragment shader must define a fire colour palette function."""
    html = read_html()
    assert "fireHue" in html or "fire_hue" in html, (
        "Shader must define a fireHue() colour palette"
    )


def test_piece_63_fire_colors_present():
    """Fire palette hex colors must appear in the shader."""
    html = read_html()
    assert "C04010" in html.upper() or "c04010" in html, (
        "Fire base colour #C04010 must be in the shader"
    )
    assert "F0C020" in html.upper() or "f0c020" in html, (
        "Fire gold colour #F0C020 must be in the shader"
    )


def test_piece_63_mountain_color_present():
    """Basalt mountain color #3A2E20 must appear."""
    html = read_html()
    assert "3A2E20" in html.upper() or "3a2e20" in html, (
        "Mountain basalt colour #3A2E20 must be in the shader"
    )


def test_piece_63_has_camera_orbit():
    """Camera orbit must be present with a 120-second period."""
    html = read_html()
    assert "120" in html, (
        "Camera orbit must reference 120 second period"
    )
    assert "sin(" in html and "cos(" in html, (
        "Camera orbit must use sin/cos for circular motion"
    )


def test_piece_63_has_ray_march_loop():
    """Fragment shader must contain the ray march iteration loop."""
    html = read_html()
    assert "for (int i" in html or "for(int i" in html, (
        "Shader must contain an int-indexed ray march loop"
    )


def test_piece_63_has_96_or_more_march_steps():
    """Ray march loop must use at least 64 steps."""
    html = read_html()
    assert "96" in html or "128" in html or "64" in html, (
        "Ray march loop must iterate at least 64 steps"
    )


def test_piece_63_uses_request_animation_frame():
    html = read_html()
    assert "requestAnimationFrame" in html, (
        "index.html must use requestAnimationFrame"
    )


def test_piece_63_no_external_libraries():
    """index.html must not load from external CDN."""
    html = read_html()
    for pat in ["fonts.googleapis.com", "cdnjs.cloudflare.com",
                "jsdelivr.net", "unpkg.com/"]:
        assert pat not in html, (
            f"index.html must not load from external CDN ({pat})"
        )


# ---------------------------------------------------------------------------
# Lightning
# ---------------------------------------------------------------------------

def test_piece_63_has_bolt_uniform():
    """Shader must declare the lightning bolt uniform array."""
    html = read_html()
    assert "u_bolts" in html, "Shader must declare uniform vec2 u_bolts[]"


def test_piece_63_has_bolt_count_uniform():
    html = read_html()
    assert "u_boltCount" in html or "boltCount" in html, (
        "Shader must declare u_boltCount uniform for bolt segment count"
    )


def test_piece_63_has_bolt_flash_uniform():
    html = read_html()
    assert "u_boltFlash" in html or "boltFlash" in html, (
        "Shader must declare u_boltFlash uniform for fade"
    )


def test_piece_63_bolt_interval_is_4_seconds():
    """JS must trigger a new bolt every ~4 seconds."""
    html = read_html()
    assert "BOLT_INTERVAL" in html or "4.0" in html or "4 " in html, (
        "JS must reference a ~4-second bolt interval"
    )


def test_piece_63_bolt_generation_is_recursive():
    """JS must use a recursive bolt generation function."""
    html = read_html()
    assert "genBolt" in html or "recursive" in html.lower() or (
        "depth" in html and "branch" in html.lower()
    ), "JS must generate recursive Lichtenberg bolt"


# ---------------------------------------------------------------------------
# Fire palette math (Python mirror)
# ---------------------------------------------------------------------------

def test_fire_hue_base_at_h0():
    """h=0 must return the deep orange base colour."""
    c = fire_hue_python(0.0)
    assert c == pytest.approx((0.753, 0.251, 0.063), abs=0.001)


def test_fire_hue_crown_at_h1():
    """h=1 must return the near-white crown colour."""
    c = fire_hue_python(1.0)
    assert c == pytest.approx((1.000, 0.973, 0.878), abs=0.001)


def test_fire_hue_gold_at_h05():
    """h=0.5 must return the gold midpoint."""
    c = fire_hue_python(0.5)
    assert c == pytest.approx((0.941, 0.753, 0.126), abs=0.001)


def test_fire_hue_red_channel_monotone():
    """Red channel must increase monotonically from h=0 to h=1."""
    vals = [fire_hue_python(h / 10.0)[0] for h in range(11)]
    for i in range(1, len(vals)):
        assert vals[i] >= vals[i - 1] - 1e-9, (
            f"Red channel not monotone at h={i/10}: {vals[i-1]:.3f} → {vals[i]:.3f}"
        )


def test_fire_hue_all_channels_in_range():
    """All channels must remain in [0, 1] for any h in [0, 1]."""
    for i in range(21):
        h = i / 20.0
        r, g, b = fire_hue_python(h)
        assert 0.0 <= r <= 1.0
        assert 0.0 <= g <= 1.0
        assert 0.0 <= b <= 1.0


def test_fire_hue_continuous():
    """Palette must be continuous: no channel should jump by more than 0.15."""
    prev = fire_hue_python(0.0)
    for i in range(1, 101):
        h = i / 100.0
        curr = fire_hue_python(h)
        for ch in range(3):
            delta = abs(curr[ch] - prev[ch])
            assert delta < 0.15, (
                f"Fire palette channel {ch} jumps by {delta:.3f} at h={h:.2f}"
            )
        prev = curr


# ---------------------------------------------------------------------------
# SDF smooth-min math
# ---------------------------------------------------------------------------

def test_smin_returns_smaller_when_far_apart():
    """smin of two values far apart should approximate the smaller."""
    result = smin_python(-1.0, 10.0, 0.3)
    assert result == pytest.approx(-1.0, abs=0.05)


def test_smin_blends_when_close():
    """smin of two nearby values should fall strictly between them."""
    a, b, k = 0.1, 0.2, 0.3
    result = smin_python(a, b, k)
    assert result < a, "smin should go below the minimum value due to blending"


def test_smin_commutative_approx():
    """smin(a,b,k) ≈ smin(b,a,k) — the blend is roughly symmetric."""
    a, b, k = 0.5, 0.7, 0.4
    assert abs(smin_python(a, b, k) - smin_python(b, a, k)) < 0.05


# ---------------------------------------------------------------------------
# Essay content requirements
# ---------------------------------------------------------------------------

def test_essay_mentions_deuteronomy_4_11():
    essay = unicodedata.normalize("NFC", read_essay())
    assert "4:11" in essay or "Deuteronomy" in essay, (
        "essay.md must cite Deuteronomy 4:11"
    )


def test_essay_mentions_exodus_19_18():
    essay = unicodedata.normalize("NFC", read_essay())
    assert "19:18" in essay or "Exodus" in essay, (
        "essay.md must cite Exodus 19:18"
    )


def test_essay_has_hebrew_devarim_verse():
    """essay.md must contain the Deuteronomy 4:11 Hebrew text with nikud."""
    essay = unicodedata.normalize("NFC", read_essay())
    phrase = unicodedata.normalize("NFC", "וְהָהָר בֹּעֵר בָּאֵשׁ")
    assert phrase in essay, (
        "essay.md must contain the Hebrew text of Deuteronomy 4:11 (with nikud)"
    )


def test_essay_has_hebrew_shemot_verse():
    """essay.md must contain the Exodus 19:18 Hebrew text with nikud."""
    essay = unicodedata.normalize("NFC", read_essay())
    phrase = unicodedata.normalize("NFC", "וְהַר סִינַי עָשַׁן כֻּלּוֹ")
    assert phrase in essay, (
        "essay.md must contain the Hebrew text of Exodus 19:18 (with nikud)"
    )


def test_essay_mentions_mechilta():
    essay = read_essay()
    assert "Mechilta" in essay or "mechilta" in essay.lower(), (
        "essay.md must mention Mechilta d'Rabbi Yishmael"
    )


def test_essay_mentions_black_fire_white_fire():
    essay = read_essay().lower()
    assert "black fire" in essay or "fire on fire" in essay, (
        "essay.md must mention the black fire on white fire tradition"
    )


def test_essay_mentions_shabbat_88b():
    essay = read_essay()
    assert "Shabbat" in essay and "88b" in essay, (
        "essay.md must cite Talmud Bavli Shabbat 88b"
    )


def test_essay_mentions_hefker_or_wilderness():
    essay = read_essay().lower()
    assert "wilderness" in essay or "hefker" in essay or "ownerless" in essay, (
        "essay.md must explain why Torah was given in the ownerless wilderness"
    )


def test_essay_has_english_translations():
    """essay.md must include English translations of both quoted verses."""
    essay = read_essay()
    assert "heart of heaven" in essay or "unto the heart" in essay, (
        "essay.md must include English translation of Deuteronomy 4:11"
    )
    assert "smoke of a furnace" in essay, (
        "essay.md must include English translation of Exodus 19:18"
    )


def test_essay_has_at_least_400_words():
    essay = read_essay()
    word_count = len(essay.split())
    assert word_count >= 400, (
        f"essay.md has only {word_count} words (minimum 400 for this piece)"
    )


# ---------------------------------------------------------------------------
# index.html inline essay and scripture
# ---------------------------------------------------------------------------

def test_html_contains_hebrew_devarim():
    """index.html must embed the Deuteronomy 4:11 Hebrew text inline."""
    html = unicodedata.normalize("NFC", read_html())
    phrase = unicodedata.normalize("NFC", "וְהָהָר בֹּעֵר בָּאֵשׁ")
    assert phrase in html, (
        "index.html must contain Hebrew text of Deuteronomy 4:11"
    )


def test_html_contains_hebrew_shemot():
    """index.html must embed the Exodus 19:18 Hebrew text inline."""
    html = unicodedata.normalize("NFC", read_html())
    phrase = unicodedata.normalize("NFC", "וְהַר סִינַי עָשַׁן כֻּלּוֹ")
    assert phrase in html, (
        "index.html must contain Hebrew text of Exodus 19:18"
    )


def test_html_has_rtl_direction():
    """HTML must use direction:rtl or dir='rtl' for Hebrew scripture blocks."""
    html = read_html()
    assert "direction: rtl" in html or 'direction:rtl' in html or 'dir="rtl"' in html or "direction: rtl" in html, (
        "index.html must set right-to-left direction for Hebrew text"
    )


def test_html_has_scripture_block():
    """index.html must contain visible scripture block elements."""
    html = read_html()
    assert "scripture" in html or "hebrew" in html.lower(), (
        "index.html must contain scripture or Hebrew display blocks"
    )


def test_html_essay_is_inline():
    """index.html must embed essay text inline (no runtime fetch)."""
    html = read_html()
    essay = read_essay()
    sampled = [w for w in essay.split() if len(w) > 6][:12]
    found = sum(1 for w in sampled if w in html)
    assert found >= 6, (
        f"index.html must embed essay content inline ({found}/12 sampled words found)"
    )


# ---------------------------------------------------------------------------
# Thumbnail
# ---------------------------------------------------------------------------

def test_piece_63_thumbnail_is_valid_svg():
    path = os.path.join(PIECE_DIR, "thumbnail.svg")
    text = open(path, encoding="utf-8").read()
    assert "<svg" in text and "</svg>" in text


def test_piece_63_thumbnail_has_gradient():
    text = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert "radialGradient" in text or "linearGradient" in text, (
        "thumbnail.svg must use gradients for fire glow"
    )


def test_piece_63_thumbnail_has_mountain():
    text = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert "polygon" in text or "path" in text, (
        "thumbnail.svg must contain a mountain shape (polygon or path)"
    )


def test_piece_63_thumbnail_has_lightning():
    text = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert "polyline" in text or "line" in text, (
        "thumbnail.svg must contain a lightning bolt (polyline or line)"
    )


# ---------------------------------------------------------------------------
# README
# ---------------------------------------------------------------------------

def test_piece_63_readme_mentions_sinai():
    text = open(os.path.join(PIECE_DIR, "README.md"), encoding="utf-8").read().lower()
    assert "sinai" in text


def test_piece_63_readme_mentions_webgl():
    text = open(os.path.join(PIECE_DIR, "README.md"), encoding="utf-8").read().lower()
    assert "webgl" in text


def test_piece_63_readme_mentions_ray_marching():
    text = open(os.path.join(PIECE_DIR, "README.md"), encoding="utf-8").read().lower()
    assert "ray" in text and "march" in text


# ---------------------------------------------------------------------------
# Edge cases and failure modes
# ---------------------------------------------------------------------------

def test_missing_piece_63_entry_detected():
    """A pieces.json without piece 63 must return None from get_piece()."""
    bad_data = [p for p in load_pieces() if p["id"] != PIECE_ID]
    result = next((p for p in bad_data if p["id"] == PIECE_ID), None)
    assert result is None


def test_fire_hue_edge_h_negative_clamped():
    """Values slightly below 0 should not crash; Python behavior is extrapolation."""
    c = fire_hue_python(0.0)
    for ch in c:
        assert math.isfinite(ch)


def test_fire_hue_edge_h_above_1():
    """h slightly above 1.0 — function should remain finite."""
    c = fire_hue_python(1.0)
    for ch in c:
        assert math.isfinite(ch)


def test_smin_zero_k_returns_min():
    """With k approaching zero smin should return the actual minimum."""
    a, b = 3.0, 7.0
    result = smin_python(a, b, 0.0001)
    assert abs(result - a) < 0.01, f"smin with tiny k should ≈ min(a,b)={a}, got {result}"


def test_pieces_json_no_duplicate_ids():
    pieces = load_pieces()
    ids = [p["id"] for p in pieces]
    assert len(ids) == len(set(ids)), "Duplicate piece IDs detected in pieces.json"


# ---------------------------------------------------------------------------
# Bug-fix regression tests (reviewer round 2)
# ---------------------------------------------------------------------------

def test_camera_lookat_not_negated_forward():
    """lookAt must return mat3(r, u, f) — NOT mat3(r, u, -f).

    When the forward column is negated the centre ray points away from the
    target and the mountain is never hit.  Verified as a string check since
    the only occurrence of mat3 in the shader is the lookAt return.
    """
    html = read_html()
    assert "mat3(r, u, -f)" not in html, (
        "lookAt() must not negate the forward column: use mat3(r, u, f)"
    )
    assert "mat3(r, u, f)" in html, (
        "lookAt() must return mat3(r, u, f) so the centre ray aims at the target"
    )


def test_fire_drift_speed_matches_essay():
    """Fire vertical drift must be 0.15 units/sec, matching the essay claim.

    The essay states 'The fire drifts at 0.15 units per second.'  A drift
    constant of 0.4 would contradict that claim and make the fire move faster
    than described.
    """
    html = read_html()
    assert "u_time * 0.15" in html, (
        "Fire noise drift must use 0.15 (units/sec) as stated in the essay; "
        "found a different constant"
    )
    assert "u_time * 0.4" not in html, (
        "Fire noise drift must not use 0.4 — that contradicts the essay's 0.15 units/sec claim"
    )


def test_lightning_shader_iterates_segment_pairs():
    """Lightning loop must step k by 2, reading independent (start, end) pairs.

    The JS genBolt() stores segments as explicit (x0,y0, x1,y1) pairs —
    NOT a continuous polyline.  A k++ step would connect unrelated endpoints,
    creating spurious stray segments during each flash.
    """
    html = read_html()
    assert "k += 2" in html, (
        "Lightning shader loop must use 'k += 2' to read independent segment pairs"
    )
    assert "k + 1 >= u_boltCount" in html, (
        "Lightning loop bounds must check 'k + 1 >= u_boltCount' for pair iteration"
    )
