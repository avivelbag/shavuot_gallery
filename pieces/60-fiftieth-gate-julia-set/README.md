# 60 — The Fiftieth Gate: Julia Set of Infinite Understanding

**Theme:** Shavuot / Chamishim Sha'arei Binah (Fifty Gates of Understanding)

**Technique:** Julia set / WebGL escape-time fractal with smooth coloring

The complex parameter *c* orbits an ellipse of radius 0.7885, drifting close to the Mandelbrot set boundary and pulling back on a ~30-second cycle. Each frame the WebGL fragment shader computes the escape-time Julia iteration *z → z² + c* per pixel, mapping the smooth (fractional) iteration count to a harvest palette: deep midnight interior, exterior bands cycling through wheat gold, harvest orange, deep violet, and pale parchment. A Hebrew gate counter (שַׁעַר א׳ … שַׁעַר נ׳) marks the orbit's position, reaching Gate 50 at closest approach to the boundary — enacting the kabbalistic teaching from Rosh Hashana 21b that Moses received 49 of 50 gates of understanding.

**Source:** Babylonian Talmud, Rosh Hashana 21b · Leviticus 23:15–16

**Files:**
- `index.html` — WebGL Julia set renderer with embedded essay, gate overlay, and quoted passages
- `essay.md` — Essay on the fifty gates of understanding, Shavuot as the fiftieth day, and the Mandelbrot boundary as mathematical analogue of the unreachable fiftieth gate
- `thumbnail.svg` — Schematic Julia set silhouette in harvest gold on midnight background
