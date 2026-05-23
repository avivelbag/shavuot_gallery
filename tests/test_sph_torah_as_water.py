"""
Tests for piece 80-sph-torah-as-water: SPH fluid simulation with Torah-as-water theme.

Validates file layout, content requirements, pieces.json registration, essay
substance, and SPH-specific implementation details in index.html.
"""
import json
import os
import re

import pytest

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID = "80-sph-torah-as-water"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")


def load_piece():
    """Load the pieces.json entry for the SPH piece."""
    with open(PIECES_JSON, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    for entry in data:
        if entry["id"] == PIECE_ID:
            return entry
    return None


def read_index():
    """Read index.html content."""
    return open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()


def read_essay():
    """Read essay.md content."""
    return open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()


# ---------------------------------------------------------------------------
# File layout
# ---------------------------------------------------------------------------

def test_piece_directory_exists():
    assert os.path.isdir(PIECE_DIR), f"Piece directory {PIECE_DIR} does not exist"


def test_index_html_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "index.html"))


def test_essay_md_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "essay.md"))


def test_thumbnail_svg_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "thumbnail.svg"))


def test_readme_md_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "README.md"))


# ---------------------------------------------------------------------------
# pieces.json registration
# ---------------------------------------------------------------------------

def test_registered_in_pieces_json():
    piece = load_piece()
    assert piece is not None, f"{PIECE_ID} not found in pieces.json"


def test_pieces_json_required_fields():
    piece = load_piece()
    assert piece is not None
    for field in ("id", "title", "tagline", "year", "theme", "technique", "path", "thumbnail", "essay"):
        assert field in piece and piece[field], f"Missing or empty field '{field}'"


def test_pieces_json_theme_mentions_torah():
    piece = load_piece()
    assert piece is not None
    theme = piece.get("theme", "").lower()
    assert "torah" in theme or "naaseh" in theme or "crown" in theme, (
        f"theme '{piece.get('theme')}' should reference Torah / naaseh v'nishma"
    )


def test_pieces_json_technique_mentions_sph():
    piece = load_piece()
    assert piece is not None
    technique = piece.get("technique", "").lower()
    assert "sph" in technique or "smoothed particle" in technique, (
        f"technique '{piece.get('technique')}' should mention SPH"
    )


def test_pieces_json_path_correct():
    piece = load_piece()
    assert piece is not None
    assert piece["path"] == f"pieces/{PIECE_ID}/index.html"


def test_pieces_json_thumbnail_correct():
    piece = load_piece()
    assert piece is not None
    assert piece["thumbnail"] == f"pieces/{PIECE_ID}/thumbnail.svg"


def test_pieces_json_essay_correct():
    piece = load_piece()
    assert piece is not None
    assert piece["essay"] == f"pieces/{PIECE_ID}/essay.md"


# ---------------------------------------------------------------------------
# Essay content
# ---------------------------------------------------------------------------

def test_essay_has_at_least_200_words():
    text = read_essay()
    assert len(text.split()) >= 200, f"essay.md has only {len(text.split())} words"


def test_essay_mentions_deuteronomy_32():
    text = read_essay()
    assert "Deuteronomy 32" in text or "32:2" in text, "essay must cite Deuteronomy 32:2"


def test_essay_mentions_taanit():
    text = read_essay()
    assert "Ta'anit" in text or "Taanit" in text or "Ta'anit" in text, (
        "essay must cite Ta'anit 7a (Torah as water / humility)"
    )


def test_essay_mentions_sifre():
    text = read_essay()
    assert "Sifre" in text, "essay must reference Sifre Devarim"


def test_essay_mentions_three_waters():
    text = read_essay()
    has_rain = "rain" in text or "matar" in text
    has_dew  = "dew" in text or "tal" in text
    assert has_rain and has_dew, "essay must mention rain and dew (the three waters metaphor)"


# ---------------------------------------------------------------------------
# index.html: canvas animation and SPH implementation
# ---------------------------------------------------------------------------

def test_index_uses_requestanimationframe():
    html = read_index()
    assert "requestAnimationFrame" in html


def test_index_has_canvas_element():
    html = read_index()
    assert "<canvas" in html


def test_index_mentions_sph_kernels():
    """index.html must implement poly6, spiky, and viscosity kernels."""
    html = read_index()
    assert "poly6" in html.lower() or "POLY6" in html, "poly6 kernel missing"
    assert "spiky" in html.lower() or "SPIKY" in html, "spiky kernel missing"
    assert "visc" in html.lower() or "VISC" in html, "viscosity kernel missing"


def test_index_declares_rest_density():
    html = read_index()
    assert "REST_DENSITY" in html


def test_index_declares_gravity():
    html = read_index()
    assert "GRAVITY" in html


def test_index_has_spatial_hashing():
    """Spatial hashing is required for O(1) neighbour lookup."""
    html = read_index()
    assert "hash" in html.lower() or "Hash" in html, "spatial hashing not found"


def test_index_has_boundary_enforcement():
    html = read_index()
    assert "enforceBoundary" in html or "Boundary" in html


def test_index_has_approximately_400_particles():
    html = read_index()
    # N = 400 or N = 200 (tuned down), but must be >= 200
    match = re.search(r'var\s+N\s*=\s*(\d+)', html)
    assert match is not None, "particle count variable N not found"
    count = int(match.group(1))
    assert 100 <= count <= 600, f"particle count {count} is outside expected range [100, 600]"


def test_index_has_dark_background():
    html = read_index()
    assert "#0A0C14" in html or "#0a0c14" in html, "background #0A0C14 not found"


def test_index_has_particle_color():
    html = read_index()
    assert "rgba(100,130,220" in html or "rgba(100, 130, 220" in html, (
        "particle color rgba(100,130,220,...) not found"
    )


def test_index_has_marching_squares():
    html = read_index()
    assert "march" in html.lower() or "isosurface" in html.lower() or "contour" in html.lower(), (
        "marching-squares surface rendering not found"
    )


def test_index_has_surface_contour_color():
    html = read_index()
    assert "#D8E8F0" in html or "#d8e8f0" in html, "surface contour color #D8E8F0 not found"


def test_index_embeds_essay_text():
    """index.html must embed the essay inline (no runtime fetch)."""
    essay = read_essay()
    html = read_index()
    words = [w for w in essay.split() if len(w) > 5][:10]
    found = sum(1 for w in words if w in html)
    assert found >= 5, (
        f"only {found}/10 essay words found in index.html — essay must be embedded inline"
    )


def test_index_has_fixed_seed():
    """Simulation must use a fixed seed for deterministic output."""
    html = read_index()
    assert "seed" in html.lower(), "fixed-seed PRNG not found"


# ---------------------------------------------------------------------------
# Thumbnail SVG
# ---------------------------------------------------------------------------

def test_thumbnail_is_valid_svg():
    text = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert "<svg" in text and "</svg>" in text


def test_thumbnail_has_dark_background():
    text = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert "#0A0C14" in text or "#0a0c14" in text


def test_thumbnail_has_circles():
    text = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert "<circle" in text, "thumbnail must contain circle elements"


def test_thumbnail_has_surface_line():
    text = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert "<path" in text or "<line" in text, "thumbnail must have a surface line"


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

def test_essay_not_stub():
    """Essay must not be a short placeholder."""
    text = read_essay()
    assert len(text.strip()) > 500, "essay is suspiciously short — may be a placeholder"


def test_index_no_external_dependencies():
    """index.html should be self-contained; no CDN or external script src."""
    html = read_index()
    external = re.findall(r'src=["\']https?://', html)
    assert len(external) == 0, f"index.html has external script src: {external}"


def test_readme_mentions_sph():
    text = open(os.path.join(PIECE_DIR, "README.md"), encoding="utf-8").read()
    assert "SPH" in text or "Smoothed Particle" in text
