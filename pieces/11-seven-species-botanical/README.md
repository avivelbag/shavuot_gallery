# Sheva Minim — Seven Species Botanical SVG

**Shavuot theme: Bikkurim / Seven Species**

A hand-coded SVG botanical illustration of the seven species of the Land of Israel, arranged as a wreath around the Hebrew text *שִׁבְעַת הַמִּינִים* (Shivat HaMinim). The composition follows the Bikkurim procession tradition described in Mishnah Bikkurim 3, in which the seven agricultural species central to the covenant are brought as first fruits to the Temple.

## Technique

- Pure SVG — no canvas, no JavaScript
- Each species rendered with SVG paths, ellipses, circles, and lines grouped under `<g>` elements with `transform` attributes
- Nine species groups arranged radially around a 600×600 viewBox: wheat (2), barley (2), pomegranate, olive, date, fig, grapes
- CSS `@keyframes sway` animation on leaf elements: ±3° rotation on a 4 s sinusoidal loop; `transform-box: fill-box; transform-origin: center bottom` anchors rotation at the stem base
- Five animation phase offsets (0 s, 0.7 s, 1.4 s, 2.1 s, 2.8 s) stagger the leaf movement across the wreath
- All styles inline inside the SVG `<defs><style>` block — no external stylesheets

## Palette

| Role | Hex |
|---|---|
| Background parchment | `#f5ead0` |
| Deep leaf green | `#2d5a1b` |
| Grape purple | `#6b2d8b` |
| Wheat gold | `#c8921a` |
| Barley gold | `#b8840f` |
| Pomegranate red | `#c0392b` |
| Olive muted green | `#7a8c2e` |
| Date amber | `#d4821a` |
| Central disk | `#efe0bc` |

## File layout

- `piece.svg` — main artwork, self-contained SVG with inline CSS animations
- `thumbnail.svg` — simplified preview at 256×256
- `index.html` — splits viewport between the artwork and the essay
- `essay.md` — theological essay (Deuteronomy 26, Bikkurim)
- `README.md` — this file
