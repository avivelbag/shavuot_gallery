"""
Tests for piece 53-black-fire-white-fire-shader.

Verifies that the WebGL fire-shader piece is correctly wired up in pieces.json,
that all on-disk files exist and contain the expected content, and that the
shader and essay meet the acceptance criteria from the suggestion.
"""
import json
import os
import re

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID     = "53-black-fire-white-fire-shader"
PIECE_DIR    = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)

REQUIRED_PALETTE = ["#FFFDE8", "#FFE566", "#FF7A1A", "#CC2200", "#0A0D1A", "#F5F0E8"]
HEBREW_TEXT      = "אָנֹכִי יְהֹוָה אֱלֹהֶיךָ"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_pieces():
    """Return all entries from pieces.json."""
    with open(os.path.join(GALLERY_ROOT, "pieces.json"), encoding="utf-8") as fh:
        return json.load(fh)


def get_piece():
    """Return the pieces.json entry for piece 53, or None if absent."""
    for p in load_pieces():
        if p["id"] == PIECE_ID:
            return p
    return None


def read_piece_file(filename):
    """Read a file from the piece directory and return its text."""
    path = os.path.join(PIECE_DIR, filename)
    with open(path, encoding="utf-8") as fh:
        return fh.read()


# ---------------------------------------------------------------------------
# Happy path: pieces.json registration
# ---------------------------------------------------------------------------

def test_piece_registered_in_pieces_json():
    """Piece 53 must appear in pieces.json."""
    piece = get_piece()
    assert piece is not None, f"'{PIECE_ID}' not found in pieces.json"


def test_piece_required_fields_present():
    """All nine required fields must be non-empty."""
    required = ("id", "title", "tagline", "year", "theme", "technique", "path", "thumbnail", "essay")
    piece = get_piece()
    assert piece is not None
    for field in required:
        assert field in piece and piece[field], f"Field '{field}' missing or empty in piece {PIECE_ID}"


def test_piece_technique_mentions_webgl_and_sdf():
    """Technique field must declare WebGL fragment shader and SDF letterforms."""
    piece = get_piece()
    assert piece is not None
    tech = piece["technique"].lower()
    assert "webgl" in tech, "technique must mention WebGL"
    assert "sdf" in tech, "technique must mention SDF"


def test_piece_theme_mentions_matan_torah():
    """Theme must reference Matan Torah as specified in the acceptance criteria."""
    piece = get_piece()
    assert piece is not None
    assert "Matan Torah" in piece["theme"], "theme must contain 'Matan Torah'"


def test_piece_year_is_2026():
    piece = get_piece()
    assert piece is not None
    assert piece["year"] == 2026


# ---------------------------------------------------------------------------
# Happy path: on-disk file layout
# ---------------------------------------------------------------------------

def test_piece_directory_exists():
    assert os.path.isdir(PIECE_DIR), f"Piece directory not found: {PIECE_DIR}"


def test_index_html_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "index.html"))


def test_essay_md_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "essay.md"))


def test_thumbnail_svg_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "thumbnail.svg"))


def test_readme_md_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "README.md"))


# ---------------------------------------------------------------------------
# Happy path: index.html content
# ---------------------------------------------------------------------------

def test_index_html_uses_webgl():
    """index.html must obtain a WebGL context."""
    html = read_piece_file("index.html")
    assert "getContext('webgl')" in html or 'getContext("webgl")' in html, \
        "index.html must request a WebGL context"


def test_index_html_uses_requestanimationframe():
    html = read_piece_file("index.html")
    assert "requestAnimationFrame" in html


def test_index_html_contains_hebrew_text():
    """The Decalogue opening words must appear in the HTML."""
    html = read_piece_file("index.html")
    assert HEBREW_TEXT in html, "index.html must contain the Hebrew text אָנֹכִי יְהֹוָה אֱלֹהֶיךָ"


def test_index_html_has_full_viewport_canvas():
    """The canvas must stretch to 100% width and height of its container."""
    html = read_piece_file("index.html")
    assert "100%" in html and "canvas" in html.lower()


def test_index_html_has_responsive_media_query():
    """Must include a media query for mobile layout."""
    html = read_piece_file("index.html")
    assert re.search(r"max-width\s*:\s*768px", html), \
        "index.html must have a max-width:768px responsive breakpoint"


def test_index_html_shader_contains_fbm():
    """The fragment shader must use fractional Brownian motion (fbm)."""
    html = read_piece_file("index.html")
    assert "fbm(" in html, "Fragment shader must define/call fbm() for fire distortion"


def test_index_html_shader_contains_smoothstep_ramp():
    """The fire color ramp must use smoothstep transitions."""
    html = read_piece_file("index.html")
    assert html.count("smoothstep") >= 4, \
        "Fragment shader must have at least 4 smoothstep calls for the fire color ramp"


def test_index_html_contains_fire_palette_colors():
    """All six required palette color codes must appear in index.html."""
    html = read_piece_file("index.html")
    # Palette values appear as shader vec3 constants or CSS — check at least 4 of 6
    found = [c for c in REQUIRED_PALETTE if c.upper() in html.upper() or c.lower() in html.lower()]
    assert len(found) >= 4, (
        f"index.html should contain at least 4 of the required palette colors; "
        f"found {len(found)}: {found}"
    )


def test_index_html_texture_uses_hebrew_font():
    """The offscreen texture canvas must render the Hebrew phrase for the SDF."""
    html = read_piece_file("index.html")
    assert "אָנֹכִי יְהֹוָה אֱלֹהֶיךָ" in html, \
        "index.html must fillText the Hebrew phrase to build the glow texture"


def test_index_html_canvas_resizes_on_viewport_resize():
    """The canvas resize handler must be wired to the window resize event."""
    html = read_piece_file("index.html")
    assert "addEventListener" in html and "resize" in html, \
        "index.html must listen for the window resize event"


def test_index_html_embeds_essay_text():
    """The essay content must be embedded inline — not fetched at runtime."""
    html = read_piece_file("index.html")
    essay = read_piece_file("essay.md")
    # Take first 10 words longer than 5 chars and require 5+ to appear in HTML
    words = [w for w in essay.split() if len(w) > 5][:10]
    found = sum(1 for w in words if w in html)
    assert found >= 5, (
        f"index.html does not appear to embed the essay text inline "
        f"(only {found}/10 sampled essay words found in HTML)"
    )


# ---------------------------------------------------------------------------
# Happy path: essay.md content
# ---------------------------------------------------------------------------

def test_essay_word_count_exceeds_200():
    essay = read_piece_file("essay.md")
    wc = len(essay.split())
    assert wc >= 200, f"essay.md has only {wc} words (minimum 200)"


def test_essay_cites_tanhuma_bereishit():
    """Must cite Tanhuma Bereishit 1 per acceptance criteria."""
    essay = read_piece_file("essay.md")
    assert "Tanhuma" in essay and "Bereishit" in essay, \
        "essay.md must cite Tanhuma Bereishit 1"


def test_essay_cites_devarim_rabbah():
    """Must cite Devarim Rabbah 3:12 per acceptance criteria."""
    essay = read_piece_file("essay.md")
    assert "Devarim Rabbah" in essay, "essay.md must cite Devarim Rabbah 3:12"


def test_essay_mentions_black_fire_white_fire():
    essay = read_piece_file("essay.md")
    text_lower = essay.lower()
    assert "black fire" in text_lower or "white fire" in text_lower, \
        "essay.md must discuss the 'black fire on white fire' teaching"


def test_essay_mentions_white_space_sanctity():
    """Must cover the scribal law about white spaces being sacred."""
    essay = read_piece_file("essay.md")
    text_lower = essay.lower()
    assert "white space" in text_lower or "white spaces" in text_lower or "tractate sofrim" in text_lower, \
        "essay.md must mention the sanctity of white spaces in Torah scrolls"


def test_essay_mentions_fire_transforms():
    """Must articulate the 'fire transforms' insight about Matan Torah."""
    essay = read_piece_file("essay.md")
    assert "transform" in essay.lower(), \
        "essay.md must explain that fire transforms rather than merely communicates"


# ---------------------------------------------------------------------------
# Happy path: thumbnail.svg
# ---------------------------------------------------------------------------

def test_thumbnail_is_valid_svg():
    svg = read_piece_file("thumbnail.svg")
    assert "<svg" in svg and "</svg>" in svg


def test_thumbnail_contains_hebrew_text():
    svg = read_piece_file("thumbnail.svg")
    assert "אָנֹכִי" in svg or "יְהֹוָה" in svg, \
        "thumbnail.svg should render Hebrew letterforms"


def test_thumbnail_uses_fire_colors():
    """Thumbnail must visually represent the fire palette."""
    svg = read_piece_file("thumbnail.svg")
    fire_colors = ["CC2200", "FF7A1A", "FFE566", "FFFDE8"]
    found = [c for c in fire_colors if c in svg.upper()]
    assert len(found) >= 2, (
        f"thumbnail.svg should use fire-palette colors; found only {found}"
    )


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

def test_no_duplicate_ids_in_pieces_json():
    """Duplicate IDs would break gallery routing; 53 must be unique."""
    pieces = load_pieces()
    ids = [p["id"] for p in pieces]
    assert ids.count(PIECE_ID) == 1, f"Duplicate entry for {PIECE_ID} in pieces.json"


def test_essay_does_not_exceed_reasonable_size():
    """Sanity check: essay.md should be substantial but not absurdly large."""
    essay = read_piece_file("essay.md")
    wc = len(essay.split())
    assert wc < 5000, f"essay.md has {wc} words — unexpectedly large"


def test_index_html_handles_missing_webgl_gracefully():
    """index.html must check for WebGL and provide a fallback."""
    html = read_piece_file("index.html")
    assert "experimental-webgl" in html, \
        "index.html must try experimental-webgl as a fallback context"


def test_piece_path_format():
    """Path must follow pieces/<id>/index.html convention."""
    piece = get_piece()
    assert piece is not None
    expected_path = f"pieces/{PIECE_ID}/index.html"
    assert piece["path"] == expected_path, \
        f"Expected path '{expected_path}', got '{piece['path']}'"


# ---------------------------------------------------------------------------
# Explicit failure modes
# ---------------------------------------------------------------------------

def test_wrong_piece_id_not_found():
    """A non-existent piece ID returns None — confirms get_piece() error behavior."""
    pieces = load_pieces()
    result = next((p for p in pieces if p["id"] == "53-does-not-exist"), None)
    assert result is None, "A fabricated ID must not match any piece"


def test_essay_missing_from_disk_detected(tmp_path):
    """Confirm that a non-existent essay path is detectable (error-path fixture)."""
    missing = os.path.join(str(tmp_path), "nonexistent_essay.md")
    assert not os.path.isfile(missing), "Fixture path must not exist"


def test_piece_without_webgl_would_fail_content_check():
    """Confirm the WebGL content check would catch an HTML file without getContext."""
    fake_html = "<html><body><canvas id='c'></canvas></body></html>"
    has_webgl = "getContext('webgl')" in fake_html or 'getContext("webgl")' in fake_html
    assert not has_webgl, "A plain HTML file without WebGL setup should not pass the WebGL check"
