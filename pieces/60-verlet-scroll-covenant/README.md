# 60 — HaBrit: The Covenant Unfurls

**Theme:** Matan Torah — the covenant ceremony of Exodus 24:3–8  
**Technique:** Verlet integration / cloth simulation (2D mass-spring grid)

## Description

A parchment Torah scroll unrolls under real-time cloth physics. The scroll is modeled as a 20×40 grid of mass-spring points connected by structural, shear, and bend constraints. Gravity pulls the cloth downward; the top row is pinned to a gold horizontal rod. Rows are released one by one during the unrolling phase, then gather back to loop.

Hebrew text — *וַיִּקַּח סֵפֶר הַבְּרִית* (Exodus 24:7) and *נַעֲשֶׂה וְנִשְׁמָע* — is pre-rendered on an offscreen canvas and mapped onto the cloth surface using per-triangle affine texture projection. The text deforms with the cloth grid.

## Differentiation from related pieces

- **42-sinai-chuppah**: Simulates a canopy (chuppah) blowing in wind using a 22×22 Verlet grid — different subject (mountain-as-chuppah, Shabbat 88a coercion midrash), different orientation (horizontal canopy vs. hanging scroll), different palette (cobalt/white vs. parchment/gold), no texture mapping.
- **55-unfurling-scroll-ruth**: Animated scroll of Ruth — different subject (Ruth's loyalty), different technique (no Verlet physics, no cloth simulation), no Hebrew text on cloth surface.

## Physics parameters

| Parameter | Value |
|---|---|
| Grid | 20 columns × 40 rows |
| Segment length | 13 px |
| Gravity | 0.25 px/frame² |
| Damping | 0.985 |
| Constraint iterations | 10 |
| Unroll rate | 1 row per 80 ms |
| Cycle | ~10 s (unroll 3.2s + hold 4s + reroll 3s) |

## Source

Exodus 24:3–8 — the covenant ceremony: Moses wrote the words, built an altar, read the Sefer HaBrit aloud, and the people declared *naaseh v'nishma*. Moses sprinkled blood on the people: "This is the blood of the covenant."

Talmud, *Shabbat* 88a: at the moment Israel said *naaseh* before *nishma*, they attained the mode of angels.
