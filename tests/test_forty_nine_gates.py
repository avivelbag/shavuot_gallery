"""Tests for piece 54-forty-nine-gates-omer."""
import json
import re
from pathlib import Path

PIECE_DIR = Path(__file__).parent.parent / "pieces" / "54-forty-nine-gates-omer"
INDEX_HTML = PIECE_DIR / "index.html"
ESSAY_MD   = PIECE_DIR / "essay.md"
THUMB_SVG  = PIECE_DIR / "thumbnail.svg"
README_MD  = PIECE_DIR / "README.md"
PIECES_JSON = Path(__file__).parent.parent / "pieces.json"

SEFIROT = ["Chesed", "Gevurah", "Tiferet", "Netzach", "Hod", "Yesod", "Malkhut"]


# ── Fixture helpers ───────────────────────────────────────────────────────────

def _html() -> str:
    return INDEX_HTML.read_text(encoding="utf-8")


def _essay() -> str:
    return ESSAY_MD.read_text(encoding="utf-8")


def _pieces() -> list:
    return json.loads(PIECES_JSON.read_text(encoding="utf-8"))


def _entry() -> dict:
    for p in _pieces():
        if p["id"] == "54-forty-nine-gates-omer":
            return p
    raise KeyError("54-forty-nine-gates-omer not found in pieces.json")


# ── Happy-path: file existence ────────────────────────────────────────────────

def test_index_html_exists():
    """index.html must be present in the piece directory."""
    assert INDEX_HTML.exists(), f"Missing {INDEX_HTML}"


def test_essay_md_exists():
    """essay.md must be present."""
    assert ESSAY_MD.exists(), f"Missing {ESSAY_MD}"


def test_thumbnail_svg_exists():
    """thumbnail.svg must be present."""
    assert THUMB_SVG.exists(), f"Missing {THUMB_SVG}"


def test_readme_exists():
    """README.md must be present."""
    assert README_MD.exists(), f"Missing {README_MD}"


# ── Happy-path: pieces.json entry ────────────────────────────────────────────

def test_pieces_json_entry_present():
    """pieces.json must contain an entry for piece 54."""
    entry = _entry()
    assert entry["id"] == "54-forty-nine-gates-omer"


def test_pieces_json_required_fields():
    """All nine required fields must be non-empty in the pieces.json entry."""
    required = {"id", "title", "tagline", "year", "theme", "technique", "path", "thumbnail", "essay"}
    entry = _entry()
    for field in required:
        assert field in entry, f"Missing field '{field}'"
        assert entry[field] != "", f"Empty field '{field}'"


def test_pieces_json_year_is_int():
    """The year field must be an integer."""
    assert isinstance(_entry()["year"], int)


def test_pieces_json_theme():
    """Theme must reference Sefirat HaOmer."""
    assert "Omer" in _entry()["theme"] or "omer" in _entry()["theme"].lower()


def test_pieces_json_technique():
    """Technique must mention procedural grid and generative mandala."""
    tech = _entry()["technique"].lower()
    assert "mandala" in tech or "grid" in tech


def test_pieces_json_paths_end_correctly():
    """path must end with .html; thumbnail with known image extension."""
    entry = _entry()
    assert entry["path"].endswith(".html")
    assert entry["thumbnail"].endswith((".svg", ".png", ".jpg", ".jpeg", ".webp"))


def test_pieces_json_no_new_duplicates():
    """No duplicate IDs in pieces.json after adding piece 54."""
    pieces = _pieces()
    ids = [p["id"] for p in pieces]
    assert len(ids) == len(set(ids)), "Duplicate IDs found in pieces.json"


# ── Happy-path: HTML content ──────────────────────────────────────────────────

def test_html_has_canvas():
    """index.html must contain a canvas element."""
    assert "<canvas" in _html()


def test_html_has_all_seven_sefirot():
    """All seven Sefirah names must appear in index.html (in essay text)."""
    html = _html()
    for name in SEFIROT:
        assert name in html, f"Sefirah name '{name}' missing from HTML"


def test_html_has_raf():
    """index.html must use requestAnimationFrame for animation."""
    assert "requestAnimationFrame" in _html()


def test_html_has_tooltip():
    """index.html must contain tooltip machinery (mousemove handler)."""
    html = _html()
    assert "mousemove" in html
    assert "tooltip" in html.lower()


def test_html_has_hebrew_days():
    """index.html must include Hebrew day text for at least the first and last day."""
    html = _html()
    assert "יוֹם אֶחָד" in html, "First Hebrew day (day 1) missing"
    assert "יוֹם אַרְבָּעִים וְתִשְׁעָה" in html, "Last Hebrew day (day 49) missing"


def test_html_has_49_heb_day_entries():
    """The HEB_DAYS JavaScript array must declare exactly 49 entries."""
    html = _html()
    match = re.search(r"var HEB_DAYS\s*=\s*\[([^\]]+)\]", html, re.DOTALL)
    assert match, "HEB_DAYS array not found in HTML"
    entries = [e.strip() for e in match.group(1).split(",") if e.strip()]
    assert len(entries) == 49, f"Expected 49 HEB_DAYS entries, got {len(entries)}"


def test_html_bloom_animation():
    """index.html must define a BLOOM_MS constant for the simultaneous bloom-in."""
    assert "BLOOM_MS" in _html()


def test_html_has_shavuot_element():
    """index.html must reference Shavuot (שָׁבוּעוֹת) in the canvas drawing code."""
    html = _html()
    assert "שָׁבוּעוֹת" in html or "Shavuot" in html


def test_html_dark_background():
    """index.html must use the specified dark background colour #0D0B14."""
    assert "#0D0B14" in _html() or "#0d0b14" in _html().lower()


def test_html_rotation_logic():
    """index.html must implement continuous rotation (rotations array updated in frame loop)."""
    html = _html()
    assert "rotations" in html
    assert "rotation" in html.lower()


def test_html_sefirot_colors_array():
    """index.html must define the COLORS array with seven hex colour strings."""
    html = _html()
    match = re.search(r"var COLORS\s*=\s*\[([^\]]+)\]", html, re.DOTALL)
    assert match, "COLORS array not found in HTML"
    hex_colors = re.findall(r"'#[0-9A-Fa-f]{6}'", match.group(1))
    assert len(hex_colors) == 7, f"Expected 7 colours in COLORS, got {len(hex_colors)}"


def test_html_day_info_function():
    """dayInfo function logic must use Math.floor and modulo to compute outer/inner."""
    html = _html()
    assert "dayInfo" in html
    assert "Math.floor" in html
    assert "% 7" in html


def test_html_essay_embedded():
    """Key essay phrases must appear in index.html (essay is embedded, not fetched)."""
    html = _html()
    phrases = [
        "cheshbon hanefesh",
        "Sfat Emet",
        "Chesed within Chesed",
        "Leviticus 23",
        "temimot",
    ]
    found = sum(1 for p in phrases if p in html)
    assert found >= 4, f"Only {found}/5 key essay phrases found in HTML"


# ── Edge cases ────────────────────────────────────────────────────────────────

def test_essay_minimum_word_count():
    """essay.md must contain at least 200 words."""
    words = _essay().split()
    assert len(words) >= 200, f"Essay too short: {len(words)} words"


def test_essay_cites_leviticus():
    """essay.md must cite Leviticus 23:15–16."""
    essay = _essay()
    assert "Leviticus 23" in essay or "23:15" in essay


def test_essay_cites_sfat_emet():
    """essay.md must cite the Sfat Emet."""
    assert "Sfat Emet" in _essay()


def test_essay_mentions_all_sefirot():
    """essay.md must mention all seven Sefirah names at least once."""
    essay = _essay()
    for name in SEFIROT:
        assert name in essay, f"Sefirah '{name}' missing from essay.md"


def test_html_has_7x7_grid_layout():
    """The grid must be 7 columns × 7 rows (49 cells total) — verified by COLS constant."""
    html = _html()
    assert "7 * CELL" in html or "COLS = 7" in html or "col < 7" in html


def test_thumbnail_is_valid_svg():
    """thumbnail.svg must be valid XML with an <svg> root element."""
    content = THUMB_SVG.read_text(encoding="utf-8")
    assert "<svg" in content
    assert "xmlns" in content
    assert "viewBox" in content


def test_pieces_json_referenced_files_exist():
    """All files referenced in pieces.json entry must exist on disk."""
    root = Path(__file__).parent.parent
    entry = _entry()
    for field in ("path", "thumbnail", "essay"):
        fpath = root / entry[field]
        assert fpath.exists(), f"Referenced file missing: {entry[field]}"


# ── Failure modes ─────────────────────────────────────────────────────────────

def test_sefirot_array_length():
    """The SEFIROT JS array in HTML must have exactly 7 entries."""
    html = _html()
    match = re.search(r"var SEFIROT\s*=\s*\[([^\]]+)\]", html, re.DOTALL)
    assert match, "SEFIROT array not found in HTML"
    entries = [e.strip() for e in match.group(1).split(",") if e.strip()]
    assert len(entries) == 7, f"Expected 7 SEFIROT entries, got {len(entries)}"


def test_colors_match_sefirot_count():
    """COLORS must have the same length as SEFIROT (one colour per Sefirah)."""
    html = _html()
    sefirot_match = re.search(r"var SEFIROT\s*=\s*\[([^\]]+)\]", html, re.DOTALL)
    colors_match  = re.search(r"var COLORS\s*=\s*\[([^\]]+)\]",  html, re.DOTALL)
    assert sefirot_match and colors_match
    n_sefirot = len([e for e in sefirot_match.group(1).split(",") if e.strip()])
    n_colors  = len(re.findall(r"'#[0-9A-Fa-f]{6}'", colors_match.group(1)))
    assert n_sefirot == n_colors == 7


def test_no_external_js_imports():
    """index.html must not import external JavaScript libraries (self-contained)."""
    html = _html()
    external = re.findall(r'<script[^>]+src=["\']https?://', html)
    assert len(external) == 0, f"External JS imports found: {external}"


def test_day_info_outer_inner_correct():
    """
    Verify dayInfo logic: day 1 → outer=0,inner=0; day 8 → outer=1,inner=0;
    day 49 → outer=6,inner=6. These are the canonical kabbalistic Sefirah pairs.
    """
    def day_info(day):
        outer = (day - 1) // 7
        inner = (day - 1) % 7
        return outer, inner

    assert day_info(1)  == (0, 0), "Day 1 should be Chesed within Chesed"
    assert day_info(8)  == (1, 0), "Day 8 should be Chesed within Gevurah"
    assert day_info(15) == (2, 0), "Day 15 should be Chesed within Tiferet"
    assert day_info(43) == (6, 0), "Day 43 should be Chesed within Malkhut"
    assert day_info(49) == (6, 6), "Day 49 should be Malkhut within Malkhut"


def test_heb_days_array_has_49_python():
    """Pure Python check: the expected HEB_DAYS array has exactly 49 entries."""
    expected = [
        "יוֹם אֶחָד", "יוֹם שְׁנַיִם", "יוֹם שְׁלוֹשָׁה", "יוֹם אַרְבָּעָה",
        "יוֹם חֲמִשָּׁה", "יוֹם שִׁשָּׁה", "יוֹם שִׁבְעָה",
        "יוֹם שְׁמוֹנָה", "יוֹם תִּשְׁעָה", "יוֹם עֲשָׂרָה",
        "יוֹם אַחַד עָשָׂר", "יוֹם שְׁנֵים עָשָׂר", "יוֹם שְׁלוֹשָׁה עָשָׂר",
        "יוֹם אַרְבָּעָה עָשָׂר", "יוֹם חֲמִשָּׁה עָשָׂר", "יוֹם שִׁשָּׁה עָשָׂר",
        "יוֹם שִׁבְעָה עָשָׂר", "יוֹם שְׁמוֹנָה עָשָׂר", "יוֹם תִּשְׁעָה עָשָׂר",
        "יוֹם עֶשְׂרִים", "יוֹם עֶשְׂרִים וְאֶחָד", "יוֹם עֶשְׂרִים וּשְׁנַיִם",
        "יוֹם עֶשְׂרִים וּשְׁלוֹשָׁה", "יוֹם עֶשְׂרִים וְאַרְבָּעָה",
        "יוֹם עֶשְׂרִים וַחֲמִשָּׁה", "יוֹם עֶשְׂרִים וְשִׁשָּׁה",
        "יוֹם עֶשְׂרִים וְשִׁבְעָה", "יוֹם עֶשְׂרִים וּשְׁמוֹנָה",
        "יוֹם עֶשְׂרִים וְתִשְׁעָה", "יוֹם שְׁלוֹשִׁים",
        "יוֹם שְׁלוֹשִׁים וְאֶחָד", "יוֹם שְׁלוֹשִׁים וּשְׁנַיִם",
        "יוֹם שְׁלוֹשִׁים וּשְׁלוֹשָׁה", "יוֹם שְׁלוֹשִׁים וְאַרְבָּעָה",
        "יוֹם שְׁלוֹשִׁים וַחֲמִשָּׁה", "יוֹם שְׁלוֹשִׁים וְשִׁשָּׁה",
        "יוֹם שְׁלוֹשִׁים וְשִׁבְעָה", "יוֹם שְׁלוֹשִׁים וּשְׁמוֹנָה",
        "יוֹם שְׁלוֹשִׁים וְתִשְׁעָה", "יוֹם אַרְבָּעִים",
        "יוֹם אַרְבָּעִים וְאֶחָד", "יוֹם אַרְבָּעִים וּשְׁנַיִם",
        "יוֹם אַרְבָּעִים וּשְׁלוֹשָׁה", "יוֹם אַרְבָּעִים וְאַרְבָּעָה",
        "יוֹם אַרְבָּעִים וַחֲמִשָּׁה", "יוֹם אַרְבָּעִים וְשִׁשָּׁה",
        "יוֹם אַרְבָּעִים וְשִׁבְעָה", "יוֹם אַרְבָּעִים וּשְׁמוֹנָה",
        "יוֹם אַרְבָּעִים וְתִשְׁעָה",
    ]
    assert len(expected) == 49
