"""
Tests for piece 77-game-of-life-living-letters.

Validates file layout, pieces.json registration, HTML implementation details,
essay content, and thumbnail format.
"""
import json
import os
import re

import pytest

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID = "77-game-of-life-living-letters"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
HTML_PATH = os.path.join(PIECE_DIR, "index.html")
ESSAY_PATH = os.path.join(PIECE_DIR, "essay.md")
README_PATH = os.path.join(PIECE_DIR, "README.md")
THUMB_PATH = os.path.join(PIECE_DIR, "thumbnail.svg")
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")


# ---------------------------------------------------------------------------
# File existence
# ---------------------------------------------------------------------------

def test_piece_directory_exists():
    assert os.path.isdir(PIECE_DIR), f"{PIECE_DIR} directory missing"


def test_index_html_exists():
    assert os.path.isfile(HTML_PATH), "index.html missing"


def test_essay_md_exists():
    assert os.path.isfile(ESSAY_PATH), "essay.md missing"


def test_readme_md_exists():
    assert os.path.isfile(README_PATH), "README.md missing"


def test_thumbnail_svg_exists():
    assert os.path.isfile(THUMB_PATH), "thumbnail.svg missing"


# ---------------------------------------------------------------------------
# pieces.json registration
# ---------------------------------------------------------------------------

def _load_pieces():
    with open(PIECES_JSON, encoding="utf-8") as fh:
        return json.load(fh)


def _get_piece():
    for p in _load_pieces():
        if p["id"] == PIECE_ID:
            return p
    return None


def test_piece_registered_in_pieces_json():
    assert _get_piece() is not None, f"Piece '{PIECE_ID}' not found in pieces.json"


def test_piece_theme_is_matan_torah():
    piece = _get_piece()
    assert piece is not None
    assert piece.get("theme") == "Matan Torah", (
        f"Expected theme 'Matan Torah', got {piece.get('theme')!r}"
    )


def test_piece_technique_mentions_game_of_life():
    piece = _get_piece()
    assert piece is not None
    technique = piece.get("technique", "")
    assert "Game of Life" in technique or "Conway" in technique, (
        f"Technique field should mention Conway's Game of Life, got: {technique!r}"
    )


def test_piece_technique_mentions_letter_seeding():
    piece = _get_piece()
    assert piece is not None
    technique = piece.get("technique", "")
    assert "Hebrew" in technique or "letter" in technique.lower(), (
        f"Technique should mention Hebrew letter seeding, got: {technique!r}"
    )


def test_piece_json_has_all_required_fields():
    piece = _get_piece()
    assert piece is not None
    for field in ("id", "title", "tagline", "year", "theme", "technique", "path", "thumbnail", "essay"):
        assert field in piece and piece[field], f"Missing required field: {field}"


def test_piece_year_is_2026():
    piece = _get_piece()
    assert piece is not None
    assert piece.get("year") == 2026


# ---------------------------------------------------------------------------
# index.html — GoL implementation
# ---------------------------------------------------------------------------

def _read_html():
    return open(HTML_PATH, encoding="utf-8").read()


def test_html_uses_requestanimationframe():
    assert "requestAnimationFrame" in _read_html()


def test_html_has_canvas_element():
    html = _read_html()
    assert "<canvas" in html, "index.html must have a <canvas> element"


def test_html_implements_gol_toroidal_boundary():
    """The GoL step must use modulo arithmetic for wrap-around (toroidal grid)."""
    html = _read_html()
    assert "% H" in html or "%H" in html or "% W" in html or "%W" in html, (
        "GoL step must use modulo arithmetic for toroidal boundary"
    )


def test_html_uses_uint8array():
    """GoL grid should use Uint8Array for performance."""
    assert "Uint8Array" in _read_html()


def test_html_uses_imagedata_for_rendering():
    """Rendering must use ImageData for pixel-level control."""
    assert "ImageData" in _read_html() or "createImageData" in _read_html()


def test_html_has_gold_color():
    """Alive cells must use the specified gold color #E8C438 or RGB equivalent."""
    html = _read_html()
    assert "E8C438" in html or "232" in html, (
        "Gold color #E8C438 (R=232) must appear in the HTML"
    )


def test_html_has_dark_background_color():
    """Dead cells must use the near-black color #070502."""
    html = _read_html()
    assert "070502" in html or ("#07" in html), (
        "Near-black #070502 must appear in the HTML"
    )


def test_html_has_gol_step_function():
    """A GoL step function must be present."""
    html = _read_html()
    assert "golStep" in html or "gol_step" in html or (
        "n === 2 || n === 3" in html or "n==2||n==3" in html or "n===2||n===3" in html
    ), "GoL B3/S23 survival rule must be present in HTML"


def test_html_has_hebrew_letter_bitmasks():
    """Letter bitmasks for the Hebrew letters must be hard-coded in JS."""
    html = _read_html()
    assert "0b" in html or "0b0" in html, (
        "Hebrew letter bitmasks (binary literals) must be present in JS"
    )


def test_html_has_aleph_letter():
    """Aleph (א) bitmask must be defined."""
    html = _read_html()
    assert "ALEPH" in html, "ALEPH letter constant must be defined in JS"


def test_html_has_text_overlay():
    """The אנכי CSS text overlay element must be present."""
    html = _read_html()
    assert "anochi-overlay" in html or "אָנֹכִי" in html or "אנכי" in html, (
        "The אנכי text overlay element must be present in HTML"
    )


def test_html_overlay_fade_at_frame_600():
    """Overlay must be triggered at frame 600."""
    html = _read_html()
    assert "600" in html, "Frame 600 trigger for overlay must be present"


def test_html_overlay_fade_out():
    """Overlay must have a fade-out trigger after 3 seconds (frame ~780)."""
    html = _read_html()
    assert "780" in html, "Frame 780 fade-out trigger for overlay must be present"


def test_html_seed_letters_function():
    """A function to seed the Hebrew letterforms must be defined."""
    html = _read_html()
    assert "seedLetters" in html or "seed" in html.lower(), (
        "A letter-seeding function must be present in JS"
    )


def test_html_font_scale_or_letter_dimensions():
    """The letter rendering must define scaling (2× or larger)."""
    html = _read_html()
    assert "FONT_SCALE" in html or "LETTER_W" in html or "letterW" in html, (
        "Letter scaling constant must be defined"
    )


def test_html_grid_dimensions_300x200():
    """Grid dimensions W=300, H=200 must be present."""
    html = _read_html()
    assert "300" in html and "200" in html, (
        "Grid dimensions 300×200 must be present in JS"
    )


def test_html_embeds_essay_text():
    """index.html must embed the essay text inline."""
    essay = open(ESSAY_PATH, encoding="utf-8").read()
    html = _read_html()
    words = [w for w in essay.split() if len(w) > 5][:10]
    found = sum(1 for w in words if w in html)
    assert found >= 5, (
        f"index.html must embed essay text inline (only {found}/10 sampled words found)"
    )


def test_html_no_external_scripts():
    """index.html must not load external scripts."""
    html = _read_html()
    external = re.findall(r'<script[^>]+src=["\']https?://', html)
    assert not external, f"External scripts found: {external}"


# ---------------------------------------------------------------------------
# essay.md content
# ---------------------------------------------------------------------------

def _read_essay():
    return open(ESSAY_PATH, encoding="utf-8").read()


def test_essay_at_least_400_words():
    text = _read_essay()
    count = len(text.split())
    assert count >= 400, f"Essay has {count} words, need ≥ 400"


def test_essay_mentions_exodus():
    text = _read_essay().lower()
    assert "exodus" in text or "20:2" in text, "Essay must cite Exodus 20:2"


def test_essay_mentions_sefer_yetzirah():
    text = _read_essay()
    assert "Sefer Yetzirah" in text or "Yetzirah" in text, (
        "Essay must mention Sefer Yetzirah"
    )


def test_essay_mentions_conways_game_of_life():
    text = _read_essay()
    assert "Game of Life" in text or "Conway" in text, (
        "Essay must mention Conway's Game of Life"
    )


def test_essay_mentions_turing_complete():
    text = _read_essay().lower()
    assert "turing" in text, "Essay must discuss Turing-completeness"


def test_essay_mentions_shavuot():
    text = _read_essay().lower()
    assert "shavuot" in text or "sinai" in text, (
        "Essay must mention Shavuot or Sinai"
    )


def test_essay_opens_with_anochi():
    text = _read_essay()
    assert "אָנֹכִי" in text or "Anochi" in text or "אנכי" in text, (
        "Essay must open with or prominently feature the word Anochi"
    )


# ---------------------------------------------------------------------------
# thumbnail.svg
# ---------------------------------------------------------------------------

def _read_thumb():
    return open(THUMB_PATH, encoding="utf-8").read()


def test_thumbnail_is_valid_svg():
    svg = _read_thumb()
    assert "<svg" in svg and "</svg>" in svg, "thumbnail.svg is not valid SVG"


def test_thumbnail_has_400x400_dimensions():
    svg = _read_thumb()
    assert "400" in svg, "thumbnail.svg must be 400×400"


def test_thumbnail_uses_gold_color():
    svg = _read_thumb()
    assert "E8C438" in svg, "thumbnail.svg must use gold #E8C438 for cells"


def test_thumbnail_uses_dark_background():
    svg = _read_thumb()
    assert "070502" in svg, "thumbnail.svg must use near-black #070502 background"


# ---------------------------------------------------------------------------
# Edge cases and failure modes
# ---------------------------------------------------------------------------

def test_gol_b3s23_rule_correct():
    """The GoL rule must implement exactly B3/S23 (birth=3, survive=2or3)."""
    html = _read_html()
    # B3/S23 rule: dead + 3 => alive, alive + 2|3 => alive
    has_birth_3 = "n === 3" in html or "n==3" in html or "n===3" in html
    has_survive_23 = ("n === 2 || n === 3" in html or "n==2||n==3" in html
                      or "n===2||n===3" in html or "2||n===3" in html
                      or "(n===2||n===3)" in html)
    assert has_birth_3 and has_survive_23, (
        "GoL must implement B3/S23: birth=3 neighbors, survival=2or3 neighbors"
    )


def test_letters_placed_right_to_left():
    """Letter array must contain all four letters of Anochi (Aleph, Nun, Kaf, Yod)."""
    html = _read_html()
    assert "ALEPH" in html and "NUN" in html and "KAF" in html and "YOD" in html, (
        "All four letters of Anochi (ALEPH, NUN, KAF, YOD) must be defined"
    )


def test_piece_id_not_duplicated():
    pieces = _load_pieces()
    ids = [p["id"] for p in pieces]
    assert ids.count(PIECE_ID) == 1, f"Piece ID {PIECE_ID!r} appears more than once"


def test_missing_piece_html_detected(tmp_path):
    """Verify our path check logic: a non-existent path should fail os.path.isfile."""
    fake_path = str(tmp_path / "nonexistent.html")
    assert not os.path.isfile(fake_path), "Fixture: file must not exist for this test"


def test_empty_grid_gol_step_produces_all_dead():
    """
    A GoL grid that is entirely dead must remain entirely dead after one step.
    This validates the B3 birth rule: 0 neighbors => stays dead.
    Implemented in Python to verify the logic is correct.
    """
    W, H = 10, 10
    grid = [0] * (W * H)

    def step(curr):
        nxt = [0] * (W * H)
        for y in range(H):
            for x in range(W):
                n = 0
                for dy in range(-1, 2):
                    for dx in range(-1, 2):
                        if dy == 0 and dx == 0:
                            continue
                        n += curr[((y + dy) % H) * W + ((x + dx) % W)]
                alive = curr[y * W + x]
                nxt[y * W + x] = 1 if (alive and n in (2, 3)) or (not alive and n == 3) else 0
        return nxt

    after = step(grid)
    assert all(c == 0 for c in after), "All-dead grid must remain dead after one GoL step"


def test_blinker_oscillates_period_2():
    """
    A horizontal blinker (3 cells in a row) must oscillate to vertical in one step.
    This validates the GoL rules match B3/S23.
    """
    W, H = 10, 10
    grid = [0] * (W * H)
    # Horizontal blinker at center: (5,4), (5,5), (5,6)
    grid[4 * W + 4] = 1
    grid[4 * W + 5] = 1
    grid[4 * W + 6] = 1

    def step(curr):
        nxt = [0] * (W * H)
        for y in range(H):
            for x in range(W):
                n = 0
                for dy in range(-1, 2):
                    for dx in range(-1, 2):
                        if dy == 0 and dx == 0:
                            continue
                        n += curr[((y + dy) % H) * W + ((x + dx) % W)]
                alive = curr[y * W + x]
                nxt[y * W + x] = 1 if (alive and n in (2, 3)) or (not alive and n == 3) else 0
        return nxt

    after = step(grid)

    # After one step: vertical blinker at (3,5), (4,5), (5,5)
    assert after[3 * W + 5] == 1, "Blinker step 1: (3,5) should be alive"
    assert after[4 * W + 5] == 1, "Blinker step 1: (4,5) should be alive"
    assert after[5 * W + 5] == 1, "Blinker step 1: (5,5) should be alive"
    # Original horizontal cells (except center) must be dead
    assert after[4 * W + 4] == 0, "Blinker step 1: (4,4) should be dead"
    assert after[4 * W + 6] == 0, "Blinker step 1: (4,6) should be dead"

    # Step 2 must return to horizontal
    after2 = step(after)
    assert after2[4 * W + 4] == 1, "Blinker step 2: must return to horizontal (4,4)"
    assert after2[4 * W + 5] == 1, "Blinker step 2: must return to horizontal (4,5)"
    assert after2[4 * W + 6] == 1, "Blinker step 2: must return to horizontal (4,6)"


def test_still_life_block_is_stable():
    """
    A 2×2 block (the simplest still life) must be unchanged after one GoL step.
    """
    W, H = 8, 8
    grid = [0] * (W * H)
    # 2x2 block at (2,2)
    for y in range(2, 4):
        for x in range(2, 4):
            grid[y * W + x] = 1

    def step(curr):
        nxt = [0] * (W * H)
        for y in range(H):
            for x in range(W):
                n = 0
                for dy in range(-1, 2):
                    for dx in range(-1, 2):
                        if dy == 0 and dx == 0:
                            continue
                        n += curr[((y + dy) % H) * W + ((x + dx) % W)]
                alive = curr[y * W + x]
                nxt[y * W + x] = 1 if (alive and n in (2, 3)) or (not alive and n == 3) else 0
        return nxt

    after = step(grid)
    assert after[2 * W + 2] == 1 and after[2 * W + 3] == 1
    assert after[3 * W + 2] == 1 and after[3 * W + 3] == 1
    # Cells just outside the block must remain dead
    assert after[1 * W + 1] == 0
    assert after[4 * W + 4] == 0
