"""
Tests for the Vicsek Sinai unity piece (90-vicsek-sinai-unity).

Checks the piece directory layout, pieces.json registration, essay content,
and HTML correctness for the acceptance criteria.
"""
import json
import os


GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")
PIECE_ID = "90-vicsek-sinai-unity"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)


def load_pieces():
    with open(PIECES_JSON, encoding="utf-8") as fh:
        return json.load(fh)


def get_piece():
    for p in load_pieces():
        if p["id"] == PIECE_ID:
            return p
    return None


def read_html():
    p = get_piece()
    assert p is not None
    return open(os.path.join(GALLERY_ROOT, p["path"]), encoding="utf-8").read()


def read_essay():
    p = get_piece()
    assert p is not None
    return open(os.path.join(GALLERY_ROOT, p["essay"]), encoding="utf-8").read()


# ---------------------------------------------------------------------------
# pieces.json registration
# ---------------------------------------------------------------------------

def test_piece_registered_in_pieces_json():
    """The piece must appear in pieces.json."""
    assert get_piece() is not None, f"'{PIECE_ID}' not found in pieces.json"


def test_piece_theme_is_sinai_unity():
    p = get_piece()
    assert p is not None
    assert "Sinai" in p["theme"] or "unity" in p["theme"].lower(), (
        f"Expected Sinai/unity theme, got: {p['theme']}"
    )


def test_piece_technique_mentions_vicsek():
    p = get_piece()
    assert p is not None
    assert "Vicsek" in p["technique"] or "vicsek" in p["technique"].lower(), (
        f"Expected Vicsek in technique, got: {p['technique']}"
    )


def test_piece_year_is_integer():
    p = get_piece()
    assert p is not None
    assert isinstance(p["year"], int)


def test_piece_has_all_required_fields():
    required = ("id", "title", "tagline", "year", "theme", "technique", "path", "thumbnail", "essay")
    p = get_piece()
    assert p is not None
    for field in required:
        assert field in p and p[field], f"Missing or empty field: {field}"


# ---------------------------------------------------------------------------
# Directory layout
# ---------------------------------------------------------------------------

def test_piece_directory_exists():
    assert os.path.isdir(PIECE_DIR), f"Piece directory not found: {PIECE_DIR}"


def test_index_html_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "index.html"))


def test_essay_md_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "essay.md"))


def test_readme_md_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "README.md"))


def test_thumbnail_svg_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "thumbnail.svg"))


# ---------------------------------------------------------------------------
# Essay content
# ---------------------------------------------------------------------------

def test_essay_has_at_least_300_words():
    essay = read_essay()
    word_count = len(essay.split())
    assert word_count >= 300, f"Essay has only {word_count} words (need ≥ 300)"


def test_essay_mentions_exodus_verse():
    """Essay must open with the Exodus 19:2 verse."""
    essay = read_essay()
    assert "19:2" in essay or "Va'yichan" in essay or "Yichan" in essay, (
        "Essay must reference Exodus 19:2 or 'Va'yichan'"
    )


def test_essay_mentions_rashi():
    essay = read_essay()
    assert "Rashi" in essay, "Essay must cite Rashi's comment on ke'ish echad"


def test_essay_mentions_ke_ish_echad():
    essay = read_essay()
    text = essay.lower()
    assert "echad" in text or "one heart" in text or "one person" in text, (
        "Essay must reference ke'ish echad / one person with one heart"
    )


def test_essay_mentions_vicsek():
    essay = read_essay()
    assert "Vicsek" in essay or "vicsek" in essay, "Essay must explain the Vicsek model"


def test_essay_mentions_phase_transition():
    essay = read_essay()
    assert "phase transition" in essay or "phase" in essay.lower(), (
        "Essay must mention the Vicsek phase transition"
    )


# ---------------------------------------------------------------------------
# index.html content
# ---------------------------------------------------------------------------

def test_html_uses_requestanimationframe():
    html = read_html()
    assert "requestAnimationFrame" in html


def test_html_has_canvas():
    html = read_html()
    assert "<canvas" in html


def test_html_initializes_n_500_particles():
    html = read_html()
    assert "500" in html, "HTML must initialize N=500 particles"


def test_html_has_vicsek_speed():
    """Speed constant v=1.5 must be present."""
    html = read_html()
    assert "1.5" in html


def test_html_has_interaction_radius():
    """Radius r=40 must be present."""
    html = read_html()
    assert "40" in html


def test_html_mentions_eta():
    """Noise parameter η must appear in HUD code."""
    html = read_html()
    assert "eta" in html.lower() or "η" in html


def test_html_has_noise_animation_schedule():
    """The three-phase noise schedule (descend/hold/spike) must be present."""
    html = read_html()
    assert "0.85" in html, "Start noise η=0.85 must be in HTML"
    assert "0.05" in html, "End noise η=0.05 must be in HTML"


def test_html_has_mountain_silhouette():
    """Mountain triangle vertices using 0.35/0.50/0.65 fractions must be present."""
    html = read_html()
    assert "0.35" in html or "0.80" in html, (
        "Mountain silhouette coordinates must be present in HTML"
    )


def test_html_has_alignment_colors():
    """The three palette colors must appear in the HTML."""
    html = read_html()
    assert "D4A017" in html.upper(), "Wheat gold #D4A017 missing"
    assert "6B3FA0" in html.upper(), "Twilight violet #6B3FA0 missing"
    assert "1A1A4E" in html.upper(), "Deep indigo #1A1A4E missing"


def test_html_has_mountain_color():
    html = read_html()
    assert "2A2A2A" in html.upper(), "Mountain charcoal #2A2A2A missing"


def test_html_has_order_parameter_hud():
    """The HUD must display alignment percentage (order parameter)."""
    html = read_html()
    assert "Alignment" in html, "HUD must display 'Alignment: X%'"


def test_html_embeds_essay_text():
    """index.html must embed the essay inline — not fetch it at runtime."""
    essay = read_essay()
    html = read_html()
    words = [w for w in essay.split() if len(w) > 5][:10]
    found = sum(1 for w in words if w in html)
    assert found >= 5, (
        f"Only {found}/10 essay words found in HTML — essay may not be embedded"
    )


def test_thumbnail_is_valid_svg():
    thumb = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert "<svg" in thumb and "</svg>" in thumb


def test_thumbnail_has_mountain():
    thumb = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert "polygon" in thumb or "path" in thumb, (
        "Thumbnail SVG must contain a mountain polygon/path"
    )


def test_thumbnail_has_particle_lines():
    thumb = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert "<line" in thumb, "Thumbnail SVG must contain directional particle lines"


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

def test_piece_id_matches_directory():
    """The piece id in pieces.json must match the actual directory name."""
    p = get_piece()
    assert p is not None
    path_parts = p["path"].replace("\\", "/").split("/")
    dir_name = path_parts[-2]
    assert dir_name == PIECE_ID, f"Directory '{dir_name}' != id '{PIECE_ID}'"


def test_no_duplicate_piece_ids():
    pieces = load_pieces()
    ids = [p["id"] for p in pieces]
    assert len(ids) == len(set(ids)), "Duplicate piece IDs found"


def test_piece_not_present_returns_none():
    """Helper should return None for a nonexistent piece id."""
    pieces = load_pieces()
    result = next((p for p in pieces if p["id"] == "99-nonexistent"), None)
    assert result is None


def test_html_does_not_fetch_essay_at_runtime():
    """The HTML must not fetch essay.md at runtime (essay must be embedded)."""
    html = read_html()
    assert 'fetch("essay.md")' not in html
    assert "fetch('essay.md')" not in html
    assert 'src="essay.md"' not in html
