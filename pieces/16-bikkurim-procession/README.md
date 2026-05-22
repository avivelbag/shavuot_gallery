# "I Declare" — Bikkurim Procession Quadtree Mosaic

**Theme:** Bikkurim / First Fruits — the procession to the Temple on Shavuot

**Technique:** Canvas 2D recursive subdivision, quadtree mosaic

## Description

A quadtree mosaic animated at 60 fps. Starting from a single warm-cream rectangle, each frame splits the largest cell along its long axis at a near-center Gaussian point. Each child cell is filled in a color from the seven-species palette — harvest gold (#d4a017), barley tan (#c8a96e), grape purple (#5b2d8e), pomegranate red (#c0392b), fig brown (#7d4a2f), olive green (#4a7c3f), and date amber (#d4850a) — with gold and olive weighted 3× for a warm, harvest-rich composition.

Children inherit their parent's color with ±10° hue jitter; every 20th split jumps to a fresh palette entry, keeping adjacent regions related while the overall composition varies.

After 300 splits the mosaic settles. The Hebrew text אֲנִי מוֹדֶה (Ani Modeh — "I declare," the opening of Deuteronomy 26:3) fades in over 1 second centered on the finished mosaic. The piece holds for 4 seconds, clears, and restarts.

## Sources

- Deuteronomy 26:1–11 (the farmer's first-fruits declaration)
- Numbers 28:26 (Shavuot as Yom HaBikkurim)
- Mishnah Bikkurim 3:1–9 (the procession to Jerusalem)
- Mishnah Bikkurim 1:3 (Shavuot as the opening of the bikkurim season)

## Files

- `index.html` — self-contained animated mosaic (no external dependencies)
- `thumbnail.svg` — static SVG preview in the seven-species palette
- `essay.md` — accompanying essay on the Bikkurim procession and Deuteronomy 26
