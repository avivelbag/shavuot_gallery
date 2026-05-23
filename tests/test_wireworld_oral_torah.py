"""
Tests for piece 93-wireworld-oral-torah.

Validates the piece directory layout, pieces.json registration, HTML content,
essay content, and thumbnail SVG.  Also contains isolated unit-level tests
of the Wireworld transition rules and the Y-junction splitter logic by
re-implementing the small pure-Python equivalents of the JS logic.
"""
import json
import os
import re

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID = "93-wireworld-oral-torah"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
INDEX_HTML = os.path.join(PIECE_DIR, "index.html")
ESSAY_MD = os.path.join(PIECE_DIR, "essay.md")
THUMBNAIL = os.path.join(PIECE_DIR, "thumbnail.svg")
README = os.path.join(PIECE_DIR, "README.md")
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_piece_entry():
    """Return the pieces.json entry for the wireworld piece, or None."""
    with open(PIECES_JSON, "r", encoding="utf-8") as fh:
        pieces = json.load(fh)
    for p in pieces:
        if p["id"] == PIECE_ID:
            return p
    return None


# ---------------------------------------------------------------------------
# Directory and file layout
# ---------------------------------------------------------------------------

def test_piece_directory_exists():
    assert os.path.isdir(PIECE_DIR), f"Piece directory {PIECE_DIR} not found"


def test_index_html_exists():
    assert os.path.isfile(INDEX_HTML), "index.html missing from piece directory"


def test_essay_md_exists():
    assert os.path.isfile(ESSAY_MD), "essay.md missing from piece directory"


def test_thumbnail_exists():
    assert os.path.isfile(THUMBNAIL), "thumbnail.svg missing from piece directory"


def test_readme_exists():
    assert os.path.isfile(README), "README.md missing from piece directory"


# ---------------------------------------------------------------------------
# pieces.json registration
# ---------------------------------------------------------------------------

def test_piece_registered_in_pieces_json():
    entry = load_piece_entry()
    assert entry is not None, f"Piece '{PIECE_ID}' not found in pieces.json"


def test_pieces_json_theme_field():
    entry = load_piece_entry()
    assert entry is not None
    assert "Oral Torah" in entry["theme"], (
        "pieces.json theme must mention 'Oral Torah'"
    )


def test_pieces_json_technique_field():
    entry = load_piece_entry()
    assert entry is not None
    assert "Wireworld" in entry["technique"], (
        "pieces.json technique must mention 'Wireworld'"
    )


def test_pieces_json_required_fields():
    entry = load_piece_entry()
    assert entry is not None
    required = ("id", "title", "tagline", "year", "theme", "technique", "path", "thumbnail", "essay")
    for field in required:
        assert field in entry and entry[field], f"Missing or empty field: {field}"


def test_pieces_json_paths_match_id():
    entry = load_piece_entry()
    assert entry is not None
    assert PIECE_ID in entry["path"]
    assert PIECE_ID in entry["thumbnail"]
    assert PIECE_ID in entry["essay"]


# ---------------------------------------------------------------------------
# essay.md content
# ---------------------------------------------------------------------------

def test_essay_minimum_word_count():
    text = open(ESSAY_MD, encoding="utf-8").read()
    words = text.split()
    assert len(words) >= 300, f"Essay has {len(words)} words, need >= 300"


def test_essay_contains_pirkei_avot_quote():
    text = open(ESSAY_MD, encoding="utf-8").read()
    assert "Pirkei Avot" in text or "Avot" in text, (
        "Essay must reference Pirkei Avot"
    )


def test_essay_contains_hebrew_pirkei_avot_opening():
    text = open(ESSAY_MD, encoding="utf-8").read()
    assert "מֹשֶׁה" in text or "משה" in text, (
        "Essay must contain the Hebrew opening of Pirkei Avot 1:1"
    )


def test_essay_contains_wireworld_explanation():
    text = open(ESSAY_MD, encoding="utf-8").read()
    # The essay must explain the Wireworld CA rule
    assert "Wireworld" in text or "Brian Silverman" in text, (
        "Essay must mention Wireworld or its creator Brian Silverman"
    )


def test_essay_mentions_kibel_and_mesarah():
    """Essay must explain the relay structure: kibel (received) and mesarah (transmitted)."""
    text = open(ESSAY_MD, encoding="utf-8").read()
    assert "kibel" in text or "kibel" in text.lower() or "received" in text, (
        "Essay must explain the meaning of 'kibel' (received)"
    )
    assert "mesarah" in text or "transmitted" in text, (
        "Essay must explain the meaning of 'mesarah' (transmitted)"
    )


def test_essay_mentions_sinai():
    text = open(ESSAY_MD, encoding="utf-8").read()
    assert "Sinai" in text, "Essay must mention Sinai"


def test_essay_mentions_wireworld_fragility():
    """Essay must discuss the 1-or-2-neighbor condition."""
    text = open(ESSAY_MD, encoding="utf-8").read()
    assert "one or two" in text.lower() or "1 or 2" in text, (
        "Essay must explain the Wireworld rule requiring exactly 1 or 2 neighbor heads"
    )


# ---------------------------------------------------------------------------
# index.html content
# ---------------------------------------------------------------------------

def test_index_html_uses_requestAnimationFrame():
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "requestAnimationFrame" in html, (
        "index.html must use requestAnimationFrame for animation"
    )


def test_index_html_has_canvas():
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "<canvas" in html, "index.html must contain a <canvas> element"


def test_index_html_defines_wireworld_states():
    """The JS must define all four Wireworld cell states."""
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "CONDUCTOR" in html, "index.html must define CONDUCTOR state"
    assert "E_HEAD" in html or "HEAD" in html, "index.html must define Electron Head state"
    assert "E_TAIL" in html or "TAIL" in html, "index.html must define Electron Tail state"


def test_index_html_uses_amber_conductor_color():
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "#C8881A" in html or "c8881a" in html.lower(), (
        "index.html must use amber conductor color #C8881A"
    )


def test_index_html_uses_head_color():
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "#FFFAF0" in html or "fffaf0" in html.lower(), (
        "index.html must use white-gold electron head color #FFFAF0"
    )


def test_index_html_uses_tail_color():
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "#8B2500" in html or "8b2500" in html.lower(), (
        "index.html must use ember-red electron tail color #8B2500"
    )


def test_index_html_uses_dark_parchment_background():
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "#1A1208" in html or "1a1208" in html.lower(), (
        "index.html must use dark parchment background #1A1208"
    )


def test_index_html_has_sinai_hebrew_label():
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "סיני" in html or "סִינַי" in html, (
        "index.html must display the Hebrew word for Sinai"
    )


def test_index_html_has_generation_labels():
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "משה" in html, "index.html must include Moses label in Hebrew (משה)"
    assert "יהושע" in html, "index.html must include Joshua label in Hebrew (יהושע)"
    assert "זקנים" in html, "index.html must include Elders label in Hebrew (זקנים)"
    assert "נביאים" in html, "index.html must include Prophets label in Hebrew (נביאים)"
    assert "כנסת הגדולה" in html, "index.html must include Great Assembly label in Hebrew"


def test_index_html_embeds_essay_text():
    """Essay text must be embedded in index.html (no runtime fetch)."""
    essay = open(ESSAY_MD, encoding="utf-8").read()
    html = open(INDEX_HTML, encoding="utf-8").read()
    words = [w for w in essay.split() if len(w) > 6][:10]
    found = sum(1 for w in words if w in html)
    assert found >= 5, (
        f"index.html must embed essay text (only {found}/10 sampled words found)"
    )


def test_index_html_bloom_effect():
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "RadialGradient" in html or "radialGradient" in html or "createRadialGradient" in html, (
        "index.html must implement bloom/glow effect via radial gradient"
    )


def test_index_html_pulse_injection():
    """The HTML must contain pulse injection logic."""
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "inject" in html.lower() or "PULSE" in html or "E_HEAD" in html, (
        "index.html must inject electron pulses into the trunk"
    )


def test_index_html_step_every_3_frames():
    """CA should step every 3 animation frames as per spec."""
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "STEP_EVERY" in html or "step_every" in html.lower() or (
        re.search(r'%\s*3', html) is not None
    ), "index.html must step CA every 3 animation frames"


# ---------------------------------------------------------------------------
# thumbnail.svg content
# ---------------------------------------------------------------------------

def test_thumbnail_is_valid_svg():
    text = open(THUMBNAIL, encoding="utf-8").read()
    assert "<svg" in text and "</svg>" in text, "thumbnail.svg must be valid SVG"


def test_thumbnail_size_400():
    text = open(THUMBNAIL, encoding="utf-8").read()
    assert '400' in text, "thumbnail.svg must have 400px dimensions"


def test_thumbnail_has_amber_wire_color():
    text = open(THUMBNAIL, encoding="utf-8").read()
    assert "#C8881A" in text or "c8881a" in text.lower(), (
        "thumbnail.svg must use amber wire color #C8881A"
    )


def test_thumbnail_has_sinai_label():
    text = open(THUMBNAIL, encoding="utf-8").read()
    assert "סיני" in text, "thumbnail.svg must include the Hebrew word סיני (Sinai)"


def test_thumbnail_has_dark_parchment_background():
    text = open(THUMBNAIL, encoding="utf-8").read()
    assert "#1A1208" in text or "1a1208" in text.lower(), (
        "thumbnail.svg background must be dark parchment #1A1208"
    )


# ---------------------------------------------------------------------------
# Pure-Python Wireworld rule verification (isolated unit tests)
# These re-implement the core CA rules to verify correctness independently
# of the JavaScript implementation.
# ---------------------------------------------------------------------------

EMPTY     = 0
CONDUCTOR = 1
E_HEAD    = 2
E_TAIL    = 3


def wireworld_step(grid, cols, rows):
    """Advance one Wireworld generation. Returns new grid (list of ints)."""
    def get(cx, cy):
        if cx < 0 or cy < 0 or cx >= cols or cy >= rows:
            return EMPTY
        return grid[cy * cols + cx]

    def count_heads(cx, cy):
        count = 0
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                if dx == 0 and dy == 0:
                    continue
                if get(cx + dx, cy + dy) == E_HEAD:
                    count += 1
        return count

    new_grid = [EMPTY] * (cols * rows)
    for cy in range(rows):
        for cx in range(cols):
            state = get(cx, cy)
            if state == EMPTY:
                new_grid[cy * cols + cx] = EMPTY
            elif state == E_HEAD:
                new_grid[cy * cols + cx] = E_TAIL
            elif state == E_TAIL:
                new_grid[cy * cols + cx] = CONDUCTOR
            else:  # CONDUCTOR
                n = count_heads(cx, cy)
                new_grid[cy * cols + cx] = E_HEAD if n in (1, 2) else CONDUCTOR
    return new_grid


def make_grid(cols, rows):
    return [EMPTY] * (cols * rows)


def set_cell(grid, cols, cx, cy, val):
    grid[cy * cols + cx] = val


def get_cell(grid, cols, cx, cy):
    return grid[cy * cols + cx]


class TestWireworldRules:

    def test_empty_stays_empty(self):
        """EMPTY cells never change state."""
        cols, rows = 3, 3
        grid = make_grid(cols, rows)
        # All cells are EMPTY
        next_g = wireworld_step(grid, cols, rows)
        assert all(c == EMPTY for c in next_g)

    def test_electron_head_becomes_tail(self):
        """E_HEAD → E_TAIL unconditionally."""
        cols, rows = 3, 3
        grid = make_grid(cols, rows)
        set_cell(grid, cols, 1, 1, E_HEAD)
        next_g = wireworld_step(grid, cols, rows)
        assert get_cell(next_g, cols, 1, 1) == E_TAIL

    def test_electron_tail_becomes_conductor(self):
        """E_TAIL → CONDUCTOR unconditionally."""
        cols, rows = 3, 3
        grid = make_grid(cols, rows)
        set_cell(grid, cols, 1, 1, E_TAIL)
        next_g = wireworld_step(grid, cols, rows)
        assert get_cell(next_g, cols, 1, 1) == CONDUCTOR

    def test_conductor_with_zero_heads_stays_conductor(self):
        """A CONDUCTOR with no E_HEAD neighbors stays CONDUCTOR."""
        cols, rows = 3, 3
        grid = make_grid(cols, rows)
        set_cell(grid, cols, 1, 1, CONDUCTOR)
        next_g = wireworld_step(grid, cols, rows)
        assert get_cell(next_g, cols, 1, 1) == CONDUCTOR

    def test_conductor_with_one_head_neighbor_fires(self):
        """A CONDUCTOR with exactly 1 E_HEAD neighbor becomes E_HEAD."""
        cols, rows = 3, 3
        grid = make_grid(cols, rows)
        set_cell(grid, cols, 1, 1, CONDUCTOR)
        set_cell(grid, cols, 0, 1, E_HEAD)  # one neighbor
        next_g = wireworld_step(grid, cols, rows)
        assert get_cell(next_g, cols, 1, 1) == E_HEAD

    def test_conductor_with_two_head_neighbors_fires(self):
        """A CONDUCTOR with exactly 2 E_HEAD neighbors becomes E_HEAD."""
        cols, rows = 5, 5
        grid = make_grid(cols, rows)
        set_cell(grid, cols, 2, 2, CONDUCTOR)
        set_cell(grid, cols, 1, 2, E_HEAD)
        set_cell(grid, cols, 3, 2, E_HEAD)
        next_g = wireworld_step(grid, cols, rows)
        assert get_cell(next_g, cols, 2, 2) == E_HEAD

    def test_conductor_with_three_heads_stays_conductor(self):
        """A CONDUCTOR with 3 E_HEAD neighbors stays CONDUCTOR (no firing)."""
        cols, rows = 5, 5
        grid = make_grid(cols, rows)
        set_cell(grid, cols, 2, 2, CONDUCTOR)
        set_cell(grid, cols, 1, 2, E_HEAD)
        set_cell(grid, cols, 3, 2, E_HEAD)
        set_cell(grid, cols, 2, 1, E_HEAD)
        next_g = wireworld_step(grid, cols, rows)
        assert get_cell(next_g, cols, 2, 2) == CONDUCTOR

    def test_conductor_with_four_heads_stays_conductor(self):
        """A CONDUCTOR with 4 E_HEAD neighbors stays CONDUCTOR."""
        cols, rows = 5, 5
        grid = make_grid(cols, rows)
        set_cell(grid, cols, 2, 2, CONDUCTOR)
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            set_cell(grid, cols, 2 + dx, 2 + dy, E_HEAD)
        next_g = wireworld_step(grid, cols, rows)
        assert get_cell(next_g, cols, 2, 2) == CONDUCTOR

    def test_signal_propagates_along_wire(self):
        """A pulse should advance one cell per step along a straight wire."""
        cols, rows = 7, 3
        grid = make_grid(cols, rows)
        # Horizontal wire of conductors
        for x in range(1, 6):
            set_cell(grid, cols, x, 1, CONDUCTOR)
        # Inject at x=1
        set_cell(grid, cols, 1, 1, E_HEAD)

        # After 1 step: position 1 is TAIL, position 2 is HEAD
        g1 = wireworld_step(grid, cols, rows)
        assert get_cell(g1, cols, 1, 1) == E_TAIL
        assert get_cell(g1, cols, 2, 1) == E_HEAD

        # After 2 steps: position 1 back to CONDUCTOR, position 2 TAIL, position 3 HEAD
        g2 = wireworld_step(g1, cols, rows)
        assert get_cell(g2, cols, 1, 1) == CONDUCTOR
        assert get_cell(g2, cols, 2, 1) == E_TAIL
        assert get_cell(g2, cols, 3, 1) == E_HEAD

    def test_y_junction_splits_signal(self):
        """
        A Y-junction splits a single signal into two branches.

        Layout (cols=7, rows=4):
           col:  0 1 2 3 4 5 6
          row 0: . . . H . . .   trunk top (E_HEAD injected here)
          row 1: . . . C . . .   trunk middle (no junction cells adjacent)
          row 2: . . C C C . .   junction: left (2,2), center (3,2), right (4,2)
          row 3: . C . . . C .   left branch (1,3) and right branch (5,3)

        Step 1: HEAD@(3,0) fires (3,1) only (junction row is 2 cells away).
        Step 2: HEAD@(3,1) fires all three junction cells (2,2),(3,2),(4,2)
                simultaneously (each has exactly 1 head diagonal-neighbor).
        Step 3: (2,2) and (4,2) fire (1,3) and (5,3) respectively — the split.
                (3,2) has no conductor neighbor to fire (empty below).
        """
        cols, rows = 7, 4
        grid = make_grid(cols, rows)

        # Trunk: one conductor cell before the junction
        set_cell(grid, cols, 3, 1, CONDUCTOR)

        # Junction row: three adjacent conductors
        set_cell(grid, cols, 2, 2, CONDUCTOR)
        set_cell(grid, cols, 3, 2, CONDUCTOR)
        set_cell(grid, cols, 4, 2, CONDUCTOR)

        # Branch tips in row 3
        set_cell(grid, cols, 1, 3, CONDUCTOR)
        set_cell(grid, cols, 5, 3, CONDUCTOR)

        # Inject HEAD at trunk top
        set_cell(grid, cols, 3, 0, E_HEAD)

        # Step 1: trunk cell (3,1) fires; only (3,0) is a head neighbor of (3,1)
        g1 = wireworld_step(grid, cols, rows)
        assert get_cell(g1, cols, 3, 0) == E_TAIL, "(3,0) HEAD must become TAIL"
        assert get_cell(g1, cols, 3, 1) == E_HEAD, (
            "Trunk cell (3,1) should fire: it has exactly 1 head neighbor (3,0)"
        )
        # Junction row must not have fired yet (distance 2 from original head)
        assert get_cell(g1, cols, 2, 2) == CONDUCTOR, "(2,2) must not fire in step 1"
        assert get_cell(g1, cols, 4, 2) == CONDUCTOR, "(4,2) must not fire in step 1"

        # Step 2: (3,1) fires all three junction cells (each sees exactly 1 head)
        g2 = wireworld_step(g1, cols, rows)
        assert get_cell(g2, cols, 3, 1) == E_TAIL, "(3,1) HEAD becomes TAIL"
        assert get_cell(g2, cols, 2, 2) == E_HEAD, (
            "Left junction cell (2,2) should fire: (3,1) is its diagonal head neighbor"
        )
        assert get_cell(g2, cols, 4, 2) == E_HEAD, (
            "Right junction cell (4,2) should fire: (3,1) is its diagonal head neighbor"
        )

        # Step 3: each of (2,2) and (4,2) fires its branch tip; junction cells → TAIL
        g3 = wireworld_step(g2, cols, rows)
        assert get_cell(g3, cols, 2, 2) == E_TAIL, "(2,2) HEAD → TAIL"
        assert get_cell(g3, cols, 4, 2) == E_TAIL, "(4,2) HEAD → TAIL"
        assert get_cell(g3, cols, 1, 3) == E_HEAD, (
            "Left branch tip (1,3) should fire: (2,2) was its head neighbor"
        )
        assert get_cell(g3, cols, 5, 3) == E_HEAD, (
            "Right branch tip (5,3) should fire: (4,2) was its head neighbor"
        )

    def test_signal_does_not_fire_from_tail(self):
        """An E_TAIL neighbor does not trigger a CONDUCTOR — only E_HEAD does."""
        cols, rows = 3, 3
        grid = make_grid(cols, rows)
        set_cell(grid, cols, 1, 1, CONDUCTOR)
        set_cell(grid, cols, 0, 1, E_TAIL)  # tail, not head
        next_g = wireworld_step(grid, cols, rows)
        assert get_cell(next_g, cols, 1, 1) == CONDUCTOR

    def test_empty_cell_unaffected_by_all_neighbors(self):
        """An EMPTY cell stays EMPTY regardless of neighbors."""
        cols, rows = 3, 3
        grid = make_grid(cols, rows)
        # Surround center with every possible non-empty state
        set_cell(grid, cols, 0, 0, CONDUCTOR)
        set_cell(grid, cols, 1, 0, E_HEAD)
        set_cell(grid, cols, 2, 0, E_TAIL)
        set_cell(grid, cols, 0, 1, E_HEAD)
        # center (1,1) stays EMPTY
        set_cell(grid, cols, 1, 1, EMPTY)
        set_cell(grid, cols, 2, 1, E_HEAD)
        set_cell(grid, cols, 0, 2, E_TAIL)
        set_cell(grid, cols, 1, 2, CONDUCTOR)
        set_cell(grid, cols, 2, 2, E_HEAD)
        next_g = wireworld_step(grid, cols, rows)
        assert get_cell(next_g, cols, 1, 1) == EMPTY
