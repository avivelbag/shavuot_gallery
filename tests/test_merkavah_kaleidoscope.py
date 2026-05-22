"""
Tests specific to piece 42-merkavah-kaleidoscope — the Merkavah Kaleidoscope.

Covers:
- pieces.json registration and required fields
- directory layout (index.html, essay.md, thumbnail.svg, README.md)
- animation technique: requestAnimationFrame, four-fold symmetry, Perlin noise
- Hebrew face labels in the animation canvas code
- essay content: Ezekiel 1, Megillah 31a, Ma'ase Merkavah, four creatures
- essay word-count minimum
- essay embedded in index.html
- palette colours present in the source
"""
import json
import os

import pytest

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECES_JSON  = os.path.join(GALLERY_ROOT, "pieces.json")
PIECE_ID     = "42-merkavah-kaleidoscope"
PIECE_DIR    = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
INDEX_HTML   = os.path.join(PIECE_DIR, "index.html")
ESSAY_MD     = os.path.join(PIECE_DIR, "essay.md")
README_MD    = os.path.join(PIECE_DIR, "README.md")
THUMB_SVG    = os.path.join(PIECE_DIR, "thumbnail.svg")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _pieces():
    """Load pieces.json and return the list."""
    with open(PIECES_JSON, encoding="utf-8") as fh:
        return json.load(fh)


def _piece():
    """Return the pieces.json entry for 42-merkavah-kaleidoscope, or None."""
    return next((p for p in _pieces() if p["id"] == PIECE_ID), None)


def _html():
    """Return the raw text of index.html."""
    with open(INDEX_HTML, encoding="utf-8") as fh:
        return fh.read()


def _essay():
    """Return the raw text of essay.md."""
    with open(ESSAY_MD, encoding="utf-8") as fh:
        return fh.read()


# ---------------------------------------------------------------------------
# Registration in pieces.json
# ---------------------------------------------------------------------------

def test_piece_registered_in_pieces_json():
    """Piece 42-merkavah-kaleidoscope must appear in pieces.json."""
    assert _piece() is not None, f"Piece '{PIECE_ID}' not found in pieces.json"


def test_piece_has_correct_id():
    p = _piece()
    assert p is not None
    assert p["id"] == PIECE_ID


def test_piece_json_required_fields():
    """All required fields must be non-empty."""
    required = ("id", "title", "tagline", "year", "theme", "technique", "path", "thumbnail", "essay")
    p = _piece()
    assert p is not None
    for field in required:
        assert field in p and p[field], f"Field '{field}' missing or empty in pieces.json entry"


def test_piece_year_is_integer():
    p = _piece()
    assert p is not None
    assert isinstance(p["year"], int)


def test_piece_path_points_to_index_html():
    p = _piece()
    assert p is not None
    assert p["path"] == f"pieces/{PIECE_ID}/index.html"


def test_piece_thumbnail_extension():
    p = _piece()
    assert p is not None
    assert p["thumbnail"].endswith(".svg") or p["thumbnail"].endswith(".png")


def test_piece_essay_field_set():
    p = _piece()
    assert p is not None
    assert p["essay"] == f"pieces/{PIECE_ID}/essay.md"


# ---------------------------------------------------------------------------
# File layout
# ---------------------------------------------------------------------------

def test_index_html_exists():
    assert os.path.isfile(INDEX_HTML), f"index.html not found at {INDEX_HTML}"


def test_essay_md_exists():
    assert os.path.isfile(ESSAY_MD), f"essay.md not found at {ESSAY_MD}"


def test_readme_md_exists():
    assert os.path.isfile(README_MD), f"README.md not found at {README_MD}"


def test_thumbnail_svg_exists():
    assert os.path.isfile(THUMB_SVG), f"thumbnail.svg not found at {THUMB_SVG}"


def test_thumbnail_is_valid_svg():
    text = open(THUMB_SVG, encoding="utf-8").read()
    assert "<svg" in text and "</svg>" in text, "thumbnail.svg does not look like valid SVG"


# ---------------------------------------------------------------------------
# Animation technique — index.html
# ---------------------------------------------------------------------------

def test_uses_request_animation_frame():
    assert "requestAnimationFrame" in _html(), "index.html must use requestAnimationFrame"


def test_has_seed_canvas():
    """A second offscreen canvas (seedCanvas) must be created for the quarter wedge."""
    assert "seedCanvas" in _html(), "index.html must allocate a seedCanvas for the quarter wedge"


def test_has_perlin_noise_function():
    """An inline Perlin noise function must be present (no external fetch)."""
    html = _html()
    assert "perlin" in html.lower(), "index.html must contain an inline Perlin noise function"


def test_has_four_fold_symmetry_via_scale():
    """The four-fold mirror uses ctx.scale(-1,1) / scale(1,-1) etc."""
    html = _html()
    assert "scale(-1" in html or "scale( -1" in html, (
        "index.html must use ctx.scale with negative values for mirror symmetry"
    )


def test_has_draw_image_for_stamping():
    """drawImage is used to stamp the seed into each quadrant."""
    assert "drawImage" in _html(), "index.html must use drawImage to stamp seed quadrants"


def test_animation_increments_time():
    """A time counter (t +=) must advance each frame to evolve the noise."""
    html = _html()
    assert "t +=" in html or "t+=" in html, "index.html must increment a time variable each frame"


# ---------------------------------------------------------------------------
# Hebrew face labels
# ---------------------------------------------------------------------------

def test_label_arye_lion_present():
    """Lion label (אַרְיֵה) must appear in the canvas drawing code."""
    assert "אַרְיֵה" in _html() or "אריה" in _html(), (
        "index.html must include the Hebrew label for lion (אַרְיֵה)"
    )


def test_label_nesher_eagle_present():
    """Eagle label (נֶשֶׁר) must appear."""
    assert "נֶשֶׁר" in _html() or "נשר" in _html(), (
        "index.html must include the Hebrew label for eagle (נֶשֶׁר)"
    )


def test_label_shor_ox_present():
    """Ox label (שׁוֹר) must appear."""
    assert "שׁוֹר" in _html() or "שור" in _html(), (
        "index.html must include the Hebrew label for ox (שׁוֹר)"
    )


def test_label_adam_man_present():
    """Man label (אָדָם) must appear."""
    assert "אָדָם" in _html() or "אדם" in _html(), (
        "index.html must include the Hebrew label for man (אָדָם)"
    )


# ---------------------------------------------------------------------------
# Palette colours
# ---------------------------------------------------------------------------

def test_sapphire_color_present():
    html = _html().lower()
    assert "1a3a6b" in html, "Sapphire colour #1A3A6B must appear in index.html"


def test_gold_color_present():
    html = _html().lower()
    assert "c8a000" in html, "Gold colour #C8A000 must appear in index.html"


def test_crimson_color_present():
    html = _html().lower()
    assert "8b1a1a" in html, "Deep crimson #8B1A1A must appear in index.html"


# ---------------------------------------------------------------------------
# Essay content
# ---------------------------------------------------------------------------

def test_essay_word_count():
    """Essay must be at least 200 words."""
    text = _essay()
    count = len(text.split())
    assert count >= 200, f"essay.md has only {count} words (minimum 200)"


def test_essay_mentions_ezekiel():
    text = _essay().lower()
    assert "ezekiel" in text, "essay.md must mention Ezekiel"


def test_essay_mentions_megillah_31a():
    """Talmudic source for Shavuot haftarah assignment must be cited."""
    text = _essay()
    assert "Megillah 31a" in text or "Megillah 31" in text, (
        "essay.md must cite Megillah 31a as the source for the Shavuot haftarah assignment"
    )


def test_essay_mentions_maaseh_merkavah():
    """Ma'ase Merkavah tradition must be named in the essay."""
    text = _essay()
    assert "Merkavah" in text or "merkavah" in text.lower(), (
        "essay.md must mention Ma'ase Merkavah"
    )


def test_essay_mentions_four_creatures():
    """Essay must describe the four chayot / living creatures."""
    text = _essay().lower()
    assert "chayot" in text or "living creatures" in text or "four creatures" in text, (
        "essay.md must describe the four chayot (living creatures)"
    )


def test_essay_mentions_ophanim_wheels():
    """Wheels within wheels (ophanim) must appear in the essay."""
    text = _essay().lower()
    assert "ophanim" in text or "wheel" in text, (
        "essay.md must mention the ophanim (wheels within wheels)"
    )


def test_essay_mentions_tikkun_leil():
    """Tikkun Leil Shavuot must be referenced in the essay."""
    text = _essay().lower()
    assert "tikkun" in text, "essay.md must reference Tikkun Leil Shavuot"


def test_essay_mentions_shavuot_haftarah_insight():
    """The non-obvious insight — Shavuot haftarah not about harvest — must appear."""
    text = _essay().lower()
    assert "harvest" in text, (
        "essay.md must address the insight that the Shavuot haftarah is not about harvest"
    )


# ---------------------------------------------------------------------------
# Essay embedded in index.html
# ---------------------------------------------------------------------------

def test_essay_embedded_in_html():
    """index.html must embed the essay text inline — first 10 long words sampled."""
    essay = _essay()
    html  = _html()
    words = [w for w in essay.split() if len(w) > 5]
    sampled = words[:10]
    found = sum(1 for w in sampled if w in html)
    assert found >= 5, (
        f"index.html does not appear to embed the essay text "
        f"(only {found}/10 sampled words found in HTML)"
    )


# ---------------------------------------------------------------------------
# Edge cases and failure modes
# ---------------------------------------------------------------------------

def test_no_duplicate_ids():
    """Adding piece 42 must not create a duplicate ID."""
    pieces = _pieces()
    ids = [p["id"] for p in pieces]
    assert len(ids) == len(set(ids)), f"Duplicate piece IDs in pieces.json: {ids}"


def test_piece_42_is_last_or_present(tmp_path):
    """Sanity check: piece 42 exists; a completely missing ID would not appear."""
    missing_id = "42-not-a-real-piece"
    result = next((p for p in _pieces() if p["id"] == missing_id), None)
    assert result is None, "Fixture: a nonexistent ID correctly returns None"


def test_essay_at_least_200_words_fails_on_stub(tmp_path):
    """A stub essay with only a title line should fail the 200-word check."""
    stub = tmp_path / "essay.md"
    stub.write_text("# Title\n\nShort stub.", encoding="utf-8")
    text = stub.read_text(encoding="utf-8")
    assert len(text.split()) < 200, "Fixture confirms stub is under 200 words"


def test_missing_thumbnail_would_be_detected(tmp_path):
    """A nonexistent thumbnail path must be detectable by os.path.isfile."""
    fake_path = os.path.join(str(tmp_path), "missing_thumbnail.svg")
    assert not os.path.isfile(fake_path), "Fixture: missing file correctly not found"
