# The Crowns — Tagin Pen-Plotter

**Shavuot theme: Tagin / Crown of Torah**

Tagin are the tiny ornamental crown-strokes found above certain letters in a Torah scroll. Their origin is described in Talmud Bavli Menachot 29b: Moses at Sinai sees God tying crowns onto the letters of the Torah. A key reading by the Maharsha (Rabbi Shmuel Eliezer Eidels) interprets this as a statement about the inexhaustible depth of Torah — crowns that would only be interpreted centuries later by Rabbi Akiva.

## Artwork

A single Hebrew letter shin (שׁ) is drawn on a parchment-colored canvas using simulated pen-plotter technique: thin bezier curves with slight hand-tremor jitter (±0.4 px random offset), rendered at 85% opacity to simulate ink bleed on parchment.

**Animation sequence:**
1. The shin is drawn stroke by stroke (~0.8 s per stroke): base bowl, left arm, middle arm, right arm.
2. After the letter is complete, tagin bloom at each of the three arm tips — three tiny upward-arcing flourishes per tip, the traditional three-stroke crown.
3. The complete image holds for 5 seconds, then fades and restarts. Total loop ≤ 13 s.

## Technique

**Pen-plotter simulation:**
- `lineWidth = 1.8`, `lineCap = 'round'`
- `strokeStyle = rgba(58,31,13,0.85)` (deep sepia at 85% opacity)
- Bezier paths are pre-computed with per-point jitter (JITTER = 0.4 px) so lines remain stable between frames
- 200 interpolated steps per bezier ensure smooth curves

**Letter geometry:**
- The shin occupies roughly 60% of the 600×600 canvas (360 px)
- Four strokes: base bowl + three arms (left, middle, right)
- Tagin at each arm tip: three arcs fanning left, center, right

## Palette

| Element | Colour |
|---------|--------|
| Background | `#f2ead8` (aged parchment) |
| Ink | `#3a1f0d` (deep sepia) at 85% opacity |

## Files

- `index.html` — self-contained canvas animation with essay embedded
- `essay.md` — ~480-word essay on tagin, Menachot 29b, the Maharsha
- `thumbnail.svg` — 400×400 monochrome static preview
