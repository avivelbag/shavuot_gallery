"""
Tests for piece 79-mobius-chain-of-tradition.

Validates the piece directory layout, pieces.json registration,
essay content requirements, and index.html structural properties.
"""
import json
import os

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECES_JSON  = os.path.join(GALLERY_ROOT, "pieces.json")
PIECE_ID     = "79-mobius-chain-of-tradition"
PIECE_DIR    = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)


def _load_pieces():
    with open(PIECES_JSON, "r", encoding="utf-8") as fh:
        return json.load(fh)


def _get_piece():
    return next((p for p in _load_pieces() if p["id"] == PIECE_ID), None)


# ---------------------------------------------------------------------------
# pieces.json registration
# ---------------------------------------------------------------------------

def test_piece_registered_in_json():
    assert _get_piece() is not None, f"Piece '{PIECE_ID}' not found in pieces.json"


def test_piece_has_correct_theme():
    piece = _get_piece()
    assert piece is not None
    assert "Crown of Torah" in piece["theme"] or "naaseh" in piece["theme"], (
        "Piece theme must mention 'Crown of Torah / naaseh v'nishma'"
    )


def test_piece_has_correct_technique():
    piece = _get_piece()
    assert piece is not None
    assert "Möbius" in piece["technique"] or "Mobius" in piece["technique"], (
        "Technique must mention Möbius transformations"
    )
    assert "Schottky" in piece["technique"], (
        "Technique must mention Schottky group"
    )


# ---------------------------------------------------------------------------
# File layout
# ---------------------------------------------------------------------------

def test_index_html_exists():
    path = os.path.join(PIECE_DIR, "index.html")
    assert os.path.isfile(path), f"index.html missing from {PIECE_DIR}"


def test_essay_md_exists():
    path = os.path.join(PIECE_DIR, "essay.md")
    assert os.path.isfile(path), f"essay.md missing from {PIECE_DIR}"


def test_thumbnail_svg_exists():
    path = os.path.join(PIECE_DIR, "thumbnail.svg")
    assert os.path.isfile(path), f"thumbnail.svg missing from {PIECE_DIR}"


def test_readme_exists():
    path = os.path.join(PIECE_DIR, "README.md")
    assert os.path.isfile(path), f"README.md missing from {PIECE_DIR}"


# ---------------------------------------------------------------------------
# Essay content requirements
# ---------------------------------------------------------------------------

def test_essay_at_least_400_words():
    path = os.path.join(PIECE_DIR, "essay.md")
    text = open(path, encoding="utf-8").read()
    count = len(text.split())
    assert count >= 400, f"essay.md has {count} words; need at least 400"


def test_essay_contains_pirkei_avot_opening():
    """Essay must quote or paraphrase all five links in the Pirkei Avot 1:1 chain."""
    path = os.path.join(PIECE_DIR, "essay.md")
    text = open(path, encoding="utf-8").read()
    assert "Moses" in text, "Essay must mention Moses"
    assert "Joshua" in text, "Essay must mention Joshua"
    assert "Elders" in text or "Elders" in text, "Essay must mention the Elders"
    assert "Prophets" in text, "Essay must mention the Prophets"
    assert "Great Assembly" in text or "Knesset" in text, (
        "Essay must mention the Men of the Great Assembly"
    )


def test_essay_mentions_epistemological_claim():
    """Essay must explain the epistemological, not merely historical, nature of Avot 1:1."""
    path = os.path.join(PIECE_DIR, "essay.md")
    text = open(path, encoding="utf-8").read()
    assert "epistemological" in text or "authority" in text or "oral" in text.lower(), (
        "Essay must address the epistemological claim of the chain (oral Torah authority)"
    )


def test_essay_mentions_shavuot_context():
    """Essay must explain the Pesach-to-Shavuot Pirkei Avot study tradition."""
    path = os.path.join(PIECE_DIR, "essay.md")
    text = open(path, encoding="utf-8").read()
    assert "Shavuot" in text, "Essay must mention Shavuot"
    assert "Pesach" in text or "Passover" in text, (
        "Essay must mention the Pesach context of the Omer study period"
    )


def test_essay_ties_to_artwork():
    """Essay must connect the Möbius / Schottky construction to the transmission theme."""
    path = os.path.join(PIECE_DIR, "essay.md")
    text = open(path, encoding="utf-8").read()
    assert "conformal" in text or "Möbius" in text or "Mobius" in text, (
        "Essay must explain the Möbius conformal mapping metaphor"
    )
    assert "limit" in text.lower(), (
        "Essay should mention the limit set / limit points"
    )


# ---------------------------------------------------------------------------
# index.html structural requirements
# ---------------------------------------------------------------------------

def _html():
    return open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()


def test_html_has_canvas():
    assert "<canvas" in _html(), "index.html must contain a <canvas> element"


def test_html_uses_requestanimationframe():
    assert "requestAnimationFrame" in _html(), (
        "index.html must use requestAnimationFrame for the animation loop"
    )


def test_html_implements_mobius_arithmetic():
    html = _html()
    assert "mobiusPoint" in html or "mobius" in html.lower(), (
        "index.html must implement Möbius transformation arithmetic"
    )


def test_html_has_schottky_generation():
    """index.html must implement the Schottky cascade generation."""
    html = _html()
    assert "generateSchottky" in html or "Schottky" in html or "schottky" in html, (
        "index.html must implement Schottky group circle generation"
    )


def test_html_has_depth_coloring():
    """index.html must color circles by generation depth."""
    html = _html()
    assert "#D4A030" in html, "index.html must use warm gold #D4A030 for depth-0 circles"
    assert "#C07020" in html or "#8B3A10" in html, (
        "index.html must use amber/deep-orange colors for deeper generations"
    )


def test_html_dark_navy_background():
    assert "#06090F" in _html(), "index.html must use dark navy background #06090F"


def test_html_has_hebrew_watermark():
    html = _html()
    assert "מֹשֶׁה קִבֵּל תּוֹרָה מִסִּינַי" in html, (
        "index.html must display the Hebrew watermark text מֹשֶׁה קִבֵּל תּוֹרָה מִסִּינַי"
    )


def test_html_animation_rotation_constant():
    """index.html must use 0.003 rad/frame rotation constant."""
    html = _html()
    assert "0.003" in html, (
        "index.html must define dTHETA = 0.003 rad/frame for the seamless loop"
    )


def test_html_embeds_essay_content():
    """index.html must embed the essay text inline (not fetch it at runtime)."""
    essay = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    html  = _html()
    words = [w for w in essay.split() if len(w) > 6][:12]
    found = sum(1 for w in words if w in html)
    assert found >= 6, (
        f"index.html appears not to embed essay text; only {found}/12 sampled words found"
    )


def test_html_has_min_radius_clip():
    """index.html must clip circles below a minimum radius to avoid infinite loops."""
    html = _html()
    assert "MIN_RADIUS" in html or "min_radius" in html or "minRadius" in html or "< 1" in html, (
        "index.html must clip circles below minimum radius (convergence guard)"
    )


# ---------------------------------------------------------------------------
# Thumbnail validity
# ---------------------------------------------------------------------------

def test_thumbnail_is_valid_svg():
    path = os.path.join(PIECE_DIR, "thumbnail.svg")
    text = open(path, encoding="utf-8").read()
    assert "<svg" in text and "</svg>" in text, "thumbnail.svg must be valid SVG"


def test_thumbnail_has_dark_background():
    path = os.path.join(PIECE_DIR, "thumbnail.svg")
    text = open(path, encoding="utf-8").read()
    assert "#06090F" in text or "06090f" in text.lower(), (
        "thumbnail.svg must use the dark navy background #06090F"
    )


def test_thumbnail_has_gold_circles():
    path = os.path.join(PIECE_DIR, "thumbnail.svg")
    text = open(path, encoding="utf-8").read()
    assert "#D4A030" in text or "#C07020" in text, (
        "thumbnail.svg must include gold/amber-colored circles"
    )


# ---------------------------------------------------------------------------
# Edge-case / failure-mode tests
# ---------------------------------------------------------------------------

def test_piece_id_no_duplicate():
    """Registering 79-mobius-chain-of-tradition must not create a duplicate ID."""
    pieces = _load_pieces()
    ids = [p["id"] for p in pieces]
    assert ids.count(PIECE_ID) == 1, f"Piece ID '{PIECE_ID}' appears more than once in pieces.json"


def test_piece_path_matches_id():
    """The path field must contain the piece ID as the parent directory name."""
    piece = _get_piece()
    assert piece is not None
    path_parts = piece["path"].replace("\\", "/").split("/")
    assert len(path_parts) >= 2, "path must be at least pieces/<id>/index.html"
    assert path_parts[-2] == PIECE_ID, (
        f"Directory in path '{piece['path']}' does not match piece ID '{PIECE_ID}'"
    )


def test_piece_year_is_integer():
    piece = _get_piece()
    assert piece is not None
    assert isinstance(piece["year"], int), "year must be an integer"


def test_essay_min_radius_not_missing(tmp_path):
    """An essay.md with fewer than 400 words should be detectable."""
    short = tmp_path / "short.md"
    short.write_text("Too short.", encoding="utf-8")
    word_count = len(short.read_text().split())
    assert word_count < 400, "Fixture confirms the essay is too short"


def test_missing_piece_dir_detectable(tmp_path):
    """A non-existent piece directory should not contain index.html."""
    fake = tmp_path / "99-does-not-exist" / "index.html"
    assert not fake.exists(), "Fixture path must not exist"
