"""
Tests for piece 60 — HaBrit: The Covenant Unfurls (Verlet cloth simulation).

Validates structure, content, physics implementation references, and
differentiation from related pieces (42-sinai-chuppah, 55-unfurling-scroll-ruth).
"""
import json
import os

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID = "60-verlet-scroll-covenant"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")


def load_pieces():
    with open(PIECES_JSON, encoding="utf-8") as f:
        return json.load(f)


def get_piece():
    for p in load_pieces():
        if p["id"] == PIECE_ID:
            return p
    return None


def read_html():
    return open(os.path.join(GALLERY_ROOT, "pieces", PIECE_ID, "index.html"), encoding="utf-8").read()


def read_essay():
    return open(os.path.join(GALLERY_ROOT, "pieces", PIECE_ID, "essay.md"), encoding="utf-8").read()


# ---------------------------------------------------------------------------
# pieces.json registration
# ---------------------------------------------------------------------------

def test_piece_registered_in_pieces_json():
    assert get_piece() is not None, f"Piece '{PIECE_ID}' not found in pieces.json"


def test_piece_has_correct_theme():
    piece = get_piece()
    assert piece is not None
    assert "Matan Torah" in piece["theme"], (
        f"Expected theme 'Matan Torah', got '{piece['theme']}'"
    )


def test_piece_has_verlet_technique():
    piece = get_piece()
    assert piece is not None
    technique = piece["technique"].lower()
    assert "verlet" in technique, (
        f"Expected 'Verlet' in technique, got '{piece['technique']}'"
    )


def test_piece_year_is_2026():
    piece = get_piece()
    assert piece is not None
    assert piece["year"] == 2026


def test_piece_id_matches_directory():
    piece = get_piece()
    assert piece is not None
    dir_name = piece["path"].replace("\\", "/").split("/")[-2]
    assert dir_name == PIECE_ID


def test_no_duplicate_ids():
    pieces = load_pieces()
    ids = [p["id"] for p in pieces]
    assert len(ids) == len(set(ids)), "Duplicate piece IDs found"


def test_piece_number_above_59():
    """Piece number must be ≥ 60 per orchestrator numbering constraint."""
    num = int(PIECE_ID.split("-")[0])
    assert num >= 60, f"Piece number {num} must be ≥ 60"


# ---------------------------------------------------------------------------
# File existence
# ---------------------------------------------------------------------------

def test_index_html_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "index.html"))


def test_essay_md_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "essay.md"))


def test_thumbnail_exists():
    thumb = get_piece()["thumbnail"]
    assert os.path.isfile(os.path.join(GALLERY_ROOT, thumb))


def test_readme_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "README.md"))


def test_thumbnail_is_svg():
    thumb_path = os.path.join(GALLERY_ROOT, get_piece()["thumbnail"])
    text = open(thumb_path, encoding="utf-8").read()
    assert "<svg" in text and "</svg>" in text


# ---------------------------------------------------------------------------
# Essay content
# ---------------------------------------------------------------------------

def test_essay_word_count():
    text = read_essay()
    word_count = len(text.split())
    assert word_count >= 200, f"Essay has only {word_count} words (need ≥ 200)"


def test_essay_cites_exodus_24():
    essay = read_essay()
    assert "24" in essay, "Essay must cite Exodus 24"
    assert "Exodus" in essay or "exodus" in essay.lower()


def test_essay_contains_naaseh_vnishma_hebrew():
    essay = read_essay()
    assert "נַעֲשֶׂה" in essay or "נעשה" in essay, (
        "Essay must contain naaseh v'nishma in Hebrew"
    )


def test_essay_contains_talmud_shabbat_88a():
    essay = read_essay()
    assert "88" in essay, "Essay must cite Talmud Shabbat 88a"


def test_essay_contains_hebrew_verse_text():
    """Orchestrator requirement: embed actual Hebrew verse text, not just citation."""
    essay = read_essay()
    # Exodus 24:7 contains וַיִּקַּח סֵפֶר הַבְּרִית
    assert "הַבְּרִית" in essay or "הברית" in essay, (
        "Essay must embed the actual Hebrew text of the covenant verse"
    )


def test_essay_contains_english_translation():
    essay = read_essay()
    assert "Book of the Covenant" in essay or "will do and we will hear" in essay, (
        "Essay must contain English translation of key verses"
    )


# ---------------------------------------------------------------------------
# index.html: canvas animation and physics
# ---------------------------------------------------------------------------

def test_html_has_canvas():
    html = read_html()
    assert "<canvas" in html


def test_html_uses_requestanimationframe():
    html = read_html()
    assert "requestAnimationFrame" in html


def test_html_has_verlet_integration():
    """Verlet integration uses previous position (px, py) and current position."""
    html = read_html()
    assert "px" in html and "py" in html, (
        "index.html must use Verlet integration with px/py previous-position fields"
    )


def test_html_has_constraint_iterations():
    """Cloth simulation requires constraint satisfaction loop."""
    html = read_html()
    assert "ITERS" in html or "iter" in html.lower(), (
        "index.html must have constraint iteration loop"
    )


def test_html_has_springs():
    html = read_html()
    assert "springs" in html or "restLen" in html, (
        "index.html must define spring constraints"
    )


def test_html_has_gravity():
    html = read_html()
    assert "GRAVITY" in html or "gravity" in html.lower()


def test_html_has_damping():
    html = read_html()
    assert "DAMPING" in html or "damping" in html.lower()


def test_html_has_unrolling_animation():
    """Scroll must unroll progressively by releasing rows."""
    html = read_html()
    assert "unrolling" in html or "releasedRows" in html or "releaseRow" in html, (
        "index.html must implement progressive row-release unrolling"
    )


def test_html_canvas_700x700():
    html = read_html()
    assert 'width="700"' in html and 'height="700"' in html, (
        "Canvas must be 700×700 as specified"
    )


def test_html_has_hebrew_text_sefer_habrit():
    html = read_html()
    assert "הַבְּרִית" in html or "הברית" in html, (
        "index.html must render 'Sefer HaBrit' Hebrew text on cloth"
    )


def test_html_has_naaseh_vnishma():
    html = read_html()
    assert "נַעֲשֶׂה" in html or "נעשה" in html, (
        "index.html must render naaseh v'nishma Hebrew text"
    )


def test_html_has_parchment_color():
    html = read_html()
    assert "FFF5DC" in html.upper() or "fff5dc" in html.lower(), (
        "index.html must use parchment color #FFF5DC"
    )


def test_html_has_gold_rod_color():
    html = read_html()
    assert "C8922A" in html.upper() or "c8922a" in html.lower(), (
        "index.html must use burnished gold #C8922A for the rod"
    )


def test_html_has_dark_background():
    html = read_html()
    assert "0D0B14" in html.upper() or "0d0b14" in html.lower(), (
        "index.html must use dark night background #0D0B14"
    )


def test_html_embeds_essay_content():
    """index.html must inline the essay text (not fetch at runtime)."""
    essay = read_essay()
    html = read_html()
    words = [w for w in essay.split() if len(w) > 5][:12]
    found = sum(1 for w in words if w in html)
    assert found >= 6, (
        f"index.html embeds too little essay text ({found}/12 long words found)"
    )


def test_html_has_texture_mapping():
    """Triangle texture mapping required for text deformation on cloth."""
    html = read_html()
    assert "setTransform" in html or "drawImage" in html, (
        "index.html must use canvas transform for texture mapping text onto cloth"
    )


def test_html_has_rod_drawing():
    """The gold rod must be explicitly rendered."""
    html = read_html()
    assert "drawRod" in html or "rodH" in html or "ROD_Y" in html, (
        "index.html must draw the gold rod"
    )


def test_html_has_loop_phases():
    """Animation must loop through unrolling/holding/rerolling phases."""
    html = read_html()
    assert "holding" in html or "rerolling" in html, (
        "index.html must implement a multi-phase animation loop"
    )


# ---------------------------------------------------------------------------
# Differentiation from related pieces
# ---------------------------------------------------------------------------

def test_different_from_sinai_chuppah():
    """Must be clearly differentiated from piece 42 (Verlet canopy piece)."""
    readme = open(os.path.join(PIECE_DIR, "README.md"), encoding="utf-8").read()
    assert "42" in readme or "chuppah" in readme.lower(), (
        "README.md must acknowledge and differentiate from piece 42-sinai-chuppah"
    )


def test_different_from_unfurling_scroll_ruth():
    """Must be clearly differentiated from piece 55 (unfurling scroll of Ruth)."""
    readme = open(os.path.join(PIECE_DIR, "README.md"), encoding="utf-8").read()
    assert "55" in readme or "ruth" in readme.lower(), (
        "README.md must acknowledge and differentiate from piece 55-unfurling-scroll-ruth"
    )


# ---------------------------------------------------------------------------
# Thumbnail SVG
# ---------------------------------------------------------------------------

def test_thumbnail_has_rod_elements():
    thumb_path = os.path.join(GALLERY_ROOT, get_piece()["thumbnail"])
    svg = open(thumb_path, encoding="utf-8").read()
    assert "C8922A" in svg.upper() or "c8922a" in svg.lower(), (
        "Thumbnail SVG must use gold rod color"
    )


def test_thumbnail_has_naaseh_vnishma_text():
    thumb_path = os.path.join(GALLERY_ROOT, get_piece()["thumbnail"])
    svg = open(thumb_path, encoding="utf-8").read()
    assert "נַעֲשֶׂה" in svg or "נעשה" in svg, (
        "Thumbnail must display naaseh v'nishma Hebrew text"
    )


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

def test_piece_json_all_fields_present():
    """All required fields must be non-empty."""
    required = ("id", "title", "tagline", "year", "theme", "technique", "path", "thumbnail", "essay")
    piece = get_piece()
    assert piece is not None
    for field in required:
        assert field in piece and piece[field], f"Field '{field}' missing or empty"


def test_essay_path_in_json_matches_file():
    piece = get_piece()
    essay_path = os.path.join(GALLERY_ROOT, piece["essay"])
    assert os.path.isfile(essay_path), f"Essay file '{piece['essay']}' not found on disk"


def test_html_path_in_json_matches_file():
    piece = get_piece()
    html_path = os.path.join(GALLERY_ROOT, piece["path"])
    assert os.path.isfile(html_path), f"HTML file '{piece['path']}' not found on disk"


def test_cloth_grid_constants_present():
    """Cloth grid dimensions COLS and ROWS must be defined in index.html."""
    html = read_html()
    assert "COLS" in html and "ROWS" in html, (
        "index.html must define COLS and ROWS cloth grid constants"
    )


def test_shear_springs_present():
    """Cloth simulation needs shear springs for stability."""
    html = read_html()
    assert "shear" in html.lower() or "SQRT2" in html or "sqrt2" in html.lower() or "Math.SQRT2" in html, (
        "index.html must include diagonal/shear springs (restLen = SEG * √2)"
    )


def test_essay_substantial_word_count():
    """Essay must be at least 300 words as specified in acceptance criteria."""
    text = read_essay()
    word_count = len(text.split())
    assert word_count >= 300, f"Essay has {word_count} words; acceptance requires ~350"
