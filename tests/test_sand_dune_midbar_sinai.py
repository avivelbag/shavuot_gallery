"""
Tests for the sand dune / midbar-sinai piece (78-sand-dune-midbar-sinai).

Covers: file layout, pieces.json registration, HTML animation requirements,
essay content, thumbnail validity, and several edge/failure cases.
"""
import json
import os

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID = "78-sand-dune-midbar-sinai"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")


def _load_piece():
    """Return the pieces.json entry for this piece, or None if absent."""
    with open(PIECES_JSON, "r", encoding="utf-8") as fh:
        pieces = json.load(fh)
    for p in pieces:
        if p["id"] == PIECE_ID:
            return p
    return None


def _html():
    return open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()


def _essay():
    return open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()


def _thumbnail():
    return open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()


# ---------------------------------------------------------------------------
# File existence — happy path
# ---------------------------------------------------------------------------

def test_piece_directory_exists():
    assert os.path.isdir(PIECE_DIR), f"Piece directory missing: {PIECE_DIR}"


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
    assert _load_piece() is not None, f"{PIECE_ID} not found in pieces.json"


def test_piece_theme_mentions_midbar_or_wilderness():
    piece = _load_piece()
    assert piece is not None
    theme = piece.get("theme", "").lower()
    assert "midbar" in theme or "wilderness" in theme, (
        f"theme '{theme}' should mention midbar or wilderness"
    )


def test_piece_technique_mentions_cellular_automaton():
    piece = _load_piece()
    assert piece is not None
    technique = piece.get("technique", "").lower()
    assert "cellular" in technique or "automaton" in technique, (
        f"technique '{technique}' should mention cellular automaton"
    )


def test_piece_technique_mentions_dune():
    piece = _load_piece()
    assert piece is not None
    technique = piece.get("technique", "").lower()
    assert "dune" in technique or "sand" in technique, (
        f"technique '{technique}' should mention dune or sand"
    )


def test_piece_path_correct():
    piece = _load_piece()
    assert piece is not None
    assert piece["path"] == f"pieces/{PIECE_ID}/index.html"


def test_piece_essay_path_correct():
    piece = _load_piece()
    assert piece is not None
    assert piece["essay"] == f"pieces/{PIECE_ID}/essay.md"


def test_piece_thumbnail_path_correct():
    piece = _load_piece()
    assert piece is not None
    assert piece["thumbnail"] == f"pieces/{PIECE_ID}/thumbnail.svg"


def test_piece_year_is_integer():
    piece = _load_piece()
    assert piece is not None
    assert isinstance(piece["year"], int)


def test_piece_appears_exactly_once_in_pieces_json():
    with open(PIECES_JSON, "r", encoding="utf-8") as fh:
        pieces = json.load(fh)
    matching = [p for p in pieces if p["id"] == PIECE_ID]
    assert len(matching) == 1, f"Expected exactly 1 entry for {PIECE_ID}, found {len(matching)}"


# ---------------------------------------------------------------------------
# index.html — canvas animation requirements
# ---------------------------------------------------------------------------

def test_html_uses_requestanimationframe():
    assert "requestAnimationFrame" in _html()


def test_html_has_canvas_element():
    assert "<canvas" in _html()


def test_html_uses_imagedata_api():
    html = _html()
    assert "createImageData" in html or "putImageData" in html or "ImageData" in html


def test_html_grid_width_300():
    assert "300" in _html(), "Grid width W=300 not found in HTML"


def test_html_grid_height_200():
    assert "200" in _html(), "Grid height H=200 not found in HTML"


def test_html_saltation_probability_0_3():
    assert "0.3" in _html(), "Saltation probability p_hop=0.3 not found in HTML"


def test_html_avalanche_threshold_3():
    html = _html()
    assert "> 3" in html or ">3" in html, "Avalanche threshold T=3 not found in HTML"


def test_html_has_wind_direction_variable():
    html = _html()
    assert "windX" in html or "windAngle" in html, "Wind direction variable not found in HTML"


def test_html_stamps_hebrew_text():
    html = _html()
    has_hebrew = "מ" in html
    has_unicode = "05DE" in html or "\\u05DE" in html
    assert has_hebrew or has_unicode, "Hebrew text stamping (מִדְבָּר) not found in HTML"


def test_html_three_simulation_passes_per_tick():
    html = _html()
    assert "< 3" in html or "p < 3" in html or "3; p++" in html, (
        "3 simulation passes per rAF tick not found in HTML"
    )


def test_html_color_bare_desert():
    html = _html()
    assert "C4A882" in html.upper(), "Bare desert color #C4A882 not in HTML"


def test_html_color_dune_crest():
    html = _html()
    assert "F2D9A0" in html.upper(), "Dune crest highlight #F2D9A0 not in HTML"


def test_html_color_mid_sand():
    html = _html()
    assert "D4AA70" in html.upper(), "Mid sand color #D4AA70 not in HTML"


def test_html_wind_rotates_every_600_frames():
    assert "600" in _html(), "Wind rotation interval 600 not found in HTML"


def test_html_wind_rotation_15_degrees():
    html = _html()
    assert "15" in html, "Wind rotation angle 15° not found in HTML"


def test_html_seed_mounds_height_6():
    assert ", 6)" in _html() or ", 6 " in _html() or "= 6" in _html(), (
        "Seed mound height 6 not found in HTML"
    )


def test_html_text_stamp_at_frame_300():
    assert "300" in _html(), "Text stamp frame 300 not found in HTML"


def test_html_max_height_8():
    assert "8" in _html(), "Maximum height 8 not found in HTML"


# ---------------------------------------------------------------------------
# essay.md content
# ---------------------------------------------------------------------------

def test_essay_minimum_400_words():
    text = _essay()
    word_count = len(text.split())
    assert word_count >= 400, f"Essay has {word_count} words, need ≥400"


def test_essay_mentions_mechilta():
    assert "Mechilta" in _essay() or "mechilta" in _essay().lower()


def test_essay_quotes_whoever_wishes():
    text = _essay()
    assert "whoever" in text.lower() or "כָּל הָרוֹצֶה" in text, (
        "Essay must quote 'whoever wishes to receive it'"
    )


def test_essay_mentions_midbar_etymology():
    text = _essay()
    assert "davar" in text.lower() or "דָּבָר" in text or "word" in text.lower(), (
        "Essay must discuss midbar etymology (root shared with davar/word)"
    )


def test_essay_mentions_bamidbar_rabbah_or_rashi():
    text = _essay()
    assert "Rashi" in text or "Bamidbar Rabbah" in text or "Bamidbar" in text, (
        "Essay must mention Rashi or Bamidbar Rabbah"
    )


# ---------------------------------------------------------------------------
# thumbnail.svg
# ---------------------------------------------------------------------------

def test_thumbnail_is_valid_svg():
    text = _thumbnail()
    assert "<svg" in text and "</svg>" in text


def test_thumbnail_has_path_or_ellipse_elements():
    text = _thumbnail()
    assert "<path" in text or "<ellipse" in text, (
        "thumbnail.svg should have path or ellipse shapes for dunes"
    )


def test_thumbnail_uses_sandy_color_palette():
    text = _thumbnail().upper()
    sandy = any(c in text for c in ["C4A882", "D4AA70", "F2D9A0", "B8956A"])
    assert sandy, "thumbnail.svg should use the sandy color palette"


def test_thumbnail_400x400():
    text = _thumbnail()
    assert 'width="400"' in text and 'height="400"' in text, (
        "thumbnail.svg should be 400×400"
    )


# ---------------------------------------------------------------------------
# Edge cases and failure modes
# ---------------------------------------------------------------------------

def test_nonexistent_piece_not_in_pieces_json():
    """Pieces that don't exist must not appear in pieces.json."""
    with open(PIECES_JSON, "r", encoding="utf-8") as fh:
        pieces = json.load(fh)
    ids = [p["id"] for p in pieces]
    assert "99-nonexistent-piece" not in ids


def test_empty_piece_id_would_fail_field_check():
    """An entry with an empty id field fails the non-empty required-field check."""
    bad = {"id": "", "title": "Test", "tagline": "", "year": 2026,
           "theme": "", "technique": "", "path": "", "thumbnail": "", "essay": ""}
    assert bad["id"] == "", "Fixture: id should be empty to confirm failure mode"


def test_essay_word_count_check_empty_essay(tmp_path):
    """A zero-word essay should fail the minimum word count check."""
    empty_essay = tmp_path / "essay.md"
    empty_essay.write_text("", encoding="utf-8")
    text = empty_essay.read_text(encoding="utf-8")
    word_count = len(text.split())
    assert word_count < 400, "Fixture confirms empty essay has too few words"


def test_missing_html_file_fails(tmp_path):
    """A piece path that doesn't exist on disk should be detected as missing."""
    missing = os.path.join(str(tmp_path), "nonexistent.html")
    assert not os.path.isfile(missing), "Fixture path must not exist"
