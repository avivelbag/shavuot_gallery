"""
Tests for piece 75-ising-one-heart-sinai.

Verifies the directory layout, pieces.json registration, HTML content
(Metropolis algorithm, temperature schedule, color palette, Hebrew overlay,
temperature readout), essay length, and thumbnail validity.
"""
import json
import os
import re

import pytest

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID     = "75-ising-one-heart-sinai"
PIECE_DIR    = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
HTML_PATH    = os.path.join(PIECE_DIR, "index.html")
ESSAY_PATH   = os.path.join(PIECE_DIR, "essay.md")
THUMB_PATH   = os.path.join(PIECE_DIR, "thumbnail.svg")
README_PATH  = os.path.join(PIECE_DIR, "README.md")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_pieces():
    """Return parsed pieces.json."""
    with open(os.path.join(GALLERY_ROOT, "pieces.json"), encoding="utf-8") as fh:
        return json.load(fh)


def get_piece():
    """Return the pieces.json entry for piece 75, or None."""
    for p in load_pieces():
        if p["id"] == PIECE_ID:
            return p
    return None


def html_text():
    """Return the full index.html content as a string."""
    with open(HTML_PATH, encoding="utf-8") as fh:
        return fh.read()


# ---------------------------------------------------------------------------
# Directory and file layout
# ---------------------------------------------------------------------------

def test_piece_directory_exists():
    assert os.path.isdir(PIECE_DIR), f"Piece directory missing: {PIECE_DIR}"


def test_index_html_exists():
    assert os.path.isfile(HTML_PATH), "index.html missing from piece directory"


def test_essay_md_exists():
    assert os.path.isfile(ESSAY_PATH), "essay.md missing from piece directory"


def test_thumbnail_svg_exists():
    assert os.path.isfile(THUMB_PATH), "thumbnail.svg missing from piece directory"


def test_readme_exists():
    assert os.path.isfile(README_PATH), "README.md missing from piece directory"


# ---------------------------------------------------------------------------
# pieces.json registration
# ---------------------------------------------------------------------------

def test_piece_registered_in_pieces_json():
    piece = get_piece()
    assert piece is not None, f"Piece '{PIECE_ID}' not found in pieces.json"


def test_piece_json_required_fields():
    piece = get_piece()
    if piece is None:
        pytest.skip("Piece not registered")
    for field in ("id", "title", "tagline", "year", "theme", "technique",
                  "path", "thumbnail", "essay"):
        assert field in piece and piece[field], (
            f"Field '{field}' missing or empty in pieces.json entry"
        )


def test_piece_theme_is_matan_torah():
    piece = get_piece()
    if piece is None:
        pytest.skip("Piece not registered")
    assert "Matan Torah" in piece["theme"], (
        f"Expected theme 'Matan Torah', got '{piece['theme']}'"
    )


def test_piece_technique_mentions_ising():
    piece = get_piece()
    if piece is None:
        pytest.skip("Piece not registered")
    assert "Ising" in piece["technique"] or "ising" in piece["technique"].lower(), (
        f"technique field should mention Ising model, got '{piece['technique']}'"
    )


def test_piece_technique_mentions_metropolis():
    piece = get_piece()
    if piece is None:
        pytest.skip("Piece not registered")
    assert "Metropolis" in piece["technique"] or "metropolis" in piece["technique"].lower(), (
        f"technique field should mention Metropolis, got '{piece['technique']}'"
    )


def test_piece_json_path_correct():
    piece = get_piece()
    if piece is None:
        pytest.skip("Piece not registered")
    assert piece["path"] == f"pieces/{PIECE_ID}/index.html"


def test_piece_json_thumbnail_correct():
    piece = get_piece()
    if piece is None:
        pytest.skip("Piece not registered")
    assert piece["thumbnail"] == f"pieces/{PIECE_ID}/thumbnail.svg"


def test_piece_json_essay_correct():
    piece = get_piece()
    if piece is None:
        pytest.skip("Piece not registered")
    assert piece["essay"] == f"pieces/{PIECE_ID}/essay.md"


# ---------------------------------------------------------------------------
# HTML content — Metropolis algorithm
# ---------------------------------------------------------------------------

def test_html_uses_requestanimationframe():
    assert "requestAnimationFrame" in html_text(), (
        "index.html must use requestAnimationFrame for animation"
    )


def test_html_contains_metropolis_function():
    html = html_text()
    assert "metropolis" in html.lower(), (
        "index.html must contain a metropolisStep function"
    )


def test_html_ising_grid_size_200():
    html = html_text()
    assert "200" in html, "index.html must reference N=200 grid size"
    assert re.search(r"N\s*=\s*200", html) or re.search(r"const N = 200", html), (
        "index.html must define N=200"
    )


def test_html_uses_int8array():
    assert "Int8Array" in html_text(), (
        "index.html must use Int8Array for efficient spin storage"
    )


def test_html_computes_delta_e():
    html = html_text()
    assert "dE" in html or "deltaE" in html or "delta_e" in html, (
        "index.html must compute energy change (dE) for the Metropolis criterion"
    )


def test_html_uses_putimagedata():
    assert "putImageData" in html_text(), (
        "index.html must render via putImageData for pixel-level control"
    )


def test_html_periodic_boundary_conditions():
    html = html_text()
    assert "% N" in html, (
        "index.html must implement periodic boundary conditions (modulo N)"
    )


# ---------------------------------------------------------------------------
# HTML content — temperature schedule
# ---------------------------------------------------------------------------

def test_html_temperature_start():
    html = html_text()
    assert "4.5" in html, "index.html must start temperature at T=4.5"


def test_html_temperature_stop():
    html = html_text()
    assert "1.5" in html, "index.html must stop temperature at T=1.5"


def test_html_temperature_pause_near_critical():
    html = html_text()
    assert "2.4" in html or "2.269" in html, (
        "index.html must pause near critical temperature (T≈2.4 or T_c≈2.269)"
    )


def test_html_temperature_step():
    html = html_text()
    assert "0.001" in html, (
        "index.html must decrease temperature by 0.001 per tick"
    )


def test_html_pause_frames_300():
    html = html_text()
    assert "300" in html, (
        "index.html must define 300-frame pauses at critical point and hold"
    )


# ---------------------------------------------------------------------------
# HTML content — color palette
# ---------------------------------------------------------------------------

def test_html_gold_color():
    html = html_text()
    assert "E8C438" in html or "232" in html, (
        "index.html must define gold color #E8C438 (warm wheat gold) for spin +1"
    )


def test_html_blue_color():
    html = html_text()
    assert "1A3068" in html or "1a3068" in html.lower(), (
        "index.html must define blue color #1A3068 (deep sapphire) for spin -1"
    )


# ---------------------------------------------------------------------------
# HTML content — overlay and temperature display
# ---------------------------------------------------------------------------

def test_html_hebrew_text_overlay():
    html = html_text()
    assert "כְּאִישׁ אֶחָד בְּלֵב אֶחָד" in html, (
        "index.html must contain the Hebrew phrase כְּאִישׁ אֶחָד בְּלֵב אֶחָד"
    )


def test_html_text_threshold_below_1_8():
    html = html_text()
    assert "1.8" in html, (
        "index.html must show Hebrew text only when T < 1.8"
    )


def test_html_temperature_readout():
    html = html_text()
    assert "temp" in html.lower() or "T = " in html or "toFixed" in html, (
        "index.html must display a temperature readout (e.g., 'T = X.XX')"
    )


def test_html_cream_text_color():
    html = html_text()
    assert "F5F0E0" in html or "f5f0e0" in html.lower(), (
        "index.html must use cream color #F5F0E0 for the Hebrew overlay text"
    )


# ---------------------------------------------------------------------------
# HTML content — essay embedded
# ---------------------------------------------------------------------------

def test_html_embeds_essay_rashi():
    html = html_text()
    assert "Rashi" in html, (
        "index.html must embed essay text mentioning Rashi"
    )


def test_html_embeds_essay_sinai():
    html = html_text()
    assert "Sinai" in html or "sinai" in html.lower(), (
        "index.html must embed essay text mentioning Sinai"
    )


def test_html_embeds_essay_naaseh_vnishma():
    html = html_text()
    assert "naaseh" in html.lower() or "naaseh" in html or "נַעֲשֶׂה" in html, (
        "index.html must embed essay text referencing naaseh v'nishma"
    )


# ---------------------------------------------------------------------------
# Essay content
# ---------------------------------------------------------------------------

def test_essay_minimum_words():
    with open(ESSAY_PATH, encoding="utf-8") as fh:
        text = fh.read()
    word_count = len(text.split())
    assert word_count >= 300, (
        f"essay.md has only {word_count} words; need at least 300 (~360 target)"
    )


def test_essay_mentions_rashi():
    with open(ESSAY_PATH, encoding="utf-8") as fh:
        text = fh.read()
    assert "Rashi" in text, "essay.md must mention Rashi's commentary"


def test_essay_mentions_phase_transition():
    with open(ESSAY_PATH, encoding="utf-8") as fh:
        text = fh.read()
    assert "phase transition" in text.lower() or "phase-transition" in text.lower(), (
        "essay.md must discuss the phase transition"
    )


def test_essay_mentions_shavuot():
    with open(ESSAY_PATH, encoding="utf-8") as fh:
        text = fh.read()
    assert "Shavuot" in text or "shavuot" in text.lower(), (
        "essay.md must connect the piece to Shavuot"
    )


def test_essay_mentions_naaseh_vnishma():
    with open(ESSAY_PATH, encoding="utf-8") as fh:
        text = fh.read()
    assert "naaseh" in text.lower() or "נַעֲשֶׂה" in text, (
        "essay.md must reference naaseh v'nishma (Exodus 24:7)"
    )


def test_essay_mentions_critical_temperature():
    with open(ESSAY_PATH, encoding="utf-8") as fh:
        text = fh.read()
    assert "2.269" in text or "T_c" in text or "critical" in text.lower(), (
        "essay.md must mention the critical temperature or 'critical' threshold"
    )


# ---------------------------------------------------------------------------
# Thumbnail validity
# ---------------------------------------------------------------------------

def test_thumbnail_is_valid_svg():
    with open(THUMB_PATH, encoding="utf-8") as fh:
        text = fh.read()
    assert "<svg" in text and "</svg>" in text, (
        "thumbnail.svg does not appear to be valid SVG"
    )


def test_thumbnail_contains_gold_color():
    with open(THUMB_PATH, encoding="utf-8") as fh:
        text = fh.read()
    assert "E8C438" in text or "e8c438" in text.lower(), (
        "thumbnail.svg must use gold color #E8C438"
    )


def test_thumbnail_contains_blue_color():
    with open(THUMB_PATH, encoding="utf-8") as fh:
        text = fh.read()
    assert "1A3068" in text or "1a3068" in text.lower(), (
        "thumbnail.svg must use blue color #1A3068"
    )


def test_thumbnail_is_400x400():
    with open(THUMB_PATH, encoding="utf-8") as fh:
        text = fh.read()
    assert 'width="400"' in text and 'height="400"' in text, (
        "thumbnail.svg must be 400×400 pixels"
    )


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

def test_piece_id_unique_in_pieces_json():
    """Duplicate IDs would break gallery routing."""
    ids = [p["id"] for p in load_pieces()]
    assert ids.count(PIECE_ID) == 1, (
        f"'{PIECE_ID}' appears {ids.count(PIECE_ID)} times in pieces.json (must be exactly 1)"
    )


def test_piece_files_all_nonempty():
    """Catches stub files accidentally committed as zero-length placeholders."""
    for path in (HTML_PATH, ESSAY_PATH, THUMB_PATH, README_PATH):
        size = os.path.getsize(path)
        assert size > 0, f"File is empty: {path}"


def test_html_has_full_viewport_canvas():
    html = html_text()
    assert "100vh" in html or "100%" in html, (
        "index.html must use full-viewport sizing for the canvas panel"
    )
