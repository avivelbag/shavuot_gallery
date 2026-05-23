"""Tests for piece 92-domain-coloring-seventy-faces."""
import json
import os
import re

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")
PIECE_ID = "92-domain-coloring-seventy-faces"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)


def _load_piece():
    with open(PIECES_JSON, encoding="utf-8") as fh:
        pieces = json.load(fh)
    for p in pieces:
        if p["id"] == PIECE_ID:
            return p
    return None


def _html():
    return open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()


def _essay():
    return open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()


# ---------------------------------------------------------------------------
# pieces.json registration
# ---------------------------------------------------------------------------

def test_piece_registered_in_json():
    piece = _load_piece()
    assert piece is not None, f"Piece '{PIECE_ID}' not found in pieces.json"


def test_piece_required_fields_present():
    piece = _load_piece()
    for field in ("id", "title", "tagline", "year", "theme", "technique", "path", "thumbnail", "essay"):
        assert field in piece and piece[field], f"Field '{field}' missing or empty"


def test_piece_theme_mentions_seventy_faces():
    piece = _load_piece()
    theme = piece["theme"].lower()
    assert "shivim" in theme or "panim" in theme or "seventy" in theme or "70" in theme, (
        "theme should reference 'shivim panim' or seventy faces"
    )


def test_piece_technique_mentions_domain_coloring():
    piece = _load_piece()
    assert "domain coloring" in piece["technique"].lower(), (
        "technique must mention 'domain coloring'"
    )


def test_piece_technique_mentions_z70():
    piece = _load_piece()
    tech = piece["technique"]
    assert "z^70" in tech or "z70" in tech.lower() or "z⁷⁰" in tech, (
        "technique must reference the z^70 function"
    )


# ---------------------------------------------------------------------------
# File layout
# ---------------------------------------------------------------------------

def test_index_html_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "index.html"))


def test_essay_md_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "essay.md"))


def test_readme_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "README.md"))


def test_thumbnail_exists():
    thumb = os.path.join(PIECE_DIR, "thumbnail.svg")
    assert os.path.isfile(thumb), "thumbnail.svg must exist"


def test_thumbnail_is_valid_svg():
    thumb = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert "<svg" in thumb and "</svg>" in thumb, "thumbnail.svg must be valid SVG"


def test_thumbnail_has_seventy_wedges():
    """The SVG thumbnail must contain 70 colored wedge paths."""
    thumb = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    paths = re.findall(r'<path[^>]+>', thumb)
    assert len(paths) == 70, f"Expected 70 wedge paths, found {len(paths)}"


def test_thumbnail_has_root_dots():
    """The SVG must include dark dot markers for the 70 roots of unity."""
    thumb = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    circles = re.findall(r'<circle[^>]+>', thumb)
    # center disk + 70 root dots = 71 total
    assert len(circles) >= 70, f"Expected ≥70 root-dot circles, found {len(circles)}"


# ---------------------------------------------------------------------------
# essay.md content
# ---------------------------------------------------------------------------

def test_essay_word_count():
    text = _essay()
    assert len(text.split()) >= 300, "essay.md must have at least 300 words"


def test_essay_cites_bamidbar_rabbah():
    text = _essay().lower()
    assert "bamidbar rabbah" in text or "במדבר רבה" in text, (
        "essay must cite Bamidbar Rabbah 13:15"
    )


def test_essay_mentions_seventy_faces():
    text = _essay().lower()
    assert "seventy faces" in text or "70 faces" in text or "שבעים פנים" in text, (
        "essay must discuss the 'seventy faces' of Torah"
    )


def test_essay_mentions_roots_of_unity():
    text = _essay().lower()
    assert "roots of unity" in text or "root of unity" in text, (
        "essay must explain the 70th roots of unity"
    )


def test_essay_mentions_sanhedrin():
    text = _essay().lower()
    assert "sanhedrin" in text, "essay must reference Sanhedrin 34a"


def test_essay_mentions_exodus():
    text = _essay().lower()
    assert "exodus" in text, "essay must reference Exodus 24 (seventy elders)"


# ---------------------------------------------------------------------------
# index.html — algorithm and animation
# ---------------------------------------------------------------------------

def test_html_uses_imagdata_pixel_loop():
    html = _html()
    assert "createImageData" in html, "must use ImageData for pixel-level rendering"
    assert "putImageData" in html, "must call putImageData to flush pixels to canvas"


def test_html_uses_requestanimationframe():
    html = _html()
    assert "requestAnimationFrame" in html, "animation must use requestAnimationFrame"


def test_html_computes_z70_via_repeated_squaring():
    """The implementation must use repeated squaring (cpow70 or equivalent)."""
    html = _html()
    assert "cpow70" in html or "z64" in html or "z^70" in html.lower() or "pow70" in html, (
        "must implement z^70 via repeated squaring"
    )


def test_html_uses_atan2_for_argument():
    html = _html()
    assert "atan2" in html, "hue must be derived from Math.atan2 (argument of f(z))"


def test_html_has_modular_shading():
    """Modular shading requires Math.log and Math.sin together."""
    html = _html()
    assert "Math.log" in html and "Math.sin" in html, (
        "modular shading requires Math.log and Math.sin"
    )


def test_html_has_rotation_animation():
    """Rotation is implemented by multiplying z by e^{-i*theta}."""
    html = _html()
    assert "theta" in html or "DTHETA" in html or "cosT" in html, (
        "animation must use a phase angle (theta) for rotation"
    )


def test_html_darkens_roots():
    """Near-zero pixels should be darkened (|f(z)| < threshold)."""
    html = _html()
    assert "0.05" in html or "< 0.05" in html or "mag <" in html.lower(), (
        "pixels near roots (|f(z)| < 0.05) must be darkened"
    )


def test_html_hsl_saturation_085():
    html = _html()
    assert "0.85" in html, "saturation must be 0.85"


def test_html_embeds_essay_text():
    """index.html must embed enough of the essay to pass the gallery's inline-text check."""
    essay = _essay()
    html = _html()
    words = [w for w in essay.split() if len(w) > 5][:15]
    found = sum(1 for w in words if w in html)
    assert found >= 8, (
        f"index.html must embed essay text inline (found {found}/15 sampled words)"
    )


def test_html_view_window_scale_3():
    """The view window spans [-1.5, 1.5], requiring a scale factor of 3."""
    html = _html()
    assert "scale = 3" in html or "* 3" in html or "scale=3" in html or "3.0" in html, (
        "view window must cover [-1.5, 1.5]x[-1.5, 1.5] (scale 3)"
    )


# ---------------------------------------------------------------------------
# Edge cases and failure modes
# ---------------------------------------------------------------------------

def test_piece_id_not_duplicated():
    with open(PIECES_JSON, encoding="utf-8") as fh:
        pieces = json.load(fh)
    ids = [p["id"] for p in pieces]
    assert ids.count(PIECE_ID) == 1, f"Piece ID '{PIECE_ID}' appears more than once"


def test_thumbnail_path_in_json_matches_disk():
    piece = _load_piece()
    full = os.path.join(GALLERY_ROOT, piece["thumbnail"])
    assert os.path.isfile(full), f"thumbnail path in JSON points to missing file: {full}"


def test_essay_path_in_json_matches_disk():
    piece = _load_piece()
    full = os.path.join(GALLERY_ROOT, piece["essay"])
    assert os.path.isfile(full), f"essay path in JSON points to missing file: {full}"


def test_html_path_in_json_matches_disk():
    piece = _load_piece()
    full = os.path.join(GALLERY_ROOT, piece["path"])
    assert os.path.isfile(full), f"path in JSON points to missing file: {full}"


def test_thumbnail_svg_has_dark_background():
    thumb = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert "rect" in thumb, "thumbnail must have a background rect"
    assert "#060610" in thumb or "fill=\"#0" in thumb, "background must be near-black"
