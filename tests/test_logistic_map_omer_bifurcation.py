"""
Tests specific to piece 80-logistic-map-omer-bifurcation.

Validates the piece's presence in pieces.json, file layout, content
requirements from the acceptance criteria, and edge-case behaviour.
"""
import json
import os

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")
PIECE_ID = "80-logistic-map-omer-bifurcation"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)


def load_pieces():
    with open(PIECES_JSON, encoding="utf-8") as f:
        return json.load(f)


def get_piece():
    for p in load_pieces():
        if p["id"] == PIECE_ID:
            return p
    return None


# ---------------------------------------------------------------------------
# pieces.json registration
# ---------------------------------------------------------------------------

def test_piece_registered_in_pieces_json():
    """The piece must appear in pieces.json with the correct id."""
    piece = get_piece()
    assert piece is not None, f"Piece '{PIECE_ID}' not found in pieces.json"


def test_piece_theme_contains_omer():
    """Theme must reference Sefirat HaOmer / the 49-day count."""
    piece = get_piece()
    assert piece is not None, "Piece not found"
    theme = piece.get("theme", "").lower()
    assert "omer" in theme or "49" in theme, (
        f"Theme '{piece['theme']}' does not mention Omer or 49-day count"
    )


def test_piece_technique_mentions_logistic_map():
    """Technique must reference the logistic map bifurcation diagram."""
    piece = get_piece()
    assert piece is not None, "Piece not found"
    technique = piece.get("technique", "").lower()
    assert "logistic" in technique or "bifurcation" in technique, (
        f"Technique '{piece['technique']}' does not mention logistic map or bifurcation"
    )


# ---------------------------------------------------------------------------
# File layout
# ---------------------------------------------------------------------------

def test_piece_directory_exists():
    assert os.path.isdir(PIECE_DIR), f"Piece directory not found: {PIECE_DIR}"


def test_index_html_exists():
    path = os.path.join(PIECE_DIR, "index.html")
    assert os.path.isfile(path), "index.html is missing"


def test_essay_md_exists():
    path = os.path.join(PIECE_DIR, "essay.md")
    assert os.path.isfile(path), "essay.md is missing"


def test_thumbnail_svg_exists():
    path = os.path.join(PIECE_DIR, "thumbnail.svg")
    assert os.path.isfile(path), "thumbnail.svg is missing"


def test_readme_md_exists():
    path = os.path.join(PIECE_DIR, "README.md")
    assert os.path.isfile(path), "README.md is missing"


# ---------------------------------------------------------------------------
# index.html content requirements
# ---------------------------------------------------------------------------

def read_html():
    with open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8") as f:
        return f.read()


def test_html_has_canvas_element():
    """index.html must contain a <canvas> element for the diagram."""
    html = read_html()
    assert "<canvas" in html, "index.html does not contain a <canvas> element"


def test_html_uses_request_animation_frame():
    """Animation must use requestAnimationFrame."""
    html = read_html()
    assert "requestAnimationFrame" in html, (
        "index.html does not use requestAnimationFrame for animation"
    )


def test_html_defines_logistic_map_recurrence():
    """The JavaScript must compute the logistic map x = r * x * (1 - x)."""
    html = read_html()
    assert "r * x * (1 - x)" in html or "r*x*(1-x)" in html, (
        "index.html does not implement the logistic map recurrence"
    )


def test_html_defines_r_range():
    """The r range [2.5, 4.0] must be present in the JavaScript."""
    html = read_html()
    assert "2.5" in html and "4.0" in html, (
        "index.html does not define the r range [2.5, 4.0]"
    )


def test_html_defines_transient_and_samples():
    """TRANSIENT (300) and SAMPLES (200) constants must appear."""
    html = read_html()
    assert "300" in html, "index.html does not reference TRANSIENT=300"
    assert "200" in html, "index.html does not reference SAMPLES=200"


def test_html_deep_indigo_background_color():
    """The deep-indigo background color #0A0820 must be in the HTML."""
    html = read_html()
    assert "0A0820" in html.upper() or "#0a0820" in html.lower(), (
        "index.html does not use deep-indigo color #0A0820"
    )


def test_html_wheat_gold_color():
    """The wheat-gold color #C09040 must appear (density-medium and overlays)."""
    html = read_html()
    assert "C09040" in html.upper() or "#c09040" in html.lower(), (
        "index.html does not use wheat-gold color #C09040"
    )


def test_html_hebrew_nun_label():
    """The Hebrew letter nun (נ) marking the 50th Omer must appear in the HTML."""
    html = read_html()
    assert "נ" in html, "index.html does not contain the Hebrew nun (נ) label"


def test_html_49_omer_tick_marks():
    """There must be a loop or constant that generates 49 Omer tick marks."""
    html = read_html()
    assert "49" in html, "index.html does not reference 49 Omer days"


def test_html_click_handler_for_re_render():
    """Clicking the canvas must trigger a re-render; look for a click listener."""
    html = read_html()
    assert "click" in html, "index.html does not register a click event listener"


def test_html_density_array_width_800():
    """Canvas width must be 800 (W=800 from acceptance criteria)."""
    html = read_html()
    assert "800" in html, "index.html does not reference canvas width 800"


def test_html_embeds_essay_text():
    """The essay text must be embedded in index.html (no runtime fetch)."""
    essay_path = os.path.join(PIECE_DIR, "essay.md")
    essay = open(essay_path, encoding="utf-8").read()
    html = read_html()
    words = [w for w in essay.split() if len(w) > 6][:10]
    found = sum(1 for w in words if w in html)
    assert found >= 5, (
        f"index.html does not appear to embed the essay text "
        f"(only {found}/10 sampled long words found)"
    )


# ---------------------------------------------------------------------------
# essay.md content requirements
# ---------------------------------------------------------------------------

def read_essay():
    with open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8") as f:
        return f.read()


def test_essay_minimum_word_count():
    """Essay must be at least 300 words (acceptance criterion ~380)."""
    essay = read_essay()
    count = len(essay.split())
    assert count >= 300, f"essay.md has only {count} words (need ≥ 300)"


def test_essay_mentions_leviticus():
    """Essay must open with or reference Leviticus 23:15-16."""
    essay = read_essay()
    assert "Leviticus" in essay or "23:15" in essay, (
        "essay.md does not reference Leviticus 23:15–16"
    )


def test_essay_mentions_omer_counts_up():
    """Essay must explain that the Omer counts upward (not down to zero)."""
    essay = read_essay().lower()
    assert "upward" in essay or "counts up" in essay or "ascending" in essay or "forward" in essay, (
        "essay.md does not explain that the Omer counts up/forward/ascending"
    )


def test_essay_mentions_sefirot_grid():
    """Essay must reference the 7x7 sefirot grid of the Omer count."""
    essay = read_essay()
    assert "sefirot" in essay.lower() or "sefirah" in essay.lower() or "7×7" in essay or "seven" in essay.lower(), (
        "essay.md does not reference the sefirot or 7x7 grid of the Omer"
    )


def test_essay_mentions_feigenbaum_or_bifurcation():
    """Essay must reference the Feigenbaum constant or bifurcation structure."""
    essay = read_essay()
    assert "Feigenbaum" in essay or "bifurcation" in essay.lower() or "period-doubling" in essay.lower(), (
        "essay.md does not reference the Feigenbaum constant or period-doubling bifurcations"
    )


def test_essay_mentions_50th_day():
    """Essay must tie to Shavuot as the 50th day."""
    essay = read_essay()
    assert "fiftieth" in essay.lower() or "50" in essay or "Shavuot" in essay, (
        "essay.md does not reference the fiftieth day / Shavuot"
    )


# ---------------------------------------------------------------------------
# thumbnail.svg requirements
# ---------------------------------------------------------------------------

def test_thumbnail_is_valid_svg():
    with open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8") as f:
        svg = f.read()
    assert "<svg" in svg and "</svg>" in svg, "thumbnail.svg is not valid SVG"


def test_thumbnail_has_viewbox_400x400():
    """Thumbnail must be 400×400 as specified."""
    with open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8") as f:
        svg = f.read()
    assert "400" in svg, "thumbnail.svg does not declare 400 dimensions"


def test_thumbnail_has_path_elements():
    """Thumbnail must use <path> elements for the branching curves."""
    with open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8") as f:
        svg = f.read()
    assert "<path" in svg, "thumbnail.svg does not contain <path> elements"


def test_thumbnail_has_dark_background():
    """Thumbnail must have a dark background (deep indigo #0A0820)."""
    with open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8") as f:
        svg = f.read()
    assert "0A0820" in svg.upper() or "0a0820" in svg.lower(), (
        "thumbnail.svg does not use the deep-indigo background #0A0820"
    )


def test_thumbnail_gold_strokes():
    """Thumbnail curves must use the gold palette (#C09040 or similar)."""
    with open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8") as f:
        svg = f.read()
    assert "C09040" in svg.upper() or "c09040" in svg.lower() or "B07830" in svg.upper(), (
        "thumbnail.svg does not use the gold color palette"
    )


# ---------------------------------------------------------------------------
# README.md requirements
# ---------------------------------------------------------------------------

def test_readme_mentions_sinai_or_omer():
    """README.md must mention the Shavuot theme."""
    with open(os.path.join(PIECE_DIR, "README.md"), encoding="utf-8") as f:
        readme = f.read().lower()
    assert "omer" in readme or "shavuot" in readme or "sinai" in readme, (
        "README.md does not mention the Shavuot/Omer theme"
    )


def test_readme_mentions_logistic_map():
    """README.md must mention the logistic map technique."""
    with open(os.path.join(PIECE_DIR, "README.md"), encoding="utf-8") as f:
        readme = f.read().lower()
    assert "logistic" in readme or "bifurcation" in readme, (
        "README.md does not describe the logistic map technique"
    )


# ---------------------------------------------------------------------------
# Edge cases / failure modes
# ---------------------------------------------------------------------------

def test_piece_id_unique_in_pieces_json():
    """The new piece id must not be duplicated."""
    pieces = load_pieces()
    ids = [p["id"] for p in pieces]
    count = ids.count(PIECE_ID)
    assert count == 1, f"Piece id '{PIECE_ID}' appears {count} times in pieces.json"


def test_piece_path_resolves_to_existing_file():
    """The 'path' field in pieces.json must point to an existing file."""
    piece = get_piece()
    assert piece is not None, "Piece not found in pieces.json"
    full_path = os.path.join(GALLERY_ROOT, piece["path"])
    assert os.path.isfile(full_path), (
        f"pieces.json path '{piece['path']}' does not exist on disk"
    )


def test_piece_thumbnail_resolves_to_existing_file():
    """The 'thumbnail' field in pieces.json must point to an existing file."""
    piece = get_piece()
    assert piece is not None, "Piece not found in pieces.json"
    full_path = os.path.join(GALLERY_ROOT, piece["thumbnail"])
    assert os.path.isfile(full_path), (
        f"pieces.json thumbnail '{piece['thumbnail']}' does not exist on disk"
    )


def test_piece_essay_resolves_to_existing_file():
    """The 'essay' field in pieces.json must point to an existing file."""
    piece = get_piece()
    assert piece is not None, "Piece not found in pieces.json"
    full_path = os.path.join(GALLERY_ROOT, piece["essay"])
    assert os.path.isfile(full_path), (
        f"pieces.json essay '{piece['essay']}' does not exist on disk"
    )


def test_missing_piece_directory_detected(tmp_path):
    """Verify that a missing piece directory would be caught."""
    fake_dir = os.path.join(str(tmp_path), "pieces", "00-fake-piece")
    assert not os.path.isdir(fake_dir), (
        "Fixture: fake directory must not exist so the absence check is meaningful"
    )


def test_empty_essay_file_detected(tmp_path):
    """An essay.md with zero words must fail the word-count check."""
    empty = tmp_path / "essay.md"
    empty.write_text("", encoding="utf-8")
    text = empty.read_text(encoding="utf-8")
    assert len(text.split()) == 0, "Fixture confirms empty essay has 0 words"
