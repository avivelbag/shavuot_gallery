# The Voice Grew Louder — Kol HaShofar Chladni

A canvas-2D Chladni figure simulation that cycles through 50 resonant modes
of a square vibrating plate, one per day of the Omer count. Theme: the shofar
at Sinai that "grew louder and louder" (Exodus 19:19), the mountain that quaked
(Exodus 19:18), and the 49-day Omer journey culminating in Shavuot.

## Technique

The Chladni eigenfunction for mode (m, n) on a square plate:

```
f(x, y) = cos(n·π·x)·cos(m·π·y) − cos(m·π·x)·cos(n·π·y)
```

where x, y ∈ [−1, 1]. Pixels where |f| < threshold receive the sand (gold)
color; those in the glow band (threshold < |f| < 3·threshold) fade smoothly
to background via a quadratic falloff; pixels above that are dark background.

**Grid:** 400×400 field values computed into a `Float32Array`. Rendered via
`ImageData` into an offscreen 400×400 canvas, then drawn scaled to fill the
art panel. Field recomputation happens once per mode change; per-frame cost
is only the blend loop (during transitions) and the ImageData paint.

**Mode sequence:** 50 (m, n) pairs chosen for visual distinctness, progressing
from simple (low m+n) to intricate (high m+n). No (m, m) pairs (they give
the zero field). Consecutive pairs differ enough in m/n ratio that transitions
are clearly visible.

**Morphing:** during the 2-second (~120-frame) transition between modes,
the blended field is `lerp(fieldA, fieldB, smoothstep(t))`. The smoothstep
easing gives the sand an organic "rearranging" feel rather than a linear fade.

**Timing:** each mode holds for ~4 s (~240 frames at 60 fps), then transitions
over ~2 s (~120 frames). Full 50-mode cycle ≈ 300 seconds (~5 minutes).

**Day 50 (Shavuot):** the threshold is modulated by `1 + 0.15·sin(tick·0.06)`,
making the nodal line width pulse gently. The label "חַג הַשָּׁבֻעוֹת" is
rendered larger with an amplified shadow glow.

**Hebrew counter:** bottom-right corner, RTL, `18px Georgia serif`. The array
of 50 Hebrew ordinal day names (יוֹם אֶחָד … יוֹם אַרְבָּעִים וְתִשְׁעָה,
then חַג הַשָּׁבֻעוֹת) is embedded in the script.

**Palette:** deep warm black #0A0804 background; wheat-gold #E8C870 nodal
lines with a quadratic-falloff glow. Suggests sand on a resonating plate.

No external dependencies; animation driven entirely by `requestAnimationFrame`.

**Theme:** Kol HaShofar / Matan Torah — Exodus 19:16–19; Leviticus 23:15–16  
**Technique:** canvas 2D — Chladni eigenfunction vibration simulation, ImageData pixel rendering, field morphing
