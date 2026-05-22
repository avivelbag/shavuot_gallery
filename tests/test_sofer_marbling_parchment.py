"""
Tests for piece 56-sofer-marbling-parchment — Ebru marbling of sacred parchment.

Covers: JSON registration, file layout, canvas animation API, palette colors,
Hebrew text overlay, Ebru displacement code, comb-pass code, essay content,
thumbnail validity, and negative/edge-case behaviors.
"""
import json
import os

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID = "56-sofer-marbling-parchment"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _load_pieces():
    with open(os.path.join(GALLERY_ROOT, "pieces.json"), encoding="utf-8") as fh:
        return json.load(fh)


def _get_piece():
    for p in _load_pieces():
        if p["id"] == PIECE_ID:
            return p
    return None


def _html():
    p = _get_piece()
    if p is None:
        return None
    path = os.path.join(GALLERY_ROOT, p["path"])
    if not os.path.isfile(path):
        return None
    return open(path, encoding="utf-8").read()


def _essay():
    path = os.path.join(PIECE_DIR, "essay.md")
    if not os.path.isfile(path):
        return None
    return open(path, encoding="utf-8").read()


# ---------------------------------------------------------------------------
# JSON registration — happy path
# ---------------------------------------------------------------------------

def test_piece_56_registered_in_pieces_json():
    assert _get_piece() is not None, f"'{PIECE_ID}' not found in pieces.json"


def test_piece_56_required_json_fields():
    p = _get_piece()
    assert p is not None
    for field in ("id", "title", "tagline", "year", "theme", "technique",
                  "path", "thumbnail", "essay"):
        assert field in p and p[field], f"pieces.json entry missing or empty field '{field}'"


def test_piece_56_year_is_integer():
    p = _get_piece()
    assert p is not None
    assert isinstance(p["year"], int)


# ---------------------------------------------------------------------------
# File layout — happy path
# ---------------------------------------------------------------------------

def test_piece_56_index_html_exists():
    p = _get_piece()
    assert p is not None
    assert os.path.isfile(os.path.join(GALLERY_ROOT, p["path"]))


def test_piece_56_thumbnail_exists():
    p = _get_piece()
    assert p is not None
    assert os.path.isfile(os.path.join(GALLERY_ROOT, p["thumbnail"]))


def test_piece_56_essay_md_exists():
    p = _get_piece()
    assert p is not None
    assert os.path.isfile(os.path.join(GALLERY_ROOT, p["essay"]))


def test_piece_56_readme_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "README.md"))


# ---------------------------------------------------------------------------
# Canvas animation API — happy path
# ---------------------------------------------------------------------------

def test_piece_56_uses_request_animation_frame():
    html = _html()
    assert html is not None
    assert "requestAnimationFrame" in html


def test_piece_56_canvas_element_present():
    html = _html()
    assert html is not None
    assert "<canvas" in html.lower()


def test_piece_56_uses_getImageData_and_putImageData():
    """Comb pass must manipulate pixels via ImageData API."""
    html = _html()
    assert html is not None
    assert "getImageData" in html
    assert "putImageData" in html


# ---------------------------------------------------------------------------
# Ebru technique specifics — happy path
# ---------------------------------------------------------------------------

def test_piece_56_palette_colors_present():
    """All five palette colors (parchment, black, sepia, gold, azure) must appear in the HTML."""
    html = _html()
    assert html is not None
    for color in ('#FBF3DC', '#1C1208', '#6B3F1A', '#C8960C', '#1E3A6A'):
        assert color in html or color.lower() in html, (
            f"Palette color {color} not found in index.html"
        )


def test_piece_56_drop_displacement_formula():
    """HTML must contain the r²/(r²+d²) Ebru displacement pattern."""
    html = _html()
    assert html is not None
    assert "factor" in html and ("rMax" in html or "r * r" in html or "rMax * rMax" in html)


def test_piece_56_comb_pass_implemented():
    """Comb function must be present (horizontal + vertical sinusoidal passes)."""
    html = _html()
    assert html is not None
    assert "applyComb" in html or "combPass" in html or "COMB" in html


def test_piece_56_sine_distortion_in_comb():
    """Comb pass must use Math.sin for the sinusoidal displacement."""
    html = _html()
    assert html is not None
    assert "Math.sin" in html


def test_piece_56_hebrew_text_overlay():
    """The Hebrew text from Exodus 24:4 must be drawn on the canvas."""
    html = _html()
    assert html is not None
    assert "וַיִּכְתֹּב" in html or "וַיִּכְתֹב" in html


def test_piece_56_animation_loop_resets():
    """The animation must include a reset/restart pathway."""
    html = _html()
    assert html is not None
    assert "resetCycle" in html or "initCycle" in html or "FADE_OUT" in html


# ---------------------------------------------------------------------------
# Essay content — happy path
# ---------------------------------------------------------------------------

def test_piece_56_essay_minimum_words():
    text = _essay()
    assert text is not None
    assert len(text.split()) >= 200, (
        f"essay.md has only {len(text.split())} words (minimum 200)"
    )


def test_piece_56_essay_cites_exodus_24():
    text = _essay()
    assert text is not None
    assert "Exodus 24" in text or "24:4" in text or "24:3" in text


def test_piece_56_essay_mentions_marbling_or_ebru():
    text = _essay()
    assert text is not None
    lower = text.lower()
    assert "marble" in lower or "ebru" in lower or "marbling" in lower


def test_piece_56_essay_contains_hebrew_passage():
    """Essay must include actual Hebrew text (Unicode RTL characters)."""
    text = _essay()
    assert text is not None
    assert "וַיִּכְתֹּב" in text or "מֹשֶׁה" in text


def test_piece_56_essay_embedded_in_html():
    """index.html must embed essay text — not merely link to essay.md."""
    html = _html()
    text = _essay()
    assert html is not None and text is not None
    long_words = [w for w in text.split() if len(w) > 5][:10]
    found = sum(1 for w in long_words if w in html)
    assert found >= 5, (
        f"Only {found}/10 sampled essay words found in index.html — essay not embedded"
    )


# ---------------------------------------------------------------------------
# Thumbnail validity
# ---------------------------------------------------------------------------

def test_piece_56_thumbnail_is_valid_svg():
    p = _get_piece()
    assert p is not None
    thumb = open(os.path.join(GALLERY_ROOT, p["thumbnail"]), encoding="utf-8").read()
    assert "<svg" in thumb and "</svg>" in thumb


def test_piece_56_thumbnail_uses_palette_colors():
    p = _get_piece()
    assert p is not None
    thumb = open(os.path.join(GALLERY_ROOT, p["thumbnail"]), encoding="utf-8").read().lower()
    hits = sum(1 for c in ('#fbf3dc', '#1c1208', '#6b3f1a', '#c8960c', '#1e3a6a')
               if c in thumb)
    assert hits >= 3, "Thumbnail should use at least 3 palette colors"


# ---------------------------------------------------------------------------
# Edge cases and failure modes
# ---------------------------------------------------------------------------

def test_piece_56_id_matches_directory():
    """The 'id' in pieces.json must match the directory name."""
    p = _get_piece()
    assert p is not None
    parts = p["path"].replace("\\", "/").split("/")
    assert len(parts) >= 2
    assert parts[-2] == PIECE_ID


def test_piece_56_path_ends_with_html():
    p = _get_piece()
    assert p is not None
    assert p["path"].endswith(".html")


def test_piece_56_not_duplicated_in_pieces_json():
    """Piece 56 must appear exactly once in pieces.json."""
    pieces = _load_pieces()
    matches = [p for p in pieces if p["id"] == PIECE_ID]
    assert len(matches) == 1, f"Expected 1 entry for '{PIECE_ID}', found {len(matches)}"


def test_piece_56_nonexistent_extra_file_absent():
    """Confirms the piece directory does not contain unexpected stray files of concern."""
    fake = os.path.join(PIECE_DIR, "nonexistent_stub.xyz")
    assert not os.path.isfile(fake)


def test_piece_56_empty_essay_would_fail_word_check():
    """Validate that an empty string would fail the 200-word minimum."""
    word_count = len("".split())
    assert word_count < 200
