# 55 — The Unfurling Scroll — Megillat Ruth

**Theme:** Book of Ruth / Megillat Ruth / Shavuot  
**Technique:** Canvas 2D — procedural calligraphic stroke animation, bezier path lettering, scroll unfurl

## Shavuot Connection

Megillat Ruth is read aloud from a handwritten scroll on Shavuot. The physical act of unrolling the megillah is part of the reading: the text comes into view as the scroll is opened. This piece makes that act visible. The parchment unfurls between two wooden rollers and the Hebrew letters of Ruth 1:16 — the declaration of loyalty — appear stroke by stroke, as if written by a sofer's pen in real time.

## Algorithm

### Scroll Unfurl

A canvas 900×500 scene. Two cylindrical wooden rods are drawn with radial gradient fills (warm highlight → dark shadow) at the left and right edges. The visible parchment width expands from 0 to the full span over ~2 seconds using a lerp toward the target width each frame. A noise texture pass — small semi-transparent circles at seeded positions — gives the parchment surface a subtle aged appearance.

### Stroke-by-Stroke Calligraphy

Each Hebrew letter in the verse is encoded as an array of canvas 2D path commands (`moveTo`, `lineTo`, `bezierCurveTo`). The control points are hand-authored to produce a calligraphic feel — not pixel-perfect but deliberately hand-drawn in style. A `drawProgress` counter advances at ~0.008 per frame (roughly 125 frames = ~6 seconds for the full verse at 60 fps). The counter maps to a letter index and a within-letter t value. Completed letters are drawn in full; the in-progress letter is drawn up to the current t by evaluating partial bezier segments.

Stroke style: `#1A0A00`, lineWidth 3, lineCap `round`, lineJoin `round`.

### Breathing Post-Reveal

After all letters are complete, the text enters a breathing state: a `shadowBlur` pulse applied each frame — `4 + 3 * sin(t * 0.001)` — with shadowColor `#C9A84C` (deep gold). The rollers also gently pulse in scale.

## Palette

| Role | Hex |
|---|---|
| Parchment cream | `#FFF8DC` |
| Ink near-black | `#1A0A00` |
| Wooden rod warm brown | `#8B5E3C` |
| Scroll shadow deep gold | `#C9A84C` |
| Background | `#2A1A0A` |

## Source References

- Ruth 1:16 (the declaration: your people shall be my people)
- Talmud Yerushalmi, Megillah 3:5 (custom of reading Ruth on Shavuot)
- Rabbi Joseph B. Soloveitchik — parallel between Ruth's acceptance and the Sinai covenant
