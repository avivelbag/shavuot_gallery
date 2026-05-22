# Chag HaKatzir — Harvest Stipple Canvas

**Theme:** Chag HaKatzir / Harvest — Shavuot as the Wheat-Harvest Festival (Exodus 23:16)

**Technique:** Canvas 2D — stipple / halftone dot-density rendering, bezier path silhouette

## Description

Three bound wheat sheaves rendered entirely in stipple: ten thousand dots painted progressively over ~3 seconds, with dot density encoding luminance. The silhouette of the sheaves is defined as bezier paths in the canvas API; the stipple engine uses `ctx.isPointInPath` to distinguish sheaf interior from sky and applies different density gradients accordingly. After the image fully develops, the piece holds for 5 seconds, fades, and restarts.

Background: warm amber-gold (`#f5c842`) fading to pale gold at the top, with a sky gradient behind the sheaves grading from morning blue to golden. Sheaf dots are deep burnt-sienna (`#6b2800`) in shadow, lighter golden-brown in midtones. Hebrew text חַג הַקָּצִיר appears in the lower canvas.

## Sources

- Exodus 23:16 (Chag HaKatzir — Festival of the Harvest)
- Exodus 34:22 (Chag HaShavuot / wheat harvest)
- Leviticus 23:9–14 (the omer — first barley sheaf offering)
- Leviticus 23:15–17 (Shtei HaLechem — two wheat loaves on Shavuot)
- Leviticus 23:22 (pe'ah and shikchah — gleaning laws)
- Ruth 2:1–23 (Ruth gleaning in the fields of Boaz)

## Files

- `index.html` — self-contained stipple animation (no external dependencies)
- `thumbnail.svg` — static SVG preview approximating the stipple effect
- `gen_thumbnail.py` — Python script that generated the thumbnail SVG
- `essay.md` — accompanying essay on Chag HaKatzir
