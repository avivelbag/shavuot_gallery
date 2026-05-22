"""
Tests for piece 64-clifford-attractor-tikkun-leil.

Validates the piece directory layout, pieces.json registration, HTML content,
and the Clifford attractor implementation details.
"""
import json
import os

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")
PIECE_ID = "64-clifford-attractor-tikkun-leil"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
INDEX_HTML = os.path.join(PIECE_DIR, "index.html")
ESSAY_MD = os.path.join(PIECE_DIR, "essay.md")
THUMBNAIL_SVG = os.path.join(PIECE_DIR, "thumbnail.svg")
README_MD = os.path.join(PIECE_DIR, "README.md")


def load_pieces():
    """Return parsed pieces.json list."""
    with open(PIECES_JSON, "r", encoding="utf-8") as fh:
        return json.load(fh)


def get_piece():
    """Return the pieces.json entry for piece 64, or None."""
    for p in load_pieces():
        if p["id"] == PIECE_ID:
            return p
    return None


# ---------------------------------------------------------------------------
# Directory layout
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
    piece = get_piece()
    assert piece is not None, f"Piece '{PIECE_ID}' not found in pieces.json"


def test_piece_theme_is_tikkun_leil():
    piece = get_piece()
    assert piece is not None
    assert "Tikkun Leil" in piece.get("theme", ""), (
        f"theme should mention 'Tikkun Leil', got: {piece.get('theme')}"
    )


def test_piece_technique_mentions_clifford():
    piece = get_piece()
    assert piece is not None
    technique = piece.get("technique", "").lower()
    assert "clifford" in technique, (
        f"technique should mention 'clifford', got: {piece.get('technique')}"
    )


def test_piece_technique_mentions_density():
    piece = get_piece()
    assert piece is not None
    technique = piece.get("technique", "").lower()
    assert "density" in technique or "histogram" in technique, (
        f"technique should mention density/histogram, got: {piece.get('technique')}"
    )


def test_piece_paths_reference_correct_id():
    piece = get_piece()
    assert piece is not None
    for field in ("path", "thumbnail", "essay"):
        assert PIECE_ID in piece[field], (
            f"Field '{field}' should contain the piece ID, got: {piece[field]}"
        )


def test_piece_no_duplicate_id():
    pieces = load_pieces()
    ids = [p["id"] for p in pieces]
    count = ids.count(PIECE_ID)
    assert count == 1, f"Piece ID '{PIECE_ID}' appears {count} times in pieces.json (expected 1)"


# ---------------------------------------------------------------------------
# index.html content — canvas and algorithm
# ---------------------------------------------------------------------------

def test_index_html_has_700x700_canvas():
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert 'width="700"' in html and 'height="700"' in html, (
        "index.html must specify a 700×700 canvas"
    )


def test_index_html_uses_float32array():
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "Float32Array" in html, (
        "index.html must use a Float32Array for the density histogram"
    )


def test_index_html_has_clifford_parameters():
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "-1.4" in html, "Primary parameter a=−1.4 must appear in index.html"
    assert "1.6" in html, "Primary parameter b=1.6 must appear in index.html"


def test_index_html_has_fallback_parameters():
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "-1.7" in html, "Fallback parameter a=−1.7 must appear in index.html"
    assert "1.8" in html, "Fallback parameter b=1.8 must appear in index.html"


def test_index_html_has_8_million_points():
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "8000000" in html or "8_000_000" in html or "TOTAL_POINTS" in html, (
        "index.html must iterate 8,000,000 points total"
    )


def test_index_html_has_batch_of_40000():
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "40000" in html or "40_000" in html or "BATCH_SIZE" in html, (
        "index.html must use batches of 40,000 points per frame"
    )


def test_index_html_uses_log_tone_map():
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "log1p" in html or "Math.log(" in html, (
        "index.html must use a logarithmic tone-map (Math.log1p or Math.log)"
    )


def test_index_html_uses_requestanimationframe():
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "requestAnimationFrame" in html, (
        "index.html must use requestAnimationFrame for the animation loop"
    )


def test_index_html_has_dawn_label_hebrew():
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "עַד אוֹר הַבֹּקֶר" in html, (
        "index.html must contain the Hebrew label עַד אוֹר הַבֹּקֶר"
    )


# ---------------------------------------------------------------------------
# index.html — colour palette
# ---------------------------------------------------------------------------

def test_index_html_has_background_colour():
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "#030510" in html or "030510" in html, (
        "index.html must use background colour #030510"
    )


def test_index_html_has_gold_colour():
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "D4A820" in html or "#d4a820" in html.lower(), (
        "index.html must include warm gold colour #D4A820 in the palette"
    )


def test_index_html_has_cream_colour():
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "FFF8E0" in html or "#fff8e0" in html.lower(), (
        "index.html must include near-white cream colour #FFF8E0 in the palette"
    )


# ---------------------------------------------------------------------------
# index.html — scripture blocks
# ---------------------------------------------------------------------------

def test_index_html_contains_shir_hashirim_hebrew():
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "אֲנִי יְשֵׁנָה" in html, (
        "index.html must embed Song of Songs 5:2 in Hebrew with nikud"
    )


def test_index_html_contains_shir_hashirim_english():
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "I sleep" in html, (
        "index.html must embed the English translation of Song of Songs 5:2"
    )


# ---------------------------------------------------------------------------
# essay.md content
# ---------------------------------------------------------------------------

def test_essay_md_substantial():
    text = open(ESSAY_MD, encoding="utf-8").read()
    word_count = len(text.split())
    assert word_count >= 300, (
        f"essay.md has only {word_count} words (expected ≥ 300 for ~400-word essay)"
    )


def test_essay_mentions_tikkun_leil():
    text = open(ESSAY_MD, encoding="utf-8").read()
    assert "Tikkun Leil" in text or "tikkun leil" in text.lower(), (
        "essay.md must discuss Tikkun Leil Shavuot"
    )


def test_essay_mentions_zohar():
    text = open(ESSAY_MD, encoding="utf-8").read()
    assert "Zohar" in text or "זוהר" in text, (
        "essay.md must cite the Zohar as the source of the custom"
    )


def test_essay_mentions_magen_avraham():
    text = open(ESSAY_MD, encoding="utf-8").read()
    assert "Magen Avraham" in text or "מגן אברהם" in text, (
        "essay.md must cite the Magen Avraham"
    )


def test_essay_mentions_pri_etz_chaim():
    text = open(ESSAY_MD, encoding="utf-8").read()
    assert "Pri Etz Chaim" in text or "פרי עץ חיים" in text, (
        "essay.md must cite the Pri Etz Chaim for the kabbalistic reason"
    )


def test_essay_contains_hebrew_scripture():
    text = open(ESSAY_MD, encoding="utf-8").read()
    assert "אֲנִי יְשֵׁנָה" in text, (
        "essay.md must quote Song of Songs 5:2 verbatim in Hebrew with nikud"
    )


def test_essay_contains_english_translation():
    text = open(ESSAY_MD, encoding="utf-8").read()
    assert "I sleep" in text, (
        "essay.md must include the English translation of Song of Songs 5:2"
    )


# ---------------------------------------------------------------------------
# thumbnail.svg
# ---------------------------------------------------------------------------

def test_thumbnail_is_valid_svg():
    text = open(THUMBNAIL_SVG, encoding="utf-8").read()
    assert "<svg" in text and "</svg>" in text, (
        "thumbnail.svg does not look like valid SVG"
    )


def test_thumbnail_has_dark_background():
    text = open(THUMBNAIL_SVG, encoding="utf-8").read()
    assert "#030510" in text or "030510" in text, (
        "thumbnail.svg must use the dark navy background #030510"
    )


def test_thumbnail_has_gradient_elements():
    text = open(THUMBNAIL_SVG, encoding="utf-8").read()
    assert "radialGradient" in text or "linearGradient" in text, (
        "thumbnail.svg must contain gradient elements for the density cloud"
    )


def test_thumbnail_has_star_dots():
    text = open(THUMBNAIL_SVG, encoding="utf-8").read()
    circle_count = text.count("<circle")
    assert circle_count >= 20, (
        f"thumbnail.svg must have at least 20 star dots, found {circle_count}"
    )


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

def test_piece_year_is_2026():
    piece = get_piece()
    assert piece is not None
    assert piece.get("year") == 2026, f"Expected year 2026, got {piece.get('year')}"


def test_index_html_has_parameter_validation():
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "validateParams" in html or "validate" in html.lower(), (
        "index.html must include parameter validation logic"
    )


def test_index_html_renders_every_5_frames():
    html = open(INDEX_HTML, encoding="utf-8").read()
    assert "RENDER_EVERY" in html or "% 5" in html, (
        "index.html must re-render every 5 frames during accumulation"
    )


def test_essay_md_word_count_at_least_200():
    """Explicit lower-bound check matching the gallery's ESSAY_MIN_WORDS requirement."""
    text = open(ESSAY_MD, encoding="utf-8").read()
    assert len(text.split()) >= 200, "essay.md must have at least 200 words"


def test_readme_mentions_tikkun_leil():
    text = open(README_MD, encoding="utf-8").read()
    assert "Tikkun Leil" in text or "tikkun leil" in text.lower(), (
        "README.md must mention Tikkun Leil Shavuot"
    )
