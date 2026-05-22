"""
Tests for piece 13-katzir-stipple — Chag HaKatzir (Harvest Stipple Canvas).

Verifies file layout, pieces.json registration, essay content,
HTML structure, and stipple animation requirements.
"""
import json
import os
import re


GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID = "13-katzir-stipple"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
HTML_PATH = os.path.join(PIECE_DIR, "index.html")
ESSAY_PATH = os.path.join(PIECE_DIR, "essay.md")
THUMB_PATH = os.path.join(PIECE_DIR, "thumbnail.svg")
README_PATH = os.path.join(PIECE_DIR, "README.md")
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")


# ---------------------------------------------------------------------------
# File layout
# ---------------------------------------------------------------------------

def test_piece_directory_exists():
    assert os.path.isdir(PIECE_DIR), f"Directory {PIECE_DIR} does not exist"


def test_index_html_exists():
    assert os.path.isfile(HTML_PATH), "index.html is missing"


def test_thumbnail_svg_exists():
    assert os.path.isfile(THUMB_PATH), "thumbnail.svg is missing"


def test_readme_exists():
    assert os.path.isfile(README_PATH), "README.md is missing"


def test_essay_md_exists():
    assert os.path.isfile(ESSAY_PATH), "essay.md is missing"


# ---------------------------------------------------------------------------
# pieces.json registration
# ---------------------------------------------------------------------------

def load_pieces():
    """Return the parsed pieces.json list."""
    with open(PIECES_JSON, encoding="utf-8") as fh:
        return json.load(fh)


def get_piece():
    """Return the katzir-stipple entry from pieces.json, or None."""
    return next((p for p in load_pieces() if p["id"] == PIECE_ID), None)


def test_piece_registered_in_pieces_json():
    assert get_piece() is not None, f"'{PIECE_ID}' not found in pieces.json"


def test_piece_id_is_13():
    """Orchestrator requires piece number 13 (not 12, which is omer-spiral)."""
    piece = get_piece()
    assert piece is not None
    assert piece["id"].startswith("13-"), f"Piece id must start with '13-', got: {piece['id']!r}"


def test_piece_has_harvest_theme():
    piece = get_piece()
    assert piece is not None
    theme = piece["theme"].lower()
    assert "harvest" in theme or "katzir" in theme, (
        f"theme field should reference Harvest or Katzir, got: {piece['theme']!r}"
    )


def test_piece_has_stipple_technique():
    piece = get_piece()
    assert piece is not None
    assert "stipple" in piece["technique"].lower(), (
        f"technique must mention stipple, got: {piece['technique']!r}"
    )


def test_piece_path_correct():
    piece = get_piece()
    assert piece is not None
    assert piece["path"] == f"pieces/{PIECE_ID}/index.html"


def test_piece_thumbnail_correct():
    piece = get_piece()
    assert piece is not None
    assert piece["thumbnail"] == f"pieces/{PIECE_ID}/thumbnail.svg"


def test_piece_essay_field_in_json():
    piece = get_piece()
    assert piece is not None
    assert piece.get("essay") == f"pieces/{PIECE_ID}/essay.md"


def test_piece_year_is_int():
    piece = get_piece()
    assert piece is not None
    assert isinstance(piece["year"], int)


def test_no_duplicate_ids():
    pieces = load_pieces()
    ids = [p["id"] for p in pieces]
    assert len(ids) == len(set(ids)), f"Duplicate piece IDs: {ids}"


def test_piece_all_required_fields():
    """All required pieces.json fields must be present and non-empty."""
    required = ("id", "title", "tagline", "year", "theme", "technique", "path", "thumbnail", "essay")
    piece = get_piece()
    assert piece is not None
    for field in required:
        val = piece.get(field)
        assert val is not None and val != "", (
            f"pieces.json entry missing or empty field: {field!r}"
        )


def test_does_not_collide_with_piece_12():
    """Piece 12 (omer-spiral) must still be registered separately."""
    pieces = load_pieces()
    ids = [p["id"] for p in pieces]
    assert "12-omer-spiral" in ids, "piece 12-omer-spiral must remain in pieces.json"
    assert "13-katzir-stipple" in ids, "piece 13-katzir-stipple must be present"


# ---------------------------------------------------------------------------
# Essay content
# ---------------------------------------------------------------------------

def read_essay():
    return open(ESSAY_PATH, encoding="utf-8").read()


def test_essay_word_count():
    text = read_essay()
    words = text.split()
    assert len(words) >= 300, f"essay.md has only {len(words)} words (need ≥ 300)"


def test_essay_references_exodus_23():
    text = read_essay()
    assert "Exodus 23" in text, "essay.md must cite Exodus 23:16 (Chag HaKatzir)"


def test_essay_references_leviticus_23():
    text = read_essay()
    assert "Leviticus 23" in text, "essay.md must cite Leviticus 23 (omer and two loaves)"


def test_essay_mentions_omer():
    text = read_essay()
    assert "omer" in text.lower(), "essay.md must mention the omer offering"


def test_essay_mentions_peah_or_gleaning():
    text = read_essay()
    lower = text.lower()
    assert "pe'ah" in lower or "gleaning" in lower or "shikchah" in lower, (
        "essay.md must reference gleaning laws (pe'ah / shikchah)"
    )


def test_essay_mentions_ruth():
    text = read_essay()
    assert "Ruth" in text, "essay.md must mention Ruth (the archetypal gleaner)"


def test_essay_not_placeholder():
    text = read_essay()
    for stub in ("TODO", "placeholder", "lorem ipsum", "FILL IN"):
        assert stub.lower() not in text.lower(), (
            f"essay.md appears to contain placeholder text: {stub!r}"
        )


# ---------------------------------------------------------------------------
# HTML / canvas structure
# ---------------------------------------------------------------------------

def read_html():
    return open(HTML_PATH, encoding="utf-8").read()


def test_html_uses_canvas():
    html = read_html()
    assert "<canvas" in html, "index.html must contain a <canvas> element"


def test_html_uses_request_animation_frame():
    html = read_html()
    assert "requestAnimationFrame" in html, (
        "index.html must use requestAnimationFrame for progressive stipple animation"
    )


def test_html_uses_is_point_in_path():
    html = read_html()
    assert "isPointInPath" in html, (
        "index.html must use ctx.isPointInPath to test dots against sheaf silhouette"
    )


def test_html_uses_bezier_curves():
    html = read_html()
    assert "bezierCurveTo" in html, (
        "index.html must define sheaf silhouette using bezierCurveTo"
    )


def test_html_uses_arc_for_dots():
    html = read_html()
    assert "ctx.arc" in html or ".arc(" in html, (
        "index.html must draw stipple dots using ctx.arc"
    )


def test_html_has_dots_per_frame_constant():
    """Progressive draw requires a per-frame dot count constant."""
    html = read_html()
    has_const = (
        "DOTS_PER_FRAME" in html or "dotsPerFrame" in html or
        "300" in html or "400" in html
    )
    assert has_const, "index.html must define a dots-per-frame constant (200–400 range)"


def test_html_has_hebrew_text():
    html = read_html()
    assert "חַג הַקָּצִיר" in html or "חַג" in html, (
        "index.html must contain Hebrew text חַג הַקָּצִיר"
    )


def test_html_embeds_essay_text():
    """Essay must be embedded verbatim in index.html."""
    essay = read_essay()
    html = read_html()
    words = [w for w in essay.split() if len(w) > 5]
    sampled = words[:10]
    found = sum(1 for w in sampled if w in html)
    assert found >= 5, (
        f"index.html does not embed essay text: only {found}/10 sampled words found"
    )


def test_html_has_warm_amber_background():
    html = read_html()
    assert "#f5c842" in html, "index.html must use warm amber-gold background #f5c842"


def test_html_has_sienna_dot_color():
    html = read_html()
    assert "#6b2800" in html, "index.html must use burnt-sienna dot color #6b2800"


def test_html_no_external_scripts():
    html = read_html()
    external = re.findall(r'<script[^>]+src=["\']https?://', html)
    assert len(external) == 0, f"index.html must not load external scripts: {external}"


def test_html_not_placeholder():
    html = read_html()
    for stub in ("TODO", "lorem ipsum", "FILL IN"):
        assert stub.lower() not in html.lower(), (
            f"index.html appears to contain placeholder text: {stub!r}"
        )


# ---------------------------------------------------------------------------
# Thumbnail SVG
# ---------------------------------------------------------------------------

def read_thumb():
    return open(THUMB_PATH, encoding="utf-8").read()


def test_thumbnail_is_valid_svg():
    svg = read_thumb()
    assert "<svg" in svg and "</svg>" in svg, "thumbnail.svg is not valid SVG"


def test_thumbnail_has_many_circles():
    svg = read_thumb()
    circles = re.findall(r'<circle', svg)
    assert len(circles) >= 200, (
        f"thumbnail.svg should have ≥200 circle elements for stipple effect, found {len(circles)}"
    )


def test_thumbnail_has_background_gradient():
    svg = read_thumb()
    assert "linearGradient" in svg or "radialGradient" in svg, (
        "thumbnail.svg should define a background gradient"
    )


def test_thumbnail_under_80kb():
    size = os.path.getsize(THUMB_PATH)
    assert size < 80 * 1024, f"thumbnail.svg is {size} bytes — must be under 80 KB"


# ---------------------------------------------------------------------------
# Edge cases and failure modes
# ---------------------------------------------------------------------------

def test_piece_directory_not_empty():
    files = os.listdir(PIECE_DIR)
    assert len(files) >= 4, f"piece directory has only {len(files)} files; expected ≥4"


def test_html_has_hold_phase():
    """The animation must hold after drawing completes before fading/restarting."""
    html = read_html()
    assert "hold" in html.lower(), (
        "index.html must implement a 'hold' phase after stipple completes"
    )


def test_gen_thumbnail_script_exists():
    gen_path = os.path.join(PIECE_DIR, "gen_thumbnail.py")
    assert os.path.isfile(gen_path), "gen_thumbnail.py must be committed alongside the piece"


def test_essay_cites_exodus_34():
    text = read_essay()
    assert "Exodus 34" in text, "essay.md must cite Exodus 34:22 (second Chag HaKatzir mention)"
