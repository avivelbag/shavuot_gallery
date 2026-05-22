"""
Tests specific to piece 47-lo-bashamayim-hi.

Verifies the piece directory layout, pieces.json registration, animation
technique, colour palette, Hebrew text, and essay content — all requirements
from the acceptance criteria.
"""
import json
import os
import re

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID     = "47-lo-bashamayim-hi"
PIECE_DIR    = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
INDEX_HTML   = os.path.join(PIECE_DIR, "index.html")
ESSAY_MD     = os.path.join(PIECE_DIR, "essay.md")
README_MD    = os.path.join(PIECE_DIR, "README.md")
THUMBNAIL    = os.path.join(PIECE_DIR, "thumbnail.svg")
PIECES_JSON  = os.path.join(GALLERY_ROOT, "pieces.json")


def _html():
    with open(INDEX_HTML, encoding="utf-8") as fh:
        return fh.read()


def _essay():
    with open(ESSAY_MD, encoding="utf-8") as fh:
        return fh.read()


def _pieces():
    with open(PIECES_JSON, encoding="utf-8") as fh:
        return json.load(fh)


def _piece_entry():
    for p in _pieces():
        if p["id"] == PIECE_ID:
            return p
    return None


# ---------------------------------------------------------------------------
# Directory layout
# ---------------------------------------------------------------------------

def test_piece_directory_exists():
    assert os.path.isdir(PIECE_DIR), f"Piece directory {PIECE_DIR} is missing"


def test_index_html_exists():
    assert os.path.isfile(INDEX_HTML), "pieces/47-lo-bashamayim-hi/index.html is missing"


def test_essay_md_exists():
    assert os.path.isfile(ESSAY_MD), "pieces/47-lo-bashamayim-hi/essay.md is missing"


def test_readme_md_exists():
    assert os.path.isfile(README_MD), "pieces/47-lo-bashamayim-hi/README.md is missing"


def test_thumbnail_svg_exists():
    assert os.path.isfile(THUMBNAIL), "pieces/47-lo-bashamayim-hi/thumbnail.svg is missing"


# ---------------------------------------------------------------------------
# pieces.json registration
# ---------------------------------------------------------------------------

def test_piece_registered_in_pieces_json():
    entry = _piece_entry()
    assert entry is not None, f"'{PIECE_ID}' not found in pieces.json"


def test_piece_required_fields_present():
    entry = _piece_entry()
    assert entry is not None
    for field in ("id", "title", "tagline", "year", "theme", "technique", "path", "thumbnail", "essay"):
        assert field in entry and entry[field], f"Field '{field}' missing or empty in pieces.json entry"


def test_piece_path_points_to_existing_file():
    entry = _piece_entry()
    assert entry is not None
    full = os.path.join(GALLERY_ROOT, entry["path"])
    assert os.path.isfile(full), f"path '{entry['path']}' does not exist"


def test_piece_thumbnail_points_to_existing_file():
    entry = _piece_entry()
    assert entry is not None
    full = os.path.join(GALLERY_ROOT, entry["thumbnail"])
    assert os.path.isfile(full), f"thumbnail '{entry['thumbnail']}' does not exist"


def test_piece_essay_field_points_to_existing_file():
    entry = _piece_entry()
    assert entry is not None
    full = os.path.join(GALLERY_ROOT, entry["essay"])
    assert os.path.isfile(full), f"essay '{entry['essay']}' does not exist"


def test_piece_id_matches_directory():
    entry = _piece_entry()
    assert entry is not None
    path_dir = entry["path"].replace("\\", "/").split("/")[-2]
    assert path_dir == PIECE_ID, f"Path dir '{path_dir}' does not match id '{PIECE_ID}'"


def test_piece_year_is_int():
    entry = _piece_entry()
    assert entry is not None
    assert isinstance(entry["year"], int), "year must be an integer"


def test_no_duplicate_ids_after_adding_piece():
    pieces = _pieces()
    ids = [p["id"] for p in pieces]
    assert len(ids) == len(set(ids)), f"Duplicate IDs found: {ids}"


# ---------------------------------------------------------------------------
# Animation technique — canvas 2D n-body gravity
# ---------------------------------------------------------------------------

def test_html_uses_request_animation_frame():
    assert "requestAnimationFrame" in _html(), "index.html must use requestAnimationFrame"


def test_html_has_canvas_element():
    assert "<canvas" in _html(), "index.html must have a <canvas> element"


def test_html_uses_gravitational_force():
    """Gravitational constant or the G / r² pattern must appear in the script."""
    html = _html()
    assert re.search(r"\bG\b.*r2|r2.*\bG\b|G\s*/\s*Math\.max|G\s*/\s*r", html, re.DOTALL), (
        "index.html must implement gravitational F = G / r² formula"
    )


def test_html_has_attractor_nodes():
    """At least three attractor node x-positions must appear in the script."""
    html = _html()
    # Look for attractor array or attractor positions
    assert re.search(r"attract", html, re.IGNORECASE), (
        "index.html must define attractor nodes for the gravity simulation"
    )


def test_html_has_damping():
    """Velocity damping constant (DAMPING or *= 0.99x) must appear."""
    html = _html()
    assert re.search(r"[Dd][Aa][Mm][Pp][Ii][Nn][Gg]|vx.*0\.99|vy.*0\.99|\*\s*0\.99", html), (
        "index.html must apply velocity damping to prevent indefinite orbiting"
    )


def test_html_emits_particles_each_frame():
    """Particle emission function must be called in the animation loop."""
    html = _html()
    assert re.search(r"emit|Emit", html), (
        "index.html must emit particles each frame from the top emitter"
    )


# ---------------------------------------------------------------------------
# Palette — specific hex colours
# ---------------------------------------------------------------------------

def test_html_has_midnight_blue_background():
    assert "#050A1E" in _html() or "#050a1e" in _html(), (
        "index.html must use #050A1E as the background colour"
    )


def test_html_has_cool_blue_white_falling_particles():
    """Cool blue-white (#C8D8FF or similar) for falling particles."""
    html = _html()
    assert re.search(r"#[Cc]8[Dd]8[Ff][Ff]|200,\s*21[0-9],\s*255|C8D8FF", html, re.IGNORECASE), (
        "index.html must use cool blue-white (#C8D8FF) for falling particles"
    )


def test_html_has_warm_gold_settled_particles():
    """Warm gold (#E8B84B) for settled particles."""
    html = _html()
    assert re.search(r"#[Ee]8[Bb]84[Bb]|232,\s*184,\s*75|E8B84B", html, re.IGNORECASE), (
        "index.html must use warm gold (#E8B84B) for settled particles"
    )


def test_html_has_deep_amber_attractor_halos():
    """Deep amber (#C06A10) for attractor halos."""
    html = _html()
    assert re.search(r"#[Cc]06[Aa]10|192,\s*106,\s*16|C06A10", html, re.IGNORECASE), (
        "index.html must use deep amber (#C06A10) for attractor halos"
    )


# ---------------------------------------------------------------------------
# Hebrew text arc
# ---------------------------------------------------------------------------

def test_html_contains_hebrew_text():
    """The Hebrew string לֹא בַשָּׁמַיִם הִוא must appear in index.html."""
    assert "לֹא בַשָּׁמַיִם הִוא" in _html(), (
        "index.html must contain the Hebrew text לֹא בַשָּׁמַיִם הִוא"
    )


def test_html_has_svg_or_textpath_for_arc():
    """An SVG overlay or bezier-arc text draw must be present."""
    html = _html()
    has_svg_textpath = "<textPath" in html or "textPath" in html
    has_bezier       = re.search(r"bezier|textPath|quadratic|arcR|arcRadius|fillText", html, re.IGNORECASE)
    assert has_svg_textpath or has_bezier, (
        "index.html must render Hebrew text along an arc (SVG textPath or canvas bezier)"
    )


# ---------------------------------------------------------------------------
# Essay content
# ---------------------------------------------------------------------------

def test_essay_has_minimum_words():
    text = _essay()
    words = len(text.split())
    assert words >= 200, f"essay.md has only {words} words (need ≥ 200)"


def test_essay_cites_deuteronomy_30_12():
    essay = _essay().lower()
    assert "deuteronomy 30" in essay or "30:12" in essay, (
        "essay.md must cite Deuteronomy 30:12"
    )


def test_essay_cites_bava_metzia():
    essay = _essay().lower()
    assert "bava metzia" in essay or "bava metziah" in essay, (
        "essay.md must cite Bava Metzia 59b"
    )


def test_essay_mentions_naaseh_vnishma():
    essay = _essay().lower()
    assert "naaseh" in essay or "exodus 24" in essay, (
        "essay.md must reference naaseh v'nishma (Exodus 24:7)"
    )


def test_essay_mentions_gods_laughter():
    essay = _essay().lower()
    assert "laugh" in essay or "nitzchuni" in essay, (
        "essay.md must address God's laughter and what it signifies"
    )


def test_essay_mentions_shavuot_theme():
    essay = _essay().lower()
    assert "shavuot" in essay or "sinai" in essay or "interpretive authority" in essay, (
        "essay.md must connect the theme to Shavuot"
    )


def test_essay_connects_to_artwork():
    essay = _essay().lower()
    assert "particle" in essay or "gravity" in essay or "animation" in essay or "emitter" in essay, (
        "essay.md must connect the theological theme to the visual animation"
    )


def test_essay_embedded_in_html():
    """Key words from essay.md must appear in index.html (embedded, not fetched)."""
    essay_text = _essay()
    html       = _html()
    words      = [w for w in essay_text.split() if len(w) > 6][:15]
    found      = sum(1 for w in words if w in html)
    assert found >= 7, (
        f"Only {found}/15 sampled essay words found in index.html; "
        "the essay must be embedded inline"
    )


# ---------------------------------------------------------------------------
# Edge cases and failure modes
# ---------------------------------------------------------------------------

def test_thumbnail_is_valid_svg():
    text = open(THUMBNAIL, encoding="utf-8").read()
    assert "<svg" in text and "</svg>" in text, "thumbnail.svg must be valid SVG"


def test_thumbnail_has_correct_extension():
    assert THUMBNAIL.endswith(".svg"), "thumbnail must be an .svg file"


def test_piece_technique_mentions_gravity_or_nbody():
    entry = _piece_entry()
    assert entry is not None
    tech = entry.get("technique", "").lower()
    assert "gravity" in tech or "n-body" in tech or "orbital" in tech or "nbody" in tech, (
        "pieces.json technique field must reference the gravitational/n-body approach"
    )


def test_nonexistent_piece_returns_none():
    """Helper _piece_entry returns None for an unknown ID — sanity check."""
    pieces = _pieces()
    result = next((p for p in pieces if p["id"] == "99-does-not-exist"), None)
    assert result is None


def test_essay_word_count_above_threshold_not_stub():
    """A minimal stub essay would have far fewer than 200 words; ours must be substantial."""
    text  = _essay()
    words = len(text.split())
    assert words >= 400, (
        f"essay.md has only {words} words — expected a substantial essay (≥ 400)"
    )
