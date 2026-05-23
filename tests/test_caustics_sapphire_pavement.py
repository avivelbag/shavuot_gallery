"""Tests for piece 77-caustics-sapphire-pavement."""
import json
import os
import re

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID = "77-caustics-sapphire-pavement"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
INDEX_HTML = os.path.join(PIECE_DIR, "index.html")
ESSAY_MD = os.path.join(PIECE_DIR, "essay.md")
THUMBNAIL_SVG = os.path.join(PIECE_DIR, "thumbnail.svg")
README_MD = os.path.join(PIECE_DIR, "README.md")
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")


def load_pieces():
    with open(PIECES_JSON, encoding="utf-8") as fh:
        return json.load(fh)


def get_piece():
    return next((p for p in load_pieces() if p["id"] == PIECE_ID), None)


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


# ---------------------------------------------------------------------------
# File existence — happy path
# ---------------------------------------------------------------------------

def test_piece_directory_exists():
    assert os.path.isdir(PIECE_DIR), f"Piece directory missing: {PIECE_DIR}"


def test_index_html_exists():
    assert os.path.isfile(INDEX_HTML), "index.html is missing"


def test_essay_md_exists():
    assert os.path.isfile(ESSAY_MD), "essay.md is missing"


def test_thumbnail_svg_exists():
    assert os.path.isfile(THUMBNAIL_SVG), "thumbnail.svg is missing"


def test_readme_md_exists():
    assert os.path.isfile(README_MD), "README.md is missing"


# ---------------------------------------------------------------------------
# pieces.json registration
# ---------------------------------------------------------------------------

def test_piece_registered_in_pieces_json():
    piece = get_piece()
    assert piece is not None, f"Piece '{PIECE_ID}' not found in pieces.json"


def test_piece_theme_is_har_sinai():
    piece = get_piece()
    assert piece is not None
    assert piece["theme"] == "Har Sinai", f"Expected theme 'Har Sinai', got {piece['theme']!r}"


def test_piece_technique_contains_caustics():
    piece = get_piece()
    assert piece is not None
    assert "caustics" in piece["technique"].lower(), (
        f"Expected 'caustics' in technique, got: {piece['technique']!r}"
    )


def test_piece_technique_contains_ray_refraction():
    piece = get_piece()
    assert piece is not None
    assert "ray refraction" in piece["technique"].lower(), (
        f"Expected 'ray refraction' in technique, got: {piece['technique']!r}"
    )


def test_piece_technique_contains_height_field():
    piece = get_piece()
    assert piece is not None
    assert "height-field" in piece["technique"].lower(), (
        f"Expected 'height-field' in technique, got: {piece['technique']!r}"
    )


# ---------------------------------------------------------------------------
# index.html — caustics simulation parameters
# ---------------------------------------------------------------------------

def test_index_html_declares_n_120():
    """N=120 must be set in the JS code."""
    html = read(INDEX_HTML)
    assert re.search(r'\bN\s*=\s*120\b', html), "N=120 not found in index.html"


def test_index_html_declares_height_field_params():
    """Height field constants A, f1, f2, f3 must appear."""
    html = read(INDEX_HTML)
    assert re.search(r'\bA\s*=\s*0\.08\b', html), "A=0.08 not found"
    assert re.search(r'\bf1\s*=\s*4\.0\b', html), "f1=4.0 not found"
    assert re.search(r'\bf2\s*=\s*4\.0\b', html), "f2=4.0 not found"
    assert re.search(r'\bf3\s*=\s*2\.8\b', html), "f3=2.8 not found"


def test_index_html_declares_phase_increments():
    """Per-frame phase increments dp1, dp2, dp3 must appear."""
    html = read(INDEX_HTML)
    assert re.search(r'dp1\s*=\s*0\.012', html), "dp1=0.012 not found"
    assert re.search(r'dp2\s*=\s*0\.015', html), "dp2=0.015 not found"
    assert re.search(r'dp3\s*=\s*0\.009', html), "dp3=0.009 not found"


def test_index_html_uses_float32array():
    """Float32Array accumulation buffer must be used."""
    html = read(INDEX_HTML)
    assert "Float32Array" in html, "Float32Array not found in index.html"


def test_index_html_uses_requestanimationframe():
    """Animation must use requestAnimationFrame."""
    html = read(INDEX_HTML)
    assert "requestAnimationFrame" in html, "requestAnimationFrame not found"


def test_index_html_has_imagesmoothing_enabled():
    """Upscale must use imageSmoothingEnabled=true."""
    html = read(INDEX_HTML)
    assert "imageSmoothingEnabled" in html, "imageSmoothingEnabled not found"


def test_index_html_has_sapphire_color():
    """Deep sapphire color #0D1B6B must be referenced."""
    html = read(INDEX_HTML)
    assert re.search(r'0[Dd]1[Bb]6[Bb]', html), "#0D1B6B not found in index.html"


def test_index_html_has_ice_white_color():
    """Ice white color #E8F4FF must be referenced."""
    html = read(INDEX_HTML)
    assert re.search(r'[Ee]8[Ff]4[Ff]{2}', html), "#E8F4FF not found in index.html"


def test_index_html_has_eta():
    """Refraction factor eta must appear."""
    html = read(INDEX_HTML)
    assert re.search(r'\beta\s*=\s*0\.33\b', html), "eta=0.33 not found in index.html"


def test_index_html_embeds_essay_content():
    """index.html must embed meaningful essay text (not fetch it at runtime)."""
    essay = read(ESSAY_MD)
    html = read(INDEX_HTML)
    words = [w for w in essay.split() if len(w) > 6][:12]
    found = sum(1 for w in words if w in html)
    assert found >= 6, (
        f"index.html does not appear to embed essay text ({found}/12 sample words found)"
    )


def test_index_html_contains_exodus_reference():
    """index.html must mention Exodus 24:10."""
    html = read(INDEX_HTML)
    assert "24:10" in html, "Exodus 24:10 reference not found in index.html"


# ---------------------------------------------------------------------------
# essay.md content
# ---------------------------------------------------------------------------

def test_essay_word_count_at_least_380():
    """Essay must be approximately 380+ words as specified."""
    text = read(ESSAY_MD)
    count = len(text.split())
    assert count >= 300, f"Essay has only {count} words (need ≥ 300)"


def test_essay_contains_hebrew_verse():
    """Essay must contain the Hebrew text of Exodus 24:10."""
    text = read(ESSAY_MD)
    assert "וַיִּרְאוּ" in text, "Hebrew verse not found in essay.md"


def test_essay_mentions_rashi():
    """Essay must mention Rashi's commentary."""
    text = read(ESSAY_MD)
    assert "Rashi" in text, "Rashi not mentioned in essay.md"


def test_essay_mentions_ramban():
    """Essay must mention Nahmanides / Ramban."""
    text = read(ESSAY_MD)
    assert "Ramban" in text or "Nahmanides" in text, "Ramban/Nahmanides not mentioned in essay.md"


def test_essay_mentions_ibn_ezra():
    """Essay must mention Ibn Ezra."""
    text = read(ESSAY_MD)
    assert "Ibn Ezra" in text, "Ibn Ezra not mentioned in essay.md"


def test_essay_mentions_caustics():
    """Essay must connect caustics to the artwork."""
    text = read(ESSAY_MD).lower()
    assert "caustic" in text, "essay.md does not mention caustics"


# ---------------------------------------------------------------------------
# thumbnail.svg
# ---------------------------------------------------------------------------

def test_thumbnail_is_valid_svg():
    """thumbnail.svg must be valid SVG."""
    text = read(THUMBNAIL_SVG)
    assert "<svg" in text and "</svg>" in text, "thumbnail.svg is not valid SVG"


def test_thumbnail_has_radial_gradient():
    """Thumbnail must use a radial gradient background."""
    text = read(THUMBNAIL_SVG)
    assert "radialGradient" in text, "thumbnail.svg missing radialGradient"


def test_thumbnail_has_caustic_paths():
    """Thumbnail must have path elements suggesting caustic curves."""
    text = read(THUMBNAIL_SVG)
    assert text.count("<path") >= 3, "thumbnail.svg has fewer than 3 path elements"


def test_thumbnail_has_ice_white_stroke():
    """Caustic paths must use ice white #E8F4FF."""
    text = read(THUMBNAIL_SVG)
    assert re.search(r'[Ee]8[Ff]4[Ff]{2}', text), "#E8F4FF not found in thumbnail.svg"


def test_thumbnail_is_400x400():
    """Thumbnail must be 400×400."""
    text = read(THUMBNAIL_SVG)
    assert 'width="400"' in text and 'height="400"' in text, (
        "thumbnail.svg is not 400×400"
    )


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

def test_piece_id_no_duplicates():
    """The new piece ID must not duplicate any existing ID."""
    pieces = load_pieces()
    ids = [p["id"] for p in pieces]
    count = ids.count(PIECE_ID)
    assert count == 1, f"Piece ID '{PIECE_ID}' appears {count} times in pieces.json"


def test_no_external_js_dependencies():
    """index.html must be self-contained — no script src pointing to a CDN."""
    html = read(INDEX_HTML)
    external = re.findall(r'<script[^>]+src=["\']https?://', html, re.IGNORECASE)
    assert len(external) == 0, f"External JS dependencies found: {external}"


def test_essay_md_no_placeholder_text():
    """essay.md must not contain placeholder stub text."""
    text = read(ESSAY_MD).lower()
    bad_phrases = ["lorem ipsum", "todo", "placeholder", "fill in", "tbd"]
    for phrase in bad_phrases:
        assert phrase not in text, f"Placeholder text '{phrase}' found in essay.md"
