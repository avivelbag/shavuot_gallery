# "Honey and Milk Beneath Your Tongue" — Moiré Hexagonal Grids

**Theme:** Milk and Honey — the twenty-times-repeated promise of *eretz zavat chalav u'dvash*, culminating in Song of Songs 4:11 as an allegory for Torah

**Technique:** moiré interference / overlapping hexagonal grids

## Description

A 700×700 canvas animation drawing two hexagonal grids at slightly different scales. The "milk" grid (cream #F5EDD5, spacing 28px) stays fixed. The "honey" grid (deep gold #C8920A, spacing 30px) slowly rotates about the canvas center at 0.0008 radians per frame — approximately thirteen minutes per full revolution at 60fps.

The moiré interference pattern arises from the 28:30 spacing ratio (≈ 14:15). Every fourteen milk cells and fifteen honey cells the grids come back into alignment, producing a beat frequency visible as slowly-drifting concentric oval rings that form, swell, and dissolve across the near-black (#080600) background.

A second animation layer adds breathing life: the milk grid's opacity pulses gently between 0.6 and 1.0 with a period of approximately eight seconds using `Math.sin(t * 0.008) * 0.2 + 0.8`. Both grids use `globalAlpha` on the canvas context.

At the bottom of the canvas a Hebrew caption in #C8920A reads "דְּבַשׁ וְחָלָב תַּחַת לְשׁוֹנֵךְ" — Song of Songs 4:11, "honey and milk beneath your tongue" — at 80% opacity.

## Sources

- Exodus 3:8 (first occurrence of "eretz zavat chalav u'dvash" — God's words to Moses at the burning bush)
- Rashi on Exodus 3:8 (citing the Midrash on spontaneous milk and fig-honey)
- Babylonian Talmud, Ketubot 111b (empirical observation of milk-and-honey abundance in Bnei Brak)
- Song of Songs 4:11 (honey and milk as allegory for Torah)
- Midrash Shir HaShirim Rabbah 4:11 (the beloved as Israel, the lover as God)
- Psalm 19:11 (Torah sweeter than honey and the honeycomb)

## Files

- `index.html` — self-contained moiré canvas animation (no external dependencies)
- `thumbnail.svg` — static SVG preview of two overlapping hexagonal grids at 5° offset, 400×400
- `essay.md` — accompanying essay on milk and honey in Torah, the Talmudic measurement, and Song of Songs
