"""
Tests specific to piece 82-nbody-souls-at-sinai.

Verifies directory layout, pieces.json registration, N-body simulation
technique, colour palette, leapfrog integration, and essay content.
"""
import json
import os
import re

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID     = "82-nbody-souls-at-sinai"
PIECE_DIR    = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
INDEX_HTML   = os.path.join(PIECE_DIR, "index.html")
ESSAY_MD     = os.path.join(PIECE_DIR, "essay.md")
README_MD    = os.path.join(PIECE_DIR, "README.md")
THUMBNAIL    = os.path.join(PIECE_DIR, "thumbnail.svg")
PIECES_JSON  = os.path.join(GALLERY_ROOT, "pieces.json")


def _html():
    with open(INDEX_HTML, encoding="utf-8") as fh:
        return fh.read()


def _essay():
    with open(ESSAY_MD, encoding="utf-8") as fh:
        return fh.read()


def _pieces():
    with open(PIECES_JSON, encoding="utf-8") as fh:
        return json.load(fh)


def _piece_entry():
    for p in _pieces():
        if p["id"] == PIECE_ID:
            return p
    return None


# ---------------------------------------------------------------------------
# Directory layout
# ---------------------------------------------------------------------------

def test_piece_directory_exists():
    assert os.path.isdir(PIECE_DIR), f"Piece directory {PIECE_DIR} is missing"


def test_index_html_exists():
    assert os.path.isfile(INDEX_HTML), f"pieces/{PIECE_ID}/index.html is missing"


def test_essay_md_exists():
    assert os.path.isfile(ESSAY_MD), f"pieces/{PIECE_ID}/essay.md is missing"


def test_readme_md_exists():
    assert os.path.isfile(README_MD), f"pieces/{PIECE_ID}/README.md is missing"


def test_thumbnail_svg_exists():
    assert os.path.isfile(THUMBNAIL), f"pieces/{PIECE_ID}/thumbnail.svg is missing"


# ---------------------------------------------------------------------------
# pieces.json registration
# ---------------------------------------------------------------------------

def test_piece_registered_in_pieces_json():
    entry = _piece_entry()
    assert entry is not None, f"'{PIECE_ID}' not found in pieces.json"


def test_piece_required_fields_present():
    entry = _piece_entry()
    assert entry is not None
    for field in ("id", "title", "tagline", "year", "theme", "technique", "path", "thumbnail", "essay"):
        assert field in entry and entry[field], f"Field '{field}' missing or empty in pieces.json entry"


def test_piece_path_points_to_existing_file():
    entry = _piece_entry()
    assert entry is not None
    full = os.path.join(GALLERY_ROOT, entry["path"])
    assert os.path.isfile(full), f"path '{entry['path']}' does not exist"


def test_piece_thumbnail_points_to_existing_file():
    entry = _piece_entry()
    assert entry is not None
    full = os.path.join(GALLERY_ROOT, entry["thumbnail"])
    assert os.path.isfile(full), f"thumbnail '{entry['thumbnail']}' does not exist"


def test_piece_essay_field_points_to_existing_file():
    entry = _piece_entry()
    assert entry is not None
    full = os.path.join(GALLERY_ROOT, entry["essay"])
    assert os.path.isfile(full), f"essay '{entry['essay']}' does not exist"


def test_piece_id_matches_directory():
    entry = _piece_entry()
    assert entry is not None
    path_dir = entry["path"].replace("\\", "/").split("/")[-2]
    assert path_dir == PIECE_ID, f"Path dir '{path_dir}' does not match id '{PIECE_ID}'"


def test_piece_year_is_int():
    entry = _piece_entry()
    assert entry is not None
    assert isinstance(entry["year"], int), "year must be an integer"


def test_no_duplicate_ids_after_adding_piece():
    pieces = _pieces()
    ids = [p["id"] for p in pieces]
    assert len(ids) == len(set(ids)), f"Duplicate IDs found: {ids}"


def test_piece_theme_mentions_sinai_and_matan_torah():
    entry = _piece_entry()
    assert entry is not None
    theme = entry.get("theme", "").lower()
    assert "sinai" in theme or "matan torah" in theme, (
        "pieces.json theme must reference Sinai or Matan Torah"
    )


def test_piece_technique_mentions_nbody_or_leapfrog():
    entry = _piece_entry()
    assert entry is not None
    tech = entry.get("technique", "").lower()
    assert "n-body" in tech or "leapfrog" in tech or "gravity" in tech or "nbody" in tech, (
        "pieces.json technique must reference N-body simulation or leapfrog integration"
    )


# ---------------------------------------------------------------------------
# Animation technique — canvas 2D N-body simulation
# ---------------------------------------------------------------------------

def test_html_uses_request_animation_frame():
    assert "requestAnimationFrame" in _html(), "index.html must use requestAnimationFrame"


def test_html_has_canvas_element():
    assert "<canvas" in _html(), "index.html must have a <canvas> element"


def test_html_defines_gravitational_constant():
    """G = 500 must appear as a named constant."""
    html = _html()
    assert re.search(r"\bG\b\s*=\s*500", html), (
        "index.html must define G = 500 (gravitational constant)"
    )


def test_html_defines_sinai_mass():
    """SINAI_MASS = 1e6 (or equivalent) must appear."""
    html = _html()
    assert re.search(r"SINAI_MASS\s*=\s*1e6|sinai_mass\s*=\s*1e6", html, re.IGNORECASE), (
        "index.html must define SINAI_MASS = 1e6"
    )


def test_html_has_softening_parameter():
    """Softening constant ε must appear to prevent singularity."""
    html = _html()
    assert re.search(r"SOFTENING\s*=\s*15|softening\s*=\s*15", html, re.IGNORECASE), (
        "index.html must define SOFTENING = 15 for the gravitational softening"
    )


def test_html_has_dt_timestep():
    """DT = 0.016 must appear as the leapfrog timestep."""
    html = _html()
    assert re.search(r"\bDT\b\s*=\s*0\.016", html), (
        "index.html must define DT = 0.016 for the leapfrog integration timestep"
    )


def test_html_implements_softened_gravity():
    """Softened gravity formula r² + ε² must appear."""
    html = _html()
    assert re.search(r"SOFTENING.*SOFTENING|softening.*softening|\beps\b.*\beps\b", html, re.IGNORECASE), (
        "index.html must implement softened gravity F = G*M/(r² + ε²)"
    )


def test_html_implements_leapfrog_half_kick():
    """Leapfrog half-kick: velocity updated with 0.5 factor."""
    html = _html()
    assert re.search(r"0\.5\s*\*\s*f", html), (
        "index.html must implement leapfrog half-kick (vx += 0.5 * f * ... * dt)"
    )


def test_html_has_three_generations():
    """Three particle generations must be defined."""
    html = _html()
    assert re.search(r"GENS|generations|gen[0-9]|GEN_", html, re.IGNORECASE), (
        "index.html must define three particle generations"
    )


def test_html_spawns_300_particles():
    """N=300 particles (3 × 100) must be implied by the constants."""
    html = _html()
    assert re.search(r"N_PER_GEN\s*=\s*100|100\s*\*\s*3|300", html), (
        "index.html must spawn 300 particles (3 generations × 100 each)"
    )


def test_html_has_trail_ring_buffer():
    """Trail ring buffer of last 30 positions must appear."""
    html = _html()
    assert re.search(r"TRAIL_LEN\s*=\s*30|trail.*30|30.*trail", html, re.IGNORECASE), (
        "index.html must implement an orbital trail of last 30 positions"
    )


def test_html_has_escape_reflection():
    """Escape prevention by velocity reflection must appear."""
    html = _html()
    assert re.search(r"ESCAPE_R|escape_r|500", html, re.IGNORECASE), (
        "index.html must prevent particle escape beyond a maximum radius"
    )


def test_html_uses_frame_persistence_not_clear():
    """Frame persistence via rgba fill instead of clearRect."""
    html = _html()
    assert re.search(r"rgba\(4,\s*3,\s*10,\s*0\.15\)", html), (
        "index.html must use rgba(4,3,10,0.15) partial fill for afterimage persistence"
    )


def test_html_has_sinai_radial_gradient():
    """Sinai central glow must use createRadialGradient."""
    html = _html()
    assert "createRadialGradient" in html, (
        "index.html must draw Sinai as a radial gradient glow"
    )


def test_html_uses_circular_orbit_speed():
    """Initial velocity formula sqrt(G*M/r) must appear."""
    html = _html()
    assert re.search(r"Math\.sqrt\s*\(.*G.*SINAI_MASS|G\s*\*\s*SINAI_MASS", html, re.DOTALL), (
        "index.html must initialise velocities using circular orbit speed sqrt(G*M/r)"
    )


# ---------------------------------------------------------------------------
# Colour palette
# ---------------------------------------------------------------------------

def test_html_has_deep_black_background():
    html = _html()
    assert "#04030A" in html or "#04030a" in html, (
        "index.html must use #04030A as the deep black background"
    )


def test_html_has_gold_generation_1():
    html = _html()
    assert re.search(r"#[Ee]8[Cc]060|E8C060", html, re.IGNORECASE), (
        "index.html must use #E8C060 warm gold for generation 1"
    )


def test_html_has_blue_generation_2():
    html = _html()
    assert re.search(r"#6090[Dd]0|6090D0", html, re.IGNORECASE), (
        "index.html must use #6090D0 sky blue for generation 2"
    )


def test_html_has_violet_generation_3():
    html = _html()
    assert re.search(r"#9060[Cc]0|9060C0", html, re.IGNORECASE), (
        "index.html must use #9060C0 violet for generation 3"
    )


# ---------------------------------------------------------------------------
# Essay content
# ---------------------------------------------------------------------------

def test_essay_minimum_words():
    text = _essay()
    words = len(text.split())
    assert words >= 400, f"essay.md has only {words} words (need ≥ 400)"


def test_essay_cites_shevuot_39a():
    essay = _essay().lower()
    assert "shevuot" in essay or "shevuot 39" in essay, (
        "essay.md must cite Talmud Bavli Shevuot 39a"
    )


def test_essay_cites_tanchuma_nitzavim():
    essay = _essay().lower()
    assert "tanchuma" in essay or "tanhuma" in essay or "nitzavim" in essay, (
        "essay.md must cite Midrash Tanchuma Nitzavim 3"
    )


def test_essay_cites_deuteronomy_29():
    essay = _essay().lower()
    assert "deuteronomy 29" in essay or "29:14" in essay or "not with you alone" in essay.lower(), (
        "essay.md must quote or cite Deuteronomy 29:13-14"
    )


def test_essay_mentions_shavuot_or_matan_torateinu():
    essay = _essay().lower()
    assert "shavuot" in essay or "matan torateinu" in essay or "zman matan" in essay, (
        "essay.md must connect the theme to Shavuot"
    )


def test_essay_connects_to_orbital_simulation():
    essay = _essay().lower()
    has_physics = any(w in essay for w in ("orbit", "gravity", "ring", "shell", "generation", "attractor"))
    assert has_physics, (
        "essay.md must connect the theological theme to the orbital simulation"
    )


def test_essay_embedded_in_html():
    """Key words from essay.md must appear in index.html (embedded inline)."""
    essay_text = _essay()
    html       = _html()
    words      = [w for w in essay_text.split() if len(w) > 6][:15]
    found      = sum(1 for w in words if w in html)
    assert found >= 7, (
        f"Only {found}/15 sampled essay words found in index.html; "
        "the essay must be embedded inline"
    )


# ---------------------------------------------------------------------------
# Thumbnail validity
# ---------------------------------------------------------------------------

def test_thumbnail_is_valid_svg():
    text = open(THUMBNAIL, encoding="utf-8").read()
    assert "<svg" in text and "</svg>" in text, "thumbnail.svg must be valid SVG"


def test_thumbnail_has_400x400_viewbox():
    text = open(THUMBNAIL, encoding="utf-8").read()
    assert "400" in text, "thumbnail.svg must be 400×400"


def test_thumbnail_has_black_background():
    text = open(THUMBNAIL, encoding="utf-8").read().lower()
    assert "#04030a" in text or "04030a" in text, (
        "thumbnail.svg must use the deep black #04030A background"
    )


def test_thumbnail_has_gold_color():
    text = open(THUMBNAIL, encoding="utf-8").read().lower()
    assert "e8c060" in text, "thumbnail.svg must include generation 1 gold color #E8C060"


def test_thumbnail_has_blue_color():
    text = open(THUMBNAIL, encoding="utf-8").read().lower()
    assert "6090d0" in text, "thumbnail.svg must include generation 2 blue color #6090D0"


def test_thumbnail_has_violet_color():
    text = open(THUMBNAIL, encoding="utf-8").read().lower()
    assert "9060c0" in text, "thumbnail.svg must include generation 3 violet color #9060C0"


def test_thumbnail_has_white_center_glow():
    text = open(THUMBNAIL, encoding="utf-8").read().lower()
    assert "ffffff" in text or "white" in text, (
        "thumbnail.svg must include white center glow for Sinai"
    )


# ---------------------------------------------------------------------------
# Edge cases and failure modes
# ---------------------------------------------------------------------------

def test_nonexistent_piece_returns_none():
    """_piece_entry returns None for an unknown ID — sanity check."""
    pieces = _pieces()
    result = next((p for p in pieces if p["id"] == "99-does-not-exist"), None)
    assert result is None


def test_essay_not_stub():
    """A minimal stub essay would be well under 400 words; ours must be substantial."""
    text  = _essay()
    words = len(text.split())
    assert words >= 400, (
        f"essay.md has only {words} words — expected substantial content (≥ 400)"
    )


def test_html_has_no_external_scripts():
    """The simulation must be self-contained with no external script imports."""
    html = _html()
    external_scripts = re.findall(r'<script[^>]+src=["\']https?://', html)
    assert len(external_scripts) == 0, (
        f"index.html must not import external scripts: {external_scripts}"
    )


def test_html_initialises_particles_on_resize():
    """initParticles must be called inside resize to handle canvas size changes."""
    html = _html()
    assert re.search(r"resize.*initParticles|initParticles.*resize", html, re.DOTALL), (
        "index.html must reinitialise particles when the canvas is resized"
    )


def test_readme_mentions_leapfrog():
    text = open(README_MD, encoding="utf-8").read().lower()
    assert "leapfrog" in text or "verlet" in text, (
        "README.md must mention the leapfrog/Verlet integration technique"
    )
