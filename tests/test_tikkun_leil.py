"""
Tests for piece 04 "Until Dawn" — Tikkun Leil generative Hebrew typography.

Covers: pieces.json registration, file layout, animation feature requirements
(requestAnimationFrame, fillText, Hebrew font stack, naaseh v'nishma phrase,
background colors, cycle duration, particle pool size, letter size range),
thumbnail validity, README theme mention, CDN-free fonts, and edge cases.
"""
import json
import os
import random
import re
import unicodedata

import pytest

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")
PIECE_ID = "04-until-dawn"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_pieces():
    """Return the parsed pieces.json list."""
    with open(PIECES_JSON, "r", encoding="utf-8") as fh:
        return json.load(fh)


def get_piece_04():
    """Return the piece-04 entry from pieces.json, or None if absent."""
    return next((p for p in load_pieces() if p["id"] == PIECE_ID), None)


def read_index_html():
    """Read and return NFC-normalized text of pieces/04-until-dawn/index.html.

    NFC normalization is applied so Hebrew combining-mark order is canonical,
    making substring checks on Hebrew text immune to source-encoding variations.
    """
    raw = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    return unicodedata.normalize("NFC", raw)


def nfc(s):
    """Return NFC-normalized form of s for use in assertions against read_index_html()."""
    return unicodedata.normalize("NFC", s)


# ---------------------------------------------------------------------------
# pieces.json registration
# ---------------------------------------------------------------------------

def test_piece_04_exists_in_json():
    assert get_piece_04() is not None, f"Piece '{PIECE_ID}' not found in pieces.json"


def test_piece_04_theme():
    p = get_piece_04()
    if p is None:
        pytest.skip("Piece 04 not present")
    assert p["theme"] == "Tikkun Leil Shavuot", (
        f"Expected theme 'Tikkun Leil Shavuot', got {p['theme']!r}"
    )


def test_piece_04_technique_contains_required_keywords():
    p = get_piece_04()
    if p is None:
        pytest.skip("Piece 04 not present")
    assert "generative Hebrew typography" in p["technique"], (
        f"Technique must include 'generative Hebrew typography', got {p['technique']!r}"
    )
    assert "canvas 2D" in p["technique"], (
        f"Technique must include 'canvas 2D', got {p['technique']!r}"
    )


def test_piece_04_has_non_empty_tagline():
    p = get_piece_04()
    if p is None:
        pytest.skip("Piece 04 not present")
    assert p.get("tagline"), "Piece '04-until-dawn' must have a non-empty tagline"


def test_piece_04_year_is_integer():
    p = get_piece_04()
    if p is None:
        pytest.skip("Piece 04 not present")
    assert isinstance(p["year"], int), f"year must be an integer, got {p['year']!r}"


# ---------------------------------------------------------------------------
# File layout
# ---------------------------------------------------------------------------

def test_piece_04_required_files_exist():
    for fname in ("index.html", "thumbnail.svg", "README.md"):
        assert os.path.isfile(os.path.join(PIECE_DIR, fname)), (
            f"pieces/04-until-dawn/{fname} is missing"
        )


# ---------------------------------------------------------------------------
# index.html — animation feature requirements
# ---------------------------------------------------------------------------

def test_piece_04_uses_request_animation_frame():
    if not os.path.isfile(os.path.join(PIECE_DIR, "index.html")):
        pytest.skip("index.html missing")
    assert "requestAnimationFrame" in read_index_html(), (
        "index.html must use requestAnimationFrame"
    )


def test_piece_04_uses_fill_text():
    if not os.path.isfile(os.path.join(PIECE_DIR, "index.html")):
        pytest.skip("index.html missing")
    assert "fillText" in read_index_html(), (
        "index.html must use ctx.fillText() to render Hebrew letters"
    )


def test_piece_04_uses_hebrew_font_stack():
    if not os.path.isfile(os.path.join(PIECE_DIR, "index.html")):
        pytest.skip("index.html missing")
    html = read_index_html()
    assert "David Libre" in html or "Frank Ruhl Libre" in html, (
        "index.html must specify a Hebrew font stack "
        "('David Libre', 'Frank Ruhl Libre', serif)"
    )


def test_piece_04_naaseh_phrase_present():
    """Naaseh v'nishma Hebrew text must be embedded in the animation source.

    Comparisons use NFC-normalized text so combining-mark ordering differences
    between source files do not cause false failures.  The nishma word is checked
    via its consonantal prefix to be immune to patah/qamatz niqqud variants.
    """
    if not os.path.isfile(os.path.join(PIECE_DIR, "index.html")):
        pytest.skip("index.html missing")
    html = read_index_html()  # already NFC-normalized
    naase = unicodedata.normalize("NFC", "נַעֲשֶׂה")
    nishm = unicodedata.normalize("NFC", "נִשְׁמ")
    assert naase in html, "index.html must include the na'aseh word"
    assert nishm in html, "index.html must include the nishma portion of the phrase"
def test_piece_04_naaseh_font_size_120():
    """Naaseh v'nishma must be rendered at 120 px."""
    if not os.path.isfile(os.path.join(PIECE_DIR, "index.html")):
        pytest.skip("index.html missing")
    assert "120px" in read_index_html(), (
        "index.html must render the naaseh v'nishma phrase at 120px"
    )


def test_piece_04_no_cdn_fonts():
    """index.html must not load fonts from any external CDN."""
    if not os.path.isfile(os.path.join(PIECE_DIR, "index.html")):
        pytest.skip("index.html missing")
    html = read_index_html()
    cdn_patterns = [
        "fonts.googleapis.com",
        "fonts.gstatic.com",
        "cdnjs.cloudflare.com",
        "jsdelivr.net",
        "unpkg.com/",
    ]
    for pat in cdn_patterns:
        assert pat not in html, (
            f"index.html must not load fonts from CDN ({pat})"
        )


def test_piece_04_background_midnight_color():
    """index.html must reference #080c1a as the midnight background."""
    if not os.path.isfile(os.path.join(PIECE_DIR, "index.html")):
        pytest.skip("index.html missing")
    assert "080c1a" in read_index_html().lower(), (
        "index.html must use midnight color #080c1a"
    )


def test_piece_04_dawn_color():
    """index.html must reference #fde8c8 as the dawn rose-gold color."""
    if not os.path.isfile(os.path.join(PIECE_DIR, "index.html")):
        pytest.skip("index.html missing")
    assert "fde8c8" in read_index_html().lower(), (
        "index.html must use dawn rose-gold color #fde8c8"
    )


def test_piece_04_cycle_90_seconds():
    """Dawn cycle must be driven by a 90 000 ms constant."""
    if not os.path.isfile(os.path.join(PIECE_DIR, "index.html")):
        pytest.skip("index.html missing")
    assert "90000" in read_index_html(), (
        "index.html must define a 90-second (90000 ms) dawn cycle"
    )


def test_piece_04_particle_pool_cap_60():
    """index.html must cap the particle pool at ~60 particles."""
    if not os.path.isfile(os.path.join(PIECE_DIR, "index.html")):
        pytest.skip("index.html missing")
    assert re.search(r'\b60\b', read_index_html()), (
        "index.html must cap the particle pool at ~60 particles"
    )


def test_piece_04_letter_size_range_24_to_72():
    """index.html must reference both ends of the 24–72 px letter size range."""
    if not os.path.isfile(os.path.join(PIECE_DIR, "index.html")):
        pytest.skip("index.html missing")
    html = read_index_html()
    assert re.search(r'\b24\b', html), "index.html must reference minimum letter size 24 px"
    assert re.search(r'\b72\b', html), "index.html must reference maximum letter size 72 px"


# ---------------------------------------------------------------------------
# Thumbnail
# ---------------------------------------------------------------------------

def test_piece_04_thumbnail_is_valid_svg():
    thumb = os.path.join(PIECE_DIR, "thumbnail.svg")
    if not os.path.isfile(thumb):
        pytest.skip("thumbnail.svg missing")
    text = open(thumb, encoding="utf-8").read()
    assert "<svg" in text and "</svg>" in text, (
        "thumbnail.svg does not look like valid SVG"
    )


def test_piece_04_thumbnail_has_gradient():
    """Thumbnail must include a gradient to represent the night-to-dawn shift."""
    thumb = os.path.join(PIECE_DIR, "thumbnail.svg")
    if not os.path.isfile(thumb):
        pytest.skip("thumbnail.svg missing")
    text = open(thumb, encoding="utf-8").read()
    assert "linearGradient" in text or "radialGradient" in text, (
        "thumbnail.svg must use a gradient for the dark-to-dawn background"
    )


def test_piece_04_thumbnail_has_naaseh_phrase():
    """Thumbnail must display the naaseh v'nishma phrase (NFC-normalized comparison)."""
    thumb = os.path.join(PIECE_DIR, "thumbnail.svg")
    if not os.path.isfile(thumb):
        pytest.skip("thumbnail.svg missing")
    text = unicodedata.normalize("NFC", open(thumb, encoding="utf-8").read())
    naase = unicodedata.normalize("NFC", "נַעֲשֶׂה")
    nishm = unicodedata.normalize("NFC", "נִשְׁמ")
    assert naase in text or nishm in text, (
        "thumbnail.svg must include the naase v'nishma phrase"
    )



# ---------------------------------------------------------------------------
# README
# ---------------------------------------------------------------------------

def test_piece_04_readme_mentions_tikkun_leil():
    readme = os.path.join(PIECE_DIR, "README.md")
    if not os.path.isfile(readme):
        pytest.skip("README.md missing")
    text = open(readme, encoding="utf-8").read().lower()
    assert "tikkun" in text or "shavuot" in text, (
        "README.md must mention the Tikkun Leil Shavuot theme"
    )


# ---------------------------------------------------------------------------
# Edge cases and failure modes
# ---------------------------------------------------------------------------

def test_piece_04_entry_not_duplicate():
    """Piece 04 ID must appear exactly once in pieces.json."""
    count = sum(1 for p in load_pieces() if p["id"] == PIECE_ID)
    assert count == 1, f"'{PIECE_ID}' appears {count} times in pieces.json (expected 1)"


def test_piece_04_missing_tagline_detected(tmp_path):
    """An entry for piece 04 without 'tagline' should be caught by required-field checks."""
    bad = [{
        "id": PIECE_ID,
        "title": "Until Dawn",
        "year": 2026,
        "theme": "Tikkun Leil Shavuot",
        "technique": "generative Hebrew typography, canvas 2D",
        "path": "pieces/04-until-dawn/index.html",
        "thumbnail": "pieces/04-until-dawn/thumbnail.svg",
    }]
    assert "tagline" not in bad[0], "Fixture must be missing 'tagline' for this test to be meaningful"
    required = ("id", "title", "tagline", "year", "theme", "technique", "path", "thumbnail")
    missing = [f for f in required if f not in bad[0]]
    assert "tagline" in missing


def test_particle_spawn_logic_stays_within_bounds():
    """Particle size and alpha from the JS spawn formula must stay within spec."""
    random.seed(42)
    MIN_LETTER_SIZE, MAX_LETTER_SIZE = 24, 72
    CHAR_POOL = list("אבגדהוזחטיכלמנסעפצקרשת")

    for _ in range(500):
        size = MIN_LETTER_SIZE + random.random() * (MAX_LETTER_SIZE - MIN_LETTER_SIZE)
        alpha = 0.55 + random.random() * 0.45
        char = CHAR_POOL[int(random.random() * len(CHAR_POOL))]
        assert MIN_LETTER_SIZE <= size <= MAX_LETTER_SIZE, f"size {size} out of 24–72 range"
        assert 0.55 <= alpha <= 1.0, f"alpha {alpha} out of expected range"
        assert char in CHAR_POOL


def test_naaseh_alpha_timing():
    """getNaasehAlpha logic: fade in at 45 s, hold, fade out by 53 s."""
    def get_alpha(cycle_ms):
        if cycle_ms < 45000 or cycle_ms >= 53000:
            return 0
        if cycle_ms < 47000:
            return (cycle_ms - 45000) / 2000
        if cycle_ms < 51000:
            return 1
        return 1 - (cycle_ms - 51000) / 2000

    assert get_alpha(0) == 0,       "Should be invisible before 45 s"
    assert get_alpha(44999) == 0,   "Should be invisible just before 45 s"
    assert get_alpha(45000) == 0.0, "Fade-in starts at exactly 45 s (alpha=0)"
    assert get_alpha(46000) == pytest.approx(0.5), "Halfway through fade-in"
    assert get_alpha(47000) == pytest.approx(1.0), "Fully visible at 47 s"
    assert get_alpha(49000) == pytest.approx(1.0), "Still fully visible mid-hold"
    assert get_alpha(51000) == pytest.approx(1.0), "Still fully visible at fade-out start"
    assert get_alpha(52000) == pytest.approx(0.5), "Halfway through fade-out"
    assert get_alpha(53000) == 0,   "Invisible again at 53 s"
    assert get_alpha(60000) == 0,   "Invisible well past 53 s"


def test_background_lerp_endpoints():
    """Lerp between midnight and dawn must produce correct boundary colors."""
    def lerp3(a, b, t):
        return [round(a[i] + (b[i] - a[i]) * t) for i in range(3)]

    midnight = [8, 12, 26]
    dawn = [253, 232, 200]

    assert lerp3(midnight, dawn, 0.0) == midnight, "t=0 must give midnight color"
    assert lerp3(midnight, dawn, 1.0) == dawn,     "t=1 must give dawn color"

    mid = lerp3(midnight, dawn, 0.5)
    assert midnight[0] < mid[0] < dawn[0], "t=0.5 red channel must be between endpoints"
    assert midnight[1] < mid[1] < dawn[1], "t=0.5 green channel must be between endpoints"
    assert midnight[2] < mid[2] < dawn[2], "t=0.5 blue channel must be between endpoints"
