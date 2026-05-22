# Wherever You Go — Ruth and Naomi Truchet Tiles

**Theme:** The Book of Ruth / Loyalty, Conversion, and the Barley Harvest (Ruth 1:16)

**Technique:** Canvas 2D — truchet tiling, figure silhouette inlay, HSL palette interpolation, gentle tile-flip animation

## Description

A 30×30 truchet tile composition in which each cell carries one of two classic quarter-circle arc variants (Smith/Truchet pair), randomly assigned, producing an organic flowing pattern of continuous curves across the canvas.

The composition is divided into two halves by palette: the left uses muted earth tones (ochre, sienna, dust — Moab, the foreign land) and the right warmer, greener tones (barley gold, leaf green — the fields of Bethlehem). The boundary is a soft gradient, not a hard line.

Two walking silhouette figures — one taller (Naomi), one shorter (Ruth) — are rendered by coloring a subset of tiles in a contrasting dark tone (#3d2b1f). The arc curves draw through the figure cells, integrating the silhouettes with the tile pattern rather than placing them above it. The figures walk toward the right (toward Bethlehem).

Hebrew text אֲשֶׁר תֵּלְכִי אֵלֵך (Ruth 1:16, "Wherever you go, I will go") appears beneath the composition in the same dark tone.

A gentle animation flips one randomly chosen non-figure tile every 4 seconds, with a 0.3 s crossfade, giving the pattern a slow breathing quality.

## Palette

- Moab side: #c2956a (ochre), #8b5e3c (sienna), #d4b483 (dust)
- Bethlehem side: #c8a84b (barley gold), #7a9e5f (leaf green), #e8d5a0 (pale straw)
- Figures and text: #3d2b1f

## Sources

- Ruth 1:16 (the declaration)
- Ruth 1:22 (arrival at the start of the barley harvest)
- Exodus 24:7 (*Na'aseh v'nishma* at Sinai)
- Talmud Bavli, Yevamot 47b (Ruth as paradigm of sincere conversion)
- Midrash Ruth Rabbah 2:14 (Ruth's declaration as completing Israel's Sinai acceptance)

## Files

- `index.html` — self-contained canvas animation (no external dependencies)
- `thumbnail.svg` — static preview: truchet grid with palette split, figure silhouettes, Hebrew text
- `essay.md` — accompanying essay on the Book of Ruth as the Shavuot reading
