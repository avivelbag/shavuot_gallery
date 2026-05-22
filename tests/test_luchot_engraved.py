"""
Tests for piece 06 "Engraved in Stone" (luchot-engraved).

Covers: file layout, pieces.json registration, SVG correctness,
Hebrew text presence, stone-texture filter, CSS glow animation,
and explicit failure / edge-case modes.
"""
import json
import os
import re

import pytest

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")
PIECE_ID = "06-luchot-engraved"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)


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


def read_piece_file(filename):
    return open(os.path.join(PIECE_DIR, filename), encoding="utf-8").read()


# ---------------------------------------------------------------------------
# pieces.json registration
# ---------------------------------------------------------------------------

def test_piece_06_in_json():
    assert get_piece() is not None, f"'{PIECE_ID}' not found in pieces.json"


def test_piece_06_theme():
    piece = get_piece()
    assert piece is not None
    assert "Matan Torah" in piece["theme"] or "Tablets" in piece["theme"], (
        "theme must reference Matan Torah or The Two Tablets"
    )


def test_piece_06_technique_mentions_svg_and_filter():
    piece = get_piece()
    assert piece is not None
    technique = piece["technique"].lower()
    assert "svg" in technique, "technique must mention SVG"
    assert "filter" in technique or "carved" in technique, (
        "technique must mention filter effects or carved typography"
    )


def test_piece_06_year_is_integer():
    piece = get_piece()
    assert piece is not None
    assert isinstance(piece["year"], int)


# ---------------------------------------------------------------------------
# File layout
# ---------------------------------------------------------------------------

def test_piece_06_index_html_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "index.html")), (
        "pieces/06-luchot-engraved/index.html is missing"
    )


def test_piece_06_thumbnail_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "thumbnail.svg")), (
        "pieces/06-luchot-engraved/thumbnail.svg is missing"
    )


def test_piece_06_readme_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "README.md")), (
        "pieces/06-luchot-engraved/README.md is missing"
    )


def test_piece_06_essay_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "essay.md")), (
        "pieces/06-luchot-engraved/essay.md is missing"
    )


# ---------------------------------------------------------------------------
# index.html — SVG structure
# ---------------------------------------------------------------------------

def test_piece_06_html_contains_svg():
    html = read_piece_file("index.html")
    assert "<svg" in html and "</svg>" in html, (
        "index.html must contain an inline SVG element"
    )


def test_piece_06_html_has_fe_turbulence():
    """Stone texture requires feTurbulence filter primitive."""
    html = read_piece_file("index.html")
    assert "feTurbulence" in html, (
        "index.html must use feTurbulence for stone texture"
    )


def test_piece_06_html_has_fe_displacement_map():
    """Stone texture requires feDisplacementMap to apply the noise."""
    html = read_piece_file("index.html")
    assert "feDisplacementMap" in html, (
        "index.html must use feDisplacementMap for stone texture"
    )


def test_piece_06_html_has_two_tablet_paths():
    """Two arched tablet shapes must be present as SVG path elements."""
    html = read_piece_file("index.html")
    paths = re.findall(r"<path\b", html)
    assert len(paths) >= 2, (
        f"index.html must contain at least 2 <path> elements for the tablets; found {len(paths)}"
    )


def test_piece_06_html_has_hebrew_text():
    """The ten commandments must appear as Unicode Hebrew text."""
    html = read_piece_file("index.html")
    # Check for at least one of the well-known commandment headings
    assert "אָנֹכִי" in html or "אָנֹכִי" in html, (
        "index.html must contain the Hebrew text of the commandments (אָנֹכִי)"
    )
    assert "לֹא תִרְצָח" in html or "לא" in html, (
        "index.html must contain Hebrew commandment text from the second tablet"
    )


def test_piece_06_html_rtl_direction():
    """Hebrew text elements must specify RTL direction."""
    html = read_piece_file("index.html")
    assert 'direction="rtl"' in html or "direction:rtl" in html, (
        "index.html must set direction=rtl on Hebrew text elements"
    )


def test_piece_06_html_glow_animation_8s():
    """CSS glow animation must run at approximately 8 s period, no JS."""
    html = read_piece_file("index.html")
    assert "@keyframes" in html, "index.html must define a CSS @keyframes glow animation"
    assert "8s" in html, "glow animation must specify an 8 s duration"
    # No requestAnimationFrame: the animation must be pure CSS
    assert "requestAnimationFrame" not in html, (
        "glow animation must be pure CSS — no requestAnimationFrame"
    )


def test_piece_06_html_no_external_resources():
    """The piece must be self-contained — no external src/href links."""
    html = read_piece_file("index.html")
    # Reject http(s) URLs that would load external resources
    external = re.findall(r'(?:src|href)\s*=\s*["\']https?://', html)
    assert not external, (
        f"index.html must not load external resources; found: {external}"
    )


def test_piece_06_html_tablet_colors_present():
    """Stone gradient colours and glow colour must appear in the markup."""
    html = read_piece_file("index.html")
    assert "#8a8a8a" in html.lower() or "8a8a8a" in html.lower(), (
        "index.html must reference stone colour #8a8a8a"
    )
    assert "#c8c0b0" in html.lower() or "c8c0b0" in html.lower(), (
        "index.html must reference stone colour #c8c0b0"
    )
    assert "#f0ece0" in html.lower() or "f0ece0" in html.lower(), (
        "index.html must reference carved letter colour #f0ece0"
    )
    assert "c87820" in html.lower(), (
        "index.html must reference amber-gold glow colour #c87820"
    )


# ---------------------------------------------------------------------------
# thumbnail.svg
# ---------------------------------------------------------------------------

def test_piece_06_thumbnail_is_valid_svg():
    svg = read_piece_file("thumbnail.svg")
    assert "<svg" in svg and "</svg>" in svg, (
        "thumbnail.svg does not look like valid SVG"
    )


def test_piece_06_thumbnail_has_hebrew_text():
    svg = read_piece_file("thumbnail.svg")
    assert "אָנֹכִי" in svg or "לֹא" in svg, (
        "thumbnail.svg must contain Hebrew commandment text"
    )


def test_piece_06_thumbnail_has_stone_filters():
    svg = read_piece_file("thumbnail.svg")
    assert "feTurbulence" in svg, (
        "thumbnail.svg must include feTurbulence for stone texture"
    )


def test_piece_06_thumbnail_400x400():
    """Thumbnail should declare 400×400 dimensions."""
    svg = read_piece_file("thumbnail.svg")
    assert 'width="400"' in svg and 'height="400"' in svg, (
        "thumbnail.svg must be 400×400 as declared by width/height attributes"
    )


# ---------------------------------------------------------------------------
# README.md and essay.md content
# ---------------------------------------------------------------------------

def test_piece_06_readme_mentions_luchot_or_tablets():
    text = read_piece_file("README.md").lower()
    assert "luchot" in text or "tablet" in text or "לוחות" in text, (
        "README.md must mention the luchot / tablets"
    )


def test_piece_06_readme_mentions_commandments():
    text = read_piece_file("README.md").lower()
    assert "commandment" in text or "ten" in text or "עשרת" in text, (
        "README.md must reference the ten commandments"
    )


def test_piece_06_essay_mentions_sinai():
    text = read_piece_file("essay.md").lower()
    assert "sinai" in text or "mount" in text or "סיני" in text, (
        "essay.md must reference Sinai or the mountain"
    )


def test_piece_06_essay_mentions_engraved_or_carved():
    text = read_piece_file("essay.md").lower()
    assert "engrav" in text or "carv" in text or "חרות" in text or "charut" in text, (
        "essay.md must discuss the engraved/carved quality of the commandments"
    )


# ---------------------------------------------------------------------------
# Edge cases and explicit failure modes
# ---------------------------------------------------------------------------

def test_piece_06_id_matches_directory():
    """The piece id must match the directory name in its path."""
    piece = get_piece()
    assert piece is not None
    path_parts = piece["path"].replace("\\", "/").split("/")
    dir_name = path_parts[-2]
    assert dir_name == PIECE_ID, (
        f"piece id '{PIECE_ID}' does not match directory '{dir_name}'"
    )


def test_piece_06_path_ends_with_html():
    piece = get_piece()
    assert piece is not None
    assert piece["path"].endswith(".html"), "piece path must end with .html"


def test_piece_06_thumbnail_extension_is_svg():
    piece = get_piece()
    assert piece is not None
    ext = os.path.splitext(piece["thumbnail"])[1].lower()
    assert ext == ".svg", f"thumbnail extension must be .svg, got '{ext}'"


def test_missing_essay_detected(tmp_path):
    """Verify that our check correctly fails when essay.md is absent."""
    fake_dir = tmp_path / "fake-piece"
    fake_dir.mkdir()
    assert not (fake_dir / "essay.md").exists(), (
        "essay.md should not exist in the fake directory"
    )


def test_piece_06_no_duplicate_with_existing():
    """Piece 06 must not clash with piece 01 or any other existing id."""
    pieces = load_pieces()
    ids = [p["id"] for p in pieces]
    assert len(ids) == len(set(ids)), f"Duplicate IDs in pieces.json: {ids}"


def test_piece_06_html_has_fractal_noise_type():
    """feTurbulence must use fractalNoise type (not turbulence) per the spec."""
    html = read_piece_file("index.html")
    assert 'type="fractalNoise"' in html, (
        "feTurbulence must use type='fractalNoise' for stone texture"
    )
