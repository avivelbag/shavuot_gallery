# 53 — Gleaning in the Fields of Boaz

**Theme:** Ruth / Harvest / Shavuot  
**Technique:** Canvas 2D — marching squares contour tracing on a 2D fBm noise field, figure silhouettes

## Shavuot Connection

The Book of Ruth — read aloud on Shavuot — is set in the barley and wheat harvest. Chapter 2 follows Ruth as she gleans in Boaz's field, a scene made possible by the *leket* commandment (Leviticus 19:9, Deuteronomy 24:19), laws given at Sinai. Ruth embodies the voluntary, wholehearted acceptance of Torah that Shavuot commemorates.

## Algorithm

### Marching Squares

The canvas is divided into a 150×100 grid. At each vertex a scalar noise value is sampled. For each cell, the four corner values are compared against a threshold to determine which of the 16 marching squares cases applies (bit encoding: TL=8, TR=4, BR=2, BL=1). Contour line segments are drawn between edge midpoints with linear interpolation for smooth sub-cell positioning. Saddle cases (5 and 10) are resolved by comparing the cell's average value to the threshold.

Ten equally-spaced thresholds produce nine contour iso-lines and ten filled choropleth bands.

### Noise Field

The scalar field is a 3-octave fractional Brownian motion (fBm) sum of bilinear-interpolated value noise, sampled from a single 64×64 wrapping lattice at scales 5×, 10×, and 20×, weighted 0.5 + 0.3 + 0.2. The field offset advances by (0.003, 0.0015) per frame, causing the contours to drift and ripple. Because the lattice wraps, the animation is seamlessly periodic.

### Figures

Five silhouettes (Ruth and four harvesters) move at constant fractional velocity across the canvas. Each is drawn with 1.5 px bezier strokes in near-black (#1A1208), representing a bent gleaning posture.

## Palette

| Role | Hex |
|---|---|
| Deep field green (lowest band) | `#2E4A26` |
| Field green | `#4A6741` |
| Light straw | `#C4BB83` |
| Straw | `#E8D5A3` (essay background reference) |
| Harvest gold (highest band) | `#C9922A` |
| Sky edge | `#8EA4B2` |
| Figure silhouette | `#1A1208` |

## Source References

- Ruth 2:1–23 (gleaning scene)
- Leviticus 19:9 (*leket* commandment)
- Deuteronomy 24:19 (sheaf-forgetting law)
- Ruth 1:16 (Ruth's declaration to Naomi)
