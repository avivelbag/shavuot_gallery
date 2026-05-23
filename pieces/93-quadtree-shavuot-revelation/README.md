# From Undivided Light, the Word

**Piece 93 — Shavuot Gallery**

Adaptive quadtree decomposition of the Hebrew word שְׁבוּעוֹת (Shavuot) hidden in an offscreen canvas. The animation begins with a single white square, recursively subdivides regions of highest variance first, and reveals the word in harvest gold on parchment. After full resolution the tree collapses in reverse, returning to the undivided, and loops.

## Connection to Shavuot

Midrash Tanchuma (*Yitro* 11) teaches that before the Torah was given, the world was *tohu vavohu* — formless and undifferentiated. The divine speech at Sinai imposed structure on formlessness: 22 letters, 613 commandments, each a subdivision of the primordial unity. The quadtree enacts this literally — a single undivided region of light, subdivided frame by frame until the word שְׁבוּעוֹת is fully articulated from the brightness.

## Technical approach

- **Offscreen canvas:** 512×512 canvas pre-renders שְׁבוּעוֹת in bold 200px serif, harvest gold (#C8941A) on parchment (#F4ECD8).
- **Summed-area table (SAT):** Six Float64 tables (R, G, B, R², G², B²) enable O(1) variance computation per region.
- **Priority queue:** Binary max-heap ordered by `variance × area` — large high-variance regions subdivide first.
- **N-acceleration:** Starts at 3 splits per frame, accelerates to 20 as the split count grows.
- **Luminosity boost:** Early deep-tree nodes boosted +12% lightness, decaying linearly with depth — light condensing as structure resolves.
- **Outlines:** lineWidth=0.5, 15% darker than fill, alpha fading as nodes shrink below 8×8.
- **Hold:** 3 seconds fully resolved.
- **Collapse:** Reverse replay of split history over 4 seconds — children merge back to parents.
- **Pause:** 1 second white before loop.

## Files

| File | Purpose |
|------|---------|
| `index.html` | Animated piece with embedded essay |
| `essay.md` | Standalone essay (~380 words) |
| `thumbnail.svg` | 400×400 thumbnail showing mid-resolution quadtree state |
| `README.md` | This file |
