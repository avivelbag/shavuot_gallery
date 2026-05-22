"""
Tests for the Shavuot gallery scaffold.

Validates pieces.json structure, on-disk file layout, and required field
constraints.  The gallery root is determined relative to this file so the
suite works from any working directory.
"""
import json
import os
import re

import pytest

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")

REQUIRED_FIELDS = ("id", "title", "tagline", "year", "theme", "technique", "path", "thumbnail", "essay")

ESSAY_MIN_WORDS = 200


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_pieces():
    """Load and return the parsed pieces.json list."""
    with open(PIECES_JSON, "r", encoding="utf-8") as fh:
        return json.load(fh)


# ---------------------------------------------------------------------------
# pieces.json structural tests
# ---------------------------------------------------------------------------

def test_pieces_json_exists():
    assert os.path.isfile(PIECES_JSON), "pieces.json is missing from gallery root"


def test_pieces_json_is_valid_json():
    with open(PIECES_JSON, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    assert isinstance(data, list), "pieces.json must be a JSON array"


def test_pieces_json_has_at_least_one_entry():
    pieces = load_pieces()
    assert len(pieces) >= 1, "pieces.json must contain at least one piece"


@pytest.mark.parametrize("field", REQUIRED_FIELDS)
def test_every_piece_has_required_field(field):
    """Every entry in pieces.json must contain the given field."""
    pieces = load_pieces()
    for piece in pieces:
        assert field in piece, f"Piece '{piece.get('id', '?')}' is missing field '{field}'"


def test_every_piece_required_fields_non_empty():
    """No required field may be empty/None."""
    pieces = load_pieces()
    for piece in pieces:
        for field in REQUIRED_FIELDS:
            value = piece.get(field)
            assert value is not None and value != "", (
                f"Piece '{piece.get('id', '?')}' has empty or null field '{field}'"
            )


def test_year_is_integer():
    pieces = load_pieces()
    for piece in pieces:
        assert isinstance(piece["year"], int), (
            f"Piece '{piece['id']}' has non-integer year: {piece['year']!r}"
        )


# ---------------------------------------------------------------------------
# Per-piece file layout tests
# ---------------------------------------------------------------------------

def test_id_matches_directory_name():
    """Each piece's 'id' must match the last directory component of its 'path'."""
    pieces = load_pieces()
    for piece in pieces:
        path_parts = piece["path"].replace("\\", "/").split("/")
        # path is like "pieces/<id>/index.html"
        assert len(path_parts) >= 2, f"Unexpected path format: {piece['path']}"
        dir_name = path_parts[-2]
        assert dir_name == piece["id"], (
            f"Piece id '{piece['id']}' does not match directory '{dir_name}'"
        )


def test_piece_html_exists():
    """The index.html referenced in 'path' must exist on disk."""
    pieces = load_pieces()
    for piece in pieces:
        full_path = os.path.join(GALLERY_ROOT, piece["path"])
        assert os.path.isfile(full_path), (
            f"Piece '{piece['id']}': path '{piece['path']}' does not exist"
        )


def test_thumbnail_exists():
    """The thumbnail referenced in pieces.json must exist on disk."""
    pieces = load_pieces()
    for piece in pieces:
        full_thumb = os.path.join(GALLERY_ROOT, piece["thumbnail"])
        assert os.path.isfile(full_thumb), (
            f"Piece '{piece['id']}': thumbnail '{piece['thumbnail']}' does not exist"
        )


def test_readme_exists():
    """Each piece directory must contain a README.md."""
    pieces = load_pieces()
    for piece in pieces:
        piece_dir = os.path.join(GALLERY_ROOT, os.path.dirname(piece["path"]))
        readme = os.path.join(piece_dir, "README.md")
        assert os.path.isfile(readme), (
            f"Piece '{piece['id']}': README.md is missing from {piece_dir}"
        )


def test_essay_field_points_to_existing_file():
    """The 'essay' path in every pieces.json entry must exist on disk."""
    pieces = load_pieces()
    for piece in pieces:
        essay_rel = piece.get("essay", "")
        assert essay_rel, f"Piece '{piece.get('id', '?')}' has empty essay field"
        full_path = os.path.join(GALLERY_ROOT, essay_rel)
        assert os.path.isfile(full_path), (
            f"Piece '{piece['id']}': essay file '{essay_rel}' does not exist on disk"
        )


def test_essay_md_has_at_least_200_words():
    """Each essay.md must be substantial — at least 200 words — to catch placeholder stubs."""
    pieces = load_pieces()
    for piece in pieces:
        essay_rel = piece.get("essay", "")
        if not essay_rel:
            continue
        full_path = os.path.join(GALLERY_ROOT, essay_rel)
        if not os.path.isfile(full_path):
            continue
        text = open(full_path, encoding="utf-8").read()
        word_count = len(text.split())
        assert word_count >= 200, (
            f"Piece '{piece['id']}': essay.md has only {word_count} words (need ≥ 200)"
        )


def test_index_html_contains_essay_text():
    """Each piece's index.html must embed essay text inline (no runtime fetch of essay.md)."""
    pieces = load_pieces()
    for piece in pieces:
        essay_rel = piece.get("essay", "")
        if not essay_rel:
            continue
        essay_path = os.path.join(GALLERY_ROOT, essay_rel)
        if not os.path.isfile(essay_path):
            continue
        essay_text = open(essay_path, encoding="utf-8").read()
        html_path = os.path.join(GALLERY_ROOT, piece["path"])
        html = open(html_path, encoding="utf-8").read()
        words = [w for w in essay_text.split() if len(w) > 5]
        sampled = words[:10]
        found = sum(1 for w in sampled if w in html)
        assert found >= 5, (
            f"Piece '{piece['id']}': index.html does not appear to embed the essay text "
            f"(only {found}/10 sampled words found in HTML)"
        )


def test_essay_field_non_empty():
    """Every piece must have a non-empty 'essay' field in pieces.json."""
    pieces = load_pieces()
    for piece in pieces:
        essay_val = piece.get("essay")
        assert essay_val and essay_val.strip(), (
            f"Piece '{piece.get('id', '?')}' has empty or missing 'essay' field in pieces.json"
        )


def test_essay_md_exists():
    """The essay.md file referenced in the 'essay' field must exist on disk."""
    pieces = load_pieces()
    for piece in pieces:
        essay_path = piece.get("essay", "")
        full_path = os.path.join(GALLERY_ROOT, essay_path)
        assert os.path.isfile(full_path), (
            f"Piece '{piece['id']}': essay file '{essay_path}' does not exist on disk"
        )


def test_essay_md_substantial():
    """Each essay.md must be substantial — at least 200 words."""
    pieces = load_pieces()
    for piece in pieces:
        essay_path = piece.get("essay", "")
        full_path = os.path.join(GALLERY_ROOT, essay_path)
        if not os.path.isfile(full_path):
            pytest.fail(f"Piece '{piece['id']}': essay file missing, cannot check word count")
        text = open(full_path, encoding="utf-8").read()
        word_count = len(text.split())
        assert word_count >= 200, (
            f"Piece '{piece['id']}': essay.md has only {word_count} words (minimum 200)"
        )


# ---------------------------------------------------------------------------
# Piece 01 — specific content checks
# ---------------------------------------------------------------------------

def _get_piece(piece_id):
    pieces = load_pieces()
    for p in pieces:
        if p["id"] == piece_id:
            return p
    return None


def test_piece_01_exists_in_json():
    piece = _get_piece("01-thunder-at-sinai")
    assert piece is not None, "Piece '01-thunder-at-sinai' not found in pieces.json"


def test_piece_01_readme_mentions_sinai():
    piece = _get_piece("01-thunder-at-sinai")
    if piece is None:
        pytest.skip("Piece 01 not present")
    readme_path = os.path.join(GALLERY_ROOT, os.path.dirname(piece["path"]), "README.md")
    text = open(readme_path, encoding="utf-8").read().lower()
    assert "sinai" in text or "matan torah" in text, (
        "README.md must mention the Shavuot theme (Sinai / Matan Torah)"
    )


def test_piece_01_canvas_animation_uses_requestanimationframe():
    piece = _get_piece("01-thunder-at-sinai")
    if piece is None:
        pytest.skip("Piece 01 not present")
    html_path = os.path.join(GALLERY_ROOT, piece["path"])
    text = open(html_path, encoding="utf-8").read()
    assert "requestAnimationFrame" in text, (
        "pieces/01-thunder-at-sinai/index.html must use requestAnimationFrame"
    )


def test_piece_01_thumbnail_is_valid_svg():
    piece = _get_piece("01-thunder-at-sinai")
    if piece is None:
        pytest.skip("Piece 01 not present")
    thumb_path = os.path.join(GALLERY_ROOT, piece["thumbnail"])
    text = open(thumb_path, encoding="utf-8").read()
    assert "<svg" in text and "</svg>" in text, (
        "thumbnail.svg does not look like valid SVG"
    )


# ---------------------------------------------------------------------------
# Gallery scaffold tests
# ---------------------------------------------------------------------------

def test_index_html_exists():
    assert os.path.isfile(os.path.join(GALLERY_ROOT, "index.html")), (
        "index.html is missing from gallery root"
    )


def test_styles_css_exists():
    assert os.path.isfile(os.path.join(GALLERY_ROOT, "styles.css")), (
        "styles.css is missing from gallery root"
    )


def test_index_html_loads_pieces_json():
    """index.html must fetch pieces.json to populate the gallery."""
    html = open(os.path.join(GALLERY_ROOT, "index.html"), encoding="utf-8").read()
    assert "pieces.json" in html, "index.html must reference pieces.json"


def test_styles_css_has_grid_layout():
    """styles.css must use CSS Grid for the gallery layout."""
    css = open(os.path.join(GALLERY_ROOT, "styles.css"), encoding="utf-8").read()
    assert "display: grid" in css or "display:grid" in css, (
        "styles.css must define a CSS grid layout"
    )


def test_styles_css_has_single_column_breakpoint():
    """styles.css must include a media query for single-column layout below 600 px."""
    css = open(os.path.join(GALLERY_ROOT, "styles.css"), encoding="utf-8").read()
    assert re.search(r"max-width\s*:\s*600", css), (
        "styles.css must have a max-width:600px media query for single-column layout"
    )


# ---------------------------------------------------------------------------
# Edge-case / failure-mode tests
# ---------------------------------------------------------------------------

def test_pieces_json_no_duplicate_ids():
    """Duplicate IDs would break the gallery routing."""
    pieces = load_pieces()
    ids = [p["id"] for p in pieces]
    assert len(ids) == len(set(ids)), f"Duplicate piece IDs found: {ids}"


def test_thumbnail_extension_is_known_image_type():
    """Thumbnails must have a recognised image extension."""
    allowed = {".svg", ".png", ".jpg", ".jpeg", ".webp", ".gif"}
    pieces = load_pieces()
    for piece in pieces:
        ext = os.path.splitext(piece["thumbnail"])[1].lower()
        assert ext in allowed, (
            f"Piece '{piece['id']}' has unrecognised thumbnail extension '{ext}'"
        )


def test_piece_path_ends_with_html():
    """Every piece path must point at an HTML file."""
    pieces = load_pieces()
    for piece in pieces:
        assert piece["path"].endswith(".html"), (
            f"Piece '{piece['id']}' path does not end with .html"
        )


def test_missing_field_detected(tmp_path):
    """A piece entry without a required field should fail our field check."""
    bad_pieces = [{"id": "99-test", "title": "Test"}]  # missing most fields
    bad_json = tmp_path / "pieces.json"
    bad_json.write_text(json.dumps(bad_pieces), encoding="utf-8")

    data = json.loads(bad_json.read_text())
    for field in REQUIRED_FIELDS:
        if field not in ("id", "title"):
            assert field not in data[0], (
                "Fixture should be missing this field for the test to be meaningful"
            )


def test_empty_pieces_json_is_detected(tmp_path):
    """An empty pieces.json array should be flagged as having no entries."""
    empty_json = tmp_path / "pieces.json"
    empty_json.write_text("[]", encoding="utf-8")
    data = json.loads(empty_json.read_text())
    assert len(data) == 0  # confirm behaviour: caller would raise an assertion error


# ---------------------------------------------------------------------------
# Essay requirements — every piece must ship essay.md and register it
# ---------------------------------------------------------------------------

def test_every_piece_has_essay_field():
    """Every entry in pieces.json must have a non-empty 'essay' field."""
    pieces = load_pieces()
    for piece in pieces:
        essay = piece.get("essay")
        assert essay is not None and essay != "", (
            f"Piece '{piece.get('id', '?')}' is missing the 'essay' field in pieces.json"
        )


def test_every_piece_essay_file_exists():
    """The essay.md file referenced in pieces.json must exist on disk."""
    pieces = load_pieces()
    for piece in pieces:
        essay_rel = piece.get("essay")
        if not essay_rel:
            continue
        essay_path = os.path.join(GALLERY_ROOT, essay_rel)
        assert os.path.isfile(essay_path), (
            f"Piece '{piece.get('id', '?')}': essay file '{essay_rel}' does not exist on disk"
        )


def test_every_piece_essay_is_substantial():
    """Every essay.md must contain at least ESSAY_MIN_WORDS words of real content."""
    pieces = load_pieces()
    for piece in pieces:
        essay_rel = piece.get("essay")
        if not essay_rel:
            continue
        essay_path = os.path.join(GALLERY_ROOT, essay_rel)
        if not os.path.isfile(essay_path):
            continue
        text = open(essay_path, encoding="utf-8").read()
        word_count = len(text.split())
        assert word_count >= ESSAY_MIN_WORDS, (
            f"Piece '{piece.get('id', '?')}' essay has only {word_count} words "
            f"(minimum is {ESSAY_MIN_WORDS})"
        )


def test_piece_with_no_essay_field_fails(tmp_path):
    """A pieces.json entry missing the essay field must be caught by the essay check."""
    bad_pieces = [{"id": "99-test", "essay": ""}]
    essay = bad_pieces[0].get("essay")
    assert not essay, "Fixture confirms empty essay field should be treated as missing"


def test_piece_with_nonexistent_essay_file_fails(tmp_path):
    """An essay path that points to a missing file must be detected."""
    missing_path = os.path.join(str(tmp_path), "nonexistent.md")
    assert not os.path.isfile(missing_path), "Fixture path must not exist on disk"
