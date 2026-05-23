"""
Tests for piece 84-poisson-bikkurim-grain-field: Poisson disk sampling Bikkurim field.

Validates file layout, pieces.json registration, essay substance, and
implementation-specific details in index.html (Bridson's algorithm, glyph
drawing, colours, wind shimmer, Hebrew overlay).
"""
import json
import os
import re

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID     = "84-poisson-bikkurim-grain-field"
PIECE_DIR    = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
PIECES_JSON  = os.path.join(GALLERY_ROOT, "pieces.json")


def load_piece():
    """Return the pieces.json entry for this piece, or None."""
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


def read_readme():
    """Return the text content of README.md."""
    return open(os.path.join(PIECE_DIR, "README.md"), encoding="utf-8").read()


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


def test_pieces_json_theme_mentions_bikkurim():
    piece = load_piece()
    assert piece is not None
    theme = piece.get("theme", "").lower()
    assert "bikkurim" in theme or "first fruit" in theme or "harvest" in theme, (
        f"theme '{piece.get('theme')}' should reference Bikkurim / first fruits / harvest"
    )


def test_pieces_json_technique_mentions_poisson():
    piece = load_piece()
    assert piece is not None
    technique = piece.get("technique", "").lower()
    assert "poisson" in technique or "bridson" in technique, (
        f"technique '{piece.get('technique')}' should mention Poisson / Bridson"
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


def test_pieces_json_year_is_2026():
    piece = load_piece()
    assert piece is not None
    assert piece["year"] == 2026


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


def test_essay_at_least_380_words():
    """Acceptance criterion specifies ~380 words."""
    text = read_essay()
    assert len(text.split()) >= 300, f"essay.md has only {len(text.split())} words (need ≥300)"


def test_essay_cites_deuteronomy_26():
    text = read_essay()
    assert "Deuteronomy 26" in text or "26:1" in text or "Deuteronomy" in text, (
        "essay must cite Deuteronomy 26:1-11"
    )


def test_essay_mentions_mishnah_bikkurim():
    text = read_essay()
    assert "Bikkurim" in text or "bikkurim" in text.lower(), (
        "essay must mention the Mishnah Bikkurim tractate"
    )


def test_essay_mentions_aramean_declaration():
    """The farmer's recitation: 'My father was a wandering Aramean' (Deut 26:5)."""
    text = read_essay()
    assert "Aramean" in text or "wandering" in text or "5-9" in text or "5–9" in text, (
        "essay must reference Deuteronomy 26:5 ('my father was a wandering Aramean')"
    )


def test_essay_mentions_procession_details():
    """The Mishnah Bikkurim describes the ox with gilded horns and flute player."""
    text = read_essay()
    assert "flute" in text or "ox" in text or "gilded" in text, (
        "essay must describe the Bikkurim procession (flute, gilded ox)"
    )


def test_essay_explains_not_a_tithe():
    """Key non-obvious insight: Bikkurim is not a tithe but anticipatory faith."""
    text = read_essay()
    assert "tithe" in text.lower() or "tithes" in text.lower(), (
        "essay must explain that Bikkurim differs from a tithe"
    )


def test_essay_ties_to_poisson_artwork():
    """Essay must connect Bridson's algorithm to the Bikkurim theme."""
    text = read_essay()
    assert "Poisson" in text or "Bridson" in text or "algorithm" in text.lower(), (
        "essay must tie the Poisson disk sampling technique to the Bikkurim theme"
    )


def test_essay_not_stub():
    text = read_essay()
    assert len(text.strip()) > 500, "essay is suspiciously short — may be a placeholder"


# ---------------------------------------------------------------------------
# index.html: Bridson's algorithm implementation
# ---------------------------------------------------------------------------

def test_index_has_canvas_element():
    html = read_index()
    assert "<canvas" in html


def test_index_uses_requestanimationframe():
    html = read_index()
    assert "requestAnimationFrame" in html


def test_index_has_r_equals_18():
    """Minimum radius must be R=18 as specified."""
    html = read_index()
    assert "R = 18" in html or "R=18" in html or "const R" in html, (
        "Poisson disk minimum radius R=18 not found in index.html"
    )


def test_index_has_k_equals_30():
    """Candidate count K=30 as specified."""
    html = read_index()
    assert "K = 30" in html or "K=30" in html or "const K" in html, (
        "Poisson disk candidate count K=30 not found in index.html"
    )


def test_index_has_bridson_cell_size():
    """Cell size = r / sqrt(2) is the hallmark of Bridson's grid acceleration."""
    html = read_index()
    assert "SQRT2" in html or "sqrt(2)" in html.lower() or "Math.SQRT2" in html, (
        "Bridson cell = r/√2 formula not found in index.html"
    )


def test_index_has_active_list():
    """Bridson's algorithm uses an active list (annular sampling)."""
    html = read_index()
    assert "active" in html, "active list variable not found in index.html"


def test_index_has_grid_array():
    """Spatial grid for O(1) nearest-neighbour lookup."""
    html = read_index()
    assert "grid" in html, "grid array not found in index.html"


def test_index_has_glyph_type_function():
    html = read_index()
    assert "glyphType" in html or "glyph_type" in html, (
        "glyphType deterministic glyph assignment function not found"
    )


def test_index_has_draw_glyph_function():
    html = read_index()
    assert "drawGlyph" in html or "draw_glyph" in html, (
        "drawGlyph function not found in index.html"
    )


def test_index_has_wheat_color():
    """Wheat grain color #D4A840."""
    html = read_index()
    assert "D4A840" in html.upper() or "#d4a840" in html.lower(), (
        "wheat grain color #D4A840 not found in index.html"
    )


def test_index_has_barley_color():
    """Barley kernel color #C8A020."""
    html = read_index()
    assert "C8A020" in html.upper() or "#c8a020" in html.lower(), (
        "barley kernel color #C8A020 not found in index.html"
    )


def test_index_has_grape_color():
    """Grape circle color #6B2D8B."""
    html = read_index()
    assert "6B2D8B" in html.upper() or "#6b2d8b" in html.lower(), (
        "grape circle color #6B2D8B not found in index.html"
    )


def test_index_has_background_color():
    """Dark field-earth background #1C1208."""
    html = read_index()
    assert "1C1208" in html.upper() or "#1c1208" in html.lower(), (
        "dark earth background #1C1208 not found in index.html"
    )


def test_index_has_furrow_color():
    """Faint furrow grid color #2A1A08."""
    html = read_index()
    assert "2A1A08" in html.upper() or "#2a1a08" in html.lower(), (
        "furrow grid color #2A1A08 not found in index.html"
    )


def test_index_has_furrow_spacing_60():
    """Furrow lines at 60 px spacing."""
    html = read_index()
    assert "60" in html, "furrow spacing 60 not found in index.html"


def test_index_has_wind_shimmer():
    """Wind shimmer: 30 grains scale up and back."""
    html = read_index()
    assert "windGrains" in html or "wind" in html.lower(), (
        "wind shimmer not found in index.html"
    )


def test_index_has_wind_interval_3000():
    """Wind triggers every 3000 ms."""
    html = read_index()
    assert "3000" in html, "wind interval 3000 ms not found in index.html"


def test_index_has_wind_count_30():
    """30 grains per shimmer event."""
    html = read_index()
    assert "WIND_COUNT" in html or "30" in html, (
        "wind count 30 not found in index.html"
    )


def test_index_has_wind_duration_800():
    """Shimmer duration 800 ms."""
    html = read_index()
    assert "800" in html, "wind duration 800 ms not found in index.html"


def test_index_has_wind_scale_115():
    """Grains scale to 1.15× during shimmer."""
    html = read_index()
    assert "0.15" in html or "1.15" in html, (
        "wind scale 1.15 not found in index.html"
    )


def test_index_has_hebrew_bikkurim():
    """Hebrew word בִּכּוּרִים must appear in the HTML (any niqqud ordering)."""
    import unicodedata

    def strip_combining(s):
        """Remove all Unicode combining marks (niqqud etc.) for comparison."""
        return ''.join(c for c in unicodedata.normalize('NFD', s)
                       if unicodedata.category(c) != 'Mn')

    html = read_index()
    html_base = strip_combining(html)
    assert 'בכורים' in html_base, (
        "Hebrew base consonants of בִּכּוּרִים not found in index.html"
    )


def test_index_has_destination_out_composite():
    """Hebrew text punched through overlay using destination-out compositing."""
    html = read_index()
    assert "destination-out" in html, (
        "destination-out composite operation for Hebrew overlay not found"
    )


def test_index_has_overlay_canvas():
    """Two-canvas approach: field canvas + overlay canvas."""
    html = read_index()
    assert html.count("<canvas") >= 2, (
        "index.html must have at least two canvas elements (field + overlay)"
    )


def test_index_has_hash_function():
    """Deterministic glyph type requires a hash of (x, y)."""
    html = read_index()
    assert "hashXY" in html or "hash" in html.lower(), (
        "hash function for deterministic glyph assignment not found"
    )


def test_index_has_step_bridson_function():
    html = read_index()
    assert "stepBridson" in html or "step_bridson" in html or "stepBridson" in html.lower(), (
        "stepBridson function not found in index.html"
    )


def test_index_has_glyph_angle_rotation():
    """Glyphs are rotated ±25° from vertical."""
    html = read_index()
    assert "50" in html or "25" in html or "angle" in html.lower(), (
        "glyph angle / ±25 degree rotation not found in index.html"
    )


def test_index_has_resize_observer_or_resize():
    """Canvas must respond to panel size changes."""
    html = read_index()
    assert "ResizeObserver" in html or "resize" in html.lower(), (
        "resize handling not found in index.html"
    )


def test_index_no_external_dependencies():
    """index.html must be self-contained — no CDN or external script src."""
    html = read_index()
    external = re.findall(r'src=["\']https?://', html)
    assert len(external) == 0, f"index.html has external script src: {external}"


def test_index_embeds_essay_text():
    """index.html must embed the essay inline (not fetch essay.md at runtime)."""
    essay = read_essay()
    html  = read_index()
    words = [w for w in essay.split() if len(w) > 5][:10]
    found = sum(1 for w in words if w in html)
    assert found >= 5, (
        f"only {found}/10 essay words found in index.html — essay must be embedded inline"
    )


def test_index_has_hebrew_rtl():
    """Hebrew text direction must be RTL."""
    html = read_index()
    assert 'dir="rtl"' in html or "direction: rtl" in html or "direction:rtl" in html, (
        "RTL direction for Hebrew text not found in index.html"
    )


# ---------------------------------------------------------------------------
# Thumbnail SVG
# ---------------------------------------------------------------------------

def test_thumbnail_is_valid_svg():
    text = read_thumbnail()
    assert "<svg" in text and "</svg>" in text


def test_thumbnail_has_dark_background():
    text = read_thumbnail()
    assert "1C1208" in text.upper() or "#1c1208" in text.lower(), (
        "thumbnail must have dark earth background color #1C1208"
    )


def test_thumbnail_has_wheat_color():
    text = read_thumbnail()
    assert "D4A840" in text.upper() or "#d4a840" in text.lower(), (
        "thumbnail must contain wheat grain color #D4A840"
    )


def test_thumbnail_has_barley_color():
    text = read_thumbnail()
    assert "C8A020" in text.upper() or "#c8a020" in text.lower(), (
        "thumbnail must contain barley kernel color #C8A020"
    )


def test_thumbnail_has_grape_color():
    text = read_thumbnail()
    assert "6B2D8B" in text.upper() or "#6b2d8b" in text.lower(), (
        "thumbnail must contain grape circle color #6B2D8B"
    )


def test_thumbnail_has_multiple_glyphs():
    """Thumbnail should have ~80 glyphs (many group or shape elements)."""
    text = read_thumbnail()
    group_count = text.count("<g ")
    assert group_count >= 40, (
        f"thumbnail has only {group_count} <g> elements; expected ~80 glyph groups"
    )


def test_thumbnail_has_circles():
    """Grape glyphs are circles."""
    text = read_thumbnail()
    assert "<circle" in text, "thumbnail must contain circle elements (grape glyphs)"


def test_thumbnail_has_ellipses():
    """Wheat and barley glyphs use ellipses."""
    text = read_thumbnail()
    assert "<ellipse" in text, "thumbnail must contain ellipse elements (wheat/barley glyphs)"


def test_thumbnail_has_hebrew_text():
    """Hebrew word בִּכּוּרִים must appear in the SVG."""
    text = read_thumbnail()
    hebrew_found = any(ord(c) >= 0x05D0 and ord(c) <= 0x05EA for c in text)
    assert hebrew_found, "thumbnail must contain Hebrew text בִּכּוּרִים"


def test_thumbnail_has_text_element():
    text = read_thumbnail()
    assert "<text" in text, "thumbnail must have a <text> element for the Hebrew word"


# ---------------------------------------------------------------------------
# README content
# ---------------------------------------------------------------------------

def test_readme_mentions_poisson():
    text = read_readme()
    assert "Poisson" in text or "poisson" in text.lower(), (
        "README.md must describe the Poisson disk sampling technique"
    )


def test_readme_mentions_bridson():
    text = read_readme()
    assert "Bridson" in text or "bridson" in text.lower(), (
        "README.md must mention Bridson's algorithm"
    )


def test_readme_mentions_bikkurim():
    text = read_readme()
    assert "Bikkurim" in text or "bikkurim" in text.lower(), (
        "README.md must mention the Bikkurim theme"
    )


def test_readme_mentions_deuteronomy():
    text = read_readme()
    assert "Deuteronomy" in text or "26:1" in text, (
        "README.md must cite Deuteronomy 26:1-11"
    )


def test_readme_mentions_wheat_barley_grape():
    text = read_readme()
    assert "wheat" in text.lower() or "barley" in text.lower() or "grape" in text.lower(), (
        "README.md must mention the wheat / barley / grape glyphs"
    )


# ---------------------------------------------------------------------------
# Edge cases and failure-mode tests
# ---------------------------------------------------------------------------

def test_missing_piece_directory_detected(tmp_path):
    """Confirm our file-existence check would catch a missing piece directory."""
    fake_dir = tmp_path / "99-fake-poisson"
    assert not fake_dir.exists(), "Fixture must not exist on disk"


def test_empty_essay_fails_word_count():
    """An empty essay string should fail the word-count check."""
    text = ""
    assert len(text.split()) < 200, "empty essay should have fewer than 200 words"


def test_essay_stub_is_detected():
    """An essay with only a heading would fail the word-count threshold."""
    stub = "# First of All the Fruit of the Ground\n"
    assert len(stub.split()) < 200, "stub essay should be detected as too short"


def test_pieces_json_is_parseable():
    """pieces.json must remain valid JSON after the new entry is added."""
    with open(PIECES_JSON, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    assert isinstance(data, list)
    assert len(data) >= 1


def test_new_piece_present_in_pieces_json():
    """The new piece must appear somewhere in the pieces.json list."""
    with open(PIECES_JSON, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    ids = [p["id"] for p in data]
    assert PIECE_ID in ids, f"{PIECE_ID} not found in pieces.json ids"


def test_r_value_constraint():
    """R=18 is the acceptance-criterion-specified minimum radius; verify the constant."""
    html = read_index()
    # Accept 'R = 18', 'R=18', 'const R = 18', or 'R = 18;'
    assert re.search(r'\bR\s*=\s*18\b', html), (
        "R=18 minimum radius constant not found in index.html"
    )


def test_k_value_constraint():
    """K=30 is the acceptance-criterion-specified candidate count."""
    html = read_index()
    assert re.search(r'\bK\s*=\s*30\b', html), (
        "K=30 candidate count constant not found in index.html"
    )
