"""
Tests for piece 15-keter-torah-harmonograph — Keter Torah (Crown of Torah).

Verifies file layout, pieces.json registration, essay content,
HTML structure, animation requirements, and harmonograph math.
"""
import json
import math
import os
import re


GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID = "15-keter-torah-harmonograph"
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
    """Return the keter-torah entry from pieces.json, or None."""
    return next((p for p in load_pieces() if p["id"] == PIECE_ID), None)


def test_piece_registered_in_pieces_json():
    assert get_piece() is not None, f"'{PIECE_ID}' not found in pieces.json"


def test_piece_has_correct_theme():
    piece = get_piece()
    assert piece is not None
    theme = piece["theme"].lower()
    assert "keter" in theme or "crown" in theme, (
        f"theme field should reference Keter/Crown, got: {piece['theme']!r}"
    )


def test_piece_has_harmonograph_technique():
    piece = get_piece()
    assert piece is not None
    technique = piece["technique"].lower()
    assert "harmonograph" in technique or "lissajous" in technique, (
        f"technique must mention harmonograph or lissajous, got: {piece['technique']!r}"
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


def test_essay_word_count():
    text = read_essay()
    words = text.split()
    assert len(words) >= 300, f"essay.md has only {len(words)} words (need ≥ 300)"


def test_essay_references_avot():
    text = read_essay()
    assert "Avot" in text or "avot" in text.lower(), (
        "essay.md must cite Mishnah Avot 4:13"
    )


def test_essay_references_menachot():
    text = read_essay()
    assert "Menachot" in text or "menachot" in text.lower(), (
        "essay.md must cite Talmud Menachot 29b (Moses and Rabbi Akiva / tagin)"
    )


def test_essay_mentions_naaseh_vnishma():
    text = read_essay()
    assert "naaseh" in text.lower() or "נעשה" in text, (
        "essay.md must mention naaseh v'nishma"
    )


def test_essay_mentions_tagin():
    text = read_essay()
    assert "tagin" in text.lower() or "crowns" in text.lower(), (
        "essay.md must discuss tagin (crowns on letters)"
    )


def test_essay_mentions_rabbi_akiva():
    text = read_essay()
    assert "Akiva" in text or "akiva" in text.lower(), (
        "essay.md must mention Rabbi Akiva (Menachot 29b)"
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


def test_html_contains_hebrew_title():
    html = read_html()
    assert "כֶּתֶר" in html or "כתר" in html, (
        "index.html must contain Hebrew text כֶּתֶר תּוֹרָה (Keter Torah)"
    )


def test_html_has_harmonograph_math():
    """Check that the harmonograph equations (sin + exp decay) are implemented."""
    html = read_html()
    assert "Math.sin" in html, "index.html must use Math.sin for harmonograph curves"
    assert "Math.exp" in html, "index.html must use Math.exp for pendulum decay"


def test_html_has_palette_colors():
    """Check that all four palette colors appear in the HTML."""
    html = read_html()
    assert "1a237e" in html.lower(), "index.html must use royal blue #1a237e"
    assert "c9a84c" in html.lower(), "index.html must use gold #c9a84c"
    assert "6a1b9a" in html.lower(), "index.html must use violet #6a1b9a"


def test_html_has_multiple_traces():
    """Check that at least 3 traces are used."""
    html = read_html()
    assert "NUM_TRACES" in html or "PALETTE" in html or "traces" in html, (
        "index.html must implement multiple harmonograph traces"
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


def test_html_has_hold_and_fade_phases():
    """Animation must hold after drawing and then fade before restart."""
    html = read_html()
    assert "holding" in html or "HOLD" in html, (
        "index.html must implement a hold phase after drawing completes"
    )
    assert "fading" in html or "FADE" in html, (
        "index.html must implement a fade phase before restart"
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


def test_thumbnail_has_harmonograph_paths():
    svg = read_thumb()
    paths = re.findall(r'<path', svg)
    assert len(paths) >= 3, (
        f"thumbnail.svg should have at least 3 <path> elements (multiple traces), "
        f"found {len(paths)}"
    )


def test_thumbnail_has_palette_color():
    svg = read_thumb()
    assert "1a237e" in svg.lower() or "c9a84c" in svg.lower(), (
        "thumbnail.svg must use the royal blue or gold palette color"
    )


def test_thumbnail_has_hebrew_text():
    svg = read_thumb()
    assert "<text" in svg, "thumbnail.svg must include Hebrew text element"


# ---------------------------------------------------------------------------
# Harmonograph math sanity checks (pure Python)
# ---------------------------------------------------------------------------

def harmonograph_point(t, phase_offset=0.0, d_variant=0.0):
    """
    Compute a single (x, y) point for the harmonograph at time t.

    Uses frequency ratios 3:2 / 2:3 as specified in the suggestion.
    Returns coordinates relative to a center at (0, 0).
    """
    f1x, f1y, f2x, f2y = 3, 2, 2, 3
    A1, A2 = 120, 100
    d1 = 0.002 + d_variant
    d2 = 0.0025 + d_variant
    phi1 = phase_offset
    phi2 = phase_offset + math.pi / 4
    decay1 = math.exp(-d1 * t)
    decay2 = math.exp(-d2 * t)
    x = A1 * math.sin(f1x * t + phi1) * decay1 + A2 * math.sin(f2x * t + phi2) * decay2
    y = A1 * math.sin(f1y * t + phi1 + math.pi / 6) * decay1 + A2 * math.sin(f2y * t + phi2 + math.pi / 3) * decay2
    return x, y


def test_harmonograph_decays_to_center():
    """At large t the curve must be very close to (0, 0) — pendulums have decayed."""
    x, y = harmonograph_point(t=5000)
    assert abs(x) < 0.05, f"Expected x ≈ 0 at t=5000, got {x}"
    assert abs(y) < 0.05, f"Expected y ≈ 0 at t=5000, got {y}"


def test_harmonograph_amplitude_at_start():
    """At t=0 the amplitude should be on the order of A1+A2 (max ~220)."""
    x, y = harmonograph_point(t=0)
    amplitude = math.hypot(x, y)
    assert amplitude > 10, (
        f"Harmonograph at t=0 should have significant amplitude, got {amplitude:.2f}"
    )


def test_harmonograph_four_phases_differ():
    """Four traces with phase offsets of π/6 must produce distinct starting points."""
    starts = [harmonograph_point(t=5.0, phase_offset=i * math.pi / 6) for i in range(4)]
    for i in range(len(starts)):
        for j in range(i + 1, len(starts)):
            dist = math.hypot(starts[i][0] - starts[j][0], starts[i][1] - starts[j][1])
            assert dist > 1.0, (
                f"Traces {i} and {j} start too close together (dist={dist:.3f}): "
                "phase offsets may not be applied"
            )


def test_harmonograph_stays_within_canvas():
    """All points (centered on 260,260 in a 520×520 canvas) must stay within bounds."""
    W, H = 520, 520
    cx, cy = W // 2, H // 2
    for i in range(1800):  # t from 0 to 900 in steps of 0.5
        t = i * 0.5
        x_rel, y_rel = harmonograph_point(t)
        x = cx + x_rel
        y = cy + y_rel
        assert 0 <= x <= W, f"Point at t={t} out of canvas (x={x:.1f})"
        assert 0 <= y <= H, f"Point at t={t} out of canvas (y={y:.1f})"


def test_harmonograph_damping_variant_changes_curve():
    """A non-zero d_variant must produce a measurably different curve than d_variant=0."""
    t = 50.0
    x0, y0 = harmonograph_point(t, d_variant=0.0)
    x1, y1 = harmonograph_point(t, d_variant=0.0005)
    dist = math.hypot(x0 - x1, y0 - y1)
    assert dist > 0.001, (
        f"Damping variant should change the curve but dist={dist:.6f}"
    )
