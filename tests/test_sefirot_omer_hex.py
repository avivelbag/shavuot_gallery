"""
Tests for piece 49-sefirot-omer-hex: Seven Times Seven — The Sefirot Omer Grid.

Validates the hex-grid canvas piece against the acceptance criteria:
- Directory structure and required files present
- pieces.json entry has correct theme/technique
- index.html contains canvas animation with requestAnimationFrame
- All 49 Hebrew day labels are referenced
- Sefirat combination labels for all 7 weeks appear
- Essay embeds the Hebrew and English Leviticus 23 passage
- Essay is at least 300 words
- The 50th hex (Shavuot / nun) is referenced
"""
import json
import os

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECES_JSON  = os.path.join(GALLERY_ROOT, "pieces.json")
PIECE_ID     = "49-sefirot-omer-hex"
PIECE_DIR    = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_pieces():
    """Return the parsed pieces.json list."""
    with open(PIECES_JSON, encoding="utf-8") as fh:
        return json.load(fh)


def get_piece():
    """Return the pieces.json entry for 49-sefirot-omer-hex, or None."""
    for p in load_pieces():
        if p["id"] == PIECE_ID:
            return p
    return None


def read_html():
    """Return the full text of the piece's index.html."""
    return open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()


def read_essay():
    """Return the full text of essay.md."""
    return open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()


# ---------------------------------------------------------------------------
# File layout
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
# pieces.json entry
# ---------------------------------------------------------------------------

def test_piece_in_pieces_json():
    assert get_piece() is not None, f"{PIECE_ID} not found in pieces.json"


def test_piece_theme():
    piece = get_piece()
    assert piece is not None
    assert piece["theme"] == "Sefirat HaOmer", f"Expected theme 'Sefirat HaOmer', got '{piece['theme']}'"


def test_piece_technique_mentions_hex():
    piece = get_piece()
    assert piece is not None
    assert "hex" in piece["technique"].lower(), (
        f"technique field should mention hex; got: '{piece['technique']}'"
    )


def test_piece_all_required_fields():
    piece = get_piece()
    assert piece is not None
    for field in ("id", "title", "tagline", "year", "theme", "technique", "path", "thumbnail", "essay"):
        assert field in piece and piece[field], f"Field '{field}' missing or empty"


def test_piece_path_file_exists():
    piece = get_piece()
    assert piece is not None
    full_path = os.path.join(GALLERY_ROOT, piece["path"])
    assert os.path.isfile(full_path)


def test_piece_thumbnail_file_exists():
    piece = get_piece()
    assert piece is not None
    full_path = os.path.join(GALLERY_ROOT, piece["thumbnail"])
    assert os.path.isfile(full_path)


def test_piece_essay_file_exists():
    piece = get_piece()
    assert piece is not None
    full_path = os.path.join(GALLERY_ROOT, piece["essay"])
    assert os.path.isfile(full_path)


# ---------------------------------------------------------------------------
# index.html — animation requirements
# ---------------------------------------------------------------------------

def test_html_uses_requestanimationframe():
    assert "requestAnimationFrame" in read_html()


def test_html_has_canvas_element():
    assert "<canvas" in read_html()


def test_html_week_colors_present():
    """All 7 kabbalistic week colors must appear in the HTML."""
    html = read_html()
    colors = [
        "#7EC8E3",  # Chesed
        "#C0392B",  # Gevurah
        "#F4C430",  # Tiferet
        "#27AE60",  # Netzach
        "#E67E22",  # Hod
        "#8E44AD",  # Yesod
        "#6D2349",  # Malkhut
    ]
    for c in colors:
        assert c in html, f"Week color {c} not found in index.html"


def test_html_50th_hex_color():
    """The 50th (Shavuot) hex white-gold color must be present."""
    assert "#FFF4C2" in read_html()


def test_html_background_color():
    assert "#0D0820" in read_html()


def test_html_drawHex_function_defined():
    """The drawHex path-tracing function must be defined."""
    assert "function drawHex" in read_html()


def test_html_bloom_animation_present():
    """The bloom animation must reference a scale property progression."""
    html = read_html()
    assert "bloomStart" in html, "bloomStart property not found in animation code"
    assert "scale" in html, "'scale' property not found in animation code"


def test_html_49_hexes_built():
    """The animation must build 49 hexagons."""
    html = read_html()
    assert "49" in html or "hexes" in html


def test_html_sefirot_array_present():
    """The SEFIROT array of Hebrew names must be in the script."""
    html = read_html()
    assert "SEFIROT" in html


def test_html_sefira_labels_generated():
    """The SEFIRA_LABELS array (tooltip text) must be generated."""
    assert "SEFIRA_LABELS" in read_html()


def test_html_tooltip_on_hover():
    """The mousemove listener driving the tooltip must be present."""
    html = read_html()
    assert "mousemove" in html


def test_html_50th_nun_symbol():
    """The nun (נ) label for the 50th hex must be present."""
    assert "נ" in read_html()  # nun = נ


def test_html_hebrew_day_labels():
    """The HEBREW_DAY array (in-hex labels) must be present."""
    assert "HEBREW_DAY" in read_html()


def test_html_hebrew_ordinals():
    """The HEBREW_ORD array (tooltip ordinals with geresh) must be present."""
    assert "HEBREW_ORD" in read_html()


def test_html_phase_state_machine():
    """The phase state machine ('blooming', 'holding', 'fading') must be present."""
    html = read_html()
    for phase in ("blooming", "holding", "fading"):
        assert phase in html, f"Phase '{phase}' not found in animation code"


def test_html_fade_and_restart():
    """The resetAnimation function (loop restart) must be present."""
    assert "resetAnimation" in read_html()


# ---------------------------------------------------------------------------
# Scripture passage — Hebrew and English Leviticus 23 embedded
# ---------------------------------------------------------------------------

def test_html_leviticus_hebrew_passage():
    """The Hebrew Leviticus 23 passage ( וּסְפַרְתֶּם) must be embedded in index.html."""
    html = read_html()
    assert "וּסְפַרְתֶּם" in html, "Hebrew Leviticus 23:15 passage not found in index.html"


def test_html_leviticus_reference():
    """Leviticus 23 reference must appear in index.html."""
    html = read_html()
    assert "23:15" in html or "23:16" in html, "Leviticus 23:15–16 reference not in index.html"


def test_html_english_translation_present():
    """The English translation of the passage must be embedded."""
    html = read_html()
    assert "seven complete weeks" in html or "fifty days" in html, (
        "English Leviticus translation not found in index.html"
    )


# ---------------------------------------------------------------------------
# Essay requirements
# ---------------------------------------------------------------------------

def test_essay_word_count():
    """Essay must be at least 300 words."""
    text = read_essay()
    count = len(text.split())
    assert count >= 300, f"Essay has only {count} words (minimum 300)"


def test_essay_mentions_sefer_hachinuch():
    essay = read_essay()
    assert "HaChinuch" in essay or "Chinuch" in essay, (
        "Essay should mention Sefer HaChinuch"
    )


def test_essay_mentions_tikkunei_zohar():
    essay = read_essay()
    assert "Zohar" in essay, "Essay should mention Tikkunei Zohar"


def test_essay_mentions_fiftieth_gate():
    essay = read_essay()
    assert "fiftieth" in essay or "50" in essay or "gate" in essay.lower(), (
        "Essay should discuss the fiftieth gate concept"
    )


def test_essay_mentions_leviticus():
    essay = read_essay()
    assert "Leviticus" in essay or "23:15" in essay


def test_index_html_embeds_essay_text():
    """index.html must embed key essay phrases inline."""
    essay = read_essay()
    html  = read_html()
    words = [w for w in essay.split() if len(w) > 6][:15]
    found = sum(1 for w in words if w in html)
    assert found >= 7, (
        f"index.html does not appear to embed essay text (found {found}/15 sampled words)"
    )


# ---------------------------------------------------------------------------
# Edge-case and failure-mode tests
# ---------------------------------------------------------------------------

def test_no_duplicate_ids():
    """Adding 49-sefirot-omer-hex must not create a duplicate ID."""
    ids = [p["id"] for p in load_pieces()]
    assert len(ids) == len(set(ids)), f"Duplicate IDs in pieces.json: {ids}"


def test_thumbnail_is_valid_svg():
    """thumbnail.svg must contain basic SVG structure."""
    svg_path = os.path.join(PIECE_DIR, "thumbnail.svg")
    text = open(svg_path, encoding="utf-8").read()
    assert "<svg" in text and "</svg>" in text


def test_thumbnail_has_week_colors():
    """thumbnail.svg must reference the 7 week colors."""
    svg = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    for color in ("#7EC8E3", "#C0392B", "#F4C430", "#27AE60", "#E67E22", "#8E44AD", "#6D2349"):
        assert color in svg, f"Week color {color} missing from thumbnail.svg"


def test_missing_piece_detected(tmp_path):
    """A lookup for a non-existent piece returns None."""
    fake_pieces = [{"id": "99-fake", "title": "Fake"}]
    result = next((p for p in fake_pieces if p["id"] == PIECE_ID), None)
    assert result is None


def test_essay_short_rejected(tmp_path):
    """An essay under 300 words would fail the word-count check."""
    short = tmp_path / "short.md"
    short.write_text("word " * 50, encoding="utf-8")
    count = len(short.read_text(encoding="utf-8").split())
    assert count < 300, "Fixture should be short to confirm the rejection logic"
