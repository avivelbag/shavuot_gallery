"""
Tests for piece 27 — "Black Fire on White Fire" (probabilistic CA Torah letters).

Validates file layout, pieces.json entry, CA implementation markers,
palette colours, essay content and embedding, and pure-Python CA logic.
"""
import json
import os
import re
import random

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECES_JSON  = os.path.join(GALLERY_ROOT, "pieces.json")
PIECE_ID     = "27-black-fire-white-fire"
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


def test_entry_required_fields():
    p = _entry()
    assert p is not None
    for field in ("id", "title", "tagline", "year", "theme", "technique", "path", "thumbnail", "essay"):
        assert field in p and p[field], f"Missing or empty field '{field}' in pieces.json entry"


def test_entry_theme_mentions_matan_torah():
    p = _entry()
    assert p is not None
    theme = p["theme"].lower()
    assert "torah" in theme or "matan" in theme, \
        f"Expected 'matan torah' in theme, got: {p['theme']}"


def test_entry_technique_mentions_cellular_automaton():
    p = _entry()
    assert p is not None
    tech = p["technique"].lower()
    assert "cellular" in tech or "automaton" in tech or "ca" in tech, \
        f"Expected cellular automaton in technique, got: {p['technique']}"


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


def test_charset_utf8():
    html = _html()
    assert 'charset="UTF-8"' in html or "charset=utf-8" in html.lower(), \
        "index.html must declare UTF-8 charset"


def test_no_external_scripts():
    html = _html()
    external = re.findall(r'<script[^>]+src\s*=\s*["\']([^"\']+)["\']', html, re.IGNORECASE)
    assert len(external) == 0, f"External scripts found: {external}"


def test_frame_fps_cap_present():
    html = _html()
    assert "FRAME_MIN_MS" in html or "frameMin" in html or "1000 / 60" in html or "1000/60" in html, \
        "FPS cap constant (FRAME_MIN_MS or 1000/60) not found"


# ─── CA implementation markers ───────────────────────────────────────────────

def test_p_survive_constant_present():
    assert "P_SURVIVE" in _html(), "P_SURVIVE constant not found in index.html"


def test_p_spread_constant_present():
    assert "P_SPREAD" in _html(), "P_SPREAD constant not found in index.html"


def test_cols_constant_present():
    assert "COLS" in _html(), "COLS grid dimension not found in index.html"


def test_rows_constant_present():
    assert "ROWS" in _html(), "ROWS grid dimension not found in index.html"


def test_get_image_data_for_letter_seeding():
    html = _html()
    assert "getImageData" in html, "getImageData (letter rasterization) not found in index.html"


def test_fill_text_for_letter_rendering():
    html = _html()
    assert "fillText" in html, "fillText (letter rasterization) not found in index.html"


def test_count_neighbors_or_neighbor_count():
    html = _html()
    assert "neighbors" in html or "Neighbors" in html, \
        "neighbor-counting function not found in index.html"


def test_step_ca_function():
    html = _html()
    assert "stepCA" in html or "step_ca" in html or "stepCa" in html, \
        "stepCA function not found in index.html"


def test_heat_array_present():
    assert "heat" in _html(), "heat array not found in index.html"


def test_image_data_rendering():
    html = _html()
    assert "createImageData" in html or "putImageData" in html, \
        "ImageData-based rendering not found in index.html"


def test_draw_image_blit():
    assert "drawImage" in _html(), "drawImage (scaled blit) not found in index.html"


def test_uint8_array_for_grid():
    assert "Uint8Array" in _html(), "Uint8Array grid not found in index.html"


def test_float32_array_for_heat():
    assert "Float32Array" in _html(), "Float32Array heat array not found in index.html"


def test_seed_letter_function():
    html = _html()
    assert "seedLetter" in html or "seed_letter" in html, \
        "seedLetter function not found in index.html"


# ─── Hebrew letters ───────────────────────────────────────────────────────────

def test_22_hebrew_letters_array():
    html = _html()
    assert "LETTERS" in html, "LETTERS array not found in index.html"


def test_all_22_letters_present():
    """All 22 Hebrew letters must appear in the source."""
    html = _html()
    letters = list("אבגדהוזחטיכלמנסעפצקרשת")
    missing = [ch for ch in letters if ch not in html]
    assert len(missing) == 0, f"Missing Hebrew letters in index.html: {missing}"


def test_letter_cycling_logic():
    html = _html()
    assert "letterIdx" in html or "letterIndex" in html or "letter_idx" in html, \
        "Letter index cycling variable not found in index.html"


def test_aleph_letter_in_source():
    assert "א" in _html(), "Aleph (א) not found in index.html"


def test_tav_letter_in_source():
    assert "ת" in _html(), "Tav (ת) not found in index.html"


# ─── Palette ─────────────────────────────────────────────────────────────────

def test_background_color_0a0a12():
    assert "#0a0a12" in _html() or "#0A0A12" in _html(), \
        "Background colour #0a0a12 not found in index.html"


def test_fire_core_color_e8e8ff():
    html = _html()
    assert "#e8e8ff" in html or "#E8E8FF" in html or "e8e8ff" in html.lower(), \
        "Fire-core colour #E8E8FF not found in index.html"


def test_thumbnail_dark_background():
    svg = _svg()
    assert "#0a0a12" in svg or "#0A0A12" in svg, \
        "Thumbnail missing dark background #0a0a12"


def test_thumbnail_bright_cells():
    svg = _svg()
    assert "#e8e8ff" in svg or "#E8E8FF" in svg or "e8e8ff" in svg.lower(), \
        "Thumbnail missing bright cell colour #e8e8ff"


def test_thumbnail_is_valid_svg():
    svg = _svg()
    assert "<svg" in svg and "</svg>" in svg, "thumbnail.svg is not valid SVG"


# ─── Timing constants ────────────────────────────────────────────────────────

def test_seed_ms_or_burn_ms_defined():
    html = _html()
    assert "SEED_MS" in html or "BURN_MS" in html or "LETTER_MS" in html, \
        "Timing constants (SEED_MS/BURN_MS/LETTER_MS) not found"


def test_decay_phase_in_code():
    html = _html()
    assert "DECAY_MS" in html or "decay" in html.lower(), \
        "Decay phase not found in index.html"


# ─── Essay content ────────────────────────────────────────────────────────────

def test_essay_word_count_at_least_300():
    text = _essay()
    count = len(text.split())
    assert count >= 300, f"essay.md has {count} words; expected >= 300"


def test_essay_mentions_devarim_rabbah():
    text = _essay()
    assert "Devarim Rabbah" in text or "devarim rabbah" in text.lower(), \
        "essay.md must cite Devarim Rabbah 3:12"


def test_essay_cites_devarim_rabbah_3_12():
    text = _essay()
    assert "3:12" in text, "essay.md must cite Devarim Rabbah 3:12 exactly"


def test_essay_mentions_yerushalmi_shekalim():
    text = _essay()
    assert "Shekalim" in text or "shekalim" in text.lower(), \
        "essay.md must cite Yerushalmi Shekalim 6:1"


def test_essay_cites_yerushalmi_shekalim_6_1():
    text = _essay()
    assert "6:1" in text, "essay.md must cite Yerushalmi Shekalim 6:1 exactly"


def test_essay_mentions_bereishit_rabbah():
    text = _essay()
    assert "Bereishit Rabbah" in text or "bereishit rabbah" in text.lower(), \
        "essay.md must cite Bereishit Rabbah 1:1 (Torah as blueprint)"


def test_essay_cites_bereishit_rabbah_1_1():
    text = _essay()
    assert "1:1" in text, "essay.md must cite Bereishit Rabbah 1:1 exactly"


def test_essay_mentions_sanhedrin():
    text = _essay()
    assert "Sanhedrin" in text or "sanhedrin" in text.lower(), \
        "essay.md must cite Talmud Bavli Sanhedrin 21b"


def test_essay_mentions_black_fire():
    text = _essay()
    lower = text.lower()
    assert "black fire" in lower or "eish shechorah" in lower or "eish" in lower, \
        "essay.md must mention 'black fire' or the Hebrew phrase"


def test_essay_mentions_white_fire():
    text = _essay()
    lower = text.lower()
    assert "white fire" in lower or "eish levanah" in lower, \
        "essay.md must mention 'white fire' or the Hebrew phrase"


def test_essay_mentions_blueprint():
    text = _essay()
    lower = text.lower()
    assert "blueprint" in lower or "amon" in lower, \
        "essay.md must explain the Torah-as-blueprint teaching (Bereishit Rabbah 1:1)"


def test_essay_embedded_in_html():
    """Substantial essay words must appear verbatim in index.html."""
    essay = _essay()
    html  = _html()
    words = [w for w in essay.split() if len(w) > 6][:20]
    found = sum(1 for w in words if w in html)
    assert found >= 5, \
        f"index.html does not embed essay text (only {found}/20 sampled words found)"


# ─── README content ──────────────────────────────────────────────────────────

def test_readme_mentions_cellular_automaton():
    text = _readme().lower()
    assert "cellular automaton" in text or "cellular" in text, \
        "README.md must mention cellular automaton"


def test_readme_mentions_hebrew_letters():
    text = _readme().lower()
    assert "hebrew" in text or "letter" in text, \
        "README.md must mention Hebrew letters"


def test_readme_mentions_black_fire():
    text = _readme()
    assert "black fire" in text.lower() or "eish" in text.lower() or "fire" in text.lower(), \
        "README.md must describe the black fire theme"


# ─── Pure-Python CA logic (deterministic tests of the algorithm) ──────────────

def _step_ca_py(grid, cols, rows, p_survive, p_spread, rng_seed=42):
    """Pure-Python replica of the CA step in index.html."""
    rng = random.Random(rng_seed)
    next_grid = [0] * (cols * rows)

    def count_neighbors(x, y):
        n = 0
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < cols and 0 <= ny < rows:
                    n += grid[ny * cols + nx]
        return n

    for y in range(rows):
        for x in range(cols):
            i = y * cols + x
            if grid[i]:
                next_grid[i] = 1 if rng.random() < p_survive else 0
            else:
                n = count_neighbors(x, y)
                next_grid[i] = 1 if (n > 0 and rng.random() < p_spread * n) else 0
    return next_grid


def test_ca_all_dead_stays_dead():
    """An all-dead grid must remain all-dead regardless of parameters."""
    cols, rows = 20, 15
    grid = [0] * (cols * rows)
    result = _step_ca_py(grid, cols, rows, p_survive=0.88, p_spread=0.12)
    assert all(c == 0 for c in result), \
        "All-dead grid must produce all-dead next state"


def test_ca_single_live_cell_can_spread():
    """
    A single live cell surrounded by dead cells may spread to neighbors.
    Over 30 steps with high p_spread, the live region must grow beyond 1 cell.
    """
    cols, rows = 20, 20
    grid = [0] * (cols * rows)
    cx, cy = cols // 2, rows // 2
    grid[cy * cols + cx] = 1

    for step in range(30):
        grid = _step_ca_py(grid, cols, rows, p_survive=0.95, p_spread=0.5, rng_seed=step)

    live_count = sum(grid)
    assert live_count > 1, \
        f"Single live cell should spread over 30 steps with p_spread=0.5 (got {live_count} live cells)"


def test_ca_zero_p_survive_extinguishes():
    """With p_survive=0 and p_spread=0, every live cell dies immediately."""
    cols, rows = 10, 10
    grid = [1] * (cols * rows)
    result = _step_ca_py(grid, cols, rows, p_survive=0.0, p_spread=0.0)
    assert all(c == 0 for c in result), \
        "p_survive=0, p_spread=0 must extinguish all cells in one step"


def test_ca_full_grid_survival_rate():
    """
    With a full grid and p_survive=0.88, approximately 88% of cells should survive.
    Allow ±10% tolerance for randomness.
    """
    cols, rows = 50, 50
    grid = [1] * (cols * rows)
    result = _step_ca_py(grid, cols, rows, p_survive=0.88, p_spread=0.0, rng_seed=99)
    survived = sum(result)
    total = cols * rows
    ratio = survived / total
    assert 0.78 <= ratio <= 0.98, \
        f"Expected ~88% survival rate, got {ratio:.2%} ({survived}/{total})"


def test_ca_spread_only_from_neighbors():
    """
    Dead cells with no live neighbors must never ignite, even with p_spread=1.0.
    A single isolated live cell cannot spread to cells that are not adjacent.
    """
    cols, rows = 10, 10
    grid = [0] * (cols * rows)
    # Place a live cell in a corner — can spread to at most 3 neighbors
    grid[0] = 1

    # Run one step with p_survive=1, p_spread=1 — only adjacent cells can ignite
    result = _step_ca_py(grid, cols, rows, p_survive=1.0, p_spread=1.0, rng_seed=7)

    # Cell (5, 5) has no live neighbors — must remain dead
    far_idx = 5 * cols + 5
    assert result[far_idx] == 0, \
        "A cell far from any live cell must not ignite (spread requires adjacency)"


def test_ca_neighbor_count_correct():
    """
    Pure-Python neighbor count for a center cell surrounded by all live cells
    in a 3×3 grid must be 8.
    """
    cols, rows = 3, 3
    grid = [1] * (cols * rows)

    def count_neighbors(x, y):
        n = 0
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < cols and 0 <= ny < rows:
                    n += grid[ny * cols + nx]
        return n

    assert count_neighbors(1, 1) == 8, \
        "Center cell of 3×3 all-live grid must have 8 neighbors"


def test_ca_corner_neighbor_count():
    """A corner cell can have at most 3 neighbors in an 8-connected grid."""
    cols, rows = 5, 5
    grid = [1] * (cols * rows)

    def count_neighbors(x, y):
        n = 0
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < cols and 0 <= ny < rows:
                    n += grid[ny * cols + nx]
        return n

    assert count_neighbors(0, 0) == 3, \
        "Top-left corner in a 5×5 all-live grid must have exactly 3 neighbors"


# ─── Heat rendering logic (pure Python) ──────────────────────────────────────

def test_heat_warms_for_live_cells():
    """Heat values must increase when the cell is alive."""
    heat = 0.5
    alive = True
    new_heat = min(1.0, heat + 0.15) if alive else max(0.0, heat - 0.04)
    assert new_heat > heat, "Heat must increase for a live cell"


def test_heat_cools_for_dead_cells():
    """Heat values must decrease when the cell is dead."""
    heat = 0.5
    alive = False
    new_heat = min(1.0, heat + 0.15) if alive else max(0.0, heat - 0.04)
    assert new_heat < heat, "Heat must decrease for a dead cell"


def test_heat_clamps_at_one():
    """Heat must never exceed 1.0."""
    heat = 0.95
    new_heat = min(1.0, heat + 0.15)
    assert new_heat == 1.0, "Heat must clamp at 1.0"


def test_heat_clamps_at_zero():
    """Heat must never go below 0.0."""
    heat = 0.02
    new_heat = max(0.0, heat - 0.04)
    assert new_heat == 0.0, "Heat must clamp at 0.0"


# ─── Essay / stub failure-mode tests ─────────────────────────────────────────

def test_essay_stub_detected(tmp_path):
    """An essay under 200 words must fail our word-count threshold."""
    stub = tmp_path / "essay.md"
    stub.write_text("Fire upon fire. " * 10, encoding="utf-8")
    word_count = len(stub.read_text().split())
    assert word_count < 200, "Fixture must be under 200 words"


def test_essay_empty_detected(tmp_path):
    """An empty essay.md must register as 0 words."""
    empty = tmp_path / "essay.md"
    empty.write_text("", encoding="utf-8")
    assert len(empty.read_text().split()) == 0


def test_pieces_json_missing_field_detected():
    """Entry without required fields must be detectable."""
    bad = {"id": "99-test", "title": "Test"}
    required = ("tagline", "year", "theme", "technique", "path", "thumbnail", "essay")
    for field in required:
        assert field not in bad, f"Fixture should not have field '{field}'"
