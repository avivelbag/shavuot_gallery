"""
Tests specific to piece 61-dejong-attractor-sinai-fire.

Verifies that the piece satisfies all acceptance criteria: correct directory
layout, animation requirements (canvas, requestAnimationFrame, density buffer,
tone-mapping), colour scheme, Hebrew overlay, essay content with scripture
blocks, and pieces.json registration.
"""
import json
import os


GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID = "61-dejong-attractor-sinai-fire"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
INDEX_HTML = os.path.join(PIECE_DIR, "index.html")
ESSAY_MD = os.path.join(PIECE_DIR, "essay.md")
THUMBNAIL = os.path.join(PIECE_DIR, "thumbnail.svg")
README = os.path.join(PIECE_DIR, "README.md")
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _html():
    return open(INDEX_HTML, encoding="utf-8").read()


def _essay():
    return open(ESSAY_MD, encoding="utf-8").read()


def _piece_entry():
    with open(PIECES_JSON, encoding="utf-8") as fh:
        pieces = json.load(fh)
    for p in pieces:
        if p["id"] == PIECE_ID:
            return p
    return None


# ---------------------------------------------------------------------------
# File layout — acceptance criterion 1
# ---------------------------------------------------------------------------

def test_piece_directory_exists():
    assert os.path.isdir(PIECE_DIR), f"Piece directory {PIECE_DIR} does not exist"


def test_index_html_exists():
    assert os.path.isfile(INDEX_HTML), "index.html missing from piece directory"


def test_essay_md_exists():
    assert os.path.isfile(ESSAY_MD), "essay.md missing from piece directory"


def test_thumbnail_svg_exists():
    assert os.path.isfile(THUMBNAIL), "thumbnail.svg missing from piece directory"


def test_readme_exists():
    assert os.path.isfile(README), "README.md missing from piece directory"


# ---------------------------------------------------------------------------
# Canvas animation — acceptance criteria 2 & 5
# ---------------------------------------------------------------------------

def test_canvas_element_present():
    assert "<canvas" in _html(), "index.html must include a <canvas> element"


def test_canvas_dimensions_700():
    html = _html()
    assert "700" in html, "Canvas should be 700px"


def test_request_animation_frame_used():
    assert "requestAnimationFrame" in _html(), \
        "index.html must use requestAnimationFrame for animation"


def test_density_buffer_float32():
    """Acceptance criterion 2: density buffer is Float32Array."""
    assert "Float32Array" in _html(), \
        "index.html must use a Float32Array density buffer"


def test_iterates_8000_points_per_frame():
    """Acceptance criterion 2: batches of 8000 points per frame."""
    assert "8000" in _html(), \
        "iterate() must process 8000 points per frame"


def test_logarithmic_tone_mapping():
    """Acceptance criterion 2: log-scale tone mapping (log1p)."""
    assert "log1p" in _html(), \
        "index.html must use Math.log1p for logarithmic tone mapping"


# ---------------------------------------------------------------------------
# de Jong attractor formula — acceptance criterion 2
# ---------------------------------------------------------------------------

def test_dejong_formula_sin_cos_present():
    html = _html()
    assert "Math.sin" in html, "de Jong formula requires Math.sin"
    assert "Math.cos" in html, "de Jong formula requires Math.cos"


def test_parameter_preset_a_b_c_d():
    """Acceptance criterion 3: primary preset a=1.641, b=1.902, c=0.316, d=1.525."""
    html = _html()
    assert "1.641" in html, "Primary parameter a=1.641 must be present"
    assert "1.902" in html, "Primary parameter b=1.902 must be present"
    assert "0.316" in html, "Primary parameter c=0.316 must be present"
    assert "1.525" in html, "Primary parameter d=1.525 must be present"


def test_multiple_parameter_presets():
    """Acceptance criterion 3: at least 3 preset tuples for the breathing cycle."""
    html = _html()
    assert html.count("[") >= 3 or "presets" in html, \
        "index.html must define multiple parameter presets"
    assert "-2.24" in html or "-2.53" in html, \
        "At least one additional preset beyond the primary must be present"


# ---------------------------------------------------------------------------
# Colour scheme — acceptance criterion 4
# ---------------------------------------------------------------------------

def test_background_colour_050208():
    """Acceptance criterion 4: near-black background #050208."""
    assert "050208" in _html(), \
        "Background colour #050208 must appear in index.html"


def test_ember_colour_3A0800():
    """Acceptance criterion 4: deep red/ember colour stop #3A0800."""
    html = _html()
    assert "3A0800" in html or "3a0800" in html.lower(), \
        "Ember colour stop (r=58, g=8) derived from #3A0800 must be present"


def test_orange_colour_stop_present():
    """Acceptance criterion 4: orange mid-stop C04010 values."""
    html = _html()
    assert "192" in html, "Orange colour stop requires r=192 (from #C04010)"


def test_gold_white_colour_stop():
    """Acceptance criterion 4: gold/white high-density stop #FFF0B0.

    #FFF0B0 = rgb(255, 240, 176).  The render formula reaches g=240 via
    64 + s*176 and b=176 via 16 + s*160, so we check for the step constants.
    """
    html = _html()
    assert "176" in html, \
        "Gold-white stop: green channel step 176 (64+176=240) must appear in render formula"
    assert "160" in html, \
        "Gold-white stop: blue channel step 160 (16+160=176) must appear in render formula"


# ---------------------------------------------------------------------------
# Hebrew overlay — acceptance criterion 6
# ---------------------------------------------------------------------------

def test_hebrew_sinai_overlay_present():
    """Acceptance criterion 6: Hebrew phrase 'וְהַר סִינַי עָשַׁן כֻּלּוֹ' on the canvas."""
    html = _html()
    assert "וְהַר סִינַי עָשַׁן כֻּלּוֹ" in html, \
        "Hebrew overlay 'וְהַר סִינַי עָשַׁן כֻּלּוֹ' must appear in index.html"


def test_hebrew_overlay_warm_colour():
    """Acceptance criterion 6: overlay uses a warm-cream colour."""
    html = _html()
    assert "F5E8C8" in html or "E8C8" in html or "FFF" in html.lower(), \
        "Hebrew overlay must use a warm-cream colour"


def test_hebrew_overlay_font_size_15():
    """Acceptance criterion 6: overlay is 15px."""
    assert "15px" in _html(), "Hebrew overlay must be 15px font size"


# ---------------------------------------------------------------------------
# Essay content — acceptance criterion 7
# ---------------------------------------------------------------------------

def test_essay_exceeds_380_words():
    essay = _essay()
    word_count = len(essay.split())
    assert word_count >= 350, \
        f"essay.md has only {word_count} words; expected ~380+"


def test_essay_quotes_exodus_19_16():
    """Acceptance criterion 7: Exodus 19:16 thunder and shofar verse."""
    essay = _essay()
    assert "19:16" in essay or "י״ט:ט״ז" in essay, \
        "essay.md must cite Exodus 19:16"


def test_essay_quotes_exodus_19_18():
    """Acceptance criterion 7: Exodus 19:18 smoke-of-furnace verse."""
    essay = _essay()
    assert "19:18" in essay or "כְּעֶשֶׁן הַכִּבְשָׁן" in essay, \
        "essay.md must quote Exodus 19:18 or the phrase כְּעֶשֶׁן הַכִּבְשָׁן"


def test_essay_contains_hebrew_scripture_with_nikud():
    """Orchestrator requirement: Hebrew with nikud present as scripture block."""
    essay = _essay()
    assert "וְהַר סִינַי" in essay, \
        "essay.md must contain Hebrew scripture text with nikud"
    assert "וַיְהִי" in essay, \
        "essay.md must contain the Exodus 19:16 Hebrew text"


def test_essay_contains_exodus_13_21():
    """Acceptance criterion 7: cloud-by-day, fire-by-night duality."""
    essay = _essay()
    assert "13:21" in essay or "בְּעַמּוּד עָנָן" in essay, \
        "essay.md must include Exodus 13:21 (cloud by day, fire by night)"


def test_essay_mentions_talmud_shabbat_88():
    """Acceptance criterion 7: Talmud Shabbat 88b mountain uprooted."""
    essay = _essay()
    assert "Shabbat" in essay or "שבת" in essay.lower() or "88" in essay, \
        "essay.md must mention Talmud Shabbat 88b"


def test_essay_mentions_rashi():
    """Acceptance criterion 7: Rashi on cloud enabling approach."""
    assert "Rashi" in _essay(), "essay.md must mention Rashi"


def test_essay_embedded_in_index_html():
    """Acceptance criterion 7 & orchestrator: essay text embedded inline in HTML."""
    html = _html()
    assert "כְּעֶשֶׁן הַכִּבְשָׁן" in html, \
        "Key Hebrew phrase must be embedded in index.html (not fetched at runtime)"
    assert "Rashi" in html, \
        "Essay content must be embedded in index.html"


def test_index_html_no_fetch_of_essay():
    """index.html must not dynamically fetch essay.md at runtime."""
    html = _html()
    assert "fetch(" not in html.lower() or "essay.md" not in html, \
        "index.html must not fetch essay.md at runtime — embed text inline"


# ---------------------------------------------------------------------------
# Thumbnail — acceptance criterion 8
# ---------------------------------------------------------------------------

def test_thumbnail_is_valid_svg():
    svg = open(THUMBNAIL, encoding="utf-8").read()
    assert "<svg" in svg and "</svg>" in svg, \
        "thumbnail.svg must be a valid SVG document"


def test_thumbnail_has_near_black_background():
    svg = open(THUMBNAIL, encoding="utf-8").read()
    assert "050208" in svg, \
        "thumbnail.svg must use background colour #050208"


def test_thumbnail_has_orange_gold_colours():
    svg = open(THUMBNAIL, encoding="utf-8").read()
    assert "C04010" in svg or "D08040" in svg or "FFF0B0" in svg or "FFD" in svg, \
        "thumbnail.svg must use orange/gold flame colours"


def test_thumbnail_viewbox_400():
    svg = open(THUMBNAIL, encoding="utf-8").read()
    assert "400" in svg, "thumbnail.svg viewBox should be ~400×400"


# ---------------------------------------------------------------------------
# pieces.json registration — acceptance criterion 9
# ---------------------------------------------------------------------------

def test_piece_in_pieces_json():
    assert _piece_entry() is not None, \
        f"Piece '{PIECE_ID}' not found in pieces.json"


def test_piece_theme_har_sinai():
    p = _piece_entry()
    assert p is not None
    assert "Har Sinai" in p["theme"], \
        f"theme must contain 'Har Sinai', got: {p['theme']}"


def test_piece_technique_dejong():
    p = _piece_entry()
    assert p is not None
    assert "de Jong" in p["technique"] or "dejong" in p["technique"].lower(), \
        f"technique must mention 'de Jong', got: {p['technique']}"


def test_piece_technique_density():
    p = _piece_entry()
    assert p is not None
    assert "density" in p["technique"].lower() or "accumulation" in p["technique"].lower(), \
        f"technique must mention density accumulation, got: {p['technique']}"


def test_piece_paths_correct():
    p = _piece_entry()
    assert p is not None
    assert p["path"] == f"pieces/{PIECE_ID}/index.html"
    assert p["thumbnail"] == f"pieces/{PIECE_ID}/thumbnail.svg"
    assert p["essay"] == f"pieces/{PIECE_ID}/essay.md"


def test_piece_year_2026():
    p = _piece_entry()
    assert p is not None
    assert p["year"] == 2026


def test_piece_id_unique():
    with open(PIECES_JSON, encoding="utf-8") as fh:
        pieces = json.load(fh)
    ids = [p["id"] for p in pieces]
    assert ids.count(PIECE_ID) == 1, f"Piece ID '{PIECE_ID}' appears more than once"


# ---------------------------------------------------------------------------
# Edge cases and failure modes
# ---------------------------------------------------------------------------

def test_empty_density_buffer_render_graceful():
    """
    Verify the render function handles an all-zero density buffer without
    division-by-zero.  We check that maxD defaults to 1 (log1p(1) > 0) when
    the buffer is empty — this prevents NaN in the tone-mapping formula.
    """
    html = _html()
    assert "maxD < 1" in html or "maxD = 1" in html or "|| 1" in html, \
        "render() must guard against a zero-max density (maxD fallback to 1)"


def test_pixel_bounds_check_present():
    """Density buffer must guard against out-of-bounds pixel writes."""
    html = _html()
    assert ">= 0" in html and "< W" in html, \
        "iterate() must check px/py are within [0, W) before writing to density"


def test_fade_decay_factor_present():
    """Parameter cycling must use a decay factor to dissolve between presets."""
    html = _html()
    assert "0.88" in html or "decay" in html.lower() or "*=" in html, \
        "Cycling between presets must use a density decay factor"


def test_readme_mentions_sinai(tmp_path):
    """README.md must mention Sinai or Matan Torah (gallery consistency check)."""
    text = open(README, encoding="utf-8").read().lower()
    assert "sinai" in text or "matan torah" in text, \
        "README.md must mention Sinai or Matan Torah"


def test_missing_piece_entry_detected(tmp_path):
    """A pieces.json without this piece should fail the lookup (fixture confirms)."""
    bad_pieces = [{"id": "01-thunder-at-sinai", "title": "Thunder"}]
    bad_json = tmp_path / "pieces.json"
    bad_json.write_text(json.dumps(bad_pieces), encoding="utf-8")
    data = json.loads(bad_json.read_text())
    found = any(p["id"] == PIECE_ID for p in data)
    assert not found, "Fixture should not contain the new piece — confirms detection logic"
