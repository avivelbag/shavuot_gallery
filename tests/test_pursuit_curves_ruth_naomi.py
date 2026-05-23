"""
Tests for piece 97-pursuit-curves-ruth-naomi.

Verifies directory layout, pieces.json registration, essay content, canvas
animation correctness, thumbnail validity, and key acceptance criteria for
the pursuit-curves / mice-problem piece.
"""
import json
import os

import pytest

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID = "97-pursuit-curves-ruth-naomi"
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


def test_piece_has_book_of_ruth_theme():
    piece = get_piece()
    assert piece is not None
    assert "Ruth" in piece["theme"], \
        f"theme should mention 'Book of Ruth', got: {piece['theme']!r}"


def test_piece_has_pursuit_curve_technique():
    piece = get_piece()
    assert piece is not None
    technique = piece["technique"].lower()
    assert "pursuit" in technique or "mice" in technique, \
        f"technique should mention pursuit curves or mice problem, got: {piece['technique']!r}"


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


def test_piece_year_is_integer():
    piece = get_piece()
    assert piece is not None
    assert isinstance(piece["year"], int), \
        f"year must be an integer, got {piece['year']!r}"


# ---------------------------------------------------------------------------
# essay.md content
# ---------------------------------------------------------------------------

def test_essay_minimum_word_count():
    text = read("essay.md")
    word_count = len(text.split())
    assert word_count >= 200, \
        f"essay.md has only {word_count} words; minimum is 200"


def test_essay_opens_with_ruth_verse():
    text = read("essay.md")
    assert "Ruth 1:16" in text or "1:16" in text, \
        "essay.md must open with or cite Ruth 1:16-17"


def test_essay_mentions_ruth():
    text = read("essay.md")
    assert "Ruth" in text, "essay.md must mention Ruth"


def test_essay_mentions_naomi():
    text = read("essay.md")
    assert "Naomi" in text, "essay.md must mention Naomi"


def test_essay_mentions_orpah():
    text = read("essay.md")
    assert "Orpah" in text, "essay.md must mention Orpah (the one who returned)"


def test_essay_mentions_yevamot():
    text = read("essay.md")
    assert "Yevamot" in text or "47b" in text, \
        "essay.md must mention Yevamot 47b (the conversion template)"


def test_essay_mentions_pursuit_curves():
    text = read("essay.md").lower()
    assert "pursuit" in text or "mice" in text or "spiral" in text, \
        "essay.md must explain the pursuit curve / mice problem mathematics"


def test_essay_mentions_omer():
    text = read("essay.md").lower()
    assert "omer" in text or "forty-nine" in text or "49" in text or "harvest" in text, \
        "essay.md must reference the Omer / harvest context of the background field"


def test_essay_is_not_placeholder():
    text = read("essay.md").lower()
    for stub in ("lorem ipsum", "placeholder", "todo", "tbd"):
        assert stub not in text, \
            f"essay.md appears to contain placeholder text: '{stub}'"


# ---------------------------------------------------------------------------
# index.html content — animation correctness
# ---------------------------------------------------------------------------

def test_index_html_uses_requestanimationframe():
    html = read("index.html")
    assert "requestAnimationFrame" in html, \
        "index.html must use requestAnimationFrame for animation"


def test_index_html_has_canvas():
    html = read("index.html")
    assert "<canvas" in html, "index.html must contain a <canvas> element"


def test_index_html_has_ruth_color():
    html = read("index.html")
    assert "#C8922A" in html, \
        "index.html must define Ruth's warm gold color #C8922A"


def test_index_html_has_naomi_color():
    html = read("index.html")
    assert "#F5EDE0" in html, \
        "index.html must define Naomi's ivory color #F5EDE0"


def test_index_html_has_orpah_color():
    html = read("index.html")
    assert "#A05040" in html, \
        "index.html must define Orpah's terracotta color #A05040"


def test_index_html_pursuit_step_delta():
    html = read("index.html")
    assert "0.8" in html, \
        "index.html must use main step δ=0.8 for the three-agent pursuit"


def test_index_html_background_step_delta():
    html = read("index.html")
    assert "0.3" in html, \
        "index.html must use background step δ=0.3 for the 49-system field"


def test_index_html_has_49_background_systems():
    html = read("index.html")
    assert "49" in html or "7" in html, \
        "index.html must create 49 (7×7) background pursuit systems"


def test_index_html_orpah_deflection_logic():
    html = read("index.html")
    assert "deflect" in html.lower() or "lerp" in html.lower() or "escape" in html.lower(), \
        "index.html must implement Orpah's direction deflection/lerp"


def test_index_html_orpah_fades():
    html = read("index.html")
    assert "opacity" in html.lower() or "globalAlpha" in html or "fade" in html.lower(), \
        "index.html must fade Orpah's opacity to 0"


def test_index_html_path_accumulation():
    html = read("index.html")
    assert "push" in html and ("lineTo" in html or "path" in html.lower()), \
        "index.html must accumulate agent positions and draw polylines"


def test_index_html_convergence_detection():
    html = read("index.html")
    assert "converge" in html.lower() or "hypot" in html or "dist" in html.lower(), \
        "index.html must detect convergence of Ruth and Naomi"


def test_index_html_pause_on_convergence():
    html = read("index.html")
    assert "pause" in html.lower() or "pauseTimer" in html or "120" in html, \
        "index.html must pause for ~2 seconds (120 frames) after convergence"


def test_index_html_loop_seamlessly():
    html = read("index.html")
    assert "fading" in html.lower() or "fadein" in html.lower() or "restart" in html.lower(), \
        "index.html must restart the animation loop seamlessly"


def test_index_html_embeds_essay_text():
    essay = read("essay.md")
    html = read("index.html")
    words = [w for w in essay.split() if len(w) > 6][:10]
    found = sum(1 for w in words if w in html)
    assert found >= 5, \
        f"index.html must embed essay text (only {found}/10 sampled words found)"


def test_index_html_is_self_contained():
    html = read("index.html")
    for cdn in ("cdn.jsdelivr.net", "cdnjs.cloudflare.com", "unpkg.com"):
        assert cdn not in html, \
            f"index.html must be self-contained — no CDN dependency on {cdn}"


def test_index_html_shadow_glow_effect():
    html = read("index.html")
    assert "shadowBlur" in html or "shadowColor" in html, \
        "index.html must use shadowBlur/shadowColor glow on main spirals"


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


def test_thumbnail_has_ruth_gold_color():
    svg = read("thumbnail.svg")
    assert "#C8922A" in svg, \
        "thumbnail.svg must include Ruth's warm gold color #C8922A"


def test_thumbnail_has_orpah_terracotta():
    svg = read("thumbnail.svg")
    assert "#A05040" in svg, \
        "thumbnail.svg must include Orpah's terracotta color #A05040"


def test_thumbnail_has_naomi_ivory():
    svg = read("thumbnail.svg")
    assert "#F5EDE0" in svg, \
        "thumbnail.svg must include Naomi's ivory color #F5EDE0"


def test_thumbnail_has_spiral_path():
    svg = read("thumbnail.svg")
    assert "<path" in svg, \
        "thumbnail.svg must include <path> elements for spiral arms"


def test_thumbnail_has_wheat_motifs():
    svg = read("thumbnail.svg")
    assert "wheat" in svg.lower() or "ellipse" in svg.lower() or "#8a6820" in svg.lower(), \
        "thumbnail.svg must include wheat-stalk corner motifs"


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

def test_readme_mentions_ruth():
    readme = read("README.md")
    assert "Ruth" in readme, "README.md must mention Ruth"


def test_readme_mentions_pursuit_curves():
    readme = read("README.md").lower()
    assert "pursuit" in readme or "mice" in readme or "spiral" in readme, \
        "README.md must describe the pursuit curve technique"


def test_readme_mentions_49_systems():
    readme = read("README.md")
    assert "49" in readme or "forty-nine" in readme.lower() or "7×7" in readme, \
        "README.md must mention the 49 background pursuit systems"


def test_pieces_json_is_valid_json_after_edit():
    with open(PIECES_JSON, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    assert isinstance(data, list)
    assert any(p["id"] == PIECE_ID for p in data)


def test_piece_id_matches_directory():
    """The piece id must match the last directory component of its path."""
    piece = get_piece()
    assert piece is not None
    path_parts = piece["path"].replace("\\", "/").split("/")
    dir_name = path_parts[-2]
    assert dir_name == PIECE_ID, \
        f"Directory name '{dir_name}' does not match piece id '{PIECE_ID}'"


@pytest.mark.parametrize("bad_id", ["97-pursuit-curves-ruth-naomi-extra", "pursuit-curves"])
def test_nonexistent_piece_ids_not_in_json(bad_id):
    """Confirms our new ID is distinct and not accidentally duplicated."""
    pieces = load_pieces()
    ids = [p["id"] for p in pieces]
    assert bad_id not in ids, \
        f"Unexpected piece id '{bad_id}' found in pieces.json"
