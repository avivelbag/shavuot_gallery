# Etz Chaim — A Tree of Life to Those Who Hold Her

**Shavuot theme: Crown of Torah / Etz Chaim — Torah as Living Tradition**

Proverbs 3:18 calls Torah "a tree of life to those who hold fast to her" (עֵץ חַיִּים הִיא לַמַּחֲזִיקִים בָּהּ). This verse is sung each time the Torah scroll is returned to the ark, linking the Shavuot moment of first giving to the ongoing act of holding. The space colonization algorithm (Runions 2007) grows a vascular tree by iteratively extending branch tips toward a field of scattered attractor points, producing an organic canopy shape without any pre-programmed blueprint — just as the living tradition emerges from the encounter of a fixed root (Sinai) and the needs of each generation.

## Artwork

A canvas animation runs the space colonization algorithm in real time. A single root node sits at the bottom center of the canvas; ~300 attractor points are scattered in an elliptical canopy region occupying the upper two-thirds of the frame. Each frame, active branch tips sense attractors within a perception radius of 80 px, average the unit direction vectors toward them (with a small upward bias), and extend one segment of 6 px. Attractors within 12 px of any node are consumed. When no attractors remain reachable, growth stops, the canvas holds for 3 seconds, then fades to near-black, and the cycle restarts with a new random attractor field.

## Algorithm

**Space colonization (Runions 2007)**

```
PERCEPTION_RADIUS = 80 px
KILL_RADIUS       = 12 px
SEGMENT_LENGTH    =  6 px
UPWARD_BIAS       =  0.35
```

Each tip accumulates normalized direction vectors to all attractors within PERCEPTION_RADIUS, adds an upward bias component, normalizes the result, and steps by SEGMENT_LENGTH. Attractors consumed by the kill radius are removed. Tips with no attractors in range die. New child nodes become the new tips. Branching emerges naturally as distinct attractor clusters pull adjacent tips in different directions.

## Palette

| Element | Colour |
|---------|--------|
| Background | `#0A1A0D` (deep forest green) |
| Branches at root | `#D4A017` (warm harvest gold) |
| Branches at tips | `#FFFBF0` (pale ivory) |
| Attractor cloud | `rgba(180,215,80,0.18)` (faint green-gold dots) |
| Hebrew inscription | `#D4A017` with glow |

## Technique

**Space colonization algorithm** — vascular tree growth, no fixed branching grammar.

**Canvas 2D** — all rendering via `CanvasRenderingContext2D`: `lineTo` for branch segments, variable `lineWidth` for taper (6px at root → 1px at tips), `arc` for attractor dots.

**Cycle animation** — grow phase (~20–30 s) → hold (3 s) → fade-to-black (2 s) → restart.

**No external libraries** — fully self-contained single HTML file.
