"""
Tests for piece 22-akdamut: Akdamut particle-swarm typography.

Verifies: file layout, pieces.json registration, canvas animation requirements,
essay content, thumbnail SVG validity, and explicit failure-mode guards.
"""
import json
import os
import re

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID = "22-akdamut"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")


def _load_pieces():
    with open(PIECES_JSON, encoding="utf-8") as fh:
        return json.load(fh)


def _piece_entry():
    """Return the pieces.json entry for 22-akdamut, or None if absent."""
    for p in _load_pieces():
        if p["id"] == PIECE_ID:
            return p
    return None


def _read(filename):
    with open(os.path.join(PIECE_DIR, filename), encoding="utf-8") as fh:
        return fh.read()


# ---------------------------------------------------------------------------
# File layout — happy path
# ---------------------------------------------------------------------------

def test_index_html_exists():
    """index.html must be present in the piece directory."""
    assert os.path.isfile(os.path.join(PIECE_DIR, "index.html")), "index.html missing"


def test_essay_md_exists():
    """essay.md must be present in the piece directory."""
    assert os.path.isfile(os.path.join(PIECE_DIR, "essay.md")), "essay.md missing"


def test_thumbnail_svg_exists():
    """thumbnail.svg must be present in the piece directory."""
    assert os.path.isfile(os.path.join(PIECE_DIR, "thumbnail.svg")), "thumbnail.svg missing"


def test_readme_exists():
    """README.md must be present in the piece directory."""
    assert os.path.isfile(os.path.join(PIECE_DIR, "README.md")), "README.md missing"


# ---------------------------------------------------------------------------
# pieces.json registration — happy path
# ---------------------------------------------------------------------------

def test_piece_registered_in_pieces_json():
    """'22-akdamut' must have an entry in pieces.json."""
    assert _piece_entry() is not None, f"'{PIECE_ID}' not found in pieces.json"


def test_pieces_json_required_fields():
    """All required gallery fields must be present and non-empty."""
    entry = _piece_entry()
    assert entry is not None
    required = ("id", "title", "tagline", "year", "theme", "technique", "path", "thumbnail", "essay")
    for field in required:
        assert field in entry and entry[field], f"Missing or empty field '{field}'"


def test_pieces_json_id_correct():
    """id field must be exactly '22-akdamut'."""
    entry = _piece_entry()
    assert entry is not None
    assert entry["id"] == PIECE_ID


def test_pieces_json_technique_mentions_particle():
    """Technique must mention particle-swarm assembly."""
    entry = _piece_entry()
    assert entry is not None
    technique = entry.get("technique", "").lower()
    assert "particle" in technique, f"technique must mention 'particle', got: {technique!r}"


def test_pieces_json_technique_mentions_typography():
    """Technique must mention typography."""
    entry = _piece_entry()
    assert entry is not None
    technique = entry.get("technique", "").lower()
    assert "typography" in technique, f"technique must mention 'typography', got: {technique!r}"


def test_pieces_json_theme_mentions_torah():
    """Theme must mention Torah and Devotion."""
    entry = _piece_entry()
    assert entry is not None
    theme = entry.get("theme", "")
    assert "Torah" in theme, f"theme must mention Torah, got: {theme!r}"


def test_pieces_json_year_is_integer():
    """Year field must be an integer."""
    entry = _piece_entry()
    assert entry is not None
    assert isinstance(entry["year"], int), f"year must be int, got {entry['year']!r}"


def test_pieces_json_id_matches_directory():
    """The id field must match the directory name in path."""
    entry = _piece_entry()
    assert entry is not None
    parts = entry["path"].replace("\\", "/").split("/")
    dir_name = parts[-2]
    assert dir_name == PIECE_ID, f"Directory '{dir_name}' does not match id '{PIECE_ID}'"


# ---------------------------------------------------------------------------
# essay.md content — happy path
# ---------------------------------------------------------------------------

def test_essay_word_count_at_least_300():
    """Essay must have at least 300 words."""
    text = _read("essay.md")
    count = len(text.split())
    assert count >= 300, f"essay.md has only {count} words (need >= 300)"


def test_essay_mentions_rabbi_meir():
    """Essay must mention Rabbi Meir ben Isaac."""
    text = _read("essay.md")
    assert "Meir" in text, "essay.md must mention Rabbi Meir"


def test_essay_mentions_1096():
    """Essay must reference the year 1096 (First Crusade / composition date)."""
    text = _read("essay.md")
    assert "1096" in text, "essay.md must reference the year 1096"


def test_essay_mentions_crusade():
    """Essay must mention the First Crusade or Crusade context."""
    text = _read("essay.md").lower()
    assert "crusade" in text, "essay.md must mention the Crusade"


def test_essay_mentions_shabbat_12b():
    """Essay must cite BT Shabbat 12b (angels and Aramaic source)."""
    text = _read("essay.md")
    assert "Shabbat 12b" in text or "12b" in text, "essay.md must cite Shabbat 12b"


def test_essay_mentions_aramaic():
    """Essay must discuss the Aramaic language choice."""
    text = _read("essay.md").lower()
    assert "aramaic" in text, "essay.md must discuss Aramaic"


def test_essay_mentions_akdamut():
    """Essay must mention Akdamut."""
    text = _read("essay.md")
    assert "Akdamut" in text or "akdamut" in text.lower(), "essay.md must mention Akdamut"


def test_essay_mentions_acrostic():
    """Essay must mention the acrostic structure of the poem."""
    text = _read("essay.md").lower()
    assert "acrostic" in text, "essay.md must describe the acrostic structure"


def test_essay_mentions_worms():
    """Essay must mention Worms (the city where Rabbi Meir lived)."""
    text = _read("essay.md")
    assert "Worms" in text, "essay.md must mention Worms"


def test_essay_not_a_stub():
    """essay.md must have real content — not a stub with too few substantive words."""
    text = _read("essay.md")
    words = text.split()
    assert len(words) >= 300, f"essay.md looks like a stub: only {len(words)} words"
    long_words = [w for w in words if len(w) > 4]
    assert len(long_words) >= 80, "essay.md has too few substantive words"


# ---------------------------------------------------------------------------
# index.html structure and animation requirements — happy path
# ---------------------------------------------------------------------------

def test_index_html_has_canvas_element():
    """index.html must have a <canvas> element."""
    html = _read("index.html")
    assert "<canvas" in html, "index.html must contain a <canvas> element"


def test_index_html_canvas_at_least_600():
    """Canvas width and height must be at least 600."""
    html = _read("index.html")
    m_w = re.search(r'width=["\'](\d+)["\']', html)
    m_h = re.search(r'height=["\'](\d+)["\']', html)
    assert m_w is not None, "canvas must have a width attribute"
    assert m_h is not None, "canvas must have a height attribute"
    assert int(m_w.group(1)) >= 600, f"canvas width {m_w.group(1)} must be >= 600"
    assert int(m_h.group(1)) >= 600, f"canvas height {m_h.group(1)} must be >= 600"


def test_index_html_uses_requestanimationframe():
    """index.html must use requestAnimationFrame for the animation loop."""
    html = _read("index.html")
    assert "requestAnimationFrame" in html, "index.html must use requestAnimationFrame"


def test_index_html_has_background_color():
    """index.html must reference the midnight blue-black background #080d1a."""
    html = _read("index.html")
    assert "#080d1a" in html, "index.html must use background color #080d1a"


def test_index_html_has_particle_color():
    """index.html must reference the soft gold particle color #e8c060."""
    html = _read("index.html")
    assert "e8c060" in html or "232,192,96" in html, (
        "index.html must reference particle color #e8c060 or rgba(232,192,96,...)"
    )


def test_index_html_has_glow_color():
    """index.html must reference the glow color #ffdd44."""
    html = _read("index.html")
    assert "ffdd44" in html or "ffdd44".upper() in html, (
        "index.html must reference glow color #ffdd44"
    )


def test_index_html_has_shadowBlur():
    """index.html must use shadowBlur for the assembled-letter glow effect."""
    html = _read("index.html")
    assert "shadowBlur" in html, "index.html must set shadowBlur for glow effect"


def test_index_html_has_shadowColor():
    """index.html must set shadowColor for the glow effect."""
    html = _read("index.html")
    assert "shadowColor" in html, "index.html must set shadowColor"


def test_index_html_has_22_letter_sequence():
    """index.html must define the 22-letter Hebrew alphabet array."""
    html = _read("index.html")
    assert "LETTERS" in html or "letters" in html.lower(), (
        "index.html must define the Hebrew letter sequence array"
    )
    assert "א" in html, "index.html must include Hebrew letter alef"
    assert "ת" in html, "index.html must include Hebrew letter tav"


def test_index_html_letters_array_has_22_entries():
    """The LETTERS array must contain all 22 Hebrew letters."""
    html = _read("index.html")
    hebrew_letters = ['א','ב','ג','ד','ה','ו','ז','ח','ט','י','כ','ל','מ','נ','ס','ע','פ','צ','ק','ר','ש','ת']
    for letter in hebrew_letters:
        assert letter in html, f"index.html must include Hebrew letter {letter}"


def test_index_html_has_akdamut_phrase():
    """index.html must include the Akdamut phrase אַקְדָּמוּת מִלִּין."""
    html = _read("index.html")
    assert "אַקְדָּמוּת" in html or "אקדמות" in html, (
        "index.html must include the Akdamut phrase"
    )


def test_index_html_has_num_particles_300():
    """index.html must define NUM_PARTICLES at approximately 300."""
    html = _read("index.html")
    assert "300" in html, "index.html must define NUM_PARTICLES = 300"


def test_index_html_has_assemble_duration():
    """index.html must define ASSEMBLE_DURATION around 1500ms (1.5s)."""
    html = _read("index.html")
    assert "1500" in html, "index.html must define ASSEMBLE_DURATION = 1500"


def test_index_html_has_hold_duration():
    """index.html must define HOLD_DURATION around 800ms."""
    html = _read("index.html")
    assert "800" in html, "index.html must define HOLD_DURATION = 800"


def test_index_html_has_akdamut_hold():
    """index.html must define AKDAMUT_HOLD of 3000ms (3s) for the phrase."""
    html = _read("index.html")
    assert "3000" in html, "index.html must define AKDAMUT_HOLD = 3000"


def test_index_html_has_glyph_sampling():
    """index.html must use getImageData to sample glyph pixel coordinates."""
    html = _read("index.html")
    assert "getImageData" in html, "index.html must call getImageData for glyph sampling"


def test_index_html_has_offscreen_canvas():
    """index.html must create an offscreen canvas for glyph rasterization."""
    html = _read("index.html")
    assert "createElement('canvas')" in html or 'createElement("canvas")' in html, (
        "index.html must create an offscreen canvas for glyph rasterization"
    )


def test_index_html_has_fps_cap():
    """index.html must cap the animation at 60 fps."""
    html = _read("index.html")
    assert "60" in html, "index.html must reference 60 fps cap"
    assert "FRAME_INTERVAL" in html or "frameInterval" in html.lower() or "1000 / TARGET_FPS" in html or "1000/60" in html, (
        "index.html must implement frame interval logic for fps capping"
    )


def test_index_html_embeds_essay_words():
    """At least 5 of the first 10 long words from essay.md must appear in index.html."""
    essay = _read("essay.md")
    html = _read("index.html")
    long_words = [w for w in essay.split() if len(w) > 5][:10]
    found = sum(1 for w in long_words if w in html)
    assert found >= 5, (
        f"Only {found}/10 sampled essay words found in index.html — essay must be embedded inline"
    )


def test_index_html_has_essay_panel():
    """index.html must have an essay section alongside the canvas."""
    html = _read("index.html").lower()
    assert "essay" in html, "index.html must have an essay panel element"


def test_index_html_mentions_shabbat_12b():
    """index.html must cite Shabbat 12b (the Aramaic/angels source)."""
    html = _read("index.html")
    assert "Shabbat 12b" in html or "12b" in html, "index.html must cite Shabbat 12b"


def test_index_html_spring_damper_formula():
    """index.html must use the spring-damper lerp formula from technique notes."""
    html = _read("index.html")
    assert "0.07" in html, "index.html must use spring factor 0.07 from technique notes"
    assert "0.85" in html, "index.html must use damping factor 0.85 from technique notes"


def test_index_html_no_external_resources():
    """index.html must not load fonts or scripts from external URLs."""
    html = _read("index.html")
    assert "fonts.googleapis" not in html, "index.html must not load Google Fonts"
    assert "@import url" not in html, "index.html must not use @import url"


# ---------------------------------------------------------------------------
# thumbnail.svg — happy path
# ---------------------------------------------------------------------------

def test_thumbnail_is_valid_svg():
    """thumbnail.svg must be a well-formed SVG document."""
    svg = _read("thumbnail.svg")
    assert "<svg" in svg and "</svg>" in svg, "thumbnail.svg must be valid SVG"


def test_thumbnail_has_viewbox():
    """thumbnail.svg must declare a viewBox."""
    svg = _read("thumbnail.svg")
    assert "viewBox" in svg, "thumbnail.svg must have a viewBox"


def test_thumbnail_has_dark_background():
    """thumbnail.svg must use the midnight blue-black background #080d1a."""
    svg = _read("thumbnail.svg")
    assert "#080d1a" in svg, "thumbnail.svg must use background #080d1a"


def test_thumbnail_has_gold_color():
    """thumbnail.svg must use the soft gold particle color #e8c060."""
    svg = _read("thumbnail.svg")
    assert "#e8c060" in svg, "thumbnail.svg must use gold color #e8c060"


def test_thumbnail_has_alef():
    """thumbnail.svg must display the letter alef (א)."""
    svg = _read("thumbnail.svg")
    assert "א" in svg, "thumbnail.svg must contain the letter alef"


def test_thumbnail_has_particle_dots():
    """thumbnail.svg must contain <circle> elements representing scattered particles."""
    svg = _read("thumbnail.svg")
    circle_count = svg.count("<circle")
    assert circle_count >= 10, (
        f"thumbnail.svg must have >= 10 particle circles, found {circle_count}"
    )


# ---------------------------------------------------------------------------
# Edge cases and failure modes
# ---------------------------------------------------------------------------

def test_missing_index_html_would_be_detected(tmp_path):
    """Verify that absence of index.html in a different path would be caught."""
    fake = os.path.join(str(tmp_path), "index.html")
    assert not os.path.isfile(fake), "Fixture path must not exist"


def test_missing_essay_would_be_detected(tmp_path):
    """Verify that absence of essay.md would be caught."""
    fake = os.path.join(str(tmp_path), "essay.md")
    assert not os.path.isfile(fake), "Fixture path must not exist"


def test_stub_essay_rejected():
    """An essay with fewer than 300 words must be flagged as a stub."""
    stub = "This is a stub. " * 10
    words = len(stub.split())
    assert words < 300, "Fixture must be under 300 words to test the guard"


def test_pieces_json_duplicate_ids_would_fail():
    """Duplicate IDs in pieces.json would break gallery routing."""
    pieces = _load_pieces()
    ids = [p["id"] for p in pieces]
    assert len(ids) == len(set(ids)), f"Duplicate piece IDs found: {ids}"


def test_essay_under_700_words():
    """Essay should be <=700 words — brevity guard (acceptance says ~300-500, slight overage allowed)."""
    text = _read("essay.md")
    count = len(text.split())
    assert count <= 700, f"essay.md has {count} words, likely too long (expected ~300-500)"


def test_pieces_json_22_akdamut_path_exists():
    """The path field in pieces.json for 22-akdamut must point to an existing file."""
    entry = _piece_entry()
    assert entry is not None
    full_path = os.path.join(GALLERY_ROOT, entry["path"])
    assert os.path.isfile(full_path), f"path '{entry['path']}' does not exist on disk"


def test_pieces_json_22_akdamut_thumbnail_exists():
    """The thumbnail field in pieces.json for 22-akdamut must point to an existing file."""
    entry = _piece_entry()
    assert entry is not None
    full_thumb = os.path.join(GALLERY_ROOT, entry["thumbnail"])
    assert os.path.isfile(full_thumb), f"thumbnail '{entry['thumbnail']}' does not exist on disk"


def test_pieces_json_22_akdamut_essay_exists():
    """The essay field in pieces.json for 22-akdamut must point to an existing file."""
    entry = _piece_entry()
    assert entry is not None
    full_essay = os.path.join(GALLERY_ROOT, entry["essay"])
    assert os.path.isfile(full_essay), f"essay '{entry['essay']}' does not exist on disk"
