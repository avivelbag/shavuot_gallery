# 08 — We Will Do and We Will Hear

**Naaseh V'Nishma / Matan Torah** · Voronoi diagram with Hebrew typography

The two words of Israel's unconditional acceptance of the Torah — נַעֲשֶׂה וְנִשְׁמַע (Exodus 24:7) — rendered as a Voronoi cell diagram on an HTML5 canvas.

Random seed points are sampled densely inside the Hebrew letterforms and sparsely outside. Seeds inside the letters are colored with warm gold and parchment tones; seeds outside recede into deep indigo and violet. Cell borders are drawn as thin white lines where adjacent cells belong to different seeds. A slow brightness wave pulses outward from the center, as if the words are still resonating.

The letter-interior test uses `getImageData` on an offscreen canvas to read back which pixels have nonzero alpha after `fillText`; this is the mechanism that creates the letter-shaped gold region. The Talmud (Shabbat 88a) records that saying naaseh v'nishma earned Israel crowns on the letters — this piece shows those letters broken into many facets, each still warm.

## Technique

- Canvas 2D with brute-force nearest-seed Voronoi at 400×250 internal resolution
- Alpha-mask letter detection via offscreen canvas + `getImageData`
- Per-frame pixel manipulation via `ImageData.data` and `putImageData`
- RTL Hebrew text rendering with nikud (Unicode combining marks)
- 200 seeds inside letterforms (gold/parchment palette), 100 outside (indigo/violet palette)
- Brightness animation wave driven by `requestAnimationFrame`

## Files

- `index.html` — self-contained piece (no external dependencies)
- `thumbnail.svg` — 400×400 static preview
- `essay.md` — contextual essay (~430 words)
- `README.md` — this file
