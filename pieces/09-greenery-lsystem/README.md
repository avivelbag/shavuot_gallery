# The Greening of the House — L-system Floral Decoration

**Shavuot theme: Greenery and Flowers / Chag Shavuot**

Decorating homes and synagogues with greenery and flowers for Shavuot is a widely observed Ashkenazi and Sephardic custom, codified by the Rama in Shulchan Aruch (Orach Chaim 494:3). The folk explanation, preserved in the Mishnah Berurah, holds that Mount Sinai was lush and green at the moment of the revelation — God prepared a blooming mountain for the giving of Torah.

## Artwork

Three to five generative plants grow from the bottom of the canvas using a 2D L-system (Lindenmayer system) turtle-graphics engine. Two plant types are rendered: a branching tree/shrub with a wide crown, and a vine with curling tendrils and grape-cluster nodes. Together they suggest the lushness of a Shavuot-decorated synagogue.

**L-system rules (tree):**
```
Axiom: F
F → FF+[+F-F-F]-[-F+F+F]
Angle: 25°
```

**L-system rules (vine):**
```
Axiom: F
F → F[+FF][-FF]F[+F][-F]
Angle: 20°
```

The turtle-graphics interpreter maintains a state stack: `[` pushes (x, y, angle, depth); `]` pops. Each `F` draws a line segment scaled by `0.6^depth`. `+` and `-` rotate by ±angle.

**Leaf nodes:** at terminal segments, a filled rotated ellipse is drawn in mid-green.

**Flower nodes:** at 1–2 levels above terminal, a five-petal flower is drawn using arc calls. Petals are white or soft rose; centers are yellow.

**Growth animation:** depth increments from 0 to max_depth (4) over ~4 seconds by revealing an increasing fraction of the L-system string. After full growth, the scene holds for 2 seconds, then the animation restarts.

## Palette

| Element | Colour |
|---------|--------|
| Canvas background | `#fafaf2` (off-white) |
| Stems / branches | `#2a5c1e` (deep green) |
| Leaves | `#4a8c3f` (leaf mid-green) |
| Flower petals (white) | `#ffffff` |
| Flower petals (rose) | `#d98c8c` (soft rose) |
| Flower centers | `#f5c842` (yellow) |

## Technique

**L-system expansion** — the production rules are applied iteratively, building a string of symbols. The turtle reads this string left-to-right to produce geometry.

**Progressive reveal** — each animation frame renders only the first `floor(progress * string.length)` symbols, giving the impression of growth from seed to full form.

**Canvas 2D** — all drawing uses `CanvasRenderingContext2D`: `lineTo` for segments, `ellipse` for leaves, arc-based petal loops for flowers.

**No external libraries** — the piece is fully self-contained in a single HTML file.
