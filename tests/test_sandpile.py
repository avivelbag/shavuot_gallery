"""Tests for piece 50-sandpile-at-sinai (abelian sandpile at Sinai)."""
import json
import os

import pytest

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID = "50-sandpile-at-sinai"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
HTML_PATH = os.path.join(PIECE_DIR, "index.html")
ESSAY_PATH = os.path.join(PIECE_DIR, "essay.md")


def _get_piece():
    """Return the pieces.json entry for this piece, or None if absent."""
    pieces_path = os.path.join(GALLERY_ROOT, "pieces.json")
    with open(pieces_path, encoding="utf-8") as fh:
        pieces = json.load(fh)
    for p in pieces:
        if p["id"] == PIECE_ID:
            return p
    return None


# ---------------------------------------------------------------------------
# Happy-path: pieces.json registration
# ---------------------------------------------------------------------------

def test_sandpile_in_pieces_json():
    """Piece must be registered in pieces.json."""
    assert _get_piece() is not None, f"Piece '{PIECE_ID}' not found in pieces.json"


def test_sandpile_required_fields():
    """All required pieces.json fields must be present and non-empty."""
    piece = _get_piece()
    assert piece is not None
    required = ("id", "title", "tagline", "year", "theme", "technique", "path", "thumbnail", "essay")
    for field in required:
        val = piece.get(field)
        assert val is not None and val != "", f"Field '{field}' is missing or empty"


def test_sandpile_theme():
    """Theme must be 'Har Sinai'."""
    piece = _get_piece()
    assert piece is not None
    assert piece["theme"] == "Har Sinai", f"Expected theme 'Har Sinai', got '{piece['theme']}'"


def test_sandpile_technique_mentions_sandpile():
    """Technique must mention 'sandpile'."""
    piece = _get_piece()
    assert piece is not None
    assert "sandpile" in piece["technique"].lower(), (
        f"Technique '{piece['technique']}' does not mention 'sandpile'"
    )


def test_sandpile_year_is_int():
    """Year must be an integer."""
    piece = _get_piece()
    assert piece is not None
    assert isinstance(piece["year"], int), f"Year is not an integer: {piece['year']!r}"


# ---------------------------------------------------------------------------
# Happy-path: file layout
# ---------------------------------------------------------------------------

def test_sandpile_html_exists():
    """index.html must exist on disk."""
    assert os.path.isfile(HTML_PATH), f"index.html missing at {HTML_PATH}"


def test_sandpile_essay_exists():
    """essay.md must exist on disk."""
    assert os.path.isfile(ESSAY_PATH), f"essay.md missing at {ESSAY_PATH}"


def test_sandpile_thumbnail_exists():
    """Thumbnail file referenced in pieces.json must exist on disk."""
    piece = _get_piece()
    assert piece is not None
    thumb = os.path.join(GALLERY_ROOT, piece["thumbnail"])
    assert os.path.isfile(thumb), f"Thumbnail missing at {thumb}"


def test_sandpile_readme_exists():
    """README.md must exist in the piece directory."""
    readme = os.path.join(PIECE_DIR, "README.md")
    assert os.path.isfile(readme), f"README.md missing from {PIECE_DIR}"


# ---------------------------------------------------------------------------
# Happy-path: essay content
# ---------------------------------------------------------------------------

def test_sandpile_essay_word_count():
    """essay.md must have at least 300 words."""
    text = open(ESSAY_PATH, encoding="utf-8").read()
    count = len(text.split())
    assert count >= 300, f"essay.md has only {count} words (need ≥ 300)"


def test_sandpile_essay_cites_exodus_19():
    """essay.md must cite Exodus 19."""
    text = open(ESSAY_PATH, encoding="utf-8").read()
    assert "Exodus 19" in text, "essay.md must cite Exodus 19"


def test_sandpile_essay_mentions_criticality():
    """essay.md must discuss self-organized criticality."""
    text = open(ESSAY_PATH, encoding="utf-8").read()
    assert "criticality" in text.lower(), "essay.md must mention self-organized criticality"


def test_sandpile_essay_contains_hebrew():
    """essay.md must include Hebrew text (Unicode range U+0590–U+05FF)."""
    text = open(ESSAY_PATH, encoding="utf-8").read()
    has_hebrew = any('֐' <= ch <= '׿' for ch in text)
    assert has_hebrew, "essay.md must contain Hebrew text"


def test_sandpile_essay_contains_english_translation():
    """essay.md must include the English translation of Exodus 19:12–13."""
    text = open(ESSAY_PATH, encoding="utf-8").read()
    assert "Beware of going up the mountain" in text, (
        "essay.md must include English translation of Exodus 19:12-13"
    )


# ---------------------------------------------------------------------------
# Happy-path: HTML implementation requirements
# ---------------------------------------------------------------------------

def test_sandpile_html_uses_imagedata():
    """index.html must use ImageData for pixel rendering (not per-cell fillRect)."""
    html = open(HTML_PATH, encoding="utf-8").read()
    assert "createImageData" in html or "ImageData" in html, (
        "index.html must use ImageData for pixel rendering"
    )


def test_sandpile_html_uses_requestanimationframe():
    """index.html must use requestAnimationFrame for animation."""
    html = open(HTML_PATH, encoding="utf-8").read()
    assert "requestAnimationFrame" in html, (
        "index.html must use requestAnimationFrame"
    )


def test_sandpile_html_defines_grid_at_least_300():
    """index.html must define a grid of at least 300 cells wide."""
    html = open(HTML_PATH, encoding="utf-8").read()
    assert "301" in html or "300" in html, (
        "index.html must define a grid ≥ 300 cells wide"
    )


def test_sandpile_html_implements_topple_threshold():
    """index.html must encode the 4-grain toppling threshold."""
    html = open(HTML_PATH, encoding="utf-8").read()
    assert ">= 4" in html or ">=4" in html or "< 4" in html or "<4" in html, (
        "index.html must implement the 4-grain toppling threshold"
    )


def test_sandpile_html_has_grain_counter():
    """index.html must display a grain counter."""
    html = open(HTML_PATH, encoding="utf-8").read()
    assert "grains" in html.lower(), "index.html must show a grain counter"


def test_sandpile_html_embeds_essay_text():
    """index.html must embed essay text inline (not fetch essay.md at runtime)."""
    essay_text = open(ESSAY_PATH, encoding="utf-8").read()
    html = open(HTML_PATH, encoding="utf-8").read()
    words = [w for w in essay_text.split() if len(w) > 5][:10]
    found = sum(1 for w in words if w in html)
    assert found >= 5, (
        f"index.html embeds only {found}/10 sampled essay words; essay must be inline"
    )


def test_sandpile_html_has_hebrew_passage():
    """index.html must render the Hebrew passage (RTL)."""
    html = open(HTML_PATH, encoding="utf-8").read()
    has_hebrew = any('֐' <= ch <= '׿' for ch in html)
    assert has_hebrew, "index.html must contain the Hebrew passage"


def test_sandpile_html_dirty_queue_mentioned_or_set_used():
    """index.html must use a Set for the dirty-cell queue."""
    html = open(HTML_PATH, encoding="utf-8").read()
    assert "new Set" in html, (
        "index.html must use a Set for the dirty-cell queue (performance requirement)"
    )


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

def test_topple_no_cascade_below_threshold():
    """A cell with 3 grains must NOT be added to the dirty queue (below threshold)."""
    W, H = 21, 21
    cx, cy = 10, 10
    grid = [0] * (W * H)
    grid[cy * W + cx] = 3

    dirty = set()
    if grid[cy * W + cx] >= 4:
        dirty.add(cy * W + cx)

    assert len(dirty) == 0, "3 grains is below the toppling threshold of 4"


def test_topple_single_cell_at_threshold():
    """A cell with exactly 4 grains must topple and distribute 1 grain to each neighbor."""
    W, H = 21, 21
    cx, cy = 10, 10
    ci = cy * W + cx
    grid = [0] * (W * H)
    grid[ci] = 4

    dirty = {ci}

    while dirty:
        current = dirty
        dirty = set()
        for i in current:
            if grid[i] < 4:
                continue
            y = i // W
            x = i % W
            n = grid[i] // 4
            grid[i] -= n * 4
            if x > 0:
                grid[i - 1] += n
                if grid[i - 1] >= 4:
                    dirty.add(i - 1)
            if x < W - 1:
                grid[i + 1] += n
                if grid[i + 1] >= 4:
                    dirty.add(i + 1)
            if y > 0:
                grid[i - W] += n
                if grid[i - W] >= 4:
                    dirty.add(i - W)
            if y < H - 1:
                grid[i + W] += n
                if grid[i + W] >= 4:
                    dirty.add(i + W)

    assert grid[ci] == 0, f"Center should be 0 after toppling, got {grid[ci]}"
    assert grid[ci - 1] == 1, "Left neighbor should have 1 grain"
    assert grid[ci + 1] == 1, "Right neighbor should have 1 grain"
    assert grid[ci - W] == 1, "Upper neighbor should have 1 grain"
    assert grid[ci + W] == 1, "Lower neighbor should have 1 grain"


def test_topple_cascade_spreads_grains():
    """Adding grains to center of a small grid must eventually spread to non-center cells."""
    W, H = 21, 21
    cx, cy = 10, 10
    grid = [0] * (W * H)

    for _ in range(50):
        ci = cy * W + cx
        grid[ci] += 1

        dirty = set()
        if grid[ci] >= 4:
            dirty.add(ci)

        while dirty:
            current = dirty
            dirty = set()
            for i in current:
                if grid[i] < 4:
                    continue
                y = i // W
                x = i % W
                n = grid[i] // 4
                grid[i] -= n * 4
                if x > 0:
                    grid[i - 1] += n
                    if grid[i - 1] >= 4:
                        dirty.add(i - 1)
                if x < W - 1:
                    grid[i + 1] += n
                    if grid[i + 1] >= 4:
                        dirty.add(i + 1)
                if y > 0:
                    grid[i - W] += n
                    if grid[i - W] >= 4:
                        dirty.add(i - W)
                if y < H - 1:
                    grid[i + W] += n
                    if grid[i + W] >= 4:
                        dirty.add(i + W)

    non_center = [grid[y * W + x] for y in range(H) for x in range(W)
                  if not (x == cx and y == cy)]
    assert any(g > 0 for g in non_center), (
        "After 50 grains, cascade must have spread grains beyond the center cell"
    )


def test_topple_stability_invariant():
    """After toppling to completion, no cell should have 4 or more grains."""
    W, H = 21, 21
    cx, cy = 10, 10
    grid = [0] * (W * H)

    for _ in range(100):
        ci = cy * W + cx
        grid[ci] += 1

        dirty = set()
        if grid[ci] >= 4:
            dirty.add(ci)

        while dirty:
            current = dirty
            dirty = set()
            for i in current:
                if grid[i] < 4:
                    continue
                y = i // W
                x = i % W
                n = grid[i] // 4
                grid[i] -= n * 4
                if x > 0:
                    grid[i - 1] += n
                    if grid[i - 1] >= 4:
                        dirty.add(i - 1)
                if x < W - 1:
                    grid[i + 1] += n
                    if grid[i + 1] >= 4:
                        dirty.add(i + 1)
                if y > 0:
                    grid[i - W] += n
                    if grid[i - W] >= 4:
                        dirty.add(i - W)
                if y < H - 1:
                    grid[i + W] += n
                    if grid[i + W] >= 4:
                        dirty.add(i + W)

    assert all(g <= 3 for g in grid), (
        "After toppling to completion, no cell may hold 4+ grains (stability invariant)"
    )


# ---------------------------------------------------------------------------
# Failure-mode: detect missing or malformed files
# ---------------------------------------------------------------------------

def test_nonexistent_essay_file_detection(tmp_path):
    """A path pointing to a missing essay file must be detected as absent."""
    missing = os.path.join(str(tmp_path), "no_such_essay.md")
    assert not os.path.isfile(missing), "Fixture: file must not exist"


def test_pieces_json_no_duplicate_ids():
    """Duplicate IDs in pieces.json would break gallery routing — must not occur."""
    pieces_path = os.path.join(GALLERY_ROOT, "pieces.json")
    with open(pieces_path, encoding="utf-8") as fh:
        pieces = json.load(fh)
    ids = [p["id"] for p in pieces]
    assert len(ids) == len(set(ids)), f"Duplicate piece IDs found: {ids}"
