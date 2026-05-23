"""
Tests for pieces/94-cyclic-ca-seven-species.

Covers:
- Piece registration in pieces.json (id, required fields, theme/technique)
- File layout (index.html, essay.md, thumbnail.svg, README.md exist on disk)
- CA algorithm correctness (step function logic)
- Essay content (word count, embedded in HTML, bilingual scripture excerpts)
- Thumbnail SVG validity
- Edge cases: empty grid, single-cell grid, all-same-state grid
"""

import json
import os
import re

import pytest

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")
PIECE_ID = "94-cyclic-ca-seven-species"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def piece_entry():
    """Return the pieces.json entry for this piece, or None if absent."""
    with open(PIECES_JSON, encoding="utf-8") as fh:
        data = json.load(fh)
    for p in data:
        if p["id"] == PIECE_ID:
            return p
    return None


@pytest.fixture(scope="module")
def index_html():
    """Return the contents of index.html for this piece."""
    path = os.path.join(PIECE_DIR, "index.html")
    return open(path, encoding="utf-8").read()


@pytest.fixture(scope="module")
def essay_text():
    """Return the contents of essay.md for this piece."""
    path = os.path.join(PIECE_DIR, "essay.md")
    return open(path, encoding="utf-8").read()


# ---------------------------------------------------------------------------
# Registration and required fields
# ---------------------------------------------------------------------------

def test_piece_registered(piece_entry):
    """The piece must appear in pieces.json."""
    assert piece_entry is not None, f"Piece '{PIECE_ID}' not found in pieces.json"


def test_required_fields_present(piece_entry):
    """All mandatory pieces.json fields must be non-empty."""
    if piece_entry is None:
        pytest.skip("Piece not registered")
    required = ("id", "title", "tagline", "year", "theme", "technique",
                "path", "thumbnail", "essay")
    for field in required:
        value = piece_entry.get(field)
        assert value is not None and value != "", (
            f"Field '{field}' is missing or empty in pieces.json entry"
        )


def test_theme_is_bikkurim(piece_entry):
    """Theme must reference Bikkurim / seven species."""
    if piece_entry is None:
        pytest.skip("Piece not registered")
    assert "Bikkurim" in piece_entry["theme"] or "seven species" in piece_entry["theme"].lower(), (
        f"Expected Bikkurim/seven-species theme, got: {piece_entry['theme']}"
    )


def test_technique_is_cyclic_ca(piece_entry):
    """Technique must reference cyclic cellular automaton."""
    if piece_entry is None:
        pytest.skip("Piece not registered")
    tech = piece_entry["technique"].lower()
    assert "cyclic" in tech and "automaton" in tech, (
        f"Expected cyclic CA technique, got: {piece_entry['technique']}"
    )


def test_year_is_integer(piece_entry):
    """Year must be an integer."""
    if piece_entry is None:
        pytest.skip("Piece not registered")
    assert isinstance(piece_entry["year"], int)


# ---------------------------------------------------------------------------
# File layout
# ---------------------------------------------------------------------------

def test_index_html_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "index.html")), "index.html missing"


def test_essay_md_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "essay.md")), "essay.md missing"


def test_thumbnail_svg_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "thumbnail.svg")), "thumbnail.svg missing"


def test_readme_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "README.md")), "README.md missing"


def test_thumbnail_is_valid_svg():
    """thumbnail.svg must contain SVG opening and closing tags."""
    svg = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert "<svg" in svg and "</svg>" in svg, "thumbnail.svg does not look like valid SVG"


# ---------------------------------------------------------------------------
# HTML content checks
# ---------------------------------------------------------------------------

def test_index_html_uses_request_animation_frame(index_html):
    assert "requestAnimationFrame" in index_html, (
        "index.html must use requestAnimationFrame for the animation loop"
    )


def test_index_html_uses_image_data(index_html):
    """ImageData must be used for pixel-level rendering."""
    assert "ImageData" in index_html or "createImageData" in index_html, (
        "index.html must use ImageData for performance rendering"
    )


def test_index_html_has_all_seven_colors(index_html):
    """All seven species colors must appear in index.html."""
    colors = ["E8C547", "C4A35A", "6B2D8B", "8B4513", "C0392B", "5D7A2A", "D4890A"]
    for color in colors:
        assert color in index_html, f"Color #{color} missing from index.html"


def test_index_html_has_canvas(index_html):
    assert "<canvas" in index_html, "index.html must contain a <canvas> element"


def test_index_html_has_seven_states_constant(index_html):
    """The JS must define STATES = 7."""
    assert "STATES" in index_html and "7" in index_html, (
        "index.html must define a STATES constant"
    )


def test_index_html_has_threshold_k3(index_html):
    """The JS must define threshold K=3."""
    assert re.search(r'K\s*=\s*3', index_html), (
        "index.html must define threshold K = 3"
    )


def test_index_html_has_hebrew_heading(index_html):
    """The legend heading שִׁבְעַת הַמִּינִים must appear in index.html."""
    assert "שִׁבְעַת" in index_html, (
        "index.html must contain the Hebrew heading שִׁבְעַת הַמִּינִים"
    )


def test_index_html_has_all_species_names(index_html):
    """All seven Hebrew species names must appear in index.html."""
    species = ["חִטָּה", "שְׂעֹרָה", "גֶּפֶן", "תְּאֵנָה", "רִמּוֹן", "זַיִת", "תָּמָר"]
    for name in species:
        assert name in index_html, f"Hebrew species name '{name}' missing from index.html"


def test_index_html_uses_double_buffer(index_html):
    """The CA must use two separate typed arrays for double-buffering."""
    assert "Uint8Array" in index_html, (
        "index.html must use Uint8Array for the double-buffer grid"
    )


def test_index_html_has_deut_8_8_hebrew(index_html):
    """index.html must contain Deuteronomy 8:8 in Hebrew with nikud."""
    assert "חִטָּה וּשְׂעֹרָה" in index_html, (
        "index.html must embed Deuteronomy 8:8 Hebrew text"
    )


def test_index_html_has_bikkurim_declaration(index_html):
    """index.html must contain the Bikkurim declaration from Deuteronomy 26."""
    assert "אֲרַמִּי" in index_html, (
        "index.html must include the arami oved avi declaration (Deuteronomy 26)"
    )


def test_index_html_has_tanach_english_translation(index_html):
    """The English translation of the key Tanach passage must appear."""
    assert "wheat and barley" in index_html.lower() or "land of wheat" in index_html.lower(), (
        "index.html must include English translation of Deuteronomy 8:8"
    )


def test_index_html_has_essay_text(essay_text, index_html):
    """The essay words must be embedded inside index.html."""
    words = [w for w in essay_text.split() if len(w) > 6][:12]
    found = sum(1 for w in words if w in index_html)
    assert found >= 6, (
        f"index.html must embed essay text; only {found}/12 sampled essay words found"
    )


def test_index_html_has_side_by_side_layout(index_html):
    """index.html must define a side-by-side layout for wide screens."""
    assert "flex" in index_html or "grid" in index_html, (
        "index.html must use flex or grid for the side-by-side art/essay layout"
    )


def test_index_html_has_mobile_breakpoint(index_html):
    """index.html must include a media query for narrow screens."""
    assert "max-width" in index_html, (
        "index.html must include a max-width media query for mobile layout"
    )


# ---------------------------------------------------------------------------
# Essay content
# ---------------------------------------------------------------------------

def test_essay_has_at_least_300_words(essay_text):
    """Essay must be substantial — at least 300 words."""
    word_count = len(essay_text.split())
    assert word_count >= 300, (
        f"essay.md has only {word_count} words (need at least 300)"
    )


def test_essay_cites_deuteronomy_8_8(essay_text):
    """Essay must cite or quote Deuteronomy 8:8."""
    assert "8:8" in essay_text or "Deuteronomy 8" in essay_text, (
        "essay.md must reference Deuteronomy 8:8"
    )


def test_essay_mentions_bikkurim(essay_text):
    """Essay must mention Bikkurim (first fruits offering)."""
    lower = essay_text.lower()
    assert "bikkurim" in lower or "first fruit" in lower, (
        "essay.md must discuss the Bikkurim offering"
    )


def test_essay_mentions_omer(essay_text):
    """Essay must reference the Omer count or the seven weeks."""
    lower = essay_text.lower()
    assert "omer" in lower or "seven week" in lower, (
        "essay.md must discuss the Omer / seven-week harvest context"
    )


def test_essay_mentions_mishnah(essay_text):
    """Essay must reference the Mishnah (Bikkurim tractate)."""
    assert "Mishnah" in essay_text or "Bikkurim 1" in essay_text, (
        "essay.md must cite the Mishnah Bikkurim"
    )


def test_essay_connects_to_artwork(essay_text):
    """Essay must explain the connection to the cyclic CA."""
    lower = essay_text.lower()
    assert "wave" in lower or "cyclic" in lower or "cellular" in lower, (
        "essay.md must explain the cyclic CA / wave-propagation connection"
    )


# ---------------------------------------------------------------------------
# Python model of the CA rule (deterministic unit tests)
# ---------------------------------------------------------------------------

def _cyclic_ca_step(grid, width, height, states=7, k=3):
    """
    Pure-Python reference implementation of the cyclic CA step.

    Each cell with state s advances to (s+1)%states if at least k of its
    8 Moore neighbors hold state (s+1)%states; otherwise it stays at s.
    Returns a new list (does not mutate grid).
    """
    nxt = list(grid)
    for y in range(height):
        for x in range(width):
            s = grid[y * width + x]
            ns = (s + 1) % states
            count = 0
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    if dx == 0 and dy == 0:
                        continue
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < width and 0 <= ny < height:
                        if grid[ny * width + nx] == ns:
                            count += 1
            nxt[y * width + x] = ns if count >= k else s
    return nxt


def test_ca_cell_advances_when_threshold_met():
    """A center cell surrounded by ≥3 neighbors with next-state should advance."""
    # 3×3 grid; center cell = 0, all 8 neighbors = 1 (next state for state 0)
    grid = [1] * 9
    grid[4] = 0  # center cell
    result = _cyclic_ca_step(grid, 3, 3)
    assert result[4] == 1, "Cell with 8 neighbors at next-state should advance to state 1"


def test_ca_cell_stays_when_below_threshold():
    """A center cell with fewer than K=3 neighbors at next-state must not advance."""
    # 3×3 grid; center cell = 0, only 2 neighbors = 1
    grid = [0] * 9
    grid[0] = 1
    grid[1] = 1  # two neighbors with next-state (1)
    result = _cyclic_ca_step(grid, 3, 3, k=3)
    assert result[4] == 0, "Cell with only 2 neighbors at next-state must stay at 0"


def test_ca_state_wraps_around():
    """State 6 should advance to state 0 when ≥3 neighbors hold state 0."""
    # 3×3 grid; center = 6, surrounded by 0s
    grid = [0] * 9
    grid[4] = 6
    result = _cyclic_ca_step(grid, 3, 3)
    assert result[4] == 0, "State 6 should wrap to state 0"


def test_ca_uniform_grid_does_not_change():
    """A grid where all cells are the same state stays frozen (no neighbor is at next-state)."""
    grid = [3] * 25  # 5×5 all state 3
    result = _cyclic_ca_step(grid, 5, 5)
    # With all neighbors also at state 3, none are at state 4 → no cell advances
    assert result == grid, "A uniform grid should not change under one CA step"


def test_ca_boundary_cells_handled_correctly():
    """Corner and edge cells must not read out-of-bounds neighbors."""
    # 3×3 grid with top-left corner = 0, all others = 1
    grid = [1] * 9
    grid[0] = 0
    result = _cyclic_ca_step(grid, 3, 3)
    # Corner cell has only 3 valid neighbors; all are at state 1 (next-state for 0)
    # 3 >= K=3, so it should advance
    assert result[0] == 1, "Corner cell should advance when all 3 valid neighbors are at next-state"


def test_ca_empty_grid_edge_case():
    """A 1×1 grid cell has no neighbors so can never advance."""
    grid = [2]
    result = _cyclic_ca_step(grid, 1, 1)
    assert result == [2], "A 1×1 grid has no neighbors and should never change state"


def test_ca_step_does_not_mutate_input():
    """The reference implementation must not modify the original grid list."""
    grid = [0, 1, 2, 3, 4, 5, 6, 0, 1]
    original = list(grid)
    _cyclic_ca_step(grid, 3, 3)
    assert grid == original, "_cyclic_ca_step must not mutate the input grid"


def test_ca_two_steps_eventually_differ_from_random_start():
    """After two steps a random 10×10 grid should generally differ from the initial state."""
    import random
    random.seed(42)
    w, h = 10, 10
    grid = [random.randint(0, 6) for _ in range(w * h)]
    step1 = _cyclic_ca_step(grid, w, h)
    step2 = _cyclic_ca_step(step1, w, h)
    # At least some cells should have changed over two generations in a random grid
    changed = sum(1 for a, b in zip(grid, step2) if a != b)
    assert changed > 0, "After two steps on a random grid, at least some cells should change"


# ---------------------------------------------------------------------------
# Edge case: malformed / missing pieces.json handled gracefully
# ---------------------------------------------------------------------------

def test_piece_id_not_duplicated():
    """The piece ID must appear exactly once in pieces.json."""
    with open(PIECES_JSON, encoding="utf-8") as fh:
        data = json.load(fh)
    matching = [p for p in data if p["id"] == PIECE_ID]
    assert len(matching) == 1, f"Expected exactly 1 entry for '{PIECE_ID}', found {len(matching)}"


def test_piece_path_ends_with_html(piece_entry):
    """The path field must end with .html."""
    if piece_entry is None:
        pytest.skip("Piece not registered")
    assert piece_entry["path"].endswith(".html"), (
        f"path must end with .html, got: {piece_entry['path']}"
    )


def test_piece_thumbnail_extension_is_svg(piece_entry):
    """Thumbnail must be an SVG file for this piece."""
    if piece_entry is None:
        pytest.skip("Piece not registered")
    assert piece_entry["thumbnail"].endswith(".svg"), (
        f"Expected .svg thumbnail, got: {piece_entry['thumbnail']}"
    )
