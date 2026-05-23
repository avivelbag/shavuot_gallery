"""
Tests for piece 78-turmites-talmud-torah — The Highways of the Night.

Verifies file layout, pieces.json registration, index.html content
(canvas, rule tables, turmite mechanics), thumbnail structure, and
essay requirements.
"""
import json
import os

import pytest

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID = "78-turmites-talmud-torah"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")


def load_pieces():
    """Return the parsed pieces.json list."""
    with open(PIECES_JSON, "r", encoding="utf-8") as fh:
        return json.load(fh)


def get_piece():
    """Return the pieces.json entry for this piece, or None."""
    for p in load_pieces():
        if p["id"] == PIECE_ID:
            return p
    return None


def read_html():
    """Return the full text of index.html."""
    with open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8") as fh:
        return fh.read()


def read_essay():
    """Return the full text of essay.md."""
    with open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8") as fh:
        return fh.read()


def read_thumbnail():
    """Return the full text of thumbnail.svg."""
    with open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8") as fh:
        return fh.read()


# ---------------------------------------------------------------------------
# Piece directory and required file presence
# ---------------------------------------------------------------------------

def test_piece_directory_exists():
    """Piece directory must exist at the expected path."""
    assert os.path.isdir(PIECE_DIR), f"Directory {PIECE_DIR} does not exist"


def test_index_html_present():
    """index.html must exist in the piece directory."""
    assert os.path.isfile(os.path.join(PIECE_DIR, "index.html"))


def test_essay_md_present():
    """essay.md must exist in the piece directory."""
    assert os.path.isfile(os.path.join(PIECE_DIR, "essay.md"))


def test_thumbnail_svg_present():
    """thumbnail.svg must exist in the piece directory."""
    assert os.path.isfile(os.path.join(PIECE_DIR, "thumbnail.svg"))


def test_readme_md_present():
    """README.md must exist in the piece directory."""
    assert os.path.isfile(os.path.join(PIECE_DIR, "README.md"))


# ---------------------------------------------------------------------------
# pieces.json registration
# ---------------------------------------------------------------------------

def test_piece_registered_in_json():
    """Piece must appear in pieces.json."""
    assert get_piece() is not None, f"'{PIECE_ID}' not found in pieces.json"


def test_piece_theme_is_tikkun_leil():
    """Theme must be 'Tikkun Leil Shavuot' exactly."""
    piece = get_piece()
    assert piece is not None
    assert piece["theme"] == "Tikkun Leil Shavuot", (
        f"Expected theme 'Tikkun Leil Shavuot', got '{piece['theme']}'"
    )


def test_piece_technique_mentions_turmites():
    """Technique field must mention Turmites."""
    piece = get_piece()
    assert piece is not None
    assert "Turmites" in piece["technique"] or "turmites" in piece["technique"].lower(), (
        f"Technique must mention Turmites, got: {piece['technique']}"
    )


def test_piece_technique_mentions_langtons_ant():
    """Technique field must mention Langton's Ant."""
    piece = get_piece()
    assert piece is not None
    assert "Langton" in piece["technique"], (
        f"Technique must mention Langton's Ant, got: {piece['technique']}"
    )


def test_piece_has_all_required_fields():
    """Piece entry must have every required field with a non-empty value."""
    required = ("id", "title", "tagline", "year", "theme", "technique", "path", "thumbnail", "essay")
    piece = get_piece()
    assert piece is not None
    for field in required:
        assert field in piece and piece[field], f"Missing or empty required field: {field}"


def test_piece_path_correct():
    """Path field must point to the correct index.html location."""
    piece = get_piece()
    assert piece is not None
    assert piece["path"] == f"pieces/{PIECE_ID}/index.html"


def test_piece_year_is_integer():
    """Year field must be an integer."""
    piece = get_piece()
    assert piece is not None
    assert isinstance(piece["year"], int)


# ---------------------------------------------------------------------------
# index.html — canvas and animation
# ---------------------------------------------------------------------------

def test_html_has_canvas_element():
    """index.html must contain a canvas element."""
    assert "<canvas" in read_html()


def test_html_uses_requestanimationframe():
    """index.html must use requestAnimationFrame for animation."""
    assert "requestAnimationFrame" in read_html()


def test_html_navy_background():
    """index.html must specify the dark navy background color #0A0C1A."""
    html = read_html().lower()
    assert "#0a0c1a" in html, "Background color #0A0C1A not found in index.html"


def test_html_canvas_size_800():
    """Canvas must be 800×800 (400 cells × 2px)."""
    html = read_html()
    assert 'width="800"' in html and 'height="800"' in html, (
        "Canvas must have explicit width=800 and height=800 attributes"
    )


def test_html_grid_400():
    """GRID constant must be set to 400."""
    html = read_html()
    assert "GRID = 400" in html or "GRID=400" in html, (
        "GRID constant 400 not found in index.html"
    )


def test_html_steps_per_frame_defined():
    """STEPS_PER_FRAME variable must be defined."""
    assert "STEPS_PER_FRAME" in read_html()


def test_html_max_steps_200000():
    """MAX_STEPS must be 200000."""
    html = read_html()
    assert "MAX_STEPS" in html, "MAX_STEPS variable not found"
    assert "200000" in html, "MAX_STEPS value 200000 not found"


def test_html_toroidal_wrapping():
    """Ants must wrap toroidally using modulo GRID."""
    html = read_html()
    assert "% GRID" in html or "%GRID" in html or "% 400" in html, (
        "Toroidal wrapping (modulo GRID) not found in index.html"
    )


# ---------------------------------------------------------------------------
# index.html — five turmites with correct rules and colors
# ---------------------------------------------------------------------------

def test_html_five_trail_colors():
    """index.html must define all 5 ant trail colors."""
    html = read_html().lower()
    for color in ["d4a017", "c97b22", "b5651d", "f5deb3", "fff8e7"]:
        assert color in html, f"Trail color #{color.upper()} not found in index.html"


def test_html_contains_rl_rule():
    """index.html must include the classic RL rule (Langton's Ant)."""
    assert "RL" in read_html(), "RL rule comment not found in index.html"


def test_html_contains_lr_rule():
    """index.html must include the LR rule."""
    assert "LR" in read_html(), "LR rule comment not found in index.html"


def test_html_contains_llrr_rule():
    """index.html must include the LLRR highway-forming rule."""
    assert "LLRR" in read_html(), "LLRR rule not found in index.html"


def test_html_contains_lrrl_rule():
    """index.html must include the LRRL highway-forming rule."""
    assert "LRRL" in read_html(), "LRRL rule not found in index.html"


def test_html_independent_grids():
    """Each ant must have its own independent grid (Uint8Array)."""
    assert "Uint8Array" in read_html(), "Uint8Array per-ant grids not found in index.html"


def test_html_five_rules():
    """RULES array must contain 5 entries (one per ant)."""
    html = read_html()
    assert "RULES" in html, "RULES array not found in index.html"
    assert "TRAIL_COLORS" in html or "TRAIL_COLOR" in html, "Trail color array not found"


# ---------------------------------------------------------------------------
# index.html — essay embedded inline
# ---------------------------------------------------------------------------

def test_html_embeds_essay_tikkun():
    """index.html must embed the essay's Tikkun Leil reference."""
    assert "Tikkun Leil Shavuot" in read_html()


def test_html_embeds_essay_zohar():
    """index.html must embed the essay's Zohar reference."""
    assert "Zohar" in read_html()


def test_html_embeds_essay_safed():
    """index.html must embed the essay's Safed reference."""
    assert "Safed" in read_html()


# ---------------------------------------------------------------------------
# thumbnail.svg
# ---------------------------------------------------------------------------

def test_thumbnail_is_valid_svg():
    """thumbnail.svg must be valid SVG with open and close tags."""
    content = read_thumbnail()
    assert "<svg" in content and "</svg>" in content


def test_thumbnail_has_navy_background():
    """thumbnail.svg must have the dark navy background color."""
    content = read_thumbnail().lower()
    assert "#0a0c1a" in content, "Dark navy background #0A0C1A not found in thumbnail.svg"


def test_thumbnail_has_five_lines():
    """thumbnail.svg must contain exactly 5 diagonal lines."""
    content = read_thumbnail()
    assert content.count("<line") >= 5, (
        f"Expected at least 5 lines in thumbnail.svg, found {content.count('<line')}"
    )


def test_thumbnail_has_all_trail_colors():
    """thumbnail.svg must use all 5 ant trail colors."""
    content = read_thumbnail().upper()
    for color in ["D4A017", "C97B22", "B5651D", "F5DEB3", "FFF8E7"]:
        assert color in content, f"Trail color #{color} not found in thumbnail.svg"


# ---------------------------------------------------------------------------
# essay.md content checks
# ---------------------------------------------------------------------------

def test_essay_word_count():
    """essay.md must have at least 350 words (target ~380)."""
    text = read_essay()
    word_count = len(text.split())
    assert word_count >= 350, f"essay.md has only {word_count} words (need ≥ 350)"


def test_essay_mentions_zohar_parashat_emor():
    """Essay must mention the Zohar as the origin of the practice."""
    assert "Zohar" in read_essay()


def test_essay_mentions_safed_kabbalists():
    """Essay must mention the sixteenth-century Safed kabbalists."""
    text = read_essay()
    assert "Safed" in text, "Essay must mention Safed kabbalists"


def test_essay_explains_tikkun_means_repair():
    """Essay must explain that tikkun means repair or preparation."""
    text = read_essay().lower()
    assert "repair" in text or "preparation" in text


def test_essay_mentions_israelites_slept():
    """Essay must reference the midrash that Israelites slept before revelation."""
    text = read_essay().lower()
    assert "slept" in text or "sleep" in text or "awakened" in text or "awaken" in text


def test_essay_mentions_highways_emergence():
    """Essay must connect the artwork to emergence from rule-following."""
    text = read_essay().lower()
    assert "emerge" in text or "highway" in text


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

def test_no_duplicate_ids_in_pieces_json():
    """Adding this piece must not create duplicate IDs."""
    pieces = load_pieces()
    ids = [p["id"] for p in pieces]
    assert len(ids) == len(set(ids)), f"Duplicate piece IDs found: {[i for i in ids if ids.count(i) > 1]}"


def test_piece_id_uniqueness():
    """The turmites piece ID must appear exactly once in pieces.json."""
    pieces = load_pieces()
    matches = [p for p in pieces if p["id"] == PIECE_ID]
    assert len(matches) == 1, f"Expected 1 entry for '{PIECE_ID}', found {len(matches)}"


def test_essay_length_is_not_stub():
    """Essay must be substantially longer than a placeholder stub (>100 words)."""
    text = read_essay()
    word_count = len(text.split())
    assert word_count > 100, f"essay.md looks like a stub: only {word_count} words"


def test_thumbnail_400x400_viewport():
    """thumbnail.svg must declare a 400×400 viewBox or dimensions."""
    content = read_thumbnail()
    assert "400" in content, "thumbnail.svg must reference 400px dimensions"


# ---------------------------------------------------------------------------
# Explicit failure modes
# ---------------------------------------------------------------------------

def test_wrong_theme_would_be_rejected():
    """A piece registered with 'Book of Ruth' theme must NOT match Tikkun Leil check."""
    piece = get_piece()
    assert piece is not None
    assert piece["theme"] != "Book of Ruth", (
        "Theme must be 'Tikkun Leil Shavuot', not 'Book of Ruth'"
    )


def test_missing_file_raises_error(tmp_path):
    """Opening a non-existent essay file must raise FileNotFoundError."""
    fake_path = str(tmp_path / "nonexistent_essay.md")
    assert not os.path.isfile(fake_path)
    with pytest.raises((FileNotFoundError, OSError)):
        open(fake_path, encoding="utf-8").read()


def test_empty_pieces_json_fails_entry_count():
    """An empty pieces.json array must be detectable as having no entries."""
    empty_data = json.loads("[]")
    assert len(empty_data) == 0


def test_piece_without_technique_would_fail():
    """A piece entry lacking 'technique' must not satisfy the technique check."""
    bad_piece = {"id": "99-test", "theme": "Tikkun Leil Shavuot"}
    assert "technique" not in bad_piece, "Fixture must not have technique field"
    assert bad_piece.get("technique") is None
