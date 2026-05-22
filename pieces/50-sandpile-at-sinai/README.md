# The Mountain That Could Not Be Touched — Abelian Sandpile at Sinai

Piece 50 of the Shavuot gallery. Interactive abelian sandpile simulation connecting the Sinai boundary command (Exodus 19:12–13) to the mathematics of self-organized criticality.

## Technique

Abelian sandpile cellular automaton on a 301×301 grid. Each cell accumulates integer grain counts; when a cell reaches four grains it topples, shedding one grain to each of its four cardinal neighbors. Grains are added 100 per frame to the center cell. The pile evolves until 200,000 grains have been added, then holds for 4 seconds and dissolves.

## Implementation

- **Dirty-cell queue**: a `Set` of flat cell indices replaces the naive full-grid scan, keeping each toppling wave O(toppled cells).
- **ImageData rendering**: `createImageData` + direct RGBA writes + `putImageData` once per frame; no per-cell `fillRect` calls.
- **Flash layer**: a `Uint8Array` marks cells that toppled in the current frame with a fire-white color, making the live cascade visible.
- **Vignette**: precomputed radial weight array darkens pixels toward corners.
- **Dissolve-restart**: `fadeAlpha` decreases over 90 frames; rendered by multiplying pixel RGB by `fadeAlpha × vignette`.

## Color mapping

| Grain count | Color | Hex |
|---|---|---|
| 0 | Deep mountain blue-black | `#0A0A18` |
| 1 | Deep stone grey | `#3A3050` |
| 2 | Warm sandstone | `#8B7355` |
| 3 | Harvest gold | `#D4A017` |
| Toppling | Fire-white flash | `#FFF8E7` |

## Files

- `index.html` — self-contained piece (no external deps)
- `essay.md` — 700-word essay on Sinai, self-organized criticality, and fractal structure
- `thumbnail.svg` — radial gradient SVG thumbnail with fractal arm lines
