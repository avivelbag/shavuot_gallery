"""
Tests for piece 87-lloyd-relaxation-flowers.

Validates the directory layout, pieces.json registration, essay content,
HTML structure, and expected algorithmic keywords in the source code.
"""
import json
import os

import pytest

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID = "87-lloyd-relaxation-flowers"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
INDEX_HTML = os.path.join(PIECE_DIR, "index.html")
ESSAY_MD = os.path.join(PIECE_DIR, "essay.md")
THUMBNAIL_SVG = os.path.join(PIECE_DIR, "thumbnail.svg")
README_MD = os.path.join(PIECE_DIR, "README.md")
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def _load_pieces():
    with open(PIECES_JSON, encoding="utf-8") as fh:
        return json.load(fh)


def _get_piece():
    return next((p for p in _load_pieces() if p["id"] == PIECE_ID), None)


# ---------------------------------------------------------------------------
# File layout — acceptance criterion: directory with all required files
# ---------------------------------------------------------------------------

def test_piece_directory_exists():
    assert os.path.isdir(PIECE_DIR), f"Piece directory {PIECE_DIR} does not exist"


def test_index_html_exists():
    assert os.path.isfile(INDEX_HTML), "index.html missing from piece directory"


def test_essay_md_exists():
    assert os.path.isfile(ESSAY_MD), "essay.md missing from piece directory"


def test_thumbnail_svg_exists():
    assert os.path.isfile(THUMBNAIL_SVG), "thumbnail.svg missing from piece directory"


def test_readme_md_exists():
    assert os.path.isfile(README_MD), "README.md missing from piece directory"


# ---------------------------------------------------------------------------
# pieces.json registration
# ---------------------------------------------------------------------------

def test_piece_registered_in_pieces_json():
    piece = _get_piece()
    assert piece is not None, f"Piece '{PIECE_ID}' not found in pieces.json"


def test_pieces_json_theme_field():
    piece = _get_piece()
    assert piece is not None
    assert "Greenery" in piece["theme"] or "flowers" in piece["theme"].lower(), (
        "theme field must reference 'Greenery and flowers'"
    )


def test_pieces_json_technique_field():
    piece = _get_piece()
    assert piece is not None
    assert "Lloyd" in piece["technique"] or "Voronoi" in piece["technique"], (
        "technique field must reference Lloyd's relaxation or Centroidal Voronoi"
    )


def test_pieces_json_path_correct():
    piece = _get_piece()
    assert piece is not None
    assert piece["path"] == f"pieces/{PIECE_ID}/index.html"


def test_pieces_json_thumbnail_correct():
    piece = _get_piece()
    assert piece is not None
    assert piece["thumbnail"] == f"pieces/{PIECE_ID}/thumbnail.svg"


def test_pieces_json_essay_correct():
    piece = _get_piece()
    assert piece is not None
    assert piece["essay"] == f"pieces/{PIECE_ID}/essay.md"


def test_pieces_json_no_duplicate_ids_after_addition():
    pieces = _load_pieces()
    ids = [p["id"] for p in pieces]
    assert len(ids) == len(set(ids)), f"Duplicate IDs found after addition: {ids}"


# ---------------------------------------------------------------------------
# essay.md content
# ---------------------------------------------------------------------------

def test_essay_substantial_length():
    text = _read(ESSAY_MD)
    word_count = len(text.split())
    assert word_count >= 300, (
        f"essay.md has only {word_count} words; expected at least 300"
    )


def test_essay_mentions_rama():
    text = _read(ESSAY_MD)
    assert "Rama" in text or "Orach Chaim" in text, (
        "essay.md must mention the Rama's ruling in Orach Chaim 494:3"
    )


def test_essay_mentions_shir_hashirim_rabbah():
    text = _read(ESSAY_MD)
    assert "Shir HaShirim Rabbah" in text or "Shir Ha" in text, (
        "essay.md must cite Shir HaShirim Rabbah"
    )


def test_essay_mentions_pirkei_derabbi_eliezer():
    text = _read(ESSAY_MD)
    assert "Pirkei" in text or "DeRabbi Eliezer" in text, (
        "essay.md must reference Pirkei DeRabbi Eliezer"
    )


def test_essay_mentions_shabbat():
    text = _read(ESSAY_MD)
    assert "Shabbat" in text or "Shabbat 88" in text, (
        "essay.md must cite Shabbat 88b"
    )


def test_essay_contains_sinai_bloom_theme():
    text = _read(ESSAY_MD)
    lower = text.lower()
    assert "bloom" in lower or "flowers" in lower or "flower" in lower, (
        "essay.md must discuss the flowering of Sinai at revelation"
    )


# ---------------------------------------------------------------------------
# index.html — canvas, algorithm, and animation requirements
# ---------------------------------------------------------------------------

def test_index_html_has_canvas():
    html = _read(INDEX_HTML)
    assert "<canvas" in html, "index.html must contain a <canvas> element"


def test_index_html_uses_requestanimationframe():
    html = _read(INDEX_HTML)
    assert "requestAnimationFrame" in html, (
        "index.html must use requestAnimationFrame for animation"
    )


def test_index_html_seeds_280_points():
    html = _read(INDEX_HTML)
    assert "280" in html, (
        "index.html must seed 280 random points (constant N = 280)"
    )


def test_index_html_lloyd_iteration_present():
    """The Lloyd iteration logic must be present (centroid computation and seed update)."""
    html = _read(INDEX_HTML)
    assert "centroid" in html.lower() or "computeCentroids" in html or "sumX" in html, (
        "index.html must implement centroid computation for Lloyd iterations"
    )


def test_index_html_voronoi_assignment_present():
    html = _read(INDEX_HTML)
    assert "assignment" in html or "computeAssignment" in html or "nearest" in html.lower(), (
        "index.html must implement Voronoi cell assignment"
    )


def test_index_html_max_60_iterations():
    html = _read(INDEX_HTML)
    assert "60" in html, (
        "index.html must stop after 60 Lloyd iterations"
    )


def test_index_html_convergence_threshold():
    html = _read(INDEX_HTML)
    assert "0.5" in html, (
        "index.html must include 0.5px convergence threshold"
    )


def test_index_html_phase_relaxing():
    html = _read(INDEX_HTML)
    assert "'relaxing'" in html or '"relaxing"' in html, (
        "index.html must use a 'relaxing' phase variable"
    )


def test_index_html_phase_blooming():
    html = _read(INDEX_HTML)
    assert "'blooming'" in html or '"blooming"' in html, (
        "index.html must use a 'blooming' phase variable"
    )


def test_index_html_phase_breathing():
    html = _read(INDEX_HTML)
    assert "'breathing'" in html or '"breathing"' in html, (
        "index.html must use a 'breathing' phase variable"
    )


def test_index_html_petal_drawing():
    html = _read(INDEX_HTML)
    assert "ellipse" in html, (
        "index.html must draw elliptical petals using ctx.ellipse()"
    )


def test_index_html_five_flower_types():
    """Five flower types must be present; accept either hex or decimal RGB representations."""
    html = _read(INDEX_HTML)
    html_lower = html.lower()
    # White anemone #FAFAF2 = rgb(250,250,242)
    assert "FAFAF2" in html or "fafaf2" in html_lower or "250, 250, 242" in html or "250,250,242" in html, (
        "white anemone petal colour (#FAFAF2 / 250,250,242) missing"
    )
    # Purple iris #7B5EA7 = rgb(123,94,167)
    assert "7B5EA7" in html or "7b5ea7" in html_lower or "123, 94, 167" in html or "123,94,167" in html, (
        "purple iris petal colour (#7B5EA7 / 123,94,167) missing"
    )
    # Soft pink rose #F4B8C1 = rgb(244,184,193)
    assert "F4B8C1" in html or "f4b8c1" in html_lower or "244, 184, 193" in html or "244,184,193" in html, (
        "soft pink rose petal colour (#F4B8C1 / 244,184,193) missing"
    )
    # Field yellow #F5E642 = rgb(245,230,66)
    assert "F5E642" in html or "f5e642" in html_lower or "245, 230, 66" in html or "245,230,66" in html, (
        "field yellow petal colour (#F5E642 / 245,230,66) missing"
    )
    # Pale blue cornflower #A8C4E0 = rgb(168,196,224)
    assert "A8C4E0" in html or "a8c4e0" in html_lower or "168, 196, 224" in html or "168,196,224" in html, (
        "cornflower blue petal colour (#A8C4E0 / 168,196,224) missing"
    )


def test_index_html_botanical_green_background():
    html = _read(INDEX_HTML)
    assert "1A2E1A" in html or "1a2e1a" in html.lower(), (
        "index.html must use deep botanical green #1A2E1A as background"
    )


def test_index_html_shadow_blur_for_glow():
    html = _read(INDEX_HTML)
    assert "shadowBlur" in html, (
        "index.html must set ctx.shadowBlur for petal glow effect"
    )


def test_index_html_breathing_sine_wave():
    """Petals must breathe using a sine wave at 0.4 Hz."""
    html = _read(INDEX_HTML)
    assert "Math.sin" in html, "breathing animation must use Math.sin"
    assert "0.4" in html or "0.05" in html, (
        "breathing scale must reference 0.4 Hz frequency or ±5 % amplitude"
    )


def test_index_html_iter_interval_250ms():
    html = _read(INDEX_HTML)
    assert "250" in html, (
        "index.html must pause 250ms between Lloyd iterations"
    )


def test_index_html_essay_embedded():
    """The essay must be embedded inline, not fetched at runtime."""
    essay_text = _read(ESSAY_MD)
    html = _read(INDEX_HTML)
    words = [w for w in essay_text.split() if len(w) > 5]
    sampled = words[:10]
    found = sum(1 for w in sampled if w in html)
    assert found >= 5, (
        f"index.html must embed the essay inline; only {found}/10 sampled words found"
    )


# ---------------------------------------------------------------------------
# thumbnail.svg
# ---------------------------------------------------------------------------

def test_thumbnail_is_svg():
    text = _read(THUMBNAIL_SVG)
    assert "<svg" in text and "</svg>" in text, "thumbnail.svg must be valid SVG"


def test_thumbnail_has_green_background():
    text = _read(THUMBNAIL_SVG)
    assert "1A2E1A" in text or "1a2e1a" in text.lower(), (
        "thumbnail.svg must have the #1A2E1A botanical-green background"
    )


def test_thumbnail_contains_flower_colours():
    text = _read(THUMBNAIL_SVG)
    assert "FAFAF2" in text or "fafaf2" in text.lower(), "white anemone colour missing from thumbnail"
    assert "7B5EA7" in text or "7b5ea7" in text.lower(), "purple iris colour missing from thumbnail"
    assert "F4B8C1" in text or "f4b8c1" in text.lower(), "soft pink rose colour missing from thumbnail"


def test_thumbnail_has_multiple_flowers():
    text = _read(THUMBNAIL_SVG)
    use_count = text.count("<use ")
    assert use_count >= 20, (
        f"thumbnail.svg should have at least 20 flower instances (<use> elements); found {use_count}"
    )


# ---------------------------------------------------------------------------
# Edge cases and failure modes
# ---------------------------------------------------------------------------

def test_essay_md_word_count_not_too_short():
    """Guard against stub essays that are shorter than the gallery minimum."""
    text = _read(ESSAY_MD)
    word_count = len(text.split())
    assert word_count >= 200, (
        f"essay.md has only {word_count} words; gallery minimum is 200"
    )


def test_index_html_imagedata_used():
    """Pixel-level Voronoi rendering must use ImageData for performance."""
    html = _read(INDEX_HTML)
    assert "ImageData" in html or "createImageData" in html or "putImageData" in html, (
        "index.html must use ImageData for efficient pixel-level Voronoi rendering"
    )


def test_pieces_json_still_valid_json():
    """Adding the new entry must not corrupt pieces.json."""
    with open(PIECES_JSON, encoding="utf-8") as fh:
        data = json.load(fh)
    assert isinstance(data, list) and len(data) >= 1


def test_piece_path_exists_on_disk():
    piece = _get_piece()
    assert piece is not None
    full_path = os.path.join(GALLERY_ROOT, piece["path"])
    assert os.path.isfile(full_path), f"Path {piece['path']} does not exist on disk"


def test_thumbnail_path_exists_on_disk():
    piece = _get_piece()
    assert piece is not None
    full_thumb = os.path.join(GALLERY_ROOT, piece["thumbnail"])
    assert os.path.isfile(full_thumb), f"Thumbnail {piece['thumbnail']} does not exist on disk"
