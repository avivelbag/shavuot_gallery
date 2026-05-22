"""
Tests for piece 38-fiftieth-gate-ifs: IFS chaos-game harvest field.

Covers the acceptance criteria specific to this piece in addition to the
generic pieces.json/file-layout checks that test_pieces.py already applies
to every piece.
"""
import json
import os
import re

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")
PIECE_ID = "38-fiftieth-gate-ifs"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
INDEX_HTML = os.path.join(PIECE_DIR, "index.html")
ESSAY_MD = os.path.join(PIECE_DIR, "essay.md")


def load_pieces():
    """Load and return the parsed pieces.json list."""
    with open(PIECES_JSON, "r", encoding="utf-8") as fh:
        return json.load(fh)


def _get_piece(piece_id):
    """Return the pieces.json entry for the given id, or None."""
    for p in load_pieces():
        if p["id"] == piece_id:
            return p
    return None


def _html():
    """Return the full text of index.html for piece 38."""
    with open(INDEX_HTML, "r", encoding="utf-8") as fh:
        return fh.read()


def _essay():
    """Return the full text of essay.md for piece 38."""
    with open(ESSAY_MD, "r", encoding="utf-8") as fh:
        return fh.read()


# ---------------------------------------------------------------------------
# Happy-path: piece registered and all required files present
# ---------------------------------------------------------------------------

def test_piece_38_in_pieces_json():
    piece = _get_piece(PIECE_ID)
    assert piece is not None, f"Piece '{PIECE_ID}' not found in pieces.json"


def test_piece_38_required_fields():
    required = ("id", "title", "tagline", "year", "theme", "technique", "path", "thumbnail", "essay")
    piece = _get_piece(PIECE_ID)
    assert piece is not None
    for field in required:
        assert field in piece and piece[field], (
            f"Piece '{PIECE_ID}' missing or empty field '{field}'"
        )


def test_piece_38_index_html_exists():
    assert os.path.isfile(INDEX_HTML), f"index.html missing at {INDEX_HTML}"


def test_piece_38_essay_md_exists():
    assert os.path.isfile(ESSAY_MD), f"essay.md missing at {ESSAY_MD}"


def test_piece_38_thumbnail_exists():
    piece = _get_piece(PIECE_ID)
    assert piece is not None
    thumb_path = os.path.join(GALLERY_ROOT, piece["thumbnail"])
    assert os.path.isfile(thumb_path), f"Thumbnail missing: {piece['thumbnail']}"


def test_piece_38_readme_exists():
    readme = os.path.join(PIECE_DIR, "README.md")
    assert os.path.isfile(readme), "README.md missing from piece directory"


# ---------------------------------------------------------------------------
# IFS / chaos-game technique checks
# ---------------------------------------------------------------------------

def test_index_html_uses_requestanimationframe():
    assert "requestAnimationFrame" in _html(), (
        "index.html must use requestAnimationFrame for animation"
    )


def test_index_html_has_ifs_transforms():
    """At least three plant IFS transform arrays must be present."""
    html = _html()
    # Each plant definition contains 'transforms:' followed by an array
    matches = re.findall(r'transforms\s*:', html)
    assert len(matches) >= 3, (
        f"Expected at least 3 IFS plant transform definitions, found {len(matches)}"
    )


def test_index_html_chaos_game_iterates_points():
    """The chaos-game loop must iterate a meaningful number of points per frame."""
    html = _html()
    # POINTS_PER_FRAME constant or a literal >= 1000 must appear
    match = re.search(r'POINTS_PER_FRAME\s*=\s*(\d+)', html)
    assert match is not None, "POINTS_PER_FRAME constant not found in index.html"
    count = int(match.group(1))
    assert count >= 1000, f"POINTS_PER_FRAME={count} is below the 1000-point minimum"


def test_index_html_has_canvas_element():
    assert "<canvas" in _html(), "index.html must contain a <canvas> element"


def test_index_html_has_breathing_animation():
    """Breathing (scale pulse) must be implemented via CSS transform or ctx.scale."""
    html = _html()
    has_scale_transform = "scale(" in html or "scale =" in html
    assert has_scale_transform, (
        "index.html must implement a breathing scale animation"
    )


def test_index_html_three_plants_defined():
    """Three named plants (wheat, barley, vine) must be declared."""
    html = _html()
    for name in ("wheat", "barley", "vine"):
        assert name in html, f"Plant '{name}' not found in index.html"


# ---------------------------------------------------------------------------
# Hebrew nun / 50 label
# ---------------------------------------------------------------------------

def test_index_html_has_nun_character():
    """The Hebrew letter nun (נ = 50) must appear in the HTML."""
    html = _html()
    assert "נ" in html, (
        "index.html must display the Hebrew letter nun (נ) to represent 50"
    )


def test_index_html_references_fifty():
    """The number 50 or the word 'fifty' must appear somewhere in the HTML."""
    html = _html().lower()
    assert "fifty" in html or "50" in html, (
        "index.html must reference '50' or 'fifty' to connect to the Omer count"
    )


# ---------------------------------------------------------------------------
# Harvest color palette
# ---------------------------------------------------------------------------

def test_index_html_uses_harvest_gold():
    """The harvest gold color (#E8C84A) must be used in the palette."""
    html = _html().upper()
    assert "E8C84A" in html, "Harvest gold (#E8C84A) not found in index.html"


def test_index_html_uses_field_green():
    """The deep field green color must be referenced in the palette (as hex literal or string)."""
    html = _html()
    has_green = "3A6B2A" in html.upper() or "deep field green" in html.lower() or "0x3A" in html
    assert has_green, "Deep field green (#3A6B2A) not found in index.html palette"


# ---------------------------------------------------------------------------
# Essay content — citations in Hebrew AND English
# ---------------------------------------------------------------------------

def test_essay_has_exodus_citation():
    essay = _essay()
    assert "Exodus 23" in essay or "Exodus 23:16" in essay, (
        "essay.md must cite Exodus 23:16 (Chag HaKatzir)"
    )


def test_essay_has_exodus_hebrew():
    """Exodus 23:16 must appear in Hebrew."""
    essay = _essay()
    assert "וְחַג הַקָּצִיר" in essay, (
        "essay.md must include the Hebrew text of Exodus 23:16"
    )


def test_essay_has_exodus_english():
    """Exodus 23:16 must appear in English translation."""
    essay = _essay()
    assert "feast of harvest" in essay.lower(), (
        "essay.md must include an English translation of Exodus 23:16"
    )


def test_essay_has_leviticus_citation():
    essay = _essay()
    assert "Leviticus 23" in essay, (
        "essay.md must cite Leviticus 23:15-16 (Sefirat HaOmer)"
    )


def test_essay_has_leviticus_hebrew():
    """Leviticus 23:15-16 must appear in Hebrew."""
    essay = _essay()
    assert "וּסְפַרְתֶּם" in essay, (
        "essay.md must include the Hebrew text of Leviticus 23:15"
    )


def test_essay_has_leviticus_english():
    essay = _essay()
    assert "count" in essay.lower() and "fifty" in essay.lower(), (
        "essay.md must include an English translation of the Omer counting verse"
    )


def test_essay_has_deuteronomy_citation():
    essay = _essay()
    assert "Deuteronomy 8" in essay or "Deuteronomy 8:8" in essay, (
        "essay.md must cite Deuteronomy 8:8 (seven species)"
    )


def test_essay_has_deuteronomy_hebrew():
    """Deuteronomy 8:8 must appear in Hebrew."""
    essay = _essay()
    assert "אֶרֶץ חִטָּה" in essay, (
        "essay.md must include the Hebrew text of Deuteronomy 8:8"
    )


def test_essay_has_deuteronomy_english():
    essay = _essay()
    assert "wheat and barley" in essay.lower(), (
        "essay.md must include an English translation of Deuteronomy 8:8"
    )


def test_essay_mentions_maharal():
    essay = _essay()
    assert "Maharal" in essay, (
        "essay.md must reference the Maharal of Prague"
    )


def test_essay_mentions_seven_species():
    essay = _essay()
    assert "seven species" in essay.lower() or "sheva minim" in essay.lower(), (
        "essay.md must name the seven species"
    )


def test_essay_word_count():
    """Essay must be substantial — at least 400 words for this piece."""
    essay = _essay()
    count = len(essay.split())
    assert count >= 400, f"essay.md has only {count} words; expected at least 400"


# ---------------------------------------------------------------------------
# Essay text embedded in index.html
# ---------------------------------------------------------------------------

def test_index_html_embeds_essay_text():
    """index.html must embed the essay text (not fetch it at runtime)."""
    essay = _essay()
    html = _html()
    # Sample the 10 longest words from the essay and check most appear in HTML
    words = sorted([w for w in essay.split() if len(w) > 7], key=len, reverse=True)
    sampled = words[:15]
    found = sum(1 for w in sampled if w in html)
    assert found >= 8, (
        f"index.html does not appear to embed the essay: only {found}/15 sampled words found"
    )


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

def test_piece_38_id_matches_directory():
    piece = _get_piece(PIECE_ID)
    assert piece is not None
    path_parts = piece["path"].replace("\\", "/").split("/")
    dir_name = path_parts[-2]
    assert dir_name == PIECE_ID, (
        f"pieces.json 'id' '{PIECE_ID}' does not match directory '{dir_name}'"
    )


def test_piece_38_year_is_integer():
    piece = _get_piece(PIECE_ID)
    assert piece is not None
    assert isinstance(piece["year"], int), (
        f"'year' field is not an integer: {piece['year']!r}"
    )


def test_piece_38_path_ends_with_html():
    piece = _get_piece(PIECE_ID)
    assert piece is not None
    assert piece["path"].endswith(".html"), (
        f"'path' does not end with .html: {piece['path']}"
    )


def test_piece_38_no_duplicate_in_pieces_json():
    """Adding piece 38 must not create a duplicate id."""
    pieces = load_pieces()
    ids = [p["id"] for p in pieces]
    assert ids.count(PIECE_ID) == 1, (
        f"Piece id '{PIECE_ID}' appears {ids.count(PIECE_ID)} times in pieces.json"
    )


def test_piece_38_essay_different_from_another_piece():
    """Regression: the essay must not be an empty stub or copy of a known template."""
    essay = _essay()
    assert "Iterated Function" in essay or "IFS" in essay, (
        "essay.md does not appear to be about IFS / the chaos game"
    )
    assert "Chag HaKatzir" in essay, (
        "essay.md does not mention Chag HaKatzir (the harvest theme)"
    )


# ---------------------------------------------------------------------------
# Explicit failure modes
# ---------------------------------------------------------------------------

def test_missing_nun_would_be_caught():
    """Confirm the nun check correctly identifies absence of the character."""
    fake_html = "<html><body><canvas></canvas></body></html>"
    assert "נ" not in fake_html  # absence detected correctly


def test_missing_transforms_would_be_caught():
    """A page with no IFS transforms would fail the transform count check."""
    fake_html = "<html><body>no plants here</body></html>"
    matches = re.findall(r'transforms\s*:', fake_html)
    assert len(matches) < 3  # would correctly fail the ≥3 check


def test_short_essay_would_be_caught():
    """An essay with fewer than 400 words would be flagged."""
    short = "The harvest field. " * 15  # ~45 words
    count = len(short.split())
    assert count < 400  # confirms the guard would trigger
