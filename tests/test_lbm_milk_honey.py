"""
Tests for piece 83-lattice-boltzmann-milk-honey.

Validates the piece exists in pieces.json with correct fields, that all
required files are present on disk, and that the simulation implementation
and essay content meet the acceptance criteria.
"""
import json
import os


GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID = "83-lattice-boltzmann-milk-honey"


def load_pieces():
    """Load and return parsed pieces.json."""
    with open(os.path.join(GALLERY_ROOT, "pieces.json"), encoding="utf-8") as fh:
        return json.load(fh)


def get_piece():
    """Return the pieces.json entry for this piece, or None."""
    for p in load_pieces():
        if p["id"] == PIECE_ID:
            return p
    return None


def piece_html():
    """Return the full text of this piece's index.html."""
    piece = get_piece()
    assert piece is not None, f"{PIECE_ID} not found in pieces.json"
    path = os.path.join(GALLERY_ROOT, piece["path"])
    return open(path, encoding="utf-8").read()


def piece_essay():
    """Return the full text of this piece's essay.md."""
    piece = get_piece()
    assert piece is not None
    path = os.path.join(GALLERY_ROOT, piece["essay"])
    return open(path, encoding="utf-8").read()


# ---------------------------------------------------------------------------
# Happy path — piece registration
# ---------------------------------------------------------------------------

def test_lbm_piece_exists_in_json():
    """Piece must be registered in pieces.json."""
    assert get_piece() is not None, f"{PIECE_ID} not found in pieces.json"


def test_lbm_piece_has_correct_theme():
    """Theme field must reference Bikkurim / milk and honey."""
    piece = get_piece()
    assert piece is not None
    theme = piece["theme"].lower()
    assert "milk and honey" in theme or "bikkurim" in theme, (
        f"Expected Bikkurim / milk and honey in theme, got: {piece['theme']!r}"
    )


def test_lbm_piece_has_correct_technique():
    """Technique field must reference Lattice Boltzmann Method / D2Q9."""
    piece = get_piece()
    assert piece is not None
    tech = piece["technique"].lower()
    assert "lattice boltzmann" in tech or "d2q9" in tech.upper(), (
        f"Expected Lattice Boltzmann in technique, got: {piece['technique']!r}"
    )


def test_lbm_piece_year_is_2026():
    """Year must be 2026."""
    piece = get_piece()
    assert piece is not None
    assert piece["year"] == 2026


# ---------------------------------------------------------------------------
# File layout — all required files must exist
# ---------------------------------------------------------------------------

def test_lbm_index_html_exists():
    """pieces/<id>/index.html must exist on disk."""
    piece = get_piece()
    assert piece is not None
    path = os.path.join(GALLERY_ROOT, piece["path"])
    assert os.path.isfile(path), f"index.html missing at {path}"


def test_lbm_thumbnail_exists():
    """pieces/<id>/thumbnail.svg must exist on disk."""
    piece = get_piece()
    assert piece is not None
    path = os.path.join(GALLERY_ROOT, piece["thumbnail"])
    assert os.path.isfile(path), f"thumbnail missing at {path}"


def test_lbm_essay_exists():
    """pieces/<id>/essay.md must exist on disk."""
    piece = get_piece()
    assert piece is not None
    path = os.path.join(GALLERY_ROOT, piece["essay"])
    assert os.path.isfile(path), f"essay.md missing at {path}"


def test_lbm_readme_exists():
    """pieces/<id>/README.md must exist on disk."""
    piece = get_piece()
    assert piece is not None
    piece_dir = os.path.join(GALLERY_ROOT, os.path.dirname(piece["path"]))
    readme = os.path.join(piece_dir, "README.md")
    assert os.path.isfile(readme), f"README.md missing at {readme}"


# ---------------------------------------------------------------------------
# index.html content — LBM implementation checks
# ---------------------------------------------------------------------------

def test_lbm_index_html_uses_requestanimationframe():
    """index.html must use requestAnimationFrame for the animation loop."""
    assert "requestAnimationFrame" in piece_html()


def test_lbm_index_html_has_canvas():
    """index.html must contain a <canvas> element."""
    assert "<canvas" in piece_html()


def test_lbm_index_html_has_d2q9_code():
    """index.html must contain D2Q9 LBM implementation markers."""
    html = piece_html()
    assert "TAU" in html or "fNew" in html or "D2Q9" in html, (
        "index.html must contain D2Q9 LBM code (TAU, fNew, or D2Q9)"
    )


def test_lbm_index_html_has_bounce_back():
    """index.html must contain the bounce-back boundary condition."""
    html = piece_html()
    assert "opp" in html or "bounce" in html.lower(), (
        "index.html must contain bounce-back boundary condition"
    )


def test_lbm_index_html_has_hebrew_inscription():
    """index.html must contain the Hebrew inscription אֶרֶץ."""
    assert "אֶרֶץ" in piece_html(), (
        "index.html must contain Hebrew inscription אֶרֶץ"
    )


def test_lbm_index_html_embeds_essay_words():
    """
    index.html must embed the essay text inline (verified by sampling
    long words from essay.md and checking for them in the HTML).
    """
    essay = piece_essay()
    html = piece_html()
    words = [w for w in essay.split() if len(w) > 6][:12]
    found = sum(1 for w in words if w in html)
    assert found >= 6, (
        f"index.html does not appear to embed the essay: only {found}/12 "
        f"sampled words found"
    )


# ---------------------------------------------------------------------------
# Edge cases — essay content and thumbnail quality
# ---------------------------------------------------------------------------

def test_lbm_essay_word_count():
    """essay.md must be at least 300 words."""
    text = piece_essay()
    count = len(text.split())
    assert count >= 300, f"essay.md has only {count} words (minimum 300)"


def test_lbm_essay_cites_deuteronomy_26():
    """essay.md must cite Deuteronomy 26:9 (the Bikkurim declaration)."""
    text = piece_essay()
    assert "26:9" in text or "Deuteronomy 26" in text, (
        "essay.md must cite Deuteronomy 26:9"
    )


def test_lbm_essay_cites_exodus_3():
    """essay.md must cite Exodus 3:8 (the Burning Bush promise)."""
    text = piece_essay()
    assert "3:8" in text or "Exodus 3" in text, (
        "essay.md must cite Exodus 3:8"
    )


def test_lbm_essay_contains_hebrew_quote():
    """essay.md must include at least one Hebrew quotation (contains nikud or Hebrew chars)."""
    text = piece_essay()
    assert "וַיְבִאֵנוּ" in text or "זָבַת" in text or "חָלָב" in text, (
        "essay.md must include a Hebrew quotation from Deuteronomy 26:9"
    )


def test_lbm_thumbnail_is_valid_svg():
    """thumbnail.svg must be a valid SVG file."""
    piece = get_piece()
    assert piece is not None
    path = os.path.join(GALLERY_ROOT, piece["thumbnail"])
    text = open(path, encoding="utf-8").read()
    assert "<svg" in text and "</svg>" in text, "thumbnail.svg is not valid SVG"


def test_lbm_thumbnail_has_cream_and_amber_colors():
    """thumbnail.svg must reference both cream and amber colour values."""
    piece = get_piece()
    path = os.path.join(GALLERY_ROOT, piece["thumbnail"])
    text = open(path, encoding="utf-8").read()
    has_cream = "FFF8E7" in text or "fff8e7" in text
    has_amber = "D4890A" in text or "d4890a" in text or "D4890" in text
    assert has_cream, "thumbnail.svg must include cream colour #FFF8E7"
    assert has_amber, "thumbnail.svg must include amber colour #D4890A"


# ---------------------------------------------------------------------------
# Explicit failure modes
# ---------------------------------------------------------------------------

def test_lbm_wrong_id_not_in_json():
    """A non-existent piece ID must not be found in pieces.json."""
    pieces = load_pieces()
    ids = [p["id"] for p in pieces]
    assert "83-nonexistent-piece" not in ids


def test_lbm_piece_path_ends_with_html():
    """The piece path must point to an HTML file."""
    piece = get_piece()
    assert piece is not None
    assert piece["path"].endswith(".html"), (
        f"path must end with .html, got: {piece['path']!r}"
    )


def test_lbm_thumbnail_extension_is_svg():
    """The thumbnail must be an SVG file."""
    piece = get_piece()
    assert piece is not None
    assert piece["thumbnail"].endswith(".svg"), (
        f"thumbnail must be .svg, got: {piece['thumbnail']!r}"
    )
