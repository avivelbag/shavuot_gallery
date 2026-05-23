# The Highways of the Night

**Shavuot theme: Tikkun Leil Shavuot**

Five turmites (Langton-family 2D Turing machines) run simultaneously on an 800×800 canvas, each following a distinct deterministic rule table. After thousands of steps of apparent chaos, long diagonal highways emerge — the emergent order of Tikkun Leil Shavuot rendered as multi-agent path tracing.

## Technique

Canvas 2D, ImageData pixel manipulation, no libraries.

**Turmites** — each ant reads its cell's color from its own independent `Uint8Array(400×400)` grid, writes a new color, turns, and moves. Rule tables include the classic Langton's Ant (RL), its mirror (LR), and three known four-state highway-forming rules (LLRR, LRRL, RLLR). The cell grids are fully independent so the ants' algorithms do not interfere; visually their trails overwrite each other, creating layered crossing highway patterns.

**Rendering** — a single `ImageData(800, 800)` is maintained. Each 400×400 cell maps to a 2×2 pixel block. Trail cells are painted in the ant's warm-tone color (alpha 0.85); cells written to state 0 are cleared to the background navy.

**Animation** — 10 turmite steps per `requestAnimationFrame` tick, capped at 60 fps. When all 5 ants have each taken 200 000 steps, the simulation resets with new random starting positions.

## Palette

| Element | Color |
|---------|-------|
| Background | `#0A0C1A` dark navy |
| Ant 1 — RL | `#D4A017` gold |
| Ant 2 — LR | `#C97B22` amber |
| Ant 3 — LLRR | `#B5651D` copper |
| Ant 4 — LRRL | `#F5DEB3` wheat |
| Ant 5 — RLLR | `#FFF8E7` cream |
