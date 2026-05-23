"""
Tests for piece 70-moire-milk-honey.

Verifies the piece directory layout, pieces.json registration, and key
content requirements from the acceptance criteria.
"""
import json
import os

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")
PIECE_ID = "70-moire-milk-honey"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)


def _load_piece():
    """Return the pieces.json entry for piece 70, or None if absent."""
    with open(PIECES_JSON, encoding="utf-8") as fh:
        pieces = json.load(fh)
    for p in pieces:
        if p["id"] == PIECE_ID:
            return p
    return None


# ---------------------------------------------------------------------------
# Registration in pieces.json
# ---------------------------------------------------------------------------

def test_piece_registered_in_pieces_json():
    piece = _load_piece()
    assert piece is not None, f"Piece '{PIECE_ID}' not found in pieces.json"


def test_piece_theme_is_milk_and_honey():
    piece = _load_piece()
    assert piece is not None
    assert "Milk and Honey" in piece["theme"], (
        f"Expected theme to contain 'Milk and Honey', got: {piece['theme']!r}"
    )


def test_piece_technique_mentions_moire():
    piece = _load_piece()
    assert piece is not None
    technique = piece["technique"].lower()
    assert "moir" in technique, (
        f"Expected technique to mention moiré, got: {piece['technique']!r}"
    )


def test_piece_technique_mentions_hexagonal():
    piece = _load_piece()
    assert piece is not None
    technique = piece["technique"].lower()
    assert "hex" in technique, (
        f"Expected technique to mention hexagonal grids, got: {piece['technique']!r}"
    )


# ---------------------------------------------------------------------------
# File layout
# ---------------------------------------------------------------------------

def test_piece_directory_exists():
    assert os.path.isdir(PIECE_DIR), f"Piece directory '{PIECE_DIR}' does not exist"


def test_index_html_exists():
    path = os.path.join(PIECE_DIR, "index.html")
    assert os.path.isfile(path), "index.html is missing from piece directory"


def test_essay_md_exists():
    path = os.path.join(PIECE_DIR, "essay.md")
    assert os.path.isfile(path), "essay.md is missing from piece directory"


def test_thumbnail_svg_exists():
    path = os.path.join(PIECE_DIR, "thumbnail.svg")
    assert os.path.isfile(path), "thumbnail.svg is missing from piece directory"


def test_readme_md_exists():
    path = os.path.join(PIECE_DIR, "README.md")
    assert os.path.isfile(path), "README.md is missing from piece directory"


# ---------------------------------------------------------------------------
# index.html content requirements
# ---------------------------------------------------------------------------

def _html():
    return open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()


def test_canvas_is_700x700():
    html = _html()
    assert 'width="700"' in html and 'height="700"' in html, (
        "Canvas must be declared as 700×700"
    )


def test_uses_request_animation_frame():
    assert "requestAnimationFrame" in _html(), (
        "index.html must use requestAnimationFrame for 60fps animation"
    )


def test_milk_color_present():
    assert "#F5EDD5" in _html(), (
        "Milk grid color #F5EDD5 must appear in index.html"
    )


def test_honey_color_present():
    assert "#C8920A" in _html(), (
        "Honey grid color #C8920A must appear in index.html"
    )


def test_background_color_present():
    assert "#080600" in _html(), (
        "Background color #080600 must appear in index.html"
    )


def test_milk_spacing_28():
    assert "28" in _html(), (
        "Milk grid spacing of 28px must appear in index.html"
    )


def test_honey_spacing_30():
    assert "30" in _html(), (
        "Honey grid spacing of 30px must appear in index.html"
    )


def test_honey_rotation_rate():
    assert "0.0008" in _html(), (
        "Honey grid rotation rate 0.0008 rad/frame must appear in index.html"
    )


def test_milk_opacity_pulse_formula():
    assert "0.008" in _html(), (
        "Milk opacity pulse formula (Math.sin(t * 0.008)) must appear in index.html"
    )


def test_hebrew_caption_present():
    html = _html()
    assert "דְּבַשׁ" in html, (
        "Hebrew caption 'דְּבַשׁ וְחָלָב תַּחַת לְשׁוֹנֵךְ' must appear in index.html"
    )


def test_essay_text_embedded_in_html():
    essay = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    html = _html()
    words = [w for w in essay.split() if len(w) > 6][:12]
    found = sum(1 for w in words if w in html)
    assert found >= 6, (
        f"index.html must embed the essay text inline; only {found}/12 sampled words found"
    )


# ---------------------------------------------------------------------------
# thumbnail.svg content
# ---------------------------------------------------------------------------

def test_thumbnail_is_valid_svg():
    content = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert "<svg" in content and "</svg>" in content, (
        "thumbnail.svg does not appear to be valid SVG"
    )


def test_thumbnail_has_dark_background():
    content = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert "#080600" in content, (
        "thumbnail.svg must use the #080600 background color"
    )


def test_thumbnail_contains_both_grid_colors():
    content = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert "#F5EDD5" in content, "thumbnail.svg must include milk color #F5EDD5"
    assert "#C8920A" in content, "thumbnail.svg must include honey color #C8920A"


def test_thumbnail_has_rotation_for_honey_grid():
    content = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert "rotate" in content, (
        "thumbnail.svg must apply a rotation transform to the honey grid"
    )


# ---------------------------------------------------------------------------
# essay.md content
# ---------------------------------------------------------------------------

def _essay():
    return open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()


def test_essay_minimum_word_count():
    text = _essay()
    count = len(text.split())
    assert count >= 350, f"essay.md has only {count} words; expected at least 350"


def test_essay_mentions_exodus_38():
    essay = _essay()
    assert "Exodus 3" in essay or "3:8" in essay, (
        "essay.md must reference Exodus 3:8 (first occurrence of the milk-and-honey phrase)"
    )


def test_essay_mentions_ketubot():
    assert "Ketubot" in _essay() or "111b" in _essay(), (
        "essay.md must mention Ketubot 111b (Talmudic empirical measurement)"
    )


def test_essay_mentions_song_of_songs():
    essay = _essay()
    assert "Song of Songs" in essay or "4:11" in essay, (
        "essay.md must reference Song of Songs 4:11"
    )


def test_essay_mentions_twenty_occurrences():
    essay = _essay().lower()
    assert "twenty" in essay, (
        "essay.md must mention the twenty occurrences of 'eretz zavat chalav u'dvash'"
    )


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

def test_piece_id_unique_in_pieces_json():
    with open(PIECES_JSON, encoding="utf-8") as fh:
        pieces = json.load(fh)
    ids = [p["id"] for p in pieces]
    assert ids.count(PIECE_ID) == 1, (
        f"Piece ID '{PIECE_ID}' appears {ids.count(PIECE_ID)} times in pieces.json (expected 1)"
    )


def test_piece_path_points_to_existing_file():
    piece = _load_piece()
    assert piece is not None
    full_path = os.path.join(GALLERY_ROOT, piece["path"])
    assert os.path.isfile(full_path), (
        f"pieces.json path '{piece['path']}' does not exist on disk"
    )


def test_piece_thumbnail_points_to_existing_file():
    piece = _load_piece()
    assert piece is not None
    full_path = os.path.join(GALLERY_ROOT, piece["thumbnail"])
    assert os.path.isfile(full_path), (
        f"pieces.json thumbnail '{piece['thumbnail']}' does not exist on disk"
    )


def test_piece_essay_points_to_existing_file():
    piece = _load_piece()
    assert piece is not None
    full_path = os.path.join(GALLERY_ROOT, piece["essay"])
    assert os.path.isfile(full_path), (
        f"pieces.json essay '{piece['essay']}' does not exist on disk"
    )


def test_piece_all_required_fields_present():
    required = ("id", "title", "tagline", "year", "theme", "technique", "path", "thumbnail", "essay")
    piece = _load_piece()
    assert piece is not None
    for field in required:
        assert field in piece and piece[field], (
            f"Piece is missing required field '{field}'"
        )
