# The Harvest Spiral — Sefirat HaOmer

A canvas 2D phyllotaxis animation: 49 seeds placed on a golden-angle spiral
(each at 137.508° from the previous, radius ∝ √i), labelled in Hebrew numerals,
slowly rotating at 0.5°/second.  A pulsing central disc (the 50th, נ) sits at
the still point of the spiral.  Faint wheat-stalk silhouettes frame the outer
ring.  Theme: the golden-angle packing common to wheat and barley — the Omer
crops of Leviticus 23:15–16 — and the mathematical structure embedded in creation.

## Technique

**Phyllotaxis placement:** for each seed index `i` (1–49):
```
angle = i × 2.39996  (golden angle in radians = 137.508° × π/180)
r     = scale × √i
x, y  = centre ± r × cos/sin(angle + globalRotation)
```

Seed 50 sits at the canvas centre `(cx, cy)`.

**Scale:** chosen so seed i=49 lands at 60% of the shorter canvas half-dimension
(`scale = min(W,H) × 0.60 / 2 / √49`), so all 49 seeds fill ~80% of the canvas.

**Disc size:** uniform radius `scale × 0.45` — this approximates the Voronoi
packing radius for equidistant seeds in a phyllotaxis lattice.

**Rotation:** a global `theta` offset increments by `0.5° / 60fps` per frame
and is added to each seed's angle before computing its screen position.

**Shimmer:** each outer disc renders with opacity `0.85 + 0.10 × sin(now/2000 + i×0.4)`.

**Pulse:** the central disc interpolates between `#FFFBE6` and `#FFD700` via
`pulse = 0.5 + 0.5 × sin(now/1500)`.

**Wheat ring:** 14 simple stalk silhouettes drawn in `rgba(200,169,80,0.13)` at
radius `min(W,H) × 0.47`.

No external dependencies; animation runs via `requestAnimationFrame`.

**Theme:** Sefirat HaOmer — Leviticus 23:15–16  
**Technique:** phyllotaxis golden-angle spiral — not used elsewhere in the gallery
