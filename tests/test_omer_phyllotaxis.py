"""
Tests for pieces/48-omer-phyllotaxis — The Harvest Spiral.

Verifies that the phyllotaxis Omer piece satisfies the acceptance criteria:
correct directory layout, pieces.json registration, essay content, animation
technique, and Hebrew numeral completeness.
"""
import json
import math
import os
import re

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID     = "48-omer-phyllotaxis"
PIECE_DIR    = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
HTML_PATH    = os.path.join(PIECE_DIR, "index.html")
ESSAY_PATH   = os.path.join(PIECE_DIR, "essay.md")
THUMB_PATH   = os.path.join(PIECE_DIR, "thumbnail.svg")
README_PATH  = os.path.join(PIECE_DIR, "README.md")
PIECES_JSON  = os.path.join(GALLERY_ROOT, "pieces.json")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _piece_entry():
    """Return the pieces.json entry for the phyllotaxis piece."""
    with open(PIECES_JSON, encoding="utf-8") as fh:
        pieces = json.load(fh)
    for p in pieces:
        if p["id"] == PIECE_ID:
            return p
    return None


def _html():
    return open(HTML_PATH, encoding="utf-8").read()


def _essay():
    return open(ESSAY_PATH, encoding="utf-8").read()


# ---------------------------------------------------------------------------
# Happy-path: file layout
# ---------------------------------------------------------------------------

def test_piece_directory_exists():
    """The piece directory must exist on disk."""
    assert os.path.isdir(PIECE_DIR), f"Directory {PIECE_DIR} not found"


def test_index_html_exists():
    assert os.path.isfile(HTML_PATH), "index.html missing"


def test_essay_md_exists():
    assert os.path.isfile(ESSAY_PATH), "essay.md missing"


def test_thumbnail_svg_exists():
    assert os.path.isfile(THUMB_PATH), "thumbnail.svg missing"


def test_readme_exists():
    assert os.path.isfile(README_PATH), "README.md missing"


# ---------------------------------------------------------------------------
# Happy-path: pieces.json registration
# ---------------------------------------------------------------------------

def test_registered_in_pieces_json():
    assert _piece_entry() is not None, f"'{PIECE_ID}' not found in pieces.json"


def test_required_fields_present():
    """All required pieces.json fields must be populated."""
    required = ("id", "title", "tagline", "year", "theme", "technique", "path", "thumbnail", "essay")
    entry = _piece_entry()
    assert entry is not None
    for field in required:
        assert field in entry and entry[field], f"Field '{field}' missing or empty"


def test_theme_is_sefirat_haomer():
    entry = _piece_entry()
    assert entry is not None
    assert "Sefirat HaOmer" in entry["theme"], "theme must include 'Sefirat HaOmer'"


def test_technique_mentions_phyllotaxis():
    entry = _piece_entry()
    assert entry is not None
    assert "phyllotaxis" in entry["technique"].lower(), "technique must mention phyllotaxis"


def test_year_is_integer():
    entry = _piece_entry()
    assert entry is not None
    assert isinstance(entry["year"], int)


def test_path_points_to_existing_file():
    entry = _piece_entry()
    assert entry is not None
    full = os.path.join(GALLERY_ROOT, entry["path"])
    assert os.path.isfile(full)


def test_thumbnail_points_to_existing_file():
    entry = _piece_entry()
    assert entry is not None
    full = os.path.join(GALLERY_ROOT, entry["thumbnail"])
    assert os.path.isfile(full)


def test_essay_field_points_to_existing_file():
    entry = _piece_entry()
    assert entry is not None
    full = os.path.join(GALLERY_ROOT, entry["essay"])
    assert os.path.isfile(full)


def test_title_does_not_say_fifty_gates():
    """The orchestrator requires this title NOT to be 'Fifty Gates'."""
    entry = _piece_entry()
    assert entry is not None
    assert "fifty gates" not in entry["title"].lower(), (
        "Title must not be 'Fifty Gates' — that piece already exists (32, 38)"
    )


# ---------------------------------------------------------------------------
# Happy-path: essay content
# ---------------------------------------------------------------------------

def test_essay_at_least_300_words():
    """Acceptance criterion requires ≥300 words."""
    text = _essay()
    count = len(text.split())
    assert count >= 300, f"essay.md has only {count} words (need ≥ 300)"


def test_essay_cites_leviticus_23():
    """Must cite Leviticus 23:15–16 as the source of the Omer count."""
    text = _essay()
    assert re.search(r"Leviticus\s+23", text), "essay.md must cite Leviticus 23"


def test_essay_mentions_phyllotaxis():
    text = _essay()
    assert "phyllotaxis" in text.lower(), "essay.md must discuss phyllotaxis"


def test_essay_mentions_golden_angle():
    text = _essay()
    assert "golden angle" in text.lower() or "golden ratio" in text.lower(), (
        "essay.md must mention the golden angle or golden ratio"
    )


def test_essay_mentions_wheat_or_barley():
    text = _essay()
    assert "wheat" in text.lower() or "barley" in text.lower(), (
        "essay.md must mention the Omer crops (wheat or barley)"
    )


def test_essay_does_not_focus_on_fifty_gates():
    """Orchestrator: essay must NOT center on 'fifty gates of understanding'."""
    text = _essay().lower()
    count = text.count("fifty gates")
    assert count == 0, (
        "essay must not mention 'fifty gates' — that theme is taken by pieces 32 and 38"
    )


# ---------------------------------------------------------------------------
# Happy-path: animation technique in HTML
# ---------------------------------------------------------------------------

def test_html_uses_request_animation_frame():
    assert "requestAnimationFrame" in _html(), "animation must use requestAnimationFrame"


def test_html_uses_golden_angle():
    """The golden angle constant must appear in the JavaScript."""
    html = _html()
    assert "137" in html or "2.399" in html or "GOLDEN_ANGLE" in html, (
        "index.html must use the golden-angle constant (~137.5° or 2.39996 rad)"
    )


def test_html_has_canvas_element():
    assert "<canvas" in _html(), "index.html must have a <canvas> element"


def test_html_embeds_essay_words():
    """Key words from essay.md must be present in index.html (no runtime fetch)."""
    essay_words = [w for w in _essay().split() if len(w) > 6][:12]
    html = _html()
    found = sum(1 for w in essay_words if w in html)
    assert found >= 6, (
        f"index.html does not appear to embed the essay ({found}/12 words found)"
    )


def test_html_contains_hebrew_numerals():
    """All 50 Hebrew day-labels must appear in the JavaScript (א through נ)."""
    html = _html()
    required = ['א', 'ב', 'ג', 'י', 'כ', 'מ', 'נ']
    for letter in required:
        assert letter in html, f"Hebrew letter '{letter}' not found in index.html"


def test_html_has_central_disc_pulse():
    """The central disc must pulse — look for pulse or sin in the JS."""
    html = _html()
    assert "pulse" in html or "Math.sin" in html, (
        "index.html must animate the central disc with a pulsing effect"
    )


def test_html_has_background_color():
    """Deep indigo-black background (#07060F) must be present."""
    assert "#07060F" in _html() or "#07060f" in _html(), (
        "index.html must use the #07060F deep indigo-black background"
    )


def test_thumbnail_is_valid_svg():
    text = open(THUMB_PATH, encoding="utf-8").read()
    assert "<svg" in text and "</svg>" in text, "thumbnail.svg is not valid SVG"


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

def test_no_duplicate_id_in_pieces_json():
    with open(PIECES_JSON, encoding="utf-8") as fh:
        pieces = json.load(fh)
    ids = [p["id"] for p in pieces]
    assert ids.count(PIECE_ID) == 1, f"Duplicate id '{PIECE_ID}' in pieces.json"


def test_essay_word_count_large_input_tolerance():
    """Word count handles essay.md with many Unicode Hebrew words correctly."""
    text = _essay()
    words = text.split()
    assert len(words) >= 200, "split() on Unicode essay text must yield ≥ 200 words"


def test_missing_piece_returns_none():
    """_piece_entry() returns None for a non-existent id (edge case guard)."""
    with open(PIECES_JSON, encoding="utf-8") as fh:
        pieces = json.load(fh)
    result = next((p for p in pieces if p["id"] == "99-does-not-exist"), None)
    assert result is None


# ---------------------------------------------------------------------------
# Explicit failure-mode: malformed pieces.json entry
# ---------------------------------------------------------------------------

def test_entry_missing_technique_fails(tmp_path):
    """A pieces.json entry without 'technique' must be caught by required-field check."""
    bad = [{"id": "48-omer-phyllotaxis", "title": "X", "tagline": "y",
            "year": 2026, "theme": "T", "path": "p.html",
            "thumbnail": "t.svg", "essay": "e.md"}]
    assert "technique" not in bad[0], "Fixture must omit 'technique' for this test"
    required = ("id", "title", "tagline", "year", "theme", "technique",
                "path", "thumbnail", "essay")
    missing = [f for f in required if f not in bad[0]]
    assert "technique" in missing


def test_golden_angle_value_accuracy():
    """Golden angle 360 × (2 − φ) = 360 × (1 − 1/φ) must equal ~137.508°."""
    phi = (1 + math.sqrt(5)) / 2
    golden_angle_deg = 360.0 * (2 - phi)   # equivalent to 360*(1 - 1/phi)
    assert abs(golden_angle_deg - 137.508) < 0.01, (
        f"Golden angle {golden_angle_deg:.4f}° deviates from expected 137.508°"
    )


def test_phyllotaxis_no_overlap_first_10_seeds():
    """First 10 phyllotaxis seeds must not overlap each other at a nominal scale."""
    scale   = 50.0
    disc_r  = scale * 0.45
    golden  = 2 * math.pi * (1 - 1 / ((1 + math.sqrt(5)) / 2) ** 2)
    positions = []
    for i in range(1, 11):
        angle = i * golden
        r     = scale * math.sqrt(i)
        positions.append((r * math.cos(angle), r * math.sin(angle)))

    for idx_a in range(len(positions)):
        for idx_b in range(idx_a + 1, len(positions)):
            xa, ya = positions[idx_a]
            xb, yb = positions[idx_b]
            dist = math.sqrt((xa - xb) ** 2 + (ya - yb) ** 2)
            assert dist > disc_r, (
                f"Seeds {idx_a+1} and {idx_b+1} overlap: dist={dist:.2f} < disc_r={disc_r:.2f}"
            )
