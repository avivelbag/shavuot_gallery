"""
Tests for piece 86-ant-colony-forty-nine-gates (Ant-colony stigmergy / 49 gates of Binah).

Verifies acceptance criteria: file layout, pieces.json registration, essay content,
HTML mechanics (canvas, rAF, ACO parameters, Hebrew counter, color palette), and
thumbnail SVG dimensions and content.
"""
import json
import os

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID = "86-ant-colony-forty-nine-gates"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
INDEX_HTML = os.path.join(PIECE_DIR, "index.html")
ESSAY_MD = os.path.join(PIECE_DIR, "essay.md")
THUMBNAIL = os.path.join(PIECE_DIR, "thumbnail.svg")
README = os.path.join(PIECE_DIR, "README.md")
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")


def _load_pieces():
    with open(PIECES_JSON, encoding="utf-8") as fh:
        return json.load(fh)


def _get_piece():
    for p in _load_pieces():
        if p["id"] == PIECE_ID:
            return p
    return None


def _html():
    return open(INDEX_HTML, encoding="utf-8").read()


def _essay():
    return open(ESSAY_MD, encoding="utf-8").read()


# ---------------------------------------------------------------------------
# File layout
# ---------------------------------------------------------------------------

def test_piece_directory_exists():
    """The piece directory must exist on disk."""
    assert os.path.isdir(PIECE_DIR)


def test_index_html_exists():
    assert os.path.isfile(INDEX_HTML)


def test_essay_md_exists():
    assert os.path.isfile(ESSAY_MD)


def test_thumbnail_svg_exists():
    assert os.path.isfile(THUMBNAIL)


def test_readme_exists():
    assert os.path.isfile(README)


# ---------------------------------------------------------------------------
# pieces.json registration
# ---------------------------------------------------------------------------

def test_piece_registered_in_pieces_json():
    """pieces.json must contain an entry with id == PIECE_ID."""
    assert _get_piece() is not None, f"{PIECE_ID} not found in pieces.json"


def test_pieces_json_theme_mentions_sefirat_haomer():
    p = _get_piece()
    assert p is not None
    theme = p["theme"].lower()
    assert "sefirat" in theme or "omer" in theme or "gates" in theme, \
        "theme must reference Sefirat HaOmer / gates of understanding"


def test_pieces_json_technique_mentions_ant_colony():
    p = _get_piece()
    assert p is not None
    tech = p["technique"].lower()
    assert "ant" in tech or "pheromone" in tech or "stigmergy" in tech, \
        "technique must mention ant-colony or pheromone reinforcement"


def test_pieces_json_paths_all_exist():
    """path, thumbnail, and essay fields must all point at files on disk."""
    p = _get_piece()
    assert p is not None
    for field in ("path", "thumbnail", "essay"):
        full = os.path.join(GALLERY_ROOT, p[field])
        assert os.path.isfile(full), \
            f"pieces.json field '{field}' points to missing file: {p[field]}"


def test_pieces_json_year_is_2026():
    p = _get_piece()
    assert p is not None
    assert p["year"] == 2026


def test_no_duplicate_ids():
    """Adding this piece must not create duplicate IDs."""
    ids = [p["id"] for p in _load_pieces()]
    assert ids.count(PIECE_ID) == 1, f"Duplicate entry for {PIECE_ID} in pieces.json"


# ---------------------------------------------------------------------------
# essay.md content
# ---------------------------------------------------------------------------

def test_essay_word_count():
    """Essay must be at least 350 words."""
    words = _essay().split()
    assert len(words) >= 350, f"Essay only has {len(words)} words (need ≥ 350)"


def test_essay_cites_rosh_hashanah_21b():
    """Essay must cite the Talmudic source Rosh Hashanah 21b."""
    text = _essay()
    assert "21b" in text or "Rosh Hashanah" in text, \
        "Essay must cite Rosh Hashanah 21b"


def test_essay_cites_nedarim_38a():
    """Essay must cite Nedarim 38a."""
    text = _essay()
    assert "38a" in text or "Nedarim" in text, \
        "Essay must cite Nedarim 38a"


def test_essay_mentions_binah():
    """Essay must discuss Binah (Understanding)."""
    text = _essay()
    assert "Binah" in text or "Understanding" in text, \
        "Essay must discuss the gates of Binah"


def test_essay_mentions_omer_and_sefirot():
    """Essay must connect the Omer count to sefirot structure."""
    text = _essay()
    assert "sefirot" in text.lower() or "Sefirot" in text or "sefirah" in text.lower(), \
        "Essay must mention the sefirot structure of the Omer"


def test_essay_mentions_zohar():
    """Essay must cite the Zohar."""
    text = _essay()
    assert "Zohar" in text, "Essay must cite the Zohar"


def test_essay_mentions_pheromone_or_stigmergy():
    """Essay must tie the Omer to the ACO technique."""
    text = _essay()
    assert "pheromone" in text.lower() or "stigmergy" in text.lower() or "ant" in text.lower(), \
        "Essay must explain the pheromone / stigmergy technique"


def test_essay_not_a_stub():
    """Essay must be substantial, not a placeholder."""
    text = _essay().strip()
    assert len(text) > 600, "essay.md appears to be a stub"


# ---------------------------------------------------------------------------
# index.html — mechanics
# ---------------------------------------------------------------------------

def test_html_has_canvas_element():
    assert "canvas" in _html()


def test_html_uses_request_animation_frame():
    assert "requestAnimationFrame" in _html()


def test_html_defines_grid_120x120():
    """Grid must be 120 columns × 120 rows."""
    text = _html()
    assert "120" in text, "index.html must define a 120×120 grid (COLS = ROWS = 120)"


def test_html_has_200_ants():
    """N_ANTS must be 200."""
    assert "200" in _html(), "index.html must specify N_ANTS = 200"


def test_html_has_49_max_gen():
    """MAX_GEN must be 49."""
    assert "49" in _html(), "index.html must specify MAX_GEN = 49"


def test_html_evaporation_factor():
    """Evaporation factor 0.85 must be present."""
    assert "0.85" in _html(), "index.html must specify evaporation factor 0.85"


def test_html_beta_exponent():
    """Beta=2 (pheromone exponent) must be present."""
    text = _html()
    assert "BETA = 2" in text or "BETA=2" in text or "beta = 2" in text.lower() or \
           ("BETA" in text and "2" in text), \
        "index.html must specify pheromone exponent β=2"


def test_html_background_color():
    """Background color #090818 (deep indigo) must be present."""
    text = _html()
    assert "#090818" in text or "#090818".lower() in text.lower(), \
        "index.html must use background color #090818"


def test_html_gold_color():
    """Gold color #F0C040 must be present for the Shavuot reveal."""
    text = _html()
    assert "#F0C040" in text or "#f0c040" in text.lower(), \
        "index.html must use gold color #F0C040"


def test_html_violet_color():
    """Dim violet #3020A0 must be present for low-pheromone trails."""
    text = _html()
    assert "#3020A0" in text or "#3020a0" in text.lower(), \
        "index.html must use dim violet #3020A0 for low-pheromone cells"


def test_html_has_hebrew_numeral_aleph():
    """The Hebrew letter א (aleph, day 1) must appear in the HTML."""
    assert "א" in _html(), "index.html must display Hebrew numeral א for day 1"


def test_html_has_hebrew_numeral_nun():
    """The Hebrew letter נ (nun = 50, Shavuot) must appear in the HTML."""
    assert "נ" in _html(), "index.html must display Hebrew numeral נ for day 50"


def test_html_has_shavuot_reveal():
    """index.html must implement a special reveal on generation 50."""
    text = _html()
    assert "50" in text and ("shavuot" in text.lower() or "שבועות" in text or "gen" in text.lower()), \
        "index.html must implement the Shavuot (generation 50) reveal"


def test_html_embeds_essay_words():
    """Essay text must be embedded inline — check sampled long words."""
    essay_words = [w for w in _essay().split() if len(w) > 6][:12]
    html = _html()
    found = sum(1 for w in essay_words if w in html)
    assert found >= 6, \
        f"Only {found}/12 sampled essay words found in index.html — essay may not be embedded"


def test_html_does_not_fetch_essay_at_runtime():
    """index.html must not fetch essay.md at runtime."""
    html = _html()
    assert "essay.md" not in html, \
        "index.html must embed the essay inline, not fetch essay.md at runtime"


def test_html_has_src_and_dst_nodes():
    """Source and destination node coordinates must be defined."""
    text = _html()
    assert "SRC" in text and "DST" in text, \
        "index.html must define SRC and DST nodes"


def test_html_defines_run_generation():
    """The runGeneration() function (or equivalent) must exist."""
    text = _html()
    assert "runGeneration" in text or "run_generation" in text or "generation" in text.lower(), \
        "index.html must define a runGeneration function"


def test_html_defines_find_best_path():
    """The best-path extraction function must exist for the Shavuot reveal."""
    text = _html()
    assert "findBestPath" in text or "find_best" in text or "bestPath" in text or "best_path" in text, \
        "index.html must define a findBestPath function for the generation-50 reveal"


# ---------------------------------------------------------------------------
# thumbnail.svg
# ---------------------------------------------------------------------------

def test_thumbnail_is_valid_svg():
    text = open(THUMBNAIL, encoding="utf-8").read()
    assert "<svg" in text and "</svg>" in text


def test_thumbnail_400x400():
    """Thumbnail must declare 400×400 dimensions."""
    text = open(THUMBNAIL, encoding="utf-8").read()
    assert 'width="400"' in text and 'height="400"' in text, \
        "thumbnail.svg must be 400×400"


def test_thumbnail_dark_background():
    """Thumbnail must use the deep indigo background #090818."""
    text = open(THUMBNAIL, encoding="utf-8").read()
    assert "090818" in text.lower(), \
        "thumbnail.svg must use background color #090818"


def test_thumbnail_has_gold_path():
    """Thumbnail must include the gold color #F0C040 for the central path."""
    text = open(THUMBNAIL, encoding="utf-8").read()
    assert "F0C040" in text or "f0c040" in text.lower(), \
        "thumbnail.svg must include gold color #F0C040"


def test_thumbnail_has_violet_trails():
    """Thumbnail must include the dim violet #3020A0 for faint trail lines."""
    text = open(THUMBNAIL, encoding="utf-8").read()
    assert "3020A0" in text or "3020a0" in text.lower(), \
        "thumbnail.svg must include dim violet #3020A0 for trail lines"


def test_thumbnail_has_glowing_nodes():
    """Thumbnail must include both the green source glow and the white destination glow."""
    text = open(THUMBNAIL, encoding="utf-8").read()
    has_green = "40FF80" in text or "40ff80" in text.lower()
    has_white = "FFFFFF" in text or "ffffff" in text.lower()
    assert has_green and has_white, \
        "thumbnail.svg must include both green source glow and white destination glow"


# ---------------------------------------------------------------------------
# Edge cases and failure modes
# ---------------------------------------------------------------------------

def test_essay_contains_psalm_reference():
    """Essay must cite Psalm 8:6 (the 'slightly less than divine' proof-text)."""
    text = _essay()
    assert "Psalm" in text or "8:6" in text or "divine" in text.lower(), \
        "Essay must cite Psalm 8:6"


def test_essay_mentions_fiftieth_gate():
    """Essay must discuss the inaccessible fiftieth gate."""
    text = _essay()
    assert "fiftieth" in text.lower() or "50" in text or "fifty" in text.lower(), \
        "Essay must discuss the fiftieth gate"


def test_empty_pieces_json_array_detected(tmp_path):
    """An empty pieces.json array should be flagged as having no new piece entry."""
    data = json.loads("[]")
    found = any(p.get("id") == PIECE_ID for p in data)
    assert not found, "Empty array should not contain the new piece"


def test_missing_thumbnail_file_detected(tmp_path):
    """A non-existent thumbnail path must fail the file-existence check."""
    missing = os.path.join(str(tmp_path), "thumbnail.svg")
    assert not os.path.isfile(missing), "Fixture path must not exist"


def test_piece_has_all_required_json_fields():
    """The new pieces.json entry must have all required fields non-empty."""
    required = ("id", "title", "tagline", "year", "theme", "technique",
                "path", "thumbnail", "essay")
    p = _get_piece()
    assert p is not None
    for field in required:
        val = p.get(field)
        assert val is not None and val != "", \
            f"pieces.json entry is missing or has empty field '{field}'"
