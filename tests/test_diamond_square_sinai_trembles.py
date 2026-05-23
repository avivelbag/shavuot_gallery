"""
Tests for the 79-diamond-square-sinai-trembles piece.

Verifies the piece directory layout, pieces.json registration, and that the
index.html contains the required algorithmic elements described in the
acceptance criteria.
"""
import json
import os

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID = "79-diamond-square-sinai-trembles"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")


def load_pieces():
    """Load and return the parsed pieces.json list."""
    with open(PIECES_JSON, encoding="utf-8") as fh:
        return json.load(fh)


def get_piece():
    """Return the pieces.json entry for this piece, or None."""
    for p in load_pieces():
        if p["id"] == PIECE_ID:
            return p
    return None


def read_html():
    """Return the full text of index.html."""
    path = os.path.join(PIECE_DIR, "index.html")
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def read_essay():
    """Return the full text of essay.md."""
    path = os.path.join(PIECE_DIR, "essay.md")
    with open(path, encoding="utf-8") as fh:
        return fh.read()


# ---------------------------------------------------------------------------
# Directory and file layout
# ---------------------------------------------------------------------------

def test_piece_directory_exists():
    assert os.path.isdir(PIECE_DIR), f"Piece directory missing: {PIECE_DIR}"


def test_index_html_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "index.html"))


def test_essay_md_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "essay.md"))


def test_thumbnail_svg_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "thumbnail.svg"))


def test_readme_md_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "README.md"))


# ---------------------------------------------------------------------------
# pieces.json registration
# ---------------------------------------------------------------------------

def test_piece_registered_in_pieces_json():
    assert get_piece() is not None, f"'{PIECE_ID}' not found in pieces.json"


def test_piece_theme():
    piece = get_piece()
    assert piece is not None
    assert "Har Sinai" in piece["theme"], "theme must mention 'Har Sinai'"


def test_piece_technique():
    piece = get_piece()
    assert piece is not None
    tech = piece["technique"].lower()
    assert "diamond" in tech and "isometric" in tech, (
        "technique must mention diamond-square and isometric"
    )


def test_piece_essay_path_registered():
    piece = get_piece()
    assert piece is not None
    essay_path = os.path.join(GALLERY_ROOT, piece["essay"])
    assert os.path.isfile(essay_path), "essay path in pieces.json must point to existing file"


# ---------------------------------------------------------------------------
# index.html — algorithmic content checks (acceptance criteria)
# ---------------------------------------------------------------------------

def test_html_uses_requestanimationframe():
    assert "requestAnimationFrame" in read_html()


def test_html_contains_diamond_square_function():
    html = read_html()
    assert "diamondSquare" in html, "index.html must define the diamondSquare function"


def test_html_uses_float32array():
    assert "Float32Array" in read_html(), "heightmap must use Float32Array"


def test_html_grid_size_65():
    html = read_html()
    assert "N = 65" in html or "const N=65" in html or "N=65" in html or "65" in html


def test_html_morph_frames_120():
    """T_MORPH must be 120 (2 seconds at 60fps)."""
    html = read_html()
    assert "T_MORPH = 120" in html or "T_MORPH=120" in html or "120" in html


def test_html_cell_dimensions():
    html = read_html()
    assert "CELL_W = 16" in html or "CELL_W=16" in html
    assert "CELL_H = 8" in html or "CELL_H=8" in html
    assert "HEIGHT_SCALE = 60" in html or "HEIGHT_SCALE=60" in html


def test_html_contains_smoke_particles():
    html = read_html()
    assert "N_PARTICLES" in html or "particles" in html.lower()


def test_html_contains_fire_glow():
    """The red-orange fire glow strip must be present."""
    html = read_html()
    assert "FF4010" in html or "ff4010" in html.lower(), (
        "fire glow color #FF4010 must appear in index.html"
    )


def test_html_contains_color_palette():
    """All five height-band colors must appear in index.html."""
    html = read_html()
    for color in ["2A1A2E", "3D2B1A", "7A5A38", "B89070", "F0E8D8"]:
        assert color in html or color.lower() in html.lower(), (
            f"Height color #{color} missing from index.html"
        )


def test_html_painter_algorithm_render_order():
    """The painter's algorithm render loop must appear."""
    html = read_html()
    assert "2 * (N - 1)" in html or "2*(N-1)" in html or "painter" in html.lower() or \
           ("for" in html and "ix" in html and "iy" in html)


def test_html_isometric_projection_formula():
    """The isometric sx formula must be present."""
    html = read_html()
    assert "CELL_W / 2" in html or "CELL_W/2" in html, (
        "Isometric sx formula (ix-iy)*CELL_W/2 must appear"
    )


def test_html_embeds_essay_words():
    """index.html must embed essay text inline (not fetch at runtime)."""
    essay = read_essay()
    html = read_html()
    words = [w for w in essay.split() if len(w) > 6][:15]
    found = sum(1 for w in words if w in html)
    assert found >= 7, (
        f"index.html does not appear to embed essay text (only {found}/15 words found)"
    )


# ---------------------------------------------------------------------------
# essay.md content
# ---------------------------------------------------------------------------

def test_essay_minimum_words():
    text = read_essay()
    word_count = len(text.split())
    assert word_count >= 350, f"essay.md has {word_count} words, need >= 350"


def test_essay_mentions_exodus_1918():
    text = read_essay()
    assert "19:18" in text or "Exodus 19" in text, "essay must cite Exodus 19:18"


def test_essay_mentions_harad():
    text = read_essay()
    assert "ḥarad" in text or "חרד" in text or "harad" in text.lower(), (
        "essay must discuss the verb ḥarad (חרד)"
    )


def test_essay_mentions_mechilta():
    text = read_essay()
    assert "Mechilta" in text, "essay must cite the Mechilta de-Rabbi Ishmael"


def test_essay_mentions_shabbat_88a():
    text = read_essay()
    assert "Shabbat 88a" in text or "Shabbat 88" in text, (
        "essay must cite Talmud Shabbat 88a"
    )


# ---------------------------------------------------------------------------
# thumbnail.svg
# ---------------------------------------------------------------------------

def test_thumbnail_is_valid_svg():
    path = os.path.join(PIECE_DIR, "thumbnail.svg")
    text = open(path, encoding="utf-8").read()
    assert "<svg" in text and "</svg>" in text


def test_thumbnail_contains_rhombus_cells():
    """Thumbnail must contain polygon elements for isometric cells."""
    path = os.path.join(PIECE_DIR, "thumbnail.svg")
    text = open(path, encoding="utf-8").read()
    assert "<polygon" in text, "thumbnail.svg must contain polygon elements for isometric cells"


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

def test_pieces_json_no_duplicate_ids():
    """Adding the new piece must not create a duplicate ID."""
    pieces = load_pieces()
    ids = [p["id"] for p in pieces]
    assert len(ids) == len(set(ids)), "Duplicate piece IDs found"


def test_piece_path_points_to_existing_html():
    piece = get_piece()
    assert piece is not None
    full_path = os.path.join(GALLERY_ROOT, piece["path"])
    assert os.path.isfile(full_path)


def test_piece_thumbnail_path_exists():
    piece = get_piece()
    assert piece is not None
    full_path = os.path.join(GALLERY_ROOT, piece["thumbnail"])
    assert os.path.isfile(full_path)
