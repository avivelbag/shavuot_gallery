"""
Tests for pieces/89-aztec-diamond-omer — the Aztec diamond Omer piece.

Covers: pieces.json registration, file layout, essay content,
HTML embeds the essay and uses requestAnimationFrame, thumbnail SVG validity,
and content-level checks for the arctic circle and shuffling algorithm text.
"""
import json
import os

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID = "89-aztec-diamond-omer"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")


def load_pieces():
    with open(PIECES_JSON, encoding="utf-8") as f:
        return json.load(f)


def get_piece():
    for p in load_pieces():
        if p["id"] == PIECE_ID:
            return p
    return None


# ---------------------------------------------------------------------------
# Happy path — pieces.json registration
# ---------------------------------------------------------------------------

def test_piece_in_pieces_json():
    assert get_piece() is not None, f"{PIECE_ID} not found in pieces.json"


def test_piece_required_fields():
    piece = get_piece()
    required = ("id", "title", "tagline", "year", "theme", "technique", "path", "thumbnail", "essay")
    for field in required:
        assert field in piece and piece[field], f"Missing or empty field: {field}"


def test_piece_theme():
    piece = get_piece()
    assert "Sefirat HaOmer" in piece["theme"] or "seven weeks" in piece["theme"].lower()


def test_piece_technique():
    piece = get_piece()
    assert "domino" in piece["technique"].lower() or "aztec" in piece["technique"].lower()


def test_piece_year_is_int():
    piece = get_piece()
    assert isinstance(piece["year"], int)


# ---------------------------------------------------------------------------
# File layout
# ---------------------------------------------------------------------------

def test_index_html_exists():
    path = os.path.join(PIECE_DIR, "index.html")
    assert os.path.isfile(path), "index.html missing"


def test_essay_md_exists():
    path = os.path.join(PIECE_DIR, "essay.md")
    assert os.path.isfile(path), "essay.md missing"


def test_readme_md_exists():
    path = os.path.join(PIECE_DIR, "README.md")
    assert os.path.isfile(path), "README.md missing"


def test_thumbnail_svg_exists():
    path = os.path.join(PIECE_DIR, "thumbnail.svg")
    assert os.path.isfile(path), "thumbnail.svg missing"


# ---------------------------------------------------------------------------
# Essay content
# ---------------------------------------------------------------------------

def test_essay_word_count():
    path = os.path.join(PIECE_DIR, "essay.md")
    text = open(path, encoding="utf-8").read()
    count = len(text.split())
    assert count >= 200, f"essay.md only {count} words (need ≥200)"


def test_essay_cites_leviticus():
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    assert "Leviticus" in text or "23:15" in text


def test_essay_mentions_arctic_circle():
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    assert "arctic circle" in text.lower()


def test_essay_mentions_merkavah():
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    assert "Merkavah" in text or "merkavah" in text.lower()


def test_essay_mentions_49():
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    assert "49" in text or "forty-nine" in text.lower()


# ---------------------------------------------------------------------------
# index.html embeds essay and animation
# ---------------------------------------------------------------------------

def test_html_embeds_essay():
    essay_text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    words = [w for w in essay_text.split() if len(w) > 5][:10]
    found = sum(1 for w in words if w in html)
    assert found >= 5, f"index.html embeds too little essay text (only {found}/10 sampled words found)"


def test_html_uses_request_animation_frame():
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "requestAnimationFrame" in html


def test_html_has_canvas():
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "<canvas" in html


def test_html_mentions_shuffling_algorithm():
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "shuffle" in html.lower() or "shuffling" in html.lower()


def test_html_has_colors():
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    for color in ('#D4A017', '#B8860B', '#4A7C59', '#2D5A3D'):
        assert color in html, f"Expected color {color} not found in index.html"


def test_html_mentions_omer_day():
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "49" in html


# ---------------------------------------------------------------------------
# Thumbnail SVG validity
# ---------------------------------------------------------------------------

def test_thumbnail_is_valid_svg():
    text = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert "<svg" in text and "</svg>" in text


def test_thumbnail_has_dark_background():
    text = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert "#0C0C0C" in text or "0c0c0c" in text.lower()


def test_thumbnail_has_domino_colors():
    text = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    for color in ('#D4A017', '#B8860B', '#4A7C59', '#2D5A3D'):
        assert color in text, f"Expected domino color {color} not in thumbnail.svg"


# ---------------------------------------------------------------------------
# Edge cases and failure modes
# ---------------------------------------------------------------------------

def test_pieces_json_no_duplicate_ids():
    ids = [p["id"] for p in load_pieces()]
    assert len(ids) == len(set(ids)), "Duplicate piece IDs in pieces.json"


def test_piece_path_matches_id():
    piece = get_piece()
    path_parts = piece["path"].replace("\\", "/").split("/")
    dir_name = path_parts[-2]
    assert dir_name == PIECE_ID


def test_thumbnail_has_arctic_circle_hint():
    text = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert "<circle" in text, "thumbnail.svg should contain a circle element for the arctic circle"


def test_essay_not_empty_stub():
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    assert len(text.strip()) > 500, "essay.md appears to be a stub"


def test_missing_piece_id_returns_none():
    result = next((p for p in load_pieces() if p["id"] == "99-nonexistent-piece"), None)
    assert result is None
