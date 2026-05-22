"""
Tests for piece 43-rose-of-sharon — Rhodonea Curves of the Covenant.

Validates the piece-specific acceptance criteria: canvas animation content,
Hebrew inscription, palette colors, opacity values, essay sources, and
pieces.json registration.
"""
import json
import os
import re

import pytest

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID = "43-rose-of-sharon"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
HTML_PATH = os.path.join(PIECE_DIR, "index.html")
ESSAY_PATH = os.path.join(PIECE_DIR, "essay.md")
THUMB_PATH = os.path.join(PIECE_DIR, "thumbnail.svg")
README_PATH = os.path.join(PIECE_DIR, "README.md")
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def html():
    """Return the full text of index.html."""
    return open(HTML_PATH, encoding="utf-8").read()


def essay():
    """Return the full text of essay.md."""
    return open(ESSAY_PATH, encoding="utf-8").read()


def pieces():
    """Return the parsed pieces.json list."""
    with open(PIECES_JSON, encoding="utf-8") as fh:
        return json.load(fh)


def get_piece():
    """Return the pieces.json entry for this piece, or None."""
    return next((p for p in pieces() if p["id"] == PIECE_ID), None)


# ---------------------------------------------------------------------------
# Directory and file existence
# ---------------------------------------------------------------------------

def test_piece_directory_exists():
    assert os.path.isdir(PIECE_DIR), f"Directory {PIECE_DIR} does not exist"


def test_index_html_exists():
    assert os.path.isfile(HTML_PATH), "index.html is missing"


def test_essay_md_exists():
    assert os.path.isfile(ESSAY_PATH), "essay.md is missing"


def test_thumbnail_svg_exists():
    assert os.path.isfile(THUMB_PATH), "thumbnail.svg is missing"


def test_readme_exists():
    assert os.path.isfile(README_PATH), "README.md is missing"


# ---------------------------------------------------------------------------
# pieces.json registration
# ---------------------------------------------------------------------------

def test_piece_registered_in_pieces_json():
    assert get_piece() is not None, f"'{PIECE_ID}' not found in pieces.json"


def test_piece_json_required_fields():
    piece = get_piece()
    assert piece is not None
    for field in ("id", "title", "tagline", "year", "theme", "technique", "path", "thumbnail", "essay"):
        assert field in piece and piece[field], f"Field '{field}' missing or empty in pieces.json entry"


def test_piece_json_paths_correct():
    piece = get_piece()
    assert piece is not None
    assert piece["path"] == f"pieces/{PIECE_ID}/index.html"
    assert piece["thumbnail"] == f"pieces/{PIECE_ID}/thumbnail.svg"
    assert piece["essay"] == f"pieces/{PIECE_ID}/essay.md"


# ---------------------------------------------------------------------------
# Canvas animation — structural checks in index.html
# ---------------------------------------------------------------------------

def test_html_uses_requestanimationframe():
    assert "requestAnimationFrame" in html(), "index.html must use requestAnimationFrame"


def test_html_has_canvas_element():
    assert "<canvas" in html(), "index.html must contain a <canvas> element"


def test_html_has_six_k_values():
    """Six distinct k = p/q values must appear in the animation JS."""
    text = html()
    # Match numeric literals that correspond to k values: 3, 5/2, 7/3, 4/3, 8/3, 9/4
    # The JS uses expressions like: { k: 3, ... }, { k: 5 / 2, ... }, etc.
    # Check that at least 5 distinct k-value snippets appear
    k_patterns = [
        r"\bk\s*:\s*3\b",
        r"\bk\s*:\s*5\s*/\s*2\b",
        r"\bk\s*:\s*7\s*/\s*3\b",
        r"\bk\s*:\s*4\s*/\s*3\b",
        r"\bk\s*:\s*8\s*/\s*3\b",
        r"\bk\s*:\s*9\s*/\s*4\b",
    ]
    found = sum(1 for pat in k_patterns if re.search(pat, text))
    assert found >= 5, f"Expected at least 5 distinct k = p/q entries, found {found}"


def test_html_opacity_values_in_range():
    """Opacity values must be in the 0.5–0.7 range per acceptance criteria."""
    text = html()
    opacity_vals = re.findall(r"opacity\s*:\s*([\d.]+)", text)
    numeric = [float(v) for v in opacity_vals if v]
    assert numeric, "No opacity values found in index.html JS"
    for val in numeric:
        assert 0.45 <= val <= 0.72, (
            f"Opacity value {val} is outside the expected 0.45–0.72 range"
        )


# ---------------------------------------------------------------------------
# Palette colors in index.html
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("color", ["#FDF6E3", "#E8A0A0", "#6B2040", "#D4A843", "#1A1035"])
def test_html_contains_palette_color(color):
    """Each required palette color must appear somewhere in index.html."""
    assert color.lower() in html().lower(), f"Palette color {color} not found in index.html"


# ---------------------------------------------------------------------------
# Hebrew inscription
# ---------------------------------------------------------------------------

def test_html_contains_hebrew_text():
    """The Hebrew verse from Song of Songs 2:1 must appear in index.html."""
    # Check for key Hebrew letters that form the inscription
    assert "חֲבַצֶּלֶת" in html() or "חבצלת" in html(), (
        "Hebrew text 'חֲבַצֶּלֶת' (rose of Sharon) not found in index.html"
    )


def test_html_contains_sharon_hebrew():
    """The word Sharon (הַשָּׁרוֹן) must appear in index.html."""
    assert "הַשָּׁרוֹן" in html() or "השרון" in html(), (
        "Hebrew 'השרון' (Sharon) not found in index.html"
    )


def test_html_uses_rtl_direction():
    """The animation must set text direction to rtl for the Hebrew inscription."""
    assert "rtl" in html(), "index.html must set direction = 'rtl' for Hebrew text"


# ---------------------------------------------------------------------------
# Glow / shadow blur
# ---------------------------------------------------------------------------

def test_html_uses_shadow_blur():
    """shadowBlur must be set to produce the glow effect per acceptance criteria."""
    assert "shadowBlur" in html(), "index.html must use shadowBlur for the glow effect"


def test_html_uses_screen_compositing():
    """Screen compositing is required for luminous petal overlaps on dark background."""
    assert "screen" in html(), "index.html must use globalCompositeOperation = 'screen'"


# ---------------------------------------------------------------------------
# Essay content — required sources and themes
# ---------------------------------------------------------------------------

def test_essay_mentions_song_of_songs_2_1():
    text = essay()
    assert "2:1" in text, "essay.md must explicitly cite Song of Songs 2:1"


def test_essay_mentions_shabbat_88b():
    text = essay().lower()
    assert "shabbat 88b" in text or "shabbat 88" in text, (
        "essay.md must cite Shabbat 88b (allegorical reading of Song of Songs)"
    )


def test_essay_mentions_yadayim_3_5():
    text = essay().lower()
    assert "yadayim 3:5" in text or "yadayim 3" in text, (
        "essay.md must cite Yadayim 3:5 (Rabbi Akiva's 'holy of holies' declaration)"
    )


def test_essay_mentions_rabbi_akiva():
    assert "Akiva" in essay() or "akiva" in essay().lower(), (
        "essay.md must mention Rabbi Akiva"
    )


def test_essay_mentions_deveikut():
    text = essay().lower()
    assert "deveikut" in text or "devekut" in text, (
        "essay.md must explain the kabbalistic concept of deveikut (clinging/union)"
    )


def test_essay_mentions_rhodonea():
    text = essay().lower()
    assert "rhodonea" in text, "essay.md must explain the rhodonea curve geometry"


def test_essay_word_count():
    text = essay()
    word_count = len(text.split())
    assert word_count >= 400, f"essay.md has only {word_count} words (need at least 400)"


# ---------------------------------------------------------------------------
# Essay text embedded in index.html
# ---------------------------------------------------------------------------

def test_html_embeds_essay_words():
    """index.html must embed substantial essay content inline."""
    essay_text = essay()
    html_text = html()
    long_words = [w for w in essay_text.split() if len(w) > 6][:15]
    found = sum(1 for w in long_words if w in html_text)
    assert found >= 8, (
        f"index.html embeds too few essay words: {found}/15 sampled long words found"
    )


# ---------------------------------------------------------------------------
# Thumbnail is valid SVG
# ---------------------------------------------------------------------------

def test_thumbnail_is_valid_svg():
    text = open(THUMB_PATH, encoding="utf-8").read()
    assert "<svg" in text and "</svg>" in text, "thumbnail.svg does not contain valid SVG markup"


def test_thumbnail_has_background_fill():
    text = open(THUMB_PATH, encoding="utf-8").read()
    assert "1A1035" in text or "1a1035" in text, (
        "thumbnail.svg must use the deep indigo background #1A1035"
    )


def test_thumbnail_has_multiple_paths():
    text = open(THUMB_PATH, encoding="utf-8").read()
    path_count = text.count("<path")
    assert path_count >= 5, f"thumbnail.svg has only {path_count} <path> elements (need at least 5)"


# ---------------------------------------------------------------------------
# Edge-case / failure-mode tests
# ---------------------------------------------------------------------------

def test_html_not_empty():
    text = html()
    assert len(text) > 2000, f"index.html seems too short ({len(text)} chars); likely incomplete"


def test_essay_not_stub():
    text = essay()
    assert "placeholder" not in text.lower(), "essay.md appears to be a placeholder stub"
    assert "todo" not in text.lower(), "essay.md contains a TODO marker"


def test_pieces_json_no_duplicate_ids():
    """Adding the new piece must not create a duplicate ID."""
    all_ids = [p["id"] for p in pieces()]
    assert len(all_ids) == len(set(all_ids)), f"Duplicate IDs in pieces.json: {all_ids}"


def test_missing_piece_id_returns_none():
    """Helper get_piece returns None for non-existent IDs — guard for test fixture reliability."""
    all_pieces = pieces()
    result = next((p for p in all_pieces if p["id"] == "99-nonexistent-piece"), None)
    assert result is None, "Expected None for non-existent piece ID"


def test_gen_thumbnail_script_exists():
    """gen_thumbnail.py must exist so the thumbnail can be regenerated."""
    gen_path = os.path.join(PIECE_DIR, "gen_thumbnail.py")
    assert os.path.isfile(gen_path), "gen_thumbnail.py is missing from piece directory"
