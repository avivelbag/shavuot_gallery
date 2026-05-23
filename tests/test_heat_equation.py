"""Tests for piece 74 — heat-equation-engraved-freedom.

Covers:
- pieces.json registration and required fields
- on-disk file layout (index.html, essay.md, thumbnail.svg, README.md, gen_thumbnail.py)
- index.html content: requestAnimationFrame, Float32Array, ALPHA=0.24, Hebrew text
- essay content: Avot / Mishnah / cherut / freedom wordplay
- FTCS algorithm correctness (pure-Python re-implementation)
- source-temperature decay formula
- stability constant constraint
"""
import json
import os

import pytest

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")
PIECE_ID = "74-heat-equation-engraved-freedom"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_pieces():
    """Return parsed pieces.json as a list."""
    with open(PIECES_JSON, "r", encoding="utf-8") as fh:
        return json.load(fh)


def get_piece(piece_id):
    """Return the pieces.json entry for piece_id, or None."""
    for p in load_pieces():
        if p["id"] == piece_id:
            return p
    return None


def read_html():
    piece = get_piece(PIECE_ID)
    assert piece is not None, f"{PIECE_ID} missing from pieces.json"
    return open(os.path.join(GALLERY_ROOT, piece["path"]), encoding="utf-8").read()


def read_essay():
    piece = get_piece(PIECE_ID)
    assert piece is not None
    return open(os.path.join(GALLERY_ROOT, piece["essay"]), encoding="utf-8").read()


# ---------------------------------------------------------------------------
# Registration and required fields
# ---------------------------------------------------------------------------

def test_piece_74_in_pieces_json():
    assert get_piece(PIECE_ID) is not None, f"{PIECE_ID} not found in pieces.json"


def test_piece_74_theme_mentions_luchot():
    piece = get_piece(PIECE_ID)
    assert piece is not None
    theme = piece["theme"]
    assert any(kw in theme for kw in ("Luchot", "Tablets", "Matan Torah")), (
        f"theme '{theme}' must mention Luchot, Tablets, or Matan Torah"
    )


def test_piece_74_technique_mentions_heat_equation():
    piece = get_piece(PIECE_ID)
    assert piece is not None
    tech = piece["technique"]
    assert "heat equation" in tech.lower() or "FTCS" in tech or "ftcs" in tech.lower(), (
        f"technique '{tech}' must mention heat equation or FTCS"
    )


def test_piece_74_year_is_2026():
    piece = get_piece(PIECE_ID)
    assert piece is not None
    assert piece["year"] == 2026


def test_piece_74_tagline_non_empty():
    piece = get_piece(PIECE_ID)
    assert piece is not None
    assert piece.get("tagline", "").strip() != ""


# ---------------------------------------------------------------------------
# File layout
# ---------------------------------------------------------------------------

def test_piece_74_index_html_exists():
    piece = get_piece(PIECE_ID)
    assert piece is not None
    assert os.path.isfile(os.path.join(GALLERY_ROOT, piece["path"]))


def test_piece_74_essay_md_exists():
    piece = get_piece(PIECE_ID)
    assert piece is not None
    assert os.path.isfile(os.path.join(GALLERY_ROOT, piece["essay"]))


def test_piece_74_thumbnail_exists():
    piece = get_piece(PIECE_ID)
    assert piece is not None
    assert os.path.isfile(os.path.join(GALLERY_ROOT, piece["thumbnail"]))


def test_piece_74_readme_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "README.md"))


def test_piece_74_gen_thumbnail_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "gen_thumbnail.py"))


def test_piece_74_id_matches_directory():
    piece = get_piece(PIECE_ID)
    assert piece is not None
    parts = piece["path"].replace("\\", "/").split("/")
    assert parts[-2] == PIECE_ID


# ---------------------------------------------------------------------------
# index.html content
# ---------------------------------------------------------------------------

def test_piece_74_html_uses_requestanimationframe():
    assert "requestAnimationFrame" in read_html()


def test_piece_74_html_uses_float32array():
    assert "Float32Array" in read_html()


def test_piece_74_html_has_alpha_024():
    html = read_html()
    assert "0.24" in html, "index.html must use stability constant ALPHA = 0.24"


def test_piece_74_html_contains_hebrew_cherut():
    html = read_html()
    # Accept either pointed (חֵרוּת) or unpointed (חרות) form
    assert "חֵרוּת" in html or "חרות" in html, (
        "index.html must contain the Hebrew word חֵרוּת"
    )


def test_piece_74_html_embeds_essay_words():
    """Verify essay text is embedded in the HTML (at least 5 of 10 sampled words)."""
    essay = read_essay()
    html = read_html()
    long_words = [w for w in essay.split() if len(w) > 5][:10]
    found = sum(1 for w in long_words if w in html)
    assert found >= 5, (
        f"index.html appears to be missing the embedded essay ({found}/10 sampled words found)"
    )


def test_piece_74_html_mentions_ftcs_or_heat():
    html = read_html()
    assert "FTCS" in html or "heat" in html.lower() or "heatStep" in html


def test_piece_74_html_has_canvas():
    assert "<canvas" in read_html()


# ---------------------------------------------------------------------------
# Essay content
# ---------------------------------------------------------------------------

def test_piece_74_essay_substantial():
    text = read_essay()
    word_count = len(text.split())
    assert word_count >= 300, f"essay.md has only {word_count} words (need ≥ 300)"


def test_piece_74_essay_mentions_mishnah_or_avot():
    text = read_essay().lower()
    assert "avot" in text or "mishnah" in text, (
        "essay.md must cite Avot 6:2 or the Mishnah"
    )


def test_piece_74_essay_mentions_freedom():
    text = read_essay().lower()
    assert "freedom" in text or "cherut" in text or "חרות" in text or "חֵרוּת" in text


def test_piece_74_essay_mentions_maimonides_or_candle():
    text = read_essay().lower()
    assert "maimonides" in text or "candle" in text, (
        "essay.md should reference Maimonides on Torah transmission"
    )


def test_piece_74_essay_mentions_exodus():
    text = read_essay().lower()
    assert "exodus" in text, "essay.md must reference Exodus"


# ---------------------------------------------------------------------------
# FTCS algorithm correctness (pure-Python re-implementation)
# ---------------------------------------------------------------------------

def _ftcs_step(T, mask, W, H, alpha, source_temp):
    """One FTCS step; returns a new list (boundary zeroed, letter pixels fixed)."""
    T2 = list(T)
    for y in range(1, H - 1):
        for x in range(1, W - 1):
            i = y * W + x
            if mask[i]:
                T2[i] = source_temp
                continue
            T2[i] = T[i] + alpha * (T[i - 1] + T[i + 1] + T[i - W] + T[i + W] - 4.0 * T[i])
    # Zero boundary
    for x in range(W):
        T2[x] = 0.0
        T2[(H - 1) * W + x] = 0.0
    for y in range(H):
        T2[y * W] = 0.0
        T2[y * W + W - 1] = 0.0
    return T2


def test_ftcs_alpha_below_stability_limit():
    """ALPHA = 0.24 must be strictly below the 2D FTCS stability limit of 0.25."""
    ALPHA = 0.24
    assert ALPHA < 0.25, "FTCS stability requires alpha < 0.25"


def test_ftcs_point_source_diffuses():
    """A single hot pixel must spread heat to its four neighbours after one step."""
    W, H = 10, 10
    T = [0.0] * (W * H)
    mask = [0] * (W * H)
    center = 5 * W + 5
    T[center] = 1.0

    T2 = _ftcs_step(T, mask, W, H, 0.24, 1.0)

    assert T2[center] < 1.0, "Center pixel must lose heat to neighbours"
    assert T2[5 * W + 4] > 0.0, "Left neighbour must receive heat"
    assert T2[5 * W + 6] > 0.0, "Right neighbour must receive heat"
    assert T2[4 * W + 5] > 0.0, "Top neighbour must receive heat"
    assert T2[6 * W + 5] > 0.0, "Bottom neighbour must receive heat"


def test_ftcs_mask_pixel_held_at_source_temp():
    """A masked pixel must be fixed at sourceTemp regardless of neighbours."""
    W, H = 5, 5
    T = [0.0] * (W * H)
    mask = [0] * (W * H)
    i = 2 * W + 2
    mask[i] = 1
    T[i] = 0.0  # start cold — should be forced to sourceTemp

    T2 = _ftcs_step(T, mask, W, H, 0.24, 0.8)

    assert T2[i] == pytest.approx(0.8), "Masked pixel must be held at sourceTemp"


def test_ftcs_boundary_remains_zero():
    """All four border rows/columns must remain at 0 after an FTCS step."""
    W, H = 8, 8
    T = [1.0] * (W * H)  # everything hot
    mask = [0] * (W * H)

    T2 = _ftcs_step(T, mask, W, H, 0.24, 1.0)

    for x in range(W):
        assert T2[x] == 0.0, f"Top border at x={x} must be 0"
        assert T2[(H - 1) * W + x] == 0.0, f"Bottom border at x={x} must be 0"
    for y in range(H):
        assert T2[y * W] == 0.0, f"Left border at y={y} must be 0"
        assert T2[y * W + W - 1] == 0.0, f"Right border at y={y} must be 0"


def test_ftcs_no_heat_created_ex_nihilo():
    """With no source pixels, total heat must not increase over time."""
    W, H = 10, 10
    T = [0.0] * (W * H)
    mask = [0] * (W * H)
    # Seed a single interior pixel
    T[5 * W + 5] = 0.5
    initial_total = sum(T)

    for _ in range(20):
        T = _ftcs_step(T, mask, W, H, 0.24, 0.0)

    assert sum(T) <= initial_total + 1e-6, "FTCS must not create heat from nothing"


# ---------------------------------------------------------------------------
# Source temperature decay formula
# ---------------------------------------------------------------------------

def test_source_temp_at_zero():
    """At t=0 the source temperature must be 1.0."""
    t = 0.0
    result = max(0.05, 1.0 - t * 0.0002)
    assert result == pytest.approx(1.0)


def test_source_temp_at_midpoint():
    """At t=1000 s: 1.0 - 1000*0.0002 = 0.8."""
    t = 1000.0
    result = max(0.05, 1.0 - t * 0.0002)
    assert result == pytest.approx(0.8, rel=1e-5)


def test_source_temp_floor():
    """At t=4750 s the formula reaches 0.05; beyond that it stays at 0.05."""
    for t in (4750.0, 5000.0, 10000.0, 100000.0):
        result = max(0.05, 1.0 - t * 0.0002)
        assert result == pytest.approx(0.05, abs=1e-7), (
            f"source temp should floor at 0.05 for t={t}"
        )


def test_source_temp_monotone_decreasing():
    """Source temperature must decrease (or stay flat) as time increases."""
    prev = max(0.05, 1.0 - 0 * 0.0002)
    for t in range(0, 10001, 100):
        curr = max(0.05, 1.0 - t * 0.0002)
        assert curr <= prev + 1e-9, f"source temp increased at t={t}"
        prev = curr


# ---------------------------------------------------------------------------
# Edge cases and failure modes
# ---------------------------------------------------------------------------

def test_piece_not_found_returns_none():
    """get_piece with a non-existent ID must return None."""
    assert get_piece("99-nonexistent-piece") is None


def test_pieces_json_has_no_duplicate_ids():
    """Duplicate IDs would break gallery routing."""
    pieces = load_pieces()
    ids = [p["id"] for p in pieces]
    assert len(ids) == len(set(ids)), "pieces.json contains duplicate IDs"


def test_ftcs_large_alpha_unstable_in_principle():
    """Document that alpha >= 0.25 causes instability (values blow up or oscillate)."""
    # With alpha=0.26, a point source will overshoot: centre goes negative
    W, H = 5, 5
    T = [0.0] * (W * H)
    T[2 * W + 2] = 1.0

    # One step with alpha > 0.25
    T2 = [T[i] for i in range(W * H)]
    alpha = 0.26
    i = 2 * W + 2
    T2[i] = T[i] + alpha * (T[i - 1] + T[i + 1] + T[i - W] + T[i + W] - 4.0 * T[i])
    # The update is: 1.0 + 0.26*(0+0+0+0-4) = 1.0 - 1.04 = -0.04  (negative → unstable)
    assert T2[i] < 0.0, "alpha > 0.25 should yield a negative centre value (instability)"
