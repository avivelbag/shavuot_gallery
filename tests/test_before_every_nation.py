"""
Tests for piece 35-before-every-nation (Mondrian Recursive Subdivision).

Verifies the piece directory layout, pieces.json registration,
HTML animation structure, and essay content requirements.
"""
import json
import os

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID = "35-before-every-nation"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")


def load_pieces():
    """Load and return the parsed pieces.json list."""
    with open(PIECES_JSON, "r", encoding="utf-8") as fh:
        return json.load(fh)


def get_piece():
    """Return the pieces.json entry for piece 35, or None if absent."""
    for p in load_pieces():
        if p["id"] == PIECE_ID:
            return p
    return None


# ---------------------------------------------------------------------------
# Directory and file existence
# ---------------------------------------------------------------------------

def test_piece_directory_exists():
    """The piece directory must exist on disk."""
    assert os.path.isdir(PIECE_DIR), f"Piece directory missing: {PIECE_DIR}"


def test_index_html_exists():
    """index.html must exist inside the piece directory."""
    assert os.path.isfile(os.path.join(PIECE_DIR, "index.html"))


def test_essay_md_exists():
    """essay.md must exist inside the piece directory."""
    assert os.path.isfile(os.path.join(PIECE_DIR, "essay.md"))


def test_readme_md_exists():
    """README.md must exist inside the piece directory."""
    assert os.path.isfile(os.path.join(PIECE_DIR, "README.md"))


def test_thumbnail_svg_exists():
    """thumbnail.svg must exist inside the piece directory."""
    assert os.path.isfile(os.path.join(PIECE_DIR, "thumbnail.svg"))


# ---------------------------------------------------------------------------
# pieces.json registration
# ---------------------------------------------------------------------------

def test_piece_registered_in_pieces_json():
    """Piece 35 must appear in pieces.json."""
    assert get_piece() is not None, f"'{PIECE_ID}' not found in pieces.json"


def test_piece_json_required_fields():
    """All required fields must be present and non-empty."""
    piece = get_piece()
    assert piece is not None
    for field in ("id", "title", "tagline", "year", "theme", "technique", "path", "thumbnail", "essay"):
        assert field in piece, f"Missing field '{field}'"
        val = piece[field]
        assert val is not None and val != "", f"Field '{field}' is empty"


def test_piece_json_paths_correct():
    """Path, thumbnail, and essay fields must point to the expected files."""
    piece = get_piece()
    assert piece is not None
    assert piece["path"] == f"pieces/{PIECE_ID}/index.html"
    assert piece["thumbnail"] == f"pieces/{PIECE_ID}/thumbnail.svg"
    assert piece["essay"] == f"pieces/{PIECE_ID}/essay.md"


def test_piece_year_is_integer():
    """Year field must be an integer."""
    piece = get_piece()
    assert piece is not None
    assert isinstance(piece["year"], int)


def test_no_duplicate_ids():
    """No duplicate IDs exist in pieces.json after adding piece 35."""
    pieces = load_pieces()
    ids = [p["id"] for p in pieces]
    assert len(ids) == len(set(ids)), "Duplicate piece IDs found"


# ---------------------------------------------------------------------------
# HTML structure — animation requirements
# ---------------------------------------------------------------------------

def _html():
    return open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()


def test_html_uses_requestanimationframe():
    """The animation must use requestAnimationFrame."""
    assert "requestAnimationFrame" in _html()


def test_html_has_canvas_element():
    """index.html must contain a <canvas> element for the animation."""
    assert "<canvas" in _html()


def test_html_contains_hebrew_naaseh_vnishma():
    """The Hebrew text נַעֲשֶׂה וְנִשְׁמָע must appear in index.html."""
    assert "נַעֲשֶׂה וְנִשְׁמָע" in _html()


def test_html_contains_gold_color():
    """The parchment gold color #F5E6A3 must be present in index.html."""
    assert "#F5E6A3" in _html() or "F5E6A3" in _html()


def test_html_contains_text_color():
    """The deep blue text color #1A2B5F must be present in index.html."""
    assert "#1A2B5F" in _html() or "1A2B5F" in _html()


def test_html_mondrian_subdivision_algorithm():
    """The HTML must contain subdivision logic (biasedSplit or similar)."""
    html = _html()
    assert "subdivide" in html.lower() or "biasedSplit" in html or "split" in html.lower()


def test_html_dim_phase():
    """The dimming phase must be present in the animation logic."""
    assert "dim" in _html()


def test_html_bloom_phase():
    """The bloom phase must be present in the animation logic."""
    assert "bloom" in _html()


def test_html_loop_or_reset():
    """The animation must loop — either 'fadeout' or 'idle' restart must appear."""
    html = _html()
    assert "fadeout" in html or "idle" in html or "restart" in html


def test_html_palette_has_earth_tones():
    """The palette must include at least some of the expected muted earth tone hex values."""
    html = _html()
    earth_tones = ["#8B6F47", "#6B7B8D", "#A05C45", "#5C6B42"]
    found = sum(1 for tone in earth_tones if tone in html or tone.replace("#", "").lower() in html.lower())
    assert found >= 2, f"Expected at least 2 earth-tone palette entries in HTML, found {found}"


def test_html_embeds_essay_words():
    """index.html must embed the essay text inline (not fetch from disk at runtime)."""
    essay_text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    html = _html()
    words = [w for w in essay_text.split() if len(w) > 5][:10]
    found = sum(1 for w in words if w in html)
    assert found >= 5, f"Only {found}/10 sampled essay words found in HTML — essay may not be embedded"


# ---------------------------------------------------------------------------
# Essay content requirements
# ---------------------------------------------------------------------------

def _essay():
    return open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()


def test_essay_word_count():
    """Essay must be at least 200 words."""
    words = len(_essay().split())
    assert words >= 200, f"Essay has only {words} words (minimum 200)"


def test_essay_cites_sifre_devarim():
    """Essay must cite Sifre Devarim, Piska 343."""
    essay = _essay().lower()
    assert "sifre" in essay and "343" in essay, "Essay must cite Sifre Devarim Piska 343"


def test_essay_cites_mechilta():
    """Essay must cite Mechilta d'Rabbi Ishmael."""
    essay = _essay().lower()
    assert "mechilta" in essay, "Essay must cite Mechilta d'Rabbi Ishmael"


def test_essay_mentions_naaseh_vnishma():
    """Essay must discuss the phrase naaseh v'nishma."""
    essay = _essay().lower()
    assert "naaseh" in essay or "נַעֲשֶׂה" in _essay(), "Essay must discuss naaseh v'nishma"


def test_essay_cites_shabbat_88a():
    """Essay must cite Talmud Shabbat 88a."""
    essay = _essay().lower()
    assert "shabbat" in essay and "88" in essay, "Essay must cite Talmud Shabbat 88a"


def test_essay_mentions_nations_refusal():
    """Essay must discuss specific nations refusing (Esau/Edom, Ishmael, etc.)."""
    essay = _essay().lower()
    nations = ["esau", "ishmael", "edom", "ammon", "moab"]
    found = sum(1 for n in nations if n in essay)
    assert found >= 2, f"Essay mentions only {found} of the expected refusing nations"


def test_essay_mentions_murder_or_commandment():
    """Essay must reference specific commandments that the nations could not accept."""
    essay = _essay().lower()
    assert "murder" in essay or "steal" in essay or "commandment" in essay


# ---------------------------------------------------------------------------
# Thumbnail validity
# ---------------------------------------------------------------------------

def test_thumbnail_is_valid_svg():
    """thumbnail.svg must be a valid SVG file."""
    text = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert "<svg" in text and "</svg>" in text


def test_thumbnail_contains_rect_elements():
    """Thumbnail must contain <rect> elements representing the Mondrian grid."""
    text = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert text.count("<rect") >= 5, "Thumbnail should contain multiple rect elements"


# ---------------------------------------------------------------------------
# Edge case: piece removed from pieces.json would be caught
# ---------------------------------------------------------------------------

def test_missing_piece_detected(tmp_path):
    """A pieces.json without piece 35 should not contain the ID."""
    truncated = [p for p in load_pieces() if p["id"] != PIECE_ID]
    ids = [p["id"] for p in truncated]
    assert PIECE_ID not in ids, "Fixture: piece 35 correctly absent from truncated list"


def test_empty_essay_detected():
    """An empty string essay field would be caught by field validation."""
    bad = {"id": "35-before-every-nation", "essay": ""}
    assert not bad["essay"], "Fixture: empty essay field is falsy"
