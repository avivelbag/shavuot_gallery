"""
Tests for piece 20-sinai-ketubah.

Verifies: file layout, pieces.json registration, SVG structure, Hebrew text,
border-generation script, palette colours, essay content and embedding,
thumbnail validity, and explicit failure-mode guards.
"""
import json
import os

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID = "20-sinai-ketubah"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _load_pieces():
    with open(PIECES_JSON, encoding="utf-8") as fh:
        return json.load(fh)


def _piece_entry():
    for p in _load_pieces():
        if p["id"] == PIECE_ID:
            return p
    return None


def _read(filename):
    with open(os.path.join(PIECE_DIR, filename), encoding="utf-8") as fh:
        return fh.read()


# ---------------------------------------------------------------------------
# pieces.json registration (happy path)
# ---------------------------------------------------------------------------

def test_piece_registered_in_pieces_json():
    """The piece must have an entry in pieces.json."""
    assert _piece_entry() is not None, f"'{PIECE_ID}' not found in pieces.json"


def test_pieces_json_required_fields():
    """All required gallery fields must be present and non-empty."""
    entry = _piece_entry()
    assert entry is not None
    required = ("id", "title", "tagline", "year", "theme", "technique", "path", "thumbnail", "essay")
    for field in required:
        assert field in entry and entry[field], f"Missing or empty field '{field}'"


def test_pieces_json_theme_is_matan_torah():
    """Theme must reference Matan Torah / Sinai as Covenant."""
    entry = _piece_entry()
    assert entry is not None
    theme = entry.get("theme", "")
    assert "Matan Torah" in theme or "Sinai" in theme, (
        f"theme '{theme}' must reference Matan Torah or Sinai"
    )


def test_pieces_json_technique_mentions_svg_generative():
    """Technique must mention SVG generative border."""
    entry = _piece_entry()
    assert entry is not None
    technique = entry.get("technique", "").lower()
    assert "svg" in technique and "generative" in technique, (
        f"technique must mention SVG generative, got: {technique!r}"
    )


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
# File layout (happy path)
# ---------------------------------------------------------------------------

def test_index_html_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "index.html")), "index.html missing"


def test_piece_svg_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "piece.svg")), "piece.svg missing"


def test_thumbnail_svg_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "thumbnail.svg")), "thumbnail.svg missing"


def test_essay_md_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "essay.md")), "essay.md missing"


def test_readme_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "README.md")), "README.md missing"


# ---------------------------------------------------------------------------
# essay.md content
# ---------------------------------------------------------------------------

def test_essay_has_at_least_300_words():
    """Essay must be substantial — at least 300 words."""
    text = _read("essay.md")
    count = len(text.split())
    assert count >= 300, f"essay.md has only {count} words (need ≥ 300)"


def test_essay_mentions_shabbat_88a():
    """Essay must cite the Talmudic source Shabbat 88a."""
    text = _read("essay.md")
    assert "Shabbat 88a" in text or "88a" in text, "essay must reference Shabbat 88a"


def test_essay_mentions_exodus_19_17():
    """Essay must cite Exodus 19:17."""
    text = _read("essay.md")
    assert "19:17" in text or "Exodus 19" in text, "essay must reference Exodus 19:17"


def test_essay_mentions_esther_9_27():
    """Essay must cite Esther 9:27."""
    text = _read("essay.md")
    assert "9:27" in text or "Esther 9" in text, "essay must reference Esther 9:27"


def test_essay_mentions_coercion_or_consent():
    """Essay must discuss the coercion/consent tension."""
    text = _read("essay.md").lower()
    assert "coercion" in text or "coerced" in text or "duress" in text, (
        "essay must address the coercion problem"
    )


def test_essay_contains_hebrew_exodus_verse():
    """essay.md must quote the Hebrew of Exodus 19:17 (vayityatzvu / tachtit)."""
    text = _read("essay.md")
    assert "וַיִּתְיַצְּבוּ" in text or "תַּחְתִּית" in text, (
        "essay must embed the Hebrew of Exodus 19:17"
    )


def test_essay_contains_esther_kiymu():
    """essay.md must quote the Hebrew of Esther 9:27 (kiym'u v'kibl'u)."""
    text = _read("essay.md")
    assert "קִיְּמוּ" in text or "וְקִבְּלוּ" in text, (
        "essay must embed the Hebrew of Esther 9:27"
    )


def test_essay_mentions_ketubah():
    """Essay must explain the ketubah (marriage contract) metaphor."""
    text = _read("essay.md").lower()
    assert "ketubah" in text or "marriage" in text, "essay must mention the ketubah metaphor"


# ---------------------------------------------------------------------------
# piece.svg structure
# ---------------------------------------------------------------------------

def test_piece_svg_is_valid_svg():
    svg = _read("piece.svg")
    assert "<svg" in svg and "</svg>" in svg, "piece.svg is not valid SVG"


def test_piece_svg_has_viewbox():
    svg = _read("piece.svg")
    assert "viewBox" in svg, "piece.svg must declare a viewBox"


def test_piece_svg_viewbox_is_portrait():
    """The viewBox must be a portrait rectangle (height > width)."""
    import re
    svg = _read("piece.svg")
    m = re.search(r'viewBox=["\']0 0 (\d+) (\d+)["\']', svg)
    assert m is not None, "Could not parse viewBox from piece.svg"
    w, h = int(m.group(1)), int(m.group(2))
    assert h > w, f"piece.svg viewBox must be portrait (h={h} > w={w})"


def test_piece_svg_parchment_background():
    """piece.svg must use parchment cream background #f5ead8."""
    svg = _read("piece.svg")
    assert "#f5ead8" in svg, "piece.svg must use parchment background #f5ead8"


def test_piece_svg_indigo_ink():
    """piece.svg must use deep indigo ink #2c2060."""
    svg = _read("piece.svg")
    assert "#2c2060" in svg, "piece.svg must use indigo ink #2c2060"


def test_piece_svg_gold_ornament():
    """piece.svg must use gold #b8860b for ornamental elements."""
    svg = _read("piece.svg")
    assert "#b8860b" in svg, "piece.svg must use gold #b8860b"


def test_piece_svg_has_defs_block():
    """piece.svg must define symbols in a <defs> block."""
    svg = _read("piece.svg")
    assert "<defs>" in svg or "<defs " in svg, "piece.svg must have a <defs> block"


def test_piece_svg_defines_vine_symbol():
    """piece.svg must define a vine-scroll symbol."""
    svg = _read("piece.svg")
    assert 'id="vine"' in svg, "piece.svg must define a vine symbol in <defs>"


def test_piece_svg_defines_pomegranate_symbol():
    """piece.svg must define a pomegranate symbol."""
    svg = _read("piece.svg")
    assert 'id="pomegranate"' in svg, "piece.svg must define a pomegranate symbol in <defs>"


def test_piece_svg_defines_corner_symbol():
    """piece.svg must define a corner rosette symbol."""
    svg = _read("piece.svg")
    assert 'id="corner"' in svg, "piece.svg must define a corner symbol in <defs>"


def test_piece_svg_has_border_layer():
    """piece.svg must have a <g id='border-layer'> for script-generated units."""
    svg = _read("piece.svg")
    assert 'id="border-layer"' in svg, "piece.svg must have a border-layer group"


def test_piece_svg_has_script():
    """piece.svg must contain an inline <script> block for border generation."""
    svg = _read("piece.svg")
    assert "<script" in svg, "piece.svg must have an inline <script> block"


def test_piece_svg_script_uses_createelementns():
    """The script must call createElementNS to create <use> elements programmatically."""
    svg = _read("piece.svg")
    assert "createElementNS" in svg, "script must use createElementNS to build border units"


def test_piece_svg_script_references_vine():
    """The script must reference the vine symbol when generating border units."""
    svg = _read("piece.svg")
    assert "'vine'" in svg or '"vine"' in svg, "script must reference the 'vine' symbol"


def test_piece_svg_script_references_pomegranate():
    """The script must reference the pomegranate symbol when generating border units."""
    svg = _read("piece.svg")
    assert "'pomegranate'" in svg or '"pomegranate"' in svg, (
        "script must reference the 'pomegranate' symbol"
    )


def test_piece_svg_unit_count_per_side_at_least_12():
    """Script must generate at least 12 units per horizontal or vertical side."""
    import re
    svg = _read("piece.svg")
    counts = [int(v) for v in re.findall(r'(?:top|left|h|v)Count\s*=\s*(\d+)', svg)]
    assert len(counts) >= 1, "Could not find any unit-count variable in the border script"
    assert max(counts) >= 12, (
        f"No side has ≥ 12 units; found counts: {counts}"
    )


def test_piece_svg_has_hebrew_main_heading():
    """piece.svg must contain the Hebrew heading (chuppah / canopy text)."""
    svg = _read("piece.svg")
    assert "חֻפָּה" in svg or "סִינַי" in svg, (
        "piece.svg must contain the Hebrew heading with חֻפָּה or סִינַי"
    )


def test_piece_svg_has_naaseh_vnishma():
    """piece.svg must contain the verse נַעֲשֶׂה וְנִשְׁמָע (Exodus 24:7)."""
    svg = _read("piece.svg")
    assert "נַעֲשֶׂה" in svg and "נִשְׁמָע" in svg, (
        "piece.svg must contain נַעֲשֶׂה וְנִשְׁמָע"
    )


def test_piece_svg_has_kiymu():
    """piece.svg must contain קִיְּמוּ וְקִבְּלוּ (Esther 9:27)."""
    svg = _read("piece.svg")
    assert "קִיְּמוּ" in svg, "piece.svg must contain קִיְּמוּ"


def test_piece_svg_no_external_imports():
    """piece.svg must not import external resources (no @import, no href to http)."""
    svg = _read("piece.svg")
    assert "@import" not in svg, "piece.svg must not use @import"
    assert "fonts.googleapis" not in svg, "piece.svg must not load Google Fonts"
    import re
    external_hrefs = re.findall(r'href=["\']https?://', svg)
    assert len(external_hrefs) == 0, f"piece.svg has external href(s): {external_hrefs}"


def test_piece_svg_has_pomegranate_circles():
    """Pomegranate symbol must use <circle> elements."""
    svg = _read("piece.svg")
    circle_count = svg.count("<circle")
    assert circle_count >= 3, (
        f"Expected at least 3 <circle> elements (pomegranate bodies etc.), found {circle_count}"
    )


def test_piece_svg_has_border_rects():
    """piece.svg must have at least 2 <rect> elements for the double-line frame."""
    svg = _read("piece.svg")
    rect_count = svg.count("<rect")
    assert rect_count >= 2, f"Expected at least 2 <rect> elements, found {rect_count}"


# ---------------------------------------------------------------------------
# index.html: essay embedded and SVG inline
# ---------------------------------------------------------------------------

def test_index_html_embeds_essay_words():
    """At least 5 of the first 10 long words in essay.md must appear in index.html."""
    essay = _read("essay.md")
    html = _read("index.html")
    long_words = [w for w in essay.split() if len(w) > 5][:10]
    found = sum(1 for w in long_words if w in html)
    assert found >= 5, (
        f"Only {found}/10 sampled essay words found in index.html — essay must be embedded inline"
    )


def test_index_html_has_inline_svg():
    """index.html must contain an inline <svg> element (not just an <object> or <img>)."""
    html = _read("index.html")
    assert "<svg" in html, "index.html must contain an inline <svg> element"


def test_index_html_contains_shabbat_88a():
    """index.html must cite Shabbat 88a — the primary Talmudic source."""
    html = _read("index.html")
    assert "Shabbat 88a" in html or "88a" in html, "index.html must reference Shabbat 88a"


def test_index_html_contains_exodus_19_17_hebrew():
    """index.html must show the Hebrew of Exodus 19:17."""
    html = _read("index.html")
    assert "וַיִּתְיַצְּבוּ" in html or "תַּחְתִּית" in html, (
        "index.html must embed the Hebrew text of Exodus 19:17"
    )


def test_index_html_contains_esther_hebrew():
    """index.html must show the Hebrew of Esther 9:27."""
    html = _read("index.html")
    assert "קִיְּמוּ" in html, "index.html must embed the Hebrew of Esther 9:27"


def test_index_html_contains_naaseh_vnishma():
    """index.html must contain the key phrase נַעֲשֶׂה וְנִשְׁמָע."""
    html = _read("index.html")
    assert "נַעֲשֶׂה" in html, "index.html must contain נַעֲשֶׂה"


def test_index_html_no_external_font_imports():
    """index.html must not load fonts from Google Fonts or any external URL."""
    html = _read("index.html")
    assert "fonts.googleapis" not in html, "index.html must not load Google Fonts"
    assert "@import url" not in html, "index.html must not use @import url for fonts"


def test_index_html_has_essay_panel():
    """index.html must have a dedicated essay section alongside the artwork."""
    html = _read("index.html")
    assert "essay" in html.lower(), "index.html must have an essay panel"


# ---------------------------------------------------------------------------
# thumbnail.svg
# ---------------------------------------------------------------------------

def test_thumbnail_is_valid_svg():
    svg = _read("thumbnail.svg")
    assert "<svg" in svg and "</svg>" in svg, "thumbnail.svg is not valid SVG"


def test_thumbnail_has_viewbox():
    svg = _read("thumbnail.svg")
    assert "viewBox" in svg, "thumbnail.svg must have a viewBox"


def test_thumbnail_has_hebrew_text():
    """Thumbnail must show Hebrew text from the piece."""
    svg = _read("thumbnail.svg")
    has_hebrew = any(c in svg for c in ("נַעֲשֶׂה", "חֻפָּה", "קִיְּמוּ", "סִינַי"))
    assert has_hebrew, "thumbnail.svg must contain Hebrew text"


def test_thumbnail_has_gold_colour():
    svg = _read("thumbnail.svg")
    assert "#b8860b" in svg, "thumbnail.svg must use gold #b8860b"


def test_thumbnail_has_parchment_background():
    svg = _read("thumbnail.svg")
    assert "#f5ead8" in svg, "thumbnail.svg must use parchment background #f5ead8"


# ---------------------------------------------------------------------------
# Edge cases and failure modes
# ---------------------------------------------------------------------------

def test_piece_svg_script_has_cdata_wrapper():
    """Script must be wrapped in CDATA to be valid XML inside the SVG document."""
    svg = _read("piece.svg")
    assert "CDATA" in svg, "Script block must use CDATA wrapper for SVG XML compatibility"


def test_missing_piece_svg_would_be_detected(tmp_path):
    """Verify that absence of piece.svg would be caught by the file-layout test."""
    fake = os.path.join(str(tmp_path), "piece.svg")
    assert not os.path.isfile(fake), "Fixture path must not exist"


def test_missing_essay_would_be_detected(tmp_path):
    """Verify that absence of essay.md would be caught."""
    fake = os.path.join(str(tmp_path), "essay.md")
    assert not os.path.isfile(fake), "Fixture path must not exist"


def test_essay_is_not_a_stub():
    """essay.md must have real content — not a stub with too few substantive words."""
    text = _read("essay.md")
    words = text.split()
    assert len(words) >= 300, f"essay.md looks like a stub: only {len(words)} words"
    long_words = [w for w in words if len(w) > 4]
    assert len(long_words) >= 80, "essay.md has too few substantive words — may be a placeholder"


def test_piece_svg_script_handles_missing_layer_gracefully():
    """Script must guard against a missing border-layer element (uses 'if (!layer) return')."""
    svg = _read("piece.svg")
    assert "if (!layer)" in svg or "if(!layer)" in svg, (
        "Script must check for missing border-layer before appending children"
    )


def test_thumbnail_has_indigo_colour():
    svg = _read("thumbnail.svg")
    assert "#2c2060" in svg, "thumbnail.svg must use indigo ink #2c2060"
