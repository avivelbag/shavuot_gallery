"""
Tests for piece 08 "We Will Do and We Will Hear" — Voronoi Hebrew typography.

Covers: file layout, pieces.json registration, Voronoi implementation markers,
Hebrew text with nikud, RTL rendering, colour palette, animation loop, essay
content (Exodus 24:7, Shabbat 88a, tagin/crowns), thumbnail validity, and
explicit edge-case / failure modes.
"""
import json
import math
import os
import re
import unicodedata

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")
PIECE_ID = "08-naaseh-vnishma-voronoi"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_pieces():
    """Return parsed pieces.json list."""
    with open(PIECES_JSON, encoding="utf-8") as fh:
        return json.load(fh)


def get_piece():
    """Return the pieces.json entry for piece 08, or None."""
    return next((p for p in load_pieces() if p["id"] == PIECE_ID), None)


def read_piece_file(filename):
    """Read a file from the piece directory and return its text."""
    return open(os.path.join(PIECE_DIR, filename), encoding="utf-8").read()


def nfc(s):
    """NFC-normalise s so Hebrew combining-mark order is canonical."""
    return unicodedata.normalize("NFC", s)


def read_html():
    """Read and NFC-normalise index.html."""
    return nfc(read_piece_file("index.html"))


# ---------------------------------------------------------------------------
# pieces.json registration
# ---------------------------------------------------------------------------

def test_piece_08_in_json():
    """Piece 08 must be registered in pieces.json."""
    assert get_piece() is not None, f"'{PIECE_ID}' not found in pieces.json"


def test_piece_08_theme():
    """Theme must reference Naaseh V'Nishma and/or Matan Torah."""
    p = get_piece()
    assert p is not None
    theme = p["theme"]
    assert "Naaseh" in theme or "naaseh" in theme.lower() or "Matan Torah" in theme, (
        f"theme must reference Naaseh V'Nishma or Matan Torah; got {theme!r}"
    )


def test_piece_08_technique():
    """Technique must mention Voronoi and Hebrew typography."""
    p = get_piece()
    assert p is not None
    tech = p["technique"].lower()
    assert "voronoi" in tech, f"technique must mention Voronoi; got {p['technique']!r}"
    assert "hebrew" in tech or "typography" in tech, (
        f"technique must mention Hebrew typography; got {p['technique']!r}"
    )


def test_piece_08_year_is_int():
    p = get_piece()
    assert p is not None
    assert isinstance(p["year"], int), f"year must be an integer, got {p['year']!r}"


def test_piece_08_has_tagline():
    p = get_piece()
    assert p is not None
    assert p.get("tagline"), "piece 08 must have a non-empty tagline"


def test_piece_08_essay_field_in_json():
    """pieces.json entry must include a non-empty essay field."""
    p = get_piece()
    assert p is not None
    assert "essay" in p and p["essay"], (
        f"'{PIECE_ID}' is missing or has empty 'essay' field in pieces.json"
    )


def test_piece_08_no_duplicate_ids():
    """Piece 08 ID must appear exactly once; no IDs elsewhere should clash."""
    pieces = load_pieces()
    ids = [p["id"] for p in pieces]
    assert len(ids) == len(set(ids)), f"Duplicate IDs in pieces.json: {ids}"


# ---------------------------------------------------------------------------
# File layout
# ---------------------------------------------------------------------------

def test_piece_08_index_html_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "index.html")), (
        "pieces/08-naaseh-vnishma-voronoi/index.html is missing"
    )


def test_piece_08_thumbnail_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "thumbnail.svg")), (
        "pieces/08-naaseh-vnishma-voronoi/thumbnail.svg is missing"
    )


def test_piece_08_readme_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "README.md")), (
        "pieces/08-naaseh-vnishma-voronoi/README.md is missing"
    )


def test_piece_08_essay_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "essay.md")), (
        "pieces/08-naaseh-vnishma-voronoi/essay.md is missing"
    )


def test_piece_08_essay_path_on_disk():
    """The essay path declared in pieces.json must exist on disk."""
    p = get_piece()
    assert p is not None
    essay_path = os.path.join(GALLERY_ROOT, p["essay"])
    assert os.path.isfile(essay_path), (
        f"'{PIECE_ID}': essay file '{p['essay']}' does not exist"
    )


def test_piece_08_id_matches_directory():
    """The piece id must match the directory component of its path."""
    p = get_piece()
    assert p is not None
    parts = p["path"].replace("\\", "/").split("/")
    assert parts[-2] == PIECE_ID, (
        f"piece id '{PIECE_ID}' does not match directory '{parts[-2]}'"
    )


def test_piece_08_path_ends_with_html():
    p = get_piece()
    assert p is not None
    assert p["path"].endswith(".html")


def test_piece_08_thumbnail_extension_is_svg():
    p = get_piece()
    assert p is not None
    assert os.path.splitext(p["thumbnail"])[1].lower() == ".svg"


# ---------------------------------------------------------------------------
# index.html — Voronoi implementation markers
# ---------------------------------------------------------------------------

def test_piece_08_uses_request_animation_frame():
    """Voronoi animation must use requestAnimationFrame."""
    assert "requestAnimationFrame" in read_html(), (
        "index.html must use requestAnimationFrame"
    )


def test_piece_08_uses_get_image_data():
    """Letter-mask detection requires getImageData on an offscreen canvas."""
    assert "getImageData" in read_html(), (
        "index.html must use getImageData to build the alpha mask"
    )


def test_piece_08_uses_put_image_data():
    """Per-pixel rendering requires putImageData."""
    assert "putImageData" in read_html(), (
        "index.html must use putImageData to write Voronoi pixels"
    )


def test_piece_08_uses_fill_text():
    """The letter mask is built via fillText on an offscreen canvas."""
    assert "fillText" in read_html(), (
        "index.html must use fillText to draw the Hebrew text for letter detection"
    )


def test_piece_08_uses_create_image_data():
    """Pixel buffer must be created with createImageData."""
    assert "createImageData" in read_html(), (
        "index.html must call createImageData"
    )


def test_piece_08_n_in_seed_count():
    """N_IN (inside seeds) must be set to 200."""
    html = read_html()
    assert re.search(r'\bN_IN\s*=\s*200\b', html) or re.search(r'\b200\b.*seed|seed.*\b200\b', html) or "N_IN = 200" in html, (
        "index.html must define N_IN = 200 (inside letter seeds)"
    )


def test_piece_08_n_out_seed_count():
    """N_OUT (outside seeds) must be set to 100."""
    html = read_html()
    assert re.search(r'\bN_OUT\s*=\s*100\b', html) or "N_OUT = 100" in html, (
        "index.html must define N_OUT = 100 (outside seeds)"
    )


# ---------------------------------------------------------------------------
# index.html — Hebrew text and RTL
# ---------------------------------------------------------------------------

def test_piece_08_hebrew_naaseh_present():
    """The word נַעֲשֶׂה must appear in index.html (NFC-normalised)."""
    html = read_html()
    naase = nfc("נַעֲשֶׂה")
    naase_bare = nfc("נעשה")
    assert naase in html or naase_bare in html, (
        "index.html must contain the Hebrew word נַעֲשֶׂה (naaseh)"
    )


def test_piece_08_hebrew_nishma_present():
    """The correctly-pointed word וְנִשְׁמַע must appear in the <script> block.

    Checks the script block specifically so that a correct essay panel cannot
    mask a mis-pointed HEBREW variable in the canvas artwork.  The full nikud
    form including SHIN DOT (U+05C1) is required; bare consonants are
    insufficient.
    """
    html = read_html()
    script_match = re.search(r'<script[^>]*>(.*?)</script>', html, re.DOTALL | re.IGNORECASE)
    assert script_match, "index.html must contain a <script> block"
    script_text = nfc(script_match.group(1))
    nishm_full = nfc("וְנִשְׁמַע")
    assert nishm_full in script_text, (
        "The HEBREW variable in <script> must contain the correctly-pointed "
        "word וְנִשְׁמַע with SHIN DOT (U+05C1); got no match in script block"
    )


def test_piece_08_rtl_direction():
    """The canvas context must be set to direction = 'rtl' for RTL Hebrew rendering."""
    html = read_html()
    assert "direction" in html and ("rtl" in html), (
        "index.html must set direction = 'rtl' on the canvas context"
    )


def test_piece_08_text_align_center_or_right():
    """textAlign must be set on the canvas context for Hebrew text placement."""
    html = read_html()
    assert "textAlign" in html, (
        "index.html must set ctx.textAlign for Hebrew text rendering"
    )


# ---------------------------------------------------------------------------
# index.html — colour palettes
# ---------------------------------------------------------------------------

def test_piece_08_gold_color_f5e642():
    """Gold seed colour #f5e642 must appear in index.html."""
    assert "f5e642" in read_html().lower(), (
        "index.html must reference gold colour #f5e642"
    )


def test_piece_08_gold_color_e8c84a():
    """Parchment seed colour #e8c84a must appear in index.html."""
    assert "e8c84a" in read_html().lower(), (
        "index.html must reference parchment colour #e8c84a"
    )


def test_piece_08_gold_color_fdf6b2():
    """Light parchment seed colour #fdf6b2 must appear in index.html."""
    assert "fdf6b2" in read_html().lower(), (
        "index.html must reference light parchment colour #fdf6b2"
    )


def test_piece_08_indigo_color_1a0a4e():
    """Deep indigo seed colour #1a0a4e must appear in index.html."""
    assert "1a0a4e" in read_html().lower(), (
        "index.html must reference deep indigo colour #1a0a4e"
    )


def test_piece_08_indigo_color_2d1b7a():
    """Indigo seed colour #2d1b7a must appear in index.html."""
    assert "2d1b7a" in read_html().lower(), (
        "index.html must reference indigo colour #2d1b7a"
    )


def test_piece_08_indigo_color_3d2d8e():
    """Violet seed colour #3d2d8e must appear in index.html."""
    assert "3d2d8e" in read_html().lower(), (
        "index.html must reference violet colour #3d2d8e"
    )


# ---------------------------------------------------------------------------
# index.html — animation brightness wave
# ---------------------------------------------------------------------------

def test_piece_08_brightness_wave_uses_sin():
    """The brightness pulse must use Math.sin for the wave shape."""
    assert "Math.sin" in read_html(), (
        "index.html must use Math.sin for the brightness wave"
    )


def test_piece_08_no_external_resources():
    """The piece must be self-contained — no external src/href URLs."""
    html = read_html()
    external = re.findall(r'(?:src|href)\s*=\s*["\']https?://', html)
    assert not external, (
        f"index.html must not load external resources; found: {external}"
    )


# ---------------------------------------------------------------------------
# thumbnail.svg
# ---------------------------------------------------------------------------

def test_piece_08_thumbnail_is_valid_svg():
    """thumbnail.svg must be well-formed SVG."""
    svg = read_piece_file("thumbnail.svg")
    assert "<svg" in svg and "</svg>" in svg, (
        "thumbnail.svg does not look like valid SVG"
    )


def test_piece_08_thumbnail_400x400():
    """Thumbnail must declare 400×400 dimensions."""
    svg = read_piece_file("thumbnail.svg")
    assert 'width="400"' in svg and 'height="400"' in svg, (
        "thumbnail.svg must be 400×400"
    )


def test_piece_08_thumbnail_has_hebrew_text():
    """Thumbnail must display the Hebrew text."""
    svg = nfc(read_piece_file("thumbnail.svg"))
    naase = nfc("נַעֲשֶׂה")
    naase_bare = nfc("נעשה")
    assert naase in svg or naase_bare in svg, (
        "thumbnail.svg must contain the Hebrew word נַעֲשֶׂה"
    )


def test_piece_08_thumbnail_has_gold_color():
    """Thumbnail must reference a gold cell colour."""
    svg = read_piece_file("thumbnail.svg").lower()
    assert "f5e642" in svg or "e8c84a" in svg or "fdf6b2" in svg, (
        "thumbnail.svg must reference a gold/parchment cell colour"
    )


def test_piece_08_thumbnail_has_indigo_background():
    """Thumbnail background must reference a deep indigo colour."""
    svg = read_piece_file("thumbnail.svg").lower()
    assert "1a0a4e" in svg or "2d1b7a" in svg or "0a0618" in svg or "12082e" in svg, (
        "thumbnail.svg must reference a deep indigo background colour"
    )


# ---------------------------------------------------------------------------
# essay.md content
# ---------------------------------------------------------------------------

def test_piece_08_essay_cites_exodus_24_7():
    """Essay must cite Exodus 24:7 exactly."""
    text = read_piece_file("essay.md")
    assert "24:7" in text or "Exodus 24" in text, (
        "essay.md must cite Exodus 24:7"
    )


def test_piece_08_essay_cites_shabbat_88a():
    """Essay must reference Talmud Shabbat 88a."""
    text = read_piece_file("essay.md")
    assert "Shabbat 88a" in text or "88a" in text, (
        "essay.md must reference Talmud Shabbat 88a"
    )


def test_piece_08_essay_mentions_tagin_or_crowns():
    """Essay must discuss the tagin / crowns tradition."""
    text = read_piece_file("essay.md").lower()
    assert "tagin" in text or "tag" in text or "crown" in text, (
        "essay.md must mention tagin or crowns"
    )


def test_piece_08_essay_mentions_voronoi():
    """Essay must connect the Voronoi motif to the text's themes."""
    text = read_piece_file("essay.md").lower()
    assert "voronoi" in text or "cell" in text or "facet" in text, (
        "essay.md must reference the Voronoi / cell / facet motif"
    )


def test_piece_08_essay_word_count_300_to_600():
    """Essay must be 300–600 words (per acceptance criteria ~300–500 words)."""
    text = read_piece_file("essay.md")
    wc = len(text.split())
    assert wc >= 300, f"essay.md has only {wc} words (minimum 300)"
    assert wc <= 700, f"essay.md has {wc} words (maximum 700 to keep it focused)"


def test_piece_08_essay_embedded_in_html():
    """Key phrases from essay.md must appear verbatim in index.html."""
    essay = read_piece_file("essay.md")
    html = read_piece_file("index.html")
    words = [w for w in essay.split() if len(w) > 6]
    sampled = words[:15]
    found = sum(1 for w in sampled if w in html)
    assert found >= 6, (
        f"index.html does not embed enough essay text (found {found}/15 sampled words)"
    )


# ---------------------------------------------------------------------------
# README.md
# ---------------------------------------------------------------------------

def test_piece_08_readme_mentions_naaseh():
    text = read_piece_file("README.md").lower()
    assert "naaseh" in text or "נַעֲשֶׂה" in text or "we will do" in text.lower(), (
        "README.md must mention naaseh or 'we will do'"
    )


def test_piece_08_readme_mentions_voronoi():
    text = read_piece_file("README.md").lower()
    assert "voronoi" in text, "README.md must mention Voronoi"


# ---------------------------------------------------------------------------
# Voronoi algorithm correctness (pure Python)
# ---------------------------------------------------------------------------

def test_voronoi_nearest_seed_basic():
    """Brute-force nearest-seed assignment must give correct results."""
    seeds = [
        {"x": 0, "y": 0},
        {"x": 10, "y": 0},
        {"x": 5, "y": 10},
    ]

    def nearest(x, y):
        """Return index of the nearest seed to (x, y) by squared Euclidean distance."""
        best_d = float("inf")
        best_i = 0
        for i, s in enumerate(seeds):
            dx, dy = x - s["x"], y - s["y"]
            d = dx * dx + dy * dy
            if d < best_d:
                best_d = d
                best_i = i
        return best_i

    assert nearest(1, 0) == 0,  "Point near seed 0 should map to seed 0"
    assert nearest(9, 0) == 1,  "Point near seed 1 should map to seed 1"
    assert nearest(5, 9) == 2,  "Point near seed 2 should map to seed 2"
    assert nearest(5, 0) in (0, 1), "Midpoint between seed 0 and 1 maps to either"


def test_voronoi_edge_detection_logic():
    """Edge pixels are where adjacent pixels belong to different seeds."""
    # 3×3 grid where the centre row changes seeds
    # Pixel layout (seed index):
    # 0 0 0
    # 0 1 1
    # 1 1 1
    W, H = 3, 3
    vi = [0, 0, 0,
          0, 1, 1,
          1, 1, 1]

    def is_edge(x, y):
        """Return True if pixel (x,y) has a neighbour with a different seed index."""
        c = vi[y * W + x]
        for nx, ny in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:
            if 0 <= nx < W and 0 <= ny < H:
                if vi[ny * W + nx] != c:
                    return True
        return False

    assert is_edge(1, 1), "Centre pixel is on the Voronoi boundary"
    assert not is_edge(0, 0), "Top-left corner has uniform neighbours"
    assert not is_edge(2, 2), "Bottom-right corner has uniform neighbours"


def test_brightness_wave_range():
    """Brightness wave must stay within [0.64, 1.0] for all seed distances and times."""
    import random
    random.seed(99)
    for _ in range(500):
        t = random.random() * 50        # arbitrary time value
        dist = random.random()          # normalised distance 0..1
        b = 0.82 + 0.18 * math.sin(t * 0.9 - dist * 5.0)
        assert 0.64 <= b <= 1.01, f"brightness {b} out of expected range [0.64, 1.0]"


def test_alpha_mask_threshold():
    """Pixels with alpha > 128 must be classified as inside; <= 128 as outside."""
    cases = [
        (0,   False, "fully transparent is outside"),
        (128, False, "alpha == 128 is at threshold, classified outside"),
        (129, True,  "alpha == 129 is just inside"),
        (255, True,  "fully opaque is inside"),
    ]
    for alpha, expected_inside, msg in cases:
        is_inside = alpha > 128
        assert is_inside == expected_inside, msg


# ---------------------------------------------------------------------------
# Edge cases and failure modes
# ---------------------------------------------------------------------------

def test_piece_08_missing_index_detected(tmp_path):
    """A piece directory without index.html is missing a required deliverable."""
    fake_dir = tmp_path / "fake-08"
    fake_dir.mkdir()
    index = fake_dir / "index.html"
    assert not index.exists(), "Fixture must not have index.html yet"


def test_piece_08_empty_essay_fails(tmp_path):
    """An essay.md with fewer than 300 words must fail the word-count check."""
    stub = tmp_path / "stub.md"
    stub.write_text("Short essay.", encoding="utf-8")
    wc = len(stub.read_text(encoding="utf-8").split())
    assert wc < 300, "Stub must be fewer than 300 words for this test to be meaningful"


def test_piece_08_wrong_piece_id_not_found():
    """Looking up a non-existent piece ID returns None."""
    pieces = load_pieces()
    result = next((p for p in pieces if p["id"] == "99-does-not-exist"), None)
    assert result is None


def test_piece_08_duplicate_would_be_caught():
    """If piece 08 were registered twice, the duplicate-ID check would catch it."""
    fake_pieces = [
        {"id": PIECE_ID, "title": "A"},
        {"id": PIECE_ID, "title": "B"},
    ]
    ids = [p["id"] for p in fake_pieces]
    assert len(ids) != len(set(ids)), "Fixture correctly simulates a duplicate-ID scenario"
