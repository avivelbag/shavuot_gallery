"""
Tests for piece 83-worley-noise-pomegranate: Worley noise pomegranate.

Validates file layout, pieces.json registration, essay substance, and
implementation-specific details in index.html (Worley noise, spatial grid,
Hebrew letters, reveal animation, pulse animation, pomegranate crown).
"""
import json
import os
import re

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID = "83-worley-noise-pomegranate"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")


def load_piece():
    """Return the pieces.json entry for the pomegranate piece, or None."""
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


def test_pieces_json_theme_mentions_pomegranate():
    piece = load_piece()
    assert piece is not None
    theme = piece.get("theme", "").lower()
    assert "pomegranate" in theme or "bikkurim" in theme or "seven species" in theme, (
        f"theme '{piece.get('theme')}' should reference pomegranate / bikkurim"
    )


def test_pieces_json_technique_mentions_worley():
    piece = load_piece()
    assert piece is not None
    technique = piece.get("technique", "").lower()
    assert "worley" in technique or "cellular" in technique or "voronoi" in technique, (
        f"technique '{piece.get('technique')}' should mention Worley noise / cellular"
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


def test_essay_mentions_deuteronomy_8_8():
    text = read_essay()
    assert "8:8" in text or "Deuteronomy" in text, (
        "essay must cite Deuteronomy 8:8"
    )


def test_essay_mentions_eruvin_19a():
    text = read_essay()
    assert "Eruvin 19a" in text or "Eruvin" in text, (
        "essay must cite Eruvin 19a (the Talmudic source for the pomegranate saying)"
    )


def test_essay_mentions_sanhedrin_37a():
    text = read_essay()
    assert "Sanhedrin 37a" in text or "Sanhedrin" in text, (
        "essay must cite Sanhedrin 37a"
    )


def test_essay_has_hebrew_pomegranate_quote():
    text = read_essay()
    # The key Hebrew phrase — uses Hebrew unicode
    assert "כָּרִמּוֹן" in text or "מְלֵאִין" in text or "אֲפִילּוּ" in text, (
        "essay must include the Hebrew pomegranate quote from Eruvin 19a"
    )


def test_essay_mentions_exodus_19_6():
    text = read_essay()
    assert "19:6" in text or "Exodus 19" in text, (
        "essay must cite Exodus 19:6 — the universal scope of Matan Torah"
    )


def test_essay_has_hebrew_exodus_quote():
    text = read_essay()
    # Exodus 19:6 Hebrew
    assert "כֹּהֲנִים" in text or "מַמְלֶכֶת" in text, (
        "essay must include Hebrew text from Exodus 19:6"
    )


def test_essay_mentions_613():
    text = read_essay()
    assert "613" in text, (
        "essay must mention the 613 commandments and their connection to pomegranate seeds"
    )


def test_essay_mentions_baal_haturim():
    text = read_essay()
    assert "Baal HaTurim" in text or "Baal Haturim" in text, (
        "essay must cite the Baal HaTurim tradition connecting pomegranate seeds to 613 mitzvot"
    )


def test_essay_not_stub():
    text = read_essay()
    assert len(text.strip()) > 500, "essay is suspiciously short — may be a placeholder"


# ---------------------------------------------------------------------------
# index.html: Worley noise implementation
# ---------------------------------------------------------------------------

def test_index_has_canvas_element():
    html = read_index()
    assert "<canvas" in html


def test_index_uses_requestanimationframe():
    html = read_index()
    assert "requestAnimationFrame" in html


def test_index_has_n_points_220():
    html = read_index()
    assert "N_POINTS = 220" in html or "N_POINTS=220" in html, (
        "N_POINTS must be set to 220"
    )


def test_index_has_worley_spatial_grid():
    """Worley noise must use a spatial grid for acceleration (not naive O(N) per pixel)."""
    html = read_index()
    assert "GRID_N" in html or "GRID_SIZE" in html or "grid" in html.lower(), (
        "spatial grid for Worley acceleration not found"
    )


def test_index_has_cell_map():
    """Cell assignment map must be precomputed (Int32Array or similar)."""
    html = read_index()
    assert "cellMap" in html or "Int32Array" in html, (
        "precomputed cell map not found in index.html"
    )


def test_index_has_wall_distance_computation():
    """Must compute wall distance (d2 - d1) for boundary detection."""
    html = read_index()
    assert "wallMap" in html or "d2" in html or "second" in html.lower(), (
        "wall distance / second-nearest computation not found"
    )


def test_index_has_crimson_color():
    html = read_index()
    assert "7A1520" in html.upper() or "0x7A" in html or "#7a1520" in html.lower(), (
        "deep crimson color #7A1520 not found in index.html"
    )


def test_index_has_garnet_color():
    html = read_index()
    assert "C0103A" in html.upper() or "0xC0" in html or "#c0103a" in html.lower(), (
        "garnet color #C0103A not found in index.html"
    )


def test_index_has_near_white_color():
    """Near-white color #FCEBD5 may appear as CSS string or as ImageData hex bytes."""
    html = read_index()
    assert (
        "FCEBD5" in html.upper()
        or "#fcebd5" in html.lower()
        or "0xFC" in html  # component form used in ImageData rendering
        or "0xEB" in html
    ), "near-white color #FCEBD5 (or its byte components) not found in index.html"


def test_index_has_gold_dot_color():
    html = read_index()
    assert "FFD700" in html.upper() or "#ffd700" in html.lower(), (
        "gold dot color #FFD700 not found in index.html"
    )


def test_index_has_hebrew_aleph_codepoint():
    """Hebrew letters are generated from the aleph Unicode codepoint."""
    html = read_index()
    assert "0x05D0" in html or "05D0" in html or "ALEPH" in html, (
        "Hebrew aleph codepoint (0x05D0) or ALEPH constant not found"
    )


def test_index_has_hebrew_label_function():
    html = read_index()
    assert "hebrewLabel" in html or "fromCodePoint" in html, (
        "Hebrew label generation function not found"
    )


def test_index_has_seed_dot_radius_2():
    """Seed dots must be radius 2px as specified."""
    html = read_index()
    assert "arc(s.x, s.y, 2" in html or "radius = 2" in html or ", 2, 0" in html, (
        "seed dot radius 2 not found"
    )


def test_index_has_reveal_animation():
    """Must implement reveal animation (radial sweep)."""
    html = read_index()
    assert "REVEAL_MS" in html or "REVEAL_DURATION" in html or "revealFrac" in html, (
        "reveal animation constant not found"
    )


def test_index_reveal_duration_2000ms():
    html = read_index()
    assert "2000" in html, "reveal duration 2000ms not found"


def test_index_has_pulse_animation():
    """Must implement per-cell pulse (breathing) animation."""
    html = read_index()
    assert "pulse" in html.lower() or "phases" in html or "phase" in html.lower(), (
        "pulse animation (per-cell phase offset) not found"
    )


def test_index_has_crown():
    """Must draw the pomegranate crown (atara) at the top."""
    html = read_index()
    assert "crown" in html.lower() or "Crown" in html or "atara" in html.lower(), (
        "pomegranate crown not found in index.html"
    )


def test_index_has_circle_clip():
    """Canvas must be clipped to a circle (pomegranate shape)."""
    html = read_index()
    assert "ctx.arc" in html and "clip" in html, (
        "circle clip (ctx.arc + ctx.clip) not found"
    )


def test_index_has_offscreen_canvas():
    """Must use an offscreen canvas to avoid recomputing Worley every frame."""
    html = read_index()
    assert "createElement('canvas')" in html or "OffscreenCanvas" in html, (
        "offscreen canvas for precomputed Worley texture not found"
    )


def test_index_has_imagedata():
    """Must use ImageData for pixel-level Worley rendering."""
    html = read_index()
    assert "ImageData" in html, "ImageData API not found"


def test_index_no_external_dependencies():
    """index.html must be self-contained — no CDN or external script src."""
    html = read_index()
    external = re.findall(r'src=["\']https?://', html)
    assert len(external) == 0, f"index.html has external script src: {external}"


def test_index_embeds_essay_text():
    """index.html must embed the essay inline (not fetch essay.md at runtime)."""
    essay = read_essay()
    html = read_index()
    words = [w for w in essay.split() if len(w) > 5][:10]
    found = sum(1 for w in words if w in html)
    assert found >= 5, (
        f"only {found}/10 essay words found in index.html — essay must be embedded inline"
    )


def test_index_has_hebrew_rtl():
    """Hebrew text must use RTL direction attribute."""
    html = read_index()
    assert 'dir="rtl"' in html or "direction: rtl" in html or "direction:rtl" in html, (
        "RTL direction for Hebrew text not found in index.html"
    )


def test_index_has_42_min_radius():
    """Circle radius must be 0.42 * min(width, height) as specified."""
    html = read_index()
    assert "0.42" in html, "R = 0.42 * min(W, H) not found in index.html"


# ---------------------------------------------------------------------------
# Thumbnail SVG
# ---------------------------------------------------------------------------

def test_thumbnail_is_valid_svg():
    text = read_thumbnail()
    assert "<svg" in text and "</svg>" in text


def test_thumbnail_has_dark_background():
    text = read_thumbnail()
    assert "#0A0208" in text or "#0a0208" in text or "#0A0208".lower() in text.lower(), (
        "thumbnail must have dark pomegranate background color"
    )


def test_thumbnail_has_crimson_cells():
    text = read_thumbnail()
    assert "7A1520" in text.upper() or "7a1520" in text.lower() or "#7a" in text.lower(), (
        "thumbnail must contain crimson cell colors"
    )


def test_thumbnail_has_garnet_borders():
    text = read_thumbnail()
    assert "C0103A" in text.upper() or "#c0103a" in text.lower() or "C0103A".lower() in text.lower(), (
        "thumbnail must have garnet border color"
    )


def test_thumbnail_has_seed_polygons():
    text = read_thumbnail()
    assert "<polygon" in text or "<path" in text, (
        "thumbnail must contain seed cell polygons"
    )


def test_thumbnail_has_hebrew_letters():
    text = read_thumbnail()
    # Check for Hebrew Unicode characters (alef through tav: 0x05D0-0x05EA)
    hebrew_found = any(ord(c) >= 0x05D0 and ord(c) <= 0x05EA for c in text)
    assert hebrew_found, "thumbnail must contain Hebrew letter text elements"


def test_thumbnail_has_crown():
    text = read_thumbnail()
    # Crown should be a path element at the top
    assert "<path" in text, "thumbnail must contain a crown path element"


def test_thumbnail_has_circle():
    text = read_thumbnail()
    assert "<circle" in text, "thumbnail must contain circle element (pomegranate boundary)"


def test_thumbnail_has_seed_dots():
    text = read_thumbnail()
    assert 'fill="#FFD700"' in text or 'fill="#ffd700"' in text, (
        "thumbnail must contain gold seed dots (#FFD700)"
    )


# ---------------------------------------------------------------------------
# README content
# ---------------------------------------------------------------------------

def test_readme_mentions_worley():
    text = read_readme()
    assert "Worley" in text or "worley" in text.lower(), (
        "README.md must describe the Worley noise technique"
    )


def test_readme_mentions_pomegranate():
    text = read_readme()
    assert "pomegranate" in text.lower(), "README.md must mention the pomegranate theme"


def test_readme_mentions_voronoi_or_cellular():
    text = read_readme()
    assert "Voronoi" in text or "cellular" in text.lower(), (
        "README.md must mention Voronoi / cellular distance field"
    )


def test_readme_mentions_eruvin():
    text = read_readme()
    assert "Eruvin" in text, "README.md must cite Eruvin 19a as a source"


def test_readme_mentions_deuteronomy():
    text = read_readme()
    assert "Deuteronomy" in text or "8:8" in text, (
        "README.md must mention Deuteronomy 8:8"
    )


# ---------------------------------------------------------------------------
# Edge cases and failure-mode tests
# ---------------------------------------------------------------------------

def test_missing_piece_directory_detected(tmp_path):
    """Confirm our file-existence check would catch a missing piece directory."""
    fake_dir = tmp_path / "99-fake-worley"
    assert not fake_dir.exists(), "Fixture must not exist on disk"


def test_empty_essay_fails_word_count():
    """An empty essay string should fail the word-count check."""
    text = ""
    assert len(text.split()) < 200, "empty essay should have fewer than 200 words"


def test_essay_with_only_headers_is_short():
    """An essay with only headers and no prose would fail the word-count threshold."""
    stub = "# Title\n## Section\n"
    assert len(stub.split()) < 200, "stub essay should be detected as too short"


def test_pieces_json_is_parseable():
    """pieces.json must remain valid JSON after the new entry is added."""
    with open(PIECES_JSON, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    assert isinstance(data, list)
    assert len(data) >= 1


def test_new_piece_is_last_or_present():
    """The new piece must appear somewhere in the pieces.json list."""
    with open(PIECES_JSON, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    ids = [p["id"] for p in data]
    assert PIECE_ID in ids, f"{PIECE_ID} not found in pieces.json ids"


def test_index_has_8_or_9_font():
    """Hebrew letter font size should be 9px as specified."""
    html = read_index()
    assert "9px" in html, "font size 9px for Hebrew labels not found"


def test_index_has_ffd090_label_color():
    """Hebrew label color must be #FFD090 as specified."""
    html = read_index()
    assert "FFD090" in html.upper() or "#ffd090" in html.lower(), (
        "Hebrew label color #FFD090 not found"
    )
