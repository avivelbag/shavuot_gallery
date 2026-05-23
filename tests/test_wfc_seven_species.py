"""
Tests for piece 79: Wave Function Collapse / Seven Species (Bikkurim).

Covers happy-path acceptance criteria, edge cases, and explicit failure modes.
"""
import json
import os

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID = "79-wave-function-collapse-seven-species"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _load_pieces():
    with open(PIECES_JSON, encoding="utf-8") as fh:
        return json.load(fh)


def _get_piece():
    for p in _load_pieces():
        if p["id"] == PIECE_ID:
            return p
    return None


def _read(rel):
    return open(os.path.join(GALLERY_ROOT, rel), encoding="utf-8").read()


# ---------------------------------------------------------------------------
# pieces.json registration
# ---------------------------------------------------------------------------

def test_piece_registered_in_pieces_json():
    """Piece must appear in pieces.json with the correct id."""
    assert _get_piece() is not None, f"Piece '{PIECE_ID}' not found in pieces.json"


def test_piece_theme_is_bikkurim_seven_species():
    """Theme must be 'Bikkurim / Seven Species'."""
    p = _get_piece()
    assert p is not None
    assert "Bikkurim" in p["theme"] and "Seven Species" in p["theme"], (
        f"Expected 'Bikkurim / Seven Species' in theme, got: {p['theme']!r}"
    )


def test_piece_technique_mentions_wfc():
    """Technique must mention Wave Function Collapse."""
    p = _get_piece()
    assert p is not None
    technique = p["technique"].lower()
    assert "wave function collapse" in technique or "wfc" in technique, (
        f"Expected technique to mention WFC, got: {p['technique']!r}"
    )


# ---------------------------------------------------------------------------
# File layout
# ---------------------------------------------------------------------------

def test_piece_directory_exists():
    assert os.path.isdir(PIECE_DIR), f"Piece directory missing: {PIECE_DIR}"


def test_index_html_exists():
    path = os.path.join(PIECE_DIR, "index.html")
    assert os.path.isfile(path), "index.html missing from piece directory"


def test_essay_md_exists():
    path = os.path.join(PIECE_DIR, "essay.md")
    assert os.path.isfile(path), "essay.md missing from piece directory"


def test_readme_exists():
    path = os.path.join(PIECE_DIR, "README.md")
    assert os.path.isfile(path), "README.md missing from piece directory"


def test_thumbnail_svg_exists():
    path = os.path.join(PIECE_DIR, "thumbnail.svg")
    assert os.path.isfile(path), "thumbnail.svg missing from piece directory"


# ---------------------------------------------------------------------------
# Essay content
# ---------------------------------------------------------------------------

def test_essay_opens_with_deuteronomy_reference():
    """Essay must open with or prominently mention Deuteronomy 8:7-8."""
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    assert "Deuteronomy" in text and ("8:7" in text or "8:8" in text), (
        "Essay must reference Deuteronomy 8:7–8 (the Seven Species verse)"
    )


def test_essay_mentions_all_seven_species():
    """Essay must mention all seven species by name."""
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read().lower()
    for species in ("wheat", "barley", "grape", "fig", "pomegranate", "olive", "date"):
        assert species in text, f"Essay does not mention species: {species}"


def test_essay_mentions_bikkurim():
    """Essay must mention Bikkurim."""
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    assert "Bikkurim" in text or "bikkurim" in text, "Essay must mention Bikkurim"


def test_essay_mentions_deuteronomy_26():
    """Essay must reference Deuteronomy 26 (the Bikkurim commandment)."""
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    assert "26" in text and "Deuteronomy" in text, (
        "Essay must reference Deuteronomy 26 (the Bikkurim declaration passage)"
    )


def test_essay_word_count_at_least_400():
    """Essay must be at least 400 words."""
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    wc = len(text.split())
    assert wc >= 400, f"Essay has only {wc} words; need ≥ 400"


# ---------------------------------------------------------------------------
# index.html — WFC implementation checks
# ---------------------------------------------------------------------------

def test_index_html_uses_request_animation_frame():
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "requestAnimationFrame" in html, (
        "index.html must use requestAnimationFrame for incremental WFC animation"
    )


def test_index_html_has_canvas_element():
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "<canvas" in html, "index.html must contain a <canvas> element"


def test_index_html_defines_tile_set():
    """index.html must define at least 7 tile types (one per species)."""
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    # check that all seven species appear as tile ids
    for species in ("wheat", "barley", "grape", "fig", "pomegranate", "olive", "date"):
        assert species in html, (
            f"index.html tile set must include a tile for species '{species}'"
        )


def test_index_html_has_wfc_entropy_logic():
    """index.html must implement lowest-entropy cell selection."""
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "entropy" in html.lower(), (
        "index.html must implement Shannon entropy-based cell selection"
    )


def test_index_html_has_propagation():
    """index.html must implement constraint propagation (propagate function)."""
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "propagate" in html, (
        "index.html must contain a propagation function for WFC constraint spreading"
    )


def test_index_html_has_restart_logic():
    """index.html must restart after the grid is fully collapsed."""
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "restart" in html, (
        "index.html must contain restart logic for looping the WFC animation"
    )


def test_index_html_uses_harvest_palette():
    """index.html must reference the harvest palette colors."""
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    # check for at least three palette colors
    palette = ["D4A017", "4A7C3F", "C0392B", "6B2D6B", "7D8B3A", "8B5E3C", "F5EDD0"]
    found = sum(1 for c in palette if c in html)
    assert found >= 3, (
        f"index.html should reference harvest palette colors; only found {found}/7"
    )


def test_index_html_embeds_essay_text():
    """Essay text must be embedded inline in index.html."""
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    essay = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    words = [w for w in essay.split() if len(w) > 6][:10]
    found = sum(1 for w in words if w in html)
    assert found >= 5, (
        f"index.html must embed essay text inline; only {found}/10 sampled words found"
    )


def test_index_html_grid_dimensions_present():
    """index.html must define the 16×10 grid."""
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "16" in html and "10" in html, (
        "index.html must define COLS=16 and ROWS=10 grid dimensions"
    )


# ---------------------------------------------------------------------------
# thumbnail SVG
# ---------------------------------------------------------------------------

def test_thumbnail_is_valid_svg():
    text = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert "<svg" in text and "</svg>" in text, "thumbnail.svg must be a valid SVG file"


def test_thumbnail_is_400x400():
    """Thumbnail must declare 400×400 dimensions."""
    text = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert 'width="400"' in text and 'height="400"' in text, (
        "thumbnail.svg must be 400×400 pixels"
    )


# ---------------------------------------------------------------------------
# Edge cases and failure modes
# ---------------------------------------------------------------------------

def test_piece_id_has_no_duplicate_in_pieces_json():
    """No duplicate IDs must exist."""
    pieces = _load_pieces()
    ids = [p["id"] for p in pieces]
    count = ids.count(PIECE_ID)
    assert count == 1, f"Piece id '{PIECE_ID}' appears {count} times in pieces.json (expected 1)"


def test_piece_path_correct_format():
    """Path must follow pieces/<id>/index.html convention."""
    p = _get_piece()
    assert p is not None
    expected = f"pieces/{PIECE_ID}/index.html"
    assert p["path"] == expected, (
        f"Piece path should be '{expected}', got '{p['path']}'"
    )


def test_missing_piece_returns_none():
    """Helper returns None for a non-existent piece id."""
    pieces = _load_pieces()
    result = next((p for p in pieces if p["id"] == "99-nonexistent-piece"), None)
    assert result is None, "Non-existent piece id should not be found in pieces.json"


def test_index_html_has_no_external_image_src():
    """index.html must not load external images (tile art is Canvas 2D only)."""
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    import re
    img_srcs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', html, re.IGNORECASE)
    external = [s for s in img_srcs if s.startswith("http")]
    assert len(external) == 0, (
        f"index.html must not load external images; found: {external}"
    )
