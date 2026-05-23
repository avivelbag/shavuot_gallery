# Seven Weeks, Seven Days: The Arctic Circle of the Omer

**Theme:** Sefirat HaOmer — seven complete weeks, the 7×7 grid of the Omer count (Leviticus 23:15–16)

**Technique:** Random domino tiling / Aztec diamond shuffling algorithm (Propp-Wilson)

## Description

An Aztec diamond of order 14 is tiled by the shuffling algorithm — create, annihilate, and slide dominoes — built up step by step from order 1 to order 14 with a 400ms pause between steps. Each domino is colored by its direction (north/south/east/west). After construction the 49 central squares are highlighted one by one with a gold pulse and an Omer-day counter. Then a new random tiling is generated and crossfaded in, looping indefinitely to demonstrate the uniformity of the distribution and the invariance of the arctic circle boundary.

The Aztec diamond of order 7 contains exactly 49 inner unit squares — one per day of the Omer count. The arctic circle theorem guarantees that the boundary between the four "frozen" corner regions and the chaotic central disk is almost always a perfect circle. The four frozen corners correspond to the four living creatures of the Merkavah (Hagigah 13a); the chaotic center is the divine cloud.

## Files

- `index.html` — self-contained animation with embedded essay (no external dependencies)
- `thumbnail.svg` — static preview showing the Aztec diamond with colored domino regions and circular boundary
- `essay.md` — accompanying essay connecting the arctic circle theorem to the Omer and Merkavah

## Sources

- Leviticus 23:15–16 (the biblical commandment to count seven complete weeks)
- Talmud Bavli, Hagigah 13a (the four living creatures of the Merkavah)
- Zohar, Emor III:97b (the 7×7 grid of sefirot combinations)
- Jockusch, Propp, Shor — "Random Domino Tilings and the Arctic Circle Theorem" (1998)
