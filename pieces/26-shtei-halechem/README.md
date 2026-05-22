# Shtei HaLechem — Two Loaves as Wave Interference

**Shavuot theme: Shtei HaLechem / Wheat Harvest**

Leviticus 23:17 commands two leavened loaves as the distinctive wave offering of Shavuot. The two-ness of the offering maps directly to wave interference: two point-sources emitting concentric sine-wave rings produce the constructive and destructive interference lattice that fills the canvas with warm wheat-gold and deep shadow.

## Artwork

An animated canvas 2D piece:

- **Two point-sources** are positioned symmetrically at 35% and 65% of canvas width, vertically centred.  Each source emits sine waves described by `sin(k·r − ωt)`, where *r* is the distance from the source to the pixel, *k* = 0.07 px⁻¹ (wavelength ≈ 90 px), and *ω* = 2.5 rad/s.
- **Wave superposition**: every pixel's amplitude is the sum of both waves, `sin(k·r₁ − ωt) + sin(k·r₂ − ωt)`, which ranges from −2 (fully destructive) to +2 (fully constructive).
- **Palette mapping**: amplitude is normalised to [0, 1] via `(val + 2) / 4` and passed through a 4-stop gradient:
  - v = 0.000 → `#2C1810` deep linen (destructive minimum)
  - v = 0.333 → `#A0622A` warm amber
  - v = 0.667 → `#D4A843` wheat gold
  - v = 1.000 → `#F5E6C8` parchment (constructive maximum)
- **Performance**: distances from each source to every pixel are precomputed once into `Float32Array` buffers; only `Math.sin` is called per frame.
- **Loaf markers**: each source position is overlaid with a small oval bread-loaf shape (canvas 2D ellipse + score marks) drawn on top via `putImageData` + subsequent 2D API calls.
- **Animation** uses `requestAnimationFrame`; `t` is derived from the elapsed wall-clock time so the cycle is frame-rate independent.

## Wave superposition formula

```
val(x, y, t) = sin(k · r₁ − ω · t) + sin(k · r₂ − ω · t)

where:
  r₁ = √((x − 280)² + (y − 300)²)
  r₂ = √((x − 520)² + (y − 300)²)
  k  = 0.07 px⁻¹
  ω  = 2.5 rad/s
```

Constructive interference (bright) occurs where `k·(r₁ − r₂) = 2πn`.
Destructive interference (dark) occurs where `k·(r₁ − r₂) = (2n+1)π`.

## Palette

| Value | Colour    | Code      |
|-------|-----------|-----------|
| 0     | Deep linen  | `#2C1810` |
| 0.333 | Warm amber  | `#A0622A` |
| 0.667 | Wheat gold  | `#D4A843` |
| 1     | Parchment   | `#F5E6C8` |

## Technique

- **Wave superposition / Moiré** — not used elsewhere in the gallery
- **ImageData pixel manipulation** — direct RGBA writes for per-pixel colour
- **Precomputed distance arrays** — Float32Array, computed once at startup
- **Canvas 2D painter's algorithm** — putImageData for interference field, then 2D API for loaf overlays
- **No external libraries** — fully self-contained single HTML file
