# Piece 52 — Milk and Honey: Halftone Drip

**Theme:** Bikkurim / Land Flowing with Milk and Honey  
**Technique:** canvas 2D — variable-radius halftone dot-screen, procedural drip density field

The phrase *eretz zavat chalav u'dvash* — a land flowing with milk and honey — is invoked throughout the Torah and reaches its ritual fulfillment on Shavuot, the day the Bikkurim (first fruits) were brought to the Temple (Deuteronomy 26:1–11).

This piece renders the two substances as two procedural halftone layers on a cream canvas. A warm amber honey drip descends from above, its sinusoidal front computed from a density function — not sampled from any image. Below, a pale blue-white milk layer rises from the lower half of the canvas. Where the two halftone grids meet, amber and milk-white dots intermingle on cream, embodying the pairing at the heart of the Land's identity.

## Animation

The drip front advances at ~30 px/s. A sine wave applied to the drip position creates three or four descending tongues of honey. Once the front clears the bottom of the canvas, the layers fade to the cream background over ~2.5 seconds, then the cycle restarts.

## Technical

- Dot grid pitch: 11 px
- Honey color: #C97B00 → #E8A020 (deep to bright amber, keyed to density)
- Milk color: #D0D8F0 (pale blue-white)
- Background: #FFF8E7 (cream)
- No CSS filters, no SVG effects, no external assets

## Files

- `index.html` — self-contained animated piece with embedded essay
- `essay.md` — accompanying essay (~600 words)
- `thumbnail.svg` — static SVG halftone preview at mid-drip state
- `README.md` — this file

## Sources

- Deuteronomy 26:1–11 (Bikkurim declaration)
- Exodus 3:8 (promise of a land flowing with milk and honey)
- Deuteronomy 32:13 (honey from the rock)
- Song of Songs 4:11
