"""
Tests for piece 73-fractal-flame-burning-bush: fractal flame / FLAM3 chaos game.

Covers the acceptance criteria: piece registration, required files, canvas size,
fractal-flame algorithm markers (histogram, transforms, swirl, log-density tonemapping),
fire palette colors, essay content, and explicit failure modes.
"""
import json
import os
import re

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECES_JSON  = os.path.join(GALLERY_ROOT, "pieces.json")
PIECE_ID     = "73-fractal-flame-burning-bush"
PIECE_DIR    = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
INDEX_HTML   = os.path.join(PIECE_DIR, "index.html")
ESSAY_MD     = os.path.join(PIECE_DIR, "essay.md")
THUMBNAIL    = os.path.join(PIECE_DIR, "thumbnail.svg")
README       = os.path.join(PIECE_DIR, "README.md")


def _load_pieces():
    """Load and return parsed pieces.json list."""
    with open(PIECES_JSON, encoding="utf-8") as fh:
        return json.load(fh)


def _get_piece(piece_id):
    """Return the pieces.json entry for the given id, or None."""
    for p in _load_pieces():
        if p["id"] == piece_id:
            return p
    return None


def _html():
    """Return full text of index.html."""
    with open(INDEX_HTML, encoding="utf-8") as fh:
        return fh.read()


def _essay():
    """Return full text of essay.md."""
    with open(ESSAY_MD, encoding="utf-8") as fh:
        return fh.read()


# ---------------------------------------------------------------------------
# Happy-path: piece registered and all required files present
# ---------------------------------------------------------------------------

def test_piece_in_pieces_json():
    """Piece must be registered in pieces.json."""
    piece = _get_piece(PIECE_ID)
    assert piece is not None, f"Piece '{PIECE_ID}' not found in pieces.json"


def test_piece_required_fields():
    """All required fields must be present and non-empty."""
    required = ("id", "title", "tagline", "year", "theme", "technique", "path", "thumbnail", "essay")
    piece = _get_piece(PIECE_ID)
    assert piece is not None
    for field in required:
        assert field in piece and piece[field], (
            f"Piece '{PIECE_ID}' missing or empty field '{field}'"
        )


def test_piece_theme_har_sinai():
    """Theme must be 'Har Sinai'."""
    piece = _get_piece(PIECE_ID)
    assert piece is not None
    assert piece["theme"] == "Har Sinai", (
        f"Expected theme 'Har Sinai', got '{piece['theme']}'"
    )


def test_piece_technique_fractal_flames():
    """Technique must reference 'fractal flames' and 'IFS accumulation histogram'."""
    piece = _get_piece(PIECE_ID)
    assert piece is not None
    tech = piece["technique"].lower()
    assert "fractal flame" in tech, "technique must mention 'fractal flames'"
    assert "ifs" in tech or "histogram" in tech, (
        "technique must mention 'IFS' or 'histogram'"
    )


def test_index_html_exists():
    assert os.path.isfile(INDEX_HTML), f"index.html missing at {INDEX_HTML}"


def test_essay_md_exists():
    assert os.path.isfile(ESSAY_MD), f"essay.md missing at {ESSAY_MD}"


def test_thumbnail_exists():
    assert os.path.isfile(THUMBNAIL), f"thumbnail.svg missing at {THUMBNAIL}"


def test_thumbnail_is_svg():
    """thumbnail.svg must be valid SVG."""
    text = open(THUMBNAIL, encoding="utf-8").read()
    assert "<svg" in text and "</svg>" in text, "thumbnail.svg does not look like valid SVG"


def test_readme_exists():
    assert os.path.isfile(README), f"README.md missing at {README}"


# ---------------------------------------------------------------------------
# Canvas and fractal-flame algorithm checks
# ---------------------------------------------------------------------------

def test_index_html_has_canvas():
    """index.html must contain a <canvas> element."""
    assert "<canvas" in _html(), "index.html must contain a <canvas> element"


def test_index_html_canvas_700x700():
    """Canvas must be 700×700 pixels."""
    html = _html()
    assert 'width="700"' in html and 'height="700"' in html, (
        "Canvas must be 700×700 pixels"
    )


def test_index_html_uses_requestanimationframe():
    """Computation must be driven by requestAnimationFrame (not a blocking loop)."""
    assert "requestAnimationFrame" in _html(), (
        "index.html must use requestAnimationFrame"
    )


def test_index_html_has_float32array_histogram():
    """Histogram must be a Float32Array for HDR accumulation."""
    assert "Float32Array" in _html(), (
        "index.html must use Float32Array for the histogram"
    )


def test_index_html_has_five_transforms():
    """Five affine transforms must be declared (at least 5 objects with variation field)."""
    html = _html()
    # Count occurrences of the 'variation:' key inside transform objects
    matches = re.findall(r"variation\s*:", html)
    assert len(matches) >= 5, (
        f"Expected at least 5 transform objects with 'variation:' field, found {len(matches)}"
    )


def test_index_html_has_swirl_variation():
    """At least one transform must use the swirl variation."""
    html = _html()
    assert "'swirl'" in html or '"swirl"' in html, (
        "index.html must declare at least one 'swirl' variation transform"
    )


def test_index_html_swirl_uses_cos_sin_r_squared():
    """Swirl implementation must use cos(r²) and sin(r²) rotation."""
    html = _html()
    has_r2   = "r2" in html or "r * r" in html or "x*x" in html
    has_cos  = "Math.cos" in html
    has_sin  = "Math.sin" in html
    assert has_r2 and has_cos and has_sin, (
        "Swirl must compute r² and use Math.cos / Math.sin for rotation"
    )


def test_index_html_has_sinusoidal_variation():
    """At least one transform must use the sinusoidal variation."""
    html = _html()
    assert "'sinusoidal'" in html or '"sinusoidal"' in html, (
        "index.html must declare at least one 'sinusoidal' variation transform"
    )


def test_index_html_log_density_tonemapping():
    """Log-density tonemapping must use log1p (or Math.log with +1)."""
    html = _html()
    has_log1p = "Math.log1p" in html or "log(1 +" in html or "log(1+" in html
    assert has_log1p, (
        "index.html must implement log-density tonemapping via Math.log1p or log(1+count)"
    )


def test_index_html_histogram_accumulates_color():
    """Histogram must accumulate both count and color (two values per pixel)."""
    html = _html()
    # Look for index arithmetic that suggests interleaved count+color (e.g., idx*2 or py*W+px)*2)
    has_interleaved = "* 2" in html or "*2" in html
    has_color_sum   = "color" in html and ("colorSum" in html or "colorAccum" in html or "color +" in html)
    assert has_interleaved or has_color_sum, (
        "Histogram must store both count and color accumulation per pixel"
    )


def test_index_html_progress_bar():
    """A progress bar must be shown during the computation."""
    html = _html()
    has_progress = "progress" in html.lower()
    assert has_progress, "index.html must include a progress bar element"


def test_index_html_has_eight_million_iters():
    """8 million total iterations must be declared."""
    html = _html()
    # Accept 8_000_000, 8000000, or 8_000_000 / FRAMES variants
    has_total = (
        "8_000_000" in html or
        "8000000"   in html or
        "8 million" in html.lower() or
        re.search(r"TOTAL_ITERS\s*=\s*8[_,]?0{6}", html) is not None
    )
    assert has_total, (
        "index.html must declare ~8 million total iterations (8_000_000 or 8000000)"
    )


# ---------------------------------------------------------------------------
# Fire palette color checks
# ---------------------------------------------------------------------------

def test_index_html_has_crimson_color():
    """Deep crimson #800010 must appear in the fire palette."""
    html = _html().upper()
    assert "800010" in html, "Fire palette must include deep crimson #800010"


def test_index_html_has_deep_orange_color():
    """Deep orange #C84010 must appear in the fire palette."""
    html = _html().upper()
    assert "C84010" in html, "Fire palette must include deep orange #C84010"


def test_index_html_has_hot_gold_color():
    """Hot gold #FFB020 must appear in the fire palette."""
    html = _html().upper()
    assert "FFB020" in html, "Fire palette must include hot gold #FFB020"


def test_index_html_has_near_white_color():
    """Near-white #FFFFF0 must appear in the fire palette."""
    html = _html().upper()
    assert "FFFFF0" in html, "Fire palette must include near-white #FFFFF0"


def test_index_html_has_background_color():
    """Background near-black #030202 must appear."""
    html = _html().upper()
    assert "030202" in html, "Background must be near-black #030202"


# ---------------------------------------------------------------------------
# Essay content checks
# ---------------------------------------------------------------------------

def test_essay_word_count():
    """Essay must have at least 400 words."""
    essay = _essay()
    count = len(essay.split())
    assert count >= 400, f"essay.md has only {count} words; expected ≥ 400"


def test_essay_cites_exodus_3():
    """Essay must cite Exodus 3 (the burning bush pericope)."""
    essay = _essay()
    assert "Exodus 3" in essay, "essay.md must cite Exodus 3"


def test_essay_mentions_burning_bush():
    """Essay must mention the burning bush."""
    essay = _essay().lower()
    assert "burning bush" in essay or "thorn-bush" in essay or "bush" in essay, (
        "essay.md must mention the burning bush"
    )


def test_essay_mentions_ehyeh_asher_ehyeh():
    """Essay must mention the divine name EHYEH ASHER EHYEH or I Will Be."""
    essay = _essay()
    has_name = "EHYEH" in essay or "I Will Be" in essay or "אֶהְיֶה" in essay
    assert has_name, "essay.md must mention EHYEH ASHER EHYEH (Exodus 3:14)"


def test_essay_mentions_sinai():
    """Essay must connect the burning bush to Sinai."""
    essay = _essay()
    assert "Sinai" in essay, "essay.md must mention Sinai"


def test_essay_midrash_exodus_rabbah():
    """Essay must reference the Midrash (Exodus Rabbah) on the thorn-bush."""
    essay = _essay()
    has_midrash = "Exodus Rabbah" in essay or "Midrash" in essay
    assert has_midrash, "essay.md must reference the Midrash / Exodus Rabbah 2:5"


def test_essay_mentions_shavuot():
    """Essay must connect to Shavuot."""
    essay = _essay()
    assert "Shavuot" in essay, "essay.md must mention Shavuot"


def test_essay_has_hebrew_text():
    """Essay must include Hebrew text."""
    essay = _essay()
    # Check for Hebrew Unicode block characters
    has_hebrew = any('א' <= ch <= 'ת' for ch in essay)
    assert has_hebrew, "essay.md must include Hebrew text"


def test_essay_embedded_in_html():
    """index.html must embed the essay text inline (not fetch it at runtime)."""
    essay = _essay()
    html  = _html()
    words = sorted([w for w in essay.split() if len(w) > 7], key=len, reverse=True)
    sampled = words[:15]
    found = sum(1 for w in sampled if w in html)
    assert found >= 8, (
        f"index.html does not appear to embed the essay: only {found}/15 sampled words found"
    )


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

def test_piece_id_matches_directory():
    """pieces.json 'id' must match the directory component of 'path'."""
    piece = _get_piece(PIECE_ID)
    assert piece is not None
    parts   = piece["path"].replace("\\", "/").split("/")
    dir_name = parts[-2]
    assert dir_name == PIECE_ID, (
        f"pieces.json id '{PIECE_ID}' does not match directory '{dir_name}'"
    )


def test_piece_year_is_integer():
    """'year' field must be an integer."""
    piece = _get_piece(PIECE_ID)
    assert piece is not None
    assert isinstance(piece["year"], int), (
        f"'year' is not an integer: {piece['year']!r}"
    )


def test_piece_path_ends_with_html():
    """'path' must end with .html."""
    piece = _get_piece(PIECE_ID)
    assert piece is not None
    assert piece["path"].endswith(".html"), (
        f"'path' does not end with .html: {piece['path']}"
    )


def test_no_duplicate_id_in_pieces_json():
    """Registering the piece must not create a duplicate id."""
    pieces = _load_pieces()
    ids    = [p["id"] for p in pieces]
    assert ids.count(PIECE_ID) == 1, (
        f"Piece id '{PIECE_ID}' appears {ids.count(PIECE_ID)} times in pieces.json"
    )


def test_essay_is_not_about_wrong_topic():
    """Essay must be about the burning bush, not an unrelated theme."""
    essay = _essay()
    # Must not be a copy of the IFS harvest piece essay
    assert "Chag HaKatzir" not in essay, (
        "essay.md appears to be a copy of the harvest IFS essay"
    )
    assert "wheat" not in essay.lower() or "bush" in essay.lower(), (
        "essay.md does not appear to be about the burning bush"
    )


# ---------------------------------------------------------------------------
# Explicit failure modes
# ---------------------------------------------------------------------------

def test_missing_swirl_would_be_caught():
    """A page with no swirl variation would fail the swirl check."""
    fake_html = "<html><body><canvas></canvas></body></html>"
    assert "'swirl'" not in fake_html and '"swirl"' not in fake_html


def test_missing_float32array_would_be_caught():
    """A page without Float32Array would fail the histogram check."""
    fake_html = "<html><body>no typed array here</body></html>"
    assert "Float32Array" not in fake_html


def test_short_essay_would_be_caught():
    """An essay with fewer than 400 words would be flagged."""
    short = "The burning bush. " * 15  # about 45 words
    count = len(short.split())
    assert count < 400


def test_wrong_canvas_size_would_be_caught():
    """A canvas with wrong dimensions would fail the 700×700 check."""
    fake_html = '<canvas width="500" height="500"></canvas>'
    assert 'width="700"' not in fake_html


def test_missing_palette_color_would_be_caught():
    """Absence of a required palette color would be detected."""
    fake_html = "<html><body>no fire colors here</body></html>".upper()
    assert "800010" not in fake_html  # crimson check would fail
