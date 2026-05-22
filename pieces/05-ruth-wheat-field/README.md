# Where You Go — Ruth in the Wheat Field

**Shavuot theme: Book of Ruth**

The Book of Ruth is read on Shavuot. At its heart is Ruth's declaration to Naomi: *"Where you go I will go, and where you stay I will stay"* — one of the most complete statements of loyalty and chosen belonging in all of scripture. This piece sets that moment in the wheat fields of Bethlehem: two figures at the edge of the harvest, one turning back, one pressing forward.

## Technique

Pure canvas 2D, no libraries. Animated with `requestAnimationFrame` targeting ≤60 fps.

**Flow field / value noise** — a 64×64 grid of random floats is built once at startup. Bilinear interpolation with a smoothstep fade curve (`3t² − 2t³`) gives continuous, band-limited output. Each stalk samples the field at its normalised position plus a time offset, producing coherent lateral wind drift that ripples across the field without hard resets.

**Wheat stalks** — ~300 stalks placed on a jittered grid covering the lower ~60% of the canvas. Each stalk is a single quadratic Bézier curve from root to tip; the tip's horizontal displacement is driven by the noise sample scaled to ±30 px. A per-stalk `createLinearGradient` shades from dark gold at the root (`#7a5500`) through mid gold (`#d4a017`) to bright yellow at the tip (`#f0c84a`). A small ellipse at the tip represents the wheat head. Stalk heights vary ±20% around a base of ~13% of canvas height.

**Silhouettes** — two static `Path2D` shapes in near-black (`#1a0f00`) represent Naomi (left, arm reaching leftward — departing) and Ruth (right, arm reaching rightward — following). Built from leg trapezoids, body trapezoids, and ellipse heads; no external asset.

**Hebrew text** — `ctx.direction = 'rtl'` is set before rendering כִּי אֲשֶׁר תֵּלְכִי אֵלֵךְ in a translucent bar at the bottom of the canvas.

## Palette

| Element | Colour |
|---------|--------|
| Sky (top) | `#c8a96e` (warm amber) |
| Sky (horizon) | `#f5e6c8` (parchment) |
| Stalk root | `#7a5500` (dark gold) |
| Stalk mid | `#d4a017` (golden wheat) |
| Stalk tip / head | `#f0c84a` (bright gold) |
| Silhouettes | `#1a0f00` (near-black brown) |
| Text bar | `rgba(0,0,0,0.38)` |
| Text | `rgba(255,248,220,0.92)` (cream-white) |
