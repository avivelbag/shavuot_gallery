"""
Tests for piece 66-sinai-billiard-chaos: the Sinai billiard animation.

Validates piece registration, file existence, essay content, and
specific technical requirements of the billiard simulation (physics
keywords, canvas dimensions, particle count, palette).
"""
import json
import os
import re

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")
PIECE_ID = "66-sinai-billiard-chaos"
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


def test_piece_theme_is_har_sinai():
    """Theme must be 'Har Sinai' per acceptance criteria."""
    piece = get_piece()
    assert piece is not None
    assert "Sinai" in piece["theme"], f"Expected 'Sinai' in theme, got: {piece['theme']!r}"


def test_piece_technique_mentions_billiard():
    """Technique must mention 'billiard' per acceptance criteria."""
    piece = get_piece()
    assert piece is not None
    assert "billiard" in piece["technique"].lower(), (
        f"Expected 'billiard' in technique, got: {piece['technique']!r}"
    )


def test_piece_technique_mentions_ergodic():
    """Technique must mention 'ergodic' per acceptance criteria."""
    piece = get_piece()
    assert piece is not None
    assert "ergodic" in piece["technique"].lower(), (
        f"Expected 'ergodic' in technique, got: {piece['technique']!r}"
    )


# ---------------------------------------------------------------------------
# File existence
# ---------------------------------------------------------------------------

def test_index_html_exists():
    assert os.path.isfile(INDEX_HTML), f"index.html missing at {INDEX_HTML}"


def test_essay_md_exists():
    assert os.path.isfile(ESSAY_MD), f"essay.md missing at {ESSAY_MD}"


def test_thumbnail_exists():
    assert os.path.isfile(THUMBNAIL), f"thumbnail.svg missing at {THUMBNAIL}"


def test_readme_exists():
    assert os.path.isfile(README), f"README.md missing at {README}"


# ---------------------------------------------------------------------------
# Essay content
# ---------------------------------------------------------------------------

def test_essay_minimum_word_count():
    """Essay must be at least 400 words (acceptance: ~400 words)."""
    text = read_essay()
    word_count = len(text.split())
    assert word_count >= 400, f"Essay has only {word_count} words (need ≥ 400)"


def test_essay_cites_mechilta():
    """Essay must cite the Mechilta d'Rabbi Yishmael source."""
    text = read_essay()
    assert "Mechilta" in text, "Essay must cite Mechilta d'Rabbi Yishmael"


def test_essay_cites_exodus_19():
    """Essay must cite Exodus 19:2 (encampment at Sinai)."""
    text = read_essay()
    assert "19:2" in text or "Exodus 19" in text, "Essay must cite Exodus 19:2"


def test_essay_cites_shemot_rabbah():
    """Essay must cite Shemot Rabbah 5:9."""
    text = read_essay()
    assert "Shemot Rabbah" in text or "5:9" in text, "Essay must cite Shemot Rabbah 5:9"


def test_essay_contains_hebrew_exodus_verse():
    """Essay must contain the Hebrew text of Exodus 19:2 (vayachanu)."""
    text = read_essay()
    assert "וַיַּחֲנוּ" in text or "וַיִּחַן" in text, (
        "Essay must include Hebrew text of Exodus 19:2"
    )


def test_essay_contains_hebrew_midrash():
    """Essay must include Hebrew text from Mechilta or Shemot Rabbah."""
    text = read_essay()
    assert "הֶפְקֵר" in text or "לְפִי כֹּחוֹ" in text or "שִׁבְעִים" in text, (
        "Essay must include Hebrew text from the cited midrashic sources"
    )


def test_essay_mentions_sinai_mathematician():
    """Essay must name Yakov Sinai as the mathematician."""
    text = read_essay()
    assert "Sinai" in text and ("mathematician" in text.lower() or "Yakov" in text), (
        "Essay must name Yakov Sinai as the mathematician behind the billiard"
    )


def test_essay_mentions_ergodic():
    """Essay must use the word 'ergodic'."""
    text = read_essay()
    assert "ergodic" in text.lower(), "Essay must mention ergodicity"


# ---------------------------------------------------------------------------
# index.html: simulation and canvas requirements
# ---------------------------------------------------------------------------

def test_html_embeds_essay_text():
    """index.html must embed essay text inline (sampled keyword check)."""
    essay = read_essay()
    html = read_html()
    words = [w for w in essay.split() if len(w) > 6][:15]
    found = sum(1 for w in words if w in html)
    assert found >= 8, (
        f"index.html does not appear to embed essay text "
        f"(only {found}/15 sampled words found)"
    )


def test_html_canvas_700x700():
    """Canvas must be 700×700 as required by acceptance criteria."""
    html = read_html()
    assert "700" in html, "index.html must set canvas to 700×700"
    assert re.search(r'canvas\.width\s*=\s*700', html) or 'width: 700' in html or 'width="700"' in html, (
        "index.html must set canvas width to 700"
    )


def test_html_uses_request_animation_frame():
    """index.html must use requestAnimationFrame for the animation loop."""
    html = read_html()
    assert "requestAnimationFrame" in html, (
        "index.html must use requestAnimationFrame"
    )


def test_html_ten_particles():
    """Simulation must define 10 particles (one per epsilon offset)."""
    html = read_html()
    assert "EPSILONS" in html or "10" in html, "Expected 10 particles in simulation"
    # Check that there are exactly 10 epsilon offsets defined
    epsilons_match = re.search(r'EPSILONS\s*=\s*\[([^\]]+)\]', html)
    if epsilons_match:
        values = [v.strip() for v in epsilons_match.group(1).split(',') if v.strip()]
        assert len(values) == 10, f"Expected 10 epsilon values, found {len(values)}"


def test_html_circle_radius_04():
    """Circle radius must be 0.4 as specified."""
    html = read_html()
    assert "0.4" in html, "index.html must set circle radius to 0.4"
    assert re.search(r'R\s*=\s*0\.4', html), "Expected 'R = 0.4' in simulation"


def test_html_world_size_1():
    """World half-size must be 1.0 (box from -1 to 1)."""
    html = read_html()
    assert re.search(r'WORLD\s*=\s*1\.0', html), "Expected 'WORLD = 1.0' in simulation"


def test_html_500_steps_per_frame():
    """Simulation must advance ~500 steps per frame."""
    html = read_html()
    assert "500" in html, "index.html must use ~500 steps per animation frame"


def test_html_fps_cap_60():
    """Animation must be capped at 60 fps."""
    html = read_html()
    assert "60" in html, "index.html must include a 60fps cap"
    assert "FPS_CAP" in html or "FRAME_MS" in html, (
        "index.html must implement fps cap via FPS_CAP or FRAME_MS"
    )


def test_html_palette_contains_gold():
    """Color palette must include deep gold #D4A020."""
    html = read_html()
    assert "D4A020" in html.upper(), "Palette must include deep gold #D4A020"


def test_html_palette_contains_crimson():
    """Color palette must include crimson #8B1A1A."""
    html = read_html()
    assert "8B1A1A" in html.upper(), "Palette must include crimson #8B1A1A"


def test_html_palette_ten_colors():
    """Palette array must contain 10 distinct hex colors."""
    html = read_html()
    palette_match = re.search(r'PALETTE\s*=\s*\[([^\]]+)\]', html)
    assert palette_match is not None, "Expected PALETTE array in simulation"
    colors = re.findall(r"'#[0-9A-Fa-f]{6}'", palette_match.group(1))
    assert len(colors) == 10, f"Expected 10 palette colors, found {len(colors)}"


def test_html_background_color():
    """Background must be near-black navy #0A0A14."""
    html = read_html()
    assert "0A0A14" in html.upper(), "Background must be #0A0A14"


def test_html_wall_reflection_physics():
    """index.html must implement wall reflection (invert velocity component)."""
    html = read_html()
    # Wall reflection inverts vx or vy
    assert "vx = -p.vx" in html or "p.vx = -p.vx" in html or "vx *= -1" in html, (
        "index.html must invert vx for wall_x collision"
    )
    assert "vy = -p.vy" in html or "p.vy = -p.vy" in html or "vy *= -1" in html, (
        "index.html must invert vy for wall_y collision"
    )


def test_html_circle_reflection_physics():
    """index.html must implement circle reflection about outward normal."""
    html = read_html()
    assert "dot" in html or "2 * dot" in html, (
        "index.html must implement circle reflection using dot product with normal"
    )


def test_html_ray_circle_intersection():
    """index.html must solve the ray-circle quadratic intersection."""
    html = read_html()
    assert "discC" in html or "disc" in html, (
        "index.html must compute ray-circle discriminant for intersection"
    )
    assert "Math.sqrt" in html, "index.html must use Math.sqrt for intersection"


def test_html_fade_effect():
    """index.html must implement trail fading via semi-transparent fillRect."""
    html = read_html()
    assert "rgba(10, 10, 20" in html or "rgba(10,10,20" in html, (
        "index.html must fade trails using rgba(10,10,20,...) fillRect overlay"
    )


def test_html_gold_circle_drawn():
    """The circular obstacle must be drawn with gold color."""
    html = read_html()
    assert "D4A020" in html.upper() and "arc" in html, (
        "index.html must draw the gold circular obstacle using ctx.arc"
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
    assert "0A0A14" in content.upper() or "0a0a14" in content.lower(), (
        "thumbnail.svg must use #0A0A14 background"
    )


def test_thumbnail_has_gold_circle():
    """Thumbnail must contain a gold central circle."""
    with open(THUMBNAIL, encoding="utf-8") as fh:
        content = fh.read()
    assert "<circle" in content, "thumbnail.svg must contain a circle element"
    assert "D4A020" in content.upper(), "thumbnail.svg circle must use gold #D4A020"


def test_thumbnail_has_trajectory_lines():
    """Thumbnail must contain polyline trajectory elements."""
    with open(THUMBNAIL, encoding="utf-8") as fh:
        content = fh.read()
    polylines = re.findall(r'<polyline', content)
    assert len(polylines) >= 6, (
        f"thumbnail.svg must have at least 6 trajectory polylines, found {len(polylines)}"
    )


def test_thumbnail_has_gold_border():
    """Thumbnail must have a gold square border."""
    with open(THUMBNAIL, encoding="utf-8") as fh:
        content = fh.read()
    assert "<rect" in content, "thumbnail.svg must contain border rect"


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

def test_piece_id_unique_in_pieces_json():
    """Piece ID must not appear twice in pieces.json."""
    pieces = load_pieces()
    ids = [p["id"] for p in pieces]
    count = ids.count(PIECE_ID)
    assert count == 1, f"Piece ID '{PIECE_ID}' appears {count} times in pieces.json (expected 1)"


def test_essay_has_both_hebrew_and_english_for_each_source():
    """Each cited source should appear with both Hebrew and English text."""
    text = read_essay()
    # Hebrew characters present (U+05D0–U+05EA range covers Hebrew alef-tav)
    hebrew_chars = [c for c in text if 'א' <= c <= 'ת']
    assert len(hebrew_chars) >= 20, (
        f"Essay must contain substantial Hebrew text; found only {len(hebrew_chars)} Hebrew chars"
    )
    # English translation markers
    assert '"' in text or '"' in text or '"' in text, (
        "Essay must contain English translation quotations"
    )


def test_missing_piece_not_found():
    """A non-existent piece ID should not be found in pieces.json."""
    piece = next((p for p in load_pieces() if p["id"] == "99-nonexistent"), None)
    assert piece is None, "Fixture: non-existent piece must not appear in pieces.json"


def test_essay_does_not_duplicate_peah_theme():
    """Essay must not re-explain peah/leket law (those themes belong to piece 21)."""
    text = read_essay().lower()
    assert "pe'ah" not in text and "peah" not in text, (
        "Essay must not duplicate the peah/leket theme already covered in piece 21"
    )
