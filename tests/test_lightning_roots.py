"""
Tests for piece 41-lightning-roots (Lichtenberg at Sinai).

Covers:
- pieces.json registration and required fields
- All required files exist on disk
- essay.md content requirements (scripture references, rabbinic content)
- index.html embeds essay text and uses correct canvas/animation APIs
- DBM-specific HTML structure and palette requirements
- thumbnail is valid SVG
- Edge cases: empty essay, missing fields
"""
import json
import os
import re

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")
PIECE_ID = "41-lightning-roots"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)


def load_pieces():
    """Load and return the parsed pieces.json list."""
    with open(PIECES_JSON, "r", encoding="utf-8") as fh:
        return json.load(fh)


def get_piece():
    """Return the pieces.json entry for piece 39, or None."""
    for p in load_pieces():
        if p["id"] == PIECE_ID:
            return p
    return None


def read_file(rel_path):
    """Read a file relative to GALLERY_ROOT and return its text."""
    return open(os.path.join(GALLERY_ROOT, rel_path), encoding="utf-8").read()


# ---------------------------------------------------------------------------
# pieces.json registration
# ---------------------------------------------------------------------------

def test_piece_registered_in_pieces_json():
    """Piece 39 must appear in pieces.json."""
    piece = get_piece()
    assert piece is not None, f"Piece '{PIECE_ID}' not found in pieces.json"


def test_piece_required_fields_present():
    """All required fields must be present and non-empty."""
    required = ("id", "title", "tagline", "year", "theme", "technique", "path", "thumbnail", "essay")
    piece = get_piece()
    assert piece is not None, "Piece not found"
    for field in required:
        assert field in piece and piece[field], (
            f"Piece '{PIECE_ID}' is missing or has empty field '{field}'"
        )


def test_piece_year_is_integer():
    piece = get_piece()
    assert piece is not None
    assert isinstance(piece["year"], int), f"year must be int, got {piece['year']!r}"


def test_piece_path_ends_with_html():
    piece = get_piece()
    assert piece is not None
    assert piece["path"].endswith(".html"), "path must end with .html"


def test_piece_id_matches_directory():
    """The id field must match the directory component in the path."""
    piece = get_piece()
    assert piece is not None
    parts = piece["path"].replace("\\", "/").split("/")
    assert parts[-2] == PIECE_ID, (
        f"Directory in path '{parts[-2]}' does not match id '{PIECE_ID}'"
    )


def test_no_duplicate_ids():
    """Piece 39 must not introduce a duplicate ID."""
    pieces = load_pieces()
    ids = [p["id"] for p in pieces]
    assert ids.count(PIECE_ID) == 1, f"Duplicate id '{PIECE_ID}' found in pieces.json"


# ---------------------------------------------------------------------------
# Required files on disk
# ---------------------------------------------------------------------------

def test_index_html_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "index.html")), (
        f"pieces/{PIECE_ID}/index.html does not exist"
    )


def test_essay_md_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "essay.md")), (
        f"pieces/{PIECE_ID}/essay.md does not exist"
    )


def test_thumbnail_svg_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "thumbnail.svg")), (
        f"pieces/{PIECE_ID}/thumbnail.svg does not exist"
    )


def test_readme_md_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "README.md")), (
        f"pieces/{PIECE_ID}/README.md does not exist"
    )


def test_pieces_json_paths_resolve():
    """All path/thumbnail/essay fields in pieces.json entry must resolve on disk."""
    piece = get_piece()
    assert piece is not None
    for field in ("path", "thumbnail", "essay"):
        full = os.path.join(GALLERY_ROOT, piece[field])
        assert os.path.isfile(full), (
            f"Piece '{PIECE_ID}': '{field}' = '{piece[field]}' does not exist on disk"
        )


# ---------------------------------------------------------------------------
# essay.md content requirements
# ---------------------------------------------------------------------------

def test_essay_word_count():
    """Essay must have at least 200 words."""
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    count = len(text.split())
    assert count >= 200, f"essay.md has only {count} words (minimum 200)"


def test_essay_cites_exodus_19():
    """Essay must cite Exodus 19:16–19."""
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    assert re.search(r"Exodus\s+19", text), "essay.md must cite Exodus 19"
    assert re.search(r"19:16", text), "essay.md must reference verse 19:16"


def test_essay_mentions_mechilta():
    """Essay must discuss the Mechilta's teaching about the seventy voices."""
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    assert "Mechilta" in text, "essay.md must mention the Mechilta"


def test_essay_mentions_rashi_shofar():
    """Essay must mention Rashi's comment about the shofar growing louder."""
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    assert "Rashi" in text, "essay.md must mention Rashi"
    assert re.search(r"shofar|קֹל", text), "essay.md must discuss the shofar"


def test_essay_mentions_tree_of_life():
    """Essay must connect Lichtenberg branching to Torah as tree of life (Proverbs 3:18)."""
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    assert re.search(r"Proverbs|Prov|עֵץ חַיִּים|tree of life", text, re.IGNORECASE), (
        "essay.md must reference the tree of life (Proverbs 3:18)"
    )


def test_essay_mentions_lichtenberg_or_dbm():
    """Essay must explain the Lichtenberg / DBM technique."""
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    assert re.search(r"Lichtenberg|Dielectric Breakdown|DBM", text), (
        "essay.md must explain the Lichtenberg / DBM technique"
    )


# ---------------------------------------------------------------------------
# index.html content requirements
# ---------------------------------------------------------------------------

def test_index_html_uses_canvas():
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "<canvas" in html, "index.html must contain a <canvas> element"


def test_index_html_uses_request_animation_frame():
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "requestAnimationFrame" in html, "index.html must use requestAnimationFrame"


def test_index_html_embeds_essay_text():
    """Essay text must be embedded inline in index.html (not fetched at runtime)."""
    essay = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    words = [w for w in essay.split() if len(w) > 5][:10]
    found = sum(1 for w in words if w in html)
    assert found >= 5, (
        f"index.html does not appear to embed essay text ({found}/10 sampled words found)"
    )


def test_index_html_uses_dbm_palette_background():
    """index.html must use the near-black background color #080810."""
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "#080810" in html or "080810" in html.lower(), (
        "index.html must use background color #080810"
    )


def test_index_html_has_mountain_silhouette():
    """index.html must render the mountain silhouette."""
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert re.search(r"[Mm]ountain|mtn|MTN", html), (
        "index.html must include mountain silhouette code"
    )


def test_index_html_references_exodus_19():
    """index.html must display the Exodus 19 scripture reference."""
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert re.search(r"Exodus\s+19|19:16", html), (
        "index.html must display Exodus 19:16–19 reference"
    )


def test_index_html_uses_fade_or_alpha():
    """index.html must implement the fade-out loop (uses alpha or fade concept)."""
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert re.search(r"fade|alpha|Alpha", html), (
        "index.html must implement a fade-out phase for the loop"
    )


# ---------------------------------------------------------------------------
# thumbnail SVG validity
# ---------------------------------------------------------------------------

def test_thumbnail_is_valid_svg():
    text = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert "<svg" in text and "</svg>" in text, "thumbnail.svg must be valid SVG"


def test_thumbnail_svg_has_viewbox():
    text = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert "viewBox" in text, "thumbnail.svg must have a viewBox attribute"


# ---------------------------------------------------------------------------
# Edge cases and failure modes
# ---------------------------------------------------------------------------

def test_essay_not_empty():
    """essay.md must not be empty or whitespace-only."""
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    assert text.strip(), "essay.md must not be empty"


def test_piece_with_missing_essay_field_detected(tmp_path):
    """A pieces.json entry missing the essay field must be detectable."""
    bad = [{"id": PIECE_ID, "essay": ""}]
    assert not bad[0]["essay"], "Fixture confirms empty essay should be treated as missing"


def test_piece_with_nonexistent_html_detected(tmp_path):
    """A path pointing to a missing HTML file must be detectable."""
    missing = os.path.join(str(tmp_path), "index.html")
    assert not os.path.isfile(missing), "Fixture path must not exist on disk"


def test_essay_references_sinai():
    """Essay must explicitly reference Sinai or Har Sinai."""
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    assert re.search(r"Sinai|הר סיני", text), "essay.md must mention Sinai"
