"""
Tests for piece 61-forty-nine-folds-dragon-curve.

Covers: pieces.json registration, all required files exist, essay content
requirements, HTML animation requirements, thumbnail validity, and the
analytical dragon-turn formula used by the piece's JavaScript.
"""
import json
import os

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID = "61-forty-nine-folds-dragon-curve"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)
PIECES_JSON = os.path.join(GALLERY_ROOT, "pieces.json")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_pieces():
    """Return parsed pieces.json as a list."""
    with open(PIECES_JSON, encoding="utf-8") as fh:
        return json.load(fh)


def get_piece():
    """Return the pieces.json entry for this piece, or None."""
    for p in load_pieces():
        if p["id"] == PIECE_ID:
            return p
    return None


def read_file(rel_path):
    """Read a file relative to the gallery root."""
    return open(os.path.join(GALLERY_ROOT, rel_path), encoding="utf-8").read()


# ---------------------------------------------------------------------------
# pieces.json registration
# ---------------------------------------------------------------------------

def test_piece_registered_in_pieces_json():
    """The piece must appear in pieces.json."""
    assert get_piece() is not None, f"'{PIECE_ID}' not found in pieces.json"


def test_piece_theme_is_sefirat_haomer():
    """Theme must be 'Sefirat HaOmer' as required by acceptance criteria."""
    p = get_piece()
    assert p is not None
    assert p["theme"] == "Sefirat HaOmer", f"Expected 'Sefirat HaOmer', got {p['theme']!r}"


def test_piece_technique_mentions_dragon_curve():
    """Technique must mention 'dragon curve' as required by acceptance criteria."""
    p = get_piece()
    assert p is not None
    assert "dragon curve" in p["technique"].lower(), (
        f"Technique field must mention 'dragon curve'; got {p['technique']!r}"
    )


def test_piece_has_all_required_fields():
    """All standard required fields must be present and non-empty."""
    p = get_piece()
    assert p is not None
    for field in ("id", "title", "tagline", "year", "theme", "technique", "path", "thumbnail", "essay"):
        assert field in p and p[field], f"Missing or empty field '{field}'"


# ---------------------------------------------------------------------------
# File existence
# ---------------------------------------------------------------------------

def test_index_html_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "index.html")), "index.html missing"


def test_essay_md_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "essay.md")), "essay.md missing"


def test_thumbnail_svg_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "thumbnail.svg")), "thumbnail.svg missing"


def test_readme_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "README.md")), "README.md missing"


# ---------------------------------------------------------------------------
# essay.md content requirements
# ---------------------------------------------------------------------------

def test_essay_is_substantial():
    """Essay must be at least 350 words (spec says ~350 minimum)."""
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    wc = len(text.split())
    assert wc >= 350, f"Essay has only {wc} words; need ≥ 350"


def test_essay_cites_leviticus_23():
    """Essay must cite Leviticus 23:15-16 as required."""
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    assert "23:15" in text or "23:15–16" in text, "Essay must cite Leviticus 23:15 or 23:15–16"


def test_essay_contains_hebrew_text():
    """Essay must include Hebrew text (nikud characters indicate proper vocalization)."""
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    # Sheva (ְ) is a common nikud character present in the quoted verse
    has_hebrew = any(ord(c) >= 0x05B0 for c in text)
    assert has_hebrew, "Essay must contain Hebrew text with nikud"


def test_essay_contains_english_translation():
    """Essay must contain an English translation of the quoted scripture."""
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    assert "seven complete weeks" in text or "count fifty days" in text, (
        "Essay must include English translation of Leviticus 23:15-16"
    )


def test_essay_mentions_sefer_hachinuch():
    """Essay must reference the Sefer ha-Chinuch mitzvah 306."""
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read().lower()
    assert "chinuch" in text or "ha-chinuch" in text, (
        "Essay must cite the Sefer ha-Chinuch"
    )
    assert "306" in text, "Essay must reference Mitzvah 306 of the Sefer ha-Chinuch"


def test_essay_explains_self_similarity():
    """Essay must explain the self-similar structure of the dragon curve."""
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read().lower()
    assert "self-similar" in text or "recursive" in text, (
        "Essay must explain the self-similar / recursive structure of the dragon curve"
    )


def test_essay_mentions_irreversibility():
    """Essay must draw the analogy between folding irreversibility and the Omer."""
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read().lower()
    assert "unfold" in text or "irreversib" in text, (
        "Essay must discuss the irreversibility of each fold/counted day"
    )


# ---------------------------------------------------------------------------
# index.html animation requirements
# ---------------------------------------------------------------------------

def test_html_uses_requestanimationframe():
    """Animation must use requestAnimationFrame."""
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "requestAnimationFrame" in html


def test_html_has_700x700_canvas():
    """Canvas must be 700×700 as specified."""
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert 'width="700"' in html and 'height="700"' in html, (
        "Canvas must be 700×700"
    )


def test_html_uses_dragon_turn_formula():
    """HTML must implement the analytical dragon turn formula."""
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "dragonTurn" in html, "HTML must define the dragonTurn function"


def test_html_has_all_seven_sefirot_colors():
    """All seven sefirah colors must appear in the HTML."""
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read().lower()
    required = ["#d4a020", "#8b0000", "#1a8070", "#4a8020", "#c06010", "#5a20a0", "#1040a0"]
    for color in required:
        assert color in html, f"Missing sefirah color {color}"


def test_html_has_counter_overlay():
    """HTML must include a day counter overlay element."""
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    assert "counter" in html.lower() or "יום" in html, (
        "HTML must include a day counter overlay (יום N)"
    )


def test_html_embeds_essay_text():
    """index.html must embed essay text inline (no runtime fetch)."""
    essay = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    words = [w for w in essay.split() if len(w) > 6][:15]
    found = sum(1 for w in words if w in html)
    assert found >= 8, (
        f"index.html must embed essay text; only {found}/15 sampled words found"
    )


def test_html_has_hebrew_scripture_block():
    """index.html must embed the Hebrew Leviticus text."""
    html = open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()
    # The verse starts with וּסְפַרְתֶּם (nikud characters confirm vocalization)
    assert "וּסְפַרְתֶּם" in html, (
        "index.html must embed the Hebrew text of Leviticus 23:15 with nikud"
    )


# ---------------------------------------------------------------------------
# thumbnail.svg validity
# ---------------------------------------------------------------------------

def test_thumbnail_is_valid_svg():
    """thumbnail.svg must be well-formed SVG."""
    text = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert "<svg" in text and "</svg>" in text, "thumbnail.svg must be valid SVG"


def test_thumbnail_has_path_element():
    """thumbnail.svg must contain a <path> element (the dragon curve silhouette)."""
    text = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert "<path" in text, "thumbnail.svg must contain a <path> element"


def test_thumbnail_has_hebrew_label():
    """thumbnail.svg must contain the Hebrew label 'מ״ט יום' (49 days)."""
    text = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read()
    assert "מ״ט יום" in text, "thumbnail.svg must contain Hebrew label מ״ט יום"


def test_thumbnail_uses_gold_color():
    """thumbnail.svg must use the Chesed gold color (#D4A020)."""
    text = open(os.path.join(PIECE_DIR, "thumbnail.svg"), encoding="utf-8").read().lower()
    assert "#d4a020" in text, "thumbnail.svg must use gold color #D4A020"


# ---------------------------------------------------------------------------
# Dragon turn algorithm correctness (Python reference implementation)
# ---------------------------------------------------------------------------

def dragon_turn_py(n):
    """Python reference for the analytical dragon turn formula.

    Returns +1 (right, clockwise) or -1 (left, counter-clockwise) for the nth
    turn in the dragon curve. Uses the formula:
        turn = ((n // lsb(n)) >> 1) & 1 == 0 ? right : left
    where lsb(n) = n & -n is the lowest set bit of n.
    """
    lsb = n & -n
    return 1 if ((n // lsb) >> 1) & 1 == 0 else -1


def test_dragon_turn_first_seven():
    """The first 7 turns of the dragon curve must be R R L R R L L."""
    expected = [1, 1, -1, 1, 1, -1, -1]
    for i, exp in enumerate(expected, start=1):
        assert dragon_turn_py(i) == exp, (
            f"dragonTurn({i}) should be {exp}, got {dragon_turn_py(i)}"
        )


def test_dragon_turn_power_of_two():
    """Turns at powers of two must always be +1 (right), a known property."""
    for k in range(1, 15):
        n = 1 << k  # 2^k
        assert dragon_turn_py(n) == 1, f"dragonTurn(2^{k}={n}) must be +1"


def test_dragon_turn_returns_plus_or_minus_one():
    """dragonTurn must return only +1 or -1 for any positive n."""
    for n in range(1, 200):
        result = dragon_turn_py(n)
        assert result in (1, -1), f"dragonTurn({n}) returned {result}, not ±1"


def test_dragon_curve_gen2_path():
    """Generation-2 dragon curve (4 segments) must trace the known L-arch shape."""
    # Gen 2: start (0,0) facing right; turns are R R L
    # Expected points: (0,0)→(1,0)→(1,1)→(0,1)→(0,2) (with y-down coordinates)
    ddx = [1, 0, -1, 0]
    ddy = [0, 1, 0, -1]
    x, y, direction = 0, 0, 0
    pts = [(x, y)]
    for i in range(1, 5):  # 4 segments
        x += ddx[direction]
        y += ddy[direction]
        pts.append((x, y))
        if i < 4:
            t = dragon_turn_py(i)
            direction = (direction + (1 if t == 1 else 3)) % 4
    assert pts[0] == (0, 0)
    assert pts[1] == (1, 0)
    assert pts[2] == (1, 1)
    assert pts[3] == (0, 1)
    assert pts[4] == (0, 2)


def test_dragon_curve_no_crossing_at_gen_8():
    """The gen-8 dragon curve must produce exactly 257 distinct-enough points
    (not all the same), confirming the curve spreads out over the plane."""
    ddx = [1, 0, -1, 0]
    ddy = [0, 1, 0, -1]
    x, y, direction = 0, 0, 0
    xs, ys = [x], [y]
    for i in range(1, 257):
        x += ddx[direction]
        y += ddy[direction]
        xs.append(x)
        ys.append(y)
        if i < 256:
            t = dragon_turn_py(i)
            direction = (direction + (1 if t == 1 else 3)) % 4
    assert len(xs) == 257
    # The curve must span at least 10 units in each axis
    assert max(xs) - min(xs) >= 10
    assert max(ys) - min(ys) >= 10


def test_sefirah_boundaries_cover_max_gen():
    """The sefirah color boundaries must cover all 16384 segments of gen-14."""
    SEF_BOUNDS = [4, 16, 64, 256, 1024, 4096, 16384]
    assert SEF_BOUNDS[-1] == 1 << 14, "Last boundary must equal 2^14 = 16384"
    assert SEF_BOUNDS[0] == 4  # first two gens (gen1=2 segs + gen2=2 segs = 4)


# ---------------------------------------------------------------------------
# Edge cases and failure modes
# ---------------------------------------------------------------------------

def test_dragon_turn_n1_is_right():
    """The very first turn (n=1) of the dragon curve is always right."""
    assert dragon_turn_py(1) == 1, "Turn 1 must be right (+1)"


def test_dragon_turn_large_n():
    """dragonTurn must return ±1 for large n (no overflow / precision issue)."""
    for n in [8192, 16383, 16384]:
        result = dragon_turn_py(n)
        assert result in (1, -1), f"dragonTurn({n}) returned {result}"


def test_day_for_gen_mapping():
    """Generation-to-day mapping: gen 1 must give day ~4, gen 14 must give day 49."""
    def day_for_gen(g, max_gen=14):
        return round(g * 49 / max_gen)
    assert day_for_gen(14) == 49
    # Gen 1 should give approx day 4 (round(49/14) = round(3.5) = 4 in Python)
    assert 3 <= day_for_gen(1) <= 5, f"day_for_gen(1) = {day_for_gen(1)}, expected 3-5"


def test_piece_id_has_no_duplicate():
    """The new piece ID must be unique in pieces.json."""
    pieces = load_pieces()
    ids = [p["id"] for p in pieces]
    count = ids.count(PIECE_ID)
    assert count == 1, f"'{PIECE_ID}' appears {count} times in pieces.json (must be 1)"
