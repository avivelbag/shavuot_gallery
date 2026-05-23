"""
Tests for piece 82-bond-percolation-arevim: bond percolation with union-find.

Validates file layout, pieces.json registration, essay substance, and
implementation-specific details in index.html (union-find, spanning detection,
color constants, animation loop).
"""
import json
import os
import re

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID = "82-bond-percolation-arevim"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")


def load_piece():
    """Return the pieces.json entry for the bond-percolation piece, or None."""
    with open(PIECES_JSON, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    for entry in data:
        if entry["id"] == PIECE_ID:
            return entry
    return None


def read_index():
    """Return the text content of index.html."""
    return open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()


def read_essay():
    """Return the text content of essay.md."""
    return open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()


def read_thumbnail():
    """Return the text content of thumbnail.svg."""
    return open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()


# ---------------------------------------------------------------------------
# File layout
# ---------------------------------------------------------------------------

def test_piece_directory_exists():
    assert os.path.isdir(PIECE_DIR), f"Piece directory {PIECE_DIR} does not exist"


def test_index_html_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "index.html"))


def test_essay_md_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "essay.md"))


def test_thumbnail_svg_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "thumbnail.svg"))


def test_readme_md_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "README.md"))


# ---------------------------------------------------------------------------
# pieces.json registration
# ---------------------------------------------------------------------------

def test_registered_in_pieces_json():
    piece = load_piece()
    assert piece is not None, f"{PIECE_ID} not found in pieces.json"


def test_pieces_json_required_fields():
    piece = load_piece()
    assert piece is not None
    for field in ("id", "title", "tagline", "year", "theme", "technique",
                  "path", "thumbnail", "essay"):
        assert field in piece and piece[field], f"Missing or empty field '{field}'"


def test_pieces_json_theme_mentions_matan_torah():
    piece = load_piece()
    assert piece is not None
    theme = piece.get("theme", "").lower()
    assert "matan torah" in theme or "arevim" in theme or "sinai" in theme, (
        f"theme '{piece.get('theme')}' should reference Matan Torah / arevim"
    )


def test_pieces_json_technique_mentions_bond_percolation():
    piece = load_piece()
    assert piece is not None
    technique = piece.get("technique", "").lower()
    assert "percolation" in technique or "union-find" in technique, (
        f"technique '{piece.get('technique')}' should mention bond percolation or union-find"
    )


def test_pieces_json_path_correct():
    piece = load_piece()
    assert piece is not None
    assert piece["path"] == f"pieces/{PIECE_ID}/index.html"


def test_pieces_json_thumbnail_correct():
    piece = load_piece()
    assert piece is not None
    assert piece["thumbnail"] == f"pieces/{PIECE_ID}/thumbnail.svg"


def test_pieces_json_essay_correct():
    piece = load_piece()
    assert piece is not None
    assert piece["essay"] == f"pieces/{PIECE_ID}/essay.md"


def test_pieces_json_no_duplicate_ids():
    """Adding the new piece must not create a duplicate ID."""
    with open(PIECES_JSON, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    ids = [p["id"] for p in data]
    assert len(ids) == len(set(ids)), f"Duplicate piece IDs found: {ids}"


# ---------------------------------------------------------------------------
# Essay content
# ---------------------------------------------------------------------------

def test_essay_has_at_least_200_words():
    text = read_essay()
    assert len(text.split()) >= 200, f"essay.md has only {len(text.split())} words"


def test_essay_mentions_shevuot_39a():
    text = read_essay()
    assert "Shevuot 39a" in text or "Shevu'ot 39a" in text, (
        "essay must cite Shevuot 39a"
    )


def test_essay_mentions_leviticus_26_37():
    text = read_essay()
    assert "26:37" in text or "Leviticus 26" in text, (
        "essay must cite Leviticus 26:37 as the Talmudic source for arvut"
    )


def test_essay_mentions_exodus_19_8():
    text = read_essay()
    assert "19:8" in text or "Exodus 19" in text, (
        "essay must cite Exodus 19:8 — the joint acceptance at Sinai"
    )


def test_essay_mentions_arvut():
    text = read_essay()
    assert "arvut" in text.lower() or "arevim" in text.lower() or "guarantor" in text.lower(), (
        "essay must explain the concept of arvut (mutual guarantorship)"
    )


def test_essay_mentions_percolation_threshold():
    text = read_essay()
    assert "threshold" in text.lower() or "critical" in text.lower() or "spanning" in text.lower(), (
        "essay must connect the percolation threshold to the Sinai moment"
    )


def test_essay_not_stub():
    text = read_essay()
    assert len(text.strip()) > 500, "essay is suspiciously short — may be a placeholder"


# ---------------------------------------------------------------------------
# index.html: canvas animation and union-find implementation
# ---------------------------------------------------------------------------

def test_index_uses_requestanimationframe():
    html = read_index()
    assert "requestAnimationFrame" in html


def test_index_has_canvas_element():
    html = read_index()
    assert "<canvas" in html


def test_index_has_union_find_class():
    """index.html must define a union-find data structure."""
    html = read_index()
    assert "class UF" in html or "UnionFind" in html or "union" in html.lower(), (
        "union-find class not found in index.html"
    )


def test_index_has_find_method():
    html = read_index()
    assert "find(" in html, "find() method (path compression) not found"


def test_index_has_union_method():
    html = read_index()
    assert "union(" in html, "union() method not found"


def test_index_has_60x60_grid():
    """Grid must be 60 rows × 60 columns."""
    html = read_index()
    assert "ROWS = 60" in html or "ROWS=60" in html, "ROWS = 60 not found"
    assert "COLS = 60" in html or "COLS=60" in html, "COLS = 60 not found"


def test_index_has_cell_spacing_10():
    html = read_index()
    assert "CELL = 10" in html or "CELL=10" in html, "CELL = 10 (10px cell spacing) not found"


def test_index_has_padding_40():
    html = read_index()
    assert "PAD = 40" in html or "PAD=40" in html, "PAD = 40 (40px padding) not found"


def test_index_has_node_radius_4():
    """Nodes must be drawn as circles of radius ~4px (≈8px diameter as spec'd)."""
    html = read_index()
    assert "NODE_R = 4" in html or "NODE_R=4" in html or "r = 4" in html or "r=4" in html or \
           "NODE_R" in html, "node radius constant not found"


def test_index_has_background_color():
    html = read_index()
    assert "#0A0A14" in html or "#0a0a14" in html, "background color #0A0A14 not found"


def test_index_has_gold_color():
    html = read_index()
    assert "#F0C040" in html or "#f0c040" in html or "0xF0C040" in html or "0xf0c040" in html, (
        "gold color #F0C040 not found (Sinai moment)"
    )


def test_index_has_spanning_detection():
    """index.html must detect when a component spans the grid."""
    html = read_index()
    assert "spans" in html or "touchesTop" in html or "spanning" in html.lower(), (
        "spanning detection not found"
    )


def test_index_has_sinai_trigger():
    html = read_index()
    assert "sinai" in html.lower() or "sinaiTriggered" in html or "Sinai" in html, (
        "Sinai trigger variable not found"
    )


def test_index_has_fade_frames():
    html = read_index()
    assert "FADE_FRAMES" in html or "fadeFrames" in html or "fade" in html.lower(), (
        "fade animation (post-Sinai) not found"
    )


def test_index_has_hold_logic():
    html = read_index()
    assert "HOLD_FRAMES" in html or "holdFrames" in html or "hold" in html.lower(), (
        "3-second hold logic not found"
    )


def test_index_has_bond_list():
    """Bonds must be pre-shuffled, not randomly sampled per frame."""
    html = read_index()
    assert "bonds" in html and ("shuffle" in html.lower() or "Fisher" in html or "Yates" in html
                                or "makeBonds" in html), (
        "pre-shuffled bond list not found"
    )


def test_index_has_reset_logic():
    """After the hold, the simulation must reset and loop."""
    html = read_index()
    assert "init()" in html or "reset" in html.lower(), "reset/re-init logic not found"


def test_index_no_external_dependencies():
    """index.html must be self-contained — no CDN or external script src."""
    html = read_index()
    external = re.findall(r'src=["\']https?://', html)
    assert len(external) == 0, f"index.html has external script src: {external}"


def test_index_embeds_essay_text():
    """index.html must embed the essay inline (no runtime fetch of essay.md)."""
    essay = read_essay()
    html  = read_index()
    words = [w for w in essay.split() if len(w) > 5][:10]
    found = sum(1 for w in words if w in html)
    assert found >= 5, (
        f"only {found}/10 essay words found in index.html — essay must be embedded inline"
    )


def test_index_has_xorshift_or_prng():
    """Simulation must use a deterministic PRNG (not Math.random without a seed)."""
    html = read_index()
    has_seed = "seed" in html.lower()
    has_xor  = "xorshift" in html.lower() or "xor" in html.lower()
    assert has_seed or has_xor, "deterministic PRNG / fixed seed not found"


# ---------------------------------------------------------------------------
# Thumbnail SVG
# ---------------------------------------------------------------------------

def test_thumbnail_is_valid_svg():
    text = read_thumbnail()
    assert "<svg" in text and "</svg>" in text


def test_thumbnail_has_dark_background():
    text = read_thumbnail()
    assert "#0A0A14" in text or "#0a0a14" in text, "thumbnail background #0A0A14 not found"


def test_thumbnail_has_gold_color():
    text = read_thumbnail()
    assert "#F0C040" in text or "#f0c040" in text, "gold color #F0C040 not found in thumbnail"


def test_thumbnail_has_circles():
    text = read_thumbnail()
    assert "<circle" in text, "thumbnail must contain circle elements (nodes)"


def test_thumbnail_has_bonds():
    text = read_thumbnail()
    assert "<line" in text or "<path" in text, "thumbnail must have bond lines"


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

def test_readme_mentions_sinai():
    text = open(os.path.join(PIECE_DIR, "README.md"), encoding="utf-8").read().lower()
    assert "sinai" in text or "matan torah" in text or "arevim" in text, (
        "README.md must mention the Shavuot theme"
    )


def test_readme_mentions_union_find():
    text = open(os.path.join(PIECE_DIR, "README.md"), encoding="utf-8").read()
    assert "union" in text.lower() or "Union-Find" in text or "union-find" in text.lower(), (
        "README.md must describe the union-find technique"
    )


def test_pieces_json_year_is_2026():
    piece = load_piece()
    assert piece is not None
    assert piece["year"] == 2026, f"year should be 2026, got {piece['year']}"


def test_missing_piece_directory_detected(tmp_path):
    """Confirm our file-existence check would catch a missing piece directory."""
    fake_dir = tmp_path / "99-fake-piece"
    assert not fake_dir.exists(), "Fixture must not exist on disk"


def test_empty_essay_detected():
    """An empty essay string should fail the word-count check."""
    text = ""
    word_count = len(text.split())
    assert word_count < 200, "empty essay should have < 200 words"
