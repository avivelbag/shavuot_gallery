# Full as a Pomegranate

**Piece 83** — Shavuot Gallery 2026

## Theme

Bikkurim / seven species / the Talmudic saying "even the empty ones among you are full of
mitzvot like a pomegranate" (Eruvin 19a; Sanhedrin 37a). The pomegranate as one of the seven
species of Deuteronomy 8:8, and as the rabbinic symbol of the soul's hidden fullness: each
of its ~613 seeds (by tradition) corresponds to one of the 613 commandments of the Torah.

## Technique

**Worley noise (F1 cellular distance field)** — for each pixel within the pomegranate circle,
find the nearest of 220 randomly placed seed points; color each pixel by the wall distance
(second-nearest minus nearest distance) to produce crisp Voronoi cell boundaries. The cell
interiors are colored warm crimson (#7A1520) with subtle per-cell variation; the cell walls
are garnet (#C0103A) shading to near-white (#FCEBD5) at the sharpest boundary pixels.

Computed via a **22×22 spatial grid** for O(1) approximate nearest-neighbour lookup: each
pixel searches only the 3×3 neighbourhood of grid bins around it, reducing comparisons from
O(N_POINTS) to O(1) per pixel. The Worley texture is precomputed once at load time into an
ImageData and baked to an offscreen canvas; subsequent frames use `ctx.drawImage` (with canvas
clip) and per-cell radial-gradient overlays for the pulse animation.

## Animation

1. **Reveal (0–2 s):** A radial wedge clip sweeps clockwise from 12 o'clock, revealing the
   pomegranate cross-section as if sliced open. Each seed centre dot (#FFD700) and Hebrew
   letter label appear as the sweep passes their angular position.

2. **Pulse (ongoing):** Each of the 220 Voronoi cells breathes slightly lighter/darker at a
   unique random phase offset via a radial gradient in `screen` compositing mode, creating
   a living, cellular heartbeat.

## Files

- `index.html` — full-viewport canvas; essay embedded inline
- `essay.md` — the essay source (~340 words; Deuteronomy 8:8, Eruvin 19a, Exodus 19:6)
- `thumbnail.svg` — 400×400 SVG pomegranate cross-section with 5-point crown
- `README.md` — this file

## Sources

- Deuteronomy 8:8 — the seven species of the Land
- Eruvin 19a; Sanhedrin 37a — "even the empty ones among you are full of mitzvot like a pomegranate"
- Baal HaTurim on Deuteronomy 8:8 — 613 seeds as mnemonic for 613 commandments
- Exodus 19:6 — "a kingdom of priests and a holy nation"
