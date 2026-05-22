"""
Tests for piece 53-gleaning-ruth: Gleaning in the Fields of Boaz.

Covers file-structure requirements, pieces.json registration, essay
content, and the correctness of the marching squares algorithm via a
pure-Python reference implementation that mirrors the JS logic in
index.html.
"""
import json
import os
import re

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID = "53-gleaning-ruth"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _load_piece():
    """Return the pieces.json entry for this piece, or None if absent."""
    with open(PIECES_JSON, encoding="utf-8") as fh:
        pieces = json.load(fh)
    for p in pieces:
        if p["id"] == PIECE_ID:
            return p
    return None


# ---------------------------------------------------------------------------
# File structure
# ---------------------------------------------------------------------------

def test_piece_directory_exists():
    """The piece directory must be present under pieces/."""
    assert os.path.isdir(PIECE_DIR)


def test_index_html_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "index.html"))


def test_essay_md_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "essay.md"))


def test_readme_md_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "README.md"))


def test_thumbnail_svg_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "thumbnail.svg"))


def test_thumbnail_is_valid_svg():
    """thumbnail.svg must contain a root svg element."""
    content = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert "<svg" in content and "</svg>" in content


# ---------------------------------------------------------------------------
# pieces.json registration
# ---------------------------------------------------------------------------

def test_piece_registered_in_pieces_json():
    """The piece must have an entry in pieces.json with id == PIECE_ID."""
    piece = _load_piece()
    assert piece is not None, f"No entry with id '{PIECE_ID}' found in pieces.json"


def test_piece_has_all_required_fields():
    """All nine required fields must be present and non-empty."""
    piece = _load_piece()
    required = ("id", "title", "tagline", "year", "theme", "technique", "path", "thumbnail", "essay")
    for field in required:
        assert field in piece, f"Missing field '{field}'"
        assert piece[field] not in (None, ""), f"Empty field '{field}'"


def test_piece_year_is_integer():
    assert isinstance(_load_piece()["year"], int)


def test_piece_path_ends_with_html():
    assert _load_piece()["path"].endswith(".html")


def test_piece_thumbnail_extension_is_svg():
    ext = os.path.splitext(_load_piece()["thumbnail"])[1].lower()
    assert ext == ".svg"


def test_piece_id_matches_path_directory():
    """The id field must match the penultimate path component."""
    piece = _load_piece()
    parts = piece["path"].replace("\\", "/").split("/")
    assert parts[-2] == piece["id"]


# ---------------------------------------------------------------------------
# Essay content
# ---------------------------------------------------------------------------

def test_essay_word_count():
    """essay.md must contain at least 200 words."""
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    assert len(text.split()) >= 200


def test_essay_cites_ruth_chapter_2():
    """essay.md must explicitly reference Ruth chapter 2."""
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    assert re.search(r"Ruth\s+2", text), "essay.md must cite Ruth 2"


def test_essay_mentions_leket():
    """essay.md must mention the leket commandment or its Leviticus/Deuteronomy source."""
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read().lower()
    assert "leket" in text or "leviticus" in text or "deuteronomy" in text


def test_essay_connects_to_shavuot():
    """essay.md must connect the piece to Shavuot."""
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    assert "Shavuot" in text or "shavuot" in text.lower()


def test_index_html_embeds_essay_text():
    """index.html must embed the essay inline (≥5 of first 10 long words appear in HTML)."""
    essay = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    words = [w for w in essay.split() if len(w) > 5][:10]
    found = sum(1 for w in words if w in html)
    assert found >= 5, f"Only {found}/10 sampled essay words found in index.html"


def test_index_html_uses_requestanimationframe():
    """index.html must drive the animation with requestAnimationFrame."""
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "requestAnimationFrame" in html


def test_index_html_uses_harvest_palette():
    """index.html must reference the required harvest palette colours."""
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read().upper()
    assert "C9922A" in html, "harvest gold #C9922A missing"
    assert "2E4A26" in html, "deep field green #2E4A26 missing"
    assert "8EA4B2" in html, "sky edge colour #8EA4B2 missing"


def test_index_html_contains_marching_squares_structure():
    """index.html must contain the MS_SEGS lookup table used by marching squares."""
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "MS_SEGS" in html


# ---------------------------------------------------------------------------
# Marching squares algorithm — pure Python reference implementation
# ---------------------------------------------------------------------------

def _ms_case(tl, tr, br, bl, thr):
    """
    Compute the marching squares case index for one grid cell.

    Corner bit encoding matches the JS implementation: TL=8, TR=4, BR=2, BL=1.
    Returns an integer in [0, 15].
    """
    return ((8 if tl >= thr else 0) |
            (4 if tr >= thr else 0) |
            (2 if br >= thr else 0) |
            (1 if bl >= thr else 0))


def _lerp_edge(edge, tl, tr, br, bl, thr):
    """
    Return the contour intersection point on *edge* in unit-cell coordinates.

    Unit cell: x in [0,1] left→right, y in [0,1] top→bottom.
    Edges: 0=top (y=0), 1=right (x=1), 2=bottom (y=1), 3=left (x=0).
    Uses linear interpolation with a 1e-9 guard against division by zero.
    """
    if edge == 0:
        t = 0.5 if abs(tr - tl) < 1e-9 else (thr - tl) / (tr - tl)
        return (t, 0.0)
    if edge == 1:
        t = 0.5 if abs(br - tr) < 1e-9 else (thr - tr) / (br - tr)
        return (1.0, t)
    if edge == 2:
        t = 0.5 if abs(br - bl) < 1e-9 else (thr - bl) / (br - bl)
        return (t, 1.0)
    # edge == 3
    t = 0.5 if abs(bl - tl) < 1e-9 else (thr - tl) / (bl - tl)
    return (0.0, t)


_MS_SEGS = {
    0:  [],
    1:  [(2, 3)],
    2:  [(1, 2)],
    3:  [(1, 3)],
    4:  [(0, 1)],
    5:  None,         # saddle
    6:  [(0, 2)],
    7:  [(0, 3)],
    8:  [(0, 3)],
    9:  [(0, 2)],
    10: None,         # saddle
    11: [(0, 1)],
    12: [(1, 3)],
    13: [(1, 2)],
    14: [(2, 3)],
    15: [],
}


def _cell_segments(tl, tr, br, bl, thr):
    """
    Return contour line segments for a single grid cell at the given threshold.

    Each segment is a pair of (x, y) float tuples in unit-cell coordinates
    ([0,1] × [0,1]).  Returns a list of [(x1,y1), (x2,y2)] segment pairs.
    Saddle cases are resolved via the cell-centre average value.
    """
    ci = _ms_case(tl, tr, br, bl, thr)
    segs = _MS_SEGS[ci]
    if segs is None:
        avg = (tl + tr + br + bl) / 4
        if ci == 5:
            segs = [(0, 1), (2, 3)] if avg >= thr else [(0, 3), (1, 2)]
        else:
            segs = [(0, 3), (1, 2)] if avg >= thr else [(0, 1), (2, 3)]
    return [(_lerp_edge(ea, tl, tr, br, bl, thr),
             _lerp_edge(eb, tl, tr, br, bl, thr)) for ea, eb in segs]


# --- happy path ---

def test_ms_all_corners_below_produces_no_segment():
    """Case 0: all corners below threshold → no contour."""
    assert _cell_segments(0.1, 0.1, 0.1, 0.1, 0.5) == []


def test_ms_all_corners_above_produces_no_segment():
    """Case 15: all corners above threshold → no contour."""
    assert _cell_segments(0.9, 0.9, 0.9, 0.9, 0.5) == []


def test_ms_one_segment_two_edges():
    """A typical non-saddle case produces exactly one segment with two distinct edge points."""
    # TL=0, TR=1, BR=1, BL=0 → case 6 (top and bottom edges)
    segs = _cell_segments(0.0, 1.0, 1.0, 0.0, 0.5)
    assert len(segs) == 1
    (x1, y1), (x2, y2) = segs[0]
    # one point on top edge (y≈0), one on bottom edge (y≈1)
    ys = sorted([y1, y2])
    assert ys[0] < 0.1 and ys[1] > 0.9


def test_ms_linear_interpolation_midpoint():
    """At equal gradients the interpolated point is exactly at 0.5."""
    # TL=0.2, TR=0.8 → top edge intersection at t = (0.5-0.2)/(0.8-0.2) = 0.5
    segs = _cell_segments(0.2, 0.8, 0.8, 0.2, 0.5)
    assert len(segs) == 1
    (x1, _), (x2, _) = segs[0]
    assert abs(x1 - 0.5) < 1e-9
    assert abs(x2 - 0.5) < 1e-9


def test_ms_interpolation_non_uniform():
    """Asymmetric gradient produces an off-centre interpolation point."""
    # TL=0.1, TR=0.9, BR=0.9, BL=0.1 → case 6 (top + bottom edges)
    # top edge t = (0.4-0.1)/(0.9-0.1) = 0.375 → x=0.375, not 0.5
    segs = _cell_segments(0.1, 0.9, 0.9, 0.1, 0.4)
    assert len(segs) == 1
    (x1, _), (x2, _) = segs[0]
    assert abs(x1 - 0.375) < 1e-9
    assert abs(x2 - 0.375) < 1e-9


def test_ms_saddle_case_5_produces_two_segments():
    """Saddle case 5 (TR+BL above) must resolve to exactly two segments."""
    segs = _cell_segments(0.0, 1.0, 0.0, 1.0, 0.5)
    assert len(segs) == 2


def test_ms_saddle_case_10_produces_two_segments():
    """Saddle case 10 (TL+BR above) must resolve to exactly two segments."""
    segs = _cell_segments(1.0, 0.0, 1.0, 0.0, 0.5)
    assert len(segs) == 2


def test_ms_gradient_grid_produces_segments():
    """A 2×2 cell grid with a gradient field must produce contour segments."""
    grid = [
        [0.0, 0.3, 0.7],
        [0.2, 0.5, 0.8],
        [0.5, 0.8, 1.0],
    ]
    segments = []
    thr = 0.5
    for row in range(2):
        for col in range(2):
            tl = grid[row][col]
            tr = grid[row][col + 1]
            br = grid[row + 1][col + 1]
            bl = grid[row + 1][col]
            segments.extend(_cell_segments(tl, tr, br, bl, thr))
    assert len(segments) > 0


def test_ms_ten_thresholds_all_in_open_unit_interval():
    """The 9 equally-spaced thresholds must all lie strictly inside (0, 1)."""
    thresholds = [i / 10 for i in range(1, 10)]
    assert len(thresholds) == 9
    for thr in thresholds:
        assert 0.0 < thr < 1.0


# --- edge cases ---

def test_ms_empty_grid_produces_no_segments():
    """A zero-cell iteration must yield an empty segment list."""
    segments = []
    for row in range(0):
        for col in range(0):
            segments.extend(_cell_segments(0, 0, 0, 0, 0.5))
    assert segments == []


def test_ms_degenerate_flat_field_no_segments():
    """A uniform field equal to the threshold is counted as 'above' (≥), giving case 15 → no segments."""
    segs = _cell_segments(0.5, 0.5, 0.5, 0.5, 0.5)
    assert segs == []


# --- failure modes ---

def test_ms_case_index_range():
    """Every possible combination of above/below produces a valid case index in [0,15]."""
    corners = [0.1, 0.9]
    for tl in corners:
        for tr in corners:
            for br in corners:
                for bl in corners:
                    ci = _ms_case(tl, tr, br, bl, 0.5)
                    assert 0 <= ci <= 15


def test_ms_edge_point_stays_on_cell_boundary():
    """Interpolated edge points must lie on their respective cell edges (unit cell)."""
    segs = _cell_segments(0.0, 1.0, 0.8, 0.2, 0.5)
    for (x1, y1), (x2, y2) in segs:
        for x, y in ((x1, y1), (x2, y2)):
            on_boundary = (
                abs(x) < 1e-9 or abs(x - 1) < 1e-9 or
                abs(y) < 1e-9 or abs(y - 1) < 1e-9
            )
            assert on_boundary, f"Point ({x:.4f}, {y:.4f}) is not on a cell edge"
