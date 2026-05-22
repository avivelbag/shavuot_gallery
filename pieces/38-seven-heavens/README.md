# Through Seven Heavens — Parallax Descent

Mouse-driven CSS/JS parallax piece in which seven SVG layers, each
representing one of the seven heavens named in Talmud Bavli Ḥagigah 12b,
slide at different rates to create the illusion of depth.

## Layer stack (back → front)

| # | Heaven | Hebrew | Depth | Visual motif |
|---|--------|--------|-------|--------------|
| 1 | Vilon  | וִילוֹן | 0.02  | Wavy curtain-lines; Har Sinai mountain silhouette with golden peak glow |
| 2 | Rakia  | רָקִיעַ | 0.05  | Stars, moon crescent, כּוֹכָבִים label |
| 3 | Sheḥakim | שְׁחָקִים | 0.10 | Millstone circles with radial divisions |
| 4 | Zevul  | זְבוּל  | 0.18  | Heavenly Temple outline with altar |
| 5 | Ma'on  | מָעוֹן  | 0.28  | Harp silhouettes, beamed eighth-notes |
| 6 | Makhon | מָכוֹן  | 0.42  | Isometric storage cubes, snowflake motifs |
| 7 | Aravot | עֲרָבוֹת | 0.60 | White soul-dots, central throne-glow, Tetragrammaton (יהוה) |

## Technique

Each `.layer` div is absolutely positioned with 15% bleed (`top: -15%; left: -15%;
width: 130%; height: 130%`) so parallax shifts never reveal the container edge.

On `mousemove`, JavaScript normalises the cursor position to ±80 / ±60 px and
smoothly interpolates toward the target (0.08 lerp per frame). When the mouse
has been idle for more than 2 seconds, a Lissajous drift takes over:
`mx = 20·sin(t·0.3)`, `my = 12·sin(t·0.2)`.

Each layer's CSS `transform` is set to `translate(mx * depth, my * depth)`.
The animation loop runs via `requestAnimationFrame`.

**Theme:** Matan Torah / Seven Heavens — Ḥagigah 12b cosmology, God's descent to Sinai  
**Technique:** CSS/JS mouse-driven parallax with layered inline SVG
