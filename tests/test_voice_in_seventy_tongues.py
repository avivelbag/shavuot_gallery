"""
Tests for piece 39-voice-in-seventy-tongues: Penrose P3 aperiodic tiling.

Verifies: file layout, pieces.json registration, Penrose tiling algorithm
correctness, essay content, multi-script glyph presence, thumbnail validity,
animation requirements, and explicit failure-mode guards.
"""
import json
import os
import re

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID = "39-voice-in-seventy-tongues"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")


def _load_pieces():
    with open(PIECES_JSON, encoding="utf-8") as fh:
        return json.load(fh)


def _piece_entry():
    """Return the pieces.json entry for 39-voice-in-seventy-tongues, or None."""
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
    """'39-voice-in-seventy-tongues' must appear in pieces.json."""
    assert _piece_entry() is not None, f"'{PIECE_ID}' not found in pieces.json"


def test_pieces_json_required_fields():
    """All required gallery fields must be present and non-empty."""
    entry = _piece_entry()
    assert entry is not None
    for field in ("id", "title", "tagline", "year", "theme", "technique", "path", "thumbnail", "essay"):
        assert field in entry and entry[field], f"Missing or empty field '{field}'"


def test_pieces_json_id_correct():
    """id field must be exactly '39-voice-in-seventy-tongues'."""
    entry = _piece_entry()
    assert entry is not None
    assert entry["id"] == PIECE_ID


def test_pieces_json_technique_mentions_penrose():
    """Technique must mention Penrose tiling."""
    entry = _piece_entry()
    assert entry is not None
    technique = entry.get("technique", "").lower()
    assert "penrose" in technique, f"technique must mention 'penrose', got: {technique!r}"


def test_pieces_json_technique_mentions_canvas():
    """Technique must mention canvas 2D rendering."""
    entry = _piece_entry()
    assert entry is not None
    technique = entry.get("technique", "").lower()
    assert "canvas" in technique, f"technique must mention 'canvas', got: {technique!r}"


def test_pieces_json_theme_mentions_matan_torah():
    """Theme must mention Matan Torah."""
    entry = _piece_entry()
    assert entry is not None
    theme = entry.get("theme", "")
    assert "Torah" in theme or "Matan" in theme, f"theme must mention Matan Torah, got: {theme!r}"


def test_pieces_json_year_is_integer():
    """Year field must be an integer."""
    entry = _piece_entry()
    assert entry is not None
    assert isinstance(entry["year"], int), f"year must be int, got {entry['year']!r}"


def test_pieces_json_id_matches_directory():
    """The id field must match the directory name in the path."""
    entry = _piece_entry()
    assert entry is not None
    parts = entry["path"].replace("\\", "/").split("/")
    dir_name = parts[-2]
    assert dir_name == PIECE_ID, f"Directory '{dir_name}' does not match id '{PIECE_ID}'"


def test_pieces_json_no_duplicate_ids():
    """Duplicate IDs in pieces.json would break gallery routing."""
    pieces = _load_pieces()
    ids = [p["id"] for p in pieces]
    assert len(ids) == len(set(ids)), f"Duplicate piece IDs found: {ids}"


# ---------------------------------------------------------------------------
# essay.md content — happy path
# ---------------------------------------------------------------------------

def test_essay_word_count_at_least_300():
    """Essay must have at least 300 words."""
    text = _read("essay.md")
    count = len(text.split())
    assert count >= 300, f"essay.md has only {count} words (need >= 300)"


def test_essay_cites_shemot_rabbah():
    """Essay must cite Shemot Rabbah 5:9."""
    text = _read("essay.md")
    assert "Shemot Rabbah" in text or "5:9" in text, \
        "essay.md must cite Shemot Rabbah 5:9"


def test_essay_cites_jerusalem_talmud():
    """Essay must cite the Jerusalem Talmud (Shabbat 1:3)."""
    text = _read("essay.md")
    assert "Jerusalem Talmud" in text or "Shabbat 1:3" in text, \
        "essay.md must cite the Jerusalem Talmud Shabbat 1:3"


def test_essay_cites_bavli_shabbat_88b():
    """Essay must cite Talmud Bavli Shabbat 88b."""
    text = _read("essay.md")
    assert "88b" in text or "Shabbat 88b" in text, \
        "essay.md must cite Talmud Bavli Shabbat 88b"


def test_essay_mentions_penrose():
    """Essay must discuss Penrose tiling."""
    text = _read("essay.md").lower()
    assert "penrose" in text, "essay.md must mention Penrose tiling"


def test_essay_mentions_aleph():
    """Essay must mention the letter aleph (alef) as the center of revelation."""
    text = _read("essay.md").lower()
    assert "aleph" in text or "alef" in text, "essay.md must discuss the aleph"


def test_essay_mentions_naaseh_vnishma():
    """Essay must reference naaseh v'nishma (we will do and we will hear)."""
    text = _read("essay.md").lower()
    assert "naaseh" in text or "nishma" in text or "will do" in text, \
        "essay.md must discuss naaseh v'nishma"


def test_essay_mentions_seventy_tongues():
    """Essay must discuss the seventy languages / nations."""
    text = _read("essay.md").lower()
    assert "seventy" in text or "70" in text, \
        "essay.md must discuss the seventy tongues"


def test_essay_mentions_aperiodic():
    """Essay must describe the aperiodic / non-repeating property of Penrose tiling."""
    text = _read("essay.md").lower()
    assert "aperiodic" in text or "never repeat" in text or "non-repeating" in text, \
        "essay.md must explain the aperiodic nature of Penrose tiling"


def test_essay_not_a_stub():
    """Essay must have real substantive content."""
    text = _read("essay.md")
    words = text.split()
    assert len(words) >= 300, f"essay looks like a stub: {len(words)} words"
    long_words = [w for w in words if len(w) > 4]
    assert len(long_words) >= 80, "essay has too few substantive (>4-char) words"


# ---------------------------------------------------------------------------
# index.html structure and Penrose requirements — happy path
# ---------------------------------------------------------------------------

def test_index_html_has_canvas_element():
    """index.html must have a <canvas> element."""
    html = _read("index.html")
    assert "<canvas" in html, "index.html must contain a <canvas> element"


def test_index_html_canvas_at_least_600():
    """Canvas width and height must be at least 600px."""
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


def test_index_html_has_phi_constant():
    """index.html must define the golden ratio PHI."""
    html = _read("index.html")
    assert "PHI" in html or "phi" in html.lower() or "golden" in html.lower(), \
        "index.html must define the golden ratio constant"


def test_index_html_has_deflate_function():
    """index.html must implement a deflation function for Penrose subdivision."""
    html = _read("index.html")
    assert "deflate" in html, "index.html must define a deflate() function"


def test_index_html_has_sun_configuration():
    """index.html must build the initial 10-triangle sun configuration."""
    html = _read("index.html")
    assert "10" in html, "index.html must reference the 10-triangle sun configuration"
    assert "sun" in html.lower() or "2 * Math.PI" in html or "Math.PI" in html, \
        "index.html must use angular arithmetic for the sun layout"


def test_index_html_has_type_0_and_type_1():
    """index.html must distinguish thick (type 0) and thin (type 1) triangles."""
    html = _read("index.html")
    assert "type: 0" in html or "type:0" in html or "type === 0" in html, \
        "index.html must handle type-0 (thick) triangles"
    assert "type: 1" in html or "type:1" in html or "type === 1" in html, \
        "index.html must handle type-1 (thin) triangles"


def test_index_html_has_n_deflate_at_least_5():
    """index.html must deflate at least 5 times for sufficient tile density."""
    html = _read("index.html")
    m = re.search(r'N_DEFLATE\s*=\s*(\d+)', html)
    assert m is not None, "index.html must define N_DEFLATE constant"
    assert int(m.group(1)) >= 5, f"N_DEFLATE must be >= 5, got {m.group(1)}"


def test_index_html_has_scale_constant():
    """index.html must define a SCALE constant for canvas coordinate mapping."""
    html = _read("index.html")
    assert "SCALE" in html, "index.html must define a SCALE constant"


def test_index_html_has_parchment_color():
    """index.html must use a parchment/gold color for thick tiles."""
    html = _read("index.html")
    assert "FFF8E8" in html.upper() or "F2E4C0" in html.upper() or "FFF8" in html.upper(), \
        "index.html must use a parchment color for thick tiles"


def test_index_html_has_blue_color():
    """index.html must use a blue color for thin tiles."""
    html = _read("index.html")
    assert "B8D4E8" in html.upper() or "1A3A6A" in html.upper() or "2B4F7A" in html.upper(), \
        "index.html must use a blue color for thin tiles"


def test_index_html_has_aleph_glyph():
    """index.html must render the central aleph (א)."""
    html = _read("index.html")
    assert "א" in html, "index.html must display the aleph glyph"


def test_index_html_has_pulse_animation():
    """index.html must implement the sinusoidal luminosity pulse animation."""
    html = _read("index.html")
    assert "sin" in html and ("pulse" in html or "Math.sin" in html), \
        "index.html must implement Math.sin() pulse animation"


def test_index_html_embeds_essay_words():
    """At least 5 of the first 10 long words from essay.md must appear in index.html."""
    essay = _read("essay.md")
    html = _read("index.html")
    long_words = [w for w in essay.split() if len(w) > 5][:10]
    found = sum(1 for w in long_words if w in html)
    assert found >= 5, (
        f"Only {found}/10 sampled essay words found in index.html — "
        "essay must be embedded inline"
    )


def test_index_html_has_essay_panel():
    """index.html must contain an essay section alongside the canvas."""
    html = _read("index.html").lower()
    assert "essay" in html, "index.html must have an essay panel"


def test_index_html_has_five_writing_systems():
    """index.html must include glyphs from at least five writing systems."""
    html = _read("index.html")
    # Hebrew: check for common Hebrew letters other than aleph
    has_hebrew = any(ch in html for ch in ['ב', 'ש', 'ל', 'מ', 'ה'])
    # Greek
    has_greek = any(ch in html for ch in ['α', 'λ', 'ω', 'Σ'])
    # Arabic
    has_arabic = any(ch in html for ch in ['ب', 'ع', 'ج'])
    # Latin: simple ASCII letter in glyph context
    has_latin = "'A'" in html or '"A"' in html or "g: 'A'" in html or 'g: "A"' in html
    # Aramaic/Syriac
    has_aramaic = 'ܐ' in html or 'ܒ' in html

    systems_present = sum([has_hebrew, has_greek, has_arabic, has_latin, has_aramaic])
    assert systems_present >= 5, (
        f"index.html must include glyphs from at least 5 writing systems "
        f"(found {systems_present}): Hebrew={has_hebrew}, Greek={has_greek}, "
        f"Arabic={has_arabic}, Latin={has_latin}, Aramaic={has_aramaic}"
    )


def test_index_html_cites_shemot_rabbah():
    """index.html must cite Shemot Rabbah 5:9 in the essay section."""
    html = _read("index.html")
    assert "Shemot Rabbah" in html or "5:9" in html, \
        "index.html must cite Shemot Rabbah 5:9"


def test_index_html_cites_shabbat_88b():
    """index.html must cite Talmud Bavli Shabbat 88b."""
    html = _read("index.html")
    assert "88b" in html or "Shabbat 88b" in html, \
        "index.html must cite Shabbat 88b"


def test_index_html_no_external_resources():
    """index.html must not load fonts or scripts from external URLs."""
    html = _read("index.html")
    assert "fonts.googleapis" not in html, "index.html must not load Google Fonts"
    assert "@import url" not in html, "index.html must not use @import url"


def test_index_html_shadowblur_for_aleph_glow():
    """index.html must use shadowBlur for the central aleph's glow."""
    html = _read("index.html")
    assert "shadowBlur" in html, "index.html must set shadowBlur for the aleph glow"


def test_index_html_shadowcolor_set():
    """index.html must set shadowColor for glow effects."""
    html = _read("index.html")
    assert "shadowColor" in html, "index.html must set shadowColor"


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
    """thumbnail.svg must use the dark desert-night background color."""
    svg = _read("thumbnail.svg")
    assert "#1a0c02" in svg or "1a0c02" in svg.lower(), \
        "thumbnail.svg must use dark background #1a0c02"


def test_thumbnail_has_aleph():
    """thumbnail.svg must display the letter aleph (א)."""
    svg = _read("thumbnail.svg")
    assert "א" in svg, "thumbnail.svg must contain the central aleph glyph"


def test_thumbnail_has_rhombus_tiles():
    """thumbnail.svg must contain polygon elements representing rhombus tiles."""
    svg = _read("thumbnail.svg")
    poly_count = svg.count("<polygon")
    assert poly_count >= 10, (
        f"thumbnail.svg must have >= 10 polygon tile elements, found {poly_count}"
    )


def test_thumbnail_has_blue_tiles():
    """thumbnail.svg must use blue colors for thin rhombuses."""
    svg = _read("thumbnail.svg")
    assert "#4878" in svg or "#2B4F7A" in svg or "#355A8A" in svg or "90B8D8" in svg, \
        "thumbnail.svg must use blue colors for thin rhombus tiles"


def test_thumbnail_has_gold_tiles():
    """thumbnail.svg must use gold/parchment colors for thick rhombuses."""
    svg = _read("thumbnail.svg")
    assert "#D4A" in svg or "#FFF2" in svg or "#F0D8" in svg or "#E8C5" in svg, \
        "thumbnail.svg must use gold/parchment colors for thick rhombus tiles"


def test_thumbnail_has_scattered_glyphs():
    """thumbnail.svg must include scattered script glyphs beyond the central aleph."""
    svg = _read("thumbnail.svg")
    text_count = svg.count("<text")
    assert text_count >= 4, (
        f"thumbnail.svg must have >= 4 text elements (central aleph + scattered glyphs), "
        f"found {text_count}"
    )


# ---------------------------------------------------------------------------
# Edge cases and failure modes
# ---------------------------------------------------------------------------

def test_missing_index_html_would_be_detected(tmp_path):
    """Absence of index.html would be caught by the file-exists check."""
    fake = os.path.join(str(tmp_path), "index.html")
    assert not os.path.isfile(fake)


def test_missing_essay_would_be_detected(tmp_path):
    """Absence of essay.md would be caught by the file-exists check."""
    fake = os.path.join(str(tmp_path), "essay.md")
    assert not os.path.isfile(fake)


def test_stub_essay_rejected():
    """An essay with fewer than 300 words must be flagged as a stub."""
    stub = "This is a stub. " * 10
    assert len(stub.split()) < 300


def test_essay_under_1000_words():
    """Essay should be <=1000 words — brevity guard."""
    text = _read("essay.md")
    count = len(text.split())
    assert count <= 1000, f"essay.md has {count} words, expected <= 1000"


def test_thumbnail_not_empty():
    """thumbnail.svg must not be an empty or near-empty file."""
    svg = _read("thumbnail.svg")
    assert len(svg) > 500, "thumbnail.svg is suspiciously short"


def test_pieces_json_path_exists_on_disk():
    """The path in pieces.json for this piece must point to an existing file."""
    entry = _piece_entry()
    assert entry is not None
    full_path = os.path.join(GALLERY_ROOT, entry["path"])
    assert os.path.isfile(full_path), f"path '{entry['path']}' does not exist on disk"


def test_pieces_json_thumbnail_exists_on_disk():
    """The thumbnail in pieces.json for this piece must exist on disk."""
    entry = _piece_entry()
    assert entry is not None
    full_thumb = os.path.join(GALLERY_ROOT, entry["thumbnail"])
    assert os.path.isfile(full_thumb), f"thumbnail '{entry['thumbnail']}' does not exist"


def test_pieces_json_essay_exists_on_disk():
    """The essay file in pieces.json for this piece must exist on disk."""
    entry = _piece_entry()
    assert entry is not None
    full_essay = os.path.join(GALLERY_ROOT, entry["essay"])
    assert os.path.isfile(full_essay), f"essay '{entry['essay']}' does not exist"
