# Lo Bashamayim Hi — Not in Heaven

A canvas-2D gravitational n-body particle simulation in which a brilliant
emitter at the top-centre releases cool blue-white particles that fall under
the gravitational pull of four "scholar" attractor nodes at the bottom.
Particles settle into warm gold clusters. Theme: the irrevocable transfer of
Torah's interpretive authority to human hands — Deuteronomy 30:12 and the
Oven of Akhnai story, Bava Metzia 59b.

## Technique

Each frame, 2–4 particles are emitted from the top-centre emitter with a
slight random horizontal scatter and a downward initial velocity. Every active
particle accumulates Newtonian gravitational force from each of the four
attractor nodes:

```
F = G / max(r², min_r²),   capped at MAX_ACCEL
```

A small global downward drift supplements gravity for particles far from the
attractors. Velocity is damped by a factor of 0.997 per frame so orbits
gradually decay rather than persisting indefinitely.

**Capture:** when a particle's distance to any attractor falls below 33 px it
is transferred from the `active[]` array to `settled[]`, positioned at a
random point within the capture radius. Settled particles are rendered in warm
gold (#E8B84B); active particles in cool blue-white (#C8D8FF) that fades in
over ~28 frames.

**Emitter corona:** a pulsing radial gradient (radius oscillates ±6 px on a
slow sine) renders the divine source as a brilliant white point with a soft
blue-white halo.

**Attractor halos:** each node draws a radial gradient in deep amber (#C06A10)
whose intensity scales with the number of settled particles at that node,
building from transparent to full glow as the cluster forms.

**Hebrew text arc:** an SVG overlay (same dimensions as the canvas, updated on
resize via `viewBox`) draws the text "לֹא בַשָּׁמַיִם הִוא" along a quadratic
bezier arc at ~46% canvas height using `<textPath>`.

No external dependencies; animation runs via `requestAnimationFrame`.

**Theme:** Matan Torah / Lo Bashamayim Hi — Deuteronomy 30:12; Bava Metzia 59b  
**Technique:** canvas 2D n-body gravity simulation — not used elsewhere in the gallery
