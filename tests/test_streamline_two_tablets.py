"""
Tests for piece 94-streamline-two-tablets.

Verifies the piece directory, file layout, pieces.json registration, essay
content, and structural correctness of the index.html canvas animation.
"""
import json
import os
import re


GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID = "94-streamline-two-tablets"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")


def _load_pieces():
    with open(PIECES_JSON, encoding="utf-8") as fh:
        return json.load(fh)


def _get_piece():
    for p in _load_pieces():
        if p["id"] == PIECE_ID:
            return p
    return None


# ---------------------------------------------------------------------------
# Directory and file layout
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
    piece = _get_piece()
    assert piece is not None, f"Piece '{PIECE_ID}' not found in pieces.json"


def test_piece_required_fields():
    piece = _get_piece()
    assert piece is not None
    for field in ("id", "title", "tagline", "year", "theme", "technique", "path", "thumbnail", "essay"):
        assert field in piece and piece[field], f"Field '{field}' missing or empty"


def test_piece_theme_contains_luchot():
    piece = _get_piece()
    assert piece is not None
    assert "Luchot" in piece["theme"] or "luchot" in piece["theme"], (
        "Theme must mention Luchot habrit"
    )


def test_piece_technique_contains_rk4():
    piece = _get_piece()
    assert piece is not None
    assert "RK4" in piece["technique"] or "rk4" in piece["technique"].lower(), (
        "Technique must mention RK4 integration"
    )


def test_piece_year_is_2026():
    piece = _get_piece()
    assert piece is not None
    assert piece["year"] == 2026


# ---------------------------------------------------------------------------
# thumbnail.svg structural checks
# ---------------------------------------------------------------------------

def test_thumbnail_is_valid_svg():
    path = os.path.join(PIECE_DIR, "thumbnail.svg")
    text = open(path, encoding="utf-8").read()
    assert "<svg" in text and "</svg>" in text


def test_thumbnail_has_correct_dimensions():
    path = os.path.join(PIECE_DIR, "thumbnail.svg")
    text = open(path, encoding="utf-8").read()
    assert 'width="400"' in text and 'height="400"' in text


def test_thumbnail_contains_tablets():
    """Thumbnail must show the two tablet outlines (rect elements)."""
    path = os.path.join(PIECE_DIR, "thumbnail.svg")
    text = open(path, encoding="utf-8").read()
    rects = re.findall(r"<rect", text)
    assert len(rects) >= 3, "Thumbnail must contain at least 2 tablet rects plus background"


def test_thumbnail_contains_field_lines():
    """Thumbnail must contain path elements representing field lines."""
    path = os.path.join(PIECE_DIR, "thumbnail.svg")
    text = open(path, encoding="utf-8").read()
    paths = re.findall(r"<path", text)
    assert len(paths) >= 5, "Thumbnail must contain at least 5 field-line path elements"


def test_thumbnail_contains_hebrew_title():
    path = os.path.join(PIECE_DIR, "thumbnail.svg")
    text = open(path, encoding="utf-8").read()
    assert "לוּחוֹת" in text or "לוחות" in text, "Thumbnail must contain Hebrew title text"


def test_thumbnail_contains_roman_numerals():
    path = os.path.join(PIECE_DIR, "thumbnail.svg")
    text = open(path, encoding="utf-8").read()
    assert "VI" in text and "X" in text and "I" in text, (
        "Thumbnail must contain Roman numerals"
    )


def test_thumbnail_electric_blue_palette():
    """Thumbnail must use the electric blue palette specified in the acceptance criteria."""
    path = os.path.join(PIECE_DIR, "thumbnail.svg")
    text = open(path, encoding="utf-8").read()
    has_blue = "#4FC3F7" in text or "#00BCD4" in text or "#0D47A1" in text
    assert has_blue, "Thumbnail must use the electric blue / cobalt palette"


# ---------------------------------------------------------------------------
# essay.md content checks
# ---------------------------------------------------------------------------

def test_essay_min_words():
    path = os.path.join(PIECE_DIR, "essay.md")
    text = open(path, encoding="utf-8").read()
    assert len(text.split()) >= 400, "essay.md must have at least 400 words"


def test_essay_opens_with_exodus_31_18():
    path = os.path.join(PIECE_DIR, "essay.md")
    text = open(path, encoding="utf-8").read()
    assert "31:18" in text or "31" in text, "Essay must cite Exodus 31:18"


def test_essay_mentions_bava_batra():
    path = os.path.join(PIECE_DIR, "essay.md")
    text = open(path, encoding="utf-8").read()
    assert "Bava Batra" in text, "Essay must mention Bava Batra 14a (fragments in the Ark)"


def test_essay_mentions_rk4():
    path = os.path.join(PIECE_DIR, "essay.md")
    text = open(path, encoding="utf-8").read()
    assert "RK4" in text or "Runge-Kutta" in text, "Essay must explain the RK4 algorithm"


def test_essay_non_crossing_theorem():
    path = os.path.join(PIECE_DIR, "essay.md")
    text = open(path, encoding="utf-8").read()
    assert "never cross" in text or "non-crossing" in text or "do not contradict" in text, (
        "Essay must discuss the non-crossing property of field lines"
    )


# ---------------------------------------------------------------------------
# index.html structural and content checks
# ---------------------------------------------------------------------------

def test_index_html_has_canvas():
    path = os.path.join(PIECE_DIR, "index.html")
    text = open(path, encoding="utf-8").read()
    assert "<canvas" in text, "index.html must contain a <canvas> element"


def test_index_html_uses_requestanimationframe():
    path = os.path.join(PIECE_DIR, "index.html")
    text = open(path, encoding="utf-8").read()
    assert "requestAnimationFrame" in text


def test_index_html_has_rk4_function():
    """index.html must implement an RK4 step function."""
    path = os.path.join(PIECE_DIR, "index.html")
    text = open(path, encoding="utf-8").read()
    assert "rk4" in text.lower() or "k1" in text and "k2" in text, (
        "index.html must contain RK4 integration code"
    )


def test_index_html_has_dipole_field():
    path = os.path.join(PIECE_DIR, "index.html")
    text = open(path, encoding="utf-8").read()
    assert "dipole" in text.lower() or "dipoleField" in text, (
        "index.html must implement dipole field computation"
    )


def test_index_html_embeds_essay_text():
    """index.html must embed the essay text inline (not fetch it at runtime)."""
    essay_path = os.path.join(PIECE_DIR, "essay.md")
    html_path = os.path.join(PIECE_DIR, "index.html")
    essay_words = [w for w in open(essay_path, encoding="utf-8").read().split() if len(w) > 6]
    html = open(html_path, encoding="utf-8").read()
    sampled = essay_words[:12]
    found = sum(1 for w in sampled if w in html)
    assert found >= 6, (
        f"index.html must embed essay text inline; only {found}/12 sampled words found"
    )


def test_index_html_has_bilingual_tanach_excerpt():
    """index.html must include a bilingual Tanach excerpt (Hebrew + English)."""
    path = os.path.join(PIECE_DIR, "index.html")
    text = open(path, encoding="utf-8").read()
    has_hebrew = "וַיִּתֵּן" in text or "לֻחֹת" in text or "אֶת-הַלֻּחֹת" in text
    has_english = "tablets of stone" in text or "finger of God" in text
    assert has_hebrew, "index.html must include the Hebrew Tanach excerpt"
    assert has_english, "index.html must include the English Tanach translation"


def test_index_html_has_tablet_outlines():
    """index.html canvas code must draw tablet outlines."""
    path = os.path.join(PIECE_DIR, "index.html")
    text = open(path, encoding="utf-8").read()
    assert "drawTablets" in text or "tablet" in text.lower(), (
        "index.html must draw the two tablet outlines"
    )


def test_index_html_has_roman_numerals():
    path = os.path.join(PIECE_DIR, "index.html")
    text = open(path, encoding="utf-8").read()
    assert '"I"' in text or "'I'" in text or '"VI"' in text, (
        "index.html must render Roman numerals on the tablets"
    )


def test_index_html_side_by_side_layout():
    """Essay and canvas must be side-by-side on wide screens."""
    path = os.path.join(PIECE_DIR, "index.html")
    text = open(path, encoding="utf-8").read()
    assert "flex-direction: row" in text or "flex-direction:row" in text, (
        "index.html must use a row flex layout for wide screens"
    )


def test_index_html_responsive_breakpoint():
    """index.html must have a responsive breakpoint for narrow screens."""
    path = os.path.join(PIECE_DIR, "index.html")
    text = open(path, encoding="utf-8").read()
    assert "max-width" in text and ("flex-direction: column" in text or "flex-direction:column" in text), (
        "index.html must stack vertically on narrow screens"
    )


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

def test_pieces_json_no_duplicate_ids():
    pieces = _load_pieces()
    ids = [p["id"] for p in pieces]
    assert len(ids) == len(set(ids)), "Duplicate piece IDs in pieces.json"


def test_thumbnail_viewbox_400x400():
    path = os.path.join(PIECE_DIR, "thumbnail.svg")
    text = open(path, encoding="utf-8").read()
    assert 'viewBox="0 0 400 400"' in text, "thumbnail.svg must have viewBox 0 0 400 400"


def test_essay_mentions_breathing_animation():
    path = os.path.join(PIECE_DIR, "essay.md")
    text = open(path, encoding="utf-8").read()
    assert "breath" in text.lower() or "drift" in text.lower() or "rotat" in text.lower(), (
        "Essay must describe the breathing/drift animation"
    )


def test_index_html_electric_blue_palette():
    """index.html must reference the required electric-blue palette colours."""
    path = os.path.join(PIECE_DIR, "index.html")
    text = open(path, encoding="utf-8").read()
    has_blue = "#4FC3F7" in text or "#00BCD4" in text or "#0D47A1" in text
    assert has_blue, "index.html must use the electric blue / cobalt palette"
