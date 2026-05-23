# One Rule, All Interpretation — Rule 110 / Oral Torah

**Shavuot theme:** Matan Torah / Written and Oral Torah

The Written Torah is finite and fixed; the Oral Torah — Talmud, Midrash, centuries of responsa — is its emergent, inexhaustible output. Rule 110, Wolfram's elementary cellular automaton proven to be Turing-complete, makes that claim visual: one rule applied row by row from a single seed produces a pattern of provably unbounded complexity.

## Technique

**Algorithm:** Elementary cellular automaton Rule 110 (binary 01101110). Each cell's next state is determined by the pattern formed by its left neighbor, itself, and its right neighbor. The rule is a lookup table of 8 entries — the entire rule fits in one byte.

**Rule table:**
| neighborhood (L,C,R) | binary | output |
|----------------------|--------|--------|
| 111 | 7 | 0 |
| 110 | 6 | 1 |
| 101 | 5 | 1 |
| 100 | 4 | 0 |
| 011 | 3 | 1 |
| 010 | 2 | 1 |
| 001 | 1 | 1 |
| 000 | 0 | 0 |

**Grid:** `W = Math.floor(canvas.width / 4)` columns × `H = Math.floor(canvas.height / 4)` rows. At 1920×1080, W ≈ 480, H ≈ 270.

**Ring buffer:** H Uint8Arrays store the last H generations. A `head` pointer wraps around modulo H. Each tick, the next generation is written into `rows[head]` (computed from `rows[(head-1+H)%H]`), then `head` advances. Rendering maps `rows[(head + i) % H]` to screen row `i * cellSize` for i in [0, H), so the oldest row appears at the top and the newest at the bottom.

**Seed:** Single ON cell at column W/2, generation 0. Produces the canonical Rule 110 pattern with its characteristic triangular structures and irregular lacunae.

**Animation:** `setInterval` at 67ms ≈ 15 generations per second.

## Palette

| Role | Hex | RGB |
|------|-----|-----|
| ON cell (deep indigo / tekhelet) | `#1C1864` | 28, 24, 100 |
| OFF cell (warm parchment) | `#F5EDD6` | 245, 237, 214 |
| Overlay text (gold) | `#C8941A` | 200, 148, 26 |

## Overlay

Bottom-right corner: "דּוֹר לְדוֹר" (*dor l'dor*, "generation to generation") in gold #C8941A, font-size 1rem, opacity 0.7. The phrase is the traditional description of how the Oral Torah passes between generations.
