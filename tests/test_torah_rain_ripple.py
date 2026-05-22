"""
Tests for piece 51-torah-like-rain.

Validates the piece-specific acceptance criteria: canvas animation structure,
essay content requirements, pieces.json registration, and differentiation from
the existing 37-dew-of-torah piece.
"""
import json
import os

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")
PIECE_ID = "51-torah-like-rain"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)


def load_pieces():
    with open(PIECES_JSON, "r", encoding="utf-8") as fh:
        return json.load(fh)


def get_piece():
    for p in load_pieces():
        if p["id"] == PIECE_ID:
            return p
    return None


def read_html():
    return open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()


def read_essay():
    return open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()


# ---------------------------------------------------------------------------
# pieces.json registration
# ---------------------------------------------------------------------------

def test_piece_registered_in_pieces_json():
    """Piece must appear in pieces.json."""
    assert get_piece() is not None, f"Piece '{PIECE_ID}' not found in pieces.json"


def test_piece_theme_is_torah_as_water():
    """Theme must be 'Torah as Water' not generic 'Matan Torah' (per orchestrator)."""
    piece = get_piece()
    assert piece is not None
    assert piece["theme"] == "Torah as Water", (
        f"Expected theme 'Torah as Water', got '{piece['theme']}'"
    )


def test_piece_technique_mentions_ripple():
    """Technique field must mention raindrop particle simulation and ripple."""
    piece = get_piece()
    assert piece is not None
    technique = piece["technique"].lower()
    assert "raindrop" in technique or "ripple" in technique, (
        f"Technique '{piece['technique']}' must mention raindrop simulation or ripple waves"
    )


def test_piece_required_fields_present():
    """All nine required fields must be present and non-empty."""
    piece = get_piece()
    assert piece is not None
    required = ("id", "title", "tagline", "year", "theme", "technique", "path", "thumbnail", "essay")
    for field in required:
        assert field in piece and piece[field], (
            f"Piece '{PIECE_ID}' missing or empty required field '{field}'"
        )


# ---------------------------------------------------------------------------
# File layout on disk
# ---------------------------------------------------------------------------

def test_index_html_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "index.html")), (
        f"pieces/{PIECE_ID}/index.html does not exist"
    )


def test_essay_md_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "essay.md")), (
        f"pieces/{PIECE_ID}/essay.md does not exist"
    )


def test_thumbnail_svg_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "thumbnail.svg")), (
        f"pieces/{PIECE_ID}/thumbnail.svg does not exist"
    )


def test_readme_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "README.md")), (
        f"pieces/{PIECE_ID}/README.md does not exist"
    )


# ---------------------------------------------------------------------------
# Canvas animation requirements
# ---------------------------------------------------------------------------

def test_html_uses_request_animation_frame():
    html = read_html()
    assert "requestAnimationFrame" in html, (
        "index.html must use requestAnimationFrame for the animation loop"
    )


def test_html_has_canvas_element():
    html = read_html()
    assert "<canvas" in html, "index.html must contain a <canvas> element"


def test_html_defines_alephbet():
    """All 22 Hebrew letters of the Aleph-Bet must be present in the JS."""
    html = read_html()
    alephbet = ['א','ב','ג','ד','ה','ו','ז','ח','ט','י','כ','ל','מ','נ','ס','ע','פ','צ','ק','ר','ש','ת']
    for letter in alephbet:
        assert letter in html, f"Hebrew letter '{letter}' not found in index.html"


def test_html_background_color_is_deep_blue_black():
    """Background must use the specified deep blue-black palette (#050A12)."""
    html = read_html()
    assert "#050A12" in html or "#050a12" in html, (
        "index.html must use #050A12 (deep blue-black) background"
    )


def test_html_drop_letter_color_is_warm_cream():
    """Rain letters must use warm cream colour (#FFF8E7)."""
    html = read_html()
    assert "#FFF8E7" in html or "#fff8e7" in html, (
        "index.html must use #FFF8E7 (warm cream) for falling letters"
    )


def test_html_ripple_uses_arc():
    """Ripple must be drawn with ctx.arc for expanding circles."""
    html = read_html()
    assert "ctx.arc" in html, (
        "index.html must use ctx.arc to draw ripple circles"
    )


def test_html_ripple_uses_pale_gold():
    """Ripple colour must use pale gold (212,168,48 components)."""
    html = read_html()
    assert "212,168,48" in html or "212, 168, 48" in html, (
        "Ripple colour must use rgba(212,168,48,...) pale gold"
    )


def test_html_ground_at_85_percent():
    """Ground line must be set at 85% of canvas height."""
    html = read_html()
    assert "0.85" in html or "GROUND_RATIO" in html, (
        "Ground line must be defined at 85% of canvas height"
    )


def test_html_pool_capped_at_40():
    """Pool of settled glyphs must be capped at max 40 entries."""
    html = read_html()
    assert "40" in html, (
        "index.html must cap the pool of settled glyphs at 40 entries"
    )


def test_html_spawn_interval_in_range():
    """Spawn interval must use 400ms base with ~300ms randomisation."""
    html = read_html()
    assert "400" in html and "300" in html, (
        "Spawn timing must use 400 + random * 300 ms interval"
    )


def test_html_gravity_acceleration():
    """Drops must accelerate under gravity (ay/ay parameter present)."""
    html = read_html()
    assert "0.04" in html, (
        "Drop gravity acceleration must be defined (0.04 pixels/frame²)"
    )


# ---------------------------------------------------------------------------
# Essay content requirements
# ---------------------------------------------------------------------------

def test_essay_has_300_plus_words():
    """Essay must have at least 300 words."""
    text = read_essay()
    word_count = len(text.split())
    assert word_count >= 300, (
        f"essay.md has only {word_count} words; need at least 300"
    )


def test_essay_cites_deut_32_2():
    """Essay must quote or cite Deuteronomy 32:2."""
    text = read_essay()
    assert "32:2" in text or "Ha'azinu" in text or "יַעֲרֹף" in text, (
        "essay.md must cite Deuteronomy 32:2 or quote from Ha'azinu"
    )


def test_essay_cites_isaiah_55():
    """Essay must reference Isaiah 55."""
    text = read_essay()
    assert "Isaiah 55" in text or "55:10" in text or "55:11" in text, (
        "essay.md must cite Isaiah 55:10-11"
    )


def test_essay_mentions_taanit_7a():
    """Essay must mention Taanit 7a (rain = day of Torah giving)."""
    text = read_essay()
    assert "Taanit 7a" in text or "Taanit" in text, (
        "essay.md must reference Taanit 7a"
    )


def test_essay_mentions_bava_kamma():
    """Essay must mention Bava Kamma 17a (words of Torah compared to water)."""
    text = read_essay()
    assert "Bava Kamma" in text, (
        "essay.md must reference Bava Kamma 17a"
    )


def test_essay_mentions_kiddushin():
    """Essay must mention Kiddushin 30b."""
    text = read_essay()
    assert "Kiddushin" in text, (
        "essay.md must reference Kiddushin 30b"
    )


def test_essay_embedded_in_html():
    """Essay text must be embedded inline in index.html (no runtime fetch)."""
    essay_text = read_essay()
    html = read_html()
    words = [w for w in essay_text.split() if len(w) > 5][:15]
    found = sum(1 for w in words if w in html)
    assert found >= 8, (
        f"index.html does not appear to embed essay text ({found}/15 sampled words found)"
    )


# ---------------------------------------------------------------------------
# Differentiation from 37-dew-of-torah
# ---------------------------------------------------------------------------

def test_essay_contrasts_rain_with_dew():
    """Essay must articulate the contrast between rain (force) and dew (gentle)."""
    text = read_essay()
    has_dew = "dew" in text.lower()
    has_rain = "rain" in text.lower()
    assert has_rain and has_dew, (
        "essay.md must discuss both rain and dew to establish the contrast"
    )


def test_palette_differs_from_dew_piece():
    """Background must use #050A12 (not #0a0a12 used by piece 37)."""
    html = read_html()
    assert "#050A12" in html or "#050a12" in html, (
        "index.html must use #050A12 background, not the dew-piece's #0a0a12"
    )


def test_no_duplicate_id_with_dew_piece():
    """Piece ID must not collide with the dew-of-torah piece."""
    pieces = load_pieces()
    ids = [p["id"] for p in pieces]
    assert "37-dew-of-torah" in ids, "Sanity check: dew piece should still exist"
    assert ids.count(PIECE_ID) == 1, f"Piece ID '{PIECE_ID}' appears more than once"


# ---------------------------------------------------------------------------
# Edge cases and failure modes
# ---------------------------------------------------------------------------

def test_thumbnail_is_valid_svg():
    svg = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert "<svg" in svg and "</svg>" in svg, (
        "thumbnail.svg must be valid SVG with opening and closing tags"
    )


def test_piece_year_is_int():
    piece = get_piece()
    assert piece is not None
    assert isinstance(piece["year"], int), (
        f"year must be an integer, got {type(piece['year'])}"
    )


def test_piece_path_format():
    """Path must follow the pieces/<id>/index.html convention."""
    piece = get_piece()
    assert piece is not None
    expected_path = f"pieces/{PIECE_ID}/index.html"
    assert piece["path"] == expected_path, (
        f"Expected path '{expected_path}', got '{piece['path']}'"
    )


def test_missing_piece_returns_none():
    """Helper get_piece returns None for a non-existent piece ID."""
    pieces = load_pieces()
    result = next((p for p in pieces if p["id"] == "99-nonexistent"), None)
    assert result is None, "Non-existent piece ID should return None"


def test_pool_opacity_value_in_html():
    """Settled letters must render at approximately 0.25 opacity."""
    html = read_html()
    assert "0.25" in html, (
        "Pool glyphs must be drawn at opacity ~0.25"
    )
