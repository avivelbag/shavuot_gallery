# Piece 86 — A Land Flowing: The Geometry of Milk and Honey

**Theme:** Milk and honey / the promised land / seven species  
**Technique:** Gyroid implicit surface cross-section, canvas 2D ImageData pixel rendering

A 2D animated cross-section of the gyroid — a triply-periodic minimal surface whose
implicit function g = sin(x)cos(y) + sin(y)cos(z) + sin(z)cos(x) describes the exact
microstructure of honeycombs and milk fat globule membranes. The z parameter advances
0.008 rad/frame, causing the cellular landscape to slowly morph. Near-zero values of g
(|g| < 0.12) map to warm cream, tracing the thin walls of the surface; positive regions
shade through honey amber to deep gold; negative regions shade through soft ivory to
light tan.

The Hebrew overlay "דְּבַשׁ וְחָלָב" floats at 25% opacity across the canvas. A radial
vignette darkens the edges so the piece reads as an interior view rather than a cropped
frame.

## Files

- `index.html` — self-contained piece with embedded essay and animation
- `essay.md` — source essay text (~360 words)
- `thumbnail.svg` — 400×400 static gyroid cross-section at z=0, 50×50 grid of 8×8px rectangles
- `README.md` — this file

## Parameters

- Scale: 8π (~25.13 rad across canvas) — gives ~4 full gyroid cells
- Time step: 0.008 rad/frame ≈ 0.48 rad/s at 60 fps
- Color surface threshold: |g| < 0.12
- Render resolution: half the CSS canvas dimensions for performance, browser upscales
