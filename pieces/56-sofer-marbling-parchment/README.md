# Before the Letters — Ebru Marbling of Sacred Parchment

**Shavuot theme: Matan Torah / The Writing of the Torah — Exodus 24:3–4**

Shavuot marks the moment Moses first wrote the covenant (Exodus 24:4). Paper marbling (Ebru) — dropping ink onto water and combing it into swirling patterns — evokes parchment, ink, and the fluid moment before letters are fixed. The oral tradition is infinite and alive; writing crystallizes it into bounded form.

## Artwork

An animated canvas 2D Ebru simulation:

- **Drop phase**: 20 circular ink blobs fall at random positions; each spreads using `r(t) = r_max × √t`. Each new drop displaces existing ink via the classic Ebru formula `dx = r² / (r² + d²)`, where `d` is the distance from drop center to existing ink point.
- **Comb phase**: two sinusoidal distortion passes — horizontal then vertical — applied to the pixel buffer via `getImageData`/`putImageData`. Amplitude grows from 0 to 28 px over 1.5 s, producing the characteristic feathered swirl of Turkish marbling.
- **Text reveal**: after ~8 s, the Hebrew words **וַיִּכְתֹּב מֹשֶׁה** (Exodus 24:4, "And Moses wrote") fade over the fixed marbled surface — appearing only once the comb has completed and the ink can no longer move.
- **Loop**: 4-second display pause, then canvas fades to blank parchment and a new random marble begins.

## Palette

| Color | Hex | Meaning |
|-------|-----|---------|
| Parchment | `#FBF3DC` | water surface / background |
| Ink black | `#1C1208` | primary ink |
| Sepia brown | `#6B3F1A` | aged manuscript |
| Gold | `#C8960C` | illuminated manuscript gold |
| Azure | `#1E3A6A` | the sapphire floor beneath the divine presence (Exodus 24:10) |

## Technique

- **Ebru drop displacement** — `r² / (r² + d²)` attenuation by distance
- **Pixel buffer comb distortion** — two-pass sinusoidal row/column shift via `getImageData`/`putImageData`
- **Radial gradient ink rendering** — `createRadialGradient` per drop, `source-over` compositing
- **State machine animation** — `requestAnimationFrame` loop with phases: DROPPING → COMBING → TEXT_FADE → DISPLAY → FADE_OUT
- No external libraries — fully self-contained single HTML file
