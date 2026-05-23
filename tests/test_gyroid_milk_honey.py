"""
Tests for piece 86-gyroid-milk-honey.

Verifies directory layout, pieces.json registration, essay content,
index.html implementation requirements, and thumbnail validity.
"""
import json
import math
import os
import re

import pytest

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID = "86-gyroid-milk-honey"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")


def load_pieces():
    """Return the parsed pieces.json list."""
    with open(PIECES_JSON, encoding="utf-8") as fh:
        return json.load(fh)


def get_piece():
    """Return the pieces.json entry for piece 86, or None."""
    for p in load_pieces():
        if p["id"] == PIECE_ID:
            return p
    return None


# ---------------------------------------------------------------------------
# Directory layout
# ---------------------------------------------------------------------------

def test_piece_directory_exists():
    assert os.path.isdir(PIECE_DIR), f"Piece directory {PIECE_DIR} not found"


def test_index_html_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "index.html"))


def test_essay_md_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "essay.md"))


def test_thumbnail_svg_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "thumbnail.svg"))


def test_readme_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "README.md"))


# ---------------------------------------------------------------------------
# pieces.json registration
# ---------------------------------------------------------------------------

def test_piece_registered_in_pieces_json():
    assert get_piece() is not None, f"'{PIECE_ID}' not found in pieces.json"


def test_piece_theme_contains_milk_and_honey():
    piece = get_piece()
    assert piece is not None
    assert "milk" in piece["theme"].lower() or "honey" in piece["theme"].lower(), (
        "theme must reference milk and honey"
    )


def test_piece_technique_mentions_gyroid():
    piece = get_piece()
    assert piece is not None
    assert "gyroid" in piece["technique"].lower(), (
        "technique must mention gyroid"
    )


def test_piece_paths_resolve():
    piece = get_piece()
    assert piece is not None
    for field in ("path", "thumbnail", "essay"):
        full = os.path.join(GALLERY_ROOT, piece[field])
        assert os.path.isfile(full), f"Field '{field}' path does not exist: {piece[field]}"


# ---------------------------------------------------------------------------
# essay.md content
# ---------------------------------------------------------------------------

def test_essay_word_count():
    """Essay must be at least 300 words."""
    essay = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    assert len(essay.split()) >= 300, "essay.md has fewer than 300 words"


def test_essay_mentions_exodus():
    essay = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    assert "Exodus" in essay or "exodus" in essay, "essay must reference Exodus 3:8"


def test_essay_mentions_deuteronomy_seven_species():
    essay = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    assert "Deuteronomy" in essay or "8:8" in essay, (
        "essay must mention Deuteronomy 8:8 and the seven species"
    )


def test_essay_mentions_talmud_date_honey():
    essay = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    lower = essay.lower()
    assert "megillah" in lower or "date honey" in lower or "date" in lower, (
        "essay must explain that dvash refers to date honey (Megillah 6a)"
    )


def test_essay_mentions_ketubot_or_redemption():
    essay = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    lower = essay.lower()
    assert "ketubot" in lower or "redemption" in lower, (
        "essay must mention Ketubot 111b or the eschatological reading"
    )


def test_essay_mentions_gyroid_or_minimal_surface():
    essay = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    lower = essay.lower()
    assert "gyroid" in lower or "minimal surface" in lower or "minimal-surface" in lower, (
        "essay must explain the gyroid as a minimal surface"
    )


# ---------------------------------------------------------------------------
# index.html implementation
# ---------------------------------------------------------------------------

def read_html():
    return open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()


def test_html_uses_imagedata():
    html = read_html()
    assert "ImageData" in html or "createImageData" in html or "putImageData" in html, (
        "index.html must use ImageData / putImageData for pixel rendering"
    )


def test_html_uses_requestanimationframe():
    html = read_html()
    assert "requestAnimationFrame" in html, "index.html must use requestAnimationFrame"


def test_html_has_gyroid_function():
    """The gyroid implicit function must appear in the JS."""
    html = read_html()
    assert "Math.sin" in html and "Math.cos" in html, (
        "index.html must implement the gyroid function using sin/cos"
    )


def test_html_uses_correct_scale():
    """Scale should be 8π."""
    html = read_html()
    assert "8 * Math.PI" in html or "8*Math.PI" in html, (
        "index.html must use scale = 8 * Math.PI"
    )


def test_html_advances_z_by_dt():
    """z must advance by approximately 0.008 per frame."""
    html = read_html()
    assert "0.008" in html, "index.html must advance z by 0.008 per frame"


def test_html_has_vignette():
    """The radial gradient vignette must be present."""
    html = read_html()
    assert "createRadialGradient" in html or "radialGradient" in html, (
        "index.html must add a radial gradient vignette overlay"
    )


def test_html_has_hebrew_text_overlay():
    """The Hebrew text overlay must be present."""
    html = read_html()
    assert "דְּבַשׁ" in html or "דבש" in html, (
        "index.html must overlay the Hebrew text דְּבַשׁ וְחָלָב"
    )


def test_html_embeds_essay_text():
    """index.html must embed the essay text (not rely on a runtime fetch)."""
    essay = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    html = read_html()
    words = [w for w in essay.split() if len(w) > 6][:12]
    found = sum(1 for w in words if w in html)
    assert found >= 6, (
        f"index.html does not appear to embed the essay text "
        f"(only {found}/12 sampled words found in HTML)"
    )


def test_html_has_cream_color():
    """The warm cream color for the gyroid surface walls must be referenced."""
    html = read_html()
    assert "FFF8E7" in html or "fff8e7" in html, (
        "index.html must use cream color #FFF8E7 for the gyroid surface"
    )


def test_html_has_amber_color():
    """The honey amber color must be referenced."""
    html = read_html()
    assert "C8780A" in html or "c8780a" in html or "0.12" in html, (
        "index.html must use amber colors for the gyroid positive region"
    )


# ---------------------------------------------------------------------------
# thumbnail.svg content
# ---------------------------------------------------------------------------

def test_thumbnail_is_valid_svg():
    svg = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert "<svg" in svg and "</svg>" in svg, "thumbnail.svg is not valid SVG"


def test_thumbnail_has_rect_elements():
    """The thumbnail must contain rect elements representing the gyroid grid."""
    svg = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert svg.count("<rect") >= 100, (
        "thumbnail.svg must contain at least 100 rect elements for the gyroid grid"
    )


def test_thumbnail_has_hebrew_letters():
    """The Hebrew letters דבש must appear faintly in the thumbnail."""
    svg = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert "דבש" in svg or "דְּבַשׁ" in svg, (
        "thumbnail.svg must include the Hebrew letters דבש"
    )


def test_thumbnail_is_400x400():
    svg = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert 'width="400"' in svg and 'height="400"' in svg, (
        "thumbnail.svg must be 400×400"
    )


# ---------------------------------------------------------------------------
# Gyroid function correctness (unit tests for the math)
# ---------------------------------------------------------------------------

def gyroid(x, y, z):
    """Python implementation of the gyroid implicit function."""
    return math.sin(x) * math.cos(y) + math.sin(y) * math.cos(z) + math.sin(z) * math.cos(x)


def test_gyroid_at_origin_is_zero():
    """The gyroid function is zero at the origin."""
    assert gyroid(0, 0, 0) == pytest.approx(0.0, abs=1e-12)


def test_gyroid_surface_threshold():
    """Points very close to a zero-crossing of the gyroid are near zero."""
    # z=0: g = sin(x)cos(y) + sin(y). At x=0, y=0: g=0.
    g = gyroid(0, 0, 0)
    assert abs(g) < 0.12, "Origin should be on the gyroid surface"


def test_gyroid_range_bounded():
    """The gyroid function is bounded within [-sqrt(3), sqrt(3)] ≈ [-1.732, 1.732]."""
    import random
    random.seed(42)
    SCALE = 8 * math.pi
    for _ in range(1000):
        x = random.uniform(0, SCALE)
        y = random.uniform(0, SCALE)
        z = random.uniform(0, SCALE)
        g = gyroid(x, y, z)
        assert -2.0 <= g <= 2.0, f"Gyroid value {g} out of expected range at ({x},{y},{z})"


def test_gyroid_is_triply_periodic():
    """The gyroid is 2π-periodic in all three coordinates."""
    x, y, z = 1.3, 2.7, 0.5
    g0 = gyroid(x, y, z)
    g_px = gyroid(x + 2 * math.pi, y, z)
    g_py = gyroid(x, y + 2 * math.pi, z)
    g_pz = gyroid(x, y, z + 2 * math.pi)
    assert g0 == pytest.approx(g_px, abs=1e-10)
    assert g0 == pytest.approx(g_py, abs=1e-10)
    assert g0 == pytest.approx(g_pz, abs=1e-10)


# ---------------------------------------------------------------------------
# Edge cases and failure modes
# ---------------------------------------------------------------------------

def test_essay_not_empty():
    essay = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read().strip()
    assert len(essay) > 0, "essay.md must not be empty"


def test_index_html_not_empty():
    html = read_html().strip()
    assert len(html) > 0, "index.html must not be empty"


def test_piece_id_is_unique():
    pieces = load_pieces()
    ids = [p["id"] for p in pieces]
    count = ids.count(PIECE_ID)
    assert count == 1, f"Piece ID '{PIECE_ID}' appears {count} times in pieces.json"


def test_html_does_not_fetch_essay_at_runtime():
    """index.html must not fetch essay.md at runtime (all content must be inline)."""
    html = read_html()
    assert "fetch(" not in html or "essay.md" not in html, (
        "index.html must not fetch essay.md at runtime — essay text must be inline"
    )
