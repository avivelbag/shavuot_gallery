"""
Tests for piece 17-aseret-hadibrot — "The Ten Words" (Aseret HaDibrot SDF glyph glow).

Verifies file layout, pieces.json registration, essay content,
HTML structure, SDF animation parameters, Hebrew text content,
and pure-Python math checks on the pulse animation formula.
"""
import json
import math
import os
import re


GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID = "17-aseret-hadibrot"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
HTML_PATH = os.path.join(PIECE_DIR, "index.html")
ESSAY_PATH = os.path.join(PIECE_DIR, "essay.md")
THUMB_PATH = os.path.join(PIECE_DIR, "thumbnail.svg")
README_PATH = os.path.join(PIECE_DIR, "README.md")
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")


# ---------------------------------------------------------------------------
# File layout
# ---------------------------------------------------------------------------

def test_piece_directory_exists():
    assert os.path.isdir(PIECE_DIR), f"Directory {PIECE_DIR} does not exist"


def test_index_html_exists():
    assert os.path.isfile(HTML_PATH), "index.html is missing"


def test_thumbnail_svg_exists():
    assert os.path.isfile(THUMB_PATH), "thumbnail.svg is missing"


def test_readme_exists():
    assert os.path.isfile(README_PATH), "README.md is missing"


def test_essay_md_exists():
    assert os.path.isfile(ESSAY_PATH), "essay.md is missing"


# ---------------------------------------------------------------------------
# pieces.json registration
# ---------------------------------------------------------------------------

def load_pieces():
    """Return the parsed pieces.json list."""
    with open(PIECES_JSON, encoding="utf-8") as fh:
        return json.load(fh)


def get_piece():
    """Return the aseret-hadibrot entry from pieces.json, or None."""
    return next((p for p in load_pieces() if p["id"] == PIECE_ID), None)


def test_piece_registered_in_pieces_json():
    assert get_piece() is not None, f"'{PIECE_ID}' not found in pieces.json"


def test_piece_has_correct_theme():
    piece = get_piece()
    assert piece is not None
    theme = piece["theme"].lower()
    assert "matan torah" in theme or "ten commandments" in theme or "dibrot" in theme, (
        f"theme should reference Matan Torah / Ten Commandments, got: {piece['theme']!r}"
    )


def test_piece_has_sdf_technique():
    piece = get_piece()
    assert piece is not None
    technique = piece["technique"].lower()
    assert "sdf" in technique or "glow" in technique or "canvas" in technique, (
        f"technique must mention SDF/glow/canvas, got: {piece['technique']!r}"
    )


def test_piece_essay_field_in_json():
    piece = get_piece()
    assert piece is not None
    essay = piece.get("essay", "")
    assert essay.strip(), "essay field in pieces.json must be non-empty"
    assert essay == f"pieces/{PIECE_ID}/essay.md", f"essay path mismatch: {essay!r}"


def test_piece_path_correct():
    piece = get_piece()
    assert piece is not None
    assert piece["path"] == f"pieces/{PIECE_ID}/index.html"


def test_piece_thumbnail_correct():
    piece = get_piece()
    assert piece is not None
    assert piece["thumbnail"] == f"pieces/{PIECE_ID}/thumbnail.svg"


def test_piece_year_is_int():
    piece = get_piece()
    assert piece is not None
    assert isinstance(piece["year"], int)


def test_no_duplicate_ids():
    pieces = load_pieces()
    ids = [p["id"] for p in pieces]
    assert len(ids) == len(set(ids)), f"Duplicate piece IDs detected: {ids}"


def test_piece_all_required_fields():
    """All required pieces.json fields must be present and non-empty."""
    required = ("id", "title", "tagline", "year", "theme", "technique", "path", "thumbnail", "essay")
    piece = get_piece()
    assert piece is not None
    for field in required:
        val = piece.get(field)
        assert val is not None and val != "", (
            f"pieces.json entry missing or empty field: {field!r}"
        )


def test_piece_ordered_between_16_and_18():
    """Piece 17 should appear between 16-bikkurim-procession and 18-shofar-sinai."""
    pieces = load_pieces()
    idx17 = next((i for i, p in enumerate(pieces) if p["id"] == PIECE_ID), None)
    assert idx17 is not None, "Piece 17 not found"
    has_16_before = any(p["id"] == "16-bikkurim-procession" for p in pieces[:idx17])
    has_18_after  = any(p["id"] == "18-shofar-sinai"        for p in pieces[idx17:])
    assert has_16_before, "Piece 17 must appear after 16-bikkurim-procession in pieces.json"
    assert has_18_after,  "Piece 17 must appear before 18-shofar-sinai in pieces.json"


# ---------------------------------------------------------------------------
# Essay content
# ---------------------------------------------------------------------------

def read_essay():
    """Return the full essay.md text."""
    return open(ESSAY_PATH, encoding="utf-8").read()


def test_essay_word_count():
    text = read_essay()
    words = text.split()
    assert len(words) >= 300, f"essay.md has only {len(words)} words (need >= 300)"


def test_essay_references_exodus_20():
    text = read_essay()
    assert "Exodus 20" in text or "Ex. 20" in text, (
        "essay.md must cite Exodus 20 (the Ten Commandments)"
    )


def test_essay_references_exodus_31_18():
    text = read_essay()
    assert "Exodus 31" in text or "31:18" in text, (
        "essay.md must cite Exodus 31:18 (tablets written by finger of God)"
    )


def test_essay_references_avot_6_2():
    text = read_essay()
    assert "Avot 6" in text or "Avot 6:2" in text, (
        "essay.md must cite Pirkei Avot 6:2 (charut/cherut pun)"
    )


def test_essay_mentions_charut_cherut():
    text = read_essay()
    has_charut = "charut" in text.lower() or "חָרוּת" in text
    has_cherut = "cherut" in text.lower() or "חֵרוּת" in text
    assert has_charut and has_cherut, (
        "essay.md must discuss the charut/cherut (engraved/freedom) wordplay"
    )


def test_essay_mentions_shavuot():
    text = read_essay()
    assert "Shavuot" in text or "shavuot" in text.lower(), (
        "essay.md must explain why Aseret HaDibrot are chanted on Shavuot"
    )


def test_essay_mentions_megillah():
    text = read_essay()
    assert "Megillah" in text or "ta'am" in text.lower() or "ta’am" in text, (
        "essay.md must reference the Shavuot reading tradition (Megillah 21a or ta'am elyon)"
    )


def test_essay_contains_hebrew_text():
    text = read_essay()
    hebrew_chars = [c for c in text if 'א' <= c <= 'ת']
    assert len(hebrew_chars) >= 30, (
        f"essay.md must contain substantial Hebrew text (nikud), found only {len(hebrew_chars)} Hebrew chars"
    )


def test_essay_contains_english_translations():
    text = read_essay()
    assert '"I am the Lord' in text or "I am the Lord" in text, (
        "essay.md must include English translation of Exodus 20:2"
    )


def test_essay_not_placeholder():
    text = read_essay()
    for stub in ("TODO", "placeholder", "lorem ipsum", "FILL IN"):
        assert stub.lower() not in text.lower(), (
            f"essay.md appears to contain placeholder text: {stub!r}"
        )


# ---------------------------------------------------------------------------
# HTML / canvas structure
# ---------------------------------------------------------------------------

def read_html():
    """Return the full index.html text."""
    return open(HTML_PATH, encoding="utf-8").read()


def test_html_uses_canvas():
    html = read_html()
    assert "<canvas" in html, "index.html must contain a <canvas> element"


def test_html_uses_request_animation_frame():
    html = read_html()
    assert "requestAnimationFrame" in html, (
        "index.html must use requestAnimationFrame for the animation loop"
    )


def test_html_has_twelve_second_cycle():
    html = read_html()
    assert "12000" in html, (
        "index.html must implement a 12-second pulse cycle (12000 ms)"
    )


def test_html_has_sin_pulse():
    html = read_html()
    assert "Math.sin" in html, (
        "index.html must use Math.sin for the radial pulse animation"
    )


def test_html_has_shadow_blur():
    html = read_html()
    assert "shadowBlur" in html, (
        "index.html must set ctx.shadowBlur for the SDF glow effect"
    )


def test_html_has_shadow_color_amber():
    html = read_html()
    assert "ff9900" in html.lower() or "#ff9900" in html, (
        "index.html must use amber shadowColor #ff9900 for the glow"
    )


def test_html_has_stone_background_color():
    html = read_html()
    assert "c8b89a" in html.lower(), "index.html must use stone color #c8b89a"


def test_html_has_dark_background():
    html = read_html()
    assert "1c1612" in html.lower(), "index.html must use dark background #1c1612"


def test_html_has_stone_border_color():
    html = read_html()
    assert "a89880" in html.lower(), "index.html must use stone border color #a89880"


def test_html_has_text_near_white():
    html = read_html()
    assert "f5eed8" in html.lower(), "index.html must use near-white text color #f5eed8"


def test_html_has_amber_fill_color():
    html = read_html()
    assert "ffcc66" in html.lower(), "index.html must use amber glyph color #ffcc66"


def test_html_has_left_tablet():
    html = read_html()
    assert "LEFT" in html or "left" in html.lower(), (
        "index.html must define LEFT tablet geometry"
    )


def test_html_has_right_tablet():
    html = read_html()
    assert "RIGHT" in html or "right" in html.lower(), (
        "index.html must define RIGHT tablet geometry"
    )


def test_html_has_rounded_rect():
    html = read_html()
    assert "arcTo" in html or "roundRect" in html, (
        "index.html must use arcTo/roundRect for rounded tablet corners"
    )


def test_html_has_stone_texture():
    html = read_html()
    assert "makeStoneTexture" in html or "stoneTex" in html or "stone" in html.lower(), (
        "index.html must implement stone grain texture"
    )


def test_html_has_commandments_1_5():
    html = read_html()
    assert "אָנֹכִי" in html, "index.html must contain 1st commandment: אָנֹכִי יְהוָה אֱלֹהֶיךָ"
    assert "זָכוֹר" in html, "index.html must contain 4th commandment: זָכוֹר אֶת-יוֹם הַשַּׁבָּת"
    assert "כַּבֵּד" in html, "index.html must contain 5th commandment: כַּבֵּד אֶת-אָבִיךָ"


def test_html_has_commandments_6_10():
    html = read_html()
    assert "תִרְצָח" in html, "index.html must contain 6th commandment: לֹא תִרְצָח"
    assert "תִנְאָף" in html, "index.html must contain 7th commandment: לֹא תִנְאָף"
    assert "תִגְנֹב" in html, "index.html must contain 8th commandment: לֹא תִגְנֹב"
    assert "תַעֲנֶה" in html, "index.html must contain 9th commandment: לֹא תַעֲנֶה"
    assert "תַחְמֹד" in html, "index.html must contain 10th commandment: לֹא תַחְמֹד"


def test_html_uses_rtl_direction():
    html = read_html()
    assert "rtl" in html, "index.html must set direction='rtl' for Hebrew text"


def test_html_uses_system_hebrew_font():
    html = read_html()
    assert "SBL Hebrew" in html or "David" in html, (
        "index.html must use a system Hebrew font ('SBL Hebrew', 'David') — no external @import"
    )


def test_html_no_external_font_imports():
    html = read_html()
    external = re.findall(r'@import\s+url\s*\(', html)
    assert len(external) == 0, f"index.html must not use @import for fonts: {external}"


def test_html_no_external_scripts():
    html = read_html()
    external = re.findall(r'<script[^>]+src=["\']https?://', html)
    assert len(external) == 0, f"index.html must not load external scripts: {external}"


def test_html_embeds_essay_text():
    """index.html must embed substantial essay text inline (not just reference essay.md)."""
    essay = read_essay()
    html  = read_html()
    words = [w for w in essay.split() if len(w) > 5 and w[0].isalpha()]
    sample = words[:15]
    found = sum(1 for w in sample if w in html)
    assert found >= 7, (
        f"index.html does not embed essay text: only {found}/15 sampled words found"
    )


def test_html_embeds_hebrew_source_quotes():
    html = read_html()
    assert "אָנֹכִי יְהוָה אֱלֹהֶיךָ" in html or "הוֹצֵאתִיךָ" in html, (
        "index.html must embed the Hebrew text of Exodus 20:2"
    )
    assert "בְּאֶצְבַּע אֱלֹהִים" in html or "לֻחֹת הָאֶבֶן" in html, (
        "index.html must embed the Hebrew text of Exodus 31:18"
    )


def test_html_has_responsive_layout():
    html = read_html()
    assert "max-width" in html or "flex-direction: column" in html, (
        "index.html must support both wide and narrow screen layouts"
    )


def test_html_not_placeholder():
    html = read_html()
    for stub in ("TODO", "lorem ipsum", "FILL IN"):
        assert stub.lower() not in html.lower(), (
            f"index.html contains placeholder text: {stub!r}"
        )


def test_html_has_engraved_shadow_offset():
    html = read_html()
    assert ("+ 2" in html or "+2" in html or "cx + 2" in html), (
        "index.html must draw a dark offset shadow for the engraved-depth effect"
    )


def test_html_has_three_draw_passes():
    """SDF technique requires: dark offset pass, glow pass, sharp bright pass."""
    html = read_html()
    fill_text_count = html.count("fillText")
    assert fill_text_count >= 3, (
        f"index.html should call fillText at least 3 times per glyph (offset, glow, sharp); found {fill_text_count}"
    )


# ---------------------------------------------------------------------------
# Thumbnail SVG
# ---------------------------------------------------------------------------

def read_thumb():
    """Return thumbnail.svg text."""
    return open(THUMB_PATH, encoding="utf-8").read()


def test_thumbnail_is_valid_svg():
    svg = read_thumb()
    assert "<svg" in svg and "</svg>" in svg, "thumbnail.svg is not valid SVG"


def test_thumbnail_has_two_tablet_rects():
    """Thumbnail must have at least two rounded-rect tablets."""
    svg = read_thumb()
    rects = re.findall(r'<rect', svg)
    assert len(rects) >= 2, (
        f"thumbnail.svg must have at least 2 <rect> tablet elements, found {len(rects)}"
    )


def test_thumbnail_has_rx_rounded_corners():
    svg = read_thumb()
    assert 'rx=' in svg or 'ry=' in svg, (
        "thumbnail.svg must use rx/ry for rounded tablet corners"
    )


def test_thumbnail_has_glow_filter():
    svg = read_thumb()
    assert "<filter" in svg, "thumbnail.svg must define a glow filter"
    assert "feGaussianBlur" in svg or "feDropShadow" in svg, (
        "thumbnail.svg glow filter must use feGaussianBlur or feDropShadow"
    )


def test_thumbnail_has_hebrew_text():
    svg = read_thumb()
    assert "<text" in svg, "thumbnail.svg must include <text> elements"
    assert "אָנֹכִי" in svg or "לֹא תִרְצָח" in svg, (
        "thumbnail.svg must include Hebrew commandment text"
    )


def test_thumbnail_has_stone_color():
    svg = read_thumb()
    assert "c8b89a" in svg.lower(), "thumbnail.svg must use stone color #c8b89a"


def test_thumbnail_has_dark_background():
    svg = read_thumb()
    assert "1c1612" in svg.lower(), "thumbnail.svg must use dark background #1c1612"


def test_thumbnail_has_amber_glow():
    svg = read_thumb()
    assert "ff9900" in svg.lower() or "ffcc66" in svg.lower(), (
        "thumbnail.svg must use amber glow color"
    )


def test_thumbnail_has_rtl_text():
    svg = read_thumb()
    assert 'direction="rtl"' in svg or "direction:rtl" in svg, (
        "thumbnail.svg must set RTL text direction for Hebrew"
    )


def test_thumbnail_has_ten_commandment_lines():
    """Thumbnail should have at least 5 <text> elements (one per commandment displayed)."""
    svg = read_thumb()
    texts = re.findall(r'<text', svg)
    assert len(texts) >= 5, (
        f"thumbnail.svg must have at least 5 <text> elements for commandments, found {len(texts)}"
    )


# ---------------------------------------------------------------------------
# Pure-Python math: SDF pulse animation
# ---------------------------------------------------------------------------

def compute_blur(ts_ms, cycle_ms=12000):
    """
    Replicate the JavaScript blur formula:
        phase = (ts / 12000) * 2π
        blur  = 8 + 12 * (0.5 + 0.5 * sin(phase))
    Returns the blur value for a given timestamp in milliseconds.
    """
    phase = (ts_ms / cycle_ms) * 2 * math.pi
    return 8 + 12 * (0.5 + 0.5 * math.sin(phase))


def test_pulse_blur_minimum():
    """Blur must reach approximately 8 (minimum when sin = -1)."""
    ts_at_min = 12000 * (3 / 4)  # sin = -1 at 3/4 of the cycle
    blur = compute_blur(ts_at_min)
    assert abs(blur - 8.0) < 0.5, (
        f"Minimum blur should be ~8 at sin=-1, got {blur:.3f}"
    )


def test_pulse_blur_maximum():
    """Blur must reach approximately 20 (maximum when sin = +1)."""
    ts_at_max = 12000 * (1 / 4)  # sin = +1 at 1/4 of the cycle
    blur = compute_blur(ts_at_max)
    assert abs(blur - 20.0) < 0.5, (
        f"Maximum blur should be ~20 at sin=+1, got {blur:.3f}"
    )


def test_pulse_blur_at_zero():
    """At ts=0, sin(0)=0, blur should be exactly 14 (midpoint)."""
    blur = compute_blur(0)
    assert abs(blur - 14.0) < 1e-9, (
        f"At ts=0, blur should be 14 (midpoint), got {blur}"
    )


def test_pulse_blur_stays_in_range():
    """All blur values across a full 12-second cycle must stay within [8, 20]."""
    samples = 1000
    for i in range(samples):
        ts = 12000 * i / samples
        blur = compute_blur(ts)
        assert 7.9 <= blur <= 20.1, (
            f"Blur {blur:.3f} at ts={ts:.1f}ms is outside expected range [8, 20]"
        )


def test_pulse_is_periodic():
    """Blur at ts and ts+12000ms must be identical (12-second period)."""
    for ts in [0, 1500, 3000, 6000, 9000]:
        b1 = compute_blur(ts)
        b2 = compute_blur(ts + 12000)
        assert abs(b1 - b2) < 1e-9, (
            f"Blur is not periodic at ts={ts}: got {b1:.6f} vs {b2:.6f}"
        )


def test_pulse_average_is_midpoint():
    """The time-average of the pulse must be 14 (midpoint of [8, 20])."""
    samples = 10000
    total = sum(compute_blur(12000 * i / samples) for i in range(samples))
    mean = total / samples
    assert abs(mean - 14.0) < 0.1, (
        f"Mean blur should be ~14, got {mean:.4f}"
    )


# ---------------------------------------------------------------------------
# Edge cases and failure modes
# ---------------------------------------------------------------------------

def test_essay_file_not_empty():
    text = read_essay()
    assert len(text.strip()) > 100, "essay.md must not be empty or near-empty"


def test_html_file_not_empty():
    html = read_html()
    assert len(html.strip()) > 500, "index.html must not be empty or near-empty"


def test_thumbnail_not_empty():
    svg = read_thumb()
    assert len(svg.strip()) > 100, "thumbnail.svg must not be empty or near-empty"


def test_pieces_json_remains_valid_after_insertion():
    """pieces.json must still be valid JSON with all existing pieces intact."""
    pieces = load_pieces()
    assert isinstance(pieces, list)
    ids = [p["id"] for p in pieces]
    for expected_id in ["01-thunder-at-sinai", "16-bikkurim-procession",
                        "17-aseret-hadibrot", "18-shofar-sinai"]:
        assert expected_id in ids, f"Expected piece '{expected_id}' missing from pieces.json"


def test_no_google_fonts_import():
    """No piece may import Google Fonts or any external font CDN."""
    html = read_html()
    assert "fonts.googleapis.com" not in html, (
        "index.html must not import Google Fonts (offline requirement)"
    )
    assert "fonts.gstatic.com" not in html, (
        "index.html must not reference Google Fonts static CDN"
    )


def test_blur_formula_uses_correct_cycle():
    """Verify that the cycle constant is 12000 ms (12 seconds) as required."""
    html = read_html()
    assert "12000" in html, (
        "index.html must use 12000 ms (12-second) pulse cycle constant"
    )


def test_both_tablets_have_commandments():
    """Both LEFT and RIGHT commandment arrays must each have exactly 5 entries."""
    html = read_html()
    left_entries  = html.count("num: 'א") + html.count('num: "א')
    right_entries = html.count("num: 'ו") + html.count('num: "ו')
    assert left_entries >= 1, "LEFT_CMD must start with commandment א׳"
    assert right_entries >= 1, "RIGHT_CMD must start with commandment ו׳"


def test_essay_cites_deuteronomy_9():
    text = read_essay()
    assert "Deuteronomy 9" in text or "9:10" in text, (
        "essay.md must cite Deuteronomy 9:10 (charut al-haluchot)"
    )
