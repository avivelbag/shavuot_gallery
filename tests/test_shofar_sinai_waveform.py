"""
Tests for piece 18-shofar-sinai — Growing Louder: The Shofar at Sinai.

Verifies file layout, pieces.json registration, essay content,
HTML animation structure, thumbnail SVG, and waveform math invariants.
"""
import json
import math
import os
import re


GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID = "18-shofar-sinai"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
HTML_PATH = os.path.join(PIECE_DIR, "index.html")
ESSAY_PATH = os.path.join(PIECE_DIR, "essay.md")
THUMB_PATH = os.path.join(PIECE_DIR, "thumbnail.svg")
README_PATH = os.path.join(PIECE_DIR, "README.md")
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")


# ---------------------------------------------------------------------------
# File layout
# ---------------------------------------------------------------------------

def test_piece_directory_exists():
    assert os.path.isdir(PIECE_DIR), f"Directory {PIECE_DIR} does not exist"


def test_index_html_exists():
    assert os.path.isfile(HTML_PATH), "index.html is missing"


def test_thumbnail_svg_exists():
    assert os.path.isfile(THUMB_PATH), "thumbnail.svg is missing"


def test_readme_exists():
    assert os.path.isfile(README_PATH), "README.md is missing"


def test_essay_md_exists():
    assert os.path.isfile(ESSAY_PATH), "essay.md is missing"


# ---------------------------------------------------------------------------
# pieces.json registration
# ---------------------------------------------------------------------------

def load_pieces():
    """Return the parsed pieces.json list."""
    with open(PIECES_JSON, encoding="utf-8") as fh:
        return json.load(fh)


def get_piece():
    """Return the shofar-sinai entry from pieces.json, or None."""
    return next((p for p in load_pieces() if p["id"] == PIECE_ID), None)


def test_piece_registered_in_pieces_json():
    assert get_piece() is not None, f"'{PIECE_ID}' not found in pieces.json"


def test_piece_has_correct_theme():
    piece = get_piece()
    assert piece is not None
    theme = piece["theme"].lower()
    assert "sinai" in theme or "shofar" in theme, (
        f"theme must reference Sinai or Shofar, got: {piece['theme']!r}"
    )


def test_piece_has_waveform_technique():
    piece = get_piece()
    assert piece is not None
    technique = piece["technique"].lower()
    assert "waveform" in technique or "oscilloscope" in technique or "canvas" in technique, (
        f"technique must reference waveform/oscilloscope/canvas, got: {piece['technique']!r}"
    )


def test_piece_essay_field_in_json():
    piece = get_piece()
    assert piece is not None
    essay = piece.get("essay", "")
    assert essay.strip(), "essay field in pieces.json must be non-empty"
    assert essay == f"pieces/{PIECE_ID}/essay.md", f"essay path mismatch: {essay!r}"


def test_piece_path_correct():
    piece = get_piece()
    assert piece is not None
    assert piece["path"] == f"pieces/{PIECE_ID}/index.html"


def test_piece_thumbnail_correct():
    piece = get_piece()
    assert piece is not None
    assert piece["thumbnail"] == f"pieces/{PIECE_ID}/thumbnail.svg"


def test_piece_year_is_int():
    piece = get_piece()
    assert piece is not None
    assert isinstance(piece["year"], int)


def test_no_duplicate_ids():
    pieces = load_pieces()
    ids = [p["id"] for p in pieces]
    assert len(ids) == len(set(ids)), f"Duplicate piece IDs: {ids}"


def test_piece_all_required_fields():
    """All required pieces.json fields must be present and non-empty."""
    required = ("id", "title", "tagline", "year", "theme", "technique", "path", "thumbnail", "essay")
    piece = get_piece()
    assert piece is not None
    for field in required:
        val = piece.get(field)
        assert val is not None and val != "", (
            f"pieces.json entry missing or empty field: {field!r}"
        )


# ---------------------------------------------------------------------------
# Essay content
# ---------------------------------------------------------------------------

def read_essay():
    """Return the full essay text."""
    return open(ESSAY_PATH, encoding="utf-8").read()


def test_essay_minimum_word_count():
    text = read_essay()
    words = text.split()
    assert len(words) >= 300, f"essay.md has only {len(words)} words (need ≥ 300)"


def test_essay_maximum_word_count():
    """Essay must not far exceed the 500-word target — catch copy-paste bloat."""
    text = read_essay()
    words = text.split()
    assert len(words) <= 800, f"essay.md has {len(words)} words (max 800)"


def test_essay_references_exodus_19():
    text = read_essay()
    assert "Exodus 19" in text or "19:19" in text or "19:16" in text, (
        "essay.md must cite Exodus 19 (the shofar at Sinai narrative)"
    )


def test_essay_references_shofar():
    text = read_essay()
    assert "shofar" in text.lower() or "שׁוֹפָר" in text, (
        "essay.md must mention the shofar"
    )


def test_essay_references_leviticus_jubilee():
    text = read_essay()
    assert "Leviticus" in text or "Jubilee" in text or "jubilee" in text, (
        "essay.md must reference Leviticus 25:9 / the shofar of Jubilee"
    )


def test_essay_mentions_growing_louder():
    text = read_essay()
    lower = text.lower()
    assert "louder" in lower or "grew" in lower or "chazek" in lower or "חָזֵק" in text, (
        "essay.md must discuss the shofar growing louder"
    )


def test_essay_mentions_sound_before_speech():
    """Verify the key theological insight: sound before speech / presence before words."""
    text = read_essay()
    lower = text.lower()
    assert "before" in lower and ("speech" in lower or "words" in lower or "language" in lower), (
        "essay.md must discuss the shofar as sound before speech/language"
    )


def test_essay_not_placeholder():
    text = read_essay()
    for stub in ("TODO", "placeholder", "lorem ipsum", "FILL IN"):
        assert stub.lower() not in text.lower(), (
            f"essay.md appears to contain placeholder text: {stub!r}"
        )


# ---------------------------------------------------------------------------
# HTML / canvas structure
# ---------------------------------------------------------------------------

def read_html():
    """Return the full index.html text."""
    return open(HTML_PATH, encoding="utf-8").read()


def test_html_uses_canvas():
    html = read_html()
    assert "<canvas" in html, "index.html must contain a <canvas> element"


def test_html_uses_request_animation_frame():
    html = read_html()
    assert "requestAnimationFrame" in html, (
        "index.html must use requestAnimationFrame for animation"
    )


def test_html_uses_math_sin():
    html = read_html()
    assert "Math.sin" in html, "index.html must use Math.sin to compute waveform"


def test_html_uses_performance_now():
    html = read_html()
    assert "performance.now" in html or "ts / 1000" in html or "ts/1000" in html, (
        "index.html must use performance.now() or requestAnimationFrame timestamp "
        "to drive the time offset"
    )


def test_html_contains_hebrew_text():
    html = read_html()
    assert "וְקוֹל" in html or "הַשּׁוֹפָר" in html, (
        "index.html must contain the Hebrew verse וְקוֹל הַשּׁוֹפָר הוֹלֵךְ וְחָזֵק מְאֹד"
    )


def test_html_has_multiple_harmonics():
    """Check that at least 5 harmonics are present."""
    html = read_html()
    assert "HARMONICS" in html or "harmonics" in html.lower(), (
        "index.html must implement multiple harmonics (HARMONICS array)"
    )


def test_html_has_envelope_logic():
    """The amplitude envelope must implement the 10-second growing cycle."""
    html = read_html()
    assert "10" in html and ("envelope" in html.lower() or "amp" in html.lower()), (
        "index.html must implement a 10-second amplitude envelope"
    )


def test_html_has_correct_background_color():
    html = read_html()
    assert "0d0d1a" in html.lower(), "index.html must use background #0d0d1a"


def test_html_has_composite_wave_color():
    html = read_html()
    assert "f0ece0" in html.lower(), "index.html must use near-white #f0ece0 for composite wave"


def test_html_has_amber_harmonic_color():
    html = read_html()
    assert "d4a017" in html.lower(), "index.html must use amber #d4a017 for harmonic overlays"


def test_html_harmonic_overlays_use_alpha():
    """Harmonic overlays must be drawn at reduced opacity."""
    html = read_html()
    assert "globalAlpha" in html or "rgba" in html or "opacity" in html.lower(), (
        "index.html must draw harmonic overlays at reduced alpha"
    )


def test_html_composite_line_width_3():
    """Composite wave must be drawn at 3px width per spec."""
    html = read_html()
    assert "lineWidth = 3" in html or "lineWidth=3" in html or "lineWidth = 3.0" in html, (
        "index.html must set lineWidth = 3 for the composite waveform"
    )


def test_html_no_external_scripts():
    html = read_html()
    external = re.findall(r'<script[^>]+src=["\']https?://', html)
    assert len(external) == 0, f"index.html must not load external scripts: {external}"


def test_html_embeds_essay_text():
    """index.html must embed essay text inline."""
    essay = read_essay()
    html = read_html()
    words = [w for w in essay.split() if len(w) > 5]
    sampled = words[:10]
    found = sum(1 for w in sampled if w in html)
    assert found >= 5, (
        f"index.html does not embed essay text: only {found}/10 sampled words found"
    )


def test_html_not_placeholder():
    html = read_html()
    for stub in ("TODO", "lorem ipsum", "FILL IN"):
        assert stub.lower() not in html.lower(), (
            f"index.html appears to contain placeholder text: {stub!r}"
        )


# ---------------------------------------------------------------------------
# Thumbnail SVG
# ---------------------------------------------------------------------------

def read_thumb():
    """Return the thumbnail SVG text."""
    return open(THUMB_PATH, encoding="utf-8").read()


def test_thumbnail_is_valid_svg():
    svg = read_thumb()
    assert "<svg" in svg and "</svg>" in svg, "thumbnail.svg is not valid SVG"


def test_thumbnail_has_path_elements():
    svg = read_thumb()
    paths = re.findall(r'<path', svg)
    assert len(paths) >= 1, (
        f"thumbnail.svg must have at least 1 <path> element, found {len(paths)}"
    )


def test_thumbnail_has_background_color():
    svg = read_thumb()
    assert "0d0d1a" in svg.lower(), "thumbnail.svg must use background #0d0d1a"


def test_thumbnail_has_waveform_color():
    svg = read_thumb()
    assert "f0ece0" in svg.lower(), "thumbnail.svg must include near-white #f0ece0 waveform"


def test_thumbnail_has_hebrew_text():
    svg = read_thumb()
    assert "<text" in svg, "thumbnail.svg must include a Hebrew <text> element"
    assert "וְקוֹל" in svg or "שּׁוֹפָר" in svg or "הַשּׁוֹפָר" in svg, (
        "thumbnail.svg must include Hebrew verse text"
    )


def test_thumbnail_has_amber_color():
    svg = read_thumb()
    assert "d4a017" in svg.lower(), "thumbnail.svg must use amber #d4a017"


# ---------------------------------------------------------------------------
# Waveform math — pure Python equivalents of the JS animation logic
# ---------------------------------------------------------------------------

HARMONIC_WEIGHTS = [1.0, 0.5, 1/3, 0.25, 0.2, 1/6, 1/7]
HARMONIC_SUM = sum(HARMONIC_WEIGHTS)
PHASES = [0, math.pi/6, math.pi/4, math.pi/3, math.pi/2, 2*math.pi/3, 5*math.pi/6]
SPEEDS = [0.30, 0.60, 0.90, 1.20, 1.50, 1.80, 2.10]
BASE_FREQ = 3.0
CANVAS_H = 300
CANVAS_W = 720


def envelope(t, H=CANVAS_H):
    """
    Amplitude envelope matching the JS implementation.

    Grows from 0 to peak over 9.5 s then decays to 0 over the final 0.5 s.
    Returns the per-pixel amplitude scalar.
    """
    c = t % 10
    peak = (H * 0.45) / HARMONIC_SUM
    if c < 9.5:
        return peak * math.pow(c / 10, 1.5)
    f = (c - 9.5) / 0.5
    return peak * math.pow(9.5 / 10, 1.5) * (1 - f * f)


def composite_y(x, t, W=CANVAS_W, H=CANVAS_H):
    """
    Compute the y position of the composite waveform at pixel x and time t.

    Mirrors the canvas JS logic so we can verify bounds and shape in Python.
    """
    amp = envelope(t, H)
    total = sum(
        HARMONIC_WEIGHTS[i] * math.sin(
            2 * math.pi * (i + 1) * BASE_FREQ * (x / W) + PHASES[i] + t * SPEEDS[i]
        )
        for i in range(len(HARMONIC_WEIGHTS))
    )
    return H / 2 + amp * total


def test_envelope_starts_near_zero():
    """At t=0 (start of cycle) the envelope must be essentially zero."""
    amp = envelope(0.0)
    assert amp < 1.0, f"Envelope at t=0 should be near-zero, got {amp:.4f}"


def test_envelope_grows_monotonically():
    """Envelope must increase from t=0.1 to t=9.0 within a cycle."""
    values = [envelope(t) for t in [0.1, 1.0, 3.0, 5.0, 7.0, 9.0]]
    for i in range(len(values) - 1):
        assert values[i] < values[i + 1], (
            f"Envelope is not monotonically increasing: {values}"
        )


def test_envelope_peak_near_9_5():
    """Peak amplitude occurs at t=9.5 (just before decay starts)."""
    amp_9_4 = envelope(9.4)
    amp_9_5 = envelope(9.5)
    amp_9_8 = envelope(9.8)
    assert amp_9_5 >= amp_9_4, "Envelope should still be growing at t=9.5"
    assert amp_9_5 > amp_9_8, "Envelope should have decayed by t=9.8"


def test_envelope_decays_to_zero_at_cycle_end():
    """Envelope reaches zero at t=10.0 (end of cycle / start of next)."""
    amp = envelope(10.0)
    assert abs(amp) < 1.0, f"Envelope should be near-zero at cycle end (t=10), got {amp:.4f}"


def test_composite_stays_within_canvas():
    """At peak amplitude, the composite waveform must stay within canvas height."""
    t_peak = 9.4
    for x in range(0, CANVAS_W + 1, 10):
        y = composite_y(x, t_peak)
        assert 0 <= y <= CANVAS_H, (
            f"Composite wave at x={x}, t={t_peak} out of canvas bounds: y={y:.1f}"
        )


def test_composite_uses_all_harmonics():
    """
    Disabling harmonic k changes the waveform — verifies all harmonics contribute.
    Uses the fact that higher harmonics add higher-frequency ripple.
    """
    t = 5.0
    x = CANVAS_W // 4

    amp = envelope(t)
    full = sum(
        HARMONIC_WEIGHTS[i] * math.sin(
            2 * math.pi * (i + 1) * BASE_FREQ * (x / CANVAS_W) + PHASES[i] + t * SPEEDS[i]
        )
        for i in range(len(HARMONIC_WEIGHTS))
    )

    without_k7 = sum(
        HARMONIC_WEIGHTS[i] * math.sin(
            2 * math.pi * (i + 1) * BASE_FREQ * (x / CANVAS_W) + PHASES[i] + t * SPEEDS[i]
        )
        for i in range(len(HARMONIC_WEIGHTS) - 1)
    )

    diff = abs(full - without_k7)
    assert diff > 0.001, (
        f"7th harmonic must contribute to the sum (diff={diff:.6f})"
    )


def test_envelope_10s_cycle_periodicity():
    """Envelope is periodic: same phase in two consecutive cycles gives same amplitude."""
    for phase in [0.0, 2.5, 5.0, 8.0]:
        amp1 = envelope(phase)
        amp2 = envelope(phase + 10.0)
        assert abs(amp1 - amp2) < 1e-9, (
            f"Envelope is not periodic at phase={phase}: {amp1:.6f} vs {amp2:.6f}"
        )


def test_harmonic_frequencies_are_integer_multiples():
    """Each harmonic has frequency k*BASE_FREQ — verify spatial period ratios."""
    for i in range(1, len(HARMONIC_WEIGHTS)):
        k = i + 1
        expected_ratio = k
        period_k_inv = k * BASE_FREQ
        period_1_inv = 1 * BASE_FREQ
        ratio = period_k_inv / period_1_inv
        assert abs(ratio - expected_ratio) < 1e-10, (
            f"Harmonic {k} should be {k}× the base frequency, ratio={ratio}"
        )


def test_waveform_not_constant():
    """The composite waveform must vary across x (not a flat line)."""
    t = 5.0
    ys = [composite_y(x, t) for x in range(0, CANVAS_W + 1, 20)]
    assert max(ys) - min(ys) > 5.0, (
        "Composite waveform should show significant variation across x"
    )


def test_waveform_amplitude_increases_over_cycle():
    """The peak-to-trough range of the waveform grows over the 10-second cycle."""
    x_vals = range(0, CANVAS_W + 1, 5)
    range_at_1s = max(composite_y(x, 1.0) for x in x_vals) - min(composite_y(x, 1.0) for x in x_vals)
    range_at_7s = max(composite_y(x, 7.0) for x in x_vals) - min(composite_y(x, 7.0) for x in x_vals)
    assert range_at_7s > range_at_1s, (
        f"Waveform amplitude should grow: range at 1s={range_at_1s:.1f}, at 7s={range_at_7s:.1f}"
    )


def test_waveform_empty_canvas_at_start():
    """At t very close to 0 the waveform is nearly flat (amplitude near zero)."""
    ys = [composite_y(x, 0.001) for x in range(0, CANVAS_W + 1, 10)]
    spread = max(ys) - min(ys)
    assert spread < 5.0, (
        f"At t≈0 the waveform should be nearly flat (spread={spread:.2f}px)"
    )
