# First of All the Fruit of the Ground

**Piece 84** — Shavuot Gallery 2026

## Theme

Bikkurim / first fruits / harvest — Deuteronomy 26:1-11. The farmer brings the first of all
the fruit of the ground to the Temple, reciting the mini-history of Israel (vv. 5-9: "My father
was a wandering Aramean…") while holding the basket before the priest. The Mishnah tractate
*Bikkurim* describes the procession: caravans led by a flute player and an ox with gilded horns,
craftsmen of Jerusalem setting down their tools to greet the pilgrims.

The non-obvious insight: Bikkurim is not a tithe but a ritualized re-enactment of gratitude.
The gift is made before the farmer knows whether the rest of the harvest will come — offering
the best before knowing if anything else will follow.

## Technique

**Poisson disk sampling (Bridson's algorithm, 2007)** — places points with guaranteed minimum
spacing (r = 18 px) while looking organically random, the mathematical structure of a cultivated
field at maximum density without crowding. The algorithm runs incrementally: one iteration of
the active-list loop per requestAnimationFrame, with each accepted point drawn immediately as
either a wheat grain, a barley kernel, or a grape circle. Glyph type is determined
deterministically from a hash of (x, y) so the layout is reproducible.

**Animation phases:**
1. *Growth* — Bridson's active-list loop runs one step per rAF frame; each accepted point is
   drawn immediately on the field canvas in the correct glyph style.
2. *Wind shimmer* — every 3 seconds after the field fills, 30 randomly chosen grains scale up
   to 1.15× and back over 0.8 s on the overlay canvas, as if a breeze passes.
3. *Hebrew overlay* — after the field fills, the word בִּכּוּרִים (Bikkurim) fades in at
   ~96 px centered on the overlay canvas; a dark earth semi-transparent layer covers the field
   except where the letterforms are, so the field is visible through the text.

## Files

- `index.html` — full-viewport two-canvas layout; essay embedded inline
- `essay.md` — the essay source (~400 words; Deuteronomy 26:1-11; Mishnah Bikkurim)
- `thumbnail.svg` — 400×400 dark earth background with ~80 scattered wheat/barley/grape glyphs
  and the Hebrew word בִּכּוּרִים in faint outline at the center
- `README.md` — this file

## Sources

- Deuteronomy 26:1-11 — the Bikkurim commandment and the Aramean declaration
- Mishnah *Bikkurim* — the procession to Jerusalem (gilded ox, flute, craftsmen greeting)
- Bridson, R. (2007). "Fast Poisson Disk Sampling in Arbitrary Dimensions". *SIGGRAPH Sketches*
