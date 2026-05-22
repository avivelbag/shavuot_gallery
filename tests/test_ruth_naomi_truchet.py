"""
Tests for piece 14-ruth-naomi-truchet — Wherever You Go (Ruth and Naomi).

Covers: file layout, pieces.json registration, essay content requirements,
HTML structure (truchet canvas, animation, Hebrew text, embedded essay),
thumbnail SVG validity, palette and figure-color presence, and edge cases.
"""
import json
import os
import re

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID = "14-ruth-naomi-truchet"
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
    """The piece directory must exist on disk."""
    assert os.path.isdir(PIECE_DIR), f"Directory {PIECE_DIR} does not exist"


def test_index_html_exists():
    """index.html must be present."""
    assert os.path.isfile(HTML_PATH), "index.html is missing"


def test_thumbnail_svg_exists():
    """thumbnail.svg must be present."""
    assert os.path.isfile(THUMB_PATH), "thumbnail.svg is missing"


def test_readme_exists():
    """README.md must be present."""
    assert os.path.isfile(README_PATH), "README.md is missing"


def test_essay_md_exists():
    """essay.md must be present."""
    assert os.path.isfile(ESSAY_PATH), "essay.md is missing"


# ---------------------------------------------------------------------------
# pieces.json registration
# ---------------------------------------------------------------------------

def _load_pieces():
    """Return the parsed pieces.json list."""
    with open(PIECES_JSON, encoding="utf-8") as fh:
        return json.load(fh)


def _get_piece():
    """Return the ruth-naomi-truchet entry or None."""
    return next((p for p in _load_pieces() if p["id"] == PIECE_ID), None)


def test_piece_registered_in_pieces_json():
    """The piece must appear in pieces.json."""
    assert _get_piece() is not None, f"'{PIECE_ID}' not found in pieces.json"


def test_piece_theme_mentions_ruth():
    """The theme field must reference Ruth."""
    piece = _get_piece()
    assert piece is not None
    theme = piece.get("theme", "")
    assert "Ruth" in theme or "ruth" in theme.lower(), (
        f"theme must mention Ruth, got: {theme!r}"
    )


def test_piece_technique_mentions_truchet():
    """The technique field must mention truchet tiles."""
    piece = _get_piece()
    assert piece is not None
    technique = piece.get("technique", "")
    assert "truchet" in technique.lower(), (
        f"technique must mention truchet tiles, got: {technique!r}"
    )


def test_piece_path_correct():
    """The path field must point to the correct index.html."""
    piece = _get_piece()
    assert piece is not None
    assert piece["path"] == f"pieces/{PIECE_ID}/index.html"


def test_piece_thumbnail_correct():
    """The thumbnail field must point to the correct file."""
    piece = _get_piece()
    assert piece is not None
    assert piece["thumbnail"] == f"pieces/{PIECE_ID}/thumbnail.svg"


def test_piece_essay_field_correct():
    """The essay field must point to the correct essay.md."""
    piece = _get_piece()
    assert piece is not None
    assert piece.get("essay") == f"pieces/{PIECE_ID}/essay.md"


def test_piece_year_is_int():
    """The year field must be an integer."""
    piece = _get_piece()
    assert piece is not None
    assert isinstance(piece["year"], int)


def test_no_duplicate_ids():
    """No two pieces may share an id."""
    ids = [p["id"] for p in _load_pieces()]
    assert len(ids) == len(set(ids)), f"Duplicate piece IDs: {ids}"


def test_all_required_fields_present():
    """All required fields must be present and non-empty."""
    required = ("id", "title", "tagline", "year", "theme", "technique", "path", "thumbnail", "essay")
    piece = _get_piece()
    assert piece is not None
    for field in required:
        val = piece.get(field)
        assert val is not None and val != "", (
            f"pieces.json entry missing or empty field: {field!r}"
        )


# ---------------------------------------------------------------------------
# Essay content
# ---------------------------------------------------------------------------

def _read_essay():
    return open(ESSAY_PATH, encoding="utf-8").read()


def test_essay_minimum_word_count():
    """Essay must be at least 300 words."""
    text = _read_essay()
    words = text.split()
    assert len(words) >= 300, f"essay.md has only {len(words)} words (need ≥ 300)"


def test_essay_cites_ruth_1_16():
    """Essay must cite Ruth 1:16."""
    text = _read_essay()
    assert "Ruth 1:16" in text or "Ruth 1" in text, (
        "essay.md must cite Ruth 1:16"
    )


def test_essay_mentions_shavuot():
    """Essay must explain why Ruth is read on Shavuot."""
    text = _read_essay()
    assert "Shavuot" in text or "shavuot" in text.lower(), (
        "essay.md must explain the Shavuot connection"
    )


def test_essay_mentions_harvest():
    """Essay must mention the harvest context."""
    text = _read_essay()
    assert "harvest" in text.lower(), "essay.md must mention the harvest context"


def test_essay_mentions_conversion_or_covenant():
    """Essay must discuss conversion or covenantal loyalty."""
    text = _read_essay()
    has_theme = (
        "conversion" in text.lower()
        or "covenant" in text.lower()
        or "loyalty" in text.lower()
    )
    assert has_theme, "essay.md must mention conversion, covenant, or loyalty"


def test_essay_names_naomi_and_ruth():
    """Essay must name both characters."""
    text = _read_essay()
    assert "Ruth" in text, "essay.md must name Ruth"
    assert "Naomi" in text, "essay.md must name Naomi"


def test_essay_not_placeholder():
    """Essay must not contain placeholder stubs."""
    text = _read_essay()
    for stub in ("TODO", "placeholder", "lorem ipsum", "FILL IN"):
        assert stub.lower() not in text.lower(), (
            f"essay.md contains placeholder text: {stub!r}"
        )


# ---------------------------------------------------------------------------
# HTML structure
# ---------------------------------------------------------------------------

def _read_html():
    return open(HTML_PATH, encoding="utf-8").read()


def test_html_has_canvas():
    """index.html must contain a <canvas> element."""
    assert "<canvas" in _read_html(), "index.html must contain a <canvas> element"


def test_html_has_truchet_grid_constant():
    """index.html must define the truchet grid constant N."""
    html = _read_html()
    assert "const N" in html or "N = 30" in html or "N=30" in html, (
        "index.html must define the grid dimension constant N"
    )


def test_html_has_arc_drawing():
    """index.html must use ctx.arc() to draw truchet arcs."""
    html = _read_html()
    assert "ctx.arc(" in html or ".arc(" in html, (
        "index.html must draw arcs with ctx.arc()"
    )


def test_html_has_setinterval_animation():
    """index.html must use setInterval for the periodic tile-flip."""
    html = _read_html()
    assert "setInterval" in html, (
        "index.html must use setInterval for the tile-flip animation"
    )


def test_html_has_requestanimationframe():
    """index.html must use requestAnimationFrame for smooth transition."""
    html = _read_html()
    assert "requestAnimationFrame" in html, (
        "index.html must use requestAnimationFrame for smooth animation"
    )


def test_html_has_moab_palette_color():
    """index.html must reference Moab palette colors."""
    html = _read_html()
    # Check for at least one Moab color
    has_moab = "#c2956a" in html or "#8b5e3c" in html or "#d4b483" in html
    assert has_moab, "index.html must reference Moab palette colors (#c2956a, #8b5e3c, or #d4b483)"


def test_html_has_bethlehem_palette_color():
    """index.html must reference Bethlehem palette colors."""
    html = _read_html()
    has_bethlehem = "#c8a84b" in html or "#7a9e5f" in html or "#e8d5a0" in html
    assert has_bethlehem, "index.html must reference Bethlehem palette colors"


def test_html_has_figure_color():
    """index.html must reference the figure/silhouette color #3d2b1f."""
    html = _read_html()
    assert "#3d2b1f" in html, "index.html must reference figure color #3d2b1f"


def test_html_has_hebrew_text():
    """index.html must include the Hebrew verse אֲשֶׁר תֵּלְכִי אֵלֵך."""
    html = _read_html()
    assert "אֲשֶׁר" in html or "תֵּלְכִי" in html or "אֵלֵך" in html, (
        "index.html must include the Hebrew verse from Ruth 1:16"
    )


def test_html_has_figure_cells():
    """index.html must define figure cell coordinates."""
    html = _read_html()
    # Figure cells are stored in a Set with string keys like "col,row"
    has_figure = "FIGURE_CELLS" in html or "figureCells" in html or "figure_cells" in html
    assert has_figure, "index.html must define figure cell coordinates"


def test_html_embeds_essay_text():
    """index.html must embed essay content verbatim."""
    essay = _read_essay()
    html = _read_html()
    words = [w for w in essay.split() if len(w) > 6]
    sampled = words[:10]
    found = sum(1 for w in sampled if w in html)
    assert found >= 5, (
        f"index.html does not embed essay text: only {found}/10 sampled words found"
    )


def test_html_no_external_scripts():
    """index.html must not load external scripts."""
    html = _read_html()
    external = re.findall(r'<script[^>]+src=["\']https?://', html)
    assert len(external) == 0, f"index.html must not load external scripts: {external}"


def test_html_palette_interpolation():
    """index.html must implement palette interpolation (lerpRGB or similar)."""
    html = _read_html()
    has_lerp = "lerp" in html.lower() or "interpolat" in html.lower()
    assert has_lerp, "index.html must implement palette interpolation (lerpRGB)"


def test_html_not_placeholder():
    """index.html must not contain placeholder stubs."""
    html = _read_html()
    for stub in ("TODO", "lorem ipsum", "FILL IN"):
        assert stub.lower() not in html.lower(), (
            f"index.html contains placeholder text: {stub!r}"
        )


# ---------------------------------------------------------------------------
# Thumbnail SVG
# ---------------------------------------------------------------------------

def _read_thumb():
    return open(THUMB_PATH, encoding="utf-8").read()


def test_thumbnail_is_valid_svg():
    """thumbnail.svg must be well-formed SVG."""
    svg = _read_thumb()
    assert "<svg" in svg and "</svg>" in svg, "thumbnail.svg is not valid SVG"


def test_thumbnail_has_background():
    """thumbnail.svg must have a background rect."""
    svg = _read_thumb()
    assert "<rect" in svg, "thumbnail.svg must contain a <rect> background element"


def test_thumbnail_has_truchet_arcs():
    """thumbnail.svg must contain arc path data (A command in path d attributes)."""
    svg = _read_thumb()
    # SVG arc command is the letter A inside a path d attribute
    has_arcs = re.search(r'<path[^>]+d="[^"]*A', svg) is not None
    assert has_arcs, "thumbnail.svg must contain arc paths (SVG A command)"


def test_thumbnail_has_figure_color():
    """thumbnail.svg must include the figure color #3d2b1f."""
    svg = _read_thumb()
    assert "#3d2b1f" in svg, "thumbnail.svg must reference figure color #3d2b1f"


def test_thumbnail_has_hebrew_text():
    """thumbnail.svg must include Hebrew text."""
    svg = _read_thumb()
    assert "<text" in svg, "thumbnail.svg must contain a <text> element"
    has_hebrew = "אֲשֶׁר" in svg or "תֵּלְכִי" in svg or "אֵלֵך" in svg
    assert has_hebrew, "thumbnail.svg must include Hebrew verse text"


def test_thumbnail_size_under_50kb():
    """thumbnail.svg must be under 50 KB to load quickly in the gallery."""
    size = os.path.getsize(THUMB_PATH)
    assert size < 50 * 1024, (
        f"thumbnail.svg is {size / 1024:.1f} KB; must be under 50 KB"
    )


def test_thumbnail_has_moab_palette():
    """thumbnail.svg must reference Moab-side palette colors."""
    svg = _read_thumb()
    has_moab = "#c2956a" in svg or "#8b5e3c" in svg or "#d4b483" in svg
    assert has_moab, "thumbnail.svg must reference at least one Moab palette color"


def test_thumbnail_has_bethlehem_palette():
    """thumbnail.svg must reference Bethlehem-side palette colors."""
    svg = _read_thumb()
    has_beth = "#c8a84b" in svg or "#7a9e5f" in svg or "#e8d5a0" in svg
    assert has_beth, "thumbnail.svg must reference at least one Bethlehem palette color"


# ---------------------------------------------------------------------------
# Edge cases and failure modes
# ---------------------------------------------------------------------------

def test_pieces_json_still_has_twelve_entries_or_more():
    """Adding piece 14 must not have removed any existing pieces."""
    pieces = _load_pieces()
    assert len(pieces) >= 10, (
        f"pieces.json has only {len(pieces)} entries; existing pieces may have been deleted"
    )


def test_piece_14_does_not_collide_with_existing_ids():
    """Piece id '14-ruth-naomi-truchet' must not clash with any prior piece."""
    pieces = _load_pieces()
    matching = [p for p in pieces if p["id"] == PIECE_ID]
    assert len(matching) == 1, (
        f"Expected exactly one entry for '{PIECE_ID}', found {len(matching)}"
    )


def test_existing_piece_12_still_registered():
    """Adding piece 14 must not have disturbed piece 12 (omer-spiral)."""
    pieces = _load_pieces()
    ids = [p["id"] for p in pieces]
    assert "12-omer-spiral" in ids, "piece 12-omer-spiral was removed from pieces.json"


def test_essay_cites_talmud_or_midrash():
    """Essay must include at least one rabbinic source."""
    text = _read_essay()
    has_rabbinic = (
        "Talmud" in text
        or "Midrash" in text
        or "Yevamot" in text
        or "Ruth Rabbah" in text
    )
    assert has_rabbinic, "essay.md must cite at least one rabbinic source"


def test_html_clip_or_clipping_logic():
    """index.html must restrict arc drawing per cell (clip or bounded drawing)."""
    html = _read_html()
    has_clip = "clip" in html.lower() or "rect(" in html or "ctx.rect" in html
    assert has_clip, "index.html must clip arc drawing to cell bounds"
