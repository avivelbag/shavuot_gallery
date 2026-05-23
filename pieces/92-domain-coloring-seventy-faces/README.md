# Seventy Faces of the One

**Shavuot theme: Matan Torah / שבעים פנים לתורה (seventy faces of Torah)**

Domain coloring of f(z) = z⁷⁰ − 1 over the complex plane. Each pixel's hue is the argument of f(z); saturation is fixed at 0.85; lightness oscillates with log|f(z)| to produce modular shading (bright rings at each order of magnitude). The 70 zeros of f — the 70th roots of unity — appear as dark points on the unit circle.

The view rotates slowly: z is replaced by z·e^{−iθ} each frame, spinning the 70-petaled color pattern around the origin at 0.003 rad/frame, completing one full turn in approximately 2100 frames (~35 s at 60 fps).

## Source

Bamidbar Rabbah 13:15 — "Torah has seventy faces" (שִׁבְעִים פָּנִים לַתּוֹרָה).
Sanhedrin 34a — a single verse yields many simultaneous senses.
Exodus 24:1, 9 — the seventy elders who ascended Sinai.

## Technique

- Canvas 2D ImageData pixel loop (no per-pixel fillRect)
- z⁷⁰ via repeated squaring: 7 squarings and 2 multiplications (z⁶⁴ · z⁴ · z²)
- HSL → RGB conversion in pure JavaScript
- requestAnimationFrame animation with 16 ms frame-time guard

## Files

- `index.html` — self-contained animated piece
- `essay.md` — ~400-word essay on the Shavuot source and the mathematics
- `thumbnail.svg` — static 400×400 pre-computed domain-coloring approximation
