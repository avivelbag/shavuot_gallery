# The Chariot of Fire — Merkavah Kaleidoscope

A four-fold kaleidoscope driven by inline Perlin noise, evoking Ezekiel's
vision of the divine chariot (*Ma'ase Merkavah*) as the Shavuot haftarah.

## Technique

Two canvases: a 400×400 `seedCanvas` (one quadrant) and an 904×904 display
canvas. Each frame:

1. The seed quadrant is filled pixel-by-pixel with fractional Brownian motion
   (4-octave Perlin noise) sampling a three-colour palette — sapphire (#1A3A6B),
   gold (#C8A000), and deep crimson (#8B1A1A). The noise z-axis advances at
   0.005 × 0.2 per frame so the field evolves continuously without ever
   repeating exactly.
2. Five thin white line segments rotate slowly around the seed centre,
   evoking fire and the ophanim wheels.
3. The seed is stamped into all four quadrants of the display canvas via
   `scale(-1,1)` / `scale(1,-1)` / `scale(-1,-1)` mirror transforms,
   producing perfect four-fold reflective symmetry.
4. Four Hebrew words — **אַרְיֵה** (lion), **נֶשֶׁר** (eagle), **שׁוֹר** (ox),
   **אָדָם** (man), the four faces of the Merkavah creatures from Ezekiel 1:10 —
   orbit the outer ring at the four cardinal points, rotating very slowly.

Animation runs at 60fps via `requestAnimationFrame`; no external dependencies.

**Theme:** Tikkun Leil Shavuot / Ma'ase Merkavah — Ezekiel 1  
**Technique:** canvas 2D — four-fold kaleidoscopic symmetry, inline Perlin noise fBm, ImageData pixel painting
