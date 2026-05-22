# The Open Corner — Pe'ah

**Shavuot theme: Bikkurim / Harvest and Social Justice**

Leviticus 23:22 appears immediately after the Shavuot/Omer legislation — a commandment to leave the pe'ah (corner of the field), leket (fallen grain), and shikchah (forgotten sheaf) for the poor and the stranger. The piece renders this law as a living field with intentionally empty corners: the absence is the point.

## Technique

Pure canvas 2D, no libraries. Animated with `requestAnimationFrame` targeting ≤60 fps.

**Perlin noise** — a standard 256-element permutation table, shuffled at startup and doubled to 512. Gradient selection via a 4-case `_grad` function; quintic fade curve (`6t⁵ − 15t⁴ + 10t³`) for smoother interpolation than classic Hermite. The noise implementation is entirely inline, under 50 lines.

**Flow field** — the canvas is treated as a ~40×30 grid of stalk positions. For each stalk, the current flow angle is `noise2d(x * 0.015, y * 0.015 + time * 0.0003) * 2π`. The stalk tip is displaced from its base by `(cos(angle) * swayAmt, sin(angle) * 0.25 * swayAmt)`, reducing vertical sway to keep stalks reading as upright grain. Each stalk is a quadratic Bézier from base to tip, control point at mid-height with half the tip displacement.

**Pe'ah exclusion zones** — four rectangular corner zones (x < 15% AND y < 15% of canvas, etc.) exclude stalk placement entirely, creating the negative-space "open corners." The corner zones are drawn in a slightly lighter ground tone (`#3a2510`) to suggest turned earth.

**Batched rendering** — all stalks are split into two color groups (`#d4a017` and `#e8c850`) and drawn in two `beginPath`/`stroke` passes to minimize context-state changes with ~1200 stalks at 60 fps.

**Hebrew label** — `פֵּאָה` fades in over 3 seconds via `ctx.globalAlpha`; `ctx.direction = 'rtl'` ensures correct right-to-left rendering.

## Palette

| Element            | Colour                  |
|--------------------|-------------------------|
| Background (field) | `#2a1a08` (deep loam)   |
| Corner zones       | `#3a2510` (turned earth)|
| Stalk gold         | `#d4a017` (wheat gold)  |
| Stalk highlight    | `#e8c850` (pale gold)   |
| Hebrew label       | `#f5e6c8` (cream)       |
