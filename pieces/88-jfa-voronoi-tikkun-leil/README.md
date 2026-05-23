# All Night They Learned: The Beit Midrash at Dawn

**Piece 88** — Shavuot Gallery 2026

## Theme

Tikkun Leil Shavuot / all-night Torah study — the custom of staying awake through Shavuot night studying Torah, first prescribed in the Zohar (Parashat Emor, III:98a) and crystallized by the Tzfat kabbalists (R. Joseph Karo, R. Shlomo Alkabetz) in the sixteenth century. The Magen Avraham (Orach Chaim 494:1) records it as universal custom. The underlying tikkun (repair) corrects Israel's drowsiness before Matan Torah, described in Shir HaShirim Rabbah 1:12.

## Technique

**Jump Flooding Algorithm (JFA) Voronoi** computed on a pixel ImageData buffer.

49 seed points (one per night-hour × Omer day) are placed in a circular arrangement with jitter. The JFA runs in O(log N) passes: in each pass, every pixel samples its 8 neighbors at the current step distance and adopts the nearest seed. After ⌊log₂(max(W,H))⌋ passes the full Voronoi diagram is computed.

The canvas begins in darkness; over 8 seconds the 49 cells activate in 7 batches (left-to-right, night-to-dawn). Each activating cell blooms outward via a distance-threshold reveal over 500 ms. Cell colors follow a gradient: midnight blue (#0A0F2E) → violet (#2D1B69) → deep orange (#B85C00) → warm gold (#F0A800) by x-position. A subtle ±3-per-channel LCG noise texture evokes candlelight parchment. Voronoi edges are overlaid with 15%-white blending. At full illumination, dawn-side cells breathe warmer (+10 red channel) at 0.2 Hz. Hebrew letter glyphs mark each seed.

## Files

- `index.html` — full-viewport canvas animation with essay embedded inline
- `essay.md` — essay source (~360 words; Zohar Emor III:98a, Magen Avraham 494:1, Shir HaShirim Rabbah 1:12)
- `thumbnail.svg` — 400×400 dark-to-dawn gradient background with stylised Voronoi cell outlines
- `README.md` — this file

## Sources

- Zohar, Parashat Emor, III:98a — the pious ones of old did not sleep Shavuot night
- Magen Avraham, Orach Chaim 494:1 — universal custom to stay awake studying Torah
- Shir HaShirim Rabbah 1:12 — Israel slept before Matan Torah; tikkun repairs this
- Roodaki, A., Bhatt, D., & Bhatt, R. (2012). Jump flooding in GPU with applications to Voronoi diagram and distance transform. *SIGGRAPH Asia Posters*
