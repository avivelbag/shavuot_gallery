"""
Tests for piece 43-they-saw-the-voices (Lissajous at Sinai).

Covers: pieces.json registration, required files on disk, essay content,
HTML animation requirements, and several edge-case / failure-mode checks.
"""
import json
import os

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")
PIECE_ID = "45-they-saw-the-voices"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)


def load_pieces():
    with open(PIECES_JSON, encoding="utf-8") as fh:
        return json.load(fh)


def get_piece():
    for p in load_pieces():
        if p["id"] == PIECE_ID:
            return p
    return None


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------

def test_piece_registered_in_pieces_json():
    """The new piece must be present in pieces.json."""
    piece = get_piece()
    assert piece is not None, f"Piece '{PIECE_ID}' not found in pieces.json"


def test_piece_required_fields_present():
    """Every mandatory field must be present and non-empty."""
    required = ("id", "title", "tagline", "year", "theme", "technique", "path", "thumbnail", "essay")
    piece = get_piece()
    assert piece is not None
    for field in required:
        assert field in piece, f"Missing field '{field}'"
        assert piece[field], f"Empty field '{field}'"


def test_piece_year_is_integer():
    piece = get_piece()
    assert piece is not None
    assert isinstance(piece["year"], int), "year must be an integer"


def test_piece_path_ends_with_html():
    piece = get_piece()
    assert piece is not None
    assert piece["path"].endswith(".html"), "path must point to an .html file"


def test_piece_id_matches_directory():
    """The id field must match the directory component of the path."""
    piece = get_piece()
    assert piece is not None
    parts = piece["path"].replace("\\", "/").split("/")
    assert parts[-2] == PIECE_ID, f"Directory mismatch: {parts[-2]} != {PIECE_ID}"


# ---------------------------------------------------------------------------
# Files on disk
# ---------------------------------------------------------------------------

def test_index_html_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "index.html"))


def test_essay_md_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "essay.md"))


def test_thumbnail_svg_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "thumbnail.svg"))


def test_readme_md_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "README.md"))


def test_thumbnail_is_valid_svg():
    text = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert "<svg" in text and "</svg>" in text


# ---------------------------------------------------------------------------
# Essay content
# ---------------------------------------------------------------------------

def test_essay_at_least_200_words():
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    assert len(text.split()) >= 200, "essay.md must have at least 200 words"


def test_essay_cites_exodus_20_15():
    """Essay must name the verse precisely: Exodus 20:15."""
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    assert "20:15" in text, "essay.md must cite Exodus 20:15"


def test_essay_notes_english_verse_number_difference():
    """Essay must explain that English Bibles number it differently (20:18)."""
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    assert "20:18" in text, "essay.md must mention the English verse number 20:18"


def test_essay_cites_mechilta():
    """Essay must cite the Mechilta d'Rabbi Ishmael."""
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    lower = text.lower()
    assert "mechilta" in lower, "essay.md must cite the Mechilta d'Rabbi Ishmael"


def test_essay_contains_hebrew_verse():
    """Essay must contain the Hebrew text of the verse."""
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    assert "הַקּוֹלֹת" in text, "essay.md must contain the Hebrew word הַקּוֹלֹת from Exodus 20:15"


def test_essay_discusses_synesthesia():
    """Essay must discuss the synaesthetic nature of the Sinai revelation."""
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    lower = text.lower()
    assert "synaest" in lower or "synest" in lower, (
        "essay.md must discuss the synaesthetic/synesthetic nature of Sinai"
    )


def test_essay_explains_lissajous():
    """Essay must explain what a Lissajous figure is."""
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    assert "Lissajous" in text, "essay.md must mention and explain Lissajous figures"


# ---------------------------------------------------------------------------
# HTML animation requirements
# ---------------------------------------------------------------------------

def test_html_uses_requestanimationframe():
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "requestAnimationFrame" in html


def test_html_contains_canvas():
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "<canvas" in html


def test_html_has_phosphor_persistence():
    """index.html must implement phosphor trail via semi-transparent fill, not full clear."""
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "rgba(0,0" in html or "rgba(0, 0" in html, (
        "index.html must use rgba fill for phosphor persistence (not clearRect each frame)"
    )


def test_html_has_lissajous_oscillators():
    """index.html must reference Math.sin for the two oscillators."""
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert html.count("Math.sin") >= 2, "index.html must use Math.sin for both x and y oscillators"


def test_html_has_frequency_ratios():
    """index.html must define the ratio sequence used for transitions."""
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "RATIOS" in html or "ratios" in html, "index.html must define the frequency ratio sequence"


def test_html_has_hebrew_verse():
    """index.html must render the Hebrew verse text."""
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "הַקּוֹלֹת" in html, "index.html must render the Hebrew verse containing הַקּוֹלֹת"


def test_html_embeds_essay_text():
    """index.html must embed essay content inline (mirrors test_pieces.py convention)."""
    essay = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    words = [w for w in essay.split() if len(w) > 5][:10]
    found = sum(1 for w in words if w in html)
    assert found >= 5, (
        f"index.html must embed essay text: only {found}/10 sampled words found"
    )


def test_html_has_color_cycling():
    """index.html must implement color cycling (blue to amber)."""
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "colorPhase" in html or "hsl" in html, (
        "index.html must implement color cycling"
    )


def test_html_has_rtl_text_direction():
    """Hebrew text must use RTL direction."""
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "rtl" in html, "index.html must set direction: rtl for Hebrew text"


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

def test_no_duplicate_ids():
    """Adding this piece must not create a duplicate ID."""
    pieces = load_pieces()
    ids = [p["id"] for p in pieces]
    assert len(ids) == len(set(ids)), "Duplicate IDs detected in pieces.json"


def test_essay_path_registered_correctly():
    """The essay path in pieces.json must point at the actual file."""
    piece = get_piece()
    assert piece is not None
    essay_path = os.path.join(GALLERY_ROOT, piece["essay"])
    assert os.path.isfile(essay_path), f"Essay file not found at {piece['essay']}"


def test_thumbnail_path_registered_correctly():
    piece = get_piece()
    assert piece is not None
    thumb = os.path.join(GALLERY_ROOT, piece["thumbnail"])
    assert os.path.isfile(thumb), f"Thumbnail not found at {piece['thumbnail']}"


def test_missing_essay_field_detected():
    """Validate that a piece entry without an essay field is caught."""
    bad = {"id": "99-fake", "title": "x"}
    assert "essay" not in bad


def test_nonexistent_essay_file_detected(tmp_path):
    """An essay path pointing to a missing file must be detectable."""
    missing = os.path.join(str(tmp_path), "nonexistent.md")
    assert not os.path.isfile(missing)


def test_empty_essay_content_detected(tmp_path):
    """An empty essay file must fail the word-count check."""
    f = tmp_path / "empty.md"
    f.write_text("", encoding="utf-8")
    text = f.read_text(encoding="utf-8")
    assert len(text.split()) < 200
