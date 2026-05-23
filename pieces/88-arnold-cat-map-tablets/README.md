# Shattered and Restored: The Two Tablets

**Theme:** Luchot / the two tablets  
**Technique:** Arnold cat map (discrete area-preserving chaotic map)  
**Year:** 2026

The Arnold cat map scrambles the Hebrew text of the first commandment — אָנֹכִי יְהוָה — and then, inevitably, restores it. The map is a bijection on the 256×256 discrete torus: no information is lost, only rearranged. After exactly 192 iterations (the period for N=256), the original image is recovered exactly.

The piece maps to the shattering and restoration of the two tablets (Exodus 32, 34). The Midrash (Shemot Rabbah 46:1) teaches that when Moses broke the tablets, the letters flew back to heaven — the text was not destroyed, only the stone. The Arnold cat map literalizes this: the pixels are rearranged but never lost. Chaos is periodic. The original is always recoverable.

## Files

- `index.html` — animated canvas: tablet image scrambles and restores in a 23-second loop
- `essay.md` — theological and mathematical essay (~380 words)
- `thumbnail.svg` — 400×400 thumbnail showing one scrambled and one legible tablet

## Animation phases

1. **SHATTERING** (iterations 0–96, 120 ms each): tablets disintegrate into noise
2. **PAUSE** (1.5 s): holds on the maximally-scrambled state  
3. **RESTORATION** (iterations 97–192): image reconstitutes letter by letter
4. **PAUSE** (2 s): holds on the restored image, then restarts

A warm-red fire tint (#FF3300, peak alpha 0.15) rises and falls between iterations 48 and 144, evoking the golden calf.
