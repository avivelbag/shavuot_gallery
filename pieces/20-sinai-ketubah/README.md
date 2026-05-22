# Piece 20 — The Mountain as Canopy: Sinai as Ketubah

**Theme:** Matan Torah / Sinai as Covenant  
**Technique:** SVG generative ornamental border, Hebrew calligraphic typography

## What it is

A ketubah (Jewish marriage contract) rendered as programmatic SVG. The piece treats the
Talmudic reading of the Sinai revelation (Shabbat 88a) in which the mountain is held over
Israel like a barrel as the visual and conceptual basis for a ketubah illumination. The
ornate vine-scroll and pomegranate border is generated at load time by an inline JavaScript
block that places `<use>` elements around the perimeter — over 13 units per horizontal side
and 21 per vertical side.

## Files

| File | Purpose |
|------|---------|
| `index.html` | HTML page with inline SVG artwork and full essay beside it |
| `piece.svg` | Standalone SVG (identical artwork, opens directly in a browser) |
| `thumbnail.svg` | 400×400 static crop of the centre of the piece |
| `essay.md` | Full essay (~600 words) on Shabbat 88a, Exodus 19:17, Esther 9:27 |
| `README.md` | This file |

## Palette

| Role | Hex |
|------|-----|
| Background (parchment) | `#f5ead8` |
| Text and border outlines (indigo) | `#2c2060` |
| Ornamental fill (gold) | `#b8860b` |

## Sources cited

- Shabbat 88a — mountain held over Israel like a barrel (*gigit*)
- Exodus 19:17 — *vayityatzvu b'tachtit ha-har*
- Exodus 24:7 — *na'aseh v'nishma*
- Esther 9:27 — *kiym'u v'kibl'u*

## Technique

The border generation script runs at page load inside `<script type="text/javascript">` …
`</script>` (CDATA-wrapped for SVG compatibility). It calls `document.createElementNS` to
append `<use>` elements referencing `<symbol>` definitions in `<defs>`. No canvas, no WebGL,
no external fonts, no external network calls.
