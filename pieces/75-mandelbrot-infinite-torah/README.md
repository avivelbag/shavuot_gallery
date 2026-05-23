# Piece 75 — Turn It and Turn It Again

**Theme:** The Crown of Torah / Naaseh v'Nishma  
**Technique:** Mandelbrot set / WebGL smooth escape-time coloring

A WebGL fragment shader renders the Mandelbrot set with continuous smooth escape-time coloring and auto-zooms into the point (−0.7269, 0.1889) on the Mandelbrot boundary — a location rich with spiral filaments. The zoom is infinite: scale decreases by factor 1.0003 per frame, resetting at 1e-12 to create a seamless cycle. The interior is rendered near-black (#050508); the exterior palette cycles through deep indigo → royal blue → sapphire → gold → amber → cream using piecewise linear interpolation on the smooth escape value. A Hebrew text overlay (Pirkei Avot 5:22) fades in after two seconds.

The piece enacts Ben Bag Bag's dictum "Turn it and turn it again, for everything is in it" — the Rabbinic teaching that Torah has infinite depth. The mathematical connection: Mitsuhiro Shishikura proved in 1998 that the Mandelbrot boundary has Hausdorff dimension 2, meaning it is as geometrically complex as a filled plane. Both the Torah and the Mandelbrot set are finitely encoded generators of infinite complexity.

## Files

- `index.html` — self-contained WebGL piece with embedded essay
- `essay.md` — source essay text (~500 words)
- `thumbnail.png` — 400×400 static render of the Mandelbrot set
- `gen_thumbnail.py` — pure Python script to regenerate the thumbnail (no dependencies beyond stdlib)
- `README.md` — this file

## Technical notes

- WebGL fragment shader with `precision highp float`
- Max iteration count: 256
- Smooth coloring formula: `smooth_iter = iter - log2(log2(|z|²)) + 4`
- Zoom target: `(-0.7269, 0.1889)`, starting scale `3.5`, multiplied by `0.9997` per frame
- Color palette: 6-stop Shavuot sequence (indigo #1A0A40, royal blue #1A3080, sapphire #1060C0, gold #C8A020, amber #D4720A, cream #F0E8D0)
