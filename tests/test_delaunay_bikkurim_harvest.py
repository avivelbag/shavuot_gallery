"""
Tests for piece 61-delaunay-bikkurim-harvest — "First Fruits: Delaunay Harvest".

Verifies file layout, pieces.json registration, essay content (including
the verbatim Hebrew scripture blocks required by the orchestrator steering),
HTML structure, and the pure-Python Bowyer-Watson / triangle-color logic.
"""
import json
import math
import os
import re
import sys

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID = "61-delaunay-bikkurim-harvest"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
HTML_PATH = os.path.join(PIECE_DIR, "index.html")
ESSAY_PATH = os.path.join(PIECE_DIR, "essay.md")
THUMB_PATH = os.path.join(PIECE_DIR, "thumbnail.svg")
README_PATH = os.path.join(PIECE_DIR, "README.md")
GEN_TOOL = os.path.join(PIECE_DIR, "tools", "gen_thumbnail.py")
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


def test_gen_thumbnail_tool_exists():
    assert os.path.isfile(GEN_TOOL), f"tools/gen_thumbnail.py is missing at {GEN_TOOL}"


# ---------------------------------------------------------------------------
# pieces.json registration
# ---------------------------------------------------------------------------

def load_pieces():
    """Return the parsed pieces.json list."""
    with open(PIECES_JSON, encoding="utf-8") as fh:
        return json.load(fh)


def get_piece():
    """Return the delaunay-bikkurim-harvest entry from pieces.json, or None."""
    return next((p for p in load_pieces() if p["id"] == PIECE_ID), None)


def test_piece_registered_in_pieces_json():
    assert get_piece() is not None, f"'{PIECE_ID}' not found in pieces.json"


def test_piece_theme_is_bikkurim():
    piece = get_piece()
    assert piece is not None
    assert "bikkurim" in piece["theme"].lower(), (
        f"theme should reference Bikkurim, got: {piece['theme']!r}"
    )


def test_piece_technique_mentions_delaunay():
    piece = get_piece()
    assert piece is not None
    assert "delaunay" in piece["technique"].lower(), (
        f"technique must mention Delaunay, got: {piece['technique']!r}"
    )


def test_piece_technique_mentions_poisson():
    piece = get_piece()
    assert piece is not None
    assert "poisson" in piece["technique"].lower(), (
        f"technique must mention Poisson-disk, got: {piece['technique']!r}"
    )


def test_piece_essay_path_correct():
    piece = get_piece()
    assert piece is not None
    assert piece.get("essay") == f"pieces/{PIECE_ID}/essay.md"


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
    assert len(ids) == len(set(ids)), f"Duplicate piece IDs found: {ids}"


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
    return open(ESSAY_PATH, encoding="utf-8").read()


def test_essay_minimum_word_count():
    text = read_essay()
    words = text.split()
    assert len(words) >= 350, f"essay.md has only {len(words)} words (need ≥ 350)"


def test_essay_quotes_deuteronomy_8_8():
    text = read_essay()
    assert "Deuteronomy 8:8" in text or "8:8" in text, (
        "essay.md must cite Deuteronomy 8:8 (the seven species)"
    )


def test_essay_quotes_deuteronomy_26():
    text = read_essay()
    assert "Deuteronomy 26" in text, (
        "essay.md must cite Deuteronomy 26 (the first-fruits commandment)"
    )


def test_essay_contains_hebrew_seven_species():
    """essay.md must contain the Hebrew text of Deut 8:8 with nikud."""
    text = read_essay()
    # Key Hebrew words from Deut 8:8 with nikud
    assert "חִטָּה" in text or "חטה" in text, "essay.md must quote Hebrew seven-species verse"
    assert "שְׂעֹרָה" in text or "שעורה" in text, "essay.md must include barley in Hebrew"


def test_essay_contains_aramean_declaration():
    text = read_essay()
    assert "Aramean" in text or "aramean" in text.lower(), (
        "essay.md must quote 'A wandering Aramean was my father' (Deut 26:5)"
    )


def test_essay_contains_hebrew_aramean_verse():
    """essay.md must contain the Hebrew of Deut 26:5 with nikud."""
    text = read_essay()
    assert "אֲרַמִּי" in text, (
        "essay.md must include the Hebrew text of Deut 26:5 (אֲרַמִּי אֹבֵד אָבִי)"
    )


def test_essay_mentions_mishnah_bikkurim():
    text = read_essay()
    assert "Bikkurim" in text or "bikkurim" in text.lower(), (
        "essay.md must cite Mishnah Bikkurim"
    )


def test_essay_mentions_procession_details():
    text = read_essay()
    assert any(word in text.lower() for word in ("procession", "ox", "flute", "basket")), (
        "essay.md must describe the Bikkurim procession (ox, flute, baskets)"
    )


def test_essay_mentions_first_ripened_fruit_insight():
    text = read_essay()
    assert any(word in text.lower() for word in ("straw", "reed", "stalk", "tied", "marker", "marking")), (
        "essay.md must describe marking the first ripened fruit (the straw/reed marker)"
    )


def test_essay_connects_to_delaunay_artwork():
    text = read_essay()
    assert "delaunay" in text.lower() or "tessell" in text.lower() or "triangul" in text.lower(), (
        "essay.md must connect the artwork (Delaunay tessellation) to the theme"
    )


def test_essay_contains_english_translation_deut_8():
    text = read_essay()
    assert "wheat and barley" in text.lower(), (
        "essay.md must include English translation of Deut 8:8"
    )


def test_essay_contains_english_translation_deut_26():
    text = read_essay()
    assert "first of all the fruit" in text.lower() or "wandering aramean" in text.lower(), (
        "essay.md must include English translations of Deut 26 verses"
    )


def test_essay_not_placeholder():
    text = read_essay()
    for stub in ("TODO", "lorem ipsum", "FILL IN", "placeholder"):
        assert stub.lower() not in text.lower(), (
            f"essay.md contains placeholder text: {stub!r}"
        )


# ---------------------------------------------------------------------------
# HTML structure
# ---------------------------------------------------------------------------

def read_html():
    return open(HTML_PATH, encoding="utf-8").read()


def test_html_embeds_essay_text():
    """index.html must embed the essay inline — checks 10 long words."""
    essay = read_essay()
    html = read_html()
    words = [w for w in essay.split() if len(w) > 5][:10]
    found = sum(1 for w in words if w in html)
    assert found >= 5, (
        f"index.html does not embed the essay text: only {found}/10 sampled words found"
    )


def test_html_contains_svg_element():
    html = read_html()
    assert "createElementNS" in html or "<svg" in html, (
        "index.html must produce an SVG element"
    )


def test_html_contains_bowyer_watson():
    html = read_html()
    assert "bowyer" in html.lower() or "inCircumcircle" in html or "circumcircle" in html.lower(), (
        "index.html must implement Delaunay/Bowyer-Watson triangulation"
    )


def test_html_contains_poisson_disk():
    html = read_html()
    assert "poisson" in html.lower() or "effectiveMin" in html or "tooClose" in html, (
        "index.html must implement Poisson-disk sampling"
    )


def test_html_contains_seven_species_colors():
    html = read_html()
    assert "#D4A020" in html or "D4A020" in html.upper(), "wheat color #D4A020 missing"
    assert "#B8860B" in html or "B8860B" in html.upper(), "barley color #B8860B missing"
    assert "#6A2080" in html or "6A2080" in html.upper(), "grape color #6A2080 missing"
    assert "#4A6020" in html or "4A6020" in html.upper(), "olive color #4A6020 missing"


def test_html_contains_sky_color():
    html = read_html()
    assert "sky" in html.lower() or "SKY_FRAC" in html or "0x7E" in html or "7EB8" in html.upper(), (
        "index.html must handle the sky zone (upper 20%)"
    )


def test_html_contains_earth_color():
    html = read_html()
    assert "#8B4030" in html or "8B4030" in html.upper(), (
        "earth/path color #8B4030 must appear in index.html"
    )


def test_html_contains_hebrew_glyphs():
    html = read_html()
    assert "חִיטָּה" in html or "חִטָּה" in html or "חיטה" in html, (
        "index.html must contain Hebrew wheat glyph for the legend"
    )
    assert "שְׂעֹרָה" in html or "שעורה" in html, (
        "index.html must contain Hebrew barley glyph"
    )


def test_html_contains_scripture_blocks():
    """index.html must embed the Hebrew scripture blocks with nikud."""
    html = read_html()
    assert "אֲרַמִּי" in html, (
        "index.html must embed the Hebrew text of Deut 26:5 (Aramean declaration)"
    )
    assert "חִטָּה" in html, (
        "index.html must embed the Hebrew text of Deut 8:8 (seven species)"
    )


def test_html_has_fetrubulence_filter():
    html = read_html()
    assert "feTurbulence" in html or "feturbulence" in html.lower(), (
        "index.html must include feTurbulence parchment texture overlay"
    )


def test_html_no_external_scripts():
    html = read_html()
    external = re.findall(r'<script[^>]+src=["\']https?://', html)
    assert len(external) == 0, f"index.html must not load external scripts: {external}"


def test_html_not_placeholder():
    html = read_html()
    for stub in ("TODO", "lorem ipsum", "FILL IN"):
        assert stub.lower() not in html.lower(), (
            f"index.html contains placeholder text: {stub!r}"
        )


def test_html_responsive_layout():
    html = read_html()
    assert "max-width" in html or "flex-direction: column" in html, (
        "index.html must support responsive layout"
    )


# ---------------------------------------------------------------------------
# Thumbnail SVG
# ---------------------------------------------------------------------------

def read_thumb():
    return open(THUMB_PATH, encoding="utf-8").read()


def test_thumbnail_is_valid_svg():
    svg = read_thumb()
    assert "<svg" in svg and "</svg>" in svg, "thumbnail.svg is not valid SVG"


def test_thumbnail_has_many_polygons():
    """Delaunay thumbnail must have at least 50 <polygon> elements."""
    svg = read_thumb()
    polys = re.findall(r'<polygon', svg)
    assert len(polys) >= 50, (
        f"thumbnail.svg should have ≥50 <polygon> elements, found {len(polys)}"
    )


def test_thumbnail_uses_species_colors():
    svg = read_thumb()
    assert "D4A020" in svg.upper(), "thumbnail.svg must use wheat color #D4A020"
    assert "4A6020" in svg.upper(), "thumbnail.svg must use olive color #4A6020"


def test_thumbnail_has_horizon_line():
    svg = read_thumb()
    assert "<line" in svg, "thumbnail.svg must include the horizon separator line"


def test_thumbnail_dimensions_400():
    svg = read_thumb()
    assert 'width="400"' in svg, "thumbnail.svg must be 400px wide"
    assert 'height="400"' in svg, "thumbnail.svg must be 400px tall"


# ---------------------------------------------------------------------------
# Pure-Python algorithm unit tests
# ---------------------------------------------------------------------------

def _in_circumcircle(ax, ay, bx, by, cx, cy, px, py):
    """Python port of the orientation-independent circumcircle test from index.html."""
    d = ax - px
    e = ay - py
    f = bx - px
    g = by - py
    h = cx - px
    k = cy - py
    det = (d*d + e*e)*(f*k - h*g) - (f*f + g*g)*(d*k - h*e) + (h*h + k*k)*(d*g - f*e)
    cross = (bx - ax)*(cy - ay) - (cx - ax)*(by - ay)
    return cross * det > 0


def _tri_color(cx, cy, W=700, H=700, SKY_FRAC=0.20, EARTH_FRAC=0.92):
    """Python port of the triangle-color function from index.html."""
    SPECIES_COLORS = ['#D4A020', '#B8860B', '#6A2080', '#7A4010', '#A01828', '#4A6020', '#8B4513']
    if cy < H * SKY_FRAC:
        return 'sky'
    if cy > H * EARTH_FRAC:
        return '#8B4030'
    h = abs(math.sin(cx * 0.017 + cy * 0.031) * 7919) % 7
    return SPECIES_COLORS[int(h)]


def test_circumcircle_point_inside():
    """A point at the centroid of a triangle is inside its circumcircle."""
    ax, ay = 0.0, 0.0
    bx, by = 10.0, 0.0
    cx, cy = 5.0, 10.0
    px, py = 5.0, 3.0  # centroid-ish, definitely inside
    assert _in_circumcircle(ax, ay, bx, by, cx, cy, px, py)


def test_circumcircle_point_outside():
    """A far-away point is not inside the circumcircle."""
    ax, ay = 0.0, 0.0
    bx, by = 1.0, 0.0
    cx, cy = 0.5, 1.0
    px, py = 100.0, 100.0
    assert not _in_circumcircle(ax, ay, bx, by, cx, cy, px, py)


def test_circumcircle_equilateral_centre():
    """Centre of equilateral triangle must be inside circumcircle."""
    ax, ay = 0.0, 0.0
    bx, by = 2.0, 0.0
    cx, cy = 1.0, math.sqrt(3)
    px, py = 1.0, math.sqrt(3) / 3  # centroid
    assert _in_circumcircle(ax, ay, bx, by, cx, cy, px, py)


def test_tri_color_sky_zone():
    assert _tri_color(350, 50) == 'sky'


def test_tri_color_earth_zone():
    assert _tri_color(350, 660) == '#8B4030'


def test_tri_color_field_zone_returns_species_color():
    """Field-zone centroids must return one of the seven species colors."""
    SPECIES_COLORS = {'#D4A020', '#B8860B', '#6A2080', '#7A4010', '#A01828', '#4A6020', '#8B4513'}
    for cx in (100.0, 250.0, 400.0, 550.0):
        for cy in (200.0, 350.0, 500.0):
            color = _tri_color(cx, cy)
            assert color in SPECIES_COLORS, (
                f"centroid ({cx},{cy}) returned unexpected color {color!r}"
            )


def test_tri_color_deterministic():
    """Same centroid must always return the same color."""
    c1 = _tri_color(300.0, 400.0)
    c2 = _tri_color(300.0, 400.0)
    assert c1 == c2


def test_bowyer_watson_triangle_count():
    """After triangulating n points, result should have approximately 2n triangles."""
    # Import the gen_thumbnail module so we can reuse its Bowyer-Watson
    sys.path.insert(0, os.path.join(PIECE_DIR, "tools"))
    import gen_thumbnail as gt

    pts = [(float(i * 20), float(j * 20)) for i in range(6) for j in range(6)]
    tris = gt.bowyer_watson(pts)
    assert len(tris) > 0, "Bowyer-Watson returned no triangles"
    # Euler: for n interior points on grid, ~2n triangles (rough check)
    assert len(tris) >= len(pts), (
        f"Expected ≥{len(pts)} triangles for {len(pts)} points, got {len(tris)}"
    )


def test_bowyer_watson_all_indices_in_range():
    """All triangle indices must be valid indices into the original point list."""
    sys.path.insert(0, os.path.join(PIECE_DIR, "tools"))
    import gen_thumbnail as gt

    pts = [(float(i * 30), float(j * 30)) for i in range(5) for j in range(5)]
    tris = gt.bowyer_watson(pts)
    n = len(pts)
    for a, b, c in tris:
        for v in (a, b, c):
            assert 0 <= v < n, (
                f"Triangle index {v} is out of range [0, {n})"
            )


def test_bowyer_watson_no_super_triangle_vertices():
    """No triangle should reference super-triangle vertices (indices ≥ n)."""
    sys.path.insert(0, os.path.join(PIECE_DIR, "tools"))
    import gen_thumbnail as gt

    pts = [(float(i * 50), float(j * 50)) for i in range(4) for j in range(4)]
    tris = gt.bowyer_watson(pts)
    n = len(pts)
    for tri in tris:
        for v in tri:
            assert v < n, f"Super-triangle vertex index {v} leaked into output (n={n})"


def test_gen_thumbnail_generates_valid_svg(tmp_path, monkeypatch):
    """Running gen_thumbnail.py must produce a valid SVG file."""
    sys.path.insert(0, os.path.join(PIECE_DIR, "tools"))
    import gen_thumbnail as gt

    out_file = tmp_path / "thumbnail.svg"

    def patched_main():
        pts = gt.generate_points(gt.SEED)
        tris = gt.bowyer_watson(pts)
        svg = gt.build_svg(pts, tris)
        out_file.write_text(svg, encoding="utf-8")

    monkeypatch.setattr(gt, "main", patched_main)
    gt.main()

    content = out_file.read_text(encoding="utf-8")
    assert "<svg" in content and "</svg>" in content
    assert "<polygon" in content


def test_tri_color_boundary_conditions():
    """Test sky/field boundary: strictly less than SKY_FRAC goes to sky zone."""
    c_just_inside_sky = _tri_color(350.0, 700 * 0.20 - 1)
    c_at_or_past_sky = _tri_color(350.0, 700 * 0.20)
    assert c_just_inside_sky == 'sky', (
        "A point strictly above SKY_FRAC should be in the sky zone"
    )
    assert c_at_or_past_sky != 'sky', (
        "A point at exactly SKY_FRAC should be in the field zone"
    )


def test_darken_hex():
    """Test the darken function from gen_thumbnail."""
    sys.path.insert(0, os.path.join(PIECE_DIR, "tools"))
    import gen_thumbnail as gt

    dark = gt.darken("#D4A020", 0.20)
    assert dark.startswith("#")
    r = int(dark[1:3], 16)
    assert r < 0xD4, "darkened red channel should be less than original"
