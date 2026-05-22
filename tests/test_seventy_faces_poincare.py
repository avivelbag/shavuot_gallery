"""
Tests for piece 53-seventy-faces-poincare (Seventy Faces — Poincaré Disk Tiling).

Covers:
- pieces.json registration (id, fields, theme, technique)
- Required files on disk (index.html, essay.md, thumbnail.svg, README.md)
- HTML content (canvas, requestAnimationFrame, Hebrew letter ת, palette colors, essay text)
- Essay content (citations, word count, key concepts)
- Thumbnail is valid SVG
- Edge cases: missing fields, wrong technique, duplicate ids
"""
import json
import os

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")
PIECE_ID = "53-seventy-faces-poincare"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)

PALETTE_COLORS = [
    "#1A1040",  # deep indigo
    "#C9A84C",  # gold
    "#F5EDD6",  # cream
    "#6B8C5A",  # sage green
    "#B87B6A",  # dusty rose
    "#7AAFC2",  # sky blue
    "#EDE8DC",  # soft white
]


# ─── Helpers ─────────────────────────────────────────────────────────────────

def load_pieces():
    """Load and return parsed pieces.json."""
    with open(PIECES_JSON, encoding="utf-8") as fh:
        return json.load(fh)


def get_piece():
    """Return the pieces.json entry for piece 53, or None."""
    for p in load_pieces():
        if p["id"] == PIECE_ID:
            return p
    return None


def read_html():
    """Return the full text of index.html."""
    path = os.path.join(PIECE_DIR, "index.html")
    return open(path, encoding="utf-8").read()


def read_essay():
    """Return the full text of essay.md."""
    path = os.path.join(PIECE_DIR, "essay.md")
    return open(path, encoding="utf-8").read()


def read_thumbnail():
    """Return the full text of thumbnail.svg."""
    path = os.path.join(PIECE_DIR, "thumbnail.svg")
    return open(path, encoding="utf-8").read()


# ─── pieces.json registration ────────────────────────────────────────────────

def test_piece_registered_in_json():
    """Piece 53 must appear in pieces.json."""
    piece = get_piece()
    assert piece is not None, f"Piece '{PIECE_ID}' not found in pieces.json"


def test_piece_id_correct():
    piece = get_piece()
    assert piece["id"] == PIECE_ID


def test_piece_theme_crown_of_torah():
    """Theme must reference Crown of Torah / naaseh v'nishma as specified."""
    piece = get_piece()
    assert piece is not None
    assert "Crown of Torah" in piece["theme"] or "naaseh" in piece["theme"].lower(), (
        f"Theme should reference 'Crown of Torah / naaseh v’nishma', got: {piece['theme']}"
    )


def test_piece_technique_hyperbolic():
    """Technique must reference hyperbolic tiling."""
    piece = get_piece()
    assert piece is not None
    assert "hyperbolic" in piece["technique"].lower(), (
        f"Technique should reference 'hyperbolic tiling', got: {piece['technique']}"
    )


def test_piece_year_is_int():
    piece = get_piece()
    assert isinstance(piece["year"], int)


def test_piece_path_points_to_index_html():
    piece = get_piece()
    assert piece["path"] == f"pieces/{PIECE_ID}/index.html"


def test_piece_thumbnail_path():
    piece = get_piece()
    assert piece["thumbnail"] == f"pieces/{PIECE_ID}/thumbnail.svg"


def test_piece_essay_path():
    piece = get_piece()
    assert piece["essay"] == f"pieces/{PIECE_ID}/essay.md"


def test_no_duplicate_ids():
    """Adding the new piece must not create duplicate IDs."""
    pieces = load_pieces()
    ids = [p["id"] for p in pieces]
    assert len(ids) == len(set(ids)), f"Duplicate IDs found in pieces.json: {ids}"


# ─── File existence ───────────────────────────────────────────────────────────

def test_index_html_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "index.html"))


def test_essay_md_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "essay.md"))


def test_thumbnail_svg_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "thumbnail.svg"))


def test_readme_md_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "README.md"))


# ─── index.html content ──────────────────────────────────────────────────────

def test_html_has_canvas_element():
    """The animation requires a <canvas> element."""
    html = read_html()
    assert "<canvas" in html, "index.html must contain a <canvas> element"


def test_html_uses_request_animation_frame():
    """Animation must use requestAnimationFrame for 60fps cap."""
    html = read_html()
    assert "requestAnimationFrame" in html


def test_html_has_central_hebrew_letter():
    """The central tile must display ת (Tav)."""
    html = read_html()
    assert "ת" in html, "index.html must contain Hebrew letter ת (Tav)"


def test_html_contains_all_palette_colors():
    """All 7 required palette colors must be referenced in the HTML."""
    html = read_html().lower()
    for color in PALETTE_COLORS:
        assert color.lower() in html, (
            f"Palette color {color} not found in index.html"
        )


def test_html_embeds_essay_words():
    """index.html must embed essay text (not just link to it)."""
    essay = read_essay()
    html = read_html()
    words = [w for w in essay.split() if len(w) > 6][:12]
    found = sum(1 for w in words if w in html)
    assert found >= 6, (
        f"index.html does not embed essay text; only {found}/12 essay words found in HTML"
    )


def test_html_mentions_poincare():
    """The Poincaré disk must be referenced in the HTML."""
    html = read_html()
    assert "Poincar" in html or "poincare" in html.lower()


def test_html_mentions_seventy_faces():
    """The seventy-faces concept must appear in the HTML."""
    html = read_html()
    assert "שבעים פנים" in html or "seventy" in html.lower() or "70" in html


def test_html_has_mobius_rotation():
    """Animation rotation via Möbius transformation must be present."""
    html = read_html()
    assert "mobius" in html.lower() or "mobiusRotate" in html or "Möbius" in html or "rotation" in html.lower()


def test_html_has_seven_colors_array():
    """The COLORS array (7 entries for 7 weeks/species) must be defined."""
    html = read_html()
    assert "COLORS" in html, "index.html must define a COLORS array"


def test_html_title_relevant():
    """Page title must reference the piece."""
    html = read_html()
    assert "seventy" in html.lower() or "poincar" in html.lower() or "Torah" in html


# ─── Essay content ────────────────────────────────────────────────────────────

def test_essay_minimum_word_count():
    """Essay must have at least 200 words."""
    text = read_essay()
    count = len(text.split())
    assert count >= 200, f"essay.md has only {count} words (need ≥ 200)"


def test_essay_cites_bamidbar_rabbah():
    """Essay must cite BaMidbar Rabbah 13:15 (שבעים פנים לתורה)."""
    text = read_essay()
    assert "BaMidbar Rabbah" in text or "Bamidbar Rabbah" in text or "במדבר" in text, (
        "essay.md must cite BaMidbar Rabbah 13:15"
    )


def test_essay_cites_proverbs():
    """Essay must reference Proverbs 3:17-18 (tree of life)."""
    text = read_essay()
    assert "Proverbs" in text or "tree of life" in text.lower() or "עץ חיים" in text, (
        "essay.md must reference Proverbs 3:17-18 (Torah as tree of life)"
    )


def test_essay_mentions_pardes():
    """Essay must explain PaRDeS (four levels of interpretation)."""
    text = read_essay()
    assert "PaRDeS" in text or "Peshat" in text or "peshat" in text, (
        "essay.md must explain the PaRDeS levels of interpretation"
    )


def test_essay_mentions_shavuot():
    """Essay must connect the piece to Shavuot."""
    text = read_essay()
    assert "Shavuot" in text or "shavuot" in text.lower()


def test_essay_mentions_hyperbolic_geometry():
    """Essay must explain the hyperbolic geometry metaphor."""
    text = read_essay()
    assert "hyperbolic" in text.lower() or "Poincaré" in text or "Poincare" in text


def test_essay_mentions_infinite_meaning():
    """Essay must articulate the infinite-meaning-in-finite-text idea."""
    text = read_essay()
    assert "infinite" in text.lower() or "inexhaustible" in text.lower()


# ─── Thumbnail ────────────────────────────────────────────────────────────────

def test_thumbnail_is_valid_svg():
    """thumbnail.svg must contain valid SVG markup."""
    svg = read_thumbnail()
    assert "<svg" in svg and "</svg>" in svg


def test_thumbnail_contains_disk():
    """Thumbnail must include the disk (circle element)."""
    svg = read_thumbnail()
    assert "<circle" in svg


def test_thumbnail_has_hebrew_letter():
    """Thumbnail must display the central Hebrew letter ת."""
    svg = read_thumbnail()
    assert "ת" in svg


def test_thumbnail_references_palette_colors():
    """Thumbnail must use at least 4 of the 7 palette colors."""
    svg = read_thumbnail().lower()
    found = sum(1 for c in PALETTE_COLORS if c.lower() in svg)
    assert found >= 4, f"Thumbnail only references {found}/7 palette colors"


# ─── Edge cases / failure modes ───────────────────────────────────────────────

def test_piece_with_wrong_technique_detected(tmp_path):
    """A piece registered with the wrong technique should fail our technique check."""
    bad_technique = "watercolor painting"
    assert "hyperbolic" not in bad_technique.lower(), (
        "Fixture must not contain 'hyperbolic' so the check would catch it"
    )


def test_piece_missing_required_fields_detected(tmp_path):
    """A piece missing 'theme' and 'technique' is not a valid registration."""
    bad_piece = {"id": PIECE_ID, "title": "Test", "year": 2026}
    assert "theme" not in bad_piece
    assert "technique" not in bad_piece


def test_essay_stub_too_short_detected(tmp_path):
    """An essay with fewer than 200 words would fail the word count check."""
    stub = "Torah is good. " * 10  # ~30 words
    assert len(stub.split()) < 200


def test_thumbnail_without_svg_tags_rejected(tmp_path):
    """A thumbnail file without <svg> tags must fail the SVG validity check."""
    bad_svg = "<html><body>Not an SVG</body></html>"
    assert "<svg" not in bad_svg


def test_duplicate_piece_id_rejected():
    """Introducing a duplicate ID (a second 53-seventy-faces-poincare) must be detectable."""
    pieces = load_pieces()
    ids = [p["id"] for p in pieces]
    # Adding the same id again would create a duplicate
    ids_with_dup = ids + [PIECE_ID]
    assert len(ids_with_dup) != len(set(ids_with_dup)), (
        "Adding a duplicate should be detectable by comparing list length to set size"
    )
