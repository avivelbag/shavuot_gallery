"""
Tests for piece 71 — circle-packing-chag-hakatzir.

Covers the gallery registration, on-disk file layout, canvas/algorithm presence
in index.html, essay content requirements, and thumbnail validity.
"""
import json
import os
import re

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")
PIECE_ID = "71-circle-packing-chag-hakatzir"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)


def _load_piece():
    with open(PIECES_JSON, encoding="utf-8") as f:
        pieces = json.load(f)
    for p in pieces:
        if p["id"] == PIECE_ID:
            return p
    return None


def _html():
    return open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()


def _essay():
    return open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()


# ---------------------------------------------------------------------------
# Happy path — gallery registration
# ---------------------------------------------------------------------------

def test_piece_registered_in_pieces_json():
    """Piece 71 must appear in pieces.json."""
    piece = _load_piece()
    assert piece is not None, f"'{PIECE_ID}' not found in pieces.json"


def test_piece_has_required_fields():
    """All required fields must be present and non-empty."""
    piece = _load_piece()
    required = ("id", "title", "tagline", "year", "theme", "technique", "path", "thumbnail", "essay")
    for field in required:
        val = piece.get(field)
        assert val is not None and val != "", f"Missing or empty field: {field!r}"


def test_piece_theme_is_bikkurim():
    piece = _load_piece()
    assert "Bikkurim" in piece["theme"] or "First Fruits" in piece["theme"], (
        f"theme should reference Bikkurim / First Fruits, got: {piece['theme']!r}"
    )


def test_piece_technique_references_circle_packing():
    piece = _load_piece()
    assert "circle packing" in piece["technique"].lower(), (
        f"technique should mention circle packing, got: {piece['technique']!r}"
    )


def test_piece_year_is_integer():
    piece = _load_piece()
    assert isinstance(piece["year"], int)


# ---------------------------------------------------------------------------
# On-disk file layout
# ---------------------------------------------------------------------------

def test_index_html_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "index.html"))


def test_essay_md_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "essay.md"))


def test_thumbnail_svg_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "thumbnail.svg"))


def test_readme_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "README.md"))


def test_pieces_json_essay_path_exists():
    piece = _load_piece()
    full = os.path.join(GALLERY_ROOT, piece["essay"])
    assert os.path.isfile(full), f"essay path does not exist on disk: {piece['essay']}"


def test_pieces_json_thumbnail_path_exists():
    piece = _load_piece()
    full = os.path.join(GALLERY_ROOT, piece["thumbnail"])
    assert os.path.isfile(full), f"thumbnail path does not exist on disk: {piece['thumbnail']}"


# ---------------------------------------------------------------------------
# index.html — canvas and algorithm
# ---------------------------------------------------------------------------

def test_html_has_canvas_700x700():
    html = _html()
    assert 'width="700"' in html and 'height="700"' in html, (
        "index.html must have a 700×700 canvas"
    )


def test_html_packing_algorithm_present():
    """The JS packing loop (grow-radius until overlap) must be present."""
    html = _html()
    assert "overlaps" in html, "index.html must define an overlaps() check for circle packing"
    assert "candidates" in html, "index.html must seed candidate centers"


def test_html_seven_species_palette_present():
    """All seven hex color codes for the species must appear in index.html."""
    html = _html()
    species_colors = ["#E8C85A", "#C8A030", "#6B2D8B", "#8B4513", "#C0392B", "#556B2F", "#8B6914"]
    for color in species_colors:
        assert color in html, f"species color {color} missing from index.html"


def test_html_parchment_background():
    """Parchment background color must appear in index.html."""
    html = _html()
    assert "#F5EDD6" in html, "parchment background #F5EDD6 missing from index.html"


def test_html_cultivating_status_text():
    """The 'cultivating' progress text must appear in index.html."""
    html = _html()
    assert "cultivating" in html.lower(), "index.html must show a 'cultivating' progress message"


def test_html_stroke_applied():
    """Each circle must be stroked; darken() helper must exist."""
    html = _html()
    assert "darken" in html, "index.html must darken fill colors for stroke"
    assert "lineWidth" in html, "index.html must set lineWidth for the stroke"


def test_html_essay_text_embedded():
    """index.html must embed the essay text inline (not fetched at runtime)."""
    essay = _essay()
    html = _html()
    words = [w for w in essay.split() if len(w) > 6][:12]
    found = sum(1 for w in words if w in html)
    assert found >= 6, (
        f"index.html does not appear to embed essay text ({found}/12 sampled words found)"
    )


# ---------------------------------------------------------------------------
# essay.md content
# ---------------------------------------------------------------------------

def test_essay_word_count():
    """essay.md must be at least 380 words."""
    text = _essay()
    assert len(text.split()) >= 380, (
        f"essay.md has only {len(text.split())} words; need ≥ 380"
    )


def test_essay_mentions_deuteronomy():
    """Essay must open with the Deuteronomy citation."""
    text = _essay()
    assert "Deuteronomy" in text, "essay.md must cite Deuteronomy 8:7–10"


def test_essay_mentions_three_names():
    """Essay must explain the three Torah names for Shavuot."""
    text = _essay()
    assert "HaShavuot" in text or "Chag HaShavuot" in text, "essay must mention Chag HaShavuot"
    assert "HaKatzir" in text or "Chag HaKatzir" in text, "essay must mention Chag HaKatzir"
    assert "HaBikkurim" in text or "Yom HaBikkurim" in text, "essay must mention Yom HaBikkurim"


def test_essay_mentions_bikkurim_ceremony():
    """Essay must describe the bikkurim ceremony and the wandering Aramean declaration."""
    text = _essay()
    assert "bikkurim" in text.lower() or "Bikkurim" in text, "essay must discuss the bikkurim ceremony"
    assert "Aramean" in text, "essay must mention the 'wandering Aramean' declaration"


def test_essay_mentions_birkat_hamazon():
    """Essay must mention the rabbinic derivation of Birkat HaMazon from Deuteronomy 8:10."""
    text = _essay()
    assert "Birkat HaMazon" in text or "Birkat Hamazon" in text, (
        "essay must mention Birkat HaMazon derived from Deuteronomy 8:10"
    )


# ---------------------------------------------------------------------------
# thumbnail.svg
# ---------------------------------------------------------------------------

def test_thumbnail_is_valid_svg():
    svg = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert "<svg" in svg and "</svg>" in svg, "thumbnail.svg does not look like valid SVG"


def test_thumbnail_has_circle_elements():
    svg = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    circles = re.findall(r"<circle", svg)
    assert len(circles) >= 20, f"thumbnail.svg has only {len(circles)} circles; need ≥ 20"


def test_thumbnail_uses_all_seven_species_colors():
    """Thumbnail must include all 7 species palette colors."""
    svg = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    species_colors = ["#E8C85A", "#C8A030", "#6B2D8B", "#8B4513", "#C0392B", "#556B2F", "#8B6914"]
    for color in species_colors:
        assert color in svg, f"species color {color} missing from thumbnail.svg"


def test_thumbnail_has_parchment_background():
    svg = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert "#F5EDD6" in svg, "thumbnail.svg must have parchment background #F5EDD6"


def test_thumbnail_dimensions_400x400():
    svg = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert 'width="400"' in svg and 'height="400"' in svg, (
        "thumbnail.svg must be 400×400"
    )


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

def test_no_duplicate_ids_in_pieces_json():
    """Adding piece 71 must not create a duplicate ID."""
    with open(PIECES_JSON, encoding="utf-8") as f:
        pieces = json.load(f)
    ids = [p["id"] for p in pieces]
    assert len(ids) == len(set(ids)), f"Duplicate IDs found in pieces.json: {ids}"


def test_piece_path_ends_with_html():
    piece = _load_piece()
    assert piece["path"].endswith(".html"), "piece path must end with .html"


def test_piece_id_matches_directory():
    """The id field must match the directory name in the path."""
    piece = _load_piece()
    parts = piece["path"].replace("\\", "/").split("/")
    dir_name = parts[-2]
    assert dir_name == piece["id"], (
        f"id '{piece['id']}' does not match directory name '{dir_name}'"
    )


def test_piece_missing_from_json_detected():
    """Verifies that searching for a nonexistent piece id returns None."""
    with open(PIECES_JSON, encoding="utf-8") as f:
        pieces = json.load(f)
    found = next((p for p in pieces if p["id"] == "99-nonexistent-piece"), None)
    assert found is None, "Expected no result for a nonexistent piece id"


def test_essay_too_short_detected(tmp_path):
    """Confirms that a very short essay would fail the word-count guard."""
    short = tmp_path / "short.md"
    short.write_text("Only a few words here.", encoding="utf-8")
    text = short.read_text(encoding="utf-8")
    assert len(text.split()) < 380, "Fixture must be shorter than 380 words for this test to be meaningful"
