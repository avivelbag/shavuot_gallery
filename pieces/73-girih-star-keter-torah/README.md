# The Crown Woven in Geometry — Girih Star / Keter Torah

**Theme:** Keter Torah — the Crown of Torah (Pirkei Avot 4:13); the tagin (decorative crowns on Torah letters)

**Technique:** Girih decagonal star polygon tiling — algorithmic canvas 2D, slow-rotation animation

## Description

An infinite field of interlocking 10-pointed decagonal star tiles covers the canvas using the classic girih construction. Each tile is drawn by computing the 10 vertices of a regular decagon, filling alternate wedge regions in royal blue (#1A2870) and warm gold (#C8900A), and stroking the structural interior chords that form the star-and-bow-tie motif. The full pattern rotates slowly at 1 degree per 3 seconds; because the decagonal tiling has 10-fold symmetry, the animation loops seamlessly every 36 degrees.

At the canvas center, one star is highlighted with a brighter gold (#FFD040) and bears the Hebrew letter **כ** (Kaf) — the first letter of *Keter*, crown — in cream, marking the focal point of the infinite pattern.

The piece connects to *Keter Torah* via two ideas: the *tagin* (small crown-shaped marks atop certain Torah letters, described in Talmud *Menachot* 29b as hiding infinite meaning), and the mathematical discovery that girih tilings are quasiperiodic — aperiodic infinite patterns encoded by a finite tile set, discovered empirically by medieval craftsmen centuries before it was formalized mathematically.

## Sources

- Pirkei Avot 4:13 (the three crowns)
- Babylonian Talmud, Menachot 29b (Moses, Rabbi Akiva, and the tagin)
- Peter J. Lu and Paul J. Steinhardt, "Decagonal and Quasi-Crystalline Tilings in Medieval Islamic Architecture," *Science* 315 (2007)

## Files

- `index.html` — self-contained animated canvas piece (no external dependencies)
- `thumbnail.svg` — static SVG preview: center star with כ surrounded by 4 tiles
- `essay.md` — accompanying essay on Keter Torah, tagin, and geometric infinity
