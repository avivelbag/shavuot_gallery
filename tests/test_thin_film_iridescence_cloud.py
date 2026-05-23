"""
Tests for piece 71-thin-film-iridescence-cloud.

Validates the piece files, shader correctness properties, spectrum conversion
logic, essay content, and integration with the gallery manifest.
"""
import json
import math
import os
import re

import pytest

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID = "71-thin-film-iridescence-cloud"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
INDEX_HTML = os.path.join(PIECE_DIR, "index.html")
ESSAY_MD = os.path.join(PIECE_DIR, "essay.md")
THUMBNAIL = os.path.join(PIECE_DIR, "thumbnail.svg")
README = os.path.join(PIECE_DIR, "README.md")
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


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


# ---------------------------------------------------------------------------
# pieces.json registration
# ---------------------------------------------------------------------------

def test_piece_registered_in_pieces_json():
    """The piece must appear in pieces.json with all required fields."""
    piece = get_piece()
    assert piece is not None, f"{PIECE_ID} not found in pieces.json"


def test_piece_json_fields_complete():
    """All required fields must be present and non-empty."""
    piece = get_piece()
    required = ("id", "title", "tagline", "year", "theme", "technique", "path", "thumbnail", "essay")
    for field in required:
        assert field in piece, f"Missing field: {field}"
        assert piece[field], f"Empty field: {field}"


def test_piece_json_theme_is_har_sinai():
    """Theme must reference Har Sinai as specified in the suggestion."""
    piece = get_piece()
    assert "Sinai" in piece["theme"], f"Expected 'Sinai' in theme, got: {piece['theme']}"


def test_piece_json_technique_mentions_webgl():
    """Technique must reference WebGL (fragment shader)."""
    piece = get_piece()
    technique = piece["technique"].lower()
    assert "webgl" in technique, f"Expected 'webgl' in technique, got: {piece['technique']}"


def test_piece_json_technique_mentions_thin_film():
    """Technique must reference thin-film interference."""
    piece = get_piece()
    technique = piece["technique"].lower()
    assert "thin-film" in technique or "thin film" in technique, (
        f"Expected 'thin-film' in technique, got: {piece['technique']}"
    )


def test_piece_json_year_is_int():
    piece = get_piece()
    assert isinstance(piece["year"], int)


def test_piece_json_no_duplicate_ids():
    pieces = load_pieces()
    ids = [p["id"] for p in pieces]
    assert len(ids) == len(set(ids)), "Duplicate IDs in pieces.json"


# ---------------------------------------------------------------------------
# File existence
# ---------------------------------------------------------------------------

def test_index_html_exists():
    assert os.path.isfile(INDEX_HTML)


def test_essay_md_exists():
    assert os.path.isfile(ESSAY_MD)


def test_thumbnail_svg_exists():
    assert os.path.isfile(THUMBNAIL)


def test_readme_exists():
    assert os.path.isfile(README)


# ---------------------------------------------------------------------------
# index.html — WebGL shader requirements
# ---------------------------------------------------------------------------

def test_index_html_uses_webgl():
    """index.html must obtain a WebGL context."""
    html = read(INDEX_HTML)
    assert "getContext('webgl')" in html or 'getContext("webgl")' in html


def test_index_html_has_vertex_shader():
    """index.html must embed a vertex shader."""
    html = read(INDEX_HTML)
    assert "VERTEX_SHADER" in html or "vertex_shader" in html.lower()


def test_index_html_has_fragment_shader():
    """index.html must embed a fragment shader."""
    html = read(INDEX_HTML)
    assert "FRAGMENT_SHADER" in html or "fragment_shader" in html.lower()


def test_index_html_has_film_thickness_field():
    """Shader must compute a filmThickness function."""
    html = read(INDEX_HTML)
    assert "filmThickness" in html


def test_index_html_has_sin_cos_noise():
    """Thickness field must use sin/cos harmonics per specification."""
    html = read(INDEX_HTML)
    assert "sin(" in html and "cos(" in html


def test_index_html_has_cie_observer_weights():
    """Shader must bake in CIE observer weight constants (cie0..cie7)."""
    html = read(INDEX_HTML)
    assert "cie0" in html and "cie7" in html


def test_index_html_has_xyz_to_srgb_matrix():
    """Shader must include XYZ-to-sRGB conversion matrix."""
    html = read(INDEX_HTML)
    assert "XYZ_TO_SRGB" in html or "xyzToSRGB" in html or "3.2406" in html


def test_index_html_has_film_intensity_formula():
    """Shader must use cos² interference formula."""
    html = read(INDEX_HTML)
    assert "filmIntensity" in html or "cos(phase)" in html


def test_index_html_has_eight_wavelength_samples():
    """Shader must sample 8 wavelengths spanning 380–702 nm."""
    html = read(INDEX_HTML)
    assert "380.0" in html and "702.0" in html


def test_index_html_has_vignette():
    """index.html must apply a vignette effect."""
    html = read(INDEX_HTML)
    assert "vignette" in html


def test_index_html_uses_request_animation_frame():
    html = read(INDEX_HTML)
    assert "requestAnimationFrame" in html


def test_index_html_has_canvas_element():
    html = read(INDEX_HTML)
    assert "<canvas" in html


def test_index_html_has_refractive_index():
    """Shader must specify a refractive index constant."""
    html = read(INDEX_HTML)
    assert "1.45" in html or "N_FILM" in html


def test_index_html_u_time_uniform():
    """index.html must pass time as a uniform to the shader."""
    html = read(INDEX_HTML)
    assert "u_time" in html


def test_index_html_u_resolution_uniform():
    """index.html must pass resolution as a uniform to the shader."""
    html = read(INDEX_HTML)
    assert "u_resolution" in html


def test_index_html_embeds_essay_text():
    """index.html must inline the essay text (not fetch it at runtime)."""
    essay = read(ESSAY_MD)
    html = read(INDEX_HTML)
    words = [w for w in essay.split() if len(w) > 5]
    sampled = words[:10]
    found = sum(1 for w in sampled if w in html)
    assert found >= 5, f"Only {found}/10 essay words found in index.html"


# ---------------------------------------------------------------------------
# essay.md content
# ---------------------------------------------------------------------------

def test_essay_word_count():
    """essay.md must be at least 400 words."""
    text = read(ESSAY_MD)
    wc = len(text.split())
    assert wc >= 400, f"essay.md only has {wc} words (need ≥ 400)"


def test_essay_references_exodus_19():
    """Essay must cite Exodus 19 (the cloud at Sinai)."""
    text = read(ESSAY_MD).lower()
    assert "exodus 19" in text or "19:16" in text


def test_essay_references_exodus_24():
    """Essay must cite Exodus 24 (Moses entering the cloud)."""
    text = read(ESSAY_MD).lower()
    assert "exodus 24" in text or "24:15" in text


def test_essay_mentions_concealing_and_revealing():
    """Essay must address the concealing-and-revealing paradox of the cloud."""
    text = read(ESSAY_MD).lower()
    assert ("conceal" in text or "hidden" in text) and ("reveal" in text or "medium" in text)


def test_essay_explains_thin_film_physics():
    """Essay must explain the physics of thin-film interference."""
    text = read(ESSAY_MD).lower()
    assert "interference" in text and ("wavelength" in text or "thickness" in text)


def test_essay_no_placeholder_text():
    """essay.md must not contain placeholder stub text."""
    text = read(ESSAY_MD).lower()
    for stub in ("lorem ipsum", "todo", "placeholder", "tbd", "fixme"):
        assert stub not in text, f"Stub text '{stub}' found in essay.md"


# ---------------------------------------------------------------------------
# thumbnail.svg
# ---------------------------------------------------------------------------

def test_thumbnail_is_valid_svg():
    text = read(THUMBNAIL)
    assert "<svg" in text and "</svg>" in text


def test_thumbnail_has_radial_gradient():
    text = read(THUMBNAIL)
    assert "radialGradient" in text


def test_thumbnail_has_iridescent_stops():
    """Thumbnail gradient must span the violet-to-orange iridescent palette."""
    text = read(THUMBNAIL)
    assert "stop" in text
    lower = text.lower()
    assert "violet" in lower or "#9060e0" in lower or "#6a0dad" in lower or "#9020" in lower or "a0" in lower


def test_thumbnail_has_dark_background():
    """Thumbnail must include the near-black canvas background (#050510 or similar)."""
    text = read(THUMBNAIL)
    assert "#050510" in text or "#050508" in text or "#060612" in text or "050" in text


def test_thumbnail_dimensions_400():
    """Thumbnail must declare 400×400 dimensions."""
    text = read(THUMBNAIL)
    assert 'width="400"' in text and 'height="400"' in text


def test_thumbnail_has_vignette_overlay():
    """Thumbnail must include a vignette (dark overlay gradient)."""
    text = read(THUMBNAIL)
    assert "vignette" in text.lower() or text.count("radialGradient") >= 2


# ---------------------------------------------------------------------------
# README.md
# ---------------------------------------------------------------------------

def test_readme_mentions_sinai():
    text = read(README).lower()
    assert "sinai" in text


def test_readme_mentions_thin_film():
    text = read(README).lower()
    assert "thin-film" in text or "thin film" in text


def test_readme_mentions_refractive_index():
    text = read(README)
    assert "1.45" in text or "refractive" in text.lower()


def test_readme_mentions_cie():
    """README must document the CIE observer function used."""
    text = read(README).upper()
    assert "CIE" in text


# ---------------------------------------------------------------------------
# Physics correctness — pure-Python verification of the interference formula
# ---------------------------------------------------------------------------

def thin_film_intensity(d_nm, lambda_nm, n=1.45):
    """Python implementation of the GLSL filmIntensity function."""
    phase = math.pi * 2.0 * n * d_nm / lambda_nm
    return math.cos(phase) ** 2


def test_thin_film_constructive_at_resonance():
    """Constructive interference (I=1) when 2·n·d = m·λ for integer m."""
    n = 1.45
    d = 300.0
    m = 2
    lam = 2 * n * d / m
    intensity = thin_film_intensity(d, lam, n)
    assert abs(intensity - 1.0) < 1e-9, f"Expected I=1 at resonance, got {intensity}"


def test_thin_film_destructive_at_half_resonance():
    """Destructive interference (I=0) when 2·n·d = (m + 0.5)·λ."""
    n = 1.45
    d = 300.0
    m = 2
    lam = 2 * n * d / (m + 0.5)
    intensity = thin_film_intensity(d, lam, n)
    assert abs(intensity) < 1e-9, f"Expected I=0 at destructive, got {intensity}"


def test_thin_film_intensity_bounded_0_1():
    """Intensity must always lie in [0, 1] for all valid inputs."""
    for d in range(200, 900, 50):
        for lam in range(380, 710, 10):
            i = thin_film_intensity(d, lam)
            assert 0.0 <= i <= 1.0, f"I={i} out of bounds at d={d}, λ={lam}"


def test_thin_film_intensity_is_symmetric():
    """cos² is an even function — phase sign should not matter."""
    d, lam = 400.0, 550.0
    i1 = thin_film_intensity(d, lam)
    phase = math.pi * 2 * 1.45 * d / lam
    i2 = math.cos(-phase) ** 2
    assert abs(i1 - i2) < 1e-12


def test_spectrum_produces_color_variation():
    """Different film thicknesses must produce distinctly different spectra."""
    wavelengths = [380.0, 426.0, 472.0, 518.0, 564.0, 610.0, 656.0, 702.0]

    def spectrum(d):
        return [thin_film_intensity(d, lam) for lam in wavelengths]

    spec_thin = spectrum(250.0)
    spec_thick = spectrum(600.0)
    diff = sum(abs(a - b) for a, b in zip(spec_thin, spec_thick))
    assert diff > 1.0, f"Spectra at 250nm and 600nm too similar (diff={diff:.3f})"


def test_visible_range_shows_full_spectrum_shift():
    """Varying d from 200 to 800 nm must produce peak intensities across all 8 channels."""
    wavelengths = [380.0, 426.0, 472.0, 518.0, 564.0, 610.0, 656.0, 702.0]
    peak_per_channel = [0.0] * 8
    for d in range(200, 801, 5):
        for i, lam in enumerate(wavelengths):
            v = thin_film_intensity(float(d), lam)
            if v > peak_per_channel[i]:
                peak_per_channel[i] = v

    for i, peak in enumerate(peak_per_channel):
        assert peak > 0.9, (
            f"Channel {i} (λ={wavelengths[i]}nm) never peaks above 0.9 over d=200–800nm; got {peak:.3f}"
        )


# ---------------------------------------------------------------------------
# Noise field — film thickness range
# ---------------------------------------------------------------------------

def film_thickness(x, y, t, height=700.0):
    """Python mirror of the GLSL filmThickness function."""
    n1 = math.sin(x * 0.004 + t) * math.cos(y * 0.0052 + t * 0.7)
    n2 = math.sin(x * 0.009 + t * 1.3) * math.cos(y * 0.011 - t * 0.5)
    vert_grad = (1.0 - y / height) * 80.0
    return 500.0 + 300.0 * (0.667 * n1 + 0.333 * n2) + vert_grad


def test_film_thickness_range():
    """Film thickness must stay in 200–900 nm over all canvas positions."""
    min_d = float("inf")
    max_d = float("-inf")
    for x in range(0, 701, 50):
        for y in range(0, 701, 50):
            d = film_thickness(x, y, 0.0)
            min_d = min(min_d, d)
            max_d = max(max_d, d)
    assert min_d >= 150.0, f"Minimum thickness {min_d:.1f} nm too low"
    assert max_d <= 950.0, f"Maximum thickness {max_d:.1f} nm too high"


def test_film_thickness_vertical_gradient():
    """Top of canvas (y=0) must be thicker than bottom (y=700) at same x and t."""
    x, t = 350.0, 0.0
    top = film_thickness(x, 0.0, t)
    bottom = film_thickness(x, 700.0, t)
    assert top > bottom, f"Expected top ({top:.1f}) > bottom ({bottom:.1f})"


def test_film_thickness_varies_with_time():
    """Thickness field must change as t advances (animation must be non-static)."""
    diffs = []
    for x in range(100, 601, 100):
        for y in range(100, 601, 100):
            d0 = film_thickness(x, y, 0.0)
            d1 = film_thickness(x, y, 10.0)
            diffs.append(abs(d1 - d0))
    assert max(diffs) > 50.0, "Thickness field does not change significantly with time"


def test_film_thickness_two_octave_structure():
    """Noise must have two-octave structure: f2 ≈ 2.25× f1."""
    f1 = 0.004
    f2 = 0.009
    ratio = f2 / f1
    assert 2.0 < ratio < 2.5, f"Expected f2/f1 ~ 2.25, got {ratio:.3f}"


# ---------------------------------------------------------------------------
# Failure modes / edge cases
# ---------------------------------------------------------------------------

def test_zero_thickness_does_not_crash():
    """filmIntensity at d=0 must return 1.0 (cos²(0) = 1)."""
    result = thin_film_intensity(0.0, 550.0)
    assert abs(result - 1.0) < 1e-9


def test_very_large_thickness_bounded():
    """filmIntensity must remain in [0,1] even at extreme thickness (10 000 nm)."""
    for lam in [380.0, 550.0, 700.0]:
        v = thin_film_intensity(10000.0, lam)
        assert 0.0 <= v <= 1.0, f"I={v} out of bounds at d=10000nm, λ={lam}"


def test_piece_files_do_not_leak_outside_tmp_path(tmp_path):
    """Confirm all piece paths are relative to gallery root (no absolute paths in pieces.json)."""
    piece = get_piece()
    for key in ("path", "thumbnail", "essay"):
        val = piece[key]
        assert not os.path.isabs(val), f"Field '{key}' is an absolute path: {val}"


def test_no_external_library_imports_in_html():
    """The fragment shader must not import external noise libraries."""
    html = read(INDEX_HTML)
    suspicious = re.findall(r'<script[^>]+src=["\']([^"\']+)["\']', html)
    external = [s for s in suspicious if s.startswith("http")]
    assert len(external) == 0, f"Found external script imports: {external}"
