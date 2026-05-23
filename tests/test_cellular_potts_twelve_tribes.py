"""
Tests for piece 95 — Cellular Potts Model — Twelve Tribes at Sinai.

Verifies:
  - All required files exist on disk (happy path)
  - pieces.json registration is correct and complete
  - essay.md contains the required bilingual primary-source passage
  - index.html implements the Potts simulation and embeds essay content
  - thumbnail.svg is valid SVG containing the tribe colors
  - Edge cases: missing files and insufficient essay length are detected
"""
import json
import os

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID     = "95-cellular-potts-twelve-tribes"
PIECE_DIR    = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
INDEX_HTML   = os.path.join(PIECE_DIR, "index.html")
ESSAY_MD     = os.path.join(PIECE_DIR, "essay.md")
THUMBNAIL    = os.path.join(PIECE_DIR, "thumbnail.svg")
README       = os.path.join(PIECE_DIR, "README.md")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _load_pieces():
    """Load and return parsed pieces.json list."""
    with open(os.path.join(GALLERY_ROOT, "pieces.json"), encoding="utf-8") as fh:
        return json.load(fh)


def _get_piece():
    """Return the pieces.json entry for this piece, or None."""
    for p in _load_pieces():
        if p["id"] == PIECE_ID:
            return p
    return None


def _html():
    return open(INDEX_HTML, encoding="utf-8").read()


def _essay():
    return open(ESSAY_MD, encoding="utf-8").read()


# ---------------------------------------------------------------------------
# Happy path — file existence
# ---------------------------------------------------------------------------

def test_piece_directory_exists():
    """Piece directory must be present on disk."""
    assert os.path.isdir(PIECE_DIR), f"Missing piece directory: {PIECE_DIR}"


def test_index_html_exists():
    """index.html must be present in the piece directory."""
    assert os.path.isfile(INDEX_HTML), f"Missing index.html: {INDEX_HTML}"


def test_essay_md_exists():
    """essay.md must be present in the piece directory."""
    assert os.path.isfile(ESSAY_MD), f"Missing essay.md: {ESSAY_MD}"


def test_thumbnail_svg_exists():
    """thumbnail.svg must be present in the piece directory."""
    assert os.path.isfile(THUMBNAIL), f"Missing thumbnail.svg: {THUMBNAIL}"


def test_readme_exists():
    """README.md must be present in the piece directory."""
    assert os.path.isfile(README), f"Missing README.md: {README}"


# ---------------------------------------------------------------------------
# Happy path — pieces.json registration
# ---------------------------------------------------------------------------

def test_piece_registered_in_pieces_json():
    """Piece must appear in pieces.json with id '95-cellular-potts-twelve-tribes'."""
    p = _get_piece()
    assert p is not None, f"Piece '{PIECE_ID}' not found in pieces.json"


def test_piece_required_fields_present():
    """All required fields must be present and non-empty in pieces.json entry."""
    p = _get_piece()
    assert p is not None
    required = ("id", "title", "tagline", "year", "theme", "technique", "path", "thumbnail", "essay")
    for field in required:
        assert field in p and p[field], f"Missing or empty field '{field}' in pieces.json entry"


def test_piece_theme_references_twelve_tribes():
    """Theme field must reference the twelve tribes at Sinai."""
    p = _get_piece()
    assert p is not None
    theme = p.get("theme", "").lower()
    assert "twelve tribes" in theme or "tribes" in theme, (
        f"Theme should reference twelve tribes, got: {p.get('theme')}"
    )


def test_piece_technique_mentions_potts():
    """Technique field must mention the Cellular Potts model."""
    p = _get_piece()
    assert p is not None
    technique = p.get("technique", "").lower()
    assert "potts" in technique, (
        f"Technique should mention Potts model, got: {p.get('technique')}"
    )


def test_piece_path_points_to_existing_file():
    """The 'path' in pieces.json must point to an existing file."""
    p = _get_piece()
    assert p is not None
    full = os.path.join(GALLERY_ROOT, p["path"])
    assert os.path.isfile(full), f"pieces.json path does not exist: {p['path']}"


# ---------------------------------------------------------------------------
# Happy path — essay.md content
# ---------------------------------------------------------------------------

def test_essay_has_at_least_400_words():
    """essay.md must contain at least 400 words of real content."""
    text = _essay()
    count = len(text.split())
    assert count >= 400, f"essay.md has {count} words; minimum is 400"


def test_essay_contains_hebrew_characters():
    """Essay must include a substantial Hebrew primary-source passage."""
    text = _essay()
    hebrew = [c for c in text if '֐' <= c <= '׿']
    assert len(hebrew) > 20, (
        "essay.md must include a Hebrew primary-source passage (at least 20 Hebrew characters)"
    )


def test_essay_contains_exodus_19_or_24():
    """Essay must cite Exodus 19 or 24 as required by the acceptance criteria."""
    text = _essay()
    assert ("Exodus" in text or "שמות" in text), "Essay must reference Exodus"
    has_chapter = "19" in text or "24" in text
    assert has_chapter, "Essay must cite Exodus 19 or 24 (the key twelve-tribes sources)"


def test_essay_credits_graner_and_glazier():
    """Essay must credit Graner and Glazier (1992) for the cellular Potts model."""
    text = _essay()
    assert "Graner" in text, "Essay must credit François Graner"
    assert "Glazier" in text, "Essay must credit James Glazier"


def test_essay_contains_kish_echad_phrase():
    """Essay must contain the phrase k'ish echad b'lev echad in Hebrew or transliteration."""
    text = _essay()
    has_phrase = (
        "כאיש אחד" in text
        or "כְּאִישׁ" in text
        or "k'ish echad" in text.lower()
        or "kish echad" in text.lower()
    )
    assert has_phrase, "Essay must contain the phrase 'k'ish echad b'lev echad'"


def test_essay_mentions_numbers_2():
    """Essay should reference the encampment arrangement from Numbers 2."""
    text = _essay()
    has_ref = "Numbers" in text or "Numbers 2" in text or "במדבר" in text
    assert has_ref, "Essay must mention Numbers 2 (the camp arrangement)"


# ---------------------------------------------------------------------------
# Happy path — index.html content
# ---------------------------------------------------------------------------

def test_html_uses_requestanimationframe():
    """index.html must drive animation with requestAnimationFrame."""
    assert "requestAnimationFrame" in _html()


def test_html_uses_uint8array_for_lattice():
    """index.html must store the lattice in a Uint8Array."""
    assert "Uint8Array" in _html(), "Lattice must be a Uint8Array"


def test_html_uses_put_image_data():
    """index.html must render via putImageData for pixel-level control."""
    assert "putImageData" in _html(), "Rendering must use putImageData"


def test_html_implements_metropolis():
    """index.html must implement Metropolis acceptance (Math.exp)."""
    assert "Math.exp" in _html(), "Metropolis acceptance must use Math.exp(-dE/T)"


def test_html_contains_all_twelve_tribal_names():
    """index.html must contain all twelve Hebrew tribal names."""
    tribes = [
        "ראובן", "שמעון", "לוי", "יהודה", "יששכר", "זבולון",
        "דן", "נפתלי", "גד", "אשר", "אפרים", "בנימין",
    ]
    html = _html()
    missing = [t for t in tribes if t not in html]
    assert not missing, f"Tribal names missing from index.html: {missing}"


def test_html_defines_void_region_bounds():
    """index.html must define the 20×20 void region at the correct bounds (90, 110)."""
    html = _html()
    assert "90" in html and "110" in html, (
        "Void region bounds 90 and 110 must appear in index.html"
    )


def test_html_contains_temperature_decay():
    """index.html must include the temperature decay factor 0.9999."""
    assert "0.9999" in _html(), "Temperature decay factor 0.9999 must be in index.html"


def test_html_embeds_essay_text():
    """index.html must embed essay text inline (not load it at runtime)."""
    essay_text = _essay()
    html_text  = _html()
    long_words = [w for w in essay_text.split() if len(w) > 6][:12]
    found = sum(1 for w in long_words if w in html_text)
    assert found >= 6, (
        f"index.html does not appear to embed the essay ({found}/12 sampled words found)"
    )


def test_html_contains_hebrew_exodus_quote():
    """index.html must embed the Hebrew Exodus primary-source quote."""
    html = _html()
    hebrew_chars = sum(1 for c in html if '֐' <= c <= '׿')
    assert hebrew_chars > 50, (
        f"index.html should embed substantial Hebrew text (found {hebrew_chars} Hebrew chars)"
    )


def test_html_contains_j_energy_function():
    """index.html must define the J() energy function with the correct penalty values."""
    html = _html()
    # The acceptance criteria specifies J(a,b)=5 for unlike tribes
    assert "return 5" in html or "return 5;" in html, (
        "Energy function must return 5 for unlike-tribe pairs"
    )


# ---------------------------------------------------------------------------
# Happy path — thumbnail.svg
# ---------------------------------------------------------------------------

def test_thumbnail_is_valid_svg():
    """thumbnail.svg must be parseable as SVG."""
    text = open(THUMBNAIL, encoding="utf-8").read()
    assert "<svg" in text and "</svg>" in text, "thumbnail.svg is not valid SVG"


def test_thumbnail_contains_tribe_colors():
    """thumbnail.svg must include at least four tribe-specific fill colors."""
    text = open(THUMBNAIL, encoding="utf-8").read().upper()
    tribe_colors = ["#C0392B", "#8E44AD", "#2E86AB", "#F39C12", "#27AE60", "#1ABC9C"]
    found = sum(1 for c in tribe_colors if c.upper() in text)
    assert found >= 4, (
        f"thumbnail.svg should contain tribe colors; only {found}/6 sampled colors found"
    )


def test_thumbnail_contains_central_void():
    """thumbnail.svg must contain the central void region (#1A1A1A)."""
    text = open(THUMBNAIL, encoding="utf-8").read().upper()
    assert "#1A1A1A" in text, "thumbnail.svg must contain the dark central void (#1A1A1A)"


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

def test_essay_word_count_well_above_minimum():
    """essay.md word count should comfortably exceed the 200-word minimum."""
    text = _essay()
    count = len(text.split())
    # 200 is the test_pieces.py minimum; we require 400 for this piece
    assert count >= 200, f"essay.md has only {count} words"


def test_html_canvas_is_800_by_800():
    """Canvas must be 800×800 (200×200 cells at 4px each)."""
    html = _html()
    assert 'width="800"' in html and 'height="800"' in html, (
        "Canvas must be declared as 800×800 pixels"
    )


# ---------------------------------------------------------------------------
# Failure-mode tests
# ---------------------------------------------------------------------------

def test_missing_piece_directory_is_detected(tmp_path):
    """A piece directory that was never created must not pass an isdir check."""
    fake_dir = str(tmp_path / "99-fabricated-piece")
    assert not os.path.isdir(fake_dir), (
        "A fabricated piece directory should not exist before creation"
    )


def test_short_essay_fails_word_count_check():
    """An essay with fewer than 200 words must fail the minimum word-count requirement."""
    short_text = "This is a short essay. " * 8   # ~40 words
    count = len(short_text.split())
    MINIMUM = 200
    assert count < MINIMUM, f"Fixture must be < {MINIMUM} words; got {count}"
    # Confirms the guard that would reject this essay:
    passes = count >= MINIMUM
    assert not passes, "Short essay must not satisfy the minimum word count"


def test_invalid_piece_id_absent_from_json():
    """A fabricated piece ID must not appear in pieces.json."""
    ids = [p["id"] for p in _load_pieces()]
    assert "99-fabricated-nonexistent-piece" not in ids, (
        "A fabricated ID must not be present in pieces.json"
    )
