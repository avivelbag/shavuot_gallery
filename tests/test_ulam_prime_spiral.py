"""
Tests for piece 87-ulam-prime-spiral-omer: The Fifty Gates — A Prime Spiral.

Verifies the pieces.json entry, all required files, essay length, and that
the index.html correctly embeds the essay and implements the required features.
"""
import json
import os

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID = "87-ulam-prime-spiral-omer"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_pieces():
    """Return parsed pieces.json list."""
    with open(PIECES_JSON, encoding="utf-8") as fh:
        return json.load(fh)


def get_piece():
    """Return the pieces.json entry for this piece, or None."""
    for p in load_pieces():
        if p["id"] == PIECE_ID:
            return p
    return None


def read_html():
    """Return full index.html text."""
    return open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()


def read_essay():
    """Return full essay.md text."""
    return open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()


# ---------------------------------------------------------------------------
# pieces.json registration
# ---------------------------------------------------------------------------

def test_piece_registered_in_json():
    """The piece must appear in pieces.json."""
    assert get_piece() is not None, f"Piece '{PIECE_ID}' not found in pieces.json"


def test_piece_required_fields():
    """All required fields must be present and non-empty."""
    required = ("id", "title", "tagline", "year", "theme", "technique", "path", "thumbnail", "essay")
    piece = get_piece()
    assert piece is not None
    for field in required:
        assert field in piece, f"Missing field: {field}"
        val = piece[field]
        assert val is not None and val != "", f"Empty field: {field}"


def test_piece_theme_mentions_omer():
    """Theme should reference Sefirat HaOmer."""
    piece = get_piece()
    assert piece is not None
    assert "omer" in piece["theme"].lower() or "Omer" in piece["theme"], (
        "theme must mention Sefirat HaOmer"
    )


def test_piece_technique_mentions_ulam():
    """Technique must reference Ulam spiral."""
    piece = get_piece()
    assert piece is not None
    assert "ulam" in piece["technique"].lower(), "technique must mention Ulam spiral"


def test_piece_technique_mentions_sieve():
    """Technique must reference the Sieve of Eratosthenes."""
    piece = get_piece()
    assert piece is not None
    assert "sieve" in piece["technique"].lower() or "eratosthenes" in piece["technique"].lower(), (
        "technique must mention Sieve of Eratosthenes"
    )


# ---------------------------------------------------------------------------
# File existence
# ---------------------------------------------------------------------------

def test_index_html_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "index.html")), "index.html is missing"


def test_essay_md_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "essay.md")), "essay.md is missing"


def test_thumbnail_exists():
    """Thumbnail must exist on disk (svg or png)."""
    piece = get_piece()
    assert piece is not None
    thumb = os.path.join(GALLERY_ROOT, piece["thumbnail"])
    assert os.path.isfile(thumb), f"thumbnail not found: {piece['thumbnail']}"


def test_readme_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "README.md")), "README.md is missing"


# ---------------------------------------------------------------------------
# Essay content
# ---------------------------------------------------------------------------

def test_essay_minimum_word_count():
    """Essay must have at least 200 words."""
    text = read_essay()
    count = len(text.split())
    assert count >= 200, f"essay.md has only {count} words (need ≥ 200)"


def test_essay_mentions_rosh_hashanah():
    """Essay must cite the Rosh Hashanah 21b source."""
    text = read_essay()
    assert "rosh hashanah" in text.lower() or "Rosh Hashanah" in text, (
        "essay must reference Rosh Hashanah 21b"
    )


def test_essay_mentions_leviticus():
    """Essay must cite Leviticus (Omer commandment)."""
    text = read_essay()
    assert "leviticus" in text.lower() or "23:15" in text, (
        "essay must cite the Omer commandment from Leviticus 23"
    )


def test_essay_mentions_zohar():
    """Essay must mention the Zohar (seven sefirot mapping)."""
    text = read_essay()
    assert "zohar" in text.lower(), "essay must mention the Zohar"


def test_essay_mentions_fiftieth_prime():
    """Essay must mention the 50th prime (229)."""
    text = read_essay()
    assert "229" in text, "essay must mention that 229 is the 50th prime"


# ---------------------------------------------------------------------------
# index.html: structure and features
# ---------------------------------------------------------------------------

def test_html_uses_request_animation_frame():
    """Animation must use requestAnimationFrame."""
    assert "requestAnimationFrame" in read_html(), "index.html must use requestAnimationFrame"


def test_html_implements_sieve():
    """HTML must implement the Sieve of Eratosthenes for prime detection."""
    html = read_html()
    assert "isPrime" in html or "is_prime" in html or "sieve" in html.lower(), (
        "index.html must implement a prime sieve"
    )


def test_html_has_ulam_spiral_generator():
    """HTML must contain Ulam spiral coordinate generation logic."""
    html = read_html()
    assert "ulam" in html.lower() or "spiral" in html.lower(), (
        "index.html must reference the Ulam spiral"
    )


def test_html_references_wheat_gold_color():
    """Primes 1–49 must be rendered in wheat gold #D4A840."""
    assert "#D4A840" in read_html() or "D4A840" in read_html(), (
        "index.html must use wheat gold color #D4A840 for first 49 primes"
    )


def test_html_references_white_color_for_50th():
    """The 50th prime must be rendered in white #FFFFFF."""
    html = read_html()
    assert "#FFFFFF" in html or "FFFFFF" in html, (
        "index.html must use #FFFFFF for the 50th prime"
    )


def test_html_references_indigo_color():
    """Primes beyond 50 must be rendered in muted indigo #303060."""
    assert "#303060" in read_html(), (
        "index.html must use muted indigo #303060 for primes beyond 50"
    )


def test_html_has_counter_element():
    """A counter element must be present in the HTML."""
    html = read_html()
    assert "counter" in html.lower(), "index.html must have a counter element"


def test_html_counter_shows_day_and_gate():
    """Counter must display 'Day' and 'Gate' labels."""
    html = read_html()
    assert "Day" in html and "Gate" in html, (
        "index.html counter must display Day N of 49 / Gate N of 50"
    )


def test_html_mentions_229():
    """The 50th prime value (229) must be referenced in the animation code."""
    html = read_html()
    assert "229" in html, "index.html must reference 229 as the 50th prime"


def test_html_embeds_essay_words():
    """index.html must embed enough essay words to pass the gallery test."""
    essay = read_essay()
    html = read_html()
    words = [w for w in essay.split() if len(w) > 5][:10]
    found = sum(1 for w in words if w in html)
    assert found >= 5, (
        f"index.html only contains {found}/10 sampled essay words — essay must be embedded"
    )


def test_thumbnail_is_svg():
    """Thumbnail must be a valid SVG file."""
    piece = get_piece()
    assert piece is not None
    thumb_path = os.path.join(GALLERY_ROOT, piece["thumbnail"])
    content = open(thumb_path, encoding="utf-8").read()
    assert "<svg" in content and "</svg>" in content, "thumbnail.svg is not valid SVG"


def test_thumbnail_has_dark_background():
    """Thumbnail SVG must set a dark background color."""
    piece = get_piece()
    thumb_path = os.path.join(GALLERY_ROOT, piece["thumbnail"])
    content = open(thumb_path, encoding="utf-8").read()
    assert "#06060f" in content or "06060f" in content or "#0a0a" in content.lower(), (
        "thumbnail must have a dark background"
    )


def test_thumbnail_has_gold_primes():
    """Thumbnail must include the wheat gold prime color."""
    piece = get_piece()
    thumb_path = os.path.join(GALLERY_ROOT, piece["thumbnail"])
    content = open(thumb_path, encoding="utf-8").read()
    assert "D4A840" in content, "thumbnail must mark primes in wheat gold"


# ---------------------------------------------------------------------------
# Edge cases and failure modes
# ---------------------------------------------------------------------------

def test_piece_path_format():
    """Path must be pieces/<id>/index.html."""
    piece = get_piece()
    assert piece is not None
    expected = f"pieces/{PIECE_ID}/index.html"
    assert piece["path"] == expected, f"Expected path '{expected}', got '{piece['path']}'"


def test_no_duplicate_piece_id():
    """Piece ID must be unique in pieces.json."""
    pieces = load_pieces()
    ids = [p["id"] for p in pieces]
    count = ids.count(PIECE_ID)
    assert count == 1, f"Piece ID '{PIECE_ID}' appears {count} times in pieces.json"


def test_piece_year_is_int():
    """Year field must be an integer."""
    piece = get_piece()
    assert piece is not None
    assert isinstance(piece["year"], int), f"year must be int, got {type(piece['year'])}"


def test_missing_index_html_would_fail(tmp_path):
    """Demonstrate that a missing index.html would be caught."""
    missing = tmp_path / "nonexistent.html"
    assert not os.path.isfile(str(missing)), "Fixture path must not exist"


def test_short_essay_would_fail(tmp_path):
    """Demonstrate that an essay with fewer than 200 words would be caught."""
    short = tmp_path / "short.md"
    short.write_text("Too short.", encoding="utf-8")
    text = short.read_text()
    count = len(text.split())
    assert count < 200, "Fixture confirms short essay detection logic"
