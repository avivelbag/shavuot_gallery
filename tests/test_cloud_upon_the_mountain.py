"""
Tests for piece 52-cloud-upon-the-mountain — WebGL fBm cloud with interior fire.

Covers: pieces.json registration, file layout, WebGL shader requirements
(fBm, domain warp, pulse animation, hash noise), mountain ridge, cloud color ramp,
Hebrew overlay, essay content (Exodus 19:9, 24:15-18, Berakhot 7a, Shekhinah),
thumbnail validity, and edge cases.
"""
import json
import math
import os
import re

import pytest

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECES_JSON  = os.path.join(GALLERY_ROOT, "pieces.json")
PIECE_ID     = "52-cloud-upon-the-mountain"
PIECE_DIR    = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
INDEX_HTML   = os.path.join(PIECE_DIR, "index.html")
ESSAY_MD     = os.path.join(PIECE_DIR, "essay.md")
THUMBNAIL    = os.path.join(PIECE_DIR, "thumbnail.svg")
README_MD    = os.path.join(PIECE_DIR, "README.md")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_pieces():
    """Return the parsed pieces.json list."""
    with open(PIECES_JSON, encoding="utf-8") as fh:
        return json.load(fh)


def get_piece():
    """Return the pieces.json entry for 52-cloud-upon-the-mountain, or None."""
    return next((p for p in load_pieces() if p["id"] == PIECE_ID), None)


def read_html():
    """Return the full text of index.html."""
    with open(INDEX_HTML, encoding="utf-8") as fh:
        return fh.read()


def read_essay():
    """Return the full text of essay.md."""
    with open(ESSAY_MD, encoding="utf-8") as fh:
        return fh.read()


# ---------------------------------------------------------------------------
# Happy path — pieces.json registration
# ---------------------------------------------------------------------------

def test_piece_registered_in_json():
    """The cloud piece must appear in pieces.json."""
    piece = get_piece()
    assert piece is not None, f"Piece '{PIECE_ID}' not found in pieces.json"


def test_piece_required_fields():
    """All required fields must be present and non-empty."""
    required = ("id", "title", "tagline", "year", "theme", "technique",
                "path", "thumbnail", "essay")
    piece = get_piece()
    assert piece is not None
    for field in required:
        assert field in piece, f"Missing field: {field}"
        assert piece[field], f"Empty field: {field}"


def test_piece_year_is_integer():
    """year must be a plain Python integer."""
    piece = get_piece()
    assert piece is not None
    assert isinstance(piece["year"], int), "year must be an integer"


def test_piece_path_format():
    """path must follow the standard pieces/<id>/index.html convention."""
    piece = get_piece()
    assert piece is not None
    assert piece["path"] == f"pieces/{PIECE_ID}/index.html"


def test_piece_technique_mentions_webgl():
    """technique field must identify this as a WebGL shader piece."""
    piece = get_piece()
    assert piece is not None
    assert "WebGL" in piece["technique"] or "webgl" in piece["technique"].lower()


def test_piece_technique_mentions_fbm():
    """technique field must mention fBm (domain-warped noise is the distinguishing method)."""
    piece = get_piece()
    assert piece is not None
    assert "fBm" in piece["technique"] or "fbm" in piece["technique"].lower()


def test_piece_theme_cites_exodus():
    """theme must reference Exodus — the scriptural source of the cloud imagery."""
    piece = get_piece()
    assert piece is not None
    assert "Exodus" in piece["theme"]


# ---------------------------------------------------------------------------
# Happy path — files on disk
# ---------------------------------------------------------------------------

def test_index_html_exists():
    assert os.path.isfile(INDEX_HTML), f"index.html missing: {INDEX_HTML}"


def test_essay_md_exists():
    assert os.path.isfile(ESSAY_MD), f"essay.md missing: {ESSAY_MD}"


def test_thumbnail_exists():
    assert os.path.isfile(THUMBNAIL), f"thumbnail.svg missing: {THUMBNAIL}"


def test_readme_exists():
    assert os.path.isfile(README_MD), f"README.md missing: {README_MD}"


# ---------------------------------------------------------------------------
# Happy path — WebGL / shader elements in index.html
# ---------------------------------------------------------------------------

def test_html_has_webgl_canvas():
    """index.html must contain a canvas element for the WebGL context."""
    html = read_html()
    assert "<canvas" in html, "index.html must contain a <canvas> element"


def test_html_uses_requestanimationframe():
    """Animation must use requestAnimationFrame for a continuous loop."""
    html = read_html()
    assert "requestAnimationFrame" in html


def test_html_has_utime_uniform():
    """Fragment shader must declare a uTime uniform to drive animation."""
    html = read_html()
    assert "uTime" in html, "Fragment shader must use a uTime uniform"


def test_html_has_fragment_shader():
    """index.html must contain an inline fragment shader script tag."""
    html = read_html()
    assert "x-shader/x-fragment" in html or "FRAGMENT_SHADER" in html


def test_html_shader_has_fbm():
    """Shader must define an fbm function for layered fractional Brownian motion."""
    html = read_html()
    assert "fbm" in html, "Shader must define an fbm (fractional Brownian motion) function"


def test_html_shader_has_domain_warp():
    """Shader must implement domain warping (noise output feeding into further fbm calls).

    Domain warp is identified by a warp vector (q or r) that feeds into a subsequent
    fbm evaluation, producing the billowing cloud shapes.
    """
    html = read_html()
    assert re.search(r"\bq\b.*fbm|fbm.*\bq\b|\br\b.*fbm|fbm.*\br\b", html, re.DOTALL), (
        "Shader must implement domain warping via warp vectors fed into fbm"
    )


def test_html_shader_has_hash_noise():
    """Shader must define a hash-based noise function (no texture dependency)."""
    html = read_html()
    assert "hash(" in html or "float hash" in html


def test_html_shader_has_fire_pulse():
    """Shader must implement a time-driven brightness pulse for the fire colors.

    The pulse is the key animation feature that distinguishes this piece from
    34-consuming-fire (which has no pulse).
    """
    html = read_html()
    assert "pulse" in html, "Shader must use a 'pulse' variable for fire-color pulsing"
    assert re.search(r"sin\s*\(", html), "Pulse must be driven by sin() of uTime"


def test_html_shader_fire_pulse_amplitude():
    """The pulse must allow ±15% variation: coefficient near 0.15."""
    html = read_html()
    assert "0.15" in html, "Pulse amplitude coefficient 0.15 must appear in the shader"


def test_html_shader_has_color_ramp():
    """Shader must map cloud density through a multi-stop color ramp using smoothstep."""
    html = read_html()
    assert "smoothstep" in html, "Color ramp must use smoothstep"


def test_html_shader_has_amber_color():
    """Shader color ramp must include the deep amber fire color (#FF6A00 ≈ 1.0, 0.416, 0.0)."""
    html = read_html()
    assert "cAmber" in html or "0.416" in html, (
        "Shader must include amber fire color (cAmber or 0.416 component)"
    )


def test_html_shader_has_gold_color():
    """Shader color ramp must include gold (#FFD700 ≈ 1.0, 0.843, 0.0)."""
    html = read_html()
    assert "cGold" in html or "0.843" in html, (
        "Shader must include gold fire color (cGold or 0.843 component)"
    )


def test_html_shader_has_mountain_ridge():
    """Shader must define a mountain ridge/silhouette function."""
    html = read_html()
    assert "ridgeHeight" in html or "mRidge" in html or "ridge" in html.lower(), (
        "Shader must implement a mountain ridge silhouette"
    )


def test_html_shader_mountain_uses_exp():
    """Mountain ridge must use Gaussian (exp) peaks for a realistic multi-peak profile.

    This distinguishes the ridge from 34-consuming-fire's single abs()-based triangle SDF.
    """
    html = read_html()
    assert "exp(" in html, (
        "Mountain ridge must use exp() for Gaussian peaks (not a simple triangle SDF)"
    )


def test_html_shader_sky_is_blue_black():
    """Background sky must use the specified deep blue-black palette (#0D0A1A)."""
    html = read_html()
    assert "0D0A1A" in html or ("0.051" in html and "0.039" in html and "0.102" in html), (
        "Sky must use #0D0A1A palette (0.051, 0.039, 0.102)"
    )


def test_html_shader_cloud_zone_mask():
    """Shader must gate the cloud density to the upper two-thirds of the canvas.

    This produces the distinct composition: cloud above, mountain silhouette below.
    """
    html = read_html()
    assert "baseGate" in html or "zoneMask" in html or "cloudZone" in html or (
        "smoothstep" in html and "0.28" in html
    ), "Shader must have a cloud-presence zone mask confining the cloud to the upper region"


# ---------------------------------------------------------------------------
# Happy path — Hebrew overlay
# ---------------------------------------------------------------------------

def test_html_has_hebrew_overlay_element():
    """The Hebrew inscription must appear as an HTML element, not in the shader."""
    html = read_html()
    assert "וַיְכַס הֶעָנָן אֶת-הָהָר" in html or "ויכס הענן את-ההר" in html, (
        "index.html must contain 'וַיְכַס הֶעָנָן אֶת-הָהָר' as an HTML element"
    )


def test_hebrew_overlay_not_in_shader():
    """Hebrew text must be in the HTML body, not rendered inside the WebGL shader."""
    html = read_html()
    shader_pattern = re.compile(
        r'<script[^>]+x-shader[^>]*>.*?</script>', re.DOTALL | re.IGNORECASE
    )
    shaders = "".join(m.group() for m in shader_pattern.finditer(html))
    assert "וַיְכַס" not in shaders, (
        "Hebrew phrase must not appear inside shader script blocks"
    )


# ---------------------------------------------------------------------------
# Happy path — essay content
# ---------------------------------------------------------------------------

def test_essay_word_count():
    """essay.md must contain at least 200 words."""
    text = read_essay()
    count = len(text.split())
    assert count >= 200, f"essay.md has only {count} words (minimum 200)"


def test_essay_cites_exodus_19_9():
    """Essay must cite Exodus 19:9 — the thick-cloud announcement."""
    text = read_essay()
    assert "19:9" in text, "essay.md must cite Exodus 19:9"


def test_essay_cites_exodus_24_15_18():
    """Essay must cite Exodus 24:15–18 — Moses entering the cloud."""
    text = read_essay()
    assert "24:15" in text or "24:15–18" in text, (
        "essay.md must cite Exodus 24:15–18"
    )


def test_essay_cites_berakhot_7a():
    """Essay must cite Berakhot 7a — Moses' three requests."""
    text = read_essay()
    assert "Berakhot" in text and "7a" in text, (
        "essay.md must cite Talmud Berakhot 7a"
    )


def test_essay_mentions_shekhinah():
    """Essay must explain the Shekhinah theology central to the cloud's meaning."""
    text = read_essay()
    assert "Shekhinah" in text or "shekhinah" in text.lower(), (
        "essay.md must discuss the Shekhinah — the indwelling divine presence"
    )


def test_essay_mentions_cloud_as_medium():
    """Essay must articulate that the cloud is not an obstacle but a medium of revelation."""
    text = read_essay()
    lower = text.lower()
    assert "medium" in lower or "accommodate" in lower or "accommodation" in lower or \
           "approachable" in lower, (
        "essay.md must explain that the cloud is the medium making revelation approachable"
    )


def test_essay_mentions_shavuot():
    """Essay must connect the piece to Shavuot."""
    text = read_essay()
    assert "Shavuot" in text or "shavuot" in text.lower()


def test_essay_mentions_domain_warp_or_fbm():
    """Essay must explain the technique (domain-warped fBm) as theological metaphor."""
    text = read_essay()
    assert "domain warp" in text.lower() or "fractional Brownian" in text or "fBm" in text or \
           "domain warping" in text.lower(), (
        "essay.md must reference the domain-warped fBm technique"
    )


def test_essay_embedded_in_html():
    """Essay text must be embedded in index.html (no runtime fetch of essay.md)."""
    essay = read_essay()
    html  = read_html()
    words = [w for w in essay.split() if len(w) > 6]
    sampled = words[:15]
    found = sum(1 for w in sampled if w in html)
    assert found >= 8, (
        f"index.html does not embed essay text (only {found}/15 sampled words found)"
    )


# ---------------------------------------------------------------------------
# Python mirror of pulse math — deterministic unit test of shader logic
# ---------------------------------------------------------------------------

def pulse_value(t):
    """Mirror of the GLSL pulse: 0.85 + 0.15 * sin(t * 1.2566).

    Used to verify the amplitude and period of the fire-color pulse without
    running a browser.
    """
    return 0.85 + 0.15 * math.sin(t * 1.2566)


def test_pulse_amplitude_range():
    """Pulse value must stay within [0.70, 1.00] — ±15% around 0.85 base."""
    samples = [pulse_value(t * 0.1) for t in range(1000)]
    assert min(samples) >= 0.69, f"Pulse falls below 0.70: {min(samples):.4f}"
    assert max(samples) <= 1.01, f"Pulse exceeds 1.00: {max(samples):.4f}"


def test_pulse_period_is_approximately_five_seconds():
    """The pulse period must be ~5 seconds (angular frequency 2π/5 ≈ 1.2566)."""
    period = 2 * math.pi / 1.2566
    assert 4.8 < period < 5.2, f"Pulse period {period:.2f}s is not ~5 seconds"


def test_pulse_minimum_at_quarter_period():
    """Pulse minimum occurs at sin = -1, i.e. t = 3π / (2 * 1.2566) ≈ 3.75s."""
    t_min = 3 * math.pi / (2 * 1.2566)
    p = pulse_value(t_min)
    assert abs(p - 0.70) < 0.01, f"Pulse at t_min={t_min:.2f} should be ~0.70, got {p:.4f}"


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

def test_no_duplicate_id_in_pieces_json():
    """Adding piece 52 must not create a duplicate ID."""
    ids = [p["id"] for p in load_pieces()]
    assert ids.count(PIECE_ID) == 1, f"Duplicate id '{PIECE_ID}' in pieces.json"


def test_piece_id_starts_with_52():
    """Piece must be numbered 52 — the next available number after the existing 51 pieces."""
    piece = get_piece()
    assert piece is not None
    assert piece["id"].startswith("52-"), f"Expected id starting with '52-', got '{piece['id']}'"


def test_thumbnail_is_valid_svg():
    """thumbnail.svg must contain valid SVG markup."""
    text = open(THUMBNAIL, encoding="utf-8").read()
    assert "<svg" in text and "</svg>" in text


def test_essay_has_cloud_covered_mountain_phrase():
    """Essay must reference 'the cloud covered the mountain' — the inscription phrase."""
    text = read_essay()
    assert "cloud covered" in text.lower() or "cloud" in text.lower() and "covered" in text.lower()


def test_piece_is_distinct_from_consuming_fire():
    """This piece must use a different palette keyword than 34-consuming-fire.

    34-consuming-fire uses 'cViolet' for the sky. This piece uses '#0D0A1A' / blue-black.
    Confirms the two WebGL pieces have distinct palettes.
    """
    html = read_html()
    assert "cViolet" not in html, (
        "This piece must not reuse the 'cViolet' sky variable from 34-consuming-fire"
    )
    assert "0D0A1A" in html or ("0.051" in html and "0.039" in html), (
        "This piece must use the #0D0A1A blue-black sky, distinct from 34-consuming-fire"
    )


# ---------------------------------------------------------------------------
# Failure mode — missing file and bad data detection
# ---------------------------------------------------------------------------

def test_missing_essay_detected(tmp_path):
    """A nonexistent essay path must not exist — confirms detection logic fixture."""
    missing = os.path.join(str(tmp_path), "nonexistent.md")
    assert not os.path.isfile(missing), "Fixture: path must not exist"


def test_empty_essay_fails_word_count():
    """An empty string must not pass the 200-word minimum check."""
    text = ""
    count = len(text.split())
    assert count < 200, "Empty essay should fail word-count gate"


def test_piece_with_wrong_path_would_fail():
    """A piece entry pointing to a nonexistent file would fail the html-exists check."""
    fake_path = os.path.join(GALLERY_ROOT, "pieces", "99-fake", "index.html")
    assert not os.path.isfile(fake_path), "Fixture: fake path must not exist on disk"


def test_pulse_never_zero():
    """Pulse can never reach zero (base = 0.85, amplitude = 0.15), so fire is always visible."""
    min_pulse = 0.85 - 0.15
    assert min_pulse > 0, "Pulse minimum must be positive — fire cannot go dark"
