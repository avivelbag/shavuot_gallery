# Ruth's Loom — Woven Fields of Bethlehem

**Theme:** Book of Ruth / Ketzir (harvest)

A warp-and-weft textile simulation set in the harvest fields of Bethlehem. Each
warp thread is a life stretched under tension; the weft shuttle passes over two
and under one (a twill), generating a diagonal rib that is the whole story of
Ruth and Boaz made visible as cloth.

## Technique

- **Canvas 2D**, pure JavaScript, no dependencies
- **700 × 700 px** canvas; 175 columns × 175 rows of 4 px threads
- **Warp colors:** barley gold (`#D4A317`), wheat cream (`#F5E6B0`), deep olive
  (`#556B2F`) — assigned per column using `|sin(i × 2.3)|` to avoid mechanical
  repetition
- **Weft colors:** rose madder (`#B5302A`) / faded linen (`#E8D9B0`) alternating;
  every 7th row rendered in bright gold (`#F0C040`) to mark Shabbat within the Omer
- **Twill rule:** cell (col, row) shows weft if `(col + row) % 3 !== 0`; otherwise
  shows warp — produces an over-2 / under-1 pattern with a 45° diagonal rib
- **Weaving animation:** timestamp-driven; 175 rows distributed over 12 000 ms via
  `requestAnimationFrame` so the cloth grows from top to bottom at a steady pace
- **Sway phase:** after weaving completes, the cloth is copied to an offscreen
  canvas; each sway frame redraws per-column strips horizontally displaced by
  `2 × sin(2π/3 × t + col × 0.05)` px (period 3 s, amplitude 2 px)
- **Hebrew inscription:** `רות ב:ב — אֵלְכָה־נָּא הַשָּׂדֶה` in a translucent
  gold overlay at the canvas top-left, drawn once on weaving completion and
  composited on every sway frame

## Palette

| Element          | Hex       |
|------------------|-----------|
| Warp — gold      | `#D4A317` |
| Warp — cream     | `#F5E6B0` |
| Warp — olive     | `#556B2F` |
| Weft — rose      | `#B5302A` |
| Weft — linen     | `#E8D9B0` |
| Weft — Shabbat   | `#F0C040` |
| Background       | `#1a1208` |
