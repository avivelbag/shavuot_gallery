# Adorned with Roses: A Shavuot Garden

**Piece 87** — Shavuot Gallery 2026

## Theme

Greenery and flowers / Matan Torah — the ancient minhag of decorating synagogues with flowers on Shavuot, recorded by the Rama (Orach Chaim 494:3) as a memorial to the flowers that bloomed at the foot of Har Sinai before the Torah was given. Sources: Shir HaShirim Rabbah 1:2, Pirkei DeRabbi Eliezer ch. 41, Shabbat 88b.

## Technique

**Centroidal Voronoi Tessellation / Lloyd's relaxation algorithm.**

280 seed points are placed randomly on the canvas and assigned to Voronoi cells via grid-accelerated nearest-neighbour search. Each Lloyd iteration moves every seed to the centroid of its Voronoi cell, producing a progressively more regular tessellation. The animation runs at approximately 4 iterations per second (one step every 250 ms), stopping after 60 iterations or when maximum seed displacement falls below 0.5 px.

During the relaxation phase, cells are coloured by their assigned flower type at reduced saturation (0.35). On convergence, a 60-frame bloom transition lerps saturation to 1.0. The final breathing phase overlays 6–8 elliptical petals per seed, radiating from each centroid, with scale breathing ±5 % at 0.4 Hz.

Five flower types: white anemone (#FAFAF2 petals), purple iris (#7B5EA7), soft pink rose (#F4B8C1), field yellow (#F5E642), pale blue cornflower (#A8C4E0). Background: deep botanical green #1A2E1A.

## Files

- `index.html` — full-viewport canvas animation with essay embedded inline
- `essay.md` — essay source (~340 words; Orach Chaim 494:3, Shir HaShirim Rabbah, Pirkei DeRabbi Eliezer, Shabbat 88b)
- `thumbnail.svg` — 400×400 deep green background with 33 stylised flowers in a hex-tessellated arrangement
- `README.md` — this file

## Sources

- Rama, Orach Chaim 494:3 — the minhag of strewing fragrant grasses on Shavuot
- Shir HaShirim Rabbah 1:2 — flowers bloomed at Sinai at the moment of revelation
- Pirkei DeRabbi Eliezer, ch. 41 — the mountain burst into bloom at Matan Torah
- Shabbat 88b — angels crowned Israel with roses and myrtles at naaseh v'nishma
- Lloyd, S. P. (1982). Least squares quantization in PCM. *IEEE Transactions on Information Theory*, 28(2), 129–137.
