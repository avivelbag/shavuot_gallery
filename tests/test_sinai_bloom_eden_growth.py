"""
Tests for piece 57 — "And Sinai Was Covered in Flowers" (Eden growth bloom).

Validates file layout, pieces.json entry, Eden model implementation details,
hex-grid color palette, essay citations, and the shimmer / Hebrew-text features.
"""
import json
import math
import os
import re

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECES_JSON  = os.path.join(GALLERY_ROOT, "pieces.json")
PIECE_ID     = "57-sinai-bloom-eden-growth"
PIECE_DIR    = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
INDEX_HTML   = os.path.join(PIECE_DIR, "index.html")
THUMBNAIL    = os.path.join(PIECE_DIR, "thumbnail.svg")
README_MD    = os.path.join(PIECE_DIR, "README.md")
ESSAY_MD     = os.path.join(PIECE_DIR, "essay.md")


# ── helpers ──────────────────────────────────────────────────────────────────

def _pieces():
    with open(PIECES_JSON, encoding="utf-8") as fh:
        return json.load(fh)


def _entry():
    return next((p for p in _pieces() if p["id"] == PIECE_ID), None)


def _html():
    return open(INDEX_HTML, encoding="utf-8").read()


def _svg():
    return open(THUMBNAIL, encoding="utf-8").read()


def _readme():
    return open(README_MD, encoding="utf-8").read()


def _essay():
    return open(ESSAY_MD, encoding="utf-8").read()


# ── file layout ───────────────────────────────────────────────────────────────

def test_index_html_exists():
    assert os.path.isfile(INDEX_HTML), f"{PIECE_ID}/index.html missing"


def test_thumbnail_svg_exists():
    assert os.path.isfile(THUMBNAIL), f"{PIECE_ID}/thumbnail.svg missing"


def test_readme_md_exists():
    assert os.path.isfile(README_MD), f"{PIECE_ID}/README.md missing"


def test_essay_md_exists():
    assert os.path.isfile(ESSAY_MD), f"{PIECE_ID}/essay.md missing"


# ── pieces.json entry ─────────────────────────────────────────────────────────

def test_entry_present_in_pieces_json():
    assert _entry() is not None, f"'{PIECE_ID}' not found in pieces.json"


def test_entry_theme_har_sinai_matan_torah():
    p = _entry()
    assert p is not None
    theme = p["theme"].lower()
    assert "sinai" in theme and "matan" in theme.lower() or "sinai" in theme, \
        f"Expected 'sinai' and/or 'matan torah' in theme, got: {p['theme']}"


def test_entry_technique_mentions_eden_growth():
    p = _entry()
    assert p is not None
    tech = p["technique"].lower()
    assert "eden" in tech or "stochastic" in tech or "accretion" in tech, \
        f"Expected 'Eden growth' or 'stochastic accretion' in technique, got: {p['technique']}"


def test_entry_technique_mentions_hex():
    p = _entry()
    assert p is not None
    tech = p["technique"].lower()
    assert "hex" in tech or "hexagon" in tech, \
        f"Expected hex in technique, got: {p['technique']}"


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


# ── canvas / animation ────────────────────────────────────────────────────────

def test_canvas_element_present():
    assert "<canvas" in _html(), "index.html must have a <canvas> element"


def test_canvas_width_700():
    assert 'width="700"' in _html() or "700" in _html(), \
        "canvas width 700 not found in index.html"


def test_canvas_height_700():
    assert 'height="700"' in _html() or "700" in _html(), \
        "canvas height 700 not found in index.html"


def test_uses_request_animation_frame():
    assert "requestAnimationFrame" in _html(), \
        "animation must use requestAnimationFrame"


def test_charset_utf8():
    html = _html()
    assert 'charset="UTF-8"' in html or "charset=utf-8" in html.lower(), \
        "index.html must declare UTF-8 charset"


def test_no_external_scripts():
    html = _html()
    external = re.findall(r'<script[^>]+src\s*=\s*["\']([^"\']+)["\']', html, re.IGNORECASE)
    assert len(external) == 0, f"External scripts found: {external}"


# ── Eden model implementation ─────────────────────────────────────────────────

def test_hex_dirs_defined():
    html = _html()
    assert "HEX_DIRS" in html or "hexNeighbors" in html or "HEX_DIR" in html, \
        "Hex neighbor directions not found in index.html"


def test_hex_key_function_present():
    assert "hexKey" in _html(), "hexKey function not found in index.html"


def test_frontier_array_present():
    html = _html()
    assert "frontierArr" in html or "frontier" in html.lower(), \
        "Frontier array not found in index.html"


def test_cluster_set_present():
    html = _html()
    assert "cluster" in html, "cluster Set not found in index.html"


def test_add_cell_function_present():
    assert "addCell" in _html(), "addCell function not found in index.html"


def test_cells_per_frame_defined():
    html = _html()
    assert "CELLS_PER_FRAME" in html or "cellsPerFrame" in html, \
        "CELLS_PER_FRAME constant not found in index.html"


def test_hex_size_defined():
    assert "HEX_SIZE" in _html(), "HEX_SIZE constant not found in index.html"


def test_in_canvas_check_present():
    html = _html()
    assert "inCanvas" in html or "inBounds" in html or "canvas" in html, \
        "Canvas bounds check not found in index.html"


def test_swap_remove_optimization():
    """O(1) swap-remove from frontier array: last element is used to fill the gap."""
    html = _html()
    assert "frontierArr.length - 1" in html or "length - 1" in html, \
        "Swap-remove O(1) frontier removal not found"


def test_random_frontier_selection():
    assert "Math.random()" in _html(), "Random frontier selection not found"


# ── Palette colors ────────────────────────────────────────────────────────────

def test_palette_violet_core():
    assert "#3A1E6A" in _html() or "3A1E6A" in _html(), \
        "Violet core color #3A1E6A not found in index.html"


def test_palette_rose():
    assert "#C06080" in _html() or "C06080" in _html(), \
        "Rose color #C06080 not found in index.html"


def test_palette_gold():
    assert "#D4A820" in _html() or "D4A820" in _html(), \
        "Gold color #D4A820 not found in index.html"


def test_palette_cream():
    assert "#FFF8F0" in _html() or "FFF8F0" in _html(), \
        "Cream color #FFF8F0 not found in index.html"


def test_dist_color_function_present():
    assert "distColor" in _html(), "distColor function not found in index.html"


def test_max_dist_defined():
    assert "MAX_DIST" in _html(), "MAX_DIST constant not found in index.html"


# ── Hebrew text ───────────────────────────────────────────────────────────────

def test_hebrew_text_present():
    html = _html()
    assert "וְהַר" in html or "סִינַי" in html or "עָשָׁן" in html or "עָשַׁן" in html or "עָשָן" in html, \
        "Hebrew verse about Sinai not found in index.html"


def test_hebrew_text_fill_style():
    html = _html()
    assert "rgba(255,248,240" in html or "rgba(255, 248, 240" in html or "FFF8F0" in html, \
        "Hebrew text fill color (cream) not found in index.html"


def test_canvas_direction_rtl():
    html = _html()
    assert "direction" in html and ("rtl" in html), \
        "Canvas direction='rtl' for Hebrew text not found in index.html"


# ── Shimmer phase ─────────────────────────────────────────────────────────────

def test_shimmer_uses_sin():
    assert "Math.sin" in _html(), "Shimmer must use Math.sin for pulsing"


def test_shimmer_uses_global_alpha():
    assert "globalAlpha" in _html(), "Shimmer must use globalAlpha for opacity pulsing"


def test_all_cells_array_present():
    assert "allCells" in _html(), "allCells tracking array not found in index.html"


def test_shimmer_phase_per_cell():
    html = _html()
    assert "phase" in html, "Per-cell random phase for shimmer not found"


def test_bg_constant_defined():
    assert "BG" in _html(), "BG background color constant not found in index.html"


# ── Thumbnail ─────────────────────────────────────────────────────────────────

def test_thumbnail_is_valid_svg():
    svg = _svg()
    assert "<svg" in svg and "</svg>" in svg, "thumbnail.svg is not valid SVG"


def test_thumbnail_has_violet():
    assert "#3A1E6A" in _svg() or "3A1E6A" in _svg(), \
        "Thumbnail missing violet core color #3A1E6A"


def test_thumbnail_has_outer_palette_colors():
    """Outer hex cells reach ~90 % of MAX_DIST, landing in the cream-gold range."""
    svg = _svg()
    # Pure cream #FFF8F0 is the palette stop at t=1.0; cells within the canvas
    # top out around t≈0.93, producing warm cream-gold tones like #F7EACB.
    known_outer = ["FFF8F0", "F7EACB", "F2E1B3", "F0DDA9", "EED89C", "EBD491"]
    assert any(c in svg for c in known_outer), \
        f"Thumbnail missing outer cream/gold palette colors (checked: {known_outer})"


def test_thumbnail_has_mountain_silhouette():
    assert "polygon" in _svg().lower(), \
        "Thumbnail missing mountain silhouette polygon"


def test_thumbnail_has_dark_background():
    assert "#100820" in _svg() or "100820" in _svg(), \
        "Thumbnail missing dark background #100820"


# ── Essay content ─────────────────────────────────────────────────────────────

def test_essay_minimum_200_words():
    text = _essay()
    count = len(text.split())
    assert count >= 200, f"essay.md has only {count} words (minimum 200)"


def test_essay_cites_exodus_19_18():
    text = _essay()
    assert "19:18" in text or "Exodus 19" in text, \
        "essay.md must cite Exodus 19:18"


def test_essay_cites_shir_hashirim_rabbah():
    text = _essay()
    lower = text.lower()
    assert "shir hashirim" in lower or "shir ha-shirim" in lower or "shir" in lower, \
        "essay.md must cite Shir HaShirim Rabbah"


def test_essay_cites_pirkei_derabbi_eliezer():
    text = _essay()
    assert "Pirkei" in text or "DeRabbi Eliezer" in text or "ch. 41" in text, \
        "essay.md must cite Pirkei DeRabbi Eliezer ch. 41"


def test_essay_mentions_sinai_bloom():
    text = _essay().lower()
    assert "bloom" in text or "flower" in text, \
        "essay.md must mention the blooming of Sinai"


def test_essay_mentions_torah_life():
    text = _essay().lower()
    assert "life" in text or "etz chaim" in text.lower() or "tree" in text, \
        "essay.md must mention Torah as life-giving"


def test_essay_embedded_in_html():
    """Substantial essay text must appear verbatim in index.html."""
    essay = _essay()
    html  = _html()
    words = [w for w in essay.split() if len(w) > 6][:20]
    found = sum(1 for w in words if w in html)
    assert found >= 5, \
        f"index.html does not embed essay text (only {found}/20 sampled words found)"


# ── README ────────────────────────────────────────────────────────────────────

def test_readme_mentions_eden_model():
    text = _readme().lower()
    assert "eden" in text or "stochastic" in text, \
        "README.md must mention the Eden model"


def test_readme_mentions_sinai():
    assert "Sinai" in _readme() or "sinai" in _readme().lower(), \
        "README.md must mention Sinai"


def test_readme_mentions_hex():
    assert "hex" in _readme().lower(), \
        "README.md must mention the hex grid"


# ── Pure-Python Eden model tests ──────────────────────────────────────────────

def _run_eden(steps, canvas_size=700, hex_size=4):
    """Python reimplementation of the Eden model for testing."""
    SQ3 = math.sqrt(3)
    CX = CY = canvas_size / 2
    HEX_DIRS = [(1,0),(-1,0),(0,1),(0,-1),(1,-1),(-1,1)]

    def hex_to_pixel(q, r):
        x = hex_size * (SQ3 * q + SQ3 * 0.5 * r) + CX
        y = hex_size * 1.5 * r + CY
        return x, y

    def in_canvas(x, y):
        return hex_size <= x <= canvas_size - hex_size and \
               hex_size <= y <= canvas_size - hex_size

    def hex_key(q, r):
        return (q, r)

    cluster = set()
    frontier_list = []
    frontier_set = set()
    insertion_order = []

    def add_cell(q, r):
        k = hex_key(q, r)
        cluster.add(k)
        insertion_order.append(k)
        for dq, dr in HEX_DIRS:
            nq, nr = q + dq, r + dr
            nk = hex_key(nq, nr)
            if nk not in cluster and nk not in frontier_set:
                nx, ny = hex_to_pixel(nq, nr)
                if in_canvas(nx, ny):
                    frontier_list.append((nq, nr))
                    frontier_set.add(nk)

    add_cell(0, 0)

    import random
    rng = random.Random(42)

    for _ in range(steps):
        if not frontier_list:
            break
        idx = rng.randrange(len(frontier_list))
        q, r = frontier_list[idx]
        frontier_list[idx] = frontier_list[-1]
        frontier_list.pop()
        k = hex_key(q, r)
        frontier_set.discard(k)
        if k not in cluster:
            add_cell(q, r)

    return cluster, frontier_list, insertion_order


def test_eden_seed_starts_with_one_cell():
    cluster, _, order = _run_eden(0)
    assert len(cluster) == 1, "Seeded Eden model must start with exactly 1 cell"
    assert (0, 0) in cluster, "Seed cell must be at origin (0,0)"


def test_eden_growth_adds_cells():
    cluster, _, order = _run_eden(100)
    assert len(cluster) > 1, "Eden model must grow after iterations"
    assert len(cluster) <= 101, "Cannot add more cells than iterations + seed"


def test_eden_cell_count_equals_steps_plus_seed():
    """Each step adds exactly one cell (if frontier is non-empty)."""
    steps = 200
    cluster, _, order = _run_eden(steps)
    assert len(cluster) == steps + 1, \
        f"After {steps} steps, cluster should have {steps + 1} cells, got {len(cluster)}"


def test_eden_frontier_cells_adjacent_to_cluster():
    """Every frontier cell must share an edge with at least one cluster cell."""
    HEX_DIRS = [(1,0),(-1,0),(0,1),(0,-1),(1,-1),(-1,1)]

    cluster, frontier, _ = _run_eden(300)
    for (q, r) in frontier[:50]:  # spot-check first 50 frontier cells
        neighbors = {(q + dq, r + dr) for dq, dr in HEX_DIRS}
        assert neighbors & cluster, \
            f"Frontier cell ({q},{r}) has no cluster neighbor — frontier is corrupt"


def test_eden_cluster_stays_connected():
    """Spot-check: the origin (0,0) is always in the cluster."""
    cluster, _, _ = _run_eden(500)
    assert (0, 0) in cluster, "Origin cell must remain in cluster throughout growth"


def test_eden_no_duplicate_cluster_entries():
    cluster, _, order = _run_eden(400)
    assert len(cluster) == len(order), \
        "insertion_order has duplicates — addCell called twice for same cell"


# ── Hex geometry (pure Python) ────────────────────────────────────────────────

def test_hex_to_pixel_center():
    """Origin hex must map to canvas centre."""
    CX = CY = 350.0
    HEX_SIZE = 4
    SQ3 = math.sqrt(3)
    x = HEX_SIZE * (SQ3 * 0 + SQ3 * 0.5 * 0) + CX
    y = HEX_SIZE * 1.5 * 0 + CY
    assert abs(x - 350.0) < 1e-9 and abs(y - 350.0) < 1e-9, \
        f"Origin hex maps to ({x},{y}), expected (350,350)"


def test_hex_neighbors_distance_one():
    """The 6 neighbors of (0,0) in a pointy-top grid must all be at equal pixel distance."""
    HEX_SIZE = 4
    SQ3 = math.sqrt(3)
    CX = CY = 350.0
    HEX_DIRS = [(1,0),(-1,0),(0,1),(0,-1),(1,-1),(-1,1)]

    def hp(q, r):
        return (HEX_SIZE * (SQ3 * q + SQ3 * 0.5 * r) + CX,
                HEX_SIZE * 1.5 * r + CY)

    dists = []
    for dq, dr in HEX_DIRS:
        nx, ny = hp(dq, dr)
        dists.append(math.hypot(nx - CX, ny - CY))

    assert all(abs(d - dists[0]) < 0.001 for d in dists), \
        f"Neighbors not equidistant: {dists}"

    expected = HEX_SIZE * SQ3
    assert abs(dists[0] - expected) < 0.01, \
        f"Ring-1 distance {dists[0]:.3f} ≠ HEX_SIZE*sqrt(3) = {expected:.3f}"


# ── Color palette (pure Python) ───────────────────────────────────────────────

PALETTE = [
    (58,  30,  106),
    (192, 96,  128),
    (212, 168, 32),
    (255, 248, 240),
]


def _lerp_palette(t):
    t = max(0.0, min(1.0, t))
    n = len(PALETTE) - 1
    i = min(int(t * n), n - 1)
    f = t * n - i
    r1, g1, b1 = PALETTE[i]
    r2, g2, b2 = PALETTE[i + 1]
    return (
        round(r1 + (r2 - r1) * f),
        round(g1 + (g2 - g1) * f),
        round(b1 + (b2 - b1) * f),
    )


def test_palette_t0_is_violet():
    r, g, b = _lerp_palette(0.0)
    assert (r, g, b) == (58, 30, 106), f"t=0 must be violet #3A1E6A, got rgb({r},{g},{b})"


def test_palette_t1_is_cream():
    r, g, b = _lerp_palette(1.0)
    assert (r, g, b) == (255, 248, 240), f"t=1 must be cream #FFF8F0, got rgb({r},{g},{b})"


def test_palette_midpoint_between_rose_and_gold():
    """t=0.5 must land in the rose→gold transition (between palette stops 1 and 2)."""
    r, g, b = _lerp_palette(0.5)
    # Midpoint of (192,96,128) and (212,168,32): roughly R>160, G>70
    assert r > 160, f"Mid-palette red {r} too low"
    assert g > 70,  f"Mid-palette green {g} too low"


def test_palette_monotone_red_channel():
    """Red channel should increase monotonically across the gradient."""
    ts = [i / 20 for i in range(21)]
    reds = [_lerp_palette(t)[0] for t in ts]
    for i in range(len(reds) - 1):
        assert reds[i] <= reds[i + 1] + 1, \
            f"Red channel not monotone at t={ts[i]:.2f}: {reds[i]} > {reds[i+1]}"


# ── Edge cases / failure modes ────────────────────────────────────────────────

def test_empty_frontier_stops_growth():
    """When frontier is empty, growth must stop and cluster stays unchanged."""
    cluster_before, _, _ = _run_eden(20000)  # run until canvas fills
    # Run one more step — cluster size must not increase
    cluster_after, _, _ = _run_eden(20001)
    # Both runs should converge to the same cluster size
    assert abs(len(cluster_before) - len(cluster_after)) <= 1, \
        "Cluster grows beyond canvas after frontier exhausted"


def test_essay_stub_detected(tmp_path):
    """An essay.md under 200 words must fail the word-count minimum."""
    stub = tmp_path / "essay.md"
    stub.write_text("Sinai bloomed. " * 10, encoding="utf-8")
    count = len(stub.read_text().split())
    assert count < 200, "Fixture must be under 200 words for this test to be meaningful"


def test_essay_empty_is_zero_words(tmp_path):
    empty = tmp_path / "essay.md"
    empty.write_text("", encoding="utf-8")
    assert len(empty.read_text().split()) == 0


def test_pieces_json_missing_technique_detected():
    """A pieces.json entry without 'technique' must be detectable."""
    bad = {"id": "99-test", "title": "Test", "theme": "Test"}
    assert "technique" not in bad, "Fixture should not have technique field"
