"""
Tests for piece 71 — Gosper Curve / Naaseh V'Nishma.

Covers the L-system logic (via gen_thumbnail.py helpers re-used in Python),
the on-disk file layout, pieces.json registration, thumbnail SVG correctness,
and edge/failure cases.
"""
import json
import math
import os
import re
import sys
import importlib.util

import pytest

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID = '71-gosper-curve-naaseh-vnishma'
PIECE_DIR = os.path.join(GALLERY_ROOT, 'pieces', PIECE_ID)
PIECES_JSON = os.path.join(GALLERY_ROOT, 'pieces.json')

# ── Load gen_thumbnail helpers by importing the module directly ────────────

def _load_gen_thumbnail():
    """Import gen_thumbnail.py from the piece directory as a module."""
    spec = importlib.util.spec_from_file_location(
        'gen_thumbnail_gosper',
        os.path.join(PIECE_DIR, 'gen_thumbnail.py'),
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope='module')
def gen():
    """Return the gen_thumbnail module (loaded once for the session)."""
    return _load_gen_thumbnail()


# ── File layout ────────────────────────────────────────────────────────────

def test_piece_directory_exists():
    assert os.path.isdir(PIECE_DIR), f'Missing piece directory: {PIECE_DIR}'


def test_index_html_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, 'index.html'))


def test_essay_md_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, 'essay.md'))


def test_thumbnail_svg_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, 'thumbnail.svg'))


def test_readme_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, 'README.md'))


def test_gen_thumbnail_py_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, 'gen_thumbnail.py'))


# ── pieces.json registration ───────────────────────────────────────────────

def _get_piece():
    with open(PIECES_JSON, 'r', encoding='utf-8') as fh:
        pieces = json.load(fh)
    for p in pieces:
        if p['id'] == PIECE_ID:
            return p
    return None


def test_piece_registered_in_pieces_json():
    assert _get_piece() is not None, f'{PIECE_ID} not found in pieces.json'


def test_piece_required_fields():
    piece = _get_piece()
    assert piece is not None
    required = ('id', 'title', 'tagline', 'year', 'theme', 'technique', 'path', 'thumbnail', 'essay')
    for field in required:
        assert field in piece and piece[field], f'Missing or empty field: {field}'


def test_piece_theme_mentions_naaseh():
    piece = _get_piece()
    assert piece is not None
    assert 'naaseh' in piece['theme'].lower() or 'nishma' in piece['theme'].lower(), (
        "theme field must mention naaseh or nishma"
    )


def test_piece_technique_mentions_gosper():
    piece = _get_piece()
    assert piece is not None
    assert 'gosper' in piece['technique'].lower(), (
        "technique field must mention Gosper curve"
    )


def test_piece_path_points_to_existing_html():
    piece = _get_piece()
    assert piece is not None
    full = os.path.join(GALLERY_ROOT, piece['path'])
    assert os.path.isfile(full), f"path '{piece['path']}' does not exist"


def test_piece_thumbnail_points_to_existing_file():
    piece = _get_piece()
    assert piece is not None
    full = os.path.join(GALLERY_ROOT, piece['thumbnail'])
    assert os.path.isfile(full), f"thumbnail '{piece['thumbnail']}' does not exist"


# ── essay.md content ───────────────────────────────────────────────────────

def test_essay_word_count():
    path = os.path.join(PIECE_DIR, 'essay.md')
    text = open(path, encoding='utf-8').read()
    count = len(text.split())
    assert count >= 360, f'Essay has only {count} words; need ≥ 360'


def test_essay_mentions_exodus():
    text = open(os.path.join(PIECE_DIR, 'essay.md'), encoding='utf-8').read()
    assert 'Exodus' in text, "Essay must cite Exodus 24:7"


def test_essay_mentions_naaseh():
    text = open(os.path.join(PIECE_DIR, 'essay.md'), encoding='utf-8').read()
    assert 'naaseh' in text.lower(), "Essay must discuss naaseh v'nishma"


def test_essay_mentions_shabbat_88a():
    text = open(os.path.join(PIECE_DIR, 'essay.md'), encoding='utf-8').read()
    assert 'Shabbat 88' in text or 'Shabbat 88a' in text, (
        "Essay must cite Talmud Shabbat 88a"
    )


def test_essay_mentions_gosper_or_flowsnake():
    text = open(os.path.join(PIECE_DIR, 'essay.md'), encoding='utf-8').read()
    lower = text.lower()
    assert 'gosper' in lower or 'flowsnake' in lower, (
        "Essay must mention the Gosper curve or flowsnake"
    )


# ── index.html content ─────────────────────────────────────────────────────

def test_html_has_canvas_700():
    html = open(os.path.join(PIECE_DIR, 'index.html'), encoding='utf-8').read()
    assert 'width="700"' in html and 'height="700"' in html, (
        "Canvas must be 700×700"
    )


def test_html_uses_requestanimationframe():
    html = open(os.path.join(PIECE_DIR, 'index.html'), encoding='utf-8').read()
    assert 'requestAnimationFrame' in html


def test_html_has_lsystem_rules():
    html = open(os.path.join(PIECE_DIR, 'index.html'), encoding='utf-8').read()
    assert 'A-B--B+A++AA+B-' in html, "HTML must contain the Gosper A→ rule"
    assert '+A-BB--B-A++A+B' in html, "HTML must contain the Gosper B→ rule"


def test_html_expands_to_level_4():
    html = open(os.path.join(PIECE_DIR, 'index.html'), encoding='utf-8').read()
    assert "expand('A', 4)" in html or 'expand("A", 4)' in html, (
        "HTML must expand the L-system to level 4"
    )


def test_html_embeds_essay_words():
    """index.html must embed the essay text inline."""
    essay = open(os.path.join(PIECE_DIR, 'essay.md'), encoding='utf-8').read()
    html = open(os.path.join(PIECE_DIR, 'index.html'), encoding='utf-8').read()
    long_words = [w for w in essay.split() if len(w) > 5][:10]
    found = sum(1 for w in long_words if w in html)
    assert found >= 5, (
        f"index.html embeds only {found}/10 sampled essay words — essay must be inline"
    )


def test_html_background_color():
    html = open(os.path.join(PIECE_DIR, 'index.html'), encoding='utf-8').read()
    assert '#050A14' in html, "Canvas background must be #050A14 (near-black deep night)"


def test_html_gold_trail_color():
    html = open(os.path.join(PIECE_DIR, 'index.html'), encoding='utf-8').read()
    assert '#C8A020' in html, "Trail color must include gold #C8A020"


def test_html_blue_trail_color():
    html = open(os.path.join(PIECE_DIR, 'index.html'), encoding='utf-8').read()
    assert '#1A3080' in html, "Trail tail color must include deep blue #1A3080"


def test_html_underlay_color():
    html = open(os.path.join(PIECE_DIR, 'index.html'), encoding='utf-8').read()
    assert '#2A3A5A' in html, "Static curve underlay must use #2A3A5A"


def test_html_dot_cream_color():
    html = open(os.path.join(PIECE_DIR, 'index.html'), encoding='utf-8').read()
    assert '#F0E8D0' in html, "Leading dot must be cream #F0E8D0"


def test_html_has_hebrew_text():
    html = open(os.path.join(PIECE_DIR, 'index.html'), encoding='utf-8').read()
    assert 'נַעֲשֶׂה' in html or 'נַעֲשֶׂה וְנִשְׁמָע' in html, (
        "HTML must contain the Hebrew text נַעֲשֶׂה וְנִשְׁמָע"
    )


# ── thumbnail.svg content ──────────────────────────────────────────────────

def test_thumbnail_is_valid_svg():
    text = open(os.path.join(PIECE_DIR, 'thumbnail.svg'), encoding='utf-8').read()
    assert '<svg' in text and '</svg>' in text


def test_thumbnail_has_path_element():
    text = open(os.path.join(PIECE_DIR, 'thumbnail.svg'), encoding='utf-8').read()
    assert '<path' in text, "thumbnail.svg must contain a <path> element"


def test_thumbnail_has_gold_stroke():
    text = open(os.path.join(PIECE_DIR, 'thumbnail.svg'), encoding='utf-8').read()
    assert '#C8A020' in text, "thumbnail.svg must use gold stroke #C8A020"


def test_thumbnail_has_deep_blue_background():
    text = open(os.path.join(PIECE_DIR, 'thumbnail.svg'), encoding='utf-8').read()
    assert '#0A1840' in text, "thumbnail.svg must have deep-blue background #0A1840"


def test_thumbnail_dimensions_400():
    text = open(os.path.join(PIECE_DIR, 'thumbnail.svg'), encoding='utf-8').read()
    assert 'width="400"' in text and 'height="400"' in text, (
        "thumbnail.svg must be 400×400"
    )


# ── L-system logic via gen_thumbnail helpers ───────────────────────────────

def test_expand_level_0_is_axiom(gen):
    assert gen.expand('A', 0) == 'A'


def test_expand_level_1_a_rule(gen):
    assert gen.expand('A', 1) == 'A-B--B+A++AA+B-'


def test_expand_level_1_b_rule(gen):
    """Expanding from B at level 1 should apply the B rule."""
    assert gen.expand('B', 1) == '+A-BB--B-A++A+B'


def test_expand_segment_count_level_3(gen):
    """Level-3 L-system must produce exactly 7^3 = 343 move characters."""
    s = gen.expand('A', 3)
    moves = sum(1 for c in s if c in ('A', 'B'))
    assert moves == 343, f"Expected 343 segments at level 3, got {moves}"


def test_expand_segment_count_level_4(gen):
    """Level-4 L-system must produce exactly 7^4 = 2401 move characters."""
    s = gen.expand('A', 4)
    moves = sum(1 for c in s if c in ('A', 'B'))
    assert moves == 2401, f"Expected 2401 segments at level 4, got {moves}"


def test_turtle_walk_produces_correct_point_count(gen):
    """Turtle walk of level-3 string must yield 344 points (343 segments + start)."""
    s = gen.expand('A', 3)
    pts = gen.turtle_walk(s)
    assert len(pts) == 344, f"Expected 344 points, got {len(pts)}"


def test_turtle_walk_level_4_point_count(gen):
    s = gen.expand('A', 4)
    pts = gen.turtle_walk(s)
    assert len(pts) == 2402, f"Expected 2402 points, got {len(pts)}"


def test_turtle_walk_unit_step_length(gen):
    """Each step in the turtle walk must have length 1.0 (within float tolerance)."""
    s = gen.expand('A', 2)
    pts = gen.turtle_walk(s)
    for i in range(1, len(pts)):
        dx = pts[i][0] - pts[i - 1][0]
        dy = pts[i][1] - pts[i - 1][1]
        length = math.hypot(dx, dy)
        assert abs(length - 1.0) < 1e-9, (
            f"Step {i} has length {length:.6f}, expected 1.0"
        )


def test_normalise_fits_within_bounds(gen):
    """Normalised points must all lie within [margin, W-margin] on both axes."""
    s = gen.expand('A', 3)
    pts = gen.turtle_walk(s)
    W, H, margin = 400, 400, 10
    scaled = gen.normalise(pts, W, H, margin)
    xs = [p[0] for p in scaled]
    ys = [p[1] for p in scaled]
    assert min(xs) >= margin - 1e-6
    assert max(xs) <= W - margin + 1e-6
    assert min(ys) >= margin - 1e-6
    assert max(ys) <= H - margin + 1e-6


def test_normalise_single_point_does_not_crash(gen):
    """Normalising a single-point list (span=0) must not raise ZeroDivisionError."""
    result = gen.normalise([(5.0, 5.0)], 400, 400, 10)
    assert len(result) == 1


def test_build_path_d_starts_with_M(gen):
    pts = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0)]
    d = gen.build_path_d(pts)
    assert d.startswith('M '), f"path d must start with 'M', got: {d[:10]}"


def test_build_path_d_segment_count(gen):
    """build_path_d of N points must contain N-1 'L' commands."""
    pts = [(float(i), 0.0) for i in range(5)]
    d = gen.build_path_d(pts)
    l_count = d.count(' L ')
    assert l_count == 4, f"Expected 4 L commands for 5 points, got {l_count}"


def test_expand_empty_axiom(gen):
    """Empty string expands to empty string at any depth."""
    assert gen.expand('', 4) == ''


def test_expand_non_rule_chars_passthrough(gen):
    """Characters outside the rule set must pass through unchanged."""
    result = gen.expand('+--+', 3)
    assert result == '+--+'


# ── README content ─────────────────────────────────────────────────────────

def test_readme_mentions_sinai_or_naaseh():
    text = open(os.path.join(PIECE_DIR, 'README.md'), encoding='utf-8').read().lower()
    assert 'naaseh' in text or 'sinai' in text or 'gosper' in text, (
        "README must mention the Shavuot theme or Gosper curve"
    )
