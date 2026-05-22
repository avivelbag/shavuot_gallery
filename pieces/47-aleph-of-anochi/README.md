# The Aleph of Anochi — Lorenz Attractor

A canvas-2D Lorenz strange attractor orbiting the silent aleph (א).
Theme: the teaching (*Shemot Rabbah* 29:9; *Makkot* 24a) that Israel received
only the first letter of the first word of Torah at Sinai — the silent aleph —
and that the whole of Torah is contained within that single bounded origin.

## Technique

The **Lorenz system** (σ = 10, ρ = 28, β = 8/3) is integrated with **Runge-Kutta 4**
at dt = 0.005. Each animation frame advances the integrator by 300 steps and draws
each step as a short `lineWidth = 0.8` stroke on the canvas.

**Projection:** the x–z plane of the Lorenz orbit gives the classic butterfly
silhouette. The coordinate range x ∈ [−22, 22], z ∈ [0, 50] is mapped to the
canvas with 10% padding on all sides.

**Fading trail:** each frame begins with a semi-transparent fill (`globalAlpha = 0.008`,
color #08061A) that slowly erases old strokes. This gives a persistent phosphor-trail
effect — recent orbit sections stay bright while older parts fade to black, creating
the impression of continuous emergence.

**Velocity coloring:** the velocity magnitude `‖(dx, dy, dz)‖` is computed at each RK4
step and normalised over the observed range. The three-stop color gradient is:
- slow (0–0.33) → deep violet `#4A1A8C`
- mid (0.33–0.67) → royal blue `#1A4ACA`
- fast (0.67–1.0) → gold `#D4A017` → near-white `#F5F0E0`

**Aleph glyph:** a single large aleph (60% of canvas shorter dimension, weight 100
"Noto Serif Hebrew" or fallback) is rendered to an offscreen canvas and then composited
onto the main canvas each frame with `globalCompositeOperation = 'screen'` at 5% opacity.
This makes the letter permanently visible without occluding the orbit; the attractor
appears to weave through and around the letter's three strokes.

**Background:** #08061A (deep indigo-black).

No external dependencies. Animation runs via `requestAnimationFrame`.

**Theme:** Matan Torah / The Aleph of Anochi — Shemot Rabbah 29:9; Makkot 24a  
**Technique:** canvas 2D — Lorenz strange attractor, RK4 integration, velocity-colored orbit, aleph glyph screen compositing
