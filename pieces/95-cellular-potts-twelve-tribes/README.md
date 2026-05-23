# As One Person, With One Heart

**Theme:** Matan Torah / the twelve tribes at Sinai
**Technique:** Cellular Potts model (Graner-Glazier, Metropolis Monte Carlo)

A 2D cellular Potts model on a 200×200 lattice where each of the twelve cell types represents one of the twelve tribes of Israel. From a randomly mixed initial state, the Metropolis Monte Carlo algorithm — with a surface-tension energy penalizing unlike-neighbor boundaries — drives the system toward coherent tribal territories radiating outward from a central void (the Tabernacle courtyard). As temperature decreases from T=10 to T=0.01, sorting completes. When the lattice converges, the text "כאיש אחד בלב אחד" fades in gold over the central void, holds three seconds, then the simulation resets and loops.

The piece embodies the Midrash on Exodus 19:2: the singular verb *va-yichan* ("and Israel camped there") signals that twelve distinct tribes achieved unity — not by merging, but by each finding its coherent territory around the common center. The Potts model makes this visible as physics.

## Primary sources

- **Exodus 19:2** — the singular *va-yichan*, "and Israel camped there" (Midrash: as one person with one heart)
- **Exodus 24:4** — Moses built an altar with twelve pillars for the twelve tribes
- **Numbers 2** — the precise encampment arrangement around the Tabernacle

## Files

- `index.html` — full animation with embedded essay; bilingual Tanach excerpts
- `essay.md` — written commentary (~480 words)
- `thumbnail.svg` — 400×400 stylized top-down view of 12 tribal sectors around a dark center
- `README.md` — this file
