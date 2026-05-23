"""
Tests for piece 73-girih-star-keter-torah: The Crown Woven in Geometry.

Validates file layout, pieces.json registration, essay content,
girih star construction algorithm requirements in index.html,
and thumbnail SVG validity.
"""
import json
import os

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID = "73-girih-star-keter-torah"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")


def load_piece():
    """Load the piece entry from pieces.json."""
    with open(PIECES_JSON, encoding="utf-8") as f:
        pieces = json.load(f)
    for p in pieces:
        if p["id"] == PIECE_ID:
            return p
    return None


# ---------------------------------------------------------------------------
# File layout tests
# ---------------------------------------------------------------------------

def test_piece_directory_exists():
    assert os.path.isdir(PIECE_DIR), f"Piece directory {PIECE_DIR} does not exist"


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
    piece = load_piece()
    assert piece is not None, f"Piece {PIECE_ID!r} not found in pieces.json"


def test_piece_theme_correct():
    piece = load_piece()
    assert piece is not None
    assert "Crown of Torah" in piece["theme"] or "Naaseh" in piece["theme"], (
        f"theme field should reference 'The Crown of Torah / Naaseh v'Nishma', got {piece['theme']!r}"
    )


def test_piece_technique_correct():
    piece = load_piece()
    assert piece is not None
    assert "girih" in piece["technique"].lower(), (
        f"technique field should mention 'girih', got {piece['technique']!r}"
    )
    assert "canvas" in piece["technique"].lower(), (
        f"technique field should mention 'canvas', got {piece['technique']!r}"
    )


def test_piece_year_is_int():
    piece = load_piece()
    assert piece is not None
    assert isinstance(piece["year"], int)


def test_piece_paths_exist():
    piece = load_piece()
    assert piece is not None
    for field in ("path", "thumbnail", "essay"):
        full = os.path.join(GALLERY_ROOT, piece[field])
        assert os.path.isfile(full), f"Field {field!r} path does not exist: {piece[field]}"


# ---------------------------------------------------------------------------
# Essay content
# ---------------------------------------------------------------------------

def test_essay_minimum_word_count():
    """Essay must be at least 300 words (spec says ~380)."""
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    words = len(text.split())
    assert words >= 300, f"Essay has only {words} words (need >= 300)"


def test_essay_mentions_pirkei_avot():
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    assert "Avot" in text or "Pirkei" in text, "Essay must mention Pirkei Avot"


def test_essay_mentions_keter_torah():
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    assert "Keter Torah" in text or "keter torah" in text.lower(), (
        "Essay must mention Keter Torah"
    )


def test_essay_mentions_tagin():
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    assert "tagin" in text.lower() or "tag" in text.lower(), (
        "Essay must discuss the tagin (decorative letter crowns)"
    )


def test_essay_mentions_menachot():
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    assert "Menachot" in text or "menachot" in text.lower(), (
        "Essay must reference Talmud Menachot 29b"
    )


def test_essay_mentions_shavuot():
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    assert "Shavuot" in text or "shavuot" in text.lower(), (
        "Essay must connect the piece to Shavuot"
    )


# ---------------------------------------------------------------------------
# index.html: algorithmic construction requirements
# ---------------------------------------------------------------------------

def test_index_html_uses_request_animation_frame():
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "requestAnimationFrame" in html, "index.html must use requestAnimationFrame for animation"


def test_index_html_uses_canvas():
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "<canvas" in html, "index.html must contain a <canvas> element"


def test_index_html_algorithmic_decagon():
    """The construction must compute decagon vertices algorithmically."""
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "Math.PI" in html, "index.html must compute angles via Math.PI (algorithmic decagon)"
    assert "Math.cos" in html and "Math.sin" in html, (
        "index.html must use Math.cos/Math.sin for vertex computation"
    )


def test_index_html_ten_vertex_decagon():
    """The code must reference 10 vertices explicitly."""
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "10" in html, "index.html must reference 10 (the decagon vertex count)"
    assert "length: 10" in html or "length:10" in html or "/ 10" in html, (
        "index.html must divide by 10 or use length 10 for the decagon construction"
    )


def test_index_html_color_palette():
    """The prescribed color palette must appear in the HTML."""
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "#1A2870" in html, "Star color #1A2870 must be in index.html"
    assert "#C8900A" in html, "Bow-tie color #C8900A must be in index.html"
    assert "#F5EDD8" in html, "Background/letter color #F5EDD8 must be in index.html"
    assert "#FFD040" in html, "Center star highlight #FFD040 must be in index.html"


def test_index_html_hebrew_letter_kaf():
    """The Hebrew letter כ must appear in index.html."""
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "כ" in html, "index.html must contain the Hebrew letter כ (Kaf)"


def test_index_html_embeds_essay_text():
    """Key essay words must appear in the HTML (essay is embedded, not fetched)."""
    essay = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    words = [w for w in essay.split() if len(w) > 6][:15]
    found = sum(1 for w in words if w in html)
    assert found >= 6, (
        f"index.html must embed essay text (only {found}/15 sampled words found)"
    )


def test_index_html_rotation_or_breathing_animation():
    """The piece must animate — either rotation or breathing (sine/opacity)."""
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    has_rotation = "rotate" in html
    has_breathing = "Math.sin" in html or "opacity" in html.lower()
    assert has_rotation or has_breathing, (
        "index.html must animate via rotation (ctx.rotate) or breathing (Math.sin opacity)"
    )


def test_index_html_canvas_700px():
    """Canvas must be 700×700 as specified."""
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert 'width="700"' in html or "width: 700" in html or "W = 700" in html, (
        "Canvas must be 700px wide"
    )
    assert 'height="700"' in html or "height: 700" in html or "H = 700" in html, (
        "Canvas must be 700px tall"
    )


# ---------------------------------------------------------------------------
# thumbnail.svg
# ---------------------------------------------------------------------------

def test_thumbnail_is_valid_svg():
    text = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert "<svg" in text and "</svg>" in text, "thumbnail.svg must be valid SVG"


def test_thumbnail_400x400():
    text = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert 'width="400"' in text and 'height="400"' in text, (
        "thumbnail.svg must be 400x400"
    )


def test_thumbnail_contains_kaf():
    text = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert "כ" in text, "thumbnail.svg must contain the Hebrew letter כ"


def test_thumbnail_under_50kb():
    size = os.path.getsize(os.path.join(PIECE_DIR, "thumbnail.svg"))
    assert size < 50 * 1024, f"thumbnail.svg must be under 50KB, is {size} bytes"


def test_thumbnail_contains_colors():
    text = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert "#1A2870" in text or "1A2870" in text, "thumbnail must use star blue #1A2870"
    assert "#FFD040" in text or "FFD040" in text, "thumbnail must show center star #FFD040"


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

def test_no_duplicate_ids_in_pieces_json():
    with open(PIECES_JSON, encoding="utf-8") as f:
        pieces = json.load(f)
    ids = [p["id"] for p in pieces]
    assert len(ids) == len(set(ids)), "Duplicate piece IDs found in pieces.json"


def test_piece_id_matches_directory():
    piece = load_piece()
    assert piece is not None
    path_parts = piece["path"].replace("\\", "/").split("/")
    dir_name = path_parts[-2]
    assert dir_name == PIECE_ID, (
        f"Directory in path {dir_name!r} does not match piece id {PIECE_ID!r}"
    )


def test_essay_not_empty():
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read().strip()
    assert len(text) > 0, "essay.md must not be empty"


def test_index_html_not_empty():
    text = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read().strip()
    assert len(text) > 100, "index.html must have substantial content"
