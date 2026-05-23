# Mountain Burning to the Heart of Heaven — Burning Ship Fractal

A full-viewport interactive Burning Ship fractal rendered via WebGL fragment shader,
themed on Deuteronomy 4:11–12: "the mountain burned with fire to the heart of
heaven — darkness, cloud, and thick darkness."

**Theme:** Har Sinai / consuming fire

**Technique:** Burning Ship fractal (smooth escape-time coloring via fractional
iteration count; WebGL fragment shader at 512 iterations per pixel; fire palette
from ember red through flame orange, gold, to white-hot; interior set black as the
unconsumed mountain core)

## Mathematical Insight

The Burning Ship differs from Mandelbrot by one operation: taking absolute values
of Re(z) and Im(z) before each squaring. This folds the complex plane, replacing
smooth circular orbits with jagged flame-like asymmetric structures.

```
z_{n+1} = (|Re(z_n)| + i|Im(z_n)|)² + c
```

The black interior — the set of points that never escape after 512 iterations —
is the unconsumed mountain core. The exterior filaments glow in proportion to
how quickly they escape: slowly escaping points (near the boundary) are white-hot;
quickly escaping points (far from the set) are dark ember red.

## On-Load Animation

An 8-second initial zoom animates from the full ship view (Re: [−2.0, 1.2],
Im: [−1.8, 0.2]) into the dramatic mast/flame filament near (−0.4, −0.55) at
width 0.08, revealing the fractal depth of the fire. Drag to pan; scroll or
pinch to zoom freely after the animation settles.

## Sinai Connection

Deuteronomy 4:11–12 describes the mountain burning with fire while surrounded
by thick darkness. The Burning Ship renders this paradox geometrically: a
bounded black interior (the unconsumed mountain) encased in infinite gradations
of fire (the escaped exterior), with an infinitely complex boundary between them.
The fire extends to every zoom level — there is no bottom, just as Sinai's
revelation has no final depth.

## Technical Notes

- WebGL 1.0 / GLSL ES 1.0 fragment shader
- 512 maximum iterations; smooth coloring via fractional escape count (log formula)
- Canvas 2D fallback for environments without WebGL
- Device pixel ratio aware (renders at full retina resolution)
- Touch support: single-finger pan, two-finger pinch-to-zoom
