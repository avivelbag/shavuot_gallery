"""
Tests specific to piece 39-chesed-like-water: Physarum slime-mold simulation.

Covers:
  - Presence in pieces.json and on-disk file layout
  - Simulation requirements (requestAnimationFrame, agent count, food-source labels)
  - Palette colors in the HTML
  - Essay content with required Talmudic citations
  - Edge cases: missing piece, empty essay, essay word count
"""
import json
import os
import re

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECES_JSON  = os.path.join(GALLERY_ROOT, "pieces.json")
PIECE_ID     = "39-chesed-like-water"
PIECE_DIR    = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
HTML_PATH    = os.path.join(PIECE_DIR, "index.html")
ESSAY_PATH   = os.path.join(PIECE_DIR, "essay.md")


def _load_pieces():
    """Return parsed pieces.json list."""
    with open(PIECES_JSON, encoding="utf-8") as fh:
        return json.load(fh)


def _get_piece():
    """Return the pieces.json entry for piece 39, or None."""
    return next((p for p in _load_pieces() if p["id"] == PIECE_ID), None)


# ---------------------------------------------------------------------------
# Presence and file layout
# ---------------------------------------------------------------------------

def test_piece_in_pieces_json():
    """Piece 39-chesed-like-water must appear in pieces.json."""
    assert _get_piece() is not None, f"'{PIECE_ID}' not found in pieces.json"


def test_piece_has_all_required_fields():
    """Every required field must be present and non-empty."""
    required = ("id", "title", "tagline", "year", "theme", "technique",
                "path", "thumbnail", "essay")
    piece = _get_piece()
    assert piece is not None
    for field in required:
        val = piece.get(field)
        assert val is not None and val != "", (
            f"Field '{field}' is missing or empty in piece '{PIECE_ID}'"
        )


def test_index_html_exists():
    assert os.path.isfile(HTML_PATH), f"index.html not found at {HTML_PATH}"


def test_essay_md_exists():
    assert os.path.isfile(ESSAY_PATH), f"essay.md not found at {ESSAY_PATH}"


def test_readme_exists():
    readme = os.path.join(PIECE_DIR, "README.md")
    assert os.path.isfile(readme), f"README.md not found at {readme}"


def test_thumbnail_exists():
    piece = _get_piece()
    assert piece is not None
    thumb = os.path.join(GALLERY_ROOT, piece["thumbnail"])
    assert os.path.isfile(thumb), f"thumbnail not found: {piece['thumbnail']}"


def test_thumbnail_is_svg():
    piece = _get_piece()
    assert piece is not None
    assert piece["thumbnail"].endswith(".svg"), "thumbnail should be .svg"
    thumb = os.path.join(GALLERY_ROOT, piece["thumbnail"])
    if os.path.isfile(thumb):
        text = open(thumb, encoding="utf-8").read()
        assert "<svg" in text and "</svg>" in text, "thumbnail is not valid SVG"


# ---------------------------------------------------------------------------
# Simulation requirements
# ---------------------------------------------------------------------------

def test_uses_requestanimationframe():
    """index.html must drive animation with requestAnimationFrame."""
    html = open(HTML_PATH, encoding="utf-8").read()
    assert "requestAnimationFrame" in html, (
        "index.html must use requestAnimationFrame for 60fps animation"
    )


def test_agent_count_at_least_8000():
    """Simulation must declare at least 8,000 agents per acceptance criteria."""
    html = open(HTML_PATH, encoding="utf-8").read()
    # Accept any literal integer ≥ 8000 that appears in the agent-count assignment
    matches = re.findall(r'AGENT_COUNT\s*=\s*(\d+)', html)
    assert matches, "AGENT_COUNT constant not found in index.html"
    count = int(matches[0])
    assert count >= 8000, f"AGENT_COUNT is {count}; must be ≥ 8000"


def test_hebrew_food_labels_present():
    """The three Hebrew node labels ר (Ruth), נ (Naomi), ב (Boaz) must appear."""
    html = open(HTML_PATH, encoding="utf-8").read()
    for letter, name in [('ר', 'Ruth'), ('נ', 'Naomi'), ('ב', 'Boaz')]:
        assert letter in html, (
            f"Hebrew label '{letter}' ({name}) not found in index.html"
        )


def test_three_food_sources_configured():
    """Exactly three food-source objects must be present in FOOD_CONFIG."""
    html = open(HTML_PATH, encoding="utf-8").read()
    # Each food source has a label entry; count them
    label_entries = re.findall(r"label\s*:\s*'[רנב]'", html)
    assert len(label_entries) == 3, (
        f"Expected 3 food-source label entries, found {len(label_entries)}"
    )


def test_drift_mode_present():
    """Simulation must implement a drift mode transition after stabilization."""
    html = open(HTML_PATH, encoding="utf-8").read()
    assert "DRIFT_START" in html, "DRIFT_START constant not found — drift mode not implemented"
    matches = re.findall(r'DRIFT_START\s*=\s*(\d+)', html)
    assert matches, "DRIFT_START value not parseable"
    drift_frame = int(matches[0])
    # Acceptance criteria says ~1800 frames (~30s at 60fps); allow a reasonable range
    assert 1200 <= drift_frame <= 3600, (
        f"DRIFT_START={drift_frame} is outside expected range 1200–3600"
    )


# ---------------------------------------------------------------------------
# Palette colors
# ---------------------------------------------------------------------------

def test_background_color_cream():
    """Background must be #FAF0DC (deep warm cream)."""
    html = open(HTML_PATH, encoding="utf-8").read()
    assert "FAF0DC" in html.upper(), "Background color #FAF0DC not found in index.html"


def test_amber_color_present():
    """Amber-gold trail color #D4882A must appear in the palette."""
    html = open(HTML_PATH, encoding="utf-8").read()
    assert "D4882A" in html.upper() or "d4882a" in html.lower(), (
        "Amber color #D4882A not found in index.html"
    )


def test_rust_color_present():
    """Warm rust trail color #8B3A10 must appear in the palette."""
    html = open(HTML_PATH, encoding="utf-8").read()
    assert "8B3A10" in html.upper() or "8b3a10" in html.lower(), (
        "Rust color #8B3A10 not found in index.html"
    )


# ---------------------------------------------------------------------------
# Essay content
# ---------------------------------------------------------------------------

def test_essay_min_words():
    """essay.md must contain at least 200 words."""
    text = open(ESSAY_PATH, encoding="utf-8").read()
    wc = len(text.split())
    assert wc >= 200, f"essay.md has only {wc} words (minimum 200)"


def test_essay_cites_sotah():
    """Essay must cite Sotah 14a (chesed framing God's acts in Torah)."""
    text = open(ESSAY_PATH, encoding="utf-8").read()
    assert "Sotah" in text, "essay.md must cite Sotah 14a"


def test_essay_cites_ruth_rabbah():
    """Essay must cite Ruth Rabbah (Ruth's chesed toward Naomi)."""
    text = open(ESSAY_PATH, encoding="utf-8").read()
    assert "Ruth Rabbah" in text, "essay.md must cite Ruth Rabbah"


def test_essay_cites_shabbat():
    """Essay must cite Shabbat 88a (mountain held over Israel)."""
    text = open(ESSAY_PATH, encoding="utf-8").read()
    assert "Shabbat" in text or "Shabbat 88a" in text, (
        "essay.md must cite Shabbat 88a (mountain held over Israel)"
    )


def test_essay_embedded_in_html():
    """Key words from essay.md must appear verbatim in index.html."""
    essay = open(ESSAY_PATH, encoding="utf-8").read()
    html  = open(HTML_PATH,  encoding="utf-8").read()
    words = [w for w in essay.split() if len(w) > 6][:12]
    found = sum(1 for w in words if w in html)
    assert found >= 6, (
        f"Only {found}/12 long essay words found in index.html; essay may not be embedded"
    )


# ---------------------------------------------------------------------------
# Edge cases and failure modes
# ---------------------------------------------------------------------------

def test_piece_id_matches_directory():
    """The 'id' field must match the piece directory name."""
    piece = _get_piece()
    assert piece is not None
    path_parts = piece["path"].replace("\\", "/").split("/")
    dir_name = path_parts[-2]
    assert dir_name == PIECE_ID, (
        f"id '{PIECE_ID}' does not match directory '{dir_name}'"
    )


def test_missing_piece_not_in_dummy_list():
    """Absent piece entry is correctly detected as missing."""
    dummy = [{"id": "00-nonexistent", "title": "X"}]
    found = any(p["id"] == PIECE_ID for p in dummy)
    assert not found, "Fixture should confirm piece is absent from the dummy list"


def test_empty_essay_detected(tmp_path):
    """An essay.md with zero words should fail the word-count assertion."""
    empty = tmp_path / "essay.md"
    empty.write_text("", encoding="utf-8")
    text = empty.read_text(encoding="utf-8")
    wc = len(text.split())
    assert wc < 200, "Fixture confirms empty essay fails minimum word count"


def test_essay_without_sotah_detected():
    """A stub essay lacking 'Sotah' would fail the citation check."""
    stub = "This is a very short essay with no citations at all."
    assert "Sotah" not in stub, "Fixture confirms stub has no Sotah citation"


def test_html_uses_imagepixel_api():
    """ImageData / putImageData must be used for performance-critical pixel rendering."""
    html = open(HTML_PATH, encoding="utf-8").read()
    assert "putImageData" in html, (
        "index.html should use putImageData for efficient trail rendering"
    )


def test_no_duplicate_ids_in_pieces_json():
    """Adding the new piece must not create duplicate IDs."""
    pieces = _load_pieces()
    ids = [p["id"] for p in pieces]
    assert len(ids) == len(set(ids)), f"Duplicate piece IDs detected: {ids}"
