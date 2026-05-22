"""
Tests specific to piece 48-two-torahs-double-helix.

Covers piece-specific acceptance criteria: correct directory layout, animation
technique, Hebrew label presence, essay content requirements, and failure modes.
"""
import json
import os

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID     = "48-two-torahs-double-helix"
PIECE_DIR    = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
INDEX_HTML   = os.path.join(PIECE_DIR, "index.html")
ESSAY_MD     = os.path.join(PIECE_DIR, "essay.md")
THUMBNAIL    = os.path.join(PIECE_DIR, "thumbnail.svg")
README_MD    = os.path.join(PIECE_DIR, "README.md")
PIECES_JSON  = os.path.join(GALLERY_ROOT, "pieces.json")


# ---------------------------------------------------------------------------
# Happy path — acceptance criteria
# ---------------------------------------------------------------------------

def test_piece_directory_exists():
    assert os.path.isdir(PIECE_DIR), f"Piece directory {PIECE_DIR} does not exist"


def test_index_html_exists():
    assert os.path.isfile(INDEX_HTML), "index.html is missing"


def test_essay_md_exists():
    assert os.path.isfile(ESSAY_MD), "essay.md is missing"


def test_thumbnail_svg_exists():
    assert os.path.isfile(THUMBNAIL), "thumbnail.svg is missing"


def test_readme_exists():
    assert os.path.isfile(README_MD), "README.md is missing"


def test_piece_registered_in_pieces_json():
    with open(PIECES_JSON, encoding="utf-8") as fh:
        pieces = json.load(fh)
    ids = [p["id"] for p in pieces]
    assert PIECE_ID in ids, f"{PIECE_ID} not found in pieces.json"


def test_piece_json_entry_has_required_fields():
    with open(PIECES_JSON, encoding="utf-8") as fh:
        pieces = json.load(fh)
    entry = next((p for p in pieces if p["id"] == PIECE_ID), None)
    assert entry is not None
    for field in ("id", "title", "tagline", "year", "theme", "technique", "path", "thumbnail", "essay"):
        assert field in entry and entry[field], f"Field '{field}' missing or empty"


def test_index_html_uses_requestanimationframe():
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "requestAnimationFrame" in html, "index.html must use requestAnimationFrame for animation"


def test_index_html_has_canvas_element():
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "<canvas" in html, "index.html must contain a <canvas> element"


def test_index_html_painter_algorithm_sort():
    """Painter's algorithm requires sorting segments by z each frame."""
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert ".sort(" in html, "index.html must sort segments by depth (painter's algorithm)"


def test_index_html_has_hebrew_label():
    """The label תּוֹרָה שֶׁבִּכְתָב / תּוֹרָה שֶׁבְּעַל פֶּה must appear in the HTML."""
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "תּוֹרָה שֶׁבִּכְתָב" in html, "Written Torah label not found in index.html"
    assert "תּוֹרָה שֶׁבְּעַל פֶּה" in html, "Oral Torah label not found in index.html"


def test_index_html_has_written_torah_words():
    """Written Torah words from Bereishit 1:1 must appear in the JS word list."""
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "בְּרֵאשִׁית" in html, "Bereishit 1:1 opening word not found in index.html"


def test_index_html_has_oral_torah_words():
    """Oral Torah words from Pirkei Avot must appear in the JS word list."""
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "מֹשֶׁה" in html, "Pirkei Avot word not found in index.html"
    assert "מִסִּינַי" in html, "Pirkei Avot word not found in index.html"


def test_index_html_gold_ribbon_color():
    """Written Torah ribbon must use the specified warm gold colour."""
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "#D4A830" in html, "Written Torah ribbon colour #D4A830 not found"


def test_index_html_green_ribbon_color():
    """Oral Torah ribbon must use the specified olive-green colour."""
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "#3A5C1A" in html, "Oral Torah ribbon colour #3A5C1A not found"


def test_index_html_background_color():
    """Canvas background must be the specified deep parchment colour."""
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "#1A1408" in html, "Background colour #1A1408 not found"


def test_index_html_rotation_speed():
    """Rotation constant π/1800 (6°/s at 60fps) must be present."""
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "1800" in html, "Rotation constant 1800 (for 6°/s) not found in index.html"


def test_index_html_helix_phase_offset():
    """The two strands must be offset by π (Math.PI) for a true double helix."""
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "Math.PI" in html, "Strand π offset (Math.PI) not found in index.html"


def test_index_html_embeds_essay_text():
    """index.html must embed essay text; it must not rely on a runtime fetch."""
    essay = open(ESSAY_MD, encoding="utf-8").read()
    html  = open(INDEX_HTML, encoding="utf-8").read()
    long_words = [w for w in essay.split() if len(w) > 6][:10]
    found = sum(1 for w in long_words if w in html)
    assert found >= 5, (
        f"index.html does not appear to embed essay text "
        f"(only {found}/10 sampled words found)"
    )


# ---------------------------------------------------------------------------
# Essay content requirements
# ---------------------------------------------------------------------------

def test_essay_cites_avot_1_1():
    essay = open(ESSAY_MD, encoding="utf-8").read()
    assert "Avot 1:1" in essay or "Avot 1" in essay, "Essay must cite Avot 1:1"


def test_essay_cites_exodus_rabbah():
    essay = open(ESSAY_MD, encoding="utf-8").read()
    assert "Exodus Rabbah" in essay, "Essay must cite Exodus Rabbah 47:1"


def test_essay_mentions_oral_written_coequal():
    essay = open(ESSAY_MD, encoding="utf-8").read()
    assert "Oral Torah" in essay or "Torah she-baal peh" in essay, (
        "Essay must discuss the Oral Torah as co-equal revelation"
    )


def test_essay_mentions_shavuot():
    essay = open(ESSAY_MD, encoding="utf-8").read()
    assert "Shavuot" in essay, "Essay must connect the visual to Shavuot"


def test_essay_min_word_count():
    essay = open(ESSAY_MD, encoding="utf-8").read()
    count = len(essay.split())
    assert count >= 200, f"Essay has only {count} words (minimum 200)"


def test_thumbnail_is_valid_svg():
    svg = open(THUMBNAIL, encoding="utf-8").read()
    assert "<svg" in svg and "</svg>" in svg, "thumbnail.svg does not look like valid SVG"


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

def test_index_html_project_function_present():
    """The 3D-to-2D projection function must be defined."""
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "function project" in html, "project() function not found"


def test_index_html_depth_scaling():
    """Font size or ribbon width must be modulated by depth."""
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "fontSize" in html or "font-size" in html.lower(), (
        "Depth-scaled font size must be used"
    )


def test_pieces_json_no_duplicate_ids_after_addition():
    with open(PIECES_JSON, encoding="utf-8") as fh:
        pieces = json.load(fh)
    ids = [p["id"] for p in pieces]
    assert len(ids) == len(set(ids)), "Duplicate piece IDs found in pieces.json"


def test_piece_path_resolves_to_existing_file():
    with open(PIECES_JSON, encoding="utf-8") as fh:
        pieces = json.load(fh)
    entry = next((p for p in pieces if p["id"] == PIECE_ID), None)
    assert entry is not None
    full_path = os.path.join(GALLERY_ROOT, entry["path"])
    assert os.path.isfile(full_path), f"path field {entry['path']} does not resolve to a file"


# ---------------------------------------------------------------------------
# Failure modes
# ---------------------------------------------------------------------------

def test_empty_word_list_would_break_animation(tmp_path):
    """An empty word list would cause modulo-by-zero; confirm lists are non-empty."""
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "WRITTEN_WORDS" in html, "WRITTEN_WORDS must be defined"
    assert "ORAL_WORDS" in html, "ORAL_WORDS must be defined"
    assert "בְּרֵאשִׁית" in html, "WRITTEN_WORDS must not be empty"
    assert "מֹשֶׁה" in html, "ORAL_WORDS must not be empty"


def test_nonexistent_piece_not_in_json(tmp_path):
    """A piece ID that was never registered should not appear in pieces.json."""
    with open(PIECES_JSON, encoding="utf-8") as fh:
        pieces = json.load(fh)
    ids = [p["id"] for p in pieces]
    assert "99-does-not-exist" not in ids


def test_essay_not_stub():
    """A stub essay (a single sentence) should not pass the word-count check."""
    stub = "This is a stub essay."
    count = len(stub.split())
    assert count < 200, "Fixture: stub should have fewer than 200 words"
    real_essay = open(ESSAY_MD, encoding="utf-8").read()
    assert len(real_essay.split()) >= 200, "Real essay must have at least 200 words"
