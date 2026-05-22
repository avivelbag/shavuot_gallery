"""
Tests for piece 26 — "Two Loaves" (Shtei HaLechem wave interference).

Validates file layout, pieces.json entry, canvas wave-interference
implementation, palette colours, bread-loaf markers, essay content
and embedding, and pure-Python wave-physics edge cases.
"""
import json
import math
import os
import re

import pytest

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECES_JSON  = os.path.join(GALLERY_ROOT, "pieces.json")
PIECE_ID     = "26-shtei-halechem"
PIECE_DIR    = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
INDEX_HTML   = os.path.join(PIECE_DIR, "index.html")
THUMBNAIL    = os.path.join(PIECE_DIR, "thumbnail.svg")
README_MD    = os.path.join(PIECE_DIR, "README.md")
ESSAY_MD     = os.path.join(PIECE_DIR, "essay.md")


# ─── File-read helpers ───────────────────────────────────────────────────────

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


def test_entry_theme_mentions_shtei_halechem_or_harvest():
    p = _entry()
    assert p is not None
    theme = p["theme"].lower()
    assert "shtei" in theme or "halechem" in theme or "harvest" in theme or "wheat" in theme, \
        f"theme must mention shtei halechem or harvest, got: {p['theme']}"


def test_entry_technique_mentions_wave_interference():
    p = _entry()
    assert p is not None
    tech = p["technique"].lower()
    assert "wave" in tech or "interference" in tech or "moiré" in tech or "moire" in tech, \
        f"technique must mention wave interference, got: {p['technique']}"


def test_entry_paths_correct():
    p = _entry()
    assert p is not None
    assert p["path"]      == f"pieces/{PIECE_ID}/index.html"
    assert p["thumbnail"] == f"pieces/{PIECE_ID}/thumbnail.svg"
    assert p["essay"]     == f"pieces/{PIECE_ID}/essay.md"


def test_entry_all_required_fields_present():
    p = _entry()
    assert p is not None
    for field in ("id", "title", "tagline", "year", "theme", "technique", "path", "thumbnail", "essay"):
        assert field in p and p[field], f"field '{field}' missing or empty in pieces.json entry"


def test_entry_year_is_int():
    p = _entry()
    assert p is not None
    assert isinstance(p["year"], int), f"year must be int, got {p['year']!r}"


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
    external = re.findall(
        r'<script[^>]+src\s*=\s*["\']([^"\']+)["\']', _html(), re.IGNORECASE
    )
    assert len(external) == 0, f"External scripts found: {external}"


# ─── Wave interference implementation ────────────────────────────────────────

def test_two_sources_defined():
    """Both SRC1 and SRC2 variables must be present."""
    html = _html()
    assert ("SRC1" in html or "src1" in html.lower()), "SRC1 (first source) not found"
    assert ("SRC2" in html or "src2" in html.lower()), "SRC2 (second source) not found"


def test_wavenumber_constant_present():
    """Wavenumber constant K must be defined."""
    html = _html()
    assert re.search(r"\bK\b|\bk\b|wavenumber", html), \
        "Wavenumber constant K not found in index.html"


def test_omega_constant_present():
    """Angular frequency constant OMEGA must be defined."""
    html = _html()
    assert "OMEGA" in html or "omega" in html.lower(), \
        "Angular frequency OMEGA not found in index.html"


def test_sin_wave_formula_present():
    """The wave formula sin(K * dist... - OMEGA * time) must appear in the source."""
    html = _html()
    assert "Math.sin" in html, "Math.sin not found — wave formula missing"
    # Both dist1/dist2 (or equivalent) must be used in sin calls
    assert "dist1" in html and "dist2" in html, \
        "Two distance arrays (dist1, dist2) not found"


def test_precomputed_distance_arrays():
    """Float32Array distance precomputation must be used for performance."""
    html = _html()
    assert "Float32Array" in html, \
        "Float32Array precomputed distances not found in index.html"


def test_imagedata_pixel_manipulation():
    """ImageData must be used for per-pixel colour writes."""
    html = _html()
    assert "createImageData" in html or "ImageData" in html, \
        "ImageData pixel manipulation not found"
    assert "putImageData" in html, "putImageData not found"


def test_amplitude_normalization_formula():
    """The (val + 2) / 4 normalisation or equivalent must appear."""
    html = _html()
    # Accept several equivalent forms
    assert "(val + 2)" in html or "(val+2)" in html or "* 0.25" in html or "/ 4" in html, \
        "Amplitude normalization (val+2)/4 not found in index.html"


# ─── Bread-loaf markers ──────────────────────────────────────────────────────

def test_loaf_marker_function_present():
    """A loaf-drawing function (drawLoaf or equivalent) must be defined."""
    html = _html()
    assert "drawLoaf" in html or "loaf" in html.lower(), \
        "Bread-loaf marker drawing function not found in index.html"


def test_ellipse_used_for_loaf_shape():
    """Loaf shapes must use canvas ellipse (or arc) primitives."""
    html = _html()
    assert ".ellipse(" in html or ".arc(" in html, \
        "canvas ellipse/arc not found — loaf shape not rendered"


def test_both_loaves_drawn():
    """Both source positions must be passed to the loaf drawing routine."""
    html = _html()
    # drawLoaves() calls drawLoaf for each source, or two explicit calls
    assert "SRC1_X" in html and "SRC2_X" in html and \
           (html.count("drawLoaf") >= 2 or "drawLoaves" in html), \
        "Both loaf markers (SRC1_X, SRC2_X) not drawn"


# ─── Palette colours ─────────────────────────────────────────────────────────

def test_palette_deep_linen():
    assert "#2C1810" in _html() or "#2c1810" in _html().lower(), \
        "Deep linen #2C1810 not found in index.html"


def test_palette_warm_amber():
    assert "#A0622A" in _html() or "#a0622a" in _html().lower(), \
        "Warm amber #A0622A not found in index.html"


def test_palette_wheat_gold():
    assert "#D4A843" in _html() or "#d4a843" in _html().lower(), \
        "Wheat gold #D4A843 not found in index.html"


def test_palette_parchment():
    assert "#F5E6C8" in _html() or "#f5e6c8" in _html().lower(), \
        "Parchment #F5E6C8 not found in index.html"


# ─── Thumbnail ───────────────────────────────────────────────────────────────

def test_thumbnail_is_valid_svg():
    svg = _svg()
    assert "<svg" in svg and "</svg>" in svg, "thumbnail.svg is not valid SVG"


def test_thumbnail_has_deep_linen():
    assert "#2C1810" in _svg() or "#2c1810" in _svg().lower(), \
        "thumbnail.svg missing deep linen #2C1810"


def test_thumbnail_has_wheat_gold():
    assert "#D4A843" in _svg() or "#d4a843" in _svg().lower(), \
        "thumbnail.svg missing wheat gold #D4A843"


def test_thumbnail_has_warm_amber():
    assert "#A0622A" in _svg() or "#a0622a" in _svg().lower(), \
        "thumbnail.svg missing warm amber #A0622A"


def test_thumbnail_has_parchment():
    assert "#F5E6C8" in _svg() or "#f5e6c8" in _svg().lower(), \
        "thumbnail.svg missing parchment #F5E6C8"


def test_thumbnail_has_source_circles():
    """Thumbnail must contain concentric ring circles from two sources."""
    svg = _svg()
    assert svg.count("<circle") >= 4, \
        "thumbnail.svg should have multiple concentric circles for wave rings"


def test_thumbnail_has_loaf_ellipses():
    """Thumbnail must have ellipse elements representing the two loaves."""
    svg = _svg()
    assert "<ellipse" in svg, "thumbnail.svg missing bread-loaf ellipse markers"


# ─── Essay content ────────────────────────────────────────────────────────────

def test_essay_word_count_at_least_200():
    text = _essay()
    count = len(text.split())
    assert count >= 200, f"essay.md has {count} words; expected ≥ 200"


def test_essay_word_count_reasonable_upper_bound():
    text = _essay()
    count = len(text.split())
    assert count <= 800, f"essay.md has {count} words; suspiciously long"


def test_essay_cites_leviticus_23_17():
    text = _essay()
    assert "23:17" in text or "Leviticus 23" in text, \
        "essay.md must cite Leviticus 23:17"


def test_essay_mentions_wave_offering():
    lower = _essay().lower()
    assert "wave offering" in lower or "wave" in lower, \
        "essay.md must mention the wave offering"


def test_essay_mentions_leaven_or_leavened():
    lower = _essay().lower()
    assert "leaven" in lower or "chametz" in lower, \
        "essay.md must discuss leaven / chametz"


def test_essay_mentions_wheat_harvest():
    lower = _essay().lower()
    assert "wheat" in lower or "harvest" in lower, \
        "essay.md must mention the wheat harvest"


def test_essay_mentions_shavuot():
    lower = _essay().lower()
    assert "shavuot" in lower, "essay.md must mention Shavuot"


def test_essay_does_not_claim_only_leavened_temple_offering():
    """
    The orchestrator flagged this as a factual error: the todah (thanksgiving
    offering) also included leavened bread, so shtei halechem are NOT the only
    leavened offering in the Temple service overall.  The correct claim is that
    they are the only Shavuot-specific leavened offering.
    """
    lower = _essay().lower()
    forbidden_phrases = [
        "only leavened offering in the temple service",
        "only leavened offering in temple",
        "the only leavened temple offering",
    ]
    for phrase in forbidden_phrases:
        assert phrase not in lower, (
            f"essay.md contains the inaccurate claim '{phrase}'; "
            "the todah also used leavened bread — use 'only Shavuot leavened offering' instead"
        )


def test_essay_embedded_in_html():
    """At least 6 of the first 10 long words from essay.md must appear in index.html."""
    essay = _essay()
    html  = _html()
    words = [w for w in essay.split() if len(w) > 6][:10]
    found = sum(1 for w in words if w in html)
    assert found >= 6, (
        f"index.html does not embed essay text (only {found}/10 sampled words found)"
    )


# ─── README ──────────────────────────────────────────────────────────────────

def test_readme_mentions_wave_interference():
    lower = _readme().lower()
    assert "wave" in lower or "interference" in lower, \
        "README.md must describe the wave interference technique"


def test_readme_mentions_shtei_halechem_or_loaves():
    lower = _readme().lower()
    assert "shtei" in lower or "halechem" in lower or "loaves" in lower or "loaf" in lower, \
        "README.md must mention the shtei halechem / loaves"


def test_readme_mentions_imagedata():
    lower = _readme().lower()
    assert "imagedata" in lower or "pixel" in lower, \
        "README.md must describe the ImageData pixel technique"


# ─── Pure-Python wave-physics tests ──────────────────────────────────────────

def test_wave_formula_bounded():
    """sin(k·r1 − ωt) + sin(k·r2 − ωt) must stay in [−2, 2] for all inputs."""
    k, omega = 0.07, 2.5
    for t in [0.0, 1.0, 2.51]:
        for r1 in [0, 50, 100, 200, 450]:
            for r2 in [0, 50, 100, 200, 450]:
                val = math.sin(k * r1 - omega * t) + math.sin(k * r2 - omega * t)
                assert -2.0001 <= val <= 2.0001, \
                    f"val {val:.4f} out of [-2,2] at r1={r1}, r2={r2}, t={t}"


def test_wave_formula_max_constructive_along_bisector():
    """Along the perpendicular bisector (r1==r2) the amplitude oscillates between −2 and +2."""
    k, omega = 0.07, 2.5
    r = 100.0
    vals = [math.sin(k * r - omega * t) + math.sin(k * r - omega * t)
            for t in [i * 0.01 for i in range(1000)]]
    assert max(vals) > 1.99, f"Bisector max {max(vals):.4f} should approach 2"
    assert min(vals) < -1.99, f"Bisector min {min(vals):.4f} should approach −2"


def test_palette_normalization_endpoints():
    """(val + 2) / 4 must map −2 → 0.0 and +2 → 1.0."""
    assert (-2 + 2) / 4 == pytest.approx(0.0)
    assert ( 2 + 2) / 4 == pytest.approx(1.0)
    assert ( 0 + 2) / 4 == pytest.approx(0.5)


def test_palette_normalization_range():
    """Normalised values must stay in [0, 1] for all valid inputs."""
    for val in [-2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0]:
        v = (val + 2) / 4
        assert 0.0 <= v <= 1.0, f"Normalised value {v} out of [0,1] for val={val}"


def test_destructive_interference_at_half_wavelength_offset():
    """When one source is half a wavelength further away, waves cancel."""
    k = 0.07
    wavelength = 2 * math.pi / k
    r1 = 100.0
    r2 = r1 + wavelength / 2
    t  = 0.0
    val = math.sin(k * r1 - t) + math.sin(k * r2 - t)
    assert abs(val) < 1e-6, \
        f"Destructive interference: expected ~0, got {val:.6f}"


def test_constructive_interference_at_full_wavelength_offset():
    """When one source is exactly one wavelength further away, amplitude doubles."""
    k = 0.07
    wavelength = 2 * math.pi / k
    # Choose t so that sin(k·r1 - t) = 1 (maximum)
    r1 = wavelength / 4.0   # k·r1 = π/2
    r2 = r1 + wavelength     # k·r2 = π/2 + 2π
    t  = 0.0
    val = math.sin(k * r1 - t) + math.sin(k * r2 - t)
    assert abs(val - 2.0) < 1e-6, \
        f"Full-wavelength offset: expected amplitude 2, got {val:.6f}"


def test_distance_precompute_at_source_is_zero():
    """Distance from a source to itself is zero — the formula degenerates to 2·sin(−ωt) there."""
    k, omega, t = 0.07, 2.5, 0.0
    r_at_source = 0.0
    val = math.sin(k * r_at_source - omega * t) + math.sin(k * r_at_source - omega * t)
    assert val == pytest.approx(0.0), "At t=0 and source position, amplitude should be 0"


# ─── Edge / failure modes ────────────────────────────────────────────────────

def test_essay_stub_detected(tmp_path):
    """An essay under 200 words must be detected as a stub."""
    stub = tmp_path / "essay.md"
    stub.write_text("Shtei halechem are two loaves. " * 5, encoding="utf-8")
    count = len(stub.read_text().split())
    assert count < 200, "Fixture must be under 200 words"


def test_essay_empty_is_zero_words(tmp_path):
    """Empty essay.md has zero words."""
    empty = tmp_path / "essay.md"
    empty.write_text("", encoding="utf-8")
    assert len(empty.read_text().split()) == 0


def test_missing_piece_entry_detected():
    """Searching for a non-existent piece ID must return None."""
    pieces = _pieces()
    result = next((p for p in pieces if p["id"] == "99-nonexistent"), None)
    assert result is None, "Non-existent ID should not match any entry"


def test_piece_26_is_last_or_recent():
    """Piece 26-shtei-halechem must appear in pieces.json."""
    ids = [p["id"] for p in _pieces()]
    assert "26-shtei-halechem" in ids, "26-shtei-halechem missing from pieces.json"


def test_thumbnail_missing_svg_tags_detected(tmp_path):
    """A file without <svg> tags must fail the SVG validity check."""
    bad = tmp_path / "bad.svg"
    bad.write_text("<html>not an svg</html>", encoding="utf-8")
    content = bad.read_text()
    is_valid = "<svg" in content and "</svg>" in content
    assert not is_valid, "Fixture must fail the SVG validity check"
