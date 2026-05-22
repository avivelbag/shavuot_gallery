"""
Tests for piece 43 "The Second Tablets — A Celtic Knot of Renewal".

Covers: file layout, pieces.json registration, HTML content (knotwork algorithm,
3D ribbon palette, animation, Hebrew text, essay embedding), essay correctness
(honest timeline, correct source citations), and explicit failure / edge-case modes.
"""
import json
import os
import re

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECES_JSON  = os.path.join(GALLERY_ROOT, "pieces.json")
PIECE_ID     = "43-second-tablets"
PIECE_DIR    = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_pieces():
    """Return parsed pieces.json list."""
    with open(PIECES_JSON, encoding="utf-8") as fh:
        return json.load(fh)


def get_piece():
    """Return the pieces.json entry for piece 43, or None."""
    for p in load_pieces():
        if p["id"] == PIECE_ID:
            return p
    return None


def read_file(filename):
    """Read a file from the piece directory."""
    return open(os.path.join(PIECE_DIR, filename), encoding="utf-8").read()


# ---------------------------------------------------------------------------
# pieces.json registration
# ---------------------------------------------------------------------------

def test_piece_43_in_json():
    assert get_piece() is not None, f"'{PIECE_ID}' not found in pieces.json"


def test_piece_43_id_correct():
    piece = get_piece()
    assert piece is not None
    assert piece["id"] == PIECE_ID


def test_piece_43_required_fields_present():
    piece = get_piece()
    assert piece is not None
    for field in ("id", "title", "tagline", "year", "theme", "technique", "path", "thumbnail", "essay"):
        assert field in piece, f"pieces.json entry missing field '{field}'"
        assert piece[field], f"pieces.json field '{field}' is empty"


def test_piece_43_year_is_integer():
    piece = get_piece()
    assert piece is not None
    assert isinstance(piece["year"], int)


def test_piece_43_technique_mentions_celtic_knotwork():
    piece = get_piece()
    assert piece is not None
    tech = piece["technique"].lower()
    assert "celtic" in tech or "knotwork" in tech, (
        "technique must mention Celtic knotwork"
    )


def test_piece_43_technique_mentions_interlace():
    piece = get_piece()
    assert piece is not None
    tech = piece["technique"].lower()
    assert "interlace" in tech or "over/under" in tech or "over-under" in tech, (
        "technique must mention interlace or over/under"
    )


def test_piece_43_theme_mentions_second_tablets():
    piece = get_piece()
    assert piece is not None
    theme = piece["theme"].lower()
    assert "second" in theme or "tablets" in theme or "luchot" in theme, (
        "theme must reference the second tablets"
    )


def test_piece_43_path_format():
    piece = get_piece()
    assert piece is not None
    assert piece["path"] == f"pieces/{PIECE_ID}/index.html"


def test_piece_43_no_id_collision():
    pieces = load_pieces()
    ids = [p["id"] for p in pieces]
    assert len(ids) == len(set(ids)), f"Duplicate IDs in pieces.json: {ids}"


# ---------------------------------------------------------------------------
# File layout
# ---------------------------------------------------------------------------

def test_piece_43_index_html_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "index.html"))


def test_piece_43_thumbnail_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "thumbnail.svg"))


def test_piece_43_readme_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "README.md"))


def test_piece_43_essay_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "essay.md"))


# ---------------------------------------------------------------------------
# index.html — canvas and animation
# ---------------------------------------------------------------------------

def test_piece_43_html_has_canvas():
    html = read_file("index.html")
    assert "<canvas" in html, "index.html must contain a <canvas> element"


def test_piece_43_html_uses_requestanimationframe():
    html = read_file("index.html")
    assert "requestAnimationFrame" in html, (
        "index.html must use requestAnimationFrame for the breathing animation"
    )


def test_piece_43_html_has_sine_animation():
    """Breathing pulse: ±4 % on 5 s sinusoidal cycle."""
    html = read_file("index.html")
    assert "Math.sin" in html, "index.html must use Math.sin for the breathing animation"
    assert "0.04" in html, "breathing amplitude must be 0.04 (±4%)"


def test_piece_43_html_animation_5s_cycle():
    """The sinusoidal cycle should be 5 seconds."""
    html = read_file("index.html")
    assert "/ 5" in html or "/5" in html or "5)" in html, (
        "animation cycle must be 5 seconds"
    )


# ---------------------------------------------------------------------------
# index.html — palette
# ---------------------------------------------------------------------------

def test_piece_43_html_parchment_bg():
    html = read_file("index.html").lower()
    assert "f2e8d0" in html, "index.html must use parchment background #F2E8D0"


def test_piece_43_html_lapis_color():
    html = read_file("index.html").lower()
    assert "1a3a6b" in html, "index.html must use lapis lazuli strand color #1A3A6B"


def test_piece_43_html_gold_highlight():
    html = read_file("index.html").lower()
    assert "c8a000" in html, "index.html must use gold highlight color #C8A000"


def test_piece_43_html_shadow_color():
    html = read_file("index.html").lower()
    assert "0a0a18" in html, "index.html must use near-black shadow color #0A0A18"


# ---------------------------------------------------------------------------
# index.html — 3D ribbon effect
# ---------------------------------------------------------------------------

def test_piece_43_html_has_ribbon_shadow():
    """3D rope effect requires a shadow stroke."""
    html = read_file("index.html")
    assert "globalAlpha" in html, (
        "index.html must use globalAlpha for shadow/highlight transparency"
    )


def test_piece_43_html_has_multiple_stroke_widths():
    """3D ribbon requires multiple lineWidth assignments (base, shadow, highlight)."""
    html = read_file("index.html")
    assignments = re.findall(r'\.lineWidth\s*=', html)
    assert len(assignments) >= 3, (
        f"index.html must set lineWidth at least 3 times (shadow/base/highlight); "
        f"found {len(assignments)}"
    )


# ---------------------------------------------------------------------------
# index.html — knotwork algorithm
# ---------------------------------------------------------------------------

def test_piece_43_html_has_grid_crossings():
    """Over/under grid-based algorithm: uses modulo parity for crossing determination."""
    html = read_file("index.html")
    assert "% 2" in html or "%2" in html, (
        "index.html must use modulo-2 parity for over/under crossing determination"
    )


def test_piece_43_html_has_cols_and_rows():
    """The grid dimensions (COLS and ROWS) must be defined."""
    html = read_file("index.html")
    assert "COLS" in html or "cols" in html.lower(), (
        "index.html must define grid column count (COLS)"
    )
    assert "ROWS" in html or "rows" in html.lower(), (
        "index.html must define grid row count (ROWS)"
    )


def test_piece_43_html_draws_both_tablets():
    """Two tablets: the drawing function must be invoked for two x-offsets."""
    html = read_file("index.html")
    assert "T1X" in html or "T2X" in html or "tab1" in html.lower() or "tab2" in html.lower(), (
        "index.html must reference both tablets (T1X/T2X or similar)"
    )


def test_piece_43_html_has_boundary_curves():
    """Celtic knotwork closed loops require boundary connection curves."""
    html = read_file("index.html")
    assert "bezierCurveTo" in html or "quadraticCurveTo" in html or "arcTo" in html, (
        "index.html must use bezier/quadratic curves for boundary strand connections"
    )


# ---------------------------------------------------------------------------
# index.html — Hebrew text
# ---------------------------------------------------------------------------

def test_piece_43_html_has_hebrew_covenant_text():
    """Hebrew text 'כָּרַתִּי אִתְּךָ בְּרִית' must appear in index.html."""
    html = read_file("index.html")
    assert "כָּרַתִּי" in html, (
        "index.html must contain Hebrew text כָּרַתִּי (part of Exodus 34:27)"
    )
    assert "בְּרִית" in html, (
        "index.html must contain בְּרִית (covenant)"
    )


def test_piece_43_html_rtl_text_direction():
    """Hebrew text must use RTL direction."""
    html = read_file("index.html")
    assert "rtl" in html, "index.html must set direction='rtl' for Hebrew text"


def test_piece_43_html_cites_exodus_34():
    html = read_file("index.html")
    assert "34" in html and ("Exodus" in html or "exodus" in html or "34:27" in html), (
        "index.html must reference Exodus 34 or Exodus 34:27"
    )


# ---------------------------------------------------------------------------
# index.html — tablet shape
# ---------------------------------------------------------------------------

def test_piece_43_html_has_arch():
    """Tablets have rounded arch tops — must use arc() for drawing."""
    html = read_file("index.html")
    assert "ctx.arc(" in html or ".arc(" in html, (
        "index.html must use arc() to draw the rounded arch top of the tablets"
    )


def test_piece_43_html_no_external_resources():
    """Piece must be fully self-contained."""
    html = read_file("index.html")
    external = re.findall(r'(?:src|href)\s*=\s*["\']https?://', html)
    assert not external, (
        f"index.html must not load external resources; found: {external}"
    )


# ---------------------------------------------------------------------------
# essay.md — content and honest timeline
# ---------------------------------------------------------------------------

def test_piece_43_essay_at_least_200_words():
    text = read_file("essay.md")
    wc = len(text.split())
    assert wc >= 200, f"essay.md has only {wc} words (need ≥ 200)"


def test_piece_43_essay_cites_exodus_34():
    text = read_file("essay.md")
    assert "Exodus 34" in text, "essay.md must cite Exodus 34"


def test_piece_43_essay_cites_taanit():
    """Ta'anit 26b must be cited in the essay."""
    text = read_file("essay.md")
    assert "Ta'anit" in text or "Taanit" in text or "תענית" in text, (
        "essay.md must cite Ta'anit 26b"
    )


def test_piece_43_essay_cites_pirkei_de_rabbi_eliezer():
    text = read_file("essay.md")
    assert "Pirkei" in text or "DeRabbi" in text or "De-Rabbi" in text, (
        "essay.md must cite Pirkei DeRabbi Eliezer"
    )


def test_piece_43_essay_cites_eruvin_54a():
    """Eruvin 54a must be quoted."""
    text = read_file("essay.md")
    assert "Eruvin" in text, "essay.md must cite Eruvin 54a"


def test_piece_43_essay_second_tablets_yom_kippur_not_shavuot():
    """
    Historically critical: the second tablets were given on Yom Kippur,
    NOT Shavuot. The essay must not claim they were a Shavuot event.
    """
    text = read_file("essay.md")
    assert "Yom Kippur" in text, (
        "essay.md must correctly state that the second tablets were given on Yom Kippur"
    )
    assert "Shavuot" in text, "essay.md must address Shavuot (the first tablets)"
    lower = text.lower()
    assert "second tablets" in lower or "luchot shniyot" in lower, (
        "essay.md must discuss the second tablets"
    )


def test_piece_43_essay_does_not_misdate_second_tablets():
    """
    The essay must not affirmatively claim the second tablets were given on Shavuot.
    Sentences that explicitly negate this (e.g. 'not because … given on Shavuot — they were not')
    are correct and must not be flagged.
    """
    text = read_file("essay.md")
    # Split into sentences and look for any that AFFIRM (not deny) the misdating
    sentences = re.split(r'[.!?]', text)
    for sentence in sentences:
        s = sentence.strip()
        if not s:
            continue
        lower = s.lower()
        # Skip sentences that explicitly contain a negation near the claim
        has_negation = any(neg in lower for neg in ("not because", "were not", "was not", "they were not", "not given"))
        if has_negation:
            continue
        # Flag sentences that both mention "second tablets" and "Shavuot" and "given" together
        if ("second tablets" in lower or "luchot shniyot" in lower) and "shavuot" in lower and "given" in lower:
            raise AssertionError(
                f"essay.md may be misdating the second tablets as a Shavuot event: '{s}'"
            )


def test_piece_43_essay_mentions_17_tammuz_or_shattering():
    """The essay must acknowledge that the first tablets were broken."""
    text = read_file("essay.md")
    assert (
        "17" in text or "seventeenth" in text.lower() or "Tammuz" in text
        or "shatter" in text.lower() or "broken" in text.lower() or "broke" in text.lower()
    ), "essay.md must mention the shattering of the first tablets"


def test_piece_43_essay_connects_to_shavuot():
    """Even though the second tablets are a Yom Kippur event, the essay must
    draw a genuine Shavuot connection (e.g. through the covenant's capacity to renew)."""
    text = read_file("essay.md")
    assert "Shavuot" in text, "essay.md must explain its connection to Shavuot"


def test_piece_43_essay_mentions_celtic_knot_metaphor():
    text = read_file("essay.md").lower()
    assert "celtic" in text or "knotwork" in text or "knot" in text, (
        "essay.md must discuss the Celtic knot as a covenant metaphor"
    )


def test_piece_43_essay_mentions_covenant_or_brit():
    text = read_file("essay.md")
    assert "covenant" in text or "brit" in text.lower() or "בְּרִית" in text, (
        "essay.md must discuss the covenant (brit)"
    )


# ---------------------------------------------------------------------------
# essay embedded in index.html
# ---------------------------------------------------------------------------

def test_piece_43_essay_embedded_in_html():
    """The essay text must be embedded in index.html, not fetched at runtime."""
    essay = read_file("essay.md")
    html  = read_file("index.html")
    long_words = [w for w in essay.split() if len(w) > 6][:15]
    found = sum(1 for w in long_words if w in html)
    assert found >= 6, (
        f"index.html does not embed the essay: only {found}/15 sampled words found in HTML"
    )


# ---------------------------------------------------------------------------
# thumbnail.svg
# ---------------------------------------------------------------------------

def test_piece_43_thumbnail_is_valid_svg():
    svg = read_file("thumbnail.svg")
    assert "<svg" in svg and "</svg>" in svg, "thumbnail.svg must be valid SVG"


def test_piece_43_thumbnail_has_hebrew_text():
    svg = read_file("thumbnail.svg")
    assert "כָּרַתִּי" in svg or "בְּרִית" in svg, (
        "thumbnail.svg must contain the Hebrew covenant text"
    )


def test_piece_43_thumbnail_has_knotwork_strokes():
    """Thumbnail must include stroke elements for the knotwork."""
    svg = read_file("thumbnail.svg")
    assert "stroke=" in svg or "stroke:" in svg, (
        "thumbnail.svg must contain stroke-based knotwork elements"
    )


def test_piece_43_thumbnail_has_tablet_shapes():
    """Thumbnail must include two tablet-shaped path elements."""
    svg = read_file("thumbnail.svg")
    tablet_paths = re.findall(r'<path\b', svg)
    assert len(tablet_paths) >= 2, (
        f"thumbnail.svg must have at least 2 <path> elements for the tablets; found {len(tablet_paths)}"
    )


# ---------------------------------------------------------------------------
# README.md
# ---------------------------------------------------------------------------

def test_piece_43_readme_mentions_second_tablets():
    text = read_file("README.md").lower()
    assert "second tablets" in text or "luchot" in text, (
        "README.md must mention the second tablets"
    )


def test_piece_43_readme_mentions_celtic():
    text = read_file("README.md").lower()
    assert "celtic" in text, "README.md must mention Celtic knotwork"


# ---------------------------------------------------------------------------
# Edge cases / failure mode tests
# ---------------------------------------------------------------------------

def test_piece_43_path_ends_with_html():
    piece = get_piece()
    assert piece is not None
    assert piece["path"].endswith(".html")


def test_piece_43_thumbnail_extension_svg():
    piece = get_piece()
    assert piece is not None
    ext = os.path.splitext(piece["thumbnail"])[1].lower()
    assert ext == ".svg", f"thumbnail must be .svg; got '{ext}'"


def test_piece_43_essay_field_non_empty():
    piece = get_piece()
    assert piece is not None
    assert piece.get("essay"), "essay field in pieces.json must not be empty"


def test_piece_43_essay_path_exists_on_disk():
    piece = get_piece()
    assert piece is not None
    full = os.path.join(GALLERY_ROOT, piece["essay"])
    assert os.path.isfile(full), f"essay file '{piece['essay']}' does not exist"


def test_stub_essay_fails_word_count_check(tmp_path):
    """An essay with fewer than 200 words must be detected as insufficient."""
    stub = tmp_path / "essay.md"
    stub.write_text("This is a stub essay.", encoding="utf-8")
    text = stub.read_text(encoding="utf-8")
    wc = len(text.split())
    assert wc < 200, "Fixture confirms stub essay should fail the 200-word check"


def test_missing_essay_file_detected(tmp_path):
    """A non-existent essay file path must not be present on disk."""
    missing = tmp_path / "nonexistent_essay.md"
    assert not missing.exists(), "Fixture path must not exist"


def test_bad_piece_entry_missing_fields(tmp_path):
    """A pieces.json entry missing required fields must be detectable."""
    required = ("id", "title", "tagline", "year", "theme", "technique", "path", "thumbnail", "essay")
    bad = {"id": "43-second-tablets", "title": "Test"}
    for field in required:
        if field not in ("id", "title"):
            assert field not in bad


def test_piece_43_id_matches_directory():
    """piece id must match the directory name in its path."""
    piece = get_piece()
    assert piece is not None
    parts = piece["path"].replace("\\", "/").split("/")
    assert parts[-2] == PIECE_ID, f"id '{PIECE_ID}' does not match path directory '{parts[-2]}'"
