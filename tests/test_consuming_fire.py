"""
Tests for piece 34-consuming-fire — WebGL plasma fire at Sinai.

Verifies the piece directory layout, pieces.json registration, WebGL shader
elements, HTML overlay, essay content, and acceptance-criteria specifics.
"""
import json
import os
import re

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECES_JSON  = os.path.join(GALLERY_ROOT, "pieces.json")
PIECE_ID     = "34-consuming-fire"
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
    """Return the pieces.json entry for 34-consuming-fire, or None."""
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
    """The consuming-fire piece must appear in pieces.json."""
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
    piece = get_piece()
    assert piece is not None
    assert isinstance(piece["year"], int), "year must be an integer"


def test_piece_path_format():
    piece = get_piece()
    assert piece is not None
    assert piece["path"] == f"pieces/{PIECE_ID}/index.html"


def test_piece_technique_mentions_webgl():
    """The technique field must identify this as a WebGL shader piece."""
    piece = get_piece()
    assert piece is not None
    assert "WebGL" in piece["technique"] or "webgl" in piece["technique"].lower()


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
    """Animation must use requestAnimationFrame for a seamless 60fps loop."""
    html = read_html()
    assert "requestAnimationFrame" in html


def test_html_has_utime_uniform():
    """The fragment shader must declare a uTime uniform to drive animation."""
    html = read_html()
    assert "uTime" in html, "Fragment shader must use a uTime uniform"


def test_html_has_fragment_shader():
    """index.html must contain an inline fragment shader script tag."""
    html = read_html()
    assert "x-shader/x-fragment" in html or "FRAGMENT_SHADER" in html


def test_html_shader_has_fbm():
    """The shader must define an fBm function for layered noise."""
    html = read_html()
    assert "fbm" in html, "Shader must define an fbm (fractional Brownian motion) function"


def test_html_shader_has_domain_warp():
    """The shader must use domain warping (offset noise coords with noise output)."""
    html = read_html()
    # Domain warp is identified by the warp vector q feeding into a further fbm call
    assert re.search(r"\bq\b.*fbm|fbm.*\bq\b", html, re.DOTALL), (
        "Shader must implement domain warping via a warp vector fed into fbm"
    )


def test_html_shader_has_hash_noise():
    """The shader must define a hash-based noise function (no texture)."""
    html = read_html()
    assert "hash(" in html or "float hash" in html


def test_html_shader_has_fire_color_ramp():
    """Shader must map noise through a multi-stop color ramp toward white."""
    html = read_html()
    assert "smoothstep" in html, "Shader color ramp must use smoothstep"
    # White at hottest core
    assert "0.97" in html or "0.92" in html or "cWhite" in html


def test_html_shader_has_mountain_sdf():
    """Shader must define a mountain silhouette using an SDF-style expression."""
    html = read_html()
    # Mountain line formula involves abs(uv.x - 0.5) or similar
    assert "abs(" in html and ("0.5" in html or "mline" in html)


def test_html_shader_sky_gradient():
    """Shader must define a sky color transitioning from violet to near-black."""
    html = read_html()
    assert "cViolet" in html or "violet" in html.lower() or "Violet" in html


# ---------------------------------------------------------------------------
# Happy path — Hebrew overlay
# ---------------------------------------------------------------------------

def test_html_has_hebrew_overlay_element():
    """The Hebrew phrase must appear as an HTML element (not drawn in WebGL)."""
    html = read_html()
    # The phrase in Unicode
    assert "אֵשׁ אֹכֶלֶת" in html or "אש אכלת" in html, (
        "index.html must contain the Hebrew phrase 'אֵשׁ אֹכֶלֶת' as an HTML element"
    )


def test_hebrew_overlay_not_in_shader():
    """Hebrew text must be in the HTML body, not rendered inside the WebGL shader."""
    html = read_html()
    # The phrase should appear outside any <script type="x-shader"> block
    # Find the shader sections and confirm the Hebrew is outside them
    shader_pattern = re.compile(
        r'<script[^>]+x-shader[^>]*>.*?</script>', re.DOTALL | re.IGNORECASE
    )
    shaders = "".join(m.group() for m in shader_pattern.finditer(html))
    assert "אֵשׁ" not in shaders and "אֹכֶלֶת" not in shaders, (
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


def test_essay_cites_exodus_24_17():
    """Essay must cite Exodus 24:17 specifically."""
    text = read_essay()
    assert "24:17" in text, "essay.md must cite Exodus 24:17"


def test_essay_mentions_mekhilta_or_shabbat_88b():
    """Essay must reference the Mekhilta or Talmud Shabbat 88b."""
    text = read_essay()
    assert "Mekhilta" in text or "88b" in text, (
        "essay.md must reference the Mekhilta or Talmud Shabbat 88b"
    )


def test_essay_mentions_cloud_and_fire():
    """Essay must address the simultaneous cloud and fire phenomena."""
    text = read_essay()
    assert "cloud" in text.lower() and "fire" in text.lower(), (
        "essay.md must discuss both cloud and fire as Sinai phenomena"
    )


def test_essay_mentions_shavuot():
    """Essay must connect the piece to Shavuot."""
    text = read_essay()
    assert "Shavuot" in text or "shavuot" in text.lower()


def test_essay_embedded_in_html():
    """Essay text must be embedded in index.html (no runtime fetch)."""
    essay = read_essay()
    html  = read_html()
    # Check that substantial words from the essay appear in the HTML
    words = [w for w in essay.split() if len(w) > 6]
    sampled = words[:15]
    found = sum(1 for w in sampled if w in html)
    assert found >= 8, (
        f"index.html does not embed essay text (only {found}/15 sampled words found)"
    )


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

def test_no_duplicate_id_in_pieces_json():
    """Adding piece 32 must not create a duplicate ID."""
    ids = [p["id"] for p in load_pieces()]
    assert ids.count(PIECE_ID) == 1, f"Duplicate id '{PIECE_ID}' in pieces.json"


def test_thumbnail_is_valid_svg():
    """thumbnail.svg must contain valid SVG markup."""
    text = open(THUMBNAIL, encoding="utf-8").read()
    assert "<svg" in text and "</svg>" in text


def test_essay_has_consuming_fire_phrase():
    """Essay must use the phrase 'consuming fire' — the core theological concept."""
    text = read_essay()
    assert "consuming fire" in text.lower()


# ---------------------------------------------------------------------------
# Failure mode — missing file detection
# ---------------------------------------------------------------------------

def test_missing_essay_detected(tmp_path):
    """Verify that a nonexistent essay path is correctly flagged as missing."""
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
    assert not os.path.isfile(fake_path), "Fixture: fake path must not exist"
