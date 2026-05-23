"""
Tests for piece 96-mst-ruth-gleaning.

Verifies that the piece directory, files, pieces.json entry, and content
all satisfy the acceptance criteria for the MST / Ruth gleaning piece.
"""
import json
import os

import pytest

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID = "96-mst-ruth-gleaning"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_pieces():
    with open(PIECES_JSON, "r", encoding="utf-8") as fh:
        return json.load(fh)


def get_piece():
    for p in load_pieces():
        if p["id"] == PIECE_ID:
            return p
    return None


def read(filename):
    path = os.path.join(PIECE_DIR, filename)
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


# ---------------------------------------------------------------------------
# Happy path: directory and file layout
# ---------------------------------------------------------------------------

def test_piece_directory_exists():
    assert os.path.isdir(PIECE_DIR), f"Piece directory {PIECE_DIR} does not exist"


def test_index_html_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "index.html")), \
        "index.html missing from piece directory"


def test_essay_md_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "essay.md")), \
        "essay.md missing from piece directory"


def test_thumbnail_svg_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "thumbnail.svg")), \
        "thumbnail.svg missing from piece directory"


def test_readme_md_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "README.md")), \
        "README.md missing from piece directory"


# ---------------------------------------------------------------------------
# pieces.json registration
# ---------------------------------------------------------------------------

def test_piece_registered_in_pieces_json():
    piece = get_piece()
    assert piece is not None, f"Piece '{PIECE_ID}' not found in pieces.json"


def test_piece_has_correct_theme():
    piece = get_piece()
    assert piece is not None
    assert "Ruth" in piece["theme"] or "harvest" in piece["theme"] or \
           "Bikkurim" in piece["theme"], \
        f"theme should relate to Ruth / harvest / Bikkurim, got: {piece['theme']!r}"


def test_piece_has_correct_technique():
    piece = get_piece()
    assert piece is not None
    technique = piece["technique"].lower()
    assert "spanning tree" in technique or "kruskal" in technique, \
        f"technique should mention spanning tree or Kruskal, got: {piece['technique']!r}"


def test_piece_paths_point_to_existing_files():
    piece = get_piece()
    assert piece is not None
    for key in ("path", "thumbnail", "essay"):
        full = os.path.join(GALLERY_ROOT, piece[key])
        assert os.path.isfile(full), \
            f"pieces.json field '{key}' points to missing file: {piece[key]}"


def test_no_duplicate_piece_id():
    pieces = load_pieces()
    ids = [p["id"] for p in pieces]
    assert ids.count(PIECE_ID) == 1, \
        f"Piece ID '{PIECE_ID}' appears {ids.count(PIECE_ID)} times in pieces.json"


# ---------------------------------------------------------------------------
# essay.md content
# ---------------------------------------------------------------------------

def test_essay_minimum_word_count():
    text = read("essay.md")
    word_count = len(text.split())
    assert word_count >= 200, \
        f"essay.md has only {word_count} words; minimum is 200"


def test_essay_mentions_ruth():
    text = read("essay.md")
    assert "Ruth" in text or "רות" in text, \
        "essay.md must mention Ruth"


def test_essay_mentions_peah():
    text = read("essay.md").lower()
    assert "peah" in text or "corner" in text or "leket" in text, \
        "essay.md must mention the law of peah / leket"


def test_essay_mentions_mikreh():
    text = read("essay.md")
    assert "mikreh" in text or "מקרה" in text or "mikreha" in text, \
        "essay.md must discuss mikreh (chance/Providence)"


def test_essay_cites_ruth_2():
    text = read("essay.md")
    assert "Ruth 2" in text or "2:2" in text or "2:3" in text, \
        "essay.md must cite Ruth chapter 2"


# ---------------------------------------------------------------------------
# index.html content
# ---------------------------------------------------------------------------

def test_index_html_uses_requestanimationframe():
    html = read("index.html")
    assert "requestAnimationFrame" in html, \
        "index.html must use requestAnimationFrame for animation"


def test_index_html_has_canvas():
    html = read("index.html")
    assert "<canvas" in html, "index.html must contain a <canvas> element"


def test_index_html_has_union_find():
    html = read("index.html")
    assert "union" in html.lower() and "find" in html.lower(), \
        "index.html must implement union-find (union and find functions)"


def test_index_html_has_kruskal_logic():
    html = read("index.html")
    assert "kruskal" in html.lower() or "sort" in html.lower(), \
        "index.html must implement Kruskal's algorithm (edge sorting/iteration)"


def test_index_html_amber_color():
    html = read("index.html")
    assert "#C8820A" in html, \
        "index.html must use accepted-edge color #C8820A (warm amber)"


def test_index_html_reject_color():
    html = read("index.html")
    assert "#8B2020" in html, \
        "index.html must use rejected-edge color #8B2020 (muted red)"


def test_index_html_background_gradient_colors():
    html = read("index.html")
    assert "#B89A50" in html, \
        "index.html must have dusty gold (#B89A50) top-of-gradient color"
    assert "#5C3D1E" in html, \
        "index.html must have field brown (#5C3D1E) bottom-of-gradient color"


def test_index_html_ruth_point():
    html = read("index.html")
    assert "Ruth" in html or "ruth" in html.lower(), \
        "index.html must distinguish Ruth's grain point"


def test_index_html_hebrew_label():
    html = read("index.html")
    assert "רות" in html, \
        "index.html must include the Hebrew label רות for Ruth's point"


def test_index_html_peah_corner_logic():
    html = read("index.html")
    assert "corner" in html.lower() or "peah" in html.lower(), \
        "index.html must implement peah corner logic"


def test_index_html_embeds_essay_text():
    essay = read("essay.md")
    html = read("index.html")
    words = [w for w in essay.split() if len(w) > 6][:10]
    found = sum(1 for w in words if w in html)
    assert found >= 5, \
        f"index.html must embed essay text (only {found}/10 sampled words found)"


# ---------------------------------------------------------------------------
# thumbnail.svg content
# ---------------------------------------------------------------------------

def test_thumbnail_is_valid_svg():
    svg = read("thumbnail.svg")
    assert "<svg" in svg and "</svg>" in svg, \
        "thumbnail.svg must be a valid SVG file"


def test_thumbnail_has_correct_dimensions():
    svg = read("thumbnail.svg")
    assert "400" in svg, \
        "thumbnail.svg should specify 400px dimensions"


def test_thumbnail_has_amber_edges():
    svg = read("thumbnail.svg")
    assert "#C8820A" in svg, \
        "thumbnail.svg must include MST edges in amber (#C8820A)"


def test_thumbnail_has_ruth_label():
    svg = read("thumbnail.svg")
    assert "רות" in svg, \
        "thumbnail.svg must include the Hebrew label רות for Ruth's point"


def test_thumbnail_has_grain_points():
    svg = read("thumbnail.svg")
    # At least a few ellipses for grain points
    assert svg.count("<ellipse") >= 10, \
        "thumbnail.svg must include at least 10 grain-point ellipses"


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

def test_essay_is_not_placeholder():
    text = read("essay.md").lower()
    for stub in ("lorem ipsum", "placeholder", "todo", "tbd"):
        assert stub not in text, \
            f"essay.md appears to contain placeholder text: '{stub}'"


def test_index_html_is_self_contained():
    """index.html must not load external JS/CSS libraries (no CDN URLs)."""
    html = read("index.html")
    for cdn in ("cdn.jsdelivr.net", "cdnjs.cloudflare.com", "unpkg.com"):
        assert cdn not in html, \
            f"index.html must be self-contained — no CDN dependency on {cdn}"


def test_pieces_json_is_valid_json_after_edit():
    with open(PIECES_JSON, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    assert isinstance(data, list)
    assert any(p["id"] == PIECE_ID for p in data)
