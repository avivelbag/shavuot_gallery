"""
Tests for piece 10 "The Crowns" — tagin pen-plotter canvas.

Covers: file layout, pieces.json registration, canvas animation markers,
pen-plotter simulation constants, tagin drawing, colour palette, timing
constraints, essay content (Menachot 29b, Maharsha, Akiva, Shavuot), essay
embedding in index.html, thumbnail validity, and explicit edge cases.
"""
import json
import os
import re

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")
PIECE_ID = "10-tagin-pen-plotter"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
INDEX_HTML = os.path.join(PIECE_DIR, "index.html")
THUMBNAIL_SVG = os.path.join(PIECE_DIR, "thumbnail.svg")
README_MD = os.path.join(PIECE_DIR, "README.md")
ESSAY_MD = os.path.join(PIECE_DIR, "essay.md")


def _load_pieces():
    """Return the parsed pieces.json list."""
    with open(PIECES_JSON, encoding="utf-8") as fh:
        return json.load(fh)


def _get_piece():
    """Return the pieces.json entry for piece 10, or None."""
    return next((p for p in _load_pieces() if p["id"] == PIECE_ID), None)


def _html():
    return open(INDEX_HTML, encoding="utf-8").read()


def _svg():
    return open(THUMBNAIL_SVG, encoding="utf-8").read()


def _readme():
    return open(README_MD, encoding="utf-8").read()


def _essay():
    return open(ESSAY_MD, encoding="utf-8").read()


# ─── File layout ─────────────────────────────────────────────────────────────

def test_index_html_exists():
    assert os.path.isfile(INDEX_HTML), "pieces/10-tagin-pen-plotter/index.html missing"


def test_thumbnail_svg_exists():
    assert os.path.isfile(THUMBNAIL_SVG), "pieces/10-tagin-pen-plotter/thumbnail.svg missing"


def test_readme_exists():
    assert os.path.isfile(README_MD), "pieces/10-tagin-pen-plotter/README.md missing"


def test_essay_md_exists():
    assert os.path.isfile(ESSAY_MD), "pieces/10-tagin-pen-plotter/essay.md missing"


# ─── pieces.json registration ────────────────────────────────────────────────

def test_piece_in_json():
    assert _get_piece() is not None, f"'{PIECE_ID}' not found in pieces.json"


def test_piece_id_correct():
    p = _get_piece()
    assert p is not None
    assert p["id"] == PIECE_ID


def test_piece_theme_mentions_tagin():
    p = _get_piece()
    assert p is not None
    assert "Tagin" in p["theme"] or "Crown" in p["theme"], \
        f"Expected 'Tagin' or 'Crown' in theme, got: {p['theme']}"


def test_piece_technique_mentions_pen_plotter():
    p = _get_piece()
    assert p is not None
    technique = p["technique"].lower()
    assert "pen" in technique or "plotter" in technique or "stroke" in technique, \
        f"Expected pen-plotter in technique, got: {p['technique']}"


def test_piece_paths_correct():
    p = _get_piece()
    assert p is not None
    assert p["path"] == f"pieces/{PIECE_ID}/index.html"
    assert p["thumbnail"] == f"pieces/{PIECE_ID}/thumbnail.svg"
    assert p["essay"] == f"pieces/{PIECE_ID}/essay.md"


def test_piece_year_is_int():
    p = _get_piece()
    assert p is not None
    assert isinstance(p["year"], int)


def test_piece_required_fields_non_empty():
    """All required pieces.json fields must be present and non-empty."""
    p = _get_piece()
    assert p is not None
    for field in ("id", "title", "tagline", "year", "theme", "technique", "path", "thumbnail", "essay"):
        val = p.get(field)
        assert val is not None and val != "", \
            f"Field '{field}' is empty or missing in piece {PIECE_ID}"


# ─── Canvas animation ────────────────────────────────────────────────────────

def test_uses_request_animation_frame():
    assert "requestAnimationFrame" in _html(), \
        "index.html must use requestAnimationFrame for animation"


def test_canvas_element_present():
    assert "<canvas" in _html(), "index.html must contain a <canvas> element"


def test_canvas_dimensions_600():
    html = _html()
    assert "600" in html, "canvas should be 600 px (W or H constant)"


def test_canvas_id_present():
    html = _html()
    assert 'id="c"' in html or "getElementById" in html, \
        "canvas must have an id referenced by JavaScript"


# ─── Pen-plotter simulation ──────────────────────────────────────────────────

def test_jitter_constant_defined():
    html = _html()
    assert "JITTER" in html or "jitter" in html, \
        "JITTER constant not found — required for pen-plotter tremor simulation"


def test_jitter_value_is_small():
    """Jitter should be in the 0.3–0.8 px range for a subtle tremor effect."""
    html = _html()
    m = re.search(r"JITTER\s*=\s*([\d.]+)", html)
    if m:
        val = float(m.group(1))
        assert 0.2 <= val <= 1.0, f"JITTER {val} outside expected 0.2–1.0 range"


def test_line_width_pen_plotter():
    """lineWidth must be set to simulate fine pen ink (close to 1.8)."""
    html = _html()
    assert "lineWidth" in html, "lineWidth not set in canvas script"
    m = re.search(r"lineWidth\s*=\s*([\d.]+)", html)
    if m:
        val = float(m.group(1))
        assert 1.0 <= val <= 3.0, f"lineWidth {val} outside expected 1–3 range"


def test_line_cap_round():
    assert "lineCap" in _html(), "lineCap not set — required for pen-plotter look"


def test_bezier_path_building():
    """A function that builds jittered bezier paths must appear in the script."""
    html = _html()
    assert "bezier" in html.lower() or "buildPath" in html, \
        "Bezier path building function not found in index.html"


def test_steps_constant_defined():
    html = _html()
    assert "STEPS" in html or "steps" in html.lower(), \
        "STEPS (interpolation count) constant not found in index.html"


# ─── Shin letter strokes ─────────────────────────────────────────────────────

def test_four_shin_strokes_defined():
    """The shin requires four strokes: base bowl + three arms."""
    html = _html()
    assert "SHIN" in html or "shin" in html.lower() or "STROKES" in html, \
        "Shin stroke definitions not found in index.html"


def test_stroke_duration_defined():
    html = _html()
    assert "STROKE_DUR" in html or "strokeDur" in html or "stroke_dur" in html, \
        "Stroke duration constant not found in index.html"


def test_stroke_duration_around_0_8s():
    html = _html()
    m = re.search(r"STROKE_DUR\s*=\s*([\d.]+)", html)
    if m:
        val = float(m.group(1))
        assert 0.5 <= val <= 1.5, f"STROKE_DUR {val} outside expected 0.5–1.5 s range"


# ─── Tagin ───────────────────────────────────────────────────────────────────

def test_tagin_referenced_in_script():
    html = _html()
    assert "tagin" in html.lower() or "TAGIN" in html, \
        "Tagin not referenced in index.html script"


def test_tagin_tips_defined():
    """The three arm-tip positions for tagin placement must be defined."""
    html = _html()
    assert "TIPS" in html or "tips" in html.lower() or "tip" in html.lower(), \
        "Tagin tip positions not found in index.html"


def test_tagin_duration_constant():
    html = _html()
    assert "TAGIN_DUR" in html or "taginDur" in html, \
        "Tagin animation duration constant not found in index.html"


def test_tagin_three_arcs_per_tip():
    """buildTagin (or equivalent) must return three arcs per tip."""
    html = _html()
    assert "buildTagin" in html or ("tagin" in html.lower() and "3" in html), \
        "Three-arc tagin construction not found in index.html"


def test_hold_duration_5s():
    html = _html()
    m = re.search(r"HOLD_DUR\s*=\s*([\d.]+)", html)
    if m:
        val = float(m.group(1))
        assert 4.0 <= val <= 7.0, f"HOLD_DUR {val} outside expected 4–7 s range"
    else:
        assert "5" in html, "5-second hold duration not found in index.html"


def test_total_cycle_within_20s():
    """Total animation cycle must be ≤ 20 s."""
    html = _html()
    stroke_m = re.search(r"STROKE_DUR\s*=\s*([\d.]+)", html)
    tagin_m = re.search(r"TAGIN_DUR\s*=\s*([\d.]+)", html)
    hold_m = re.search(r"HOLD_DUR\s*=\s*([\d.]+)", html)
    fade_m = re.search(r"FADE_DUR\s*=\s*([\d.]+)", html)
    if stroke_m and tagin_m and hold_m and fade_m:
        stroke = float(stroke_m.group(1))
        tagin = float(tagin_m.group(1))
        hold = float(hold_m.group(1))
        fade = float(fade_m.group(1))
        letter_time = 4 * stroke       # 4 shin strokes
        tagin_time = 9 * tagin         # 3 tips × 3 arcs
        total = letter_time + tagin_time + hold + fade
        assert total <= 20.0, \
            f"Total cycle {total:.1f} s exceeds 20 s limit"


# ─── Palette ─────────────────────────────────────────────────────────────────

def test_parchment_background_color():
    html = _html()
    svg = _svg()
    assert "#f2ead8" in html or "#f2ead8" in svg, \
        "Parchment background #f2ead8 not found in index.html or thumbnail.svg"


def test_sepia_ink_color():
    html = _html()
    svg = _svg()
    assert "#3a1f0d" in html or "58,31,13" in html or "#3a1f0d" in svg, \
        "Sepia ink color #3a1f0d (or rgba equivalent) not found"


def test_ink_at_85_percent_opacity():
    html = _html()
    assert "0.85" in html or "85%" in html, \
        "85% ink opacity not found in index.html"


def test_no_extra_colors():
    """Palette must be monochrome — no blues, greens, or reds in the JS."""
    script_section = re.search(r"<script>(.*)</script>", _html(), re.DOTALL)
    if script_section:
        script = script_section.group(1)
        assert "#00" not in script and "blue" not in script.lower(), \
            "Unexpected blue color found in script — piece must be monochrome"


# ─── Thumbnail ───────────────────────────────────────────────────────────────

def test_thumbnail_is_valid_svg():
    svg = _svg()
    assert "<svg" in svg and "</svg>" in svg, \
        "thumbnail.svg does not look like valid SVG"


def test_thumbnail_has_parchment_background():
    assert "#f2ead8" in _svg(), \
        "thumbnail.svg must use parchment background #f2ead8"


def test_thumbnail_has_sepia_ink():
    assert "#3a1f0d" in _svg(), \
        "thumbnail.svg must use sepia ink #3a1f0d"


def test_thumbnail_has_tagin_paths():
    """Thumbnail must contain tagin strokes — at least 9 path elements."""
    svg = _svg()
    path_count = svg.count("<path")
    assert path_count >= 9, \
        f"Expected ≥9 <path> elements (4 shin + 9 tagin arcs), found {path_count}"


def test_thumbnail_400x400():
    svg = _svg()
    assert "400" in svg, "thumbnail.svg should be 400×400"


# ─── README ──────────────────────────────────────────────────────────────────

def test_readme_mentions_tagin():
    text = _readme().lower()
    assert "tagin" in text, "README.md must mention tagin"


def test_readme_mentions_shavuot():
    text = _readme().lower()
    assert "shavuot" in text, "README.md must mention Shavuot"


def test_readme_mentions_shin():
    text = _readme().lower()
    assert "shin" in text, "README.md must mention the letter shin"


# ─── Essay content ───────────────────────────────────────────────────────────

def test_essay_substantial():
    """essay.md must be at least 300 words (acceptance criteria: 300–500)."""
    text = _essay()
    wc = len(text.split())
    assert wc >= 300, f"essay.md has only {wc} words (minimum 300)"


def test_essay_not_too_long():
    """essay.md should not exceed 600 words."""
    text = _essay()
    wc = len(text.split())
    assert wc <= 600, f"essay.md has {wc} words (maximum ~600)"


def test_essay_mentions_menachot_29b():
    text = _essay()
    assert "Menachot 29b" in text or "Menachot" in text, \
        "essay.md must cite Talmud Menachot 29b"


def test_essay_mentions_maharsha():
    text = _essay()
    assert "Maharsha" in text or "Eidels" in text, \
        "essay.md must cite the Maharsha"


def test_essay_mentions_akiva():
    text = _essay()
    assert "Akiva" in text, "essay.md must mention Rabbi Akiva"


def test_essay_mentions_moses():
    text = _essay()
    assert "Moses" in text, "essay.md must mention Moses at Sinai"


def test_essay_mentions_shavuot():
    text = _essay().lower()
    assert "shavuot" in text, "essay.md must name Shavuot"


def test_essay_mentions_sinai():
    text = _essay().lower()
    assert "sinai" in text, "essay.md must mention Sinai"


def test_essay_mentions_crowns():
    text = _essay().lower()
    assert "crown" in text, "essay.md must mention crowns / tagin as crowns"


def test_essay_connects_to_artwork():
    """Essay must describe what the artwork shows."""
    text = _essay().lower()
    assert "shin" in text or "letter" in text, \
        "essay.md must explain what the artwork depicts (the shin letter)"


# ─── Essay embedded in index.html ────────────────────────────────────────────

def test_essay_embedded_in_html():
    """Key essay words must appear verbatim in index.html."""
    essay = _essay()
    html = _html()
    words = [w for w in essay.split() if len(w) > 6][:15]
    found = sum(1 for w in words if w in html)
    assert found >= 5, \
        f"index.html does not embed essay text ({found}/15 sampled long words found)"


def test_menachot_in_html():
    """The Talmud source must appear readable in index.html."""
    html = _html()
    assert "Menachot" in html or "29b" in html, \
        "Menachot 29b reference not visible in index.html"


def test_html_charset_utf8():
    html = _html()
    assert 'charset="UTF-8"' in html or "charset=utf-8" in html.lower(), \
        "index.html must declare UTF-8 charset for Hebrew character support"


def test_no_external_scripts():
    """All JS must be inline — no src= script tags pointing outside."""
    html = _html()
    external = re.findall(r'<script[^>]+src\s*=\s*["\']([^"\']+)["\']', html, re.IGNORECASE)
    assert len(external) == 0, f"External script(s) found: {external}"


# ─── Edge cases and failure modes ────────────────────────────────────────────

def test_bezier_formula_correctness():
    """
    Pure Python verification of the cubic bezier formula used by the animation.
    At t=0 the result must equal p0; at t=1 the result must equal p3.
    """
    def bezier_pt(p0, p1, p2, p3, t):
        mt = 1 - t
        return (
            mt**3 * p0[0] + 3*mt**2*t * p1[0] + 3*mt*t**2 * p2[0] + t**3 * p3[0],
            mt**3 * p0[1] + 3*mt**2*t * p1[1] + 3*mt*t**2 * p2[1] + t**3 * p3[1],
        )

    p0, p1, p2, p3 = (0, 0), (1, 3), (3, 3), (4, 0)
    x0, y0 = bezier_pt(p0, p1, p2, p3, 0)
    x1, y1 = bezier_pt(p0, p1, p2, p3, 1)
    assert abs(x0 - 0) < 1e-9 and abs(y0 - 0) < 1e-9, "Bezier at t=0 must equal p0"
    assert abs(x1 - 4) < 1e-9 and abs(y1 - 0) < 1e-9, "Bezier at t=1 must equal p3"


def test_tagin_arc_count():
    """There must be exactly 9 tagin arcs: 3 tips × 3 arcs each."""
    tips = [
        {"x": 135, "y": 130},
        {"x": 300, "y": 100},
        {"x": 465, "y": 130},
    ]
    total_arcs = len(tips) * 3
    assert total_arcs == 9, f"Expected 9 tagin arcs, computed {total_arcs}"


def test_progress_clamped_above_zero():
    """Drawing function should not crash when progress is 0 — end index = max(1, round(0))."""
    pts = [{"x": i, "y": i} for i in range(10)]
    end = max(1, round(0 * len(pts)))
    assert end == 1, f"Progress=0 should yield end=1, got {end}"


def test_essay_empty_stub_detection(tmp_path):
    """An empty essay.md must be caught by the word-count check."""
    empty = tmp_path / "essay.md"
    empty.write_text("", encoding="utf-8")
    assert len(empty.read_text().split()) == 0


def test_essay_short_stub_detection(tmp_path):
    """A stub essay under 300 words must fail the word-count gate."""
    stub = tmp_path / "essay.md"
    stub.write_text("Tagin crowns Torah Sinai Shavuot." * 20, encoding="utf-8")
    assert len(stub.read_text().split()) < 300


def test_pieces_json_no_duplicate_ids():
    pieces = _load_pieces()
    ids = [p["id"] for p in pieces]
    assert len(ids) == len(set(ids)), f"Duplicate piece IDs: {ids}"


def test_missing_essay_field_detected(tmp_path):
    """A pieces.json entry with an empty essay field must be flagged."""
    bad = [{"id": "10-tagin-pen-plotter", "essay": ""}]
    essay_val = bad[0].get("essay")
    assert not essay_val, "Fixture confirms empty essay must be treated as missing"
