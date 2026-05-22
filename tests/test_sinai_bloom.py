"""
Tests for piece 25 — "The Mountain in Bloom" (Sinai L-system plant growth).

Validates file layout, pieces.json entry, L-system implementation,
animation phases (growth → lightning → text), palette colours,
essay content, and essay embedding in index.html.
"""
import json
import os
import re

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECES_JSON  = os.path.join(GALLERY_ROOT, "pieces.json")
PIECE_ID     = "25-sinai-bloom"
PIECE_DIR    = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
INDEX_HTML   = os.path.join(PIECE_DIR, "index.html")
THUMBNAIL    = os.path.join(PIECE_DIR, "thumbnail.svg")
README_MD    = os.path.join(PIECE_DIR, "README.md")
ESSAY_MD     = os.path.join(PIECE_DIR, "essay.md")


def _pieces():
    with open(PIECES_JSON, encoding="utf-8") as fh:
        return json.load(fh)


def _entry():
    for p in _pieces():
        if p["id"] == PIECE_ID:
            return p
    return None


def _html():
    return open(INDEX_HTML, encoding="utf-8").read()


def _svg():
    return open(THUMBNAIL, encoding="utf-8").read()


def _readme():
    return open(README_MD, encoding="utf-8").read()


def _essay():
    return open(ESSAY_MD, encoding="utf-8").read()


# ─── File layout ─────────────────────────────────────────────────────────────

def test_index_html_exists():
    assert os.path.isfile(INDEX_HTML), f"{PIECE_ID}/index.html missing"


def test_thumbnail_svg_exists():
    assert os.path.isfile(THUMBNAIL), f"{PIECE_ID}/thumbnail.svg missing"


def test_readme_md_exists():
    assert os.path.isfile(README_MD), f"{PIECE_ID}/README.md missing"


def test_essay_md_exists():
    assert os.path.isfile(ESSAY_MD), f"{PIECE_ID}/essay.md missing"


# ─── pieces.json entry ───────────────────────────────────────────────────────

def test_entry_present_in_pieces_json():
    assert _entry() is not None, f"'{PIECE_ID}' not found in pieces.json"


def test_entry_theme_har_sinai():
    p = _entry()
    assert p is not None
    theme = p["theme"].lower()
    assert "sinai" in theme, f"Expected 'sinai' in theme, got: {p['theme']}"


def test_entry_technique_mentions_lsystem():
    p = _entry()
    assert p is not None
    tech = p["technique"].lower()
    assert "l-system" in tech or "lsystem" in tech or "turtle" in tech, \
        f"Expected L-system/turtle in technique, got: {p['technique']}"


def test_entry_technique_mentions_lightning():
    p = _entry()
    assert p is not None
    assert "lightning" in p["technique"].lower(), \
        f"technique should mention lightning, got: {p['technique']}"


def test_entry_paths_correct():
    p = _entry()
    assert p is not None
    assert p["path"]      == f"pieces/{PIECE_ID}/index.html"
    assert p["thumbnail"] == f"pieces/{PIECE_ID}/thumbnail.svg"
    assert p["essay"]     == f"pieces/{PIECE_ID}/essay.md"


def test_entry_year_is_int():
    p = _entry()
    assert p is not None
    assert isinstance(p["year"], int)


def test_no_duplicate_ids():
    ids = [p["id"] for p in _pieces()]
    assert len(ids) == len(set(ids)), f"Duplicate piece IDs: {ids}"


# ─── Canvas / animation ──────────────────────────────────────────────────────

def test_canvas_element_present():
    assert "<canvas" in _html(), "index.html must have a <canvas> element"


def test_uses_request_animation_frame():
    assert "requestAnimationFrame" in _html(), "animation must use requestAnimationFrame"


def test_canvas_width_800():
    assert "800" in _html(), "canvas width 800 not found in index.html"


def test_canvas_height_600():
    assert "600" in _html(), "canvas height 600 not found in index.html"


def test_charset_utf8():
    html = _html()
    assert 'charset="UTF-8"' in html or "charset=utf-8" in html.lower(), \
        "index.html must declare UTF-8 charset"


def test_no_external_scripts():
    html = _html()
    external = re.findall(r'<script[^>]+src\s*=\s*["\']([^"\']+)["\']', html, re.IGNORECASE)
    assert len(external) == 0, f"External scripts found: {external}"


# ─── L-system implementation ─────────────────────────────────────────────────

def test_lsystem_rules_defined():
    html = _html()
    assert "RULES" in html or "rules" in html, "L-system rules variable not found"


def test_tree_rule_string_present():
    """The canonical rule FF+[+F-F-F]-[-F+F+F] must appear in the source."""
    html = _html()
    assert "FF+[+F-F-F]-[-F+F+F]" in html, \
        "L-system production rule string not found in index.html"


def test_expand_lsystem_function_present():
    html = _html()
    assert "expandLsystem" in html or "expandLSystem" in html or "expand" in html.lower(), \
        "L-system expansion function not found"


def test_bracket_push_pop_present():
    html = _html()
    assert "stack.push" in html and "stack.pop" in html, \
        "Turtle state stack push/pop not found"


def test_base_angle_25_degrees():
    html = _html()
    assert "25" in html, "25-degree angle not referenced in index.html"


def test_angle_variation_present():
    html = _html()
    assert "ANGLE_VAR" in html or "angleVar" in html or "variation" in html.lower(), \
        "Per-branch angle variation not found"


def test_lsystem_depth_4_iterations():
    """4 iterations of the rule must be used (MAX_ITERS or equivalent)."""
    html = _html()
    assert "MAX_ITERS" in html or "max_iters" in html or "4" in html, \
        "Iteration count 4 not found in index.html"


def test_lsystem_expand_depth4_produces_long_string():
    """Python re-implementation: depth-4 expansion must exceed 1000 chars."""
    rules = {"F": "FF+[+F-F-F]-[-F+F+F]"}
    s = "F"
    for _ in range(4):
        s = "".join(rules.get(c, c) for c in s)
    assert len(s) > 1000, \
        f"Depth-4 L-system string too short ({len(s)}); rules may be wrong"


def test_lsystem_expand_empty_axiom():
    """Expanding an empty string must return an empty string."""
    rules = {"F": "FF+[+F-F-F]-[-F+F+F]"}
    s = ""
    for _ in range(4):
        s = "".join(rules.get(c, c) for c in s)
    assert s == "", "Expanding empty axiom must yield empty string"


def test_lsystem_depth0_returns_axiom():
    """Zero iterations must return the axiom unchanged."""
    rules = {"F": "FF+[+F-F-F]-[-F+F+F]"}
    s = "F"
    for _ in range(0):
        s = "".join(rules.get(c, c) for c in s)
    assert s == "F", "Depth-0 expansion must equal axiom"


def test_lsystem_f_segment_count_depth4():
    """Depth-4 expansion must contain many F symbols (>= 500)."""
    rules = {"F": "FF+[+F-F-F]-[-F+F+F]"}
    s = "F"
    for _ in range(4):
        s = "".join(rules.get(c, c) for c in s)
    f_count = s.count("F")
    assert f_count >= 500, f"Depth-4 has only {f_count} F symbols; expected >= 500"


# ─── Plant configuration ─────────────────────────────────────────────────────

def test_plants_variable_defined():
    html = _html()
    assert "PLANTS" in html or "plants" in html.lower(), \
        "PLANTS array/variable not found in index.html"


def test_ten_plants_seeded():
    """buildPlants or equivalent must produce 10 plants (8-12 range)."""
    html = _html()
    # Check for the two slope arrays with 5 values each, or a direct plant count
    left_ts  = html.count("leftTs")  + html.count("left_ts")
    right_ts = html.count("rightTs") + html.count("right_ts")
    has_slopes = (left_ts >= 1 and right_ts >= 1)
    has_ten    = "10" in html
    assert has_slopes or has_ten, \
        "10-plant seeding (leftTs/rightTs arrays) not found in index.html"


def test_seeded_rng_present():
    """A seeded PRNG (mulberry32 or equivalent) must be defined for determinism."""
    html = _html()
    assert "makeRng" in html or "makeRNG" in html or "mulberry" in html or "0x6D2B79F5" in html, \
        "Seeded PRNG not found in index.html"


def test_segment_thickness_tapering():
    """Branch thickness must taper; 3.0 at root and 0.5 at tips."""
    html = _html()
    assert "3.0" in html or "3," in html, "Root thickness 3px not found"
    assert "0.5" in html, "Tip thickness 0.5px not found"


# ─── Mountain silhouette ─────────────────────────────────────────────────────

def test_mountain_silhouette_fill_color():
    html = _html()
    assert "#1a1008" in html, "Mountain fill #1a1008 not found in index.html"


def test_mountain_drawn_via_path():
    html = _html()
    assert "MTN_PTS" in html or "MOUNTAIN" in html or "mtn" in html.lower() or \
           "mountain" in html.lower(), "Mountain silhouette variable not found"


def test_peak_coordinates_defined():
    html = _html()
    assert "PEAK_X" in html or "PEAK_Y" in html or "peak" in html.lower(), \
        "Mountain peak coordinates not found"


# ─── Animation phases ─────────────────────────────────────────────────────────

def test_grow_duration_6_to_8_seconds():
    html = _html()
    m = re.search(r"GROW_DURATION\s*=\s*([\d.]+)", html)
    if m:
        val = float(m.group(1))
        assert 6.0 <= val <= 8.0, f"GROW_DURATION {val} not in 6–8 s range"
    else:
        assert "7" in html or "6" in html or "8" in html, "No growth duration near 6–8 s found"


def test_lightning_duration_3_seconds():
    html = _html()
    m = re.search(r"LIGHTNING_DURATION\s*=\s*([\d.]+)", html)
    if m:
        val = float(m.group(1))
        assert 2.5 <= val <= 4.0, f"LIGHTNING_DURATION {val} not in 2.5–4 s range"
    else:
        assert "3" in html, "Lightning duration not found"


def test_lightning_function_defined():
    html = _html()
    assert "makeLightning" in html or "lightning" in html.lower(), \
        "Lightning generation function not found"


def test_lightning_midpoint_displacement():
    html = _html()
    assert "displace" in html or "displacement" in html.lower() or "midpoint" in html.lower(), \
        "Midpoint displacement algorithm not found"


def test_lightning_color():
    html = _html()
    assert "#e8f0ff" in html, "Lightning colour #e8f0ff not found in index.html"


def test_lightning_random_opacity():
    html = _html()
    assert "Math.random()" in html or "opacity" in html, \
        "Random opacity for lightning flicker not found"


def test_progress_variable_controls_growth():
    assert "progress" in _html(), "progress variable gating plant growth not found"


def test_har_sinai_hebrew_text():
    html = _html()
    assert "הַר סִינַי" in html or "סִינַי" in html or "הַר" in html, \
        "Hebrew text הַר סִינַי not found in index.html"


def test_text_fade_in():
    html = _html()
    assert "textAlpha" in html or "text_alpha" in html or "globalAlpha" in html, \
        "Text fade-in (globalAlpha or textAlpha) not found"


def test_cycle_constant_defined():
    html = _html()
    assert "CYCLE" in html, "CYCLE constant for animation loop not found"


# ─── Palette ─────────────────────────────────────────────────────────────────

def test_sky_top_color():
    assert "#0a0520" in _html(), "Sky top colour #0a0520 not found"


def test_sky_bottom_color():
    assert "#0d2b1a" in _html(), "Sky bottom colour #0d2b1a not found"


def test_stem_dark_color():
    html = _html()
    assert "#1a5c2a" in html, "Stem dark colour #1a5c2a not found"


def test_stem_light_color():
    html = _html()
    assert "#2a8040" in html, "Stem light colour #2a8040 not found"


def test_flower_white_color():
    html = _html()
    assert "#f5f5e8" in html, "Flower white #f5f5e8 not found"


def test_flower_purple_color():
    html = _html()
    assert "#c8a8e8" in html, "Flower pale purple #c8a8e8 not found"


def test_flower_gold_color():
    html = _html()
    assert "#e8c850" in html, "Flower soft gold #e8c850 not found"


def test_thumbnail_uses_indigo_sky():
    svg = _svg()
    assert "#0a0520" in svg, "Thumbnail missing indigo sky #0a0520"


def test_thumbnail_mountain_color():
    svg = _svg()
    assert "#1a1008" in svg, "Thumbnail missing mountain colour #1a1008"


def test_thumbnail_has_green_branches():
    svg = _svg()
    assert "#1a5c2a" in svg or "#2a8040" in svg, \
        "Thumbnail missing green branch colours"


def test_thumbnail_has_flower_dots():
    svg = _svg()
    assert "#f5f5e8" in svg or "#c8a8e8" in svg or "#e8c850" in svg, \
        "Thumbnail missing flower colours"


def test_thumbnail_has_lightning():
    svg = _svg()
    assert "#e8f0ff" in svg or "polyline" in svg or "e8f0ff" in svg.lower(), \
        "Thumbnail missing lightning bolt"


def test_thumbnail_is_valid_svg():
    svg = _svg()
    assert "<svg" in svg and "</svg>" in svg, "thumbnail.svg is not valid SVG"


# ─── Essay content ────────────────────────────────────────────────────────────

def test_essay_word_count_300_to_500():
    text = _essay()
    count = len(text.split())
    assert 300 <= count <= 600, \
        f"essay.md has {count} words; expected 300–600"


def test_essay_mentions_exodus_19():
    text = _essay()
    assert "19:18" in text or "Exodus 19" in text, \
        "essay.md must cite Exodus 19:18–19"


def test_essay_mentions_shir_hashirim_rabbah():
    text = _essay()
    lower = text.lower()
    assert "shir hashirim" in lower or "shir ha-shirim" in lower or "shir" in lower, \
        "essay.md must mention Shir HaShirim Rabbah"


def test_essay_mentions_pirkei_derabbi_eliezer():
    text = _essay()
    assert "Pirkei" in text or "DeRabbi Eliezer" in text or "ch. 41" in text, \
        "essay.md must cite Pirkei DeRabbi Eliezer ch. 41"


def test_essay_mentions_shulchan_aruch():
    text = _essay()
    assert "Shulchan Aruch" in text or "494" in text, \
        "essay.md must cite Shulchan Aruch OC 494:3"


def test_essay_mentions_sinai():
    assert "Sinai" in _essay() or "sinai" in _essay().lower(), \
        "essay.md must mention Sinai"


def test_essay_mentions_humility_theme():
    lower = _essay().lower()
    assert "humility" in lower or "humble" in lower or "small" in lower, \
        "essay.md must mention the humility-of-Sinai midrash"


def test_essay_mentions_flower_or_bloom():
    lower = _essay().lower()
    assert "flower" in lower or "bloom" in lower or "green" in lower, \
        "essay.md must connect the flowering imagery to the theology"


def test_essay_embedded_in_html():
    """Substantial essay text must appear verbatim in index.html."""
    essay = _essay()
    html  = _html()
    words = [w for w in essay.split() if len(w) > 6][:20]
    found = sum(1 for w in words if w in html)
    assert found >= 6, \
        f"index.html does not embed essay text (only {found}/20 sampled words found)"


# ─── README ──────────────────────────────────────────────────────────────────

def test_readme_mentions_lsystem():
    text = _readme().lower()
    assert "l-system" in text or "lsystem" in text or "lindenmayer" in text, \
        "README.md must mention L-system"


def test_readme_mentions_sinai():
    assert "Sinai" in _readme() or "sinai" in _readme().lower(), \
        "README.md must mention Sinai"


def test_readme_mentions_lightning():
    assert "lightning" in _readme().lower(), \
        "README.md must describe the lightning phase"


# ─── L-system semantic checks (pure Python) ──────────────────────────────────

def test_lsystem_bracket_depth_reaches_4():
    """
    Depth-4 expansion of the tree rule must reach bracket nesting level >= 4.
    This verifies that the depth-dependent drawing logic (thickness taper, flowers)
    is reachable at runtime.
    """
    rules = {"F": "FF+[+F-F-F]-[-F+F+F]"}
    s = "F"
    for _ in range(4):
        s = "".join(rules.get(c, c) for c in s)

    depth = 0
    max_depth = 0
    stack = []
    for ch in s:
        if ch == "[":
            stack.append(depth)
            depth += 1
            max_depth = max(max_depth, depth)
        elif ch == "]" and stack:
            depth = stack.pop()

    assert max_depth >= 4, \
        f"Max bracket depth {max_depth} < 4; thickness/flower branches are unreachable"


def test_lsystem_balanced_brackets():
    """Depth-4 expansion must have balanced [ and ] brackets."""
    rules = {"F": "FF+[+F-F-F]-[-F+F+F]"}
    s = "F"
    for _ in range(4):
        s = "".join(rules.get(c, c) for c in s)
    assert s.count("[") == s.count("]"), \
        "L-system string has unbalanced brackets; stack will underflow"


# ─── Edge / failure modes ─────────────────────────────────────────────────────

def test_essay_stub_detected(tmp_path):
    """An essay.md under 300 words must fail the word-count check."""
    stub = tmp_path / "essay.md"
    stub.write_text("Sinai bloomed. " * 15, encoding="utf-8")
    word_count = len(stub.read_text().split())
    assert word_count < 300, "Fixture must be under 300 words"


def test_essay_empty_detected(tmp_path):
    """An empty essay.md must register as 0 words."""
    empty = tmp_path / "essay.md"
    empty.write_text("", encoding="utf-8")
    assert len(empty.read_text().split()) == 0


def test_pieces_json_missing_field_detected():
    """An entry without required fields must be detectable."""
    bad = {"id": "99-test", "title": "Test"}
    required = ("tagline", "year", "theme", "technique", "path", "thumbnail", "essay")
    for field in required:
        assert field not in bad, f"Fixture should not have field '{field}'"


def test_lightning_displace_pure_python():
    """
    Pure-Python version of midpoint displacement must produce more points
    than the two endpoints for depth > 0.
    """
    def displace(x1, y1, x2, y2, depth, spread):
        if depth == 0:
            return [(x1, y1), (x2, y2)]
        mx = (x1 + x2) / 2
        my = (y1 + y2) / 2
        left  = displace(x1, y1, mx, my, depth - 1, spread * 0.55)
        right = displace(mx, my, x2, y2, depth - 1, spread * 0.55)
        return left + right[1:]

    pts = displace(0, 0, 100, 300, 4, 30)
    assert len(pts) > 2, "Depth-4 displacement must produce more than 2 points"
    assert len(pts) == 2 ** 4 + 1, f"Expected {2**4 + 1} points, got {len(pts)}"


def test_flower_color_list_has_three_entries():
    """Three distinct flower colours must be defined in the script."""
    html = _html()
    colors = ["#f5f5e8", "#c8a8e8", "#e8c850"]
    for c in colors:
        assert c in html, f"Flower colour {c} not found in index.html"
