# They Saw the Voices — Lissajous at Sinai

A canvas-2D Lissajous figure animating the synaesthetic revelation at Sinai:
Exodus 20:15 (Hebrew), *"all the people saw the thunderings."*

## Technique

Two independent phase accumulators `φx` and `φy` advance each frame at
`ωx · BASE_OMEGA` and `ωy · BASE_OMEGA`. The plotted point is
`(A·sin(φx + δ), A·sin(φy))` where `δ` drifts slowly to prevent the figure
from ever closing completely and holding still.

**Frequency ratio schedule:** 1:1 → 2:1 → 3:2 → 3:4 → 5:3 → 4:3, cycling
continuously. Each transition is interpolated over ~8 seconds (smoothstep
easing); each closed figure is briefly held for ~3 seconds before the next
transition begins.

**Phosphor trail:** instead of clearing the canvas each frame, a
semi-transparent dark rectangle (`rgba(0,0,8,0.04)`) is drawn over the
previous frame, so old points fade slowly. A bright circle and radial-gradient
glow are drawn at the current point.

**Color:** a `colorPhase` variable (0–1) cycles slowly. In the first half it
interpolates from electric blue (HSL 220, 100%, 55%) toward white. In the
second half it drifts from white toward amber/gold (HSL ~45, 100%, 50%),
evoking Sinai's lightning and fire.

**Hebrew text:** `וְכָל-הָעָם רֹאִים אֶת-הַקּוֹלֹת` (Exodus 20:15) is rendered in
a small serif font at bottom-center with `direction: rtl`, at low opacity so
it does not compete with the figure.

Animation runs at 60fps via `requestAnimationFrame`; no external dependencies.

**Theme:** Matan Torah / Synaesthetic revelation — Exodus 20:15 (Hebrew); Mechilta d'Rabbi Ishmael, Yitro 9  
**Technique:** canvas 2D — two-frequency Lissajous oscillator, phosphor-persistence trail, slow ratio interpolation
