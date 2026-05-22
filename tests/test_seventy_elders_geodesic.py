"""
Tests for piece 56 — They Saw God and Ate (geodesic crown of the 70 elders).

Covers: file layout, pieces.json registration, essay quality,
HTML embedding, animation technique markers, and edge-case behaviour.
"""
import json
import os

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID = "56-seventy-elders-geodesic"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
INDEX_HTML = os.path.join(PIECE_DIR, "index.html")
ESSAY_MD   = os.path.join(PIECE_DIR, "essay.md")
THUMB_SVG  = os.path.join(PIECE_DIR, "thumbnail.svg")
README_MD  = os.path.join(PIECE_DIR, "README.md")
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")


# ── Helpers ───────────────────────────────────────────────────────────────

def _load_pieces():
    with open(PIECES_JSON, "r", encoding="utf-8") as fh:
        return json.load(fh)

def _get_piece():
    for p in _load_pieces():
        if p["id"] == PIECE_ID:
            return p
    return None


# ── File layout (happy path) ──────────────────────────────────────────────

def test_piece_directory_exists():
    assert os.path.isdir(PIECE_DIR), f"Piece directory missing: {PIECE_DIR}"


def test_index_html_exists():
    assert os.path.isfile(INDEX_HTML), "index.html missing"


def test_essay_md_exists():
    assert os.path.isfile(ESSAY_MD), "essay.md missing"


def test_thumbnail_svg_exists():
    assert os.path.isfile(THUMB_SVG), "thumbnail.svg missing"


def test_readme_md_exists():
    assert os.path.isfile(README_MD), "README.md missing"


# ── pieces.json registration ──────────────────────────────────────────────

def test_piece_registered_in_json():
    assert _get_piece() is not None, f"Piece '{PIECE_ID}' not found in pieces.json"


def test_pieces_json_required_fields():
    piece = _get_piece()
    assert piece is not None
    for field in ("id", "title", "tagline", "year", "theme", "technique", "path", "thumbnail", "essay"):
        assert field in piece and piece[field], f"Field '{field}' missing or empty"


def test_pieces_json_theme():
    piece = _get_piece()
    assert piece is not None
    assert "Sinai" in piece["theme"] or "Covenant" in piece["theme"], (
        "theme must reference Sinai or the Covenant"
    )


def test_pieces_json_technique():
    piece = _get_piece()
    assert piece is not None
    assert "geodesic" in piece["technique"].lower() or "projection" in piece["technique"].lower(), (
        "technique must mention geodesic or JS projection"
    )


def test_pieces_json_paths_correct():
    piece = _get_piece()
    assert piece is not None
    assert piece["path"]      == f"pieces/{PIECE_ID}/index.html"
    assert piece["thumbnail"] == f"pieces/{PIECE_ID}/thumbnail.svg"
    assert piece["essay"]     == f"pieces/{PIECE_ID}/essay.md"


# ── Essay quality ─────────────────────────────────────────────────────────

def test_essay_word_count():
    text = open(ESSAY_MD, encoding="utf-8").read()
    assert len(text.split()) >= 400, "essay.md must have at least 400 words"


def test_essay_cites_exodus_24():
    text = open(ESSAY_MD, encoding="utf-8").read()
    assert "24:9" in text or "24:11" in text, "essay must cite Exodus 24"


def test_essay_mentions_rashi():
    text = open(ESSAY_MD, encoding="utf-8").read().lower()
    assert "rashi" in text, "essay must discuss Rashi's reading"


def test_essay_mentions_nachmanides():
    text = open(ESSAY_MD, encoding="utf-8").read().lower()
    assert "nachmanides" in text or "ramban" in text, "essay must discuss Nachmanides"


def test_essay_contains_hebrew():
    text = open(ESSAY_MD, encoding="utf-8").read()
    # Check for Hebrew Unicode block (U+0590–U+05FF)
    assert any('֐' <= ch <= '׿' for ch in text), (
        "essay.md must contain Hebrew text"
    )


def test_essay_mentions_shavuot_connection():
    text = open(ESSAY_MD, encoding="utf-8").read().lower()
    assert "shavuot" in text or "tikkun" in text, (
        "essay must connect to Shavuot / Tikkun Leil Shavuot"
    )


# ── HTML embedding ────────────────────────────────────────────────────────

def test_index_html_embeds_essay_words():
    """Enough long words from the essay must appear verbatim in the HTML."""
    essay = open(ESSAY_MD, encoding="utf-8").read()
    html  = open(INDEX_HTML, encoding="utf-8").read()
    words = [w for w in essay.split() if len(w) > 6][:15]
    found = sum(1 for w in words if w in html)
    assert found >= 7, (
        f"index.html does not embed enough essay text (found {found}/15 sampled words)"
    )


def test_index_html_has_canvas():
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "<canvas" in html, "index.html must contain a <canvas> element"


def test_index_html_uses_requestanimationframe():
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "requestAnimationFrame" in html, "animation must use requestAnimationFrame"


def test_index_html_no_webgl():
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "getContext('webgl')" not in html and 'getContext("webgl")' not in html, (
        "piece must use pure canvas 2D, not WebGL"
    )


def test_index_html_has_essay_panel():
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "essay-panel" in html, "index.html must have an essay-panel div"


def test_index_html_has_hebrew_overlay():
    html = open(INDEX_HTML, encoding="utf-8").read()
    # The Hebrew phrase contains characters in U+05D0–U+05FF range
    assert any('א' <= ch <= '׿' for ch in html), (
        "index.html must contain Hebrew characters (the overlay phrase)"
    )


# ── Geodesic technique markers ────────────────────────────────────────────

def test_index_html_has_icosahedron():
    html = open(INDEX_HTML, encoding="utf-8").read().lower()
    assert "icosahedron" in html or "icosah" in html or "subdiv" in html, (
        "JS must reference icosahedron subdivision"
    )


def test_index_html_has_rotation_math():
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "Math.cos" in html and "Math.sin" in html, (
        "JS must use cos/sin for rotation matrix"
    )


def test_index_html_has_perspective_divide():
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "focal" in html or "PUSH" in html or "focal" in html.lower(), (
        "JS must implement perspective divide with a focal / depth factor"
    )


def test_index_html_has_painters_algorithm():
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert ".sort(" in html, "JS must sort faces for painter's algorithm"


# ── Thumbnail ─────────────────────────────────────────────────────────────

def test_thumbnail_is_valid_svg():
    text = open(THUMB_SVG, encoding="utf-8").read()
    assert "<svg" in text and "</svg>" in text, "thumbnail.svg must be valid SVG"


def test_thumbnail_has_amber_color():
    text = open(THUMB_SVG, encoding="utf-8").read()
    assert "F5C842" in text or "f5c842" in text.lower(), (
        "thumbnail must use amber elder color #F5C842"
    )


def test_thumbnail_has_dark_background():
    text = open(THUMB_SVG, encoding="utf-8").read()
    assert "080D24" in text or "080d24" in text.lower(), (
        "thumbnail must use dark navy background #080D24"
    )


# ── Edge cases ────────────────────────────────────────────────────────────

def test_essay_md_not_empty():
    text = open(ESSAY_MD, encoding="utf-8").read().strip()
    assert len(text) > 0, "essay.md must not be empty"


def test_index_html_not_empty():
    text = open(INDEX_HTML, encoding="utf-8").read().strip()
    assert len(text) > 0, "index.html must not be empty"


def test_no_duplicate_piece_id():
    pieces = _load_pieces()
    ids = [p["id"] for p in pieces]
    count = ids.count(PIECE_ID)
    assert count == 1, f"Piece ID '{PIECE_ID}' appears {count} times in pieces.json"


def test_piece_year_is_integer():
    piece = _get_piece()
    assert piece is not None
    assert isinstance(piece["year"], int), "year must be an integer"


# ── Failure mode ──────────────────────────────────────────────────────────

def test_nonexistent_piece_not_found(tmp_path):
    """A piece ID that was never registered should return None from _get_piece-style lookup."""
    pieces = _load_pieces()
    result = next((p for p in pieces if p["id"] == "99-nonexistent-piece"), None)
    assert result is None, "Lookup of non-existent piece must return None"
