# Piece 07 — A Land Flowing

**Theme:** Milk and Honey / Bikkurim  
**Technique:** reaction-diffusion (Gray-Scott), canvas 2D

A Gray-Scott reaction-diffusion simulation that renders the "land flowing with milk and honey" (Exodus 3:8, Deuteronomy 26:9) as organic, viscous pattern-forming flows. The U field maps to cream white and the V field maps through honey gold to dark amber, producing forms that pool and spread in slowly evolving loops.

The Hebrew phrase אֶרֶץ זָבַת חָלָב וּדְבַשׁ is composited semi-transparently over the canvas.

## Files

- `index.html` — self-contained piece with embedded essay
- `essay.md` — source essay text (~400 words)
- `thumbnail.png` — 256×256 steady-state snapshot
- `gen_thumbnail.py` — Python script to regenerate the thumbnail (requires NumPy and Pillow)
- `README.md` — this file

## Parameters

Gray-Scott: F=0.055, k=0.062, Du=0.16, Dv=0.08. These produce worm/coral-like patterns. Simulation grid: 256×256, double-buffered Float32Arrays. Color ramp: cream (#fdf6e3) → honey (#d4a017) → amber (#8b5a00).
