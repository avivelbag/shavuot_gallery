# The Standing Grain — Verlet Wheat Harvest

A 2D Verlet spring-mass simulation of a wheat field swaying in a Perlin-noise wind,
depicting the moment of Chag HaKatzir — the biblical Festival of the Harvest (Exodus 23:16).

Each stalk is a chain of 7–9 particles linked by distance and angular constraints.
The base particle is pinned to the ground. Per frame: gravity (0, +0.4) acts on all
free particles; wind force is sampled from a scrolling 2D Perlin noise field; distance
constraints are relaxed via Jakobsen iteration (3 passes); angular constraints between
consecutive segments restore each stalk toward vertical with stiffness 0.3.

120–180 stalks are distributed across the bottom third of the canvas using a jitter
grid with randomized offsets to avoid clumping. Background stalks are drawn smaller
and slightly desaturated to create depth.

Every 8–12 seconds a gust sweeps through (noise multiplier ×2.5 for 2 seconds),
causing the field to lean and recover in a ripple wave from left to right.

**Theme:** Chag HaKatzir / The Wheat Harvest — Exodus 23:16; Sefirat HaOmer (Leviticus 23:15–16); Book of Ruth

**Technique:** canvas 2D — Verlet spring-mass chain, Jakobsen constraint relaxation,
inline Perlin noise, procedural wheat stalk rendering
