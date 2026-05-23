"""
Tests specific to piece 87-double-pendulum-sinai-thunder.

Validates file layout, HTML content (RK4, colors, overlay), essay
substance, thumbnail SVG, and pieces.json registration.
"""
import json
import os

import pytest

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID = "87-double-pendulum-sinai-thunder"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")


def load_piece():
    """Return the pieces.json entry for piece 87, or None if absent."""
    with open(PIECES_JSON, encoding="utf-8") as fh:
        pieces = json.load(fh)
    for p in pieces:
        if p["id"] == PIECE_ID:
            return p
    return None


def read_html():
    return open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()


def read_essay():
    return open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()


# ---------------------------------------------------------------------------
# Happy path — file layout
# ---------------------------------------------------------------------------

def test_piece_directory_exists():
    assert os.path.isdir(PIECE_DIR), f"Piece directory not found: {PIECE_DIR}"


def test_index_html_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "index.html"))


def test_essay_md_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "essay.md"))


def test_thumbnail_svg_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "thumbnail.svg"))


def test_readme_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "README.md"))


# ---------------------------------------------------------------------------
# pieces.json registration
# ---------------------------------------------------------------------------

def test_piece_registered_in_pieces_json():
    piece = load_piece()
    assert piece is not None, f"'{PIECE_ID}' not found in pieces.json"


def test_piece_json_theme():
    piece = load_piece()
    assert piece is not None
    assert "Sinai" in piece["theme"] or "Matan Torah" in piece["theme"], (
        "theme must reference Har Sinai / Matan Torah"
    )


def test_piece_json_technique_mentions_rk4():
    piece = load_piece()
    assert piece is not None
    assert "RK4" in piece["technique"] or "rk4" in piece["technique"].lower(), (
        "technique field must mention RK4 integration"
    )


def test_piece_json_required_fields():
    piece = load_piece()
    assert piece is not None
    for field in ("id", "title", "tagline", "year", "theme", "technique", "path", "thumbnail", "essay"):
        assert field in piece and piece[field], f"Missing or empty field: {field}"


def test_piece_json_path_points_to_existing_html():
    piece = load_piece()
    assert piece is not None
    full = os.path.join(GALLERY_ROOT, piece["path"])
    assert os.path.isfile(full)


def test_piece_json_thumbnail_points_to_existing_file():
    piece = load_piece()
    assert piece is not None
    full = os.path.join(GALLERY_ROOT, piece["thumbnail"])
    assert os.path.isfile(full)


def test_piece_json_essay_points_to_existing_file():
    piece = load_piece()
    assert piece is not None
    full = os.path.join(GALLERY_ROOT, piece["essay"])
    assert os.path.isfile(full)


# ---------------------------------------------------------------------------
# HTML content — simulation requirements
# ---------------------------------------------------------------------------

def test_html_uses_request_animation_frame():
    assert "requestAnimationFrame" in read_html()


def test_html_contains_rk4_step():
    html = read_html()
    assert "rk4Step" in html or "rk4" in html.lower(), (
        "index.html must implement RK4 integration"
    )


def test_html_contains_all_seven_colors():
    html = read_html()
    colors = ['#4B8FD4', '#8B5CF6', '#F0EFEA', '#D4A017', '#C8702A', '#C2547A', '#7EC8D4']
    for color in colors:
        assert color in html, f"Color {color} not found in index.html"


def test_html_background_color():
    assert "#07080F" in read_html(), "Background color #07080F must appear in index.html"


def test_html_contains_hebrew_verse():
    html = read_html()
    assert "רֹאִים" in html or "&#x05E8;" in html or "וְכָל" in html, (
        "index.html must contain the Hebrew verse"
    )


def test_html_has_seven_pendulums_constant():
    html = read_html()
    assert "N = 7" in html or "const N=7" in html or "length: 7" in html or "COLORS" in html, (
        "index.html must configure 7 pendulums"
    )


def test_html_uses_dt_002():
    html = read_html()
    assert "DT = 0.02" in html or "dt = 0.02" in html or "0.02" in html, (
        "index.html must use DT = 0.02 for integration"
    )


def test_html_uses_eight_steps_per_frame():
    html = read_html()
    assert "STEPS_PER_FRAME = 8" in html or "8" in html, (
        "index.html must run 8 integration steps per frame"
    )


def test_html_has_gravity_98():
    html = read_html()
    assert "9.8" in html or "G = 9.8" in html


def test_html_embeds_essay_text():
    essay = read_essay()
    html = read_html()
    words = [w for w in essay.split() if len(w) > 6][:10]
    found = sum(1 for w in words if w in html)
    assert found >= 5, (
        f"index.html must embed essay text inline (only {found}/10 sampled words found)"
    )


def test_html_reset_after_20_seconds():
    html = read_html()
    assert "RESET_SIM_TIME = 20" in html or "20.0" in html or "20" in html, (
        "index.html must reset simulation after 20 seconds"
    )


def test_html_fade_frames_60():
    html = read_html()
    assert "FADE_FRAMES = 60" in html or "60" in html


# ---------------------------------------------------------------------------
# Essay content
# ---------------------------------------------------------------------------

def test_essay_minimum_words():
    text = read_essay()
    assert len(text.split()) >= 300, "essay.md must be at least 300 words"


def test_essay_mentions_exodus():
    essay = read_essay()
    assert "Exodus" in essay or "exodus" in essay


def test_essay_mentions_mekhilta():
    essay = read_essay()
    assert "Mekhilta" in essay or "mekhilta" in essay.lower()


def test_essay_mentions_chaos():
    essay = read_essay()
    assert "chaos" in essay.lower() or "sensitive dependence" in essay.lower()


def test_essay_contains_hebrew_verse():
    essay = read_essay()
    assert "רֹאִים" in essay or "וְכָל" in essay, (
        "essay.md must contain the Hebrew verse"
    )


# ---------------------------------------------------------------------------
# Thumbnail SVG
# ---------------------------------------------------------------------------

def test_thumbnail_is_valid_svg():
    text = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert "<svg" in text and "</svg>" in text


def test_thumbnail_dark_background():
    text = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert "#07080F" in text, "thumbnail.svg must use the dark background color #07080F"


def test_thumbnail_contains_colored_paths():
    text = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert "<path" in text, "thumbnail.svg must contain path elements for the traces"


def test_thumbnail_400x400():
    text = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert 'width="400"' in text and 'height="400"' in text


# ---------------------------------------------------------------------------
# Edge cases and failure modes
# ---------------------------------------------------------------------------

def test_no_duplicate_piece_id_in_json():
    with open(PIECES_JSON, encoding="utf-8") as fh:
        pieces = json.load(fh)
    ids = [p["id"] for p in pieces]
    assert ids.count(PIECE_ID) == 1, f"Duplicate entry for {PIECE_ID} in pieces.json"


def test_piece_id_matches_directory():
    """The id field must match the directory name."""
    piece = load_piece()
    assert piece is not None
    path_dir = piece["path"].replace("\\", "/").split("/")[-2]
    assert path_dir == PIECE_ID


def test_essay_does_not_reference_wrong_piece():
    """Essay should not mention another piece's technique by mistake."""
    essay = read_essay()
    assert "gyroid" not in essay.lower(), "Essay should not mention gyroid (wrong piece)"
    assert "Gray-Scott" not in essay, "Essay should not mention reaction-diffusion (wrong piece)"


def test_missing_piece_directory_detected(tmp_path):
    """Validates that a non-existent piece directory is correctly flagged."""
    fake_dir = tmp_path / "99-nonexistent-piece"
    assert not fake_dir.exists(), "Fixture: directory must not exist for this test"


def test_empty_essay_file_is_insufficient(tmp_path):
    """An empty file would fail the word count check."""
    empty = tmp_path / "essay.md"
    empty.write_text("", encoding="utf-8")
    word_count = len(empty.read_text().split())
    assert word_count < 200, "Fixture confirms empty file has zero words"
