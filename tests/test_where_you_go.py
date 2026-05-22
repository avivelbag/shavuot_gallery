"""
Tests specific to piece 33-where-you-go (string art portrait of Ruth).

Validates the piece's presence in pieces.json, the required files, the essay
content, and the canvas/JavaScript implementation in index.html.
"""
import json
import os
import re

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")
PIECE_ID = "33-where-you-go"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_pieces():
    """Load and return the parsed pieces.json list."""
    with open(PIECES_JSON, encoding="utf-8") as fh:
        return json.load(fh)


def get_piece():
    """Return the pieces.json entry for piece 33, or None."""
    for p in load_pieces():
        if p["id"] == PIECE_ID:
            return p
    return None


def read_html():
    """Return the full text of the piece's index.html."""
    path = os.path.join(PIECE_DIR, "index.html")
    return open(path, encoding="utf-8").read()


def read_essay():
    """Return the full text of the piece's essay.md."""
    path = os.path.join(PIECE_DIR, "essay.md")
    return open(path, encoding="utf-8").read()


# ---------------------------------------------------------------------------
# pieces.json registration
# ---------------------------------------------------------------------------

def test_piece_33_in_pieces_json():
    """Piece 33-where-you-go must be registered in pieces.json."""
    assert get_piece() is not None, f"'{PIECE_ID}' not found in pieces.json"


def test_piece_33_required_fields():
    """All required fields must be present and non-empty."""
    required = ("id", "title", "tagline", "year", "theme", "technique",
                "path", "thumbnail", "essay")
    piece = get_piece()
    assert piece is not None
    for field in required:
        val = piece.get(field)
        assert val is not None and val != "", (
            f"Field '{field}' is missing or empty in piece {PIECE_ID}"
        )


def test_piece_33_year_is_integer():
    piece = get_piece()
    assert piece is not None
    assert isinstance(piece["year"], int), "year must be an integer"


def test_piece_33_path_ends_with_html():
    piece = get_piece()
    assert piece is not None
    assert piece["path"].endswith(".html"), "path must end with .html"


def test_piece_33_id_matches_directory():
    """The id must match the directory component of the path."""
    piece = get_piece()
    assert piece is not None
    parts = piece["path"].replace("\\", "/").split("/")
    assert parts[-2] == PIECE_ID, (
        f"Directory in path '{piece['path']}' does not match id '{PIECE_ID}'"
    )


# ---------------------------------------------------------------------------
# File layout on disk
# ---------------------------------------------------------------------------

def test_piece_33_index_html_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "index.html")), (
        "pieces/33-where-you-go/index.html is missing"
    )


def test_piece_33_essay_md_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "essay.md")), (
        "pieces/33-where-you-go/essay.md is missing"
    )


def test_piece_33_readme_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "README.md")), (
        "pieces/33-where-you-go/README.md is missing"
    )


def test_piece_33_thumbnail_exists():
    piece = get_piece()
    assert piece is not None
    thumb = os.path.join(GALLERY_ROOT, piece["thumbnail"])
    assert os.path.isfile(thumb), f"Thumbnail '{piece['thumbnail']}' does not exist"


def test_piece_33_thumbnail_is_svg():
    piece = get_piece()
    assert piece is not None
    thumb_path = os.path.join(GALLERY_ROOT, piece["thumbnail"])
    text = open(thumb_path, encoding="utf-8").read()
    assert "<svg" in text and "</svg>" in text, (
        "thumbnail.svg does not contain valid SVG markup"
    )


# ---------------------------------------------------------------------------
# Essay content
# ---------------------------------------------------------------------------

def test_piece_33_essay_at_least_200_words():
    text = read_essay()
    word_count = len(text.split())
    assert word_count >= 200, (
        f"essay.md has only {word_count} words (minimum 200)"
    )


def test_piece_33_essay_mentions_ruth_116():
    """Essay must cite Ruth 1:16 precisely."""
    text = read_essay()
    assert "1:16" in text, "essay.md must cite Ruth 1:16"
    assert "Ruth" in text, "essay.md must mention Ruth"


def test_piece_33_essay_mentions_naaseh_vnishma():
    """Essay must surface the Shavuot connection via naaseh v'nishma."""
    text = read_essay()
    assert "naaseh" in text.lower() or "naaseh v'nishma" in text.lower(), (
        "essay.md must mention 'naaseh v'nishma' (Israel's covenant at Sinai)"
    )


def test_piece_33_essay_mentions_yevamot():
    """Essay must cite Talmud Yevamot 47b on conversion paralleling Sinai."""
    text = read_essay()
    assert "Yevamot" in text or "47b" in text, (
        "essay.md must cite Talmud Yevamot 47b"
    )


def test_piece_33_essay_mentions_david():
    """Essay must note Ruth as great-grandmother of David (messianic hinge)."""
    text = read_essay()
    assert "David" in text, (
        "essay.md must mention that Ruth becomes the great-grandmother of King David"
    )


def test_piece_33_essay_mentions_voluntary():
    """Essay must characterize Ruth's choice as voluntary."""
    text = read_essay()
    lower = text.lower()
    assert "voluntar" in lower, (
        "essay.md must describe Ruth's acceptance as voluntary"
    )


def test_piece_33_essay_mentions_naomi_urges_return():
    """Essay must explain the context: Naomi urging Ruth to return to Moab."""
    text = read_essay()
    lower = text.lower()
    assert "naomi" in lower, "essay.md must mention Naomi"
    assert "moab" in lower, "essay.md must mention Moab (the land Ruth chose to leave)"


# ---------------------------------------------------------------------------
# index.html — canvas and animation implementation
# ---------------------------------------------------------------------------

def test_piece_33_html_uses_requestanimationframe():
    html = read_html()
    assert "requestAnimationFrame" in html, (
        "index.html must use requestAnimationFrame for animation"
    )


def test_piece_33_html_has_canvas():
    html = read_html()
    assert "<canvas" in html, "index.html must contain a <canvas> element"


def test_piece_33_html_background_color():
    """index.html must use the specified dark field-brown background (#1A1208)."""
    html = read_html()
    assert "#1A1208" in html or "#1a1208" in html.lower(), (
        "index.html must use background color #1A1208"
    )


def test_piece_33_html_line_color():
    """index.html must use linen-white (#F0E8D5) for the thread lines."""
    html = read_html()
    assert "#F0E8D5" in html or "#f0e8d5" in html.lower(), (
        "index.html must use line color #F0E8D5"
    )


def test_piece_33_html_semi_transparent_lines():
    """Lines must be drawn with a semi-transparent globalAlpha (0.08–0.12)."""
    html = read_html()
    alpha_matches = re.findall(r'LINE_ALPHA\s*=\s*([\d.]+)', html)
    if alpha_matches:
        alpha = float(alpha_matches[0])
        assert 0.06 <= alpha <= 0.15, (
            f"LINE_ALPHA should be 0.08–0.12, got {alpha}"
        )
    else:
        assert "globalAlpha" in html, (
            "index.html must set globalAlpha for semi-transparent lines"
        )


def test_piece_33_html_pin_count():
    """The implementation must declare N = 200–300 pins."""
    html = read_html()
    matches = re.findall(r'\bN\s*=\s*(\d+)', html)
    if matches:
        n_vals = [int(m) for m in matches]
        assert any(200 <= v <= 300 for v in n_vals), (
            f"Pin count N must be 200–300, found values: {n_vals}"
        )


def test_piece_33_html_contains_hebrew_verse():
    """index.html must embed the Hebrew verse from Ruth 1:16."""
    html = read_html()
    # Check for the Hebrew text (or a key fragment)
    assert "תֵּלְכִי" in html or "אֶל-אֲשֶׁר" in html, (
        "index.html must contain the Hebrew text of Ruth 1:16"
    )


def test_piece_33_html_embeds_essay_text():
    """index.html must embed essay text inline (at least 5 of 10 sampled long words)."""
    essay_text = read_essay()
    html = read_html()
    words = [w for w in essay_text.split() if len(w) > 5]
    sampled = words[:10]
    found = sum(1 for w in sampled if w in html)
    assert found >= 5, (
        f"index.html does not appear to embed essay text "
        f"(only {found}/10 sampled words found in HTML): {sampled}"
    )


def test_piece_33_html_greedy_algorithm_keywords():
    """index.html must implement the greedy string-art selection algorithm."""
    html = read_html()
    # The greedy algorithm reads residual values and picks the best-scoring line.
    assert "residual" in html, (
        "index.html must maintain a 'residual' array for greedy line selection"
    )
    assert "bestScore" in html or "best_score" in html or "bestPin" in html, (
        "index.html must implement greedy best-score selection"
    )


def test_piece_33_html_animation_phases():
    """index.html must implement hold and fade phases."""
    html = read_html()
    assert "holding" in html or "HOLD_MS" in html, (
        "index.html must implement a hold phase after drawing completes"
    )
    assert "fading" in html or "FADE" in html, (
        "index.html must implement a fade/restart phase"
    )


# ---------------------------------------------------------------------------
# Edge cases and failure modes
# ---------------------------------------------------------------------------

def test_piece_33_not_duplicate_id():
    """Piece ID 33-where-you-go must appear exactly once in pieces.json."""
    pieces = load_pieces()
    ids = [p["id"] for p in pieces]
    count = ids.count(PIECE_ID)
    assert count == 1, f"'{PIECE_ID}' appears {count} times in pieces.json (expected 1)"


def test_piece_33_essay_path_is_correct(tmp_path):
    """The essay field in pieces.json must point to the real file, not a placeholder."""
    piece = get_piece()
    assert piece is not None
    essay_path = os.path.join(GALLERY_ROOT, piece["essay"])
    assert os.path.isfile(essay_path), (
        f"Essay path '{piece['essay']}' does not exist on disk"
    )
    text = open(essay_path, encoding="utf-8").read().strip()
    assert len(text) > 100, "essay.md appears to be empty or a stub"


def test_nonexistent_piece_id_returns_none():
    """Helper get_piece() must return None for an unknown ID."""
    pieces = load_pieces()
    missing = next((p for p in pieces if p["id"] == "99-does-not-exist"), None)
    assert missing is None


def test_essay_word_count_boundary():
    """essay.md must comfortably exceed the 200-word minimum."""
    text = read_essay()
    word_count = len(text.split())
    assert word_count >= 300, (
        f"essay.md has only {word_count} words; expected substantially more than 200"
    )
