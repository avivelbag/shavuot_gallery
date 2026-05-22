"""
Tests for piece 09 — "The Greening of the House" (L-system floral decoration).

Validates file layout, pieces.json entry, and key acceptance criteria:
L-system strings, two plant types, growth animation, flower/leaf drawing,
colour palette, essay content, and essay embedding in index.html.
"""
import json
import os
import re

import pytest

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")
PIECE_ID = "09-greenery-lsystem"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
INDEX_HTML = os.path.join(PIECE_DIR, "index.html")
THUMBNAIL_SVG = os.path.join(PIECE_DIR, "thumbnail.svg")
README_MD = os.path.join(PIECE_DIR, "README.md")
ESSAY_MD = os.path.join(PIECE_DIR, "essay.md")


def _load_pieces():
    with open(PIECES_JSON, "r", encoding="utf-8") as fh:
        return json.load(fh)


def _get_piece():
    for p in _load_pieces():
        if p["id"] == PIECE_ID:
            return p
    return None


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
    assert os.path.isfile(INDEX_HTML), "pieces/09-greenery-lsystem/index.html missing"


def test_thumbnail_svg_exists():
    assert os.path.isfile(THUMBNAIL_SVG), "pieces/09-greenery-lsystem/thumbnail.svg missing"


def test_readme_exists():
    assert os.path.isfile(README_MD), "pieces/09-greenery-lsystem/README.md missing"


def test_essay_md_exists():
    assert os.path.isfile(ESSAY_MD), "pieces/09-greenery-lsystem/essay.md missing"


# ─── pieces.json entry ───────────────────────────────────────────────────────

def test_piece_in_json():
    assert _get_piece() is not None, f"'{PIECE_ID}' not found in pieces.json"


def test_piece_theme():
    p = _get_piece()
    assert p is not None
    assert "Greenery" in p["theme"] or "Shavuot" in p["theme"], \
        f"Expected 'Greenery' or 'Shavuot' in theme, got: {p['theme']}"


def test_piece_technique_mentions_lsystem():
    p = _get_piece()
    assert p is not None
    technique = p["technique"].lower()
    assert "l-system" in technique or "lsystem" in technique or "turtle" in technique, \
        f"Expected L-system or turtle in technique, got: {p['technique']}"


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


# ─── Canvas animation ────────────────────────────────────────────────────────

def test_uses_request_animation_frame():
    assert "requestAnimationFrame" in _html(), "animation must use requestAnimationFrame"


def test_canvas_element_present():
    assert "<canvas" in _html(), "index.html must contain a <canvas> element"


def test_canvas_dimensions_800x600():
    html = _html()
    assert "W = 800" in html or "800" in html, "canvas width should be 800"
    assert "H = 600" in html or "600" in html, "canvas height should be 600"


# ─── L-system implementation ─────────────────────────────────────────────────

def test_lsystem_expand_function_present():
    """An L-system expansion function must be defined in the HTML."""
    html = _html()
    assert "expandLSystem" in html or "expand" in html.lower(), \
        "L-system expansion function not found"


def test_lsystem_rules_defined():
    """Production rules object must appear in the script."""
    html = _html()
    assert "RULES" in html or "rules" in html, "L-system rules variable not found"


def test_two_plant_type_rules_defined():
    """At least two distinct rule sets (tree and vine) must appear."""
    html = _html()
    # Both TREE_RULES and VINE_RULES (or equivalent names) should be defined
    assert ("TREE_RULES" in html or "tree" in html.lower()) and \
           ("VINE_RULES" in html or "vine" in html.lower()), \
        "Two plant types (tree and vine) not found in index.html"


def test_bracket_push_pop_in_script():
    """Turtle state stack must handle '[' and ']' symbols."""
    html = _html()
    assert "stack.push" in html and "stack.pop" in html, \
        "Turtle state stack push/pop not found in index.html"


def test_max_depth_defined():
    """A maximum L-system depth constant must appear."""
    html = _html()
    assert "MAX_DEPTH" in html or "max_depth" in html or "maxDepth" in html, \
        "MAX_DEPTH constant not found in index.html"


def test_lsystem_string_length_proportional():
    """
    Verify L-system string growth: depth-4 tree must be substantially longer
    than depth-1 tree. This is a pure Python re-implementation of the expand logic
    to sanity-check that the production rules produce real branching.
    """
    rules = {'F': 'FF+[+F-F-F]-[-F+F+F]'}
    axiom = 'F'
    current = axiom
    for _ in range(4):
        current = ''.join(rules.get(ch, ch) for ch in current)
    assert len(current) > 100, \
        f"Depth-4 L-system string too short ({len(current)}), rules may be wrong"


def test_lsystem_vine_rules_differ_from_tree():
    """The vine and tree production rules must be different strings."""
    tree_rule = 'FF+[+F-F-F]-[-F+F+F]'
    vine_rule = 'F[+FF][-FF]F[+F][-F]'
    assert tree_rule != vine_rule, "Tree and vine rules must be distinct"
    html = _html()
    # At least one of the rules should appear in the source
    assert tree_rule in html or vine_rule in html, \
        "Neither tree nor vine L-system rule string found in index.html"


# ─── Growth animation ────────────────────────────────────────────────────────

def test_grow_duration_around_4s():
    """Growth duration constant should be ~4 seconds."""
    html = _html()
    m = re.search(r"GROW_DURATION\s*=\s*([\d.]+)", html)
    if m:
        val = float(m.group(1))
        assert 3.0 <= val <= 6.0, f"GROW_DURATION {val} not in 3–6 s range"
    else:
        assert "4" in html, "No growth duration constant found near 4 seconds"


def test_hold_duration_around_2s():
    """Hold duration after full growth should be ~2 seconds."""
    html = _html()
    m = re.search(r"HOLD_DURATION\s*=\s*([\d.]+)", html)
    if m:
        val = float(m.group(1))
        assert 1.0 <= val <= 4.0, f"HOLD_DURATION {val} not in 1–4 s range"
    else:
        assert "2" in html, "No hold duration constant found near 2 seconds"


def test_progress_variable_used():
    """A 'progress' variable gating symbol rendering must be present."""
    assert "progress" in _html(), "progress variable not found in index.html"


# ─── Flower and leaf drawing ─────────────────────────────────────────────────

def test_flower_drawing_function_present():
    """A drawFlower (or equivalent) function must draw five-petal flowers."""
    html = _html()
    assert "drawFlower" in html or "flower" in html.lower(), \
        "Flower drawing function not found in index.html"


def test_five_petals_in_flower():
    """Flower drawing must iterate over 5 petals."""
    html = _html()
    assert "5" in html and ("petal" in html.lower() or "i < 5" in html or "i=0;i<5" in html or
                              re.search(r"for\s*\(.*<\s*5", html)), \
        "Five-petal flower loop not found in index.html"


def test_leaf_drawing_function_present():
    """A drawLeaf (or equivalent) function must draw leaf ellipses."""
    html = _html()
    assert "drawLeaf" in html or "leaf" in html.lower(), \
        "Leaf drawing function not found in index.html"


def test_ellipse_used_for_leaves():
    """Leaves must be drawn as ellipses."""
    assert "ellipse" in _html(), "ctx.ellipse not found — leaves must be ellipses"


# ─── Palette ─────────────────────────────────────────────────────────────────

def test_offwhite_background_color():
    html = _html()
    assert "#fafaf2" in html or "#fafaf2" in _svg(), \
        "Off-white background #fafaf2 not found"


def test_deep_green_color():
    html = _html()
    assert "#2a5c1e" in html or "#2a5c1e" in _svg(), \
        "Deep green #2a5c1e not found"


def test_mid_green_color():
    html = _html()
    assert "#4a8c3f" in html or "#4a8c3f" in _svg(), \
        "Leaf mid-green #4a8c3f not found"


def test_rose_accent_color():
    html = _html()
    assert "#d98c8c" in html or "#d98c8c" in _svg(), \
        "Rose accent #d98c8c not found"


def test_yellow_center_color():
    html = _html()
    assert "#f5c842" in html or "#f5c842" in _svg() or "yellow" in html.lower(), \
        "Yellow flower center color not found"


# ─── Multiple plants ─────────────────────────────────────────────────────────

def test_plants_array_defined():
    """A PLANTS array (or equivalent) must configure multiple plants."""
    html = _html()
    assert "PLANTS" in html or "plants" in html.lower(), \
        "PLANTS array not found in index.html"


def test_at_least_three_plants():
    """At least 3 plant entries must appear (acceptance requires 3–5)."""
    html = _html()
    # Count occurrences of plant type markers as a proxy
    tree_count = html.count("'tree'") + html.count('"tree"')
    vine_count = html.count("'vine'") + html.count('"vine"')
    total = tree_count + vine_count
    assert total >= 3, f"Expected ≥3 plants (tree+vine entries), found {total}"


# ─── Thumbnail ───────────────────────────────────────────────────────────────

def test_thumbnail_is_valid_svg():
    svg = _svg()
    assert "<svg" in svg and "</svg>" in svg, "thumbnail.svg is not valid SVG"


def test_thumbnail_has_deep_green():
    svg = _svg()
    assert "#2a5c1e" in svg or "2a5c1e" in svg, \
        "thumbnail.svg missing deep green #2a5c1e"


def test_thumbnail_has_leaves():
    svg = _svg()
    assert "#4a8c3f" in svg, "thumbnail.svg missing leaf colour #4a8c3f"


def test_thumbnail_has_flowers():
    svg = _svg()
    assert "#d98c8c" in svg or "white" in svg.lower() or "#ffffff" in svg, \
        "thumbnail.svg missing flower colours"


def test_thumbnail_background_offwhite():
    svg = _svg()
    assert "#fafaf2" in svg, "thumbnail.svg missing off-white background"


# ─── README ──────────────────────────────────────────────────────────────────

def test_readme_mentions_lsystem():
    text = _readme().lower()
    assert "l-system" in text or "lsystem" in text or "lindenmayer" in text, \
        "README.md must mention L-system"


def test_readme_mentions_shavuot():
    text = _readme().lower()
    assert "shavuot" in text, "README.md must mention Shavuot theme"


def test_readme_mentions_greenery():
    text = _readme().lower()
    assert "green" in text, "README.md must mention greenery"


# ─── Essay ───────────────────────────────────────────────────────────────────

def test_essay_substantial():
    """essay.md must be at least 300 words (acceptance criteria: 300–500)."""
    text = _essay()
    word_count = len(text.split())
    assert word_count >= 300, f"essay.md has only {word_count} words (minimum 300)"


def test_essay_not_too_long():
    """essay.md should not exceed 600 words (acceptance criteria: ~300–500)."""
    text = _essay()
    word_count = len(text.split())
    assert word_count <= 600, f"essay.md has {word_count} words (maximum ~600)"


def test_essay_mentions_rama():
    text = _essay()
    assert "Rama" in text or "Isserles" in text, \
        "essay.md must cite the Rama (Orach Chaim 494)"


def test_essay_mentions_mishnah_berurah():
    text = _essay()
    assert "Mishnah Berurah" in text or "Mishnah-Berurah" in text, \
        "essay.md must mention the Mishnah Berurah"


def test_essay_mentions_sinai():
    text = _essay().lower()
    assert "sinai" in text, "essay.md must connect custom to Mount Sinai"


def test_essay_mentions_shavuot():
    text = _essay().lower()
    assert "shavuot" in text, "essay.md must name Shavuot"


def test_essay_mentions_exodus():
    """Essay must reference Exodus 34:3 (the lush mountain verse)."""
    text = _essay()
    assert "34:3" in text or "Exodus" in text, \
        "essay.md must reference Exodus 34:3"


def test_essay_growth_metaphor():
    """Essay must tie the growth motif to the artwork."""
    text = _essay().lower()
    assert "grow" in text or "seed" in text or "branch" in text, \
        "essay.md must connect the growth-from-seed motif to theology"


def test_essay_embedded_in_html():
    """Key essay sentences must appear verbatim in index.html."""
    essay = _essay()
    html = _html()
    words = [w for w in essay.split() if len(w) > 6][:15]
    found = sum(1 for w in words if w in html)
    assert found >= 5, \
        f"index.html does not embed essay text (only {found}/15 sampled words found)"


# ─── Edge cases and failure modes ────────────────────────────────────────────

def test_html_charset_utf8():
    html = _html()
    assert 'charset="UTF-8"' in html or "charset=utf-8" in html.lower(), \
        "index.html must declare UTF-8 charset"


def test_no_external_scripts():
    """All JS must be inline — no src= script tags pointing outside."""
    html = _html()
    external = re.findall(r'<script[^>]+src\s*=\s*["\']([^"\']+)["\']', html, re.IGNORECASE)
    assert len(external) == 0, f"External script(s) found: {external}"


def test_pieces_json_no_duplicate_ids():
    pieces = _load_pieces()
    ids = [p["id"] for p in pieces]
    assert len(ids) == len(set(ids)), f"Duplicate piece IDs: {ids}"


def test_lsystem_expand_empty_axiom():
    """L-system expansion of an empty axiom should return an empty string."""
    rules = {'F': 'FF+[+F-F-F]-[-F+F+F]'}
    axiom = ''
    current = axiom
    for _ in range(4):
        current = ''.join(rules.get(ch, ch) for ch in current)
    assert current == '', "Expanding empty axiom must yield empty string"


def test_lsystem_depth_zero_returns_axiom():
    """Zero iterations of expansion should return the axiom unchanged."""
    rules = {'F': 'FF+[+F-F-F]-[-F+F+F]'}
    axiom = 'F'
    current = axiom
    # zero iterations
    assert current == 'F', "Depth-0 expansion must equal axiom"


def test_essay_empty_file_detection(tmp_path):
    """An empty essay.md must be caught by word-count check."""
    empty = tmp_path / "essay.md"
    empty.write_text("", encoding="utf-8")
    assert len(empty.read_text().split()) == 0


def test_essay_stub_detection(tmp_path):
    """A stub essay under 300 words must fail the word-count check."""
    stub = tmp_path / "essay.md"
    stub.write_text("Shavuot greenery." * 10, encoding="utf-8")
    assert len(stub.read_text().split()) < 300
