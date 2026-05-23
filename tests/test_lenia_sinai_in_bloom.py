"""
Tests for piece 80-lenia-sinai-in-bloom (Lenia continuous cellular automaton).

Validates that the piece directory is correctly structured, that pieces.json
is updated with the right theme and technique fields, and that the index.html
implements the required Lenia parameters.
"""
import json
import os
import re

import pytest

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID = "80-lenia-sinai-in-bloom"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_pieces():
    """Return the parsed pieces.json list."""
    with open(PIECES_JSON, "r", encoding="utf-8") as fh:
        return json.load(fh)


def get_piece():
    """Return the pieces.json entry for the Lenia piece, or None."""
    for p in load_pieces():
        if p["id"] == PIECE_ID:
            return p
    return None


def read_file(rel):
    """Read a file relative to the gallery root and return its text."""
    with open(os.path.join(GALLERY_ROOT, rel), "r", encoding="utf-8") as fh:
        return fh.read()


# ---------------------------------------------------------------------------
# Directory and file existence
# ---------------------------------------------------------------------------

def test_piece_directory_exists():
    assert os.path.isdir(PIECE_DIR), f"Piece directory {PIECE_DIR} does not exist"


def test_index_html_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "index.html")), \
        "index.html missing from piece directory"


def test_essay_md_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "essay.md")), \
        "essay.md missing from piece directory"


def test_thumbnail_svg_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "thumbnail.svg")), \
        "thumbnail.svg missing from piece directory"


def test_readme_md_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "README.md")), \
        "README.md missing from piece directory"


# ---------------------------------------------------------------------------
# pieces.json registration
# ---------------------------------------------------------------------------

def test_piece_registered_in_pieces_json():
    assert get_piece() is not None, \
        f"Piece '{PIECE_ID}' not found in pieces.json"


def test_piece_theme_contains_greenery():
    piece = get_piece()
    assert piece is not None
    theme = piece.get("theme", "").lower()
    assert "greenery" in theme or "flowers" in theme or "bloom" in theme, \
        f"theme '{piece['theme']}' should mention greenery/flowers/bloom"


def test_piece_technique_contains_lenia():
    piece = get_piece()
    assert piece is not None
    technique = piece.get("technique", "").lower()
    assert "lenia" in technique, \
        f"technique '{piece['technique']}' must mention Lenia"


def test_piece_technique_contains_convolution():
    piece = get_piece()
    assert piece is not None
    technique = piece.get("technique", "").lower()
    assert "convolution" in technique or "kernel" in technique, \
        f"technique '{piece['technique']}' must mention kernel/convolution"


def test_piece_path_points_to_html():
    piece = get_piece()
    assert piece is not None
    assert piece["path"].endswith(".html"), "path must end with .html"
    full = os.path.join(GALLERY_ROOT, piece["path"])
    assert os.path.isfile(full), f"path '{piece['path']}' does not exist on disk"


def test_piece_thumbnail_points_to_svg():
    piece = get_piece()
    assert piece is not None
    full = os.path.join(GALLERY_ROOT, piece["thumbnail"])
    assert os.path.isfile(full), f"thumbnail '{piece['thumbnail']}' does not exist on disk"


def test_piece_essay_field_points_to_existing_file():
    piece = get_piece()
    assert piece is not None
    full = os.path.join(GALLERY_ROOT, piece["essay"])
    assert os.path.isfile(full), f"essay '{piece['essay']}' does not exist on disk"


# ---------------------------------------------------------------------------
# essay.md content
# ---------------------------------------------------------------------------

def test_essay_mentions_pirkei_de_rabbi_eliezer():
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    assert "Pirkei" in text or "pirkei" in text, \
        "essay.md must reference Pirkei de-Rabbi Eliezer"


def test_essay_mentions_shir_hashirim():
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    assert "Shir" in text or "Song of Songs" in text, \
        "essay.md must reference Song of Songs / Shir HaShirim"


def test_essay_mentions_lenia():
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    assert "Lenia" in text or "lenia" in text, \
        "essay.md must mention Lenia"


def test_essay_at_least_350_words():
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    word_count = len(text.split())
    assert word_count >= 350, \
        f"essay.md has only {word_count} words; the suggestion calls for ~380 words"


def test_essay_mentions_ashkenazi_custom():
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read().lower()
    assert "ashkenaz" in text or "synagogue" in text or "flowers" in text, \
        "essay.md must mention the Ashkenazi custom of flowers/greenery"


# ---------------------------------------------------------------------------
# index.html — Lenia implementation checks
# ---------------------------------------------------------------------------

def test_index_html_uses_requestanimationframe():
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "requestAnimationFrame" in html, \
        "index.html must use requestAnimationFrame for the animation loop"


def test_index_html_has_float32array_grid():
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "Float32Array" in html, \
        "index.html must use Float32Array for the state grid"


def test_index_html_has_grid_size_128():
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert re.search(r'\b128\b', html), \
        "index.html must declare N=128 (128×128 grid)"


def test_index_html_has_kernel_radius_7():
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert re.search(r'\bR\s*=\s*7\b', html) or "= 7" in html, \
        "index.html must set kernel radius R=7"


def test_index_html_has_mu_015():
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "0.15" in html, \
        "index.html must define mu=0.15 (Orbium growth parameter)"


def test_index_html_has_sigma_0017():
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "0.017" in html, \
        "index.html must define sigma=0.017 (Orbium growth parameter)"


def test_index_html_has_dt_01():
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "0.1" in html, \
        "index.html must define dt=0.1 (integration time step)"


def test_index_html_has_ring_kernel_construction():
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "0.5" in html and "1.0" in html, \
        "index.html must define the ring kernel bounds (r >= 0.5 to r <= 1.0)"


def test_index_html_has_toroidal_wrap():
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "% N" in html, \
        "index.html must implement toroidal wrap using modulo N"


def test_index_html_has_forest_green_color():
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "1A3020" in html or "1a3020" in html, \
        "index.html must use forest green #1A3020 as the zero-state color"


def test_index_html_has_pale_gold_color():
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "D4C060" in html or "d4c060" in html, \
        "index.html must use pale gold #D4C060 as the high-state color"


def test_index_html_has_imagedata_rendering():
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "ImageData" in html or "createImageData" in html or "putImageData" in html, \
        "index.html must use ImageData for pixel-level rendering"


def test_index_html_has_autoreseed_logic():
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "300" in html and "seed" in html.lower(), \
        "index.html must auto-reseed if population collapses after ~300 frames"


def test_index_html_embeds_essay_text():
    essay = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    words = [w for w in essay.split() if len(w) > 6][:15]
    found = sum(1 for w in words if w in html)
    assert found >= 8, \
        f"index.html must embed essay text (only {found}/{len(words)} sampled words found)"


# ---------------------------------------------------------------------------
# thumbnail.svg
# ---------------------------------------------------------------------------

def test_thumbnail_is_valid_svg():
    text = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert "<svg" in text and "</svg>" in text, \
        "thumbnail.svg does not look like valid SVG"


def test_thumbnail_has_green_background():
    text = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert "1A3020" in text or "1a3020" in text, \
        "thumbnail.svg must use #1A3020 as the green field background"


def test_thumbnail_has_golden_flowers():
    text = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert "D4C060" in text or "d4c060" in text, \
        "thumbnail.svg must include golden petal elements (#D4C060)"


def test_thumbnail_has_ellipses_for_petals():
    text = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert "<ellipse" in text, \
        "thumbnail.svg must use <ellipse> elements for flower petals"


def test_thumbnail_has_400x400_viewbox():
    text = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert "400" in text, \
        "thumbnail.svg must be 400×400"


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

def test_piece_id_has_no_duplicate_in_pieces_json():
    pieces = load_pieces()
    ids = [p["id"] for p in pieces]
    assert ids.count(PIECE_ID) == 1, \
        f"Piece '{PIECE_ID}' appears more than once in pieces.json"


def test_piece_year_is_2026():
    piece = get_piece()
    assert piece is not None
    assert piece["year"] == 2026, f"Expected year 2026, got {piece['year']}"


def test_essay_does_not_exceed_1500_words():
    """Sanity upper-bound — essay should be focused, not a dissertation."""
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    word_count = len(text.split())
    assert word_count <= 1500, \
        f"essay.md has {word_count} words — suspiciously long, check for duplication"


def test_index_html_no_external_script_imports():
    """Self-contained piece: no <script src=...> tags loading external CDNs."""
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    external = re.findall(r'<script[^>]+src=["\']https?://', html, re.IGNORECASE)
    assert len(external) == 0, \
        f"index.html must not load external scripts: {external}"
