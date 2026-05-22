"""
Tests for piece 67-particle-life-bikkurim-procession: particle life Bikkurim animation.

Validates piece registration, file existence, essay content, and specific technical
requirements of the particle life simulation (species counts, force matrix, canvas,
Hebrew caption, motion parameters).
"""
import json
import os
import re

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")
PIECE_ID = "67-particle-life-bikkurim-procession"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
INDEX_HTML = os.path.join(PIECE_DIR, "index.html")
ESSAY_MD = os.path.join(PIECE_DIR, "essay.md")
THUMBNAIL = os.path.join(PIECE_DIR, "thumbnail.svg")
README = os.path.join(PIECE_DIR, "README.md")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_pieces():
    """Return parsed pieces.json list."""
    with open(PIECES_JSON, encoding="utf-8") as fh:
        return json.load(fh)


def get_piece():
    """Return the pieces.json entry for this piece, or None."""
    return next((p for p in load_pieces() if p["id"] == PIECE_ID), None)


def read_html():
    """Return index.html contents as a string."""
    with open(INDEX_HTML, encoding="utf-8") as fh:
        return fh.read()


def read_essay():
    """Return essay.md contents as a string."""
    with open(ESSAY_MD, encoding="utf-8") as fh:
        return fh.read()


# ---------------------------------------------------------------------------
# Registration in pieces.json
# ---------------------------------------------------------------------------

def test_piece_registered_in_pieces_json():
    """Piece must appear in pieces.json with correct id."""
    assert get_piece() is not None, f"'{PIECE_ID}' not found in pieces.json"


def test_piece_required_fields():
    """All nine required fields must be non-empty in pieces.json entry."""
    required = ("id", "title", "tagline", "year", "theme", "technique", "path", "thumbnail", "essay")
    piece = get_piece()
    assert piece is not None
    for field in required:
        val = piece.get(field)
        assert val is not None and val != "", f"Field '{field}' is empty in pieces.json entry"


def test_piece_theme_is_bikkurim():
    """Theme must be 'Bikkurim' per acceptance criteria."""
    piece = get_piece()
    assert piece is not None
    assert "Bikkurim" in piece["theme"], f"Expected 'Bikkurim' in theme, got: {piece['theme']!r}"


def test_piece_technique_mentions_particle_life():
    """Technique must mention 'particle life' per acceptance criteria."""
    piece = get_piece()
    assert piece is not None
    assert "particle life" in piece["technique"].lower(), (
        f"Expected 'particle life' in technique, got: {piece['technique']!r}"
    )


def test_piece_technique_mentions_attraction_repulsion():
    """Technique must mention attraction-repulsion."""
    piece = get_piece()
    assert piece is not None
    tech = piece["technique"].lower()
    assert "attraction" in tech or "repulsion" in tech, (
        f"Expected 'attraction' or 'repulsion' in technique, got: {piece['technique']!r}"
    )


# ---------------------------------------------------------------------------
# File existence
# ---------------------------------------------------------------------------

def test_index_html_exists():
    """index.html must exist."""
    assert os.path.isfile(INDEX_HTML), f"index.html missing at {INDEX_HTML}"


def test_essay_md_exists():
    """essay.md must exist."""
    assert os.path.isfile(ESSAY_MD), f"essay.md missing at {ESSAY_MD}"


def test_thumbnail_exists():
    """thumbnail.svg must exist."""
    assert os.path.isfile(THUMBNAIL), f"thumbnail.svg missing at {THUMBNAIL}"


def test_readme_exists():
    """README.md must exist."""
    assert os.path.isfile(README), f"README.md missing at {README}"


# ---------------------------------------------------------------------------
# Essay content
# ---------------------------------------------------------------------------

def test_essay_minimum_word_count():
    """Essay must be at least 400 words per acceptance criteria."""
    text = read_essay()
    word_count = len(text.split())
    assert word_count >= 400, f"Essay has only {word_count} words (need ≥ 400)"


def test_essay_cites_mishnah_bikkurim():
    """Essay must cite Mishnah Bikkurim."""
    text = read_essay()
    assert "Bikkurim" in text, "Essay must cite Mishnah Bikkurim"


def test_essay_cites_deuteronomy_26():
    """Essay must cite Deuteronomy 26:5–10 (Arami oved avi)."""
    text = read_essay()
    assert "26:" in text or "Deuteronomy 26" in text, "Essay must cite Deuteronomy 26"


def test_essay_mentions_arami_oved_avi():
    """Essay must reference the Arami oved avi declaration."""
    text = read_essay()
    assert "Arami" in text or "אֲרַמִּי" in text, (
        "Essay must mention the Arami oved avi declaration"
    )


def test_essay_contains_hebrew_deuteronomy():
    """Essay must contain Hebrew text of Deuteronomy 26."""
    text = read_essay()
    assert "אֲרַמִּי" in text or "אֹבֵד" in text, (
        "Essay must include Hebrew text of Deuteronomy 26:5"
    )


def test_essay_contains_hebrew_mishnah():
    """Essay must contain Hebrew text from Mishnah Bikkurim."""
    text = read_essay()
    assert "וְהֶחָלִיל" in text or "הַבִּכּוּרִים" in text, (
        "Essay must include Hebrew text from Mishnah Bikkurim"
    )


def test_essay_mentions_haggadah_connection():
    """Essay must make the connection to the Haggadah/Seder."""
    text = read_essay()
    assert "Haggadah" in text or "Seder" in text, (
        "Essay must connect Bikkurim declaration to the Passover Haggadah/Seder"
    )


def test_essay_mentions_sifrei_devarim():
    """Essay must cite Sifrei Devarim as the source for the Haggadah connection."""
    text = read_essay()
    assert "Sifrei" in text or "Pesachim" in text, (
        "Essay must cite Sifrei Devarim or Pesachim 116a for the Haggadah connection"
    )


def test_essay_three_names_of_shavuot():
    """Essay must mention the three names of Shavuot."""
    text = read_essay()
    assert "Bikkurim" in text and ("Katzir" in text or "Shavuot" in text), (
        "Essay must discuss Shavuot's multiple names including Yom HaBikkurim"
    )


def test_essay_has_substantial_hebrew():
    """Essay must contain at least 30 Hebrew characters."""
    text = read_essay()
    hebrew_chars = [c for c in text if 'א' <= c <= 'ת']
    assert len(hebrew_chars) >= 30, (
        f"Essay must contain substantial Hebrew text; found only {len(hebrew_chars)} Hebrew chars"
    )


# ---------------------------------------------------------------------------
# index.html: canvas and animation requirements
# ---------------------------------------------------------------------------

def test_html_embeds_essay_text():
    """index.html must embed essay text inline (sampled keyword check)."""
    essay = read_essay()
    html = read_html()
    words = [w for w in essay.split() if len(w) > 6][:15]
    found = sum(1 for w in words if w in html)
    assert found >= 8, (
        f"index.html does not appear to embed the essay text "
        f"(only {found}/15 sampled words found)"
    )


def test_html_canvas_700x700():
    """Canvas must be 700×700 per acceptance criteria."""
    html = read_html()
    assert re.search(r'canvas\.width\s*=\s*700', html) or 'width: 700' in html or 'width="700"' in html, (
        "index.html must set canvas width to 700"
    )
    assert re.search(r'canvas\.height\s*=\s*700', html) or 'height: 700' in html or 'height="700"' in html, (
        "index.html must set canvas height to 700"
    )


def test_html_uses_request_animation_frame():
    """index.html must use requestAnimationFrame for the animation loop."""
    html = read_html()
    assert "requestAnimationFrame" in html, (
        "index.html must use requestAnimationFrame"
    )


def test_html_pilgrim_color():
    """Pilgrims must use warm gold #C8A020."""
    html = read_html()
    assert "C8A020" in html.upper(), "index.html must use pilgrim color #C8A020"


def test_html_musician_color():
    """Musicians must use deep green #3A7040."""
    html = read_html()
    assert "3A7040" in html.upper(), "index.html must use musician color #3A7040"


def test_html_escort_color():
    """Escort must use deep blue #1A3080."""
    html = read_html()
    assert "1A3080" in html.upper(), "index.html must use escort color #1A3080"


def test_html_pilgrim_count_300():
    """Pilgrim count must be ~300."""
    html = read_html()
    assert "300" in html, "index.html must specify ~300 pilgrims"


def test_html_musician_count_80():
    """Musician count must be ~80."""
    html = read_html()
    assert "80" in html, "index.html must specify ~80 musicians"


def test_html_escort_count_40():
    """Escort count must be ~40."""
    html = read_html()
    assert "40" in html, "index.html must specify ~40 escort"


def test_html_attraction_radius_120():
    """Attraction radius R must be 120."""
    html = read_html()
    assert "120" in html, "index.html must set attraction radius R=120"


def test_html_repulsion_radius_15():
    """Short-range repulsion radius must be 15."""
    html = read_html()
    assert "15" in html, "index.html must set repulsion radius R_REPEL=15"


def test_html_drift_force():
    """Rightward drift must be applied (0.02)."""
    html = read_html()
    assert "0.02" in html, "index.html must apply drift force of 0.02"


def test_html_damping():
    """Velocity damping must be 0.85."""
    html = read_html()
    assert "0.85" in html, "index.html must apply velocity damping of 0.85"


def test_html_max_speed_3():
    """Max speed must be clamped to 3."""
    html = read_html()
    assert "MAX_SPEED" in html or re.search(r'>\s*3\b', html), (
        "index.html must clamp max speed to 3px/frame"
    )


def test_html_toroidal_wrap():
    """Particles must wrap toroidally using modulo."""
    html = read_html()
    assert "% W" in html or "% H" in html or "% width" in html or "modulo" in html.lower(), (
        "index.html must implement toroidal wrapping"
    )


def test_html_attraction_matrix():
    """Attraction matrix A must be defined."""
    html = read_html()
    assert re.search(r'\bA\s*=\s*\[', html), "index.html must define attraction matrix A"


def test_html_background_color():
    """Background must be near-black #0A0A08."""
    html = read_html()
    assert "0A0A08" in html.upper() or "0a0a08" in html.lower(), (
        "Background must be #0A0A08"
    )


def test_html_hebrew_caption():
    """index.html must display the Hebrew flute caption."""
    html = read_html()
    assert "וְהֶחָלִיל" in html, (
        "index.html must display Hebrew caption 'וְהֶחָלִיל מַכֶּה לִפְנֵיהֶם'"
    )


def test_html_fps_cap_60():
    """Animation must be capped at 60fps."""
    html = read_html()
    assert "60" in html and ("FRAME_MS" in html or "FPS_CAP" in html or "fps" in html.lower()), (
        "index.html must implement a 60fps cap"
    )


def test_html_three_species():
    """HTML must define exactly 3 species with distinct colors."""
    html = read_html()
    colors_found = sum(1 for c in ["C8A020", "3A7040", "1A3080"] if c.upper() in html.upper())
    assert colors_found == 3, (
        f"index.html must define 3 species colors, found only {colors_found}"
    )


def test_html_particle_radius_3():
    """Each particle must be drawn as radius-3 circle."""
    html = read_html()
    assert re.search(r'arc\s*\(.*,\s*3\s*,', html) or "radius 3" in html or ", 3," in html, (
        "index.html must draw particles with radius 3"
    )


# ---------------------------------------------------------------------------
# Thumbnail SVG
# ---------------------------------------------------------------------------

def test_thumbnail_is_valid_svg():
    """thumbnail.svg must be a valid SVG file."""
    with open(THUMBNAIL, encoding="utf-8") as fh:
        content = fh.read()
    assert "<svg" in content and "</svg>" in content, "thumbnail.svg is not valid SVG"


def test_thumbnail_has_dark_background():
    """Thumbnail must use near-black background."""
    with open(THUMBNAIL, encoding="utf-8") as fh:
        content = fh.read()
    assert "0A0A08" in content.upper() or "0a0a08" in content.lower(), (
        "thumbnail.svg must use #0A0A08 background"
    )


def test_thumbnail_has_gold_circles():
    """Thumbnail must contain gold circles for pilgrims."""
    with open(THUMBNAIL, encoding="utf-8") as fh:
        content = fh.read()
    assert "<circle" in content, "thumbnail.svg must contain circle elements"
    assert "C8A020" in content.upper(), "thumbnail.svg must contain gold #C8A020 circles"


def test_thumbnail_has_green_circles():
    """Thumbnail must contain green circles for musicians."""
    with open(THUMBNAIL, encoding="utf-8") as fh:
        content = fh.read()
    assert "3A7040" in content.upper(), "thumbnail.svg must contain green #3A7040 circles"


def test_thumbnail_has_blue_circles():
    """Thumbnail must contain blue circles for escort."""
    with open(THUMBNAIL, encoding="utf-8") as fh:
        content = fh.read()
    assert "1A3080" in content.upper(), "thumbnail.svg must contain blue #1A3080 circles"


def test_thumbnail_has_motion_trails():
    """Thumbnail must suggest motion with trail lines."""
    with open(THUMBNAIL, encoding="utf-8") as fh:
        content = fh.read()
    assert "<line" in content, "thumbnail.svg must contain motion trail line elements"


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

def test_piece_id_unique_in_pieces_json():
    """Piece ID must not appear twice in pieces.json."""
    pieces = load_pieces()
    ids = [p["id"] for p in pieces]
    count = ids.count(PIECE_ID)
    assert count == 1, f"Piece ID '{PIECE_ID}' appears {count} times in pieces.json (expected 1)"


def test_essay_cites_both_hebrew_and_english():
    """Essay must contain both Hebrew characters and English translations."""
    text = read_essay()
    hebrew_chars = [c for c in text if 'א' <= c <= 'ת']
    assert len(hebrew_chars) >= 20, (
        f"Essay must have substantial Hebrew text; found {len(hebrew_chars)} chars"
    )
    assert '"' in text or '"' in text or '"' in text or 'wandering' in text.lower(), (
        "Essay must contain English translations of Hebrew sources"
    )


def test_missing_piece_not_found():
    """A non-existent piece ID must not appear in pieces.json."""
    piece = next((p for p in load_pieces() if p["id"] == "99-nonexistent-piece"), None)
    assert piece is None, "Fixture: non-existent piece must not appear in pieces.json"


def test_essay_does_not_describe_stipple():
    """Essay must not describe stipple/Lloyd's algorithm (belongs to piece 66)."""
    text = read_essay().lower()
    assert "lloyd" not in text and "stipple" not in text, (
        "Essay must not describe the stipple technique already used in piece 66"
    )


def test_html_species_count_array():
    """HTML must define an array of species particle counts."""
    html = read_html()
    assert re.search(r'SPECIES_COUNT\s*=\s*\[', html) or (
        "300" in html and "80" in html and "40" in html
    ), "index.html must define particle counts for each species"
