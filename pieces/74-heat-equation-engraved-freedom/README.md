# Piece 74 — חָרוּת / חֵרוּת — Engraved and Free

**Theme:** The Tablets / Luchot / Matan Torah
**Technique:** 2D heat equation / FTCS finite-difference diffusion

The word חֵרוּת (cherut, freedom) is seared white-hot into a dark stone surface.
The FTCS (forward-time centered-space) finite-difference scheme diffuses the heat
outward each frame, producing a warm amber halo around the letter shapes. The
letters are held at a slowly decaying source temperature — the inscription that
endures — while the surrounding stone radiates warmth without limit.

The piece is rooted in the Mishnaic wordplay (Avot 6:2): do not read *charut*
(חָרוּת, engraved) but *cherut* (חֵרוּת, freedom). The dark letter voids are the
charut; the diffusing glow is the cherut.

## Files

- `index.html` — self-contained piece with embedded essay and FTCS simulation
- `essay.md` — source essay text (~420 words)
- `thumbnail.svg` — static SVG thumbnail: amber halo, dark letter voids
- `gen_thumbnail.py` — Python script to regenerate as `thumbnail.png` (requires NumPy; Pillow optional)
- `README.md` — this file

## Simulation parameters

- Grid: 400×300, Float32Array double-buffered
- Stability constant α: 0.24 (below the 0.25 FTCS limit)
- Steps per frame: 3
- Source temperature: `max(0.05, 1.0 − t × 0.0002)` — slow decay over hours
- Re-engraving cycle: 90 seconds
- Palette: #1A1410 → #3D1A08 → #C84A08 → #E8A020 → #FFF0C0
