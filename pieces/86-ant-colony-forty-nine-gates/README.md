# Forty-Nine Gates of Understanding

**Piece 86** — Shavuot Gallery 2026

## Theme

Sefirat HaOmer / 49 gates of understanding — Rosh Hashanah 21b; Nedarim 38a.

The Talmud teaches that fifty gates of Binah (Understanding) were created in the world, and all
were given to Moses except the fiftieth. Moses stood at forty-nine — the maximum a human being can
reach by effort. The fiftieth gate opened only at Matan Torah, by divine gift.

The forty-nine days of the Omer are not merely a countdown. Each day is an ascent through one
of the forty-nine combinations of the seven lower sefirot (7×7 = 49), as taught in the Zohar
(Parashat Emor) and the Sefirat HaOmer practice: a structured walk through the complete architecture
of the divine attributes.

## Technique

**Ant-colony stigmergy (ACO)** — pheromone-based path reinforcement on a 120×120 grid.

- 200 ants per generation perform a random walk biased by pheromone (β=2) and distance to the
  destination (α=1).
- Successful ants deposit pheromone inversely proportional to path length; all pheromone evaporates
  by factor 0.85 after each generation.
- 49 generations run at ~1.5 s each; the network of explored paths converges progressively.
- After generation 49, a 1-second pause shows the faint accumulated network.
- Generation 50 (Shavuot): the single highest-pheromone path blazes gold; all other trails dim.

Color: background #090818 (deep indigo); pheromone interpolates from #3020A0 (dim violet, low) to
#F0C040 (bright gold, high); source node green glow; destination (Sinai) white star glow.

Generation counter in Hebrew numerals (א–מט, then נ), upper left.

## Files

- `index.html` — full-viewport canvas animation with essay embedded inline
- `essay.md` — essay source (~420 words; Rosh Hashanah 21b, Nedarim 38a, Zohar Parashat Emor)
- `thumbnail.svg` — 400×400 faint violet path network with a central gold path and two glowing nodes
- `README.md` — this file

## Sources

- Rosh Hashanah 21b — fifty gates of understanding; all given to Moses except one
- Nedarim 38a — Moses surpassed all prophets in understanding
- Psalm 8:6 — "You have made him slightly less than divine"
- Zohar, Parashat Emor — the 7×7 sefirot structure of Sefirat HaOmer
- Dorigo, M. (1992). *Optimization, Learning and Natural Algorithms*. (original ACO formulation)
