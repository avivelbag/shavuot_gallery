"""
Tests for piece 96-simulated-annealing-sinai: "The Fire That Does Not Consume".

Validates directory layout, pieces.json registration, essay content,
index.html completeness, and thumbnail SVG validity.
"""
import json
import os

import pytest

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID = "96-simulated-annealing-sinai"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")


# ── helpers ───────────────────────────────────────────────────────────────────

def load_pieces():
    with open(PIECES_JSON, encoding="utf-8") as fh:
        return json.load(fh)


def get_piece():
    return next((p for p in load_pieces() if p["id"] == PIECE_ID), None)


# ── directory and file existence ──────────────────────────────────────────────

def test_piece_directory_exists():
    assert os.path.isdir(PIECE_DIR), f"Missing piece directory: {PIECE_DIR}"


def test_index_html_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "index.html"))


def test_essay_md_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "essay.md"))


def test_thumbnail_svg_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "thumbnail.svg"))


def test_readme_md_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "README.md"))


# ── pieces.json registration ──────────────────────────────────────────────────

def test_piece_registered_in_pieces_json():
    piece = get_piece()
    assert piece is not None, f"Piece '{PIECE_ID}' not found in pieces.json"


def test_piece_required_fields_present():
    piece = get_piece()
    required = ("id", "title", "tagline", "year", "theme", "technique", "path", "thumbnail", "essay")
    for field in required:
        assert field in piece and piece[field], f"Missing or empty field '{field}' in pieces.json entry"


def test_piece_theme_matches_acceptance():
    piece = get_piece()
    assert "Matan Torah" in piece["theme"] or "Har Sinai" in piece["theme"], (
        "theme must reference 'Matan Torah / Har Sinai'"
    )


def test_piece_technique_mentions_annealing():
    piece = get_piece()
    assert "annealing" in piece["technique"].lower(), (
        "technique field must mention simulated annealing"
    )


def test_piece_year_is_integer():
    piece = get_piece()
    assert isinstance(piece["year"], int)


# ── essay content ─────────────────────────────────────────────────────────────

def test_essay_word_count_at_least_420():
    essay_path = os.path.join(PIECE_DIR, "essay.md")
    text = open(essay_path, encoding="utf-8").read()
    word_count = len(text.split())
    assert word_count >= 420, f"Essay has {word_count} words; need ≥ 420"


def test_essay_mentions_deuteronomy():
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    assert "Deuteronomy" in text or "4:11" in text, (
        "essay must cite Deuteronomy 4:11-12"
    )


def test_essay_mentions_midrash():
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read().lower()
    assert "midrash" in text or "shemot rabbah" in text, (
        "essay must mention the Midrash / Shemot Rabbah"
    )


def test_essay_mentions_kirkpatrick():
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    assert "Kirkpatrick" in text or "1983" in text, (
        "essay must reference Kirkpatrick et al. 1983"
    )


def test_essay_mentions_cooling():
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read().lower()
    assert "cool" in text or "anneal" in text, (
        "essay must explain the cooling / annealing concept"
    )


# ── index.html content ────────────────────────────────────────────────────────

def test_index_html_uses_request_animation_frame():
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "requestAnimationFrame" in html


def test_index_html_has_canvas_element():
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "<canvas" in html


def test_index_html_embeds_essay_text():
    essay = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    html  = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    words = [w for w in essay.split() if len(w) > 5]
    sampled = words[:10]
    found = sum(1 for w in sampled if w in html)
    assert found >= 5, (
        f"index.html does not appear to embed the essay (only {found}/10 sampled words found)"
    )


def test_index_html_mentions_temperature():
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "T_MAX" in html or "T_max" in html or "T_MAX" in html or "temperature" in html.lower()


def test_index_html_has_particle_count():
    """N=2000 particles must be configured in the simulation."""
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "2000" in html, "index.html must configure N=2000 particles"


def test_index_html_has_fire_colour():
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read().upper()
    assert "FF4500" in html or "FF8C00" in html, (
        "index.html must use fire orange-red colour (#FF4500 or #FF8C00)"
    )


def test_index_html_has_indigo_colour():
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read().upper()
    assert "1C1864" in html or "4B0082" in html, (
        "index.html must use deep indigo colour (#1C1864 or #4B0082)"
    )


def test_index_html_has_lighter_compositing():
    """Glow bloom requires ctx.globalCompositeOperation = 'lighter'."""
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "lighter" in html


def test_index_html_has_spatial_hash_grid():
    """Performance requires a spatial hash grid, not O(N²) pairwise."""
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "grid" in html.lower() or "CELL" in html or "cellOf" in html


def test_index_html_has_hexagonal_lattice():
    """Crystal formation requires hexagonal lattice targeting."""
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "lattice" in html.lower() or "sqrt(3)" in html or "1.732" in html


def test_index_html_has_spring_force():
    """Spring force toward lattice targets is required for crystal lock-in."""
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "spring" in html.lower() or "SPRING" in html or "springK" in html


def test_index_html_has_metropolis_criterion():
    """Metropolis-Hastings acceptance criterion: exp(-dE/T)."""
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "exp(" in html or "Math.exp" in html


def test_index_html_has_loop_reset():
    """The animation must loop — reset T to T_MAX and re-scatter."""
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "T_MAX" in html or "scatter" in html or "reset" in html.lower()


# ── thumbnail SVG validity ────────────────────────────────────────────────────

def test_thumbnail_is_valid_svg():
    text = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert "<svg" in text and "</svg>" in text


def test_thumbnail_has_400x400_dimensions():
    text = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert 'width="400"' in text and 'height="400"' in text


def test_thumbnail_has_diagonal_divider():
    """Gold diagonal line divides the two temperature panels."""
    text = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read().upper()
    assert "<LINE" in text or "<line" in text.lower(), (
        "thumbnail must contain a diagonal line element"
    )
    assert "D4A017" in text or "FFD700" in text or "GOLD" in text, (
        "thumbnail diagonal line must be gold-coloured"
    )


def test_thumbnail_has_both_panels():
    """Thumbnail must show scattered (hot) and lattice (cool) panels."""
    text = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read().upper()
    assert "2A0A00" in text or "FF4500" in text  # hot panel background / particles
    assert "050A1A" in text or "4B0082" in text  # cool panel background / particles


# ── edge cases ────────────────────────────────────────────────────────────────

def test_no_duplicate_id_in_pieces_json():
    """Duplicate IDs break gallery routing."""
    pieces = load_pieces()
    ids = [p["id"] for p in pieces]
    assert ids.count(PIECE_ID) == 1, f"Piece '{PIECE_ID}' appears more than once in pieces.json"


def test_essay_path_matches_pieces_json():
    piece = get_piece()
    expected = f"pieces/{PIECE_ID}/essay.md"
    assert piece["essay"] == expected, (
        f"essay path in pieces.json '{piece['essay']}' != '{expected}'"
    )


def test_thumbnail_path_matches_pieces_json():
    piece = get_piece()
    expected = f"pieces/{PIECE_ID}/thumbnail.svg"
    assert piece["thumbnail"] == expected


def test_index_html_path_matches_pieces_json():
    piece = get_piece()
    expected = f"pieces/{PIECE_ID}/index.html"
    assert piece["path"] == expected


def test_essay_does_not_mention_ising_model():
    """Per spec: this is NOT an Ising physics simulation — annealing is the narrative spine."""
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read().lower()
    assert "ising model" not in text, (
        "essay should not describe an Ising model; this piece is about simulated annealing"
    )


def test_index_html_has_gaussian_perturbation():
    """Proposal moves must be Gaussian noise with sigma proportional to T."""
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "gauss" in html.lower() or "box-muller" in html.lower() or "gaussRand" in html
