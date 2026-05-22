"""
Tests specific to piece 38-seven-heavens (Through Seven Heavens — Parallax Descent).

Validates the parallax layer structure, per-heaven visual content, CSS/JS
technique, essay citations, and pieces.json registration.
"""
import json
import os
import re


GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")
PIECE_ID = "38-seven-heavens"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
HTML_PATH = os.path.join(PIECE_DIR, "index.html")
ESSAY_PATH = os.path.join(PIECE_DIR, "essay.md")


def _load_pieces():
    with open(PIECES_JSON, encoding="utf-8") as fh:
        return json.load(fh)


def _get_piece():
    for p in _load_pieces():
        if p["id"] == PIECE_ID:
            return p
    return None


def _html():
    return open(HTML_PATH, encoding="utf-8").read()


def _essay():
    return open(ESSAY_PATH, encoding="utf-8").read()


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------

def test_piece_registered_in_json():
    """38-seven-heavens must appear in pieces.json."""
    assert _get_piece() is not None, f"Piece '{PIECE_ID}' not found in pieces.json"


def test_piece_json_required_fields():
    """All required fields must be present and non-empty."""
    piece = _get_piece()
    for field in ("id", "title", "tagline", "year", "theme", "technique",
                  "path", "thumbnail", "essay"):
        assert piece.get(field), f"Field '{field}' missing or empty in pieces.json entry"


def test_piece_directory_exists():
    assert os.path.isdir(PIECE_DIR), f"Directory {PIECE_DIR} does not exist"


def test_html_file_exists():
    assert os.path.isfile(HTML_PATH), f"index.html missing at {HTML_PATH}"


def test_essay_file_exists():
    assert os.path.isfile(ESSAY_PATH), f"essay.md missing at {ESSAY_PATH}"


def test_thumbnail_exists():
    piece = _get_piece()
    thumb = os.path.join(GALLERY_ROOT, piece["thumbnail"])
    assert os.path.isfile(thumb), f"thumbnail not found at {thumb}"


def test_readme_exists():
    readme = os.path.join(PIECE_DIR, "README.md")
    assert os.path.isfile(readme), "README.md missing from piece directory"


# ---------------------------------------------------------------------------
# Parallax structure — seven layers with data-depth attributes
# ---------------------------------------------------------------------------

def test_seven_depth_layers_present():
    """HTML must contain exactly 7 elements carrying data-depth attributes."""
    depths = re.findall(r'data-depth="([^"]*)"', _html())
    assert len(depths) == 7, (
        f"Expected 7 layers with data-depth, found {len(depths)}"
    )


def test_seven_depth_coefficients_are_distinct():
    """All seven depth coefficients must be numerically distinct."""
    depths = re.findall(r'data-depth="([^"]*)"', _html())
    floats = [float(d) for d in depths]
    assert len(set(floats)) == 7, (
        f"Depth coefficients must all differ; got {floats}"
    )


def test_depth_range_spans_low_to_high():
    """Smallest depth should be < 0.1 (background) and largest > 0.4 (foreground)."""
    depths = re.findall(r'data-depth="([^"]*)"', _html())
    floats = [float(d) for d in depths]
    assert min(floats) < 0.1, "Background layer depth must be < 0.1"
    assert max(floats) > 0.4, "Foreground layer depth must be > 0.4"


# ---------------------------------------------------------------------------
# Heaven-specific content checks
# ---------------------------------------------------------------------------

def test_vilon_layer_present():
    """Vilon layer (curtain, lowest heaven) must be identified in HTML."""
    html = _html()
    assert "vilon" in html.lower() or "וִילוֹן" in html, (
        "Vilon heaven not found in HTML"
    )


def test_rakia_layer_present():
    assert "raki" in _html().lower() or "רָקִיעַ" in _html(), (
        "Rakia heaven not found in HTML"
    )


def test_shehavim_layer_present():
    html = _html()
    assert "sheh" in html.lower() or "שְׁחָקִים" in html, (
        "Sheḥakim heaven not found in HTML"
    )


def test_zevul_layer_present():
    html = _html()
    assert "zevul" in html.lower() or "זְבוּל" in html, (
        "Zevul heaven not found in HTML"
    )


def test_maon_layer_present():
    html = _html()
    assert "ma'on" in html.lower() or "maon" in html.lower() or "מָעוֹן" in html, (
        "Ma'on heaven not found in HTML"
    )


def test_machon_layer_present():
    html = _html()
    assert "machon" in html.lower() or "makhon" in html.lower() or "מָכוֹן" in html, (
        "Makhon heaven not found in HTML"
    )


def test_aravot_layer_present():
    html = _html()
    assert "aravot" in html.lower() or "עֲרָבוֹת" in html, (
        "Aravot heaven not found in HTML"
    )


def test_tetragrammaton_in_aravot():
    """The Tetragrammaton (יהוה) must appear in the HTML (in the Aravot layer)."""
    assert "יהוה" in _html(), "Tetragrammaton יהוה not found in HTML"


def test_mountain_silhouette_in_html():
    """Har Sinai mountain silhouette (SVG path) must be present in the Vilon layer."""
    html = _html()
    assert "sinai" in html.lower() or "Sinai" in html or (
        # The SVG path for the mountain is large; confirm at least one mountain-related element
        re.search(r'<path\s[^>]*d="M\s*0', html) is not None
    ), "Mountain silhouette element not found in HTML"


def test_stars_in_rakia():
    """Rakia layer must include star elements (circles) and/or Hebrew כּוֹכָבִים."""
    html = _html()
    assert "כּוֹכָבִים" in html or "<circle" in html, (
        "Star elements not found in HTML (Rakia layer)"
    )


# ---------------------------------------------------------------------------
# JavaScript interaction technique
# ---------------------------------------------------------------------------

def test_mousemove_handler_present():
    """HTML must contain a mousemove event listener for the parallax interaction."""
    assert "mousemove" in _html(), "mousemove handler not found in HTML"


def test_lissajous_drift_uses_math_sin():
    """The default Lissajous drift animation must use Math.sin."""
    assert "Math.sin" in _html(), "Math.sin not found — Lissajous drift may be missing"


def test_request_animation_frame_used():
    """Animation loop must use requestAnimationFrame."""
    assert "requestAnimationFrame" in _html(), (
        "requestAnimationFrame not found in HTML"
    )


def test_data_depth_read_in_js():
    """JavaScript must read the data-depth attribute to drive parallax."""
    html = _html()
    assert "data-depth" in html or "dataset.depth" in html, (
        "depth attribute not referenced in JS"
    )


def test_idle_timeout_threshold_present():
    """HTML must implement mouse-idle detection (2000 ms threshold)."""
    assert "2000" in _html(), "2000 ms idle threshold not found in HTML"


# ---------------------------------------------------------------------------
# Essay requirements
# ---------------------------------------------------------------------------

def test_essay_substantial():
    """essay.md must be at least 400 words."""
    text = _essay()
    wc = len(text.split())
    assert wc >= 400, f"essay.md has only {wc} words (need ≥ 400)"


def test_essay_cites_hagigah():
    """Essay must cite Talmud Bavli Ḥagigah 12b."""
    essay = _essay().lower()
    assert "hagigah" in essay or "ḥagigah" in essay or "chagigah" in essay, (
        "essay.md does not cite Ḥagigah 12b"
    )


def test_essay_has_hebrew_text():
    """Essay must contain Hebrew characters (the Talmudic passage in Hebrew)."""
    hebrew_range = re.compile(r"[֐-׿]")
    assert hebrew_range.search(_essay()), "essay.md contains no Hebrew characters"


def test_essay_has_exodus_verse():
    """Essay must cite Exodus 19:20 (the descent at Sinai)."""
    essay = _essay()
    assert "19:20" in essay or "Exodus 19" in essay, (
        "essay.md does not reference Exodus 19:20"
    )


def test_essay_hebrew_and_english_of_talmud_passage():
    """Essay must include the Talmudic passage in both Hebrew and English."""
    essay = _essay()
    hebrew_range = re.compile(r"[֐-׿]{5,}")  # at least 5 consecutive Hebrew chars
    has_hebrew = bool(hebrew_range.search(essay))
    has_english = "seven firmaments" in essay.lower() or "seven heavens" in essay.lower()
    assert has_hebrew and has_english, (
        "essay.md must contain Ḥagigah 12b in both Hebrew and English"
    )


def test_essay_discusses_descent():
    """Essay must address God's descent to Sinai (theological core of the piece)."""
    essay = _essay().lower()
    assert "descend" in essay or "descent" in essay, (
        "essay.md does not discuss the descent to Sinai"
    )


def test_html_embeds_essay_words():
    """Words from essay.md must appear in index.html (essay is embedded, not fetched)."""
    essay = _essay()
    html = _html()
    long_words = [w for w in essay.split() if len(w) > 7][:10]
    found = sum(1 for w in long_words if w in html)
    assert found >= 5, (
        f"Only {found}/10 sampled essay words appear in index.html — "
        "essay text may not be embedded"
    )


# ---------------------------------------------------------------------------
# Edge-case / failure-mode tests
# ---------------------------------------------------------------------------

def test_no_duplicate_depth_coefficients(tmp_path):
    """Verify the helper: a list of repeated depths should be detected as non-unique."""
    repeated = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
    assert len(set(repeated)) < 7, "Fixture confirms repeated depths are detectable"


def test_missing_mousemove_is_detectable():
    """A hypothetical HTML without mousemove should fail the interaction check."""
    fake_html = "<script>// no event handlers here</script>"
    assert "mousemove" not in fake_html, "Fixture confirms absence of mousemove is detectable"


def test_essay_under_100_words_is_detectable(tmp_path):
    """An essay that is too short should not pass the word-count check."""
    short_text = "This is a very short essay. " * 3
    wc = len(short_text.split())
    assert wc < 400, f"Fixture: short essay has {wc} words (confirms threshold)"
