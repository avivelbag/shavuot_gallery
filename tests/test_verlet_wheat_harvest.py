"""
Tests for piece 74-verlet-wheat-harvest — The Standing Grain.

Covers pieces.json registration, on-disk file layout, essay content
requirements, and canvas animation correctness for this piece.
"""
import json
import os

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID = "74-verlet-wheat-harvest"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")


def load_piece():
    """Return the pieces.json entry for this piece, or None if absent."""
    with open(PIECES_JSON, encoding="utf-8") as fh:
        data = json.load(fh)
    for entry in data:
        if entry.get("id") == PIECE_ID:
            return entry
    return None


# ---------------------------------------------------------------------------
# Registration checks
# ---------------------------------------------------------------------------

def test_piece_registered_in_pieces_json():
    assert load_piece() is not None, f"{PIECE_ID} not found in pieces.json"


def test_piece_theme_contains_katzir():
    piece = load_piece()
    assert piece is not None
    assert "Katzir" in piece["theme"] or "katzir" in piece["theme"].lower(), (
        "theme must reference Chag HaKatzir"
    )


def test_piece_technique_mentions_verlet():
    piece = load_piece()
    assert piece is not None
    assert "Verlet" in piece["technique"] or "verlet" in piece["technique"].lower(), (
        "technique must mention Verlet"
    )


def test_piece_technique_mentions_wheat():
    piece = load_piece()
    assert piece is not None
    assert "wheat" in piece["technique"].lower(), (
        "technique must mention wheat stalks"
    )


# ---------------------------------------------------------------------------
# File layout checks
# ---------------------------------------------------------------------------

def test_index_html_exists():
    path = os.path.join(PIECE_DIR, "index.html")
    assert os.path.isfile(path), "index.html missing"


def test_essay_md_exists():
    path = os.path.join(PIECE_DIR, "essay.md")
    assert os.path.isfile(path), "essay.md missing"


def test_thumbnail_svg_exists():
    path = os.path.join(PIECE_DIR, "thumbnail.svg")
    assert os.path.isfile(path), "thumbnail.svg missing"


def test_readme_md_exists():
    path = os.path.join(PIECE_DIR, "README.md")
    assert os.path.isfile(path), "README.md missing"


# ---------------------------------------------------------------------------
# Essay content checks
# ---------------------------------------------------------------------------

def test_essay_mentions_three_names():
    """Essay must open with the three biblical names of Shavuot."""
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    assert "HaShavuot" in text or "Chag HaShavuot" in text, "essay must mention Chag HaShavuot"
    assert "HaKatzir" in text, "essay must mention Chag HaKatzir"
    assert "HaBikkurim" in text or "Bikkurim" in text, "essay must mention Chag HaBikkurim"


def test_essay_cites_exodus_23():
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    assert "Exodus 23" in text or "23:16" in text, "essay must cite Exodus 23:16"


def test_essay_mentions_omer():
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    assert "Omer" in text or "omer" in text, "essay must discuss the Omer count"


def test_essay_mentions_ruth():
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    assert "Ruth" in text, "essay must mention the Book of Ruth"


def test_essay_word_count():
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    count = len(text.split())
    assert count >= 300, f"essay has only {count} words; need at least 300"


# ---------------------------------------------------------------------------
# index.html simulation checks
# ---------------------------------------------------------------------------

def _html():
    return open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()


def test_index_uses_requestAnimationFrame():
    assert "requestAnimationFrame" in _html(), "must use requestAnimationFrame"


def test_index_has_canvas():
    html = _html()
    assert "<canvas" in html, "must include a <canvas> element"


def test_index_has_verlet_integration():
    """HTML must contain Verlet integration code (px/py pattern)."""
    html = _html()
    assert "p.px" in html or "px = p.x" in html or ".px" in html, (
        "must contain Verlet integration (px/py previous-position fields)"
    )


def test_index_has_gravity():
    html = _html()
    assert "GRAVITY" in html or "gravity" in html.lower(), "must define gravity constant"


def test_index_has_perlin_noise():
    html = _html()
    assert "noise2" in html or "perlin" in html.lower() or "perm" in html, (
        "must implement Perlin noise"
    )


def test_index_has_distance_constraints():
    html = _html()
    assert "segLen" in html or "rest" in html or "constraint" in html.lower(), (
        "must implement distance constraints"
    )


def test_index_has_angular_constraints():
    html = _html()
    assert "ANGULAR" in html or "angular" in html.lower() or "stiffness" in html.lower(), (
        "must implement angular constraints"
    )


def test_index_has_wind_force():
    html = _html()
    assert "windForce" in html or "wind" in html.lower(), "must implement wind force"


def test_index_embeds_essay_text():
    """index.html must visibly embed the essay (not fetch it at runtime)."""
    essay = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    html = _html()
    words = [w for w in essay.split() if len(w) > 5][:15]
    found = sum(1 for w in words if w in html)
    assert found >= 8, (
        f"index.html does not appear to embed essay text ({found}/15 sampled words found)"
    )


def test_index_has_sky_background_color():
    html = _html()
    assert "#B8D4E8" in html or "B8D4E8" in html.upper(), (
        "sky background color #B8D4E8 must appear in index.html"
    )


def test_index_has_ground_color():
    html = _html()
    assert "#6B4A20" in html or "6B4A20" in html.upper(), (
        "ground color #6B4A20 must appear in index.html"
    )


def test_index_has_wheat_head_drawing():
    html = _html()
    assert "ellipse" in html or "D4A800" in html.upper(), (
        "wheat head drawing (ellipse or gold color #D4A800) must appear in index.html"
    )


# ---------------------------------------------------------------------------
# Thumbnail checks
# ---------------------------------------------------------------------------

def test_thumbnail_is_valid_svg():
    svg = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert "<svg" in svg and "</svg>" in svg, "thumbnail.svg must be valid SVG"


def test_thumbnail_has_wheat_colors():
    svg = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert "D4A800" in svg.upper() or "C8A020" in svg.upper(), (
        "thumbnail must include wheat gold palette colors"
    )


def test_thumbnail_has_sky_color():
    svg = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert "B8D4E8" in svg.upper(), "thumbnail must include sky color #B8D4E8"


# ---------------------------------------------------------------------------
# Edge cases / failure modes
# ---------------------------------------------------------------------------

def test_nonexistent_piece_not_registered():
    """A piece that does not exist must not appear in pieces.json."""
    with open(PIECES_JSON, encoding="utf-8") as fh:
        data = json.load(fh)
    ids = {e["id"] for e in data}
    assert "99-nonexistent-piece" not in ids


def test_piece_id_unique_in_registry():
    """The piece id must appear exactly once."""
    with open(PIECES_JSON, encoding="utf-8") as fh:
        data = json.load(fh)
    matching = [e for e in data if e.get("id") == PIECE_ID]
    assert len(matching) == 1, f"Expected 1 entry for {PIECE_ID}, found {len(matching)}"


def test_essay_does_not_stub_placeholder():
    """Essay must not be a one-liner placeholder."""
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    lines = [ln for ln in text.splitlines() if ln.strip()]
    assert len(lines) >= 10, "essay.md appears to be a stub (fewer than 10 non-empty lines)"
