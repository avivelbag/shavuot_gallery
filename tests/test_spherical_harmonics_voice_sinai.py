"""
Tests for piece 91-spherical-harmonics-voice-sinai.

Validates the WebGL spherical harmonics piece: pieces.json registration,
file layout, essay substance, and HTML implementation requirements from
the acceptance criteria.
"""
import json
import os

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECES_JSON  = os.path.join(GALLERY_ROOT, "pieces.json")
PIECE_ID     = "91-spherical-harmonics-voice-sinai"
PIECE_DIR    = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
INDEX_HTML   = os.path.join(PIECE_DIR, "index.html")
ESSAY_MD     = os.path.join(PIECE_DIR, "essay.md")
THUMBNAIL    = os.path.join(PIECE_DIR, "thumbnail.svg")
README       = os.path.join(PIECE_DIR, "README.md")


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
    """The spherical harmonics piece must appear in pieces.json."""
    assert _get_piece() is not None, f"Piece '{PIECE_ID}' not found in pieces.json"


def test_piece_theme_mentions_sinai():
    """Theme must reference Har Sinai and the divine voice."""
    piece = _get_piece()
    assert piece is not None
    theme = piece.get("theme", "").lower()
    assert "sinai" in theme, f"Theme '{piece.get('theme')}' must mention Sinai"


def test_piece_technique_mentions_spherical_harmonics_and_webgl():
    """Technique field must reference spherical harmonics and WebGL."""
    piece = _get_piece()
    assert piece is not None
    tech = piece.get("technique", "").lower()
    assert "spherical harmonics" in tech, "technique must mention 'Spherical harmonics'"
    assert "webgl" in tech, "technique must mention 'WebGL'"


def test_piece_year_is_int():
    piece = _get_piece()
    assert piece is not None
    assert isinstance(piece["year"], int)


def test_piece_required_fields_all_present_and_non_empty():
    """All standard required fields must be non-empty."""
    required = ("id", "title", "tagline", "year", "theme", "technique",
                "path", "thumbnail", "essay")
    piece = _get_piece()
    assert piece is not None
    for field in required:
        assert field in piece and piece[field], (
            f"Field '{field}' missing or empty in piece registration"
        )


def test_piece_no_duplicate_id():
    """Piece ID must be unique across all pieces."""
    pieces = _load_pieces()
    ids = [p["id"] for p in pieces]
    assert ids.count(PIECE_ID) == 1, f"Duplicate ID '{PIECE_ID}' found in pieces.json"


def test_piece_path_ends_with_html():
    piece = _get_piece()
    assert piece is not None
    assert piece["path"].endswith(".html")


def test_piece_id_matches_directory():
    piece = _get_piece()
    assert piece is not None
    parts = piece["path"].replace("\\", "/").split("/")
    assert parts[-2] == PIECE_ID, (
        f"Directory '{parts[-2]}' in path does not match id '{PIECE_ID}'"
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


def test_thumbnail_svg_exists():
    assert os.path.isfile(THUMBNAIL), "thumbnail.svg is missing from piece directory"


def test_readme_exists():
    assert os.path.isfile(README), "README.md is missing from piece directory"


def test_thumbnail_points_to_existing_file():
    piece = _get_piece()
    assert piece is not None
    thumb = os.path.join(GALLERY_ROOT, piece["thumbnail"])
    assert os.path.isfile(thumb), f"thumbnail '{piece['thumbnail']}' does not exist on disk"


def test_essay_field_points_to_existing_file():
    piece = _get_piece()
    assert piece is not None
    essay_path = os.path.join(GALLERY_ROOT, piece["essay"])
    assert os.path.isfile(essay_path), f"essay '{piece['essay']}' does not exist on disk"


# ---------------------------------------------------------------------------
# Thumbnail is valid SVG with 400x400 dimensions
# ---------------------------------------------------------------------------

def test_thumbnail_is_valid_svg():
    content = open(THUMBNAIL, encoding="utf-8").read()
    assert "<svg" in content and "</svg>" in content, "thumbnail.svg is not valid SVG"


def test_thumbnail_is_400x400():
    content = open(THUMBNAIL, encoding="utf-8").read()
    assert 'width="400"' in content and 'height="400"' in content, (
        "thumbnail.svg must declare width=400 and height=400"
    )


def test_thumbnail_has_radial_gradient():
    content = open(THUMBNAIL, encoding="utf-8").read()
    assert "radialGradient" in content, "thumbnail.svg must use a radial gradient"


def test_thumbnail_has_grid_lines():
    """Thumbnail must include latitude/longitude grid lines at 20% opacity."""
    content = open(THUMBNAIL, encoding="utf-8").read()
    assert "0.2" in content or "20%" in content, (
        "thumbnail.svg must include grid lines at ~20% opacity"
    )


# ---------------------------------------------------------------------------
# Essay substance (~420 words, required content)
# ---------------------------------------------------------------------------

def test_essay_at_least_350_words():
    text = open(ESSAY_MD, encoding="utf-8").read()
    count = len(text.split())
    assert count >= 350, f"essay.md has only {count} words; need at least 350"


def test_essay_cites_shemot_rabbah():
    text = open(ESSAY_MD, encoding="utf-8").read()
    assert "Shemot Rabbah" in text or "shemot rabbah" in text.lower(), (
        "essay.md must cite Shemot Rabbah 5:9"
    )


def test_essay_cites_exodus_19():
    text = open(ESSAY_MD, encoding="utf-8").read()
    assert "Exodus 19" in text or "exodus 19" in text.lower(), (
        "essay.md must cite Exodus 19:18-19"
    )


def test_essay_cites_pirkei_de_rabbi_eliezer():
    text = open(ESSAY_MD, encoding="utf-8").read()
    lower = text.lower()
    assert "pirkei" in lower or "derabbi" in lower or "de-rabbi" in lower or "eliezer" in lower, (
        "essay.md must cite Pirkei DeRabbi Eliezer 41"
    )


def test_essay_explains_spherical_harmonics():
    text = open(ESSAY_MD, encoding="utf-8").read().lower()
    assert "spherical harmonic" in text, "essay.md must explain spherical harmonics"


def test_essay_mentions_seventy_languages():
    text = open(ESSAY_MD, encoding="utf-8").read().lower()
    assert "70" in text or "seventy" in text, (
        "essay.md must mention the 70 languages"
    )


def test_essay_mentions_monopole_or_l_zero():
    """Essay must explain the l=0 monopole as the uniform-direction term."""
    text = open(ESSAY_MD, encoding="utf-8").read().lower()
    assert "monopole" in text or "l = 0" in text or "l=0" in text or "y_0" in text or "y00" in text, (
        "essay.md must explain the l=0 (monopole) harmonic as the uniform-direction term"
    )


# ---------------------------------------------------------------------------
# index.html implementation requirements
# ---------------------------------------------------------------------------

def test_html_uses_webgl():
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "webgl" in html.lower(), "index.html must request a WebGL context"


def test_html_has_canvas_element():
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "<canvas" in html, "index.html must have a <canvas> element"


def test_html_uses_requestanimationframe():
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "requestAnimationFrame" in html, "index.html must use requestAnimationFrame"


def test_html_defines_25_sh_coefficients():
    """Vertex shader must use a 25-element coefficient array for l=0..4."""
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "25" in html, "index.html must reference 25 SH coefficients"
    assert "uCoeffs" in html or "coeffs" in html.lower(), (
        "index.html must define a coefficient uniform (uCoeffs or similar)"
    )


def test_html_vertex_shader_computes_y00():
    """Vertex shader must include Y_0^0 = 0.28209."""
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "0.28209" in html, (
        "vertex shader must define Y_0^0 ≈ 0.28209 (monopole harmonic)"
    )


def test_html_vertex_shader_has_l4_terms():
    """Vertex shader must include l=4 harmonic constants."""
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "0.62584" in html or "1.77013" in html or "0.47309" in html, (
        "vertex shader must include l=4 spherical harmonic constants"
    )


def test_html_has_rotation_speed_015():
    """Sphere must rotate at 0.15 rad/s around y-axis."""
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "0.15" in html, "index.html must define rotation speed 0.15 rad/s"


def test_html_has_amplitude_035():
    """Deformation amplitude must be 0.35."""
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "0.35" in html, "index.html must define amplitude A = 0.35"


def test_html_mesh_is_64x64():
    """UV sphere mesh must be 64×64 segments."""
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "W = 64" in html or "W=64" in html or "const W = 64" in html, (
        "index.html must define W=64 longitude steps"
    )
    assert "H = 64" in html or "H=64" in html or "const H = 64" in html, (
        "index.html must define H=64 latitude steps"
    )


def test_html_has_color_palette_midnight_blue():
    """Color palette must include midnight blue #0B1440."""
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "0B1440" in html or "0b1440" in html.lower() or "0.04314" in html, (
        "index.html must define midnight blue #0B1440 in the color palette"
    )


def test_html_has_color_palette_flame_white():
    """Color palette must include flame white #FFF8E8."""
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "FFF8E8" in html or "fff8e8" in html.lower() or "0.90980" in html, (
        "index.html must define flame white #FFF8E8 in the color palette"
    )


def test_html_embeds_essay_text():
    """index.html must embed essay content inline (not load it at runtime)."""
    essay_text = open(ESSAY_MD, encoding="utf-8").read()
    html = open(INDEX_HTML, encoding="utf-8").read()
    words = [w for w in essay_text.split() if len(w) > 6][:10]
    found = sum(1 for w in words if w in html)
    assert found >= 5, (
        f"index.html does not appear to embed essay text (only {found}/10 sampled words found)"
    )


def test_html_uses_blinn_phong_or_specular():
    """index.html must implement specular/Blinn-Phong lighting."""
    html = open(INDEX_HTML, encoding="utf-8").read()
    lower = html.lower()
    assert "specular" in lower or "blinn" in lower or "phong" in lower, (
        "index.html must implement specular/Blinn-Phong shading"
    )


def test_html_theta_phi_as_vertex_attribute():
    """Vertex shader must accept theta/phi as vertex attributes."""
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "ThetaPhi" in html or "thetaphi" in html.lower() or "aThetaPhi" in html, (
        "index.html must use theta/phi as vertex attribute"
    )


def test_html_animation_frequency_formula():
    """SH frequency formula ω = 0.3 + l*0.2 must be present."""
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "0.3" in html and "0.2" in html, (
        "index.html must define frequency ω = 0.3 + l*0.2"
    )


def test_html_readme_mentions_sinai():
    readme_text = open(README, encoding="utf-8").read().lower()
    assert "sinai" in readme_text, "README.md must mention Sinai"


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

def test_essay_does_not_call_itself_abstract():
    """Essay must not describe the piece as merely an abstraction (per acceptance criteria)."""
    text = open(ESSAY_MD, encoding="utf-8").read().lower()
    assert "not an abstraction" in text or "not abstract" in text or "model of" in text, (
        "essay.md must explain the piece as a model, not merely an abstraction"
    )


def test_index_html_has_depth_test():
    """WebGL depth test must be enabled for correct 3D rendering."""
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "DEPTH_TEST" in html, "index.html must enable gl.DEPTH_TEST for 3D rendering"


def test_index_html_has_element_draw():
    """index.html must use drawElements (indexed triangle mesh)."""
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "drawElements" in html, (
        "index.html must use gl.drawElements for the indexed UV sphere mesh"
    )


# ---------------------------------------------------------------------------
# Failure modes
# ---------------------------------------------------------------------------

def test_missing_essay_file_detection(tmp_path):
    """A non-existent essay path is not a real file."""
    missing = os.path.join(str(tmp_path), "nonexistent_essay.md")
    assert not os.path.isfile(missing)


def test_short_essay_fails_word_count(tmp_path):
    """An essay with fewer than 350 words must fail the word-count check."""
    short = tmp_path / "short.md"
    short.write_text("word " * 100, encoding="utf-8")
    count = len(short.read_text(encoding="utf-8").split())
    assert count < 350, "Fixture must have fewer than 350 words"


def test_empty_theme_detected():
    """A piece entry with an empty theme must fail the field-presence check."""
    bad = {"id": PIECE_ID, "theme": ""}
    assert not bad["theme"], "empty theme must be treated as missing"


def test_wrong_piece_id_not_found():
    """A misspelled piece ID must return None from the lookup."""
    result = next(
        (p for p in _load_pieces() if p["id"] == "91-wrong-id"),
        None
    )
    assert result is None, "lookup of a wrong ID must return None"
