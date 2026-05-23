"""
Tests for piece 84-rossler-crown-of-torah (Rössler strange attractor / Keter Torah).

Verifies acceptance criteria: file layout, pieces.json registration, essay content,
HTML mechanics (canvas, RK4, particle system, Hebrew watermark), and thumbnail SVG.
"""
import json
import os
import re

import pytest

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID = "84-rossler-crown-of-torah"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
INDEX_HTML = os.path.join(PIECE_DIR, "index.html")
ESSAY_MD = os.path.join(PIECE_DIR, "essay.md")
THUMBNAIL = os.path.join(PIECE_DIR, "thumbnail.svg")
README = os.path.join(PIECE_DIR, "README.md")
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")


def _load_pieces():
    with open(PIECES_JSON, encoding="utf-8") as fh:
        return json.load(fh)


def _get_piece():
    for p in _load_pieces():
        if p["id"] == PIECE_ID:
            return p
    return None


def _html():
    return open(INDEX_HTML, encoding="utf-8").read()


def _essay():
    return open(ESSAY_MD, encoding="utf-8").read()


# ---------------------------------------------------------------------------
# File layout
# ---------------------------------------------------------------------------

def test_piece_directory_exists():
    """The piece directory must be present on disk."""
    assert os.path.isdir(PIECE_DIR)


def test_index_html_exists():
    assert os.path.isfile(INDEX_HTML)


def test_essay_md_exists():
    assert os.path.isfile(ESSAY_MD)


def test_thumbnail_svg_exists():
    assert os.path.isfile(THUMBNAIL)


def test_readme_exists():
    assert os.path.isfile(README)


# ---------------------------------------------------------------------------
# pieces.json registration
# ---------------------------------------------------------------------------

def test_piece_registered_in_pieces_json():
    """pieces.json must contain an entry with id == PIECE_ID."""
    assert _get_piece() is not None, f"{PIECE_ID} not found in pieces.json"


def test_pieces_json_theme():
    p = _get_piece()
    assert p is not None
    assert "Keter Torah" in p["theme"], "theme must reference Keter Torah"


def test_pieces_json_technique():
    p = _get_piece()
    assert p is not None
    assert "Rössler" in p["technique"] or "Rossler" in p["technique"], \
        "technique must mention the Rössler attractor"


def test_pieces_json_paths_correct():
    """The path, thumbnail, and essay fields must point at existing files."""
    p = _get_piece()
    assert p is not None
    for field in ("path", "thumbnail", "essay"):
        full = os.path.join(GALLERY_ROOT, p[field])
        assert os.path.isfile(full), f"pieces.json field '{field}' points to missing file: {p[field]}"


# ---------------------------------------------------------------------------
# essay.md content
# ---------------------------------------------------------------------------

def test_essay_word_count():
    """Essay must be at least 300 words."""
    text = _essay()
    words = text.split()
    assert len(words) >= 300, f"Essay only has {len(words)} words (need ≥ 300)"


def test_essay_cites_pirkei_avot_5_22():
    """Essay must cite Pirkei Avot 5:22 (Ben Bag Bag)."""
    text = _essay()
    assert "5:22" in text or "Avot 5" in text, "Essay must cite Pirkei Avot 5:22"


def test_essay_mentions_three_crowns():
    """Essay must mention the three crowns (Avot 4:13)."""
    text = _essay()
    assert "4:13" in text or "three crown" in text.lower() or "Keter Kehunah" in text, \
        "Essay must discuss the three crowns of Mishnah Avot 4:13"


def test_essay_mentions_pardes():
    """Essay must reference PaRDeS (the four layers of Torah interpretation)."""
    text = _essay()
    assert "PaRDeS" in text or "peshat" in text.lower(), \
        "Essay must reference PaRDeS / layers of Torah meaning"


def test_essay_mentions_rossler():
    """Essay must name Rössler and his attractor."""
    text = _essay()
    assert "Rössler" in text or "Rossler" in text, "Essay must name the Rössler attractor"


def test_essay_mentions_keter():
    """Essay must discuss Keter Torah."""
    text = _essay()
    assert "Keter" in text, "Essay must discuss Keter Torah"


# ---------------------------------------------------------------------------
# index.html — mechanics
# ---------------------------------------------------------------------------

def test_html_has_canvas():
    assert "canvas" in _html()


def test_html_uses_request_animation_frame():
    assert "requestAnimationFrame" in _html()


def test_html_defines_rk4():
    """RK4 integrator must be present in the HTML."""
    text = _html()
    assert "rk4" in text or "RK4" in text, "index.html must define an RK4 integrator"


def test_html_has_rossler_parameters():
    """The classical Rössler parameters a=0.2, b=0.2, c=5.7 must appear."""
    text = _html()
    assert "5.7" in text, "index.html must contain Rössler parameter c = 5.7"
    assert "0.2" in text, "index.html must contain Rössler parameters a = b = 0.2"


def test_html_has_800_particles():
    """800 particles must be specified."""
    text = _html()
    assert "800" in text, "index.html must spawn 800 particles"


def test_html_has_trail_length_60():
    """Trail length of 60 must be specified."""
    text = _html()
    assert "60" in text, "index.html must specify a trail length of 60"


def test_html_has_warmup():
    """500-step warmup must be present."""
    text = _html()
    assert "500" in text, "index.html must warm up particles for 500 steps"


def test_html_has_kaf_watermark():
    """Hebrew letter כ (kaf) must appear as a watermark in the HTML."""
    text = _html()
    assert "כ" in text, "index.html must embed the Hebrew letter כ as a watermark"


def test_html_background_color():
    """Background color #05040F must be present."""
    assert "#05040F" in _html() or "#05040f" in _html().lower()


def test_html_has_gold_color():
    """Gold color #F0C040 must be present for the crown rim."""
    text = _html()
    assert "#F0C040" in text or "#f0c040" in text.lower(), \
        "index.html must use gold color #F0C040 for the crown rim"


def test_html_has_sapphire_color():
    """Sapphire color #1A1A8A must be present for the attractor base."""
    text = _html()
    assert "#1A1A8A" in text or "#1a1a8a" in text.lower(), \
        "index.html must use sapphire color #1A1A8A for the attractor base"


def test_html_dt_is_0_01():
    """Integration step dt = 0.01 must be set."""
    text = _html()
    assert "0.01" in text, "index.html must use dt = 0.01"


def test_html_rotation_rate():
    """Rotation rate 0.001 rad/frame must appear."""
    assert "0.001" in _html()


def test_html_embeds_essay_words():
    """Essay text must be embedded inline — check first 10 long words."""
    essay_words = [w for w in _essay().split() if len(w) > 6][:10]
    html = _html()
    found = sum(1 for w in essay_words if w in html)
    assert found >= 5, f"Only {found}/10 essay words found in index.html — essay may not be embedded"


# ---------------------------------------------------------------------------
# thumbnail.svg content
# ---------------------------------------------------------------------------

def test_thumbnail_is_svg():
    text = open(THUMBNAIL, encoding="utf-8").read()
    assert "<svg" in text and "</svg>" in text


def test_thumbnail_has_dark_background():
    text = open(THUMBNAIL, encoding="utf-8").read()
    assert "#05040F" in text or "#05040f" in text.lower() or "05040" in text.lower()


def test_thumbnail_has_kaf_letter():
    """Thumbnail must contain the Hebrew letter כ."""
    text = open(THUMBNAIL, encoding="utf-8").read()
    assert "כ" in text, "thumbnail.svg must include the Hebrew letter כ"


def test_thumbnail_has_gradient_from_sapphire_to_gold():
    """Thumbnail must contain both sapphire and gold color values."""
    text = open(THUMBNAIL, encoding="utf-8").read()
    has_sapphire = "1A1A8A" in text or "1a1a8a" in text.lower()
    has_gold = "F0C040" in text or "f0c040" in text.lower()
    assert has_sapphire and has_gold, "thumbnail.svg must use sapphire and gold colors"


# ---------------------------------------------------------------------------
# Edge cases and failure modes
# ---------------------------------------------------------------------------

def test_no_duplicate_ids_introduced():
    """Registering the new piece must not create duplicate IDs."""
    ids = [p["id"] for p in _load_pieces()]
    assert ids.count(PIECE_ID) == 1, f"Duplicate entry for {PIECE_ID} in pieces.json"


def test_essay_is_not_empty_stub():
    """Essay must not be a trivial placeholder."""
    text = _essay().strip()
    assert len(text) > 500, "essay.md appears to be a stub (too short)"


def test_html_does_not_fetch_essay_at_runtime():
    """index.html must not rely on fetch() or XMLHttpRequest to load essay content."""
    html = _html()
    assert "essay.md" not in html or "fetch" not in html, \
        "index.html must embed the essay inline, not fetch essay.md at runtime"


def test_thumbnail_400x400():
    """Thumbnail must declare 400×400 dimensions."""
    text = open(THUMBNAIL, encoding="utf-8").read()
    assert 'width="400"' in text and 'height="400"' in text, \
        "thumbnail.svg must be 400×400"
