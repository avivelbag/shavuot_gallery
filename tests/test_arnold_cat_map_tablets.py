"""
Tests for piece 88-arnold-cat-map-tablets.

Covers:
- pieces.json registration and required fields
- On-disk file layout (index.html, essay.md, thumbnail.svg, README.md)
- Arnold cat map correctness (period, bijection property)
- HTML content: Uint32Array double buffering, arnoldStep, fire tint, phase constants
- Essay content: Exodus reference, Talmud, Midrash citations
- Edge cases: empty/malformed data, missing files
"""
import json
import os

import pytest

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")
PIECE_ID = "88-arnold-cat-map-tablets"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)


def load_pieces():
    with open(PIECES_JSON, encoding="utf-8") as fh:
        return json.load(fh)


def get_piece():
    for p in load_pieces():
        if p["id"] == PIECE_ID:
            return p
    return None


def read_html():
    return open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()


def read_essay():
    return open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()


def read_thumbnail():
    return open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------

def test_piece_registered_in_json():
    piece = get_piece()
    assert piece is not None, f"Piece '{PIECE_ID}' not found in pieces.json"


def test_piece_theme():
    piece = get_piece()
    assert piece is not None
    assert "Luchot" in piece["theme"] or "two tablets" in piece["theme"].lower(), (
        f"Theme should mention Luchot/the two tablets, got: {piece['theme']}"
    )


def test_piece_technique_mentions_arnold():
    piece = get_piece()
    assert piece is not None
    assert "Arnold" in piece["technique"] or "arnold" in piece["technique"].lower(), (
        f"Technique should mention Arnold cat map, got: {piece['technique']}"
    )


def test_piece_year():
    piece = get_piece()
    assert piece is not None
    assert piece["year"] == 2026


# ---------------------------------------------------------------------------
# File layout
# ---------------------------------------------------------------------------

def test_index_html_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "index.html"))


def test_essay_md_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "essay.md"))


def test_thumbnail_svg_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "thumbnail.svg"))


def test_readme_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "README.md"))


# ---------------------------------------------------------------------------
# HTML content — Arnold cat map implementation
# ---------------------------------------------------------------------------

def test_html_has_arnold_step_function():
    html = read_html()
    assert "arnoldStep" in html, "index.html must define arnoldStep function"


def test_html_has_period_192():
    html = read_html()
    assert "192" in html, "index.html must reference the period P=192"


def test_html_uses_uint32array():
    html = read_html()
    assert "Uint32Array" in html, "index.html must use Uint32Array for pixel double-buffering"


def test_html_has_fire_tint_color():
    html = read_html()
    assert "#FF3300" in html or "FF3300" in html, (
        "index.html must apply warm-red fire tint #FF3300"
    )


def test_html_has_iteration_counter():
    html = read_html()
    assert "Iteration" in html, "index.html must display an iteration counter"


def test_html_has_hebrew_text():
    html = read_html()
    assert "אָנֹכִי" in html or "אָנֹכִי" in html, (
        "index.html must render the Hebrew text of the first commandment"
    )


def test_html_uses_requestanimationframe():
    html = read_html()
    assert "requestAnimationFrame" in html, (
        "index.html must use requestAnimationFrame for animation"
    )


def test_html_has_double_buffering():
    """Verify two pixel buffers for the cat map double-buffering scheme."""
    html = read_html()
    assert html.count("Uint32Array") >= 2, (
        "index.html must allocate at least two Uint32Array buffers (bufA and bufB)"
    )


def test_html_has_canvas_256():
    """The off-screen canvas must be 256×256."""
    html = read_html()
    assert "256" in html, "index.html must reference the 256×256 grid size"


def test_html_has_step_interval_120ms():
    html = read_html()
    assert "120" in html, "index.html must advance the map every 120ms"


def test_html_has_shattering_phase():
    html = read_html()
    assert "SHATTERING" in html or "shattering" in html.lower(), (
        "index.html must implement the SHATTERING phase"
    )


def test_html_has_restoration_phase():
    html = read_html()
    assert "RESTORATION" in html or "restoration" in html.lower(), (
        "index.html must implement the RESTORATION phase"
    )


def test_html_has_pause_timing():
    """Check that both pause durations (1500ms and 2000ms) are present."""
    html = read_html()
    assert "1500" in html, "index.html must pause 1.5s (1500ms) after shattering phase"
    assert "2000" in html, "index.html must pause 2s (2000ms) after restoration phase"


def test_html_has_parchment_color():
    html = read_html()
    assert "F5E6C8" in html, "index.html must use parchment color #F5E6C8"


def test_html_has_background_color():
    html = read_html()
    assert "0B1220" in html, "index.html must use deep-blue background #0B1220"


# ---------------------------------------------------------------------------
# Essay content
# ---------------------------------------------------------------------------

def test_essay_word_count():
    essay = read_essay()
    words = essay.split()
    assert len(words) >= 300, (
        f"essay.md has only {len(words)} words; expected at least 300"
    )


def test_essay_mentions_exodus():
    essay = read_essay()
    assert "Exodus" in essay or "exodus" in essay.lower(), (
        "essay.md must reference Exodus 32:19"
    )


def test_essay_mentions_talmud():
    essay = read_essay()
    assert "Talmud" in essay or "Shabbat" in essay, (
        "essay.md must reference Talmud Shabbat 87a"
    )


def test_essay_mentions_midrash():
    essay = read_essay()
    assert "Midrash" in essay or "Shemot Rabbah" in essay, (
        "essay.md must reference Midrash Shemot Rabbah 46:1"
    )


def test_essay_mentions_letters_flying():
    """The non-obvious Midrashic insight: letters flew back to heaven."""
    essay = read_essay()
    text_lower = essay.lower()
    assert "flew" in text_lower or "heaven" in text_lower or "flew back" in text_lower, (
        "essay.md must mention the letters flying back to heaven (Shemot Rabbah 46:1)"
    )


def test_essay_mentions_period():
    essay = read_essay()
    assert "192" in essay or "period" in essay.lower(), (
        "essay.md must mention the period P=192 of the Arnold cat map"
    )


def test_essay_embedded_in_html():
    """Essay text must be inlined into index.html (no runtime fetch)."""
    essay = read_essay()
    html = read_html()
    words = [w for w in essay.split() if len(w) > 6]
    sampled = words[:10]
    found = sum(1 for w in sampled if w in html)
    assert found >= 5, (
        f"index.html does not appear to embed the essay text "
        f"(only {found}/10 sampled words found)"
    )


# ---------------------------------------------------------------------------
# Thumbnail
# ---------------------------------------------------------------------------

def test_thumbnail_is_svg():
    svg = read_thumbnail()
    assert "<svg" in svg and "</svg>" in svg, "thumbnail.svg must be valid SVG"


def test_thumbnail_has_dark_background():
    svg = read_thumbnail()
    assert "0B1220" in svg, "thumbnail.svg must use the dark-blue background #0B1220"


def test_thumbnail_has_parchment_tablets():
    svg = read_thumbnail()
    assert "F5E6C8" in svg, "thumbnail.svg must show parchment-colored tablet shapes"


def test_thumbnail_has_amber_border():
    svg = read_thumbnail()
    assert "D4A017" in svg or "amber" in svg.lower() or "#D4" in svg, (
        "thumbnail.svg must have warm amber borders on the tablets"
    )


def test_thumbnail_has_hebrew_text():
    svg = read_thumbnail()
    assert "אָנֹכִי" in svg or "יְהוָה" in svg or "א" in svg, (
        "thumbnail.svg must include Hebrew letterforms on the right tablet"
    )


# ---------------------------------------------------------------------------
# Arnold cat map mathematical properties (Python verification)
# ---------------------------------------------------------------------------

def _arnold_period(N):
    """Compute the period of the Arnold cat map on Z_N by tracking one point."""
    x, y = 1, 0
    for i in range(1, N * N + 1):
        x, y = (x + y) % N, (x + 2 * y) % N
        if x == 1 and y == 0:
            return i
    return None


def _arnold_step_full(buf, N):
    """Apply one Arnold cat map step to a flat integer array of size N*N."""
    out = [0] * (N * N)
    for y in range(N):
        for x in range(N):
            nx = (x + y) % N
            ny = (x + 2 * y) % N
            out[ny * N + nx] = buf[y * N + x]
    return out


def test_arnold_period_256_is_192():
    """The period of the Arnold cat map on Z_256 must be 192."""
    assert _arnold_period(256) == 192, (
        "Arnold cat map period for N=256 should be 192"
    )


def test_arnold_map_is_bijection_small():
    """Every destination cell is filled exactly once — the map is a bijection."""
    N = 8
    buf = list(range(N * N))
    out = _arnold_step_full(buf, N)
    assert sorted(out) == sorted(buf), (
        "Arnold cat map must be a bijection: every value appears exactly once in output"
    )


def test_arnold_map_period_restores_original_small():
    """After P iterations the original buffer is exactly restored (small grid)."""
    N = 12
    period = _arnold_period(N)
    assert period is not None, f"Could not find period for N={N}"
    buf = list(range(N * N))
    current = list(buf)
    for _ in range(period):
        current = _arnold_step_full(current, N)
    assert current == buf, (
        f"After {period} iterations the buffer must equal the original for N={N}"
    )


def test_arnold_map_single_step_changes_image():
    """One iteration of the map must change the image (non-trivial for N≥2)."""
    N = 4
    buf = list(range(N * N))
    out = _arnold_step_full(buf, N)
    assert out != buf, "One Arnold step should produce a different arrangement"


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

def test_piece_path_ends_with_html():
    piece = get_piece()
    assert piece is not None
    assert piece["path"].endswith(".html"), "piece path must end with .html"


def test_piece_has_all_required_fields():
    required = ("id", "title", "tagline", "year", "theme", "technique", "path", "thumbnail", "essay")
    piece = get_piece()
    assert piece is not None
    for field in required:
        assert field in piece and piece[field], (
            f"Piece '{PIECE_ID}' missing or empty field '{field}'"
        )


def test_no_duplicate_piece_id():
    pieces = load_pieces()
    ids = [p["id"] for p in pieces]
    assert ids.count(PIECE_ID) == 1, f"Duplicate entry for '{PIECE_ID}' in pieces.json"


def test_essay_path_matches_json():
    """The essay field in pieces.json must point to the actual essay.md."""
    piece = get_piece()
    assert piece is not None
    expected = f"pieces/{PIECE_ID}/essay.md"
    assert piece["essay"] == expected, (
        f"essay field should be '{expected}', got '{piece['essay']}'"
    )


def test_arnold_period_different_N():
    """Verify period computation for a different N as a sanity check."""
    period = _arnold_period(12)
    assert period is not None and period > 0, (
        "Period for N=12 should be a positive integer"
    )
    assert period <= 12 * 12, "Period must be at most N^2"
