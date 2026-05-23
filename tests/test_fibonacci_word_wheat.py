"""Tests for the Fibonacci word wheat piece (02-fibonacci-word-wheat).

Covers the make_thumbnail helper functions, on-disk file layout, pieces.json
registration, and content requirements of the index.html and essay.md.
"""
import importlib.util
import json
import math
import os

import pytest

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", "02-fibonacci-word-wheat")
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")
PIECE_ID = "02-fibonacci-word-wheat"
PHI = (1 + math.sqrt(5)) / 2


# ---------------------------------------------------------------------------
# Load make_thumbnail module for unit tests
# ---------------------------------------------------------------------------

def _load_make_thumbnail():
    """Import make_thumbnail.py from the piece directory as a module."""
    spec = importlib.util.spec_from_file_location(
        "make_thumbnail",
        os.path.join(PIECE_DIR, "make_thumbnail.py"),
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def mt():
    """Return the make_thumbnail module."""
    return _load_make_thumbnail()


# ---------------------------------------------------------------------------
# Unit tests for fib_word
# ---------------------------------------------------------------------------

def test_fib_word_returns_1_or_2(mt):
    """fib_word must return only the values 1 or 2 for its first 200 positions."""
    for n in range(200):
        v = mt.fib_word(n)
        assert v in (1, 2), f"fib_word({n}) = {v}, expected 1 or 2"


def test_fib_word_encodes_fibonacci_word_correctly(mt):
    """Verify the first 8 characters match F(6)='01001010' (F1='1', F2='0' convention).

    fib_word returns 1 for character '1' and 2 for character '0'.
    F(6) = "01001010" → expected pattern: [2,1,2,2,1,2,1,2]
    """
    expected = [2, 1, 2, 2, 1, 2, 1, 2]
    for n, exp in enumerate(expected):
        assert mt.fib_word(n) == exp, (
            f"fib_word({n}) = {mt.fib_word(n)}, expected {exp} "
            f"(F(6) = '01001010')"
        )


def test_fib_word_density_matches_golden_ratio(mt):
    """The fraction of '1' characters in the Fibonacci word converges to 1/φ².

    In 1000 characters, the count of positions where fib_word==1 should be
    within 5% of 1000/φ² ≈ 381.
    """
    n_samples = 1000
    count_one = sum(1 for n in range(n_samples) if mt.fib_word(n) == 1)
    expected = n_samples / (PHI ** 2)
    assert abs(count_one - expected) < n_samples * 0.05, (
        f"Count of '1' values = {count_one}, expected ~{expected:.1f} (±5%)"
    )


# ---------------------------------------------------------------------------
# Unit tests for walk
# ---------------------------------------------------------------------------

def test_walk_returns_length_plus_one_points(mt):
    """walk(n) must return exactly n+1 points (start + one point per step)."""
    for length in (0, 1, 10, 987):
        pts = mt.walk(length)
        assert len(pts) == length + 1, (
            f"walk({length}) returned {len(pts)} points, expected {length + 1}"
        )


def test_walk_starts_at_origin(mt):
    """walk must always begin at (0, 0)."""
    pts = mt.walk(50)
    assert pts[0] == (0, 0), f"walk did not start at origin: {pts[0]}"


def test_walk_unit_steps(mt):
    """Each consecutive pair of points must differ by exactly one unit in x or y."""
    pts = mt.walk(100)
    for i in range(len(pts) - 1):
        dx = abs(pts[i + 1][0] - pts[i][0])
        dy = abs(pts[i + 1][1] - pts[i][1])
        assert dx + dy == 1, (
            f"Step {i}: ({pts[i]} → {pts[i+1]}) is not a unit step"
        )


def test_walk_depth16_has_987_segments(mt):
    """The F(16) walk (987 segments) must have 988 points."""
    pts = mt.walk(987)
    assert len(pts) == 988


def test_walk_empty(mt):
    """walk(0) must return a single point at the origin."""
    pts = mt.walk(0)
    assert pts == [(0, 0)]


def test_walk_bounding_box_depth16_reasonable(mt):
    """The F(16) bounding box must be strictly smaller than the walk length.

    The fractal folds back densely, so the bounding box should be much smaller
    than 987 in both dimensions — confirming the walk is not a straight line.
    """
    pts = mt.walk(987)
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    span_x = max(xs) - min(xs)
    span_y = max(ys) - min(ys)
    assert span_x < 987 and span_y < 987, "Walk does not fold back"
    assert span_x > 0 and span_y > 0, "Walk is completely degenerate"


# ---------------------------------------------------------------------------
# Unit tests for make_svg
# ---------------------------------------------------------------------------

def test_make_svg_produces_valid_svg(mt):
    """make_svg must produce a string containing SVG root element."""
    pts = mt.walk(13)
    svg = mt.make_svg(pts)
    assert "<svg" in svg and "</svg>" in svg


def test_make_svg_contains_polyline(mt):
    """make_svg must include a polyline element."""
    pts = mt.walk(13)
    svg = mt.make_svg(pts)
    assert "<polyline" in svg


def test_make_svg_background_color(mt):
    """The background rect must use the specified background color."""
    pts = mt.walk(13)
    svg = mt.make_svg(pts, bg="#1A1A1A")
    assert "#1A1A1A" in svg


def test_make_svg_respects_size(mt):
    """SVG width and height attributes must match the requested size."""
    pts = mt.walk(5)
    svg = mt.make_svg(pts, size=200)
    assert 'width="200"' in svg and 'height="200"' in svg


# ---------------------------------------------------------------------------
# File layout tests
# ---------------------------------------------------------------------------

def test_piece_directory_exists():
    """The piece directory must exist on disk."""
    assert os.path.isdir(PIECE_DIR), f"Piece directory not found: {PIECE_DIR}"


def test_index_html_exists():
    """index.html must exist in the piece directory."""
    assert os.path.isfile(os.path.join(PIECE_DIR, "index.html"))


def test_essay_md_exists():
    """essay.md must exist in the piece directory."""
    assert os.path.isfile(os.path.join(PIECE_DIR, "essay.md"))


def test_thumbnail_svg_exists():
    """thumbnail.svg must exist in the piece directory."""
    assert os.path.isfile(os.path.join(PIECE_DIR, "thumbnail.svg"))


def test_readme_md_exists():
    """README.md must exist in the piece directory."""
    assert os.path.isfile(os.path.join(PIECE_DIR, "README.md"))


def test_make_thumbnail_py_exists():
    """make_thumbnail.py must exist in the piece directory."""
    assert os.path.isfile(os.path.join(PIECE_DIR, "make_thumbnail.py"))


# ---------------------------------------------------------------------------
# thumbnail.svg content tests
# ---------------------------------------------------------------------------

def test_thumbnail_is_valid_svg():
    """thumbnail.svg must contain well-formed SVG markup."""
    path = os.path.join(PIECE_DIR, "thumbnail.svg")
    text = open(path, encoding="utf-8").read()
    assert "<svg" in text and "</svg>" in text, "thumbnail.svg is not valid SVG"


def test_thumbnail_contains_polyline():
    """thumbnail.svg must contain a polyline element."""
    path = os.path.join(PIECE_DIR, "thumbnail.svg")
    text = open(path, encoding="utf-8").read()
    assert "<polyline" in text, "thumbnail.svg does not contain a polyline"


def test_thumbnail_background_is_near_black():
    """thumbnail.svg must have a near-black (#0A0A0A) background."""
    path = os.path.join(PIECE_DIR, "thumbnail.svg")
    text = open(path, encoding="utf-8").read()
    assert "#0A0A0A" in text or "0A0A0A" in text.upper(), (
        "thumbnail.svg does not appear to use the near-black background"
    )


def test_thumbnail_uses_wheat_gold():
    """thumbnail.svg must use wheat gold (#E8C84A) for the curve."""
    path = os.path.join(PIECE_DIR, "thumbnail.svg")
    text = open(path, encoding="utf-8").read()
    assert "E8C84A" in text.upper(), (
        "thumbnail.svg does not appear to use wheat gold (#E8C84A)"
    )


# ---------------------------------------------------------------------------
# essay.md content tests
# ---------------------------------------------------------------------------

def test_essay_has_at_least_300_words():
    """essay.md must contain at least 300 words."""
    path = os.path.join(PIECE_DIR, "essay.md")
    text = open(path, encoding="utf-8").read()
    word_count = len(text.split())
    assert word_count >= 300, f"essay.md has only {word_count} words (need ≥ 300)"


def test_essay_mentions_leviticus():
    """essay.md must cite Leviticus 23 (the omer commandment)."""
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    assert "Leviticus" in text or "23:10" in text, (
        "essay.md does not mention Leviticus 23"
    )


def test_essay_mentions_fibonacci():
    """essay.md must discuss Fibonacci numbers or the Fibonacci word."""
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    assert "Fibonacci" in text, "essay.md does not mention Fibonacci"


def test_essay_mentions_sefirot_or_zohar():
    """essay.md must reference the Zohar or the sefirot grid."""
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    assert "Zohar" in text or "sefirot" in text or "sefirah" in text, (
        "essay.md does not mention the Zohar or sefirot"
    )


def test_essay_mentions_deuteronomy():
    """essay.md must cite Deuteronomy 8:8 (wheat as one of seven species)."""
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    assert "Deuteronomy" in text or "8:8" in text, (
        "essay.md does not mention Deuteronomy 8:8"
    )


# ---------------------------------------------------------------------------
# index.html content tests
# ---------------------------------------------------------------------------

def _html():
    return open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()


def test_index_html_uses_canvas():
    """index.html must contain a canvas element."""
    assert "<canvas" in _html(), "index.html does not contain a canvas element"


def test_index_html_uses_requestanimationframe():
    """index.html must use requestAnimationFrame for animation."""
    assert "requestAnimationFrame" in _html(), (
        "index.html does not use requestAnimationFrame"
    )


def test_index_html_contains_fib_word_function():
    """index.html must define the fibWord function."""
    html = _html()
    assert "fibWord" in html, "index.html does not define fibWord"


def test_index_html_contains_omer_counter_elements():
    """index.html must contain both the day and week counter display elements."""
    html = _html()
    assert "day-display" in html, "index.html missing #day-display element"
    assert "week-display" in html, "index.html missing #week-display element"


def test_index_html_embeds_essay_text():
    """index.html must embed the essay text inline (not just link to essay.md)."""
    html = _html()
    essay = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    long_words = [w for w in essay.split() if len(w) > 6][:10]
    found = sum(1 for w in long_words if w in html)
    assert found >= 5, (
        f"index.html does not appear to embed essay text "
        f"(only {found}/10 sampled words found)"
    )


def test_index_html_uses_phi_constant():
    """index.html must define the golden ratio (PHI) for the fibWord formula."""
    html = _html()
    assert "PHI" in html or "Math.sqrt(5)" in html, (
        "index.html does not appear to compute the golden ratio"
    )


def test_index_html_length_constant():
    """index.html must reference the F(22) depth-22 length 17711."""
    assert "17711" in _html(), "index.html does not reference LENGTH = 17711"


def test_index_html_hold_frames_or_seconds():
    """index.html must implement the hold/loop logic (HOLD_FRAMES or equivalent)."""
    html = _html()
    assert "HOLD_FRAMES" in html or "holdCount" in html or "holding" in html, (
        "index.html does not appear to implement hold/loop state"
    )


# ---------------------------------------------------------------------------
# pieces.json registration tests
# ---------------------------------------------------------------------------

def _load_pieces():
    with open(PIECES_JSON, encoding="utf-8") as fh:
        return json.load(fh)


def _get_piece(pid):
    return next((p for p in _load_pieces() if p["id"] == pid), None)


def test_piece_registered_in_pieces_json():
    """The piece must appear in pieces.json with the correct id."""
    piece = _get_piece(PIECE_ID)
    assert piece is not None, f"Piece '{PIECE_ID}' not found in pieces.json"


def test_piece_json_theme():
    """The piece's theme field must mention Sefirat HaOmer."""
    piece = _get_piece(PIECE_ID)
    assert piece is not None
    assert "Sefirat HaOmer" in piece.get("theme", "") or "Omer" in piece.get("theme", ""), (
        "Piece theme does not mention Sefirat HaOmer"
    )


def test_piece_json_technique():
    """The piece's technique field must mention Fibonacci."""
    piece = _get_piece(PIECE_ID)
    assert piece is not None
    assert "Fibonacci" in piece.get("technique", ""), (
        "Piece technique does not mention Fibonacci"
    )


def test_piece_json_paths_correct():
    """The path, thumbnail, and essay fields must point to existing files."""
    piece = _get_piece(PIECE_ID)
    assert piece is not None
    for field in ("path", "thumbnail", "essay"):
        full = os.path.join(GALLERY_ROOT, piece[field])
        assert os.path.isfile(full), (
            f"Piece field '{field}' = '{piece[field]}' does not exist on disk"
        )


def test_piece_json_no_duplicate_id():
    """The new piece ID must appear exactly once in pieces.json."""
    pieces = _load_pieces()
    ids = [p["id"] for p in pieces]
    count = ids.count(PIECE_ID)
    assert count == 1, f"ID '{PIECE_ID}' appears {count} times in pieces.json"


# ---------------------------------------------------------------------------
# make_thumbnail regeneration test
# ---------------------------------------------------------------------------

def test_make_thumbnail_regenerates_svg(tmp_path, mt):
    """Running walk + make_svg must produce valid SVG output."""
    pts = mt.walk(987)
    svg = mt.make_svg(pts)
    out = tmp_path / "thumb.svg"
    out.write_text(svg, encoding="utf-8")
    content = out.read_text(encoding="utf-8")
    assert "<svg" in content
    assert "<polyline" in content
    assert "E8C84A" in content.upper()


# ---------------------------------------------------------------------------
# Edge-case / failure-mode tests
# ---------------------------------------------------------------------------

def test_walk_large_input_does_not_crash(mt):
    """walk must handle a moderately large input (depth 22 = 17711) without error."""
    pts = mt.walk(17711)
    assert len(pts) == 17712


def test_make_svg_single_point_does_not_crash(mt):
    """make_svg with a two-point degenerate walk must not raise an exception."""
    pts = mt.walk(1)
    svg = mt.make_svg(pts)
    assert "<svg" in svg


def test_missing_thumbnail_would_fail(tmp_path):
    """Confirm that a missing thumbnail path is detectable (sanity fixture)."""
    missing = os.path.join(str(tmp_path), "nonexistent.svg")
    assert not os.path.isfile(missing)


def test_empty_essay_would_fail(tmp_path):
    """Confirm that an empty essay.md would fail the word-count check."""
    empty = tmp_path / "essay.md"
    empty.write_text("", encoding="utf-8")
    word_count = len(empty.read_text().split())
    assert word_count < 300
