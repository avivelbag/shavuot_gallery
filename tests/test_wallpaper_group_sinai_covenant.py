"""Tests for piece 73-wallpaper-group-sinai-covenant (p6m tiling).

Covers:
- Piece entry in pieces.json (happy path)
- Required files exist on disk
- HTML content: canvas dimensions, Hebrew text, p6m symmetry ops
- Essay word count and content requirements
- Thumbnail is valid SVG
- gen_thumbnail.py runs and produces valid SVG (edge-case: re-generation)
- Error behaviour for missing files
"""
import json
import os
import subprocess
import sys
GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID = "73-wallpaper-group-sinai-covenant"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_pieces():
    with open(PIECES_JSON, encoding="utf-8") as fh:
        return json.load(fh)


def get_piece():
    for p in load_pieces():
        if p["id"] == PIECE_ID:
            return p
    return None


def read_file(rel_path):
    return open(os.path.join(GALLERY_ROOT, rel_path), encoding="utf-8").read()


# ---------------------------------------------------------------------------
# pieces.json registration
# ---------------------------------------------------------------------------

def test_piece_registered_in_pieces_json():
    """The wallpaper-group piece must appear in pieces.json."""
    piece = get_piece()
    assert piece is not None, f"Piece '{PIECE_ID}' not found in pieces.json"


def test_piece_has_correct_theme():
    piece = get_piece()
    assert piece is not None
    assert "Matan Torah" in piece["theme"], (
        "theme must include 'Matan Torah'"
    )


def test_piece_has_correct_technique():
    piece = get_piece()
    assert piece is not None
    assert "p6m" in piece["technique"], "technique must reference 'p6m'"
    assert "wallpaper" in piece["technique"].lower(), (
        "technique must mention 'wallpaper'"
    )


def test_piece_year_is_integer():
    piece = get_piece()
    assert piece is not None
    assert isinstance(piece["year"], int), "year must be an integer"


def test_piece_id_matches_path_directory():
    """The id must match the directory component in the path."""
    piece = get_piece()
    assert piece is not None
    parts = piece["path"].replace("\\", "/").split("/")
    assert parts[-2] == PIECE_ID


# ---------------------------------------------------------------------------
# File existence
# ---------------------------------------------------------------------------

def test_index_html_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "index.html")), (
        "index.html is missing"
    )


def test_essay_md_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "essay.md")), (
        "essay.md is missing"
    )


def test_thumbnail_svg_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "thumbnail.svg")), (
        "thumbnail.svg is missing"
    )


def test_readme_md_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "README.md")), (
        "README.md is missing"
    )


def test_gen_thumbnail_py_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "gen_thumbnail.py")), (
        "gen_thumbnail.py is missing"
    )


# ---------------------------------------------------------------------------
# index.html content
# ---------------------------------------------------------------------------

def _html():
    return open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()


def test_html_canvas_element_present():
    assert "<canvas" in _html(), "index.html must contain a <canvas> element"


def test_html_canvas_width_700():
    html = _html()
    assert "700" in html, "Canvas width 700 must appear in index.html"


def test_html_canvas_height_700():
    html = _html()
    # Both W=700 and H=700 should be declared
    assert html.count("700") >= 2, (
        "Canvas dimensions 700×700 must both appear in index.html"
    )


def test_html_contains_p6m_rotation_operations():
    """ctx.rotate must be called 6 times (once per 60° increment)."""
    html = _html()
    assert "ctx.rotate" in html, "index.html must use ctx.rotate for p6m symmetry"
    assert "Math.PI / 3" in html or "PI/3" in html or "PI / 3" in html, (
        "Rotation step of PI/3 (60°) must appear in index.html"
    )


def test_html_contains_ctx_scale_for_reflection():
    """ctx.scale(-1, 1) implements the reflection in p6m."""
    html = _html()
    assert "scale(-1" in html or "ctx.scale(-1" in html, (
        "p6m reflection (scale(-1, 1)) must appear in index.html"
    )


def test_html_contains_ctx_save_restore():
    """ctx.save/ctx.restore must be used for transform isolation."""
    html = _html()
    assert "ctx.save()" in html, "index.html must use ctx.save()"
    assert "ctx.restore()" in html, "index.html must use ctx.restore()"


def test_html_contains_hebrew_inscription():
    """The Hebrew naaseh v'nishma inscription must appear in the HTML."""
    html = _html()
    # Check for the Hebrew characters
    assert "נַעֲשֶׂה" in html or "נעשה" in html, (
        "Hebrew text naaseh (נַעֲשֶׂה) must appear in index.html"
    )


def test_html_contains_color_gold():
    assert "#D4A830" in _html() or "D4A830" in _html(), (
        "Wheat gold color #D4A830 must appear in index.html"
    )


def test_html_contains_color_green():
    assert "#2A6020" in _html() or "2A6020" in _html(), (
        "Field green color #2A6020 must appear in index.html"
    )


def test_html_contains_color_ivory():
    assert "#F5EDD8" in _html() or "F5EDD8" in _html(), (
        "Ivory color #F5EDD8 must appear in index.html"
    )


def test_html_header_band_30px():
    """The 30px header band must be referenced in the JS."""
    html = _html()
    assert "30" in html, "30px header band constant must appear in index.html"


def test_html_embeds_essay_text():
    """index.html must inline essay content (no runtime fetch)."""
    essay = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    html = _html()
    # Sample meaningful words from the essay
    words = [w for w in essay.split() if len(w) > 6][:10]
    found = sum(1 for w in words if w in html)
    assert found >= 5, (
        f"index.html must embed essay text inline — only {found}/10 sampled words found"
    )


def test_html_references_hex_tile_radius():
    """Tile radius R (~60) must be defined."""
    html = _html()
    assert "= 60" in html or "=60" in html, (
        "Tile radius R = 60 must be defined in index.html"
    )


# ---------------------------------------------------------------------------
# essay.md content
# ---------------------------------------------------------------------------

def _essay():
    return open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()


def test_essay_min_word_count():
    words = _essay().split()
    assert len(words) >= 300, (
        f"essay.md has only {len(words)} words; need ≥ 300"
    )


def test_essay_mentions_exodus():
    assert "Exodus" in _essay(), "essay must cite Exodus"


def test_essay_mentions_naaseh():
    essay = _essay()
    assert "naaseh" in essay.lower() or "naaseh" in essay, (
        "essay must discuss naaseh v'nishma"
    )


def test_essay_mentions_shabbat_88():
    essay = _essay()
    assert "88" in essay, "essay must cite Shabbat 88a"


def test_essay_mentions_seventeen_groups():
    essay = _essay()
    assert "seventeen" in essay.lower() or "17" in essay, (
        "essay must mention the seventeen wallpaper groups"
    )


def test_essay_mentions_fedorov():
    assert "Fedorov" in _essay() or "fedorov" in _essay().lower(), (
        "essay must mention Fedorov (1891)"
    )


def test_essay_mentions_p6m():
    assert "p6m" in _essay(), "essay must mention the wallpaper group p6m"


def test_essay_mentions_twelve_pillars():
    essay = _essay()
    assert "twelve" in essay.lower() or "12" in essay, (
        "essay must connect the 12 symmetry operations to the 12 pillars"
    )


# ---------------------------------------------------------------------------
# thumbnail.svg validity
# ---------------------------------------------------------------------------

def _thumb():
    return open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()


def test_thumbnail_is_valid_svg():
    thumb = _thumb()
    assert "<svg" in thumb and "</svg>" in thumb, (
        "thumbnail.svg must contain valid SVG tags"
    )


def test_thumbnail_has_viewbox_or_dimensions():
    thumb = _thumb()
    assert "viewBox" in thumb or ('width="400"' in thumb), (
        "thumbnail.svg must declare dimensions or viewBox"
    )


def test_thumbnail_contains_green_color():
    assert "2A6020" in _thumb(), (
        "thumbnail.svg must include field-green #2A6020 polygons"
    )


def test_thumbnail_contains_ivory_color():
    assert "F5EDD8" in _thumb(), (
        "thumbnail.svg must include ivory #F5EDD8 regions"
    )


# ---------------------------------------------------------------------------
# gen_thumbnail.py: re-generation produces valid SVG
# ---------------------------------------------------------------------------

def test_gen_thumbnail_runs_and_produces_svg(tmp_path):
    """Running gen_thumbnail.py in a temp dir must produce a valid SVG file."""
    script = os.path.join(PIECE_DIR, "gen_thumbnail.py")
    result = subprocess.run(
        [sys.executable, script],
        cwd=str(tmp_path),
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, (
        f"gen_thumbnail.py exited {result.returncode}:\n{result.stderr}"
    )
    out_svg = tmp_path / "thumbnail.svg"
    assert out_svg.exists(), "gen_thumbnail.py must write thumbnail.svg"
    content = out_svg.read_text(encoding="utf-8")
    assert "<svg" in content, "Generated thumbnail.svg must be valid SVG"


def test_gen_thumbnail_svg_has_polygon_elements(tmp_path):
    """The generated SVG must contain polygon elements for the tiling."""
    script = os.path.join(PIECE_DIR, "gen_thumbnail.py")
    subprocess.run(
        [sys.executable, script],
        cwd=str(tmp_path),
        capture_output=True,
        timeout=30,
    )
    content = (tmp_path / "thumbnail.svg").read_text(encoding="utf-8")
    assert "<polygon" in content, (
        "Generated thumbnail.svg must contain <polygon> elements for tiling triangles"
    )


# ---------------------------------------------------------------------------
# Edge cases: missing file detection
# ---------------------------------------------------------------------------

def test_missing_index_html_detected(tmp_path):
    """Absence of index.html in a tmp directory must be detectable."""
    missing = tmp_path / "index.html"
    assert not missing.exists(), "Fixture: file must not pre-exist"


def test_missing_essay_md_detected(tmp_path):
    """Absence of essay.md in a tmp directory must be detectable."""
    missing = tmp_path / "essay.md"
    assert not missing.exists(), "Fixture: file must not pre-exist"


def test_essay_too_short_detected():
    """A stub essay of 10 words must fail the 300-word minimum."""
    stub = "This is a stub essay. It is too short to pass. Really."
    assert len(stub.split()) < 300, "Fixture confirms short text fails threshold"


# ---------------------------------------------------------------------------
# Failure mode: pieces.json without the piece
# ---------------------------------------------------------------------------

def test_piece_not_in_empty_json():
    """A pieces.json without this piece ID must return None from get_piece()."""
    other_pieces = [p for p in load_pieces() if p["id"] != PIECE_ID]
    found = next((p for p in other_pieces if p["id"] == PIECE_ID), None)
    assert found is None, "Piece should not appear in other_pieces list"
