"""
Tests for the gallery theme-filter, keyboard navigation, and dark/light toggle
features added to index.html and styles.css.

Verifies that the filter-chip UI elements, JavaScript logic, URL-hash behaviour,
CSS custom properties, keyboard navigation handlers, and theme toggle button
required by the acceptance criteria are present in the source files.
"""
import os
import re

GALLERY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_HTML = os.path.join(GALLERY_ROOT, "index.html")
STYLES_CSS = os.path.join(GALLERY_ROOT, "styles.css")


def _read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


# ---------------------------------------------------------------------------
# Structural presence tests
# ---------------------------------------------------------------------------

def test_filter_row_element_present():
    """index.html must contain the #filter-row element above the piece grid."""
    html = _read(INDEX_HTML)
    assert 'id="filter-row"' in html, (
        'index.html is missing the <div id="filter-row"> element'
    )


def test_filter_row_before_gallery_grid():
    """#filter-row must appear before #gallery-grid in the DOM source order."""
    html = _read(INDEX_HTML)
    pos_filter = html.find('id="filter-row"')
    pos_grid = html.find('id="gallery-grid"')
    assert pos_filter != -1, 'filter-row element not found'
    assert pos_grid != -1, 'gallery-grid element not found'
    assert pos_filter < pos_grid, (
        '#filter-row must appear before #gallery-grid in index.html'
    )


# ---------------------------------------------------------------------------
# JavaScript filter-logic tests
# ---------------------------------------------------------------------------

def test_js_hash_update_pattern_present():
    """index.html must contain the location.hash update pattern for bookmarkable filters."""
    html = _read(INDEX_HTML)
    assert 'location.hash' in html, (
        'index.html is missing location.hash assignment for URL-hash filter state'
    )


def test_js_encode_uri_component_for_hash():
    """The hash must be set via encodeURIComponent so themes with spaces are URL-safe."""
    html = _read(INDEX_HTML)
    assert 'encodeURIComponent' in html, (
        'index.html must use encodeURIComponent when writing the theme to location.hash'
    )


def test_js_apply_filter_function_present():
    """index.html must define applyFilter to hide/show cards."""
    html = _read(INDEX_HTML)
    assert 'applyFilter' in html, (
        'index.html must define the applyFilter function'
    )


def test_js_filter_chip_class_used():
    """index.html must create buttons with class filter-chip."""
    html = _read(INDEX_HTML)
    assert 'filter-chip' in html, (
        'index.html must reference the filter-chip CSS class'
    )


def test_js_data_theme_attribute_set_on_cards():
    """Cards must receive a data-theme attribute so the filter can match them."""
    html = _read(INDEX_HTML)
    assert 'dataset.theme' in html or 'data-theme' in html, (
        'index.html must set data-theme on each piece card'
    )


def test_js_all_chip_clears_hash():
    """Clicking the All chip must clear the URL hash (empty string assignment)."""
    html = _read(INDEX_HTML)
    assert re.search(r"location\.hash\s*=\s*['\"](?:#?)['\"]", html) or \
           re.search(r"=== ['\"]All['\"]", html), (
        "index.html must clear location.hash when the 'All' chip is selected"
    )


def test_js_hash_read_on_load():
    """index.html must read location.hash on load to pre-apply the bookmarked filter."""
    html = _read(INDEX_HTML)
    assert re.search(r'location\.hash', html), (
        'index.html must read location.hash to restore filter state on page load'
    )


# ---------------------------------------------------------------------------
# CSS tests
# ---------------------------------------------------------------------------

def test_css_filter_chip_class_defined():
    """styles.css must define the .filter-chip rule."""
    css = _read(STYLES_CSS)
    assert '.filter-chip' in css, (
        'styles.css must define the .filter-chip rule'
    )


def test_css_active_chip_distinct_style():
    """styles.css must define .filter-chip.active with a filled background."""
    css = _read(STYLES_CSS)
    assert '.filter-chip.active' in css, (
        'styles.css must define a .filter-chip.active rule for the highlighted chip'
    )


def test_css_filter_row_wraps_on_mobile():
    """styles.css must use flex-wrap so chips wrap on narrow viewports."""
    css = _read(STYLES_CSS)
    assert 'flex-wrap' in css, (
        'styles.css must use flex-wrap on .filter-row for mobile wrapping'
    )


def test_css_chips_min_height_36px():
    """Chips must have min-height of at least 36 px for touch targets."""
    css = _read(STYLES_CSS)
    assert re.search(r'min-height\s*:\s*36px', css), (
        'styles.css must set min-height: 36px on .filter-chip for tappability'
    )


def test_css_accent_variable_defined():
    """:root must define --accent so chip colours reference a single source of truth."""
    css = _read(STYLES_CSS)
    assert '--accent' in css, (
        'styles.css must define the --accent CSS custom property'
    )


# ---------------------------------------------------------------------------
# Edge-case / failure-mode tests
# ---------------------------------------------------------------------------

def test_no_inline_styles_for_chips():
    """Chip styles must live in styles.css, not as inline style= attributes."""
    html = _read(INDEX_HTML)
    assert 'border-radius: 16px' not in html and 'border-radius:16px' not in html, (
        'Chip border-radius must be in styles.css, not inlined in index.html'
    )


def test_pieces_json_not_modified():
    """pieces.json must not be changed by this feature (acceptance criterion)."""
    import json
    pieces_path = os.path.join(GALLERY_ROOT, "pieces.json")
    with open(pieces_path, encoding="utf-8") as fh:
        pieces = json.load(fh)
    assert len(pieces) >= 1, "pieces.json must still contain at least one entry"
    for piece in pieces:
        assert "theme" in piece, f"Piece {piece.get('id')} must retain 'theme' field"


def test_filter_js_under_60_lines():
    """The filter-specific JS should be concise — signal check for < 60 filter lines."""
    html = _read(INDEX_HTML)
    filter_keywords = ['applyFilter', 'buildChips', 'selectTheme', 'setActiveChip']
    script_start = html.find('<script>')
    script_end = html.find('</script>')
    assert script_start != -1 and script_end != -1
    script = html[script_start:script_end]
    filter_lines = [ln for ln in script.splitlines()
                    if any(kw in ln for kw in filter_keywords)]
    assert len(filter_lines) <= 60, (
        f'Filter-related JS lines ({len(filter_lines)}) exceed 60-line budget'
    )


# ---------------------------------------------------------------------------
# Dark/light theme toggle tests
# ---------------------------------------------------------------------------

def test_theme_toggle_button_present():
    """index.html must contain the theme toggle button with id=theme-toggle."""
    html = _read(INDEX_HTML)
    assert 'id="theme-toggle"' in html, (
        'index.html is missing the theme toggle button with id="theme-toggle"'
    )


def test_theme_toggle_has_aria_label():
    """The theme toggle button must carry an aria-label for screen-reader accessibility."""
    html = _read(INDEX_HTML)
    toggle_pos = html.find('id="theme-toggle"')
    assert toggle_pos != -1, 'theme-toggle button not found'
    surrounding = html[max(0, toggle_pos - 200):toggle_pos + 200]
    assert 'aria-label' in surrounding, (
        'The theme toggle button must have an aria-label attribute'
    )


def test_css_custom_property_bg_defined():
    """styles.css must define the --bg custom property for theme-aware background."""
    css = _read(STYLES_CSS)
    assert re.search(r'--bg\s*:', css), (
        'styles.css must define the --bg CSS custom property'
    )


def test_css_custom_property_fg_defined():
    """styles.css must define the --fg custom property for theme-aware text colour."""
    css = _read(STYLES_CSS)
    assert re.search(r'--fg\s*:', css), (
        'styles.css must define the --fg CSS custom property'
    )


def test_css_custom_property_card_bg_defined():
    """styles.css must define the --card-bg custom property for card backgrounds."""
    css = _read(STYLES_CSS)
    assert re.search(r'--card-bg\s*:', css), (
        'styles.css must define the --card-bg CSS custom property'
    )


def test_css_custom_property_card_border_defined():
    """styles.css must define the --card-border custom property for card outlines."""
    css = _read(STYLES_CSS)
    assert re.search(r'--card-border\s*:', css), (
        'styles.css must define the --card-border CSS custom property'
    )


def test_css_light_theme_block_present():
    """styles.css must contain a [data-theme="light"] override block."""
    css = _read(STYLES_CSS)
    assert '[data-theme="light"]' in css, (
        'styles.css must define a [data-theme="light"] block to override dark defaults'
    )


def test_css_body_uses_bg_variable():
    """body background must use var(--bg) so toggling the theme changes the page background."""
    css = _read(STYLES_CSS)
    assert 'var(--bg)' in css, (
        'styles.css must use var(--bg) somewhere (e.g. body background)'
    )


def test_css_body_uses_fg_variable():
    """body color must use var(--fg) so toggling the theme changes text colour."""
    css = _read(STYLES_CSS)
    assert 'var(--fg)' in css, (
        'styles.css must use var(--fg) somewhere (e.g. body color)'
    )


def test_js_theme_persisted_in_localstorage():
    """index.html must write and read the theme choice from localStorage."""
    html = _read(INDEX_HTML)
    assert 'localStorage.setItem' in html, (
        'index.html must persist the theme choice via localStorage.setItem'
    )
    assert 'localStorage.getItem' in html, (
        'index.html must restore the theme via localStorage.getItem on load'
    )


def test_css_theme_toggle_min_44px():
    """The #theme-toggle button must have min-height of at least 44px for mobile touch targets."""
    css = _read(STYLES_CSS)
    assert re.search(r'min-height\s*:\s*44px', css), (
        'styles.css must set min-height: 44px on #theme-toggle for mobile usability'
    )


# ---------------------------------------------------------------------------
# Keyboard navigation tests
# ---------------------------------------------------------------------------

def test_js_arrow_right_key_handled():
    """index.html must handle the ArrowRight keydown event for forward navigation."""
    html = _read(INDEX_HTML)
    assert 'ArrowRight' in html, (
        'index.html must contain ArrowRight key handling for keyboard navigation'
    )


def test_js_arrow_left_key_handled():
    """index.html must handle the ArrowLeft keydown event for backward navigation."""
    html = _read(INDEX_HTML)
    assert 'ArrowLeft' in html, (
        'index.html must contain ArrowLeft key handling for keyboard navigation'
    )


def test_js_escape_key_closes_modal():
    """index.html must handle the Escape keydown event to close the piece modal."""
    html = _read(INDEX_HTML)
    assert 'Escape' in html, (
        'index.html must handle the Escape key to close the modal'
    )


def test_js_tabindex_on_cards():
    """Piece cards must receive tabIndex so Tab/Shift-Tab cycles keyboard focus."""
    html = _read(INDEX_HTML)
    assert 'tabIndex' in html or 'tabindex' in html, (
        'index.html must set tabIndex on piece cards to enable Tab navigation'
    )


def test_js_arrow_nav_inside_script():
    """ArrowRight and ArrowLeft handling must be inside the <script> block, not inline."""
    html = _read(INDEX_HTML)
    script_start = html.find('<script>')
    script_end = html.rfind('</script>')
    assert script_start != -1 and script_end != -1, '<script> block not found'
    script = html[script_start:script_end]
    assert 'ArrowRight' in script, 'ArrowRight must be handled inside <script>'
    assert 'ArrowLeft' in script, 'ArrowLeft must be handled inside <script>'


def test_css_focus_ring_defined():
    """styles.css must define a visible :focus or :focus-visible rule for keyboard users."""
    css = _read(STYLES_CSS)
    assert ':focus' in css, (
        'styles.css must define a :focus or :focus-visible rule for keyboard focus ring'
    )


# ---------------------------------------------------------------------------
# Edge-case / failure-mode tests (keyboard + theme)
# ---------------------------------------------------------------------------

def test_no_outline_none_globally():
    """styles.css must not suppress focus outlines with a universal outline:none rule."""
    css = _read(STYLES_CSS)
    assert not re.search(r'\*\s*\{[^}]*outline\s*:\s*none', css), (
        'styles.css must not globally suppress outlines — keyboard users need focus rings'
    )


def test_light_theme_overrides_bg_and_fg():
    """The [data-theme="light"] block must override both --bg and --fg."""
    css = _read(STYLES_CSS)
    light_match = re.search(
        r'\[data-theme=["\']light["\']\]\s*\{([^}]+)\}', css, re.DOTALL
    )
    assert light_match is not None, '[data-theme="light"] block not found'
    block = light_match.group(1)
    assert '--bg' in block, '--bg must be overridden in the light theme block'
    assert '--fg' in block, '--fg must be overridden in the light theme block'


def test_theme_toggle_not_inline_styled():
    """The toggle button must not carry inline style= attributes — styles belong in CSS."""
    html = _read(INDEX_HTML)
    toggle_pos = html.find('id="theme-toggle"')
    assert toggle_pos != -1, 'theme-toggle not found'
    tag_end = html.find('>', toggle_pos)
    tag_html = html[toggle_pos:tag_end]
    assert 'style=' not in tag_html, (
        'The theme-toggle button must not use inline style= attributes'
    )
