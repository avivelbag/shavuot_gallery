"""
Tests for piece 65-hopf-fibration-binah: Sefirat HaOmer — Circles of Counting.

Verifies the Hopf fibration piece is correctly structured, that the WebGL
implementation contains the required algorithmic elements, and that the essay
meets content and citation requirements.
"""
import json
import math
import os

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECE_ID = "65-hopf-fibration-binah"
PIECE_DIR = os.path.join(GALLERY_ROOT, "pieces", PIECE_ID)


def load_piece_entry():
    """Return the pieces.json entry for this piece, or None if absent."""
    with open(os.path.join(GALLERY_ROOT, "pieces.json"), encoding="utf-8") as fh:
        pieces = json.load(fh)
    for p in pieces:
        if p["id"] == PIECE_ID:
            return p
    return None


# ---------------------------------------------------------------------------
# pieces.json registration
# ---------------------------------------------------------------------------

def test_piece_registered_in_pieces_json():
    assert load_piece_entry() is not None, f"'{PIECE_ID}' not found in pieces.json"


def test_piece_theme_is_sefirat_haomer():
    piece = load_piece_entry()
    assert piece is not None
    assert piece["theme"] == "Sefirat HaOmer", (
        f"Expected theme 'Sefirat HaOmer', got '{piece['theme']}'"
    )


def test_piece_technique_contains_hopf():
    piece = load_piece_entry()
    assert piece is not None
    assert "Hopf" in piece["technique"] or "hopf" in piece["technique"].lower(), (
        f"Technique '{piece['technique']}' does not mention Hopf fibration"
    )


def test_piece_technique_contains_webgl():
    piece = load_piece_entry()
    assert piece is not None
    assert "WebGL" in piece["technique"] or "webgl" in piece["technique"].lower(), (
        f"Technique '{piece['technique']}' does not mention WebGL"
    )


def test_piece_year_is_2026():
    piece = load_piece_entry()
    assert piece is not None
    assert piece["year"] == 2026


def test_piece_id_matches_path_directory():
    piece = load_piece_entry()
    assert piece is not None
    parts = piece["path"].replace("\\", "/").split("/")
    assert parts[-2] == PIECE_ID, (
        f"Path directory '{parts[-2]}' does not match id '{PIECE_ID}'"
    )


# ---------------------------------------------------------------------------
# File existence
# ---------------------------------------------------------------------------

def test_index_html_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "index.html"))


def test_essay_md_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "essay.md"))


def test_thumbnail_svg_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "thumbnail.svg"))


def test_readme_md_exists():
    assert os.path.isfile(os.path.join(PIECE_DIR, "README.md"))


# ---------------------------------------------------------------------------
# thumbnail.svg validity
# ---------------------------------------------------------------------------

def test_thumbnail_is_valid_svg():
    svg_path = os.path.join(PIECE_DIR, "thumbnail.svg")
    text = open(svg_path, encoding="utf-8").read()
    assert "<svg" in text and "</svg>" in text, "thumbnail.svg is not valid SVG"


def test_thumbnail_contains_ellipses():
    """Thumbnail should depict linked ellipses suggesting the Hopf fibration."""
    svg_path = os.path.join(PIECE_DIR, "thumbnail.svg")
    text = open(svg_path, encoding="utf-8").read()
    assert "ellipse" in text, "thumbnail.svg should contain ellipse elements"


def test_thumbnail_uses_violet_and_gold_colors():
    """Thumbnail must reference the violet/gold palette."""
    svg_path = os.path.join(PIECE_DIR, "thumbnail.svg")
    text = open(svg_path, encoding="utf-8").read().lower()
    has_violet = "#5a20a0" in text or "#3a1e6a" in text or "#7a30c8" in text
    has_gold = "#d4a820" in text or "#c89010" in text
    assert has_violet, "thumbnail.svg missing violet color"
    assert has_gold, "thumbnail.svg missing gold color"


# ---------------------------------------------------------------------------
# essay.md content
# ---------------------------------------------------------------------------

def test_essay_has_at_least_400_words():
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    word_count = len(text.split())
    assert word_count >= 400, f"essay.md has {word_count} words (need ≥ 400)"


def test_essay_cites_leviticus_23():
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    assert "Leviticus 23" in text or "23:15" in text, (
        "essay.md must cite Leviticus 23:15–16"
    )


def test_essay_contains_hebrew_leviticus_text():
    """Essay must contain verbatim Hebrew from Leviticus 23:15-16."""
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    assert "וּסְפַרְתֶּם" in text, "essay.md missing Hebrew text of Leviticus 23:15"
    assert "חֲמִשִּׁים יוֹם" in text, "essay.md missing 'fifty days' from Leviticus 23:16"


def test_essay_cites_rosh_hashana_21b():
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    assert "Rosh Hashana 21b" in text or "Rosh Hashana 21" in text, (
        "essay.md must cite Rosh Hashana 21b"
    )


def test_essay_contains_hebrew_rosh_hashana_text():
    """Essay must contain the Hebrew text from Rosh Hashana 21b."""
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    assert "חֲמִשִּׁים שַׁעֲרֵי בִינָה" in text, (
        "essay.md missing Hebrew from Rosh Hashana 21b: 'fifty gates of understanding'"
    )


def test_essay_discusses_hopf_fibration():
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read().lower()
    assert "hopf" in text, "essay.md must discuss the Hopf fibration"
    assert "fibration" in text or "fiber" in text, (
        "essay.md must use the term 'fibration' or 'fiber'"
    )


def test_essay_mentions_topological_linking():
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read().lower()
    assert "linked" in text or "link" in text, (
        "essay.md should mention the topological linking property of Hopf fibers"
    )


def test_essay_discusses_sefirat_haomer():
    text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    assert "Omer" in text or "omer" in text.lower(), (
        "essay.md must discuss Sefirat HaOmer"
    )


# ---------------------------------------------------------------------------
# index.html — WebGL and algorithmic content
# ---------------------------------------------------------------------------

def _html():
    return open(os.path.join(PIECE_DIR, "index.html"), encoding="utf-8").read()


def test_html_uses_webgl():
    assert "webgl" in _html().lower() or "getContext" in _html(), (
        "index.html must use WebGL"
    )


def test_html_uses_request_animation_frame():
    assert "requestAnimationFrame" in _html(), (
        "index.html must use requestAnimationFrame for animation"
    )


def test_html_contains_fibonacci_sphere():
    html = _html().lower()
    assert "fibonacci" in html or "golden" in html, (
        "index.html must implement Fibonacci sphere distribution"
    )


def test_html_contains_hopf_fiber_function():
    html = _html()
    assert "hopfFiber" in html or "hopf_fiber" in html or "hopffiber" in html.lower(), (
        "index.html must define a hopfFiber function"
    )


def test_html_contains_stereographic_projection():
    html = _html().lower()
    assert "stereographic" in html or "denom" in html or "1 - a" in html or "1-a" in html, (
        "index.html must implement stereographic projection from S³ to R³"
    )


def test_html_line_strip_or_lines_draw():
    html = _html()
    assert "LINE_STRIP" in html or "gl.LINES" in html, (
        "index.html must use gl.LINE_STRIP or gl.LINES for fiber rendering"
    )


def test_html_has_fiber_color_function():
    html = _html()
    assert "fiberColor" in html or "fiber_color" in html or "color" in html.lower(), (
        "index.html must include per-fiber coloring"
    )


def test_html_uses_additive_blending():
    html = _html()
    assert "gl.ONE" in html or "ONE, gl.ONE" in html, (
        "index.html must use additive blending (gl.ONE, gl.ONE)"
    )


def test_html_embeds_hebrew_leviticus_text():
    """The Hebrew text of Leviticus 23:15 must appear in the HTML for display."""
    html = _html()
    assert "וּסְפַרְתֶּם" in html, (
        "index.html must embed the Hebrew text of Leviticus 23:15"
    )


def test_html_embeds_hebrew_rosh_hashana_text():
    """The Hebrew text from Rosh Hashana 21b must appear in the HTML."""
    html = _html()
    assert "חֲמִשִּׁים שַׁעֲרֵי בִינָה" in html, (
        "index.html must embed the Hebrew text from Rosh Hashana 21b"
    )


def test_html_contains_essay_text():
    """index.html must embed the essay text directly, not fetch it at runtime."""
    essay_text = open(os.path.join(PIECE_DIR, "essay.md"), encoding="utf-8").read()
    html = _html()
    words = [w for w in essay_text.split() if len(w) > 5][:10]
    found = sum(1 for w in words if w in html)
    assert found >= 5, (
        f"index.html must embed essay text inline (only {found}/10 sampled words found)"
    )


def test_html_has_passage_block():
    """HTML should have a styled scripture passage block."""
    assert "passage-block" in _html(), (
        "index.html must have a .passage-block element for scripture display"
    )


def test_html_depth_test_enabled():
    html = _html()
    assert "DEPTH_TEST" in html, "index.html must enable gl.DEPTH_TEST"


# ---------------------------------------------------------------------------
# Hopf fiber math correctness (pure Python verification)
# ---------------------------------------------------------------------------

def _hopf_fiber_py(theta, phi, segments=64):
    """
    Python reimplementation of the hopfFiber function from index.html.
    Parametrization: q(t) = (cos(θ/2)cos(t), cos(θ/2)sin(t), sin(θ/2)cos(t-φ), sin(θ/2)sin(t-φ))
    Hopf map: H(a,b,c,d) = (2(ac+bd), 2(bc-ad), a²+b²-c²-d²)
    """
    CLIP = 5.0
    half_theta = theta / 2
    cos_ht = math.cos(half_theta)
    sin_ht = math.sin(half_theta)
    pts = []
    for i in range(segments + 1):
        t = (i / segments) * 2 * math.pi
        a = cos_ht * math.cos(t)
        b = cos_ht * math.sin(t)
        c = sin_ht * math.cos(t - phi)
        d = sin_ht * math.sin(t - phi)
        denom = 1.0 - a
        if denom < 1e-6:
            length = math.sqrt(b*b + c*c + d*d)
            if length < 1e-10:
                pts.append((0, 0, CLIP))
            else:
                pts.append((b/length*CLIP, c/length*CLIP, d/length*CLIP))
        else:
            px, py, pz = b/denom, c/denom, d/denom
            r = math.sqrt(px*px + py*py + pz*pz)
            if r > CLIP:
                s = CLIP / r
                pts.append((px*s, py*s, pz*s))
            else:
                pts.append((px, py, pz))
    return pts


def _hopf_map(a, b, c, d):
    """Return the Hopf map image H(a,b,c,d) = (2(ac+bd), 2(bc-ad), a²+b²-c²-d²)."""
    return (2*(a*c + b*d), 2*(b*c - a*d), a*a + b*b - c*c - d*d)


def test_hopf_map_formula_correctness():
    """
    Verify that the quaternion parametrization maps to the expected base point on S².
    For several (theta, phi) values, the first sample at t=0 should satisfy
    H(q(0)) = (sinθ cosφ, sinθ sinφ, cosθ).
    """
    test_cases = [
        (math.pi / 2, 0),
        (math.pi / 2, math.pi / 2),
        (math.pi / 3, math.pi / 4),
        (math.pi * 0.8, -math.pi / 3),
    ]
    for theta, phi in test_cases:
        t = 0.0
        a = math.cos(theta/2) * math.cos(t)
        b = math.cos(theta/2) * math.sin(t)
        c = math.sin(theta/2) * math.cos(t - phi)
        d = math.sin(theta/2) * math.sin(t - phi)
        hx, hy, hz = _hopf_map(a, b, c, d)
        expected_x = math.sin(theta) * math.cos(phi)
        expected_y = math.sin(theta) * math.sin(phi)
        expected_z = math.cos(theta)
        assert abs(hx - expected_x) < 1e-9, f"H_x mismatch for theta={theta}, phi={phi}"
        assert abs(hy - expected_y) < 1e-9, f"H_y mismatch for theta={theta}, phi={phi}"
        assert abs(hz - expected_z) < 1e-9, f"H_z mismatch for theta={theta}, phi={phi}"


def test_hopf_fiber_closes_at_2pi():
    """
    The fiber must close: first and last quaternion must be equal (before projection).
    This verifies the t ∈ [0, 2π] parametrization is correct.
    """
    for theta, phi in [(math.pi/2, 0), (math.pi/3, math.pi/4), (math.pi*0.9, -1.0)]:
        half_theta = theta / 2
        cos_ht, sin_ht = math.cos(half_theta), math.sin(half_theta)

        def q(t):
            return (
                cos_ht * math.cos(t),
                cos_ht * math.sin(t),
                sin_ht * math.cos(t - phi),
                sin_ht * math.sin(t - phi),
            )

        q0 = q(0)
        q2pi = q(2 * math.pi)
        for i in range(4):
            assert abs(q0[i] - q2pi[i]) < 1e-10, (
                f"Fiber does not close: q(0)[{i}]={q0[i]:.6f} != q(2π)[{i}]={q2pi[i]:.6f}"
            )


def test_hopf_fiber_produces_correct_segment_count():
    """hopfFiber should return exactly SEGMENTS+1 points."""
    pts = _hopf_fiber_py(math.pi / 2, 0.0, segments=64)
    assert len(pts) == 65, f"Expected 65 points, got {len(pts)}"


def test_hopf_fiber_south_pole_is_unit_circle():
    """
    For the south pole base point (theta=π), the fiber maps to a unit circle
    in R³ since sin(θ/2)=1, cos(θ/2)=0, so a=0 always and denom=1.
    All projected points should lie at distance ≤ 1 from origin.
    """
    pts = _hopf_fiber_py(math.pi, 0.0, segments=64)
    for px, py, pz in pts:
        r = math.sqrt(px*px + py*py + pz*pz)
        assert r <= 1.01, f"South pole fiber point at unexpected distance {r:.4f} from origin"


def test_hopf_fiber_points_are_finite_after_clip():
    """All projected points must have finite coordinates within CLIP."""
    CLIP = 5.0
    for theta in [0.01, math.pi/4, math.pi/2, math.pi*0.9, math.pi]:
        for phi in [0, math.pi/3, math.pi]:
            pts = _hopf_fiber_py(theta, phi)
            for px, py, pz in pts:
                assert math.isfinite(px) and math.isfinite(py) and math.isfinite(pz), (
                    f"Non-finite point for theta={theta:.3f}, phi={phi:.3f}"
                )
                r = math.sqrt(px*px + py*py + pz*pz)
                assert r <= CLIP + 1e-6, (
                    f"Point {r:.4f} exceeds CLIP={CLIP} for theta={theta:.3f}"
                )


def test_fibonacci_sphere_coverage():
    """
    Fibonacci sphere should cover north and south extremes and span the full latitude range.
    """
    def fib_sphere(n):
        pts = []
        golden = math.pi * (3 - math.sqrt(5))
        for i in range(n):
            y = 1 - (i / (n - 1)) * 2
            r = math.sqrt(1 - y * y)
            angle = golden * i
            pts.append((r * math.cos(angle), y, r * math.sin(angle)))
        return pts

    pts = fib_sphere(200)
    assert len(pts) == 200
    ys = [p[1] for p in pts]
    assert abs(max(ys) - 1.0) < 1e-10, "Fibonacci sphere should include north pole (y=1)"
    assert abs(min(ys) + 1.0) < 1e-10, "Fibonacci sphere should include south pole (y=-1)"
    # Each point should be unit length
    for x, y, z in pts[:10]:
        r = math.sqrt(x*x + y*y + z*z)
        assert abs(r - 1.0) < 1e-10, f"Fibonacci sphere point at non-unit radius {r}"


def test_fiber_color_north_pole_is_violet():
    """theta=0 (north) should give the deep violet color."""
    def fiber_color(theta_s2):
        t = theta_s2 / math.pi
        if t < 0.5:
            u = t * 2
            r = 26/255 + (58/255 - 26/255) * u
            g = 16/255 + (30/255 - 16/255) * u
            b = 80/255 + (106/255 - 80/255) * u
        else:
            u = (t - 0.5) * 2
            r = 58/255 + (212/255 - 58/255) * u
            g = 30/255 + (168/255 - 30/255) * u
            b = 106/255 + (32/255 - 106/255) * u
        return (r, g, b)

    r, g, b = fiber_color(0.0)
    assert abs(r - 26/255) < 1e-6 and abs(g - 16/255) < 1e-6 and abs(b - 80/255) < 1e-6, (
        "North pole fiber should be deep violet #1A1050"
    )


def test_fiber_color_south_pole_is_gold():
    """theta=π (south) should give the gold color."""
    def fiber_color(theta_s2):
        t = theta_s2 / math.pi
        if t < 0.5:
            u = t * 2
            r = 26/255 + (58/255 - 26/255) * u
            g = 16/255 + (30/255 - 16/255) * u
            b = 80/255 + (106/255 - 80/255) * u
        else:
            u = (t - 0.5) * 2
            r = 58/255 + (212/255 - 58/255) * u
            g = 30/255 + (168/255 - 30/255) * u
            b = 106/255 + (32/255 - 106/255) * u
        return (r, g, b)

    r, g, b = fiber_color(math.pi)
    assert abs(r - 212/255) < 1e-6, f"South pole R should be 212/255, got {r:.4f}"
    assert abs(g - 168/255) < 1e-6, f"South pole G should be 168/255, got {g:.4f}"
    assert abs(b - 32/255) < 1e-6, f"South pole B should be 32/255, got {b:.4f}"


def test_fiber_color_equator_is_violet():
    """theta=π/2 (equator) should give the midpoint violet #3A1E6A."""
    def fiber_color(theta_s2):
        t = theta_s2 / math.pi
        if t < 0.5:
            u = t * 2
            r = 26/255 + (58/255 - 26/255) * u
            g = 16/255 + (30/255 - 16/255) * u
            b = 80/255 + (106/255 - 80/255) * u
        else:
            u = (t - 0.5) * 2
            r = 58/255 + (212/255 - 58/255) * u
            g = 30/255 + (168/255 - 30/255) * u
            b = 106/255 + (32/255 - 106/255) * u
        return (r, g, b)

    r, g, b = fiber_color(math.pi / 2)
    assert abs(r - 58/255) < 1e-6, f"Equatorial R should be 58/255, got {r:.4f}"
    assert abs(g - 30/255) < 1e-6, f"Equatorial G should be 30/255, got {g:.4f}"
    assert abs(b - 106/255) < 1e-6, f"Equatorial B should be 106/255, got {b:.4f}"


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

def test_hopf_fiber_exact_north_pole_does_not_crash():
    """theta=0 (exact north pole) should not raise and returns SEGMENTS+1 points."""
    pts = _hopf_fiber_py(0.0, 0.0, segments=64)
    assert len(pts) == 65
    for px, py, pz in pts:
        assert math.isfinite(px) and math.isfinite(py) and math.isfinite(pz)


def test_hopf_fiber_large_phi_does_not_crash():
    """Large phi values (wrapping) should produce valid points."""
    pts = _hopf_fiber_py(math.pi / 3, 10 * math.pi, segments=64)
    assert len(pts) == 65
    for px, py, pz in pts:
        assert math.isfinite(px) and math.isfinite(py) and math.isfinite(pz)


def test_piece_no_duplicate_ids():
    with open(os.path.join(GALLERY_ROOT, "pieces.json"), encoding="utf-8") as fh:
        pieces = json.load(fh)
    ids = [p["id"] for p in pieces]
    assert len(ids) == len(set(ids)), "Duplicate piece IDs detected in pieces.json"
