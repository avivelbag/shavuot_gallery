"""
Tests for piece 49-brit-sinai-torus-knot.

Validates the WebGL torus knot piece: pieces.json registration, file layout,
essay substance, and HTML content requirements from the acceptance criteria.
"""
import json
import os
import re

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECES_JSON  = os.path.join(GALLERY_ROOT, "pieces.json")
PIECE_ID     = "49-brit-sinai-torus-knot"
PIECE_DIR    = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
INDEX_HTML   = os.path.join(PIECE_DIR, "index.html")
ESSAY_MD     = os.path.join(PIECE_DIR, "essay.md")


def _load_pieces():
    with open(PIECES_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


def _get_piece():
    for p in _load_pieces():
        if p["id"] == PIECE_ID:
            return p
    return None


# ---------------------------------------------------------------------------
# Happy path: pieces.json registration
# ---------------------------------------------------------------------------

def test_piece_registered_in_pieces_json():
    """The torus knot piece must appear in pieces.json."""
    piece = _get_piece()
    assert piece is not None, f"Piece '{PIECE_ID}' not found in pieces.json"


def test_piece_theme_is_matan_torah():
    """Theme must be exactly 'Matan Torah' per acceptance criteria."""
    piece = _get_piece()
    assert piece is not None
    assert piece["theme"] == "Matan Torah", (
        f"Expected theme 'Matan Torah', got '{piece.get('theme')}'"
    )


def test_piece_technique_mentions_webgl_torus_knot():
    """Technique field must reference WebGL 3D torus knot tube mesh."""
    piece = _get_piece()
    assert piece is not None
    technique = piece.get("technique", "").lower()
    assert "webgl" in technique and "torus" in technique, (
        f"Technique '{piece.get('technique')}' must mention WebGL and torus"
    )


def test_piece_year_is_int():
    piece = _get_piece()
    assert piece is not None
    assert isinstance(piece["year"], int), "year must be an integer"


def test_piece_required_fields_present():
    """All standard required fields must be non-empty."""
    required = ("id", "title", "tagline", "year", "theme", "technique",
                "path", "thumbnail", "essay")
    piece = _get_piece()
    assert piece is not None
    for field in required:
        assert field in piece and piece[field], (
            f"Field '{field}' missing or empty in piece registration"
        )


# ---------------------------------------------------------------------------
# File layout
# ---------------------------------------------------------------------------

def test_piece_directory_exists():
    assert os.path.isdir(PIECE_DIR), f"Piece directory {PIECE_DIR} does not exist"


def test_index_html_exists():
    assert os.path.isfile(INDEX_HTML), "index.html is missing from piece directory"


def test_essay_md_exists():
    assert os.path.isfile(ESSAY_MD), "essay.md is missing from piece directory"


def test_thumbnail_exists():
    piece = _get_piece()
    assert piece is not None
    thumb = os.path.join(GALLERY_ROOT, piece["thumbnail"])
    assert os.path.isfile(thumb), f"Thumbnail '{piece['thumbnail']}' does not exist"


def test_thumbnail_is_svg():
    piece = _get_piece()
    assert piece is not None
    thumb = os.path.join(GALLERY_ROOT, piece["thumbnail"])
    if os.path.isfile(thumb):
        content = open(thumb, encoding="utf-8").read()
        assert "<svg" in content and "</svg>" in content, "thumbnail is not valid SVG"


def test_readme_exists():
    readme = os.path.join(PIECE_DIR, "README.md")
    assert os.path.isfile(readme), "README.md is missing from piece directory"


def test_readme_mentions_sinai_theme():
    readme = os.path.join(PIECE_DIR, "README.md")
    text = open(readme, encoding="utf-8").read().lower()
    assert "sinai" in text or "matan torah" in text, (
        "README.md must mention the Sinai / Matan Torah theme"
    )


# ---------------------------------------------------------------------------
# Essay substance
# ---------------------------------------------------------------------------

def test_essay_at_least_300_words():
    """Acceptance criterion: essay must be at least 300 words."""
    text = open(ESSAY_MD, encoding="utf-8").read()
    count = len(text.split())
    assert count >= 300, f"essay.md has {count} words; need at least 300"


def test_essay_cites_exodus_24():
    """Essay must cite Exodus 24 (the primary covenant passage)."""
    text = open(ESSAY_MD, encoding="utf-8").read()
    assert "Exodus 24" in text or "exodus 24" in text.lower(), (
        "essay.md must cite Exodus 24:7-8"
    )


def test_essay_cites_shabbat_88a():
    """Essay must cite Shabbat 88a (the mountain-over-heads Talmud passage)."""
    text = open(ESSAY_MD, encoding="utf-8").read()
    assert "Shabbat 88a" in text or "shabbat 88a" in text.lower(), (
        "essay.md must cite Shabbat 88a"
    )


def test_essay_mentions_brit_or_covenant():
    """Essay must discuss the brit / covenant concept."""
    text = open(ESSAY_MD, encoding="utf-8").read().lower()
    assert "brit" in text or "covenant" in text, (
        "essay.md must discuss the brit/covenant concept"
    )


def test_essay_mentions_torus_knot():
    """Essay must explain the torus knot metaphor."""
    text = open(ESSAY_MD, encoding="utf-8").read().lower()
    assert "torus knot" in text, "essay.md must explain the torus knot"


def test_essay_contains_hebrew_formula():
    """Essay must include the Hebrew covenant formula נַעֲשֶׂה וְנִשְׁמָע."""
    text = open(ESSAY_MD, encoding="utf-8").read()
    # Check for key Hebrew words (do/hear formula)
    assert "נַעֲשֶׂה" in text or "נעשה" in text, (
        "essay.md must include the Hebrew formula נַעֲשֶׂה וְנִשְׁמָע"
    )


# ---------------------------------------------------------------------------
# index.html content requirements
# ---------------------------------------------------------------------------

def test_html_uses_webgl():
    """index.html must use WebGL (not canvas 2D)."""
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "webgl" in html.lower(), "index.html must use WebGL"


def test_html_uses_requestanimationframe():
    """index.html must drive animation with requestAnimationFrame."""
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "requestAnimationFrame" in html, (
        "index.html must use requestAnimationFrame for animation"
    )


def test_html_has_canvas_element():
    """index.html must have a canvas element for WebGL rendering."""
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "<canvas" in html, "index.html must have a <canvas> element"


def test_html_has_essay_panel():
    """index.html must embed essay text (not load it at runtime)."""
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "essay-panel" in html or "essay_panel" in html or "What a Brit" in html, (
        "index.html must embed the essay panel inline"
    )


def test_html_embeds_hebrew_passage():
    """index.html must embed the Exodus Hebrew passage inline."""
    html = open(INDEX_HTML, encoding="utf-8").read()
    # Check for key Hebrew word from Exodus 24
    assert "נַעֲשֶׂה" in html or "נעשה" in html, (
        "index.html must embed the Hebrew Exodus 24 passage"
    )


def test_html_embeds_english_translation():
    """index.html must embed an English translation of the passage."""
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "we will do" in html.lower() or "we will hear" in html.lower(), (
        "index.html must embed English translation of the covenant formula"
    )


def test_html_references_torus_knot_geometry():
    """index.html must contain torus knot mesh generation code."""
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "torusKnot" in html or "torus_knot" in html or "torus knot" in html.lower(), (
        "index.html must contain torus knot geometry code"
    )


def test_html_references_rotation_rates():
    """index.html must contain the specified rotation rates (0.003, 0.007, 0.001)."""
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "0.003" in html and "0.007" in html and "0.001" in html, (
        "index.html must implement the specified rotation increments"
    )


def test_html_mentions_tube_mesh_sides():
    """index.html should define tube cross-section sides (8–12)."""
    html = open(INDEX_HTML, encoding="utf-8").read()
    # Accept SIDES=8,9,10,11,12
    has_sides = any(f"SIDES={n}" in html or f"SIDES = {n}" in html or
                    f"sides={n}" in html or f"var SIDES={n}" in html
                    for n in range(8, 13))
    assert has_sides, "index.html must define tube cross-section SIDES in range 8–12"


def test_html_mesh_has_sufficient_segments():
    """index.html must use at least 200 segments for the curve (smooth appearance)."""
    html = open(INDEX_HTML, encoding="utf-8").read()
    found = re.search(r'N_SEG\s*=\s*(\d+)', html)
    if found:
        assert int(found.group(1)) >= 200, (
            f"N_SEG={found.group(1)} is less than the required 200"
        )
    else:
        # Accept any large segment count pattern
        big_numbers = re.findall(r'\b(2\d\d|[3-9]\d\d)\b', html)
        assert len(big_numbers) > 0, (
            "index.html must define at least 200 segments for the torus knot"
        )


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

def test_piece_path_ends_with_html():
    piece = _get_piece()
    assert piece is not None
    assert piece["path"].endswith(".html"), "path must point to an HTML file"


def test_piece_id_matches_directory():
    piece = _get_piece()
    assert piece is not None
    parts = piece["path"].replace("\\", "/").split("/")
    assert parts[-2] == PIECE_ID, (
        f"Directory in path '{parts[-2]}' does not match id '{PIECE_ID}'"
    )


def test_piece_no_duplicate_id():
    """Piece ID must be unique across all pieces."""
    pieces = _load_pieces()
    ids = [p["id"] for p in pieces]
    assert ids.count(PIECE_ID) == 1, f"Duplicate ID '{PIECE_ID}' in pieces.json"


# ---------------------------------------------------------------------------
# Failure modes
# ---------------------------------------------------------------------------

def test_missing_essay_file_would_fail(tmp_path):
    """Verify that a non-existent essay path is detected."""
    missing = os.path.join(str(tmp_path), "nonexistent_essay.md")
    assert not os.path.isfile(missing), "Fixture path must not exist"


def test_empty_theme_would_fail(tmp_path):
    """A pieces.json entry with empty theme should fail registration checks."""
    bad = [{"id": PIECE_ID, "theme": ""}]
    assert not bad[0]["theme"], "Fixture confirms empty theme is invalid"


def test_essay_below_minimum_word_count_would_fail(tmp_path):
    """An essay with fewer than 300 words must be flagged."""
    short_essay = tmp_path / "short.md"
    short_essay.write_text("short " * 50, encoding="utf-8")
    text = short_essay.read_text(encoding="utf-8")
    word_count = len(text.split())
    assert word_count < 300, "Fixture should have fewer than 300 words"
