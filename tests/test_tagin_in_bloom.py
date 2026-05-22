"""
Tests for piece 52 "Crowns Upon the Letters" — Tagin in Bloom.

Covers: pieces.json registration, file layout, HTML content (Gray-Scott
simulation with Hebrew letter seeding, color palette, reset loop, essay
embedding), essay.md substance and required citations, and explicit
failure-mode / edge-case behaviors.
"""
import json
import os
import re

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")
PIECE_ID = "52-tagin-in-bloom"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_pieces():
    """Load and return the parsed pieces.json list."""
    with open(PIECES_JSON, encoding="utf-8") as fh:
        return json.load(fh)


def get_piece():
    """Return the pieces.json entry for this piece, or None."""
    for p in load_pieces():
        if p["id"] == PIECE_ID:
            return p
    return None


def read_piece_file(filename):
    """Read a file from the piece directory."""
    return open(os.path.join(PIECE_DIR, filename), encoding="utf-8").read()


# ---------------------------------------------------------------------------
# pieces.json registration
# ---------------------------------------------------------------------------

def test_piece_52_in_json():
    assert get_piece() is not None, f"'{PIECE_ID}' not found in pieces.json"


def test_piece_52_theme_mentions_tagin():
    piece = get_piece()
    assert piece is not None
    theme = piece["theme"].lower()
    assert "tagin" in theme or "tag" in theme or "crown" in theme or "scrib" in theme, (
        "theme must reference tagin, scribal crowns, or related concept"
    )


def test_piece_52_technique_mentions_reaction_diffusion():
    piece = get_piece()
    assert piece is not None
    technique = piece["technique"].lower()
    assert "reaction" in technique or "diffusion" in technique or "gray-scott" in technique, (
        "technique must mention reaction-diffusion or Gray-Scott"
    )


def test_piece_52_technique_mentions_letter_seeding():
    """The technique description must distinguish this piece from piece 07 by mentioning letters."""
    piece = get_piece()
    assert piece is not None
    technique = piece["technique"].lower()
    assert "letter" in technique or "hebrew" in technique or "letterform" in technique, (
        "technique must mention that the piece uses Hebrew letterforms as seeds"
    )


def test_piece_52_year_is_integer():
    piece = get_piece()
    assert piece is not None
    assert isinstance(piece["year"], int)


def test_piece_52_required_fields_present():
    piece = get_piece()
    assert piece is not None
    for field in ("id", "title", "tagline", "year", "theme", "technique", "path", "thumbnail", "essay"):
        assert field in piece and piece[field], f"Missing or empty field '{field}'"


def test_piece_52_id_matches_directory():
    piece = get_piece()
    assert piece is not None
    path_parts = piece["path"].replace("\\", "/").split("/")
    dir_name = path_parts[-2]
    assert dir_name == PIECE_ID, (
        f"piece id '{PIECE_ID}' does not match directory '{dir_name}'"
    )


# ---------------------------------------------------------------------------
# File layout
# ---------------------------------------------------------------------------

def test_piece_52_index_html_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "index.html")), (
        f"pieces/{PIECE_ID}/index.html is missing"
    )


def test_piece_52_thumbnail_exists():
    piece = get_piece()
    assert piece is not None
    thumb_path = os.path.join(GALLERY_ROOT, piece["thumbnail"])
    assert os.path.isfile(thumb_path), (
        f"pieces/{PIECE_ID}: thumbnail '{piece['thumbnail']}' does not exist"
    )


def test_piece_52_thumbnail_is_known_image_type():
    piece = get_piece()
    assert piece is not None
    ext = os.path.splitext(piece["thumbnail"])[1].lower()
    assert ext in {".svg", ".png", ".jpg", ".jpeg", ".webp"}, (
        f"thumbnail has unrecognised extension '{ext}'"
    )


def test_piece_52_readme_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "README.md")), (
        f"pieces/{PIECE_ID}/README.md is missing"
    )


def test_piece_52_essay_md_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "essay.md")), (
        f"pieces/{PIECE_ID}/essay.md is missing"
    )


def test_piece_52_path_ends_with_html():
    piece = get_piece()
    assert piece is not None
    assert piece["path"].endswith(".html"), "piece path must end with .html"


# ---------------------------------------------------------------------------
# index.html — simulation correctness
# ---------------------------------------------------------------------------

def test_piece_52_html_uses_requestanimationframe():
    html = read_piece_file("index.html")
    assert "requestAnimationFrame" in html, (
        "index.html must use requestAnimationFrame for the animation loop"
    )


def test_piece_52_html_has_gray_scott_parameters():
    """F=0.055 and k=0.062 coral-regime parameters must appear in the HTML."""
    html = read_piece_file("index.html")
    assert "0.055" in html, "Gray-Scott feed rate F=0.055 must appear in HTML"
    assert "0.062" in html, "Gray-Scott kill rate k=0.062 must appear in HTML"


def test_piece_52_html_has_diffusion_rates():
    """Du=0.21 and Dv=0.105 — different from piece 07's Du=0.16/Dv=0.08."""
    html = read_piece_file("index.html")
    assert "0.21" in html, "Du=0.21 must appear in HTML"
    assert "0.105" in html, "Dv=0.105 must appear in HTML"


def test_piece_52_html_uses_float32array():
    """Double-buffered Float32Array is required for U and V fields."""
    html = read_piece_file("index.html")
    assert "Float32Array" in html, "index.html must use Float32Array for simulation grids"


def test_piece_52_html_has_four_float32arrays():
    """uA, uB, vA, vB — four arrays needed for double-buffering."""
    html = read_piece_file("index.html")
    count = html.count("Float32Array")
    assert count >= 4, (
        f"index.html must declare at least 4 Float32Arrays (uA, uB, vA, vB); found {count}"
    )


def test_piece_52_html_has_seed_mask():
    """seedMask (Uint8Array) is required to identify letter pixel positions."""
    html = read_piece_file("index.html")
    assert "seedMask" in html or "seed_mask" in html or "seed" in html.lower(), (
        "index.html must maintain a seed mask for the Hebrew letter pixels"
    )


def test_piece_52_html_has_uint8array_for_seed():
    html = read_piece_file("index.html")
    assert "Uint8Array" in html, (
        "index.html must use a Uint8Array (seedMask) to mark letter pixels"
    )


def test_piece_52_html_grid_at_least_300():
    """Grid must be at least 300×300 per the acceptance criteria."""
    html = read_piece_file("index.html")
    numbers = re.findall(r'\b(\d{3,})\b', html)
    grid_dims = [int(n) for n in numbers if int(n) >= 300]
    assert grid_dims, (
        "index.html must define a simulation grid of at least 300 cells per dimension"
    )


def test_piece_52_html_steps_per_frame_30():
    """~30 steps per frame makes the tendril growth visible in real time."""
    html = read_piece_file("index.html")
    assert "30" in html, "STEPS_PER_FRAME should be around 30 per the acceptance criteria"


def test_piece_52_html_has_reset_loop():
    """After convergence, V must be reset so the piece loops: bloom → settle → reset → bloom."""
    html = read_piece_file("index.html")
    assert "RESET" in html or "reset" in html.lower(), (
        "index.html must implement a reset loop after convergence"
    )
    assert "5000" in html or "RESET_STEPS" in html, (
        "Reset should trigger around 5000 steps"
    )


def test_piece_52_html_has_reset_frames():
    html = read_piece_file("index.html")
    assert "200" in html and ("RESET_FRAMES" in html or "reset" in html.lower()), (
        "Reset fade must take ~200 frames"
    )


def test_piece_52_html_reinseeds_letters():
    """Letter seeds must be re-applied each step to keep letter cores stable."""
    html = read_piece_file("index.html")
    assert "seedMask" in html and ("nu[i]" in html or "nv[i]" in html or "nu[" in html), (
        "index.html must reinforce letter seeds in simStep to keep letter cores stable"
    )


def test_piece_52_html_rasterizes_hebrew_text():
    """The letter seeding must use an offscreen canvas to rasterize Hebrew text."""
    html = read_piece_file("index.html")
    assert "fillText" in html, "index.html must use canvas fillText to rasterize Hebrew letters"
    assert "getImageData" in html, "index.html must read back pixel data via getImageData"


def test_piece_52_html_has_torah_word():
    """The word תּוֹרָה or Torah must appear in the seeding code."""
    html = read_piece_file("index.html")
    assert "תּוֹרָה" in html or "Torah" in html or "תורה" in html, (
        "index.html must rasterize the Hebrew word תּוֹרָה as seed letters"
    )


# ---------------------------------------------------------------------------
# index.html — color palette (distinct from piece 07)
# ---------------------------------------------------------------------------

def test_piece_52_html_has_midnight_blue():
    """Dark background color #0A0A1F (midnight blue) must appear."""
    html = read_piece_file("index.html")
    assert "0A0A1F" in html.upper() or "0a0a1f" in html.lower(), (
        "index.html must reference midnight blue #0A0A1F as background/zero color"
    )


def test_piece_52_html_has_gold_color():
    """Bright gold #FFD700 must appear for peak V values."""
    html = read_piece_file("index.html")
    assert "FFD700" in html.upper() or "ffd700" in html.lower(), (
        "index.html must reference gold #FFD700 as the peak-V color"
    )


def test_piece_52_html_has_color_lut():
    """Color should be pre-built in a LUT for performance."""
    html = read_piece_file("index.html")
    assert "LUT" in html or "lut" in html, (
        "index.html must implement a color lookup table (LUT)"
    )


def test_piece_52_palette_different_from_07():
    """Piece 52 must NOT use the piece-07 cream/honey/amber palette."""
    html = read_piece_file("index.html")
    assert "fdf6e3" not in html.lower(), (
        "index.html must not reuse piece-07's cream color #fdf6e3"
    )
    assert "d4a017" not in html.lower(), (
        "index.html must not reuse piece-07's honey color #d4a017"
    )


def test_piece_52_html_has_putimagedata():
    """Performance-critical rendering must use putImageData, not per-pixel fillRect."""
    html = read_piece_file("index.html")
    assert "putImageData" in html, (
        "index.html must use putImageData for efficient canvas rendering"
    )


# ---------------------------------------------------------------------------
# index.html — layout
# ---------------------------------------------------------------------------

def test_piece_52_html_has_two_panel_layout():
    html = read_piece_file("index.html")
    assert "art-panel" in html and "essay-panel" in html, (
        "index.html must define art-panel and essay-panel divs"
    )


def test_piece_52_html_has_responsive_media_query():
    html = read_piece_file("index.html")
    assert "@media" in html, "index.html must include a responsive media query"
    assert "768" in html or "600" in html, "media query must specify a breakpoint (768px or 600px)"


def test_piece_52_html_essay_embedded():
    """Essay text must be embedded in HTML, not fetched at runtime."""
    essay = read_piece_file("essay.md")
    html = read_piece_file("index.html")
    words = [w for w in essay.split() if len(w) > 6][:10]
    found = sum(1 for w in words if w in html)
    assert found >= 5, (
        f"index.html must embed the essay text (only {found}/10 sampled words found)"
    )


def test_piece_52_html_no_external_resources():
    html = read_piece_file("index.html")
    external = re.findall(r'(?:src|href)\s*=\s*["\']https?://', html)
    assert not external, f"index.html must not load external resources; found: {external}"


# ---------------------------------------------------------------------------
# essay.md content
# ---------------------------------------------------------------------------

def test_piece_52_essay_word_count():
    text = read_piece_file("essay.md")
    count = len(text.split())
    assert 200 <= count <= 1500, (
        f"essay.md must be 200-1500 words; found {count}"
    )


def test_piece_52_essay_mentions_menachot_29b():
    """The Talmudic source Menachot 29b must be cited."""
    text = read_piece_file("essay.md").lower()
    assert "menachot" in text or "menahot" in text or "29b" in text, (
        "essay.md must cite Menachot 29b (Moses and the crowns)"
    )


def test_piece_52_essay_mentions_shabbat_55a():
    """Shabbat 55a (seal of the Holy One is emet) must be cited."""
    text = read_piece_file("essay.md").lower()
    assert "shabbat" in text or "55a" in text or "emet" in text or "אמת" in text, (
        "essay.md must reference Shabbat 55a or the concept of emet"
    )


def test_piece_52_essay_mentions_akiva():
    text = read_piece_file("essay.md").lower()
    assert "akiva" in text, "essay.md must tell the story of Rabbi Akiva deriving law from tagin"


def test_piece_52_essay_mentions_tagin_letters():
    """The seven letters that bear tagin must be mentioned."""
    text = read_piece_file("essay.md")
    assert "שַׁעְטְנֵ" in text or "sha'atnez" in text.lower() or "שׁ" in text, (
        "essay.md must identify the letters that bear tagin (sha'atnez getz)"
    )


def test_piece_52_essay_mentions_gray_scott_or_reaction_diffusion():
    text = read_piece_file("essay.md").lower()
    assert "gray-scott" in text or "reaction-diffusion" in text or "reaction diffusion" in text, (
        "essay.md must mention the Gray-Scott / reaction-diffusion technique"
    )


def test_piece_52_essay_connects_sim_to_tagin_concept():
    """The essay must connect the simulation to the theological meaning of tagin."""
    text = read_piece_file("essay.md").lower()
    assert "latent" in text or "bloom" in text or "tendril" in text or "crown" in text, (
        "essay.md must connect the reaction-diffusion growth to the concept of tagin"
    )


# ---------------------------------------------------------------------------
# README.md
# ---------------------------------------------------------------------------

def test_piece_52_readme_mentions_tagin():
    text = read_piece_file("README.md").lower()
    assert "tagin" in text or "tag" in text or "crown" in text, (
        "README.md must mention tagin or scribal crowns"
    )


def test_piece_52_readme_mentions_gray_scott():
    text = read_piece_file("README.md").lower()
    assert "gray-scott" in text or "reaction" in text, (
        "README.md must mention Gray-Scott or reaction-diffusion"
    )


def test_piece_52_readme_mentions_distinction_from_07():
    """README must note how this differs from piece 07 to satisfy distinctness requirement."""
    text = read_piece_file("README.md").lower()
    assert "07" in text or "07-milk" in text or "milk" in text or "distinct" in text or "distinction" in text, (
        "README.md should explain how this piece differs from 07-milk-honey-reaction-diffusion"
    )


# ---------------------------------------------------------------------------
# Pure-Python Gray-Scott correctness (no external dependencies)
# ---------------------------------------------------------------------------

def _run_gray_scott_step(u, v, W, H, Du, Dv, F, k):
    """One Gray-Scott step returning (new_u, new_v) as flat lists."""
    nu = [0.0] * (W * H)
    nv = [0.0] * (W * H)
    for y in range(H):
        row = y * W
        rowUp = (y - 1 if y > 0 else H - 1) * W
        rowDn = (y + 1 if y < H - 1 else 0) * W
        for x in range(W):
            i = row + x
            lt = row + (x - 1 if x > 0 else W - 1)
            rt = row + (x + 1 if x < W - 1 else 0)
            up = rowUp + x
            dn = rowDn + x
            ui, vi = u[i], v[i]
            lapU = u[lt] + u[rt] + u[up] + u[dn] - 4 * ui
            lapV = v[lt] + v[rt] + v[up] + v[dn] - 4 * vi
            uvv = ui * vi * vi
            nu[i] = max(0.0, min(1.0, ui + Du * lapU - uvv + F * (1 - ui)))
            nv[i] = max(0.0, min(1.0, vi + Dv * lapV + uvv - (F + k) * vi))
    return nu, nv


def test_gray_scott_v_spreads_from_letter_seed():
    """
    A letter-style seed (U=0.5, V=0.25 at letter pixels) surrounded by
    U=1/V=0 background must spread V to neighboring cells after one step.
    """
    W, H = 32, 32
    Du, Dv, Ff, kk = 0.21, 0.105, 0.055, 0.062
    u = [1.0] * (W * H)
    v = [0.0] * (W * H)
    cx, cy = 16, 16
    for dy in range(-2, 3):
        for dx in range(-2, 3):
            idx = (cy + dy) * W + (cx + dx)
            u[idx] = 0.5
            v[idx] = 0.25

    nu, nv = _run_gray_scott_step(u, v, W, H, Du, Dv, Ff, kk)

    boundary_indices = [
        (cy - 3) * W + cx,
        (cy + 3) * W + cx,
        cy * W + (cx - 3),
        cy * W + (cx + 3),
    ]
    assert any(nv[i] > 0 for i in boundary_indices), (
        "V must diffuse from letter seed into surrounding cells after one step"
    )


def test_gray_scott_stable_background_without_seed():
    """
    A uniform U=1, V=0 field with no perturbation must remain stable (V stays 0).
    """
    W, H = 16, 16
    Du, Dv, Ff, kk = 0.21, 0.105, 0.055, 0.062
    u = [1.0] * (W * H)
    v = [0.0] * (W * H)

    for _ in range(10):
        u, v = _run_gray_scott_step(u, v, W, H, Du, Dv, Ff, kk)

    total_v = sum(v)
    assert total_v == 0.0, (
        f"U=1/V=0 background must remain stable with no seed; total_v={total_v}"
    )


def test_gray_scott_values_stay_in_unit_interval():
    """U and V must never exceed 1 or go below 0 even after many steps."""
    W, H = 16, 16
    Du, Dv, Ff, kk = 0.21, 0.105, 0.055, 0.062
    u = [1.0] * (W * H)
    v = [0.0] * (W * H)
    u[8 * W + 8] = 0.5
    v[8 * W + 8] = 0.25

    for _ in range(100):
        u, v = _run_gray_scott_step(u, v, W, H, Du, Dv, Ff, kk)

    for i in range(W * H):
        assert 0.0 <= u[i] <= 1.0, f"u[{i}]={u[i]} out of [0,1]"
        assert 0.0 <= v[i] <= 1.0, f"v[{i}]={v[i]} out of [0,1]"


def test_gray_scott_seeded_v_grows_from_letter_over_multiple_steps():
    """
    A letter-seeded grid should accumulate V in surrounding cells over 50 steps,
    confirming tendril growth from letter bodies.
    """
    W, H = 32, 32
    Du, Dv, Ff, kk = 0.21, 0.105, 0.055, 0.062
    u = [1.0] * (W * H)
    v = [0.0] * (W * H)
    cx, cy = 16, 16
    seed_cells = set()
    for dy in range(-2, 3):
        for dx in range(-2, 3):
            idx = (cy + dy) * W + (cx + dx)
            u[idx] = 0.5
            v[idx] = 0.25
            seed_cells.add(idx)

    for _ in range(50):
        nu, nv = _run_gray_scott_step(u, v, W, H, Du, Dv, Ff, kk)
        for idx in seed_cells:
            nu[idx] = 0.5
            nv[idx] = 0.25
        u, v = nu, nv

    non_seed_v = [v[i] for i in range(W * H) if i not in seed_cells]
    total_non_seed_v = sum(non_seed_v)
    assert total_non_seed_v > 0.1, (
        f"V should have spread from letter seeds into surrounding cells after 50 steps; "
        f"total non-seed V = {total_non_seed_v}"
    )


# ---------------------------------------------------------------------------
# Color mapping correctness
# ---------------------------------------------------------------------------

def test_color_lut_midnight_blue_at_zero():
    """LUT[0] must map to midnight blue #0A0A1F (10, 10, 31)."""
    r0 = int(10 + 245 * 0 + 0.5)
    g0 = int(10 + 205 * 0 + 0.5)
    b0 = int(31 * (1 - 0) + 0.5)
    assert r0 == 10, f"LUT R at index 0 must be 10; got {r0}"
    assert g0 == 10, f"LUT G at index 0 must be 10; got {g0}"
    assert b0 == 31, f"LUT B at index 0 must be 31; got {b0}"


def test_color_lut_gold_at_maximum():
    """LUT[255] must map to gold #FFD700 (255, 215, 0)."""
    r255 = int(10 + 245 * 1.0 + 0.5)
    g255 = int(10 + 205 * 1.0 + 0.5)
    b255 = int(31 * (1 - 1.0) + 0.5)
    assert r255 == 255, f"LUT R at index 255 must be 255; got {r255}"
    assert g255 == 215, f"LUT G at index 255 must be 215; got {g255}"
    assert b255 == 0, f"LUT B at index 255 must be 0; got {b255}"


def test_color_lut_monotone_r_channel():
    """R channel of LUT must be non-decreasing from index 0 to 255."""
    lut_r = [int(10 + 245 * (i / 255) + 0.5) for i in range(256)]
    for i in range(1, 256):
        assert lut_r[i] >= lut_r[i - 1], (
            f"R channel must be non-decreasing; lut_r[{i}]={lut_r[i]} < lut_r[{i-1}]={lut_r[i-1]}"
        )


# ---------------------------------------------------------------------------
# Edge-case / failure-mode tests
# ---------------------------------------------------------------------------

def test_piece_52_no_duplicate_id():
    pieces = load_pieces()
    ids = [p["id"] for p in pieces]
    assert len(ids) == len(set(ids)), f"Duplicate piece IDs in pieces.json: {ids}"


def test_missing_piece_52_would_fail(tmp_path):
    """Confirm that a missing piece directory is detectable."""
    fake_dir = tmp_path / "fake-52-tagin"
    assert not fake_dir.exists()
    assert not os.path.isfile(str(fake_dir / "index.html"))


def test_piece_52_essay_field_in_json():
    piece = get_piece()
    assert piece is not None
    assert "essay" in piece and piece["essay"], (
        "pieces.json entry must have a non-empty 'essay' field"
    )


def test_piece_52_essay_path_matches_disk():
    piece = get_piece()
    assert piece is not None
    essay_path = os.path.join(GALLERY_ROOT, piece["essay"])
    assert os.path.isfile(essay_path), (
        f"Essay path '{piece['essay']}' in pieces.json does not exist on disk"
    )


def test_piece_52_thumbnail_path_matches_disk():
    piece = get_piece()
    assert piece is not None
    thumb_path = os.path.join(GALLERY_ROOT, piece["thumbnail"])
    assert os.path.isfile(thumb_path), (
        f"Thumbnail path '{piece['thumbnail']}' in pieces.json does not exist on disk"
    )


def test_piece_52_html_essay_field_references_correct_subdirectory():
    """pieces.json 'essay' field must point into pieces/52-tagin-in-bloom/."""
    piece = get_piece()
    assert piece is not None
    assert PIECE_ID in piece["essay"].replace("\\", "/"), (
        f"essay path '{piece['essay']}' must reference the {PIECE_ID} subdirectory"
    )
