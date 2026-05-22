"""
Tests for piece 51-am-segulah-boids (Am Segulah boids flocking simulation).

Covers the acceptance criteria: directory layout, index.html canvas animation,
essay content requirements, and pieces.json registration.
"""
import json
import os
import re

import pytest

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID = "51-am-segulah-boids"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")


def load_piece():
    """Return the pieces.json entry for 51-am-segulah-boids, or None."""
    with open(PIECES_JSON, encoding="utf-8") as fh:
        data = json.load(fh)
    for entry in data:
        if entry["id"] == PIECE_ID:
            return entry
    return None


def read_html():
    """Return the text of index.html."""
    return open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()


def read_essay():
    """Return the text of essay.md."""
    return open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()


# ---------------------------------------------------------------------------
# Directory and file layout
# ---------------------------------------------------------------------------

def test_piece_directory_exists():
    assert os.path.isdir(PIECE_DIR), f"Piece directory {PIECE_DIR} does not exist"


def test_index_html_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "index.html"))


def test_essay_md_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "essay.md"))


def test_readme_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "README.md"))


def test_thumbnail_svg_exists():
    thumb = os.path.join(PIECE_DIR, "thumbnail.svg")
    assert os.path.isfile(thumb)
    text = open(thumb, encoding="utf-8").read()
    assert "<svg" in text and "</svg>" in text


# ---------------------------------------------------------------------------
# pieces.json registration
# ---------------------------------------------------------------------------

def test_piece_registered_in_pieces_json():
    entry = load_piece()
    assert entry is not None, f"{PIECE_ID} not found in pieces.json"


def test_piece_required_fields_present():
    entry = load_piece()
    for field in ("id", "title", "tagline", "year", "theme", "technique", "path", "thumbnail", "essay"):
        assert field in entry, f"Field '{field}' missing from pieces.json entry"
        assert entry[field], f"Field '{field}' is empty in pieces.json entry"


def test_piece_theme_is_am_segulah():
    """Theme must be specific per orchestrator guidance — not generic 'Matan Torah'."""
    entry = load_piece()
    theme = entry["theme"].lower()
    assert "am segulah" in theme or "covenant" in theme, (
        f"Theme should be 'Am Segulah / Covenant', got: {entry['theme']!r}"
    )


def test_piece_technique_mentions_boids():
    entry = load_piece()
    assert "boids" in entry["technique"].lower(), (
        f"Technique must mention boids, got: {entry['technique']!r}"
    )


def test_piece_year_is_integer():
    entry = load_piece()
    assert isinstance(entry["year"], int)


# ---------------------------------------------------------------------------
# index.html — canvas animation
# ---------------------------------------------------------------------------

def test_index_html_uses_requestanimationframe():
    assert "requestAnimationFrame" in read_html()


def test_index_html_has_canvas_element():
    html = read_html()
    assert "<canvas" in html


def test_index_html_has_400_boids():
    """N = 400 must be declared in the simulation code."""
    html = read_html()
    assert "400" in html, "index.html must declare N = 400 boids"


def test_index_html_background_color():
    """Canvas background must be midnight blue #060A18."""
    html = read_html()
    assert "#060A18" in html or "060A18" in html.lower(), (
        "Background colour #060A18 not found in index.html"
    )


def test_index_html_gold_color():
    """Gold boid color #FFD700 must be used."""
    html = read_html()
    assert "FFD700" in html.upper()


def test_index_html_sinai_glow_amber():
    """Sinai glow uses deep amber #FF8C00."""
    html = read_html()
    assert "FF8C00" in html.upper()


def test_index_html_has_separation_radius():
    """SEP_R = 25 must appear in the code."""
    html = read_html()
    assert "25" in html, "Separation radius 25 not found in index.html"


def test_index_html_has_alignment_radius():
    """ALI_R = 50 must appear in the code."""
    html = read_html()
    assert "50" in html, "Alignment radius 50 not found in index.html"


def test_index_html_has_cohesion_radius():
    """COH_R = 80 must appear in the code."""
    html = read_html()
    assert "80" in html, "Cohesion radius 80 not found in index.html"


def test_index_html_has_sinai_radius_fraction():
    """Sinai radius must be set to ~15% of canvas width."""
    html = read_html()
    assert "0.15" in html, "Sinai radius fraction 0.15 not found in index.html"


def test_index_html_uses_float32array():
    """Float32Array buffers must be used for cache-friendly boid state."""
    html = read_html()
    assert "Float32Array" in html


def test_index_html_has_hebrew_watermark():
    """Hebrew phrase must appear as a watermark on the canvas."""
    html = read_html()
    assert "כְּאִישׁ אֶחָד בְּלֵב אֶחָד" in html


def test_index_html_has_soft_trail_clear():
    """Partial alpha clear (rgba with alpha < 1) produces motion trails."""
    html = read_html()
    assert "rgba(6,10,24" in html or "rgba(6, 10, 24" in html, (
        "Soft trail clear using rgba(6,10,24,…) not found in index.html"
    )


def test_index_html_has_12_clusters():
    """Boids must be initialised in 12 clusters (one per tribe)."""
    html = read_html()
    assert "12" in html, "12 initial clusters not referenced in index.html"


def test_index_html_wraps_at_edges():
    """Position wrapping at canvas edges must be implemented."""
    html = read_html()
    assert "+= W" in html or "+= H" in html or "-= W" in html or "-= H" in html, (
        "Edge wrapping code not found in index.html"
    )


# ---------------------------------------------------------------------------
# essay.md content
# ---------------------------------------------------------------------------

def test_essay_at_least_300_words():
    text = read_essay()
    word_count = len(text.split())
    assert word_count >= 300, f"Essay has only {word_count} words (need ≥ 300)"


def test_essay_cites_exodus_19_2():
    text = read_essay()
    assert "19:2" in text or "Exodus 19" in text, "Essay must cite Exodus 19:2"


def test_essay_cites_exodus_19_5_6():
    text = read_essay()
    assert "19:5" in text or "19:6" in text or "Am Segulah" in text or "am segulah" in text.lower(), (
        "Essay must cite Exodus 19:5-6 (Am Segulah)"
    )


def test_essay_cites_mechilta():
    text = read_essay()
    assert "Mekhilta" in text or "Mechilta" in text or "Yitro 9" in text, (
        "Essay must cite Mechilta d'Rabbi Yishmael, Yitro 9"
    )


def test_essay_cites_shemot_rabbah():
    text = read_essay()
    assert "Shemot Rabbah" in text or "28:6" in text, (
        "Essay must cite Shemot Rabbah 28:6"
    )


def test_essay_mentions_kingdom_of_priests():
    text = read_essay()
    assert "kingdom of priests" in text.lower() or "mamlekhet kohanim" in text.lower(), (
        "Essay must discuss 'kingdom of priests' (Exodus 19:6)"
    )


def test_essay_mentions_boids_or_simulation():
    text = read_essay()
    assert "boid" in text.lower() or "simulation" in text.lower() or "flock" in text.lower(), (
        "Essay must connect the simulation to the theological theme"
    )


def test_essay_mentions_naaseh_vnishma():
    text = read_essay()
    assert "na'aseh" in text.lower() or "naaseh" in text.lower(), (
        "Essay must mention na'aseh v'nishmah"
    )


def test_essay_embedded_in_html():
    """Words from essay.md must appear in index.html (embedded, not fetched)."""
    essay = read_essay()
    html = read_html()
    words = [w for w in essay.split() if len(w) > 6][:15]
    found = sum(1 for w in words if w in html)
    assert found >= 8, (
        f"Only {found}/15 essay words found in index.html — essay must be embedded"
    )


# ---------------------------------------------------------------------------
# Edge cases and failure modes
# ---------------------------------------------------------------------------

def test_no_duplicate_piece_id():
    """Piece ID must be unique across pieces.json."""
    with open(PIECES_JSON, encoding="utf-8") as fh:
        data = json.load(fh)
    ids = [e["id"] for e in data]
    assert ids.count(PIECE_ID) == 1, f"Duplicate entry for {PIECE_ID} in pieces.json"


def test_piece_path_resolves_to_existing_file():
    entry = load_piece()
    full_path = os.path.join(GALLERY_ROOT, entry["path"])
    assert os.path.isfile(full_path), f"path '{entry['path']}' does not resolve to a file"


def test_piece_thumbnail_resolves_to_existing_file():
    entry = load_piece()
    full_path = os.path.join(GALLERY_ROOT, entry["thumbnail"])
    assert os.path.isfile(full_path), f"thumbnail '{entry['thumbnail']}' does not resolve to a file"


def test_piece_essay_path_resolves_to_existing_file():
    entry = load_piece()
    full_path = os.path.join(GALLERY_ROOT, entry["essay"])
    assert os.path.isfile(full_path), f"essay '{entry['essay']}' does not resolve to a file"


def test_html_has_no_external_script_fetch():
    """index.html must not load essay.md via fetch — it must be inline."""
    html = read_html()
    assert "fetch" not in html or "essay.md" not in html, (
        "index.html must not fetch essay.md at runtime — embed it inline"
    )


def test_essay_has_rashi_gloss():
    """Essay must explicitly reference Rashi's gloss."""
    text = read_essay()
    assert "Rashi" in text or "rashi" in text.lower(), "Essay must mention Rashi's gloss on Exodus 19:2"
