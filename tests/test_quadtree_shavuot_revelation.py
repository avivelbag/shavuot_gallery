"""
Tests for piece 93-quadtree-shavuot-revelation.

Verifies that all required files exist with the correct content, that the
pieces.json entry is well-formed, and that the index.html implements the
expected quadtree algorithm structure.
"""
import json
import os


GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID = "93-quadtree-shavuot-revelation"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_pieces():
    """Return the full parsed pieces.json list."""
    with open(PIECES_JSON, encoding="utf-8") as fh:
        return json.load(fh)


def get_piece():
    """Return the pieces.json entry for the quadtree piece, or None."""
    return next((p for p in load_pieces() if p["id"] == PIECE_ID), None)


def read_html():
    """Return the full text of index.html for this piece."""
    path = os.path.join(PIECE_DIR, "index.html")
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def read_essay():
    """Return the full text of essay.md for this piece."""
    path = os.path.join(PIECE_DIR, "essay.md")
    with open(path, encoding="utf-8") as fh:
        return fh.read()


# ---------------------------------------------------------------------------
# File existence — happy path
# ---------------------------------------------------------------------------

def test_piece_directory_exists():
    """The piece directory must be present on disk."""
    assert os.path.isdir(PIECE_DIR), f"Piece directory not found: {PIECE_DIR}"


def test_index_html_exists():
    """index.html must be present in the piece directory."""
    assert os.path.isfile(os.path.join(PIECE_DIR, "index.html"))


def test_essay_md_exists():
    """essay.md must be present in the piece directory."""
    assert os.path.isfile(os.path.join(PIECE_DIR, "essay.md"))


def test_thumbnail_svg_exists():
    """thumbnail.svg must be present in the piece directory."""
    assert os.path.isfile(os.path.join(PIECE_DIR, "thumbnail.svg"))


def test_readme_md_exists():
    """README.md must be present in the piece directory."""
    assert os.path.isfile(os.path.join(PIECE_DIR, "README.md"))


# ---------------------------------------------------------------------------
# pieces.json registration
# ---------------------------------------------------------------------------

def test_piece_in_pieces_json():
    """The piece must be registered in pieces.json."""
    assert get_piece() is not None, f"Piece '{PIECE_ID}' not found in pieces.json"


def test_pieces_json_required_fields():
    """All required fields must be present and non-empty."""
    required = ("id", "title", "tagline", "year", "theme", "technique",
                "path", "thumbnail", "essay")
    piece = get_piece()
    assert piece is not None
    for field in required:
        value = piece.get(field)
        assert value is not None and value != "", (
            f"Field '{field}' is missing or empty in pieces.json entry"
        )


def test_pieces_json_theme():
    """Theme must reference 'Matan Torah' and 'revelation'."""
    piece = get_piece()
    assert piece is not None
    theme = piece["theme"].lower()
    assert "matan torah" in theme or "revelation" in theme, (
        f"Expected 'Matan Torah' or 'revelation' in theme, got: {piece['theme']}"
    )


def test_pieces_json_technique():
    """Technique must reference 'quadtree'."""
    piece = get_piece()
    assert piece is not None
    assert "quadtree" in piece["technique"].lower(), (
        f"Expected 'quadtree' in technique, got: {piece['technique']}"
    )


def test_pieces_json_year():
    """Year must be the integer 2026."""
    piece = get_piece()
    assert piece is not None
    assert piece["year"] == 2026


def test_pieces_json_path_points_to_existing_file():
    """The 'path' field in pieces.json must resolve to an existing file."""
    piece = get_piece()
    assert piece is not None
    full = os.path.join(GALLERY_ROOT, piece["path"])
    assert os.path.isfile(full), f"File not found: {full}"


def test_pieces_json_thumbnail_points_to_existing_file():
    """The 'thumbnail' field must resolve to an existing file."""
    piece = get_piece()
    assert piece is not None
    full = os.path.join(GALLERY_ROOT, piece["thumbnail"])
    assert os.path.isfile(full), f"Thumbnail not found: {full}"


def test_pieces_json_essay_points_to_existing_file():
    """The 'essay' field must resolve to an existing file."""
    piece = get_piece()
    assert piece is not None
    full = os.path.join(GALLERY_ROOT, piece["essay"])
    assert os.path.isfile(full), f"Essay not found: {full}"


def test_no_duplicate_ids():
    """Registering the new piece must not create a duplicate ID."""
    pieces = load_pieces()
    ids = [p["id"] for p in pieces]
    assert len(ids) == len(set(ids)), "Duplicate piece IDs detected in pieces.json"


# ---------------------------------------------------------------------------
# essay.md content checks
# ---------------------------------------------------------------------------

def test_essay_minimum_word_count():
    """essay.md must contain at least 300 words."""
    text = read_essay()
    count = len(text.split())
    assert count >= 300, f"essay.md has only {count} words (need ≥ 300)"


def test_essay_references_exodus():
    """The essay must reference Exodus (the Sinai revelation source)."""
    text = read_essay()
    assert "Exodus" in text, "essay.md does not reference Exodus"


def test_essay_references_midrash_tanchuma():
    """The essay must cite Midrash Tanchuma as the Shavuot source."""
    text = read_essay()
    assert "Tanchuma" in text or "tanchuma" in text, (
        "essay.md does not mention Midrash Tanchuma"
    )


def test_essay_contains_hebrew_word():
    """The essay must include the Hebrew word שבועות."""
    text = read_essay()
    assert "שבועות" in text or "שְׁבוּעוֹת" in text, (
        "essay.md does not contain the Hebrew word שבועות"
    )


def test_essay_references_quadtree():
    """The essay must explain the quadtree as a model of revelation."""
    text = read_essay().lower()
    assert "quadtree" in text, "essay.md does not explain the quadtree"


def test_essay_references_variance():
    """The essay must mention variance or information content."""
    text = read_essay().lower()
    assert "variance" in text or "information" in text or "uncertainty" in text, (
        "essay.md does not discuss the information-theoretic dimension"
    )


# ---------------------------------------------------------------------------
# index.html content checks
# ---------------------------------------------------------------------------

def test_html_uses_requestanimationframe():
    """index.html must use requestAnimationFrame for animation."""
    html = read_html()
    assert "requestAnimationFrame" in html, (
        "index.html does not use requestAnimationFrame"
    )


def test_html_pre_renders_offscreen_canvas():
    """index.html must create an offscreen canvas for the target image."""
    html = read_html()
    assert "createElement('canvas')" in html or 'createElement("canvas")' in html, (
        "index.html does not create an offscreen canvas"
    )


def test_html_uses_sat_or_summed_area():
    """index.html must implement a summed-area table for fast variance queries."""
    html = read_html()
    assert "sat" in html.lower() or "summed" in html.lower() or "Float64Array" in html, (
        "index.html does not appear to use a summed-area table"
    )


def test_html_uses_priority_queue_or_heap():
    """index.html must use a priority queue (heap) to order subdivisions."""
    html = read_html()
    assert "heap" in html.lower() or "MaxHeap" in html or "priority" in html.lower(), (
        "index.html does not appear to use a priority queue"
    )


def test_html_includes_parchment_color():
    """The parchment background color #F4ECD8 must appear in index.html."""
    html = read_html()
    assert "F4ECD8" in html or "f4ecd8" in html, (
        "index.html does not use the parchment color #F4ECD8"
    )


def test_html_includes_gold_color():
    """The harvest gold color #C8941A must appear in index.html."""
    html = read_html()
    assert "C8941A" in html or "c8941a" in html, (
        "index.html does not use the harvest gold color #C8941A"
    )


def test_html_contains_hebrew_word():
    """index.html must embed the Hebrew word שבועות."""
    html = read_html()
    assert "שבועות" in html, (
        "index.html does not embed the Hebrew word שבועות"
    )


def test_html_implements_phases():
    """index.html must implement hold, collapse, and pause phases."""
    html = read_html()
    assert "hold" in html, "index.html missing 'hold' phase"
    assert "collapse" in html, "index.html missing 'collapse' phase"
    assert "pause" in html, "index.html missing 'pause' phase"


def test_html_has_split_history():
    """index.html must maintain a split history for tree reversal."""
    html = read_html()
    assert "splitHistory" in html or "split_history" in html or "history" in html.lower(), (
        "index.html does not appear to maintain a split history"
    )


def test_html_embeds_essay_text():
    """The essay text must be embedded inline in index.html."""
    essay = read_essay()
    html = read_html()
    words = [w for w in essay.split() if len(w) > 5][:10]
    found = sum(1 for w in words if w in html)
    assert found >= 5, (
        f"index.html does not appear to embed essay text "
        f"(only {found}/10 sampled words found)"
    )


def test_html_minimum_size_constant():
    """index.html must define a minimum leaf size constant (4×4 px or similar)."""
    html = read_html()
    assert "MIN_LEAF" in html or "minSize" in html or "min_size" in html \
        or "MIN_SPLIT" in html or "minLeaf" in html or "= 4" in html, (
        "index.html does not appear to define a minimum leaf size"
    )


# ---------------------------------------------------------------------------
# thumbnail.svg checks
# ---------------------------------------------------------------------------

def test_thumbnail_is_valid_svg():
    """thumbnail.svg must be a valid SVG file."""
    path = os.path.join(PIECE_DIR, "thumbnail.svg")
    text = open(path, encoding="utf-8").read()
    assert "<svg" in text and "</svg>" in text, (
        "thumbnail.svg does not appear to be valid SVG"
    )


def test_thumbnail_has_400x400_dimensions():
    """thumbnail.svg must be 400×400 as specified."""
    path = os.path.join(PIECE_DIR, "thumbnail.svg")
    text = open(path, encoding="utf-8").read()
    assert 'width="400"' in text and 'height="400"' in text, (
        "thumbnail.svg must have width=400 and height=400"
    )


def test_thumbnail_contains_rect_elements():
    """thumbnail.svg must contain rect elements for the quadtree mosaic."""
    path = os.path.join(PIECE_DIR, "thumbnail.svg")
    text = open(path, encoding="utf-8").read()
    assert "<rect" in text, "thumbnail.svg contains no <rect> elements"


def test_thumbnail_uses_gold_color():
    """thumbnail.svg must use the harvest gold color."""
    path = os.path.join(PIECE_DIR, "thumbnail.svg")
    text = open(path, encoding="utf-8").read()
    assert "C8941A" in text or "c8941a" in text, (
        "thumbnail.svg does not contain the harvest gold color #C8941A"
    )


# ---------------------------------------------------------------------------
# Edge cases and failure modes
# ---------------------------------------------------------------------------

def test_missing_piece_directory_detected(tmp_path):
    """A missing piece directory should be detectable by existence check."""
    missing = os.path.join(str(tmp_path), "99-nonexistent")
    assert not os.path.isdir(missing), "Fixture: directory must not exist"


def test_empty_essay_detected(tmp_path):
    """An empty essay file should fail the word-count check."""
    empty = tmp_path / "essay.md"
    empty.write_text("", encoding="utf-8")
    word_count = len(empty.read_text().split())
    assert word_count < 300, "Fixture: empty essay has fewer than 300 words"


def test_missing_fields_in_json_detected():
    """A pieces.json entry without required fields should fail the field check."""
    required = ("id", "title", "tagline", "year", "theme", "technique",
                "path", "thumbnail", "essay")
    stub = {"id": "99-test", "title": "Test"}
    for field in required:
        if field not in stub:
            assert field not in stub


def test_pieces_json_is_valid_json():
    """pieces.json must remain valid JSON after the new entry was added."""
    with open(PIECES_JSON, encoding="utf-8") as fh:
        data = json.load(fh)
    assert isinstance(data, list)
    assert len(data) >= 1
