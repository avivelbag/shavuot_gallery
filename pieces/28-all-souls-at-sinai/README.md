# All Souls Were Present — Sinai DLA Gathering

**Shavuot theme: Matan Torah / The Covenant Across All Generations**

The midrash in Tanhuma Nitzavim (3) and the Talmud in Shevuot (39a) teach that every Jewish soul — across all generations — was present at the giving of the Torah on Sinai. The verse in Deuteronomy 29:14 is the textual basis: "also with those who are not here with us today." This is the foundation for why each generation is personally bound by the Sinai covenant, and why the Haggadah instructs each person to see themselves as having personally left Egypt.

## Artwork

A canvas 2D diffusion-limited aggregation (DLA) simulation. Particles are released from random positions at the edge of the visible area, perform a Brownian random walk (8-directional on-lattice), and freeze when they touch the growing aggregate anchored at the canvas centre.

### Seed

The aggregate is seeded with a triangle outline representing Mount Sinai — a small mountain silhouette rasterised via Bresenham line algorithm at canvas centre. DLA grows outward from the mountain's edges, producing the branching dendritic structure characteristic of DLA.

### Algorithm

- **Occupancy grid:** `Uint8Array` of size `cW × cH`; lookup is O(1)
- **Walker pool:** up to 180 concurrent walkers
- **Steps per frame:** adaptive — `max(15, floor(aggRadius × 0.4))` — increases as the aggregate grows so the wider spawn ring doesn't stall visible growth
- **Spawn radius:** `aggRadius × 1.25 + 20` (close to aggregate frontier)
- **Kill radius:** `spawnRadius × 2.8` (far enough to allow meandering back)
- **Collision:** 8-connected neighbourhood check; walker freezes at its current position when any neighbour is occupied

### Rendering

- **Background:** `#0D1B2A` (deep midnight blue), cleared each frame
- **Aggregate:** drawn lazily to an off-screen canvas using `createRadialGradient` (white centre → blue-white mid → transparent outer, radius 4 px) at each freeze event; composited with a single `drawImage` per frame
- **Walkers:** 1×1 px dots at `rgba(100,170,255,0.32)` — barely visible, like souls crossing the darkness

## Palette

| Element             | Colour                          |
|---------------------|---------------------------------|
| Background          | `#0D1B2A` (midnight blue)       |
| Aggregate core      | `rgba(255,255,255,0.95)` white  |
| Aggregate mid-glow  | `rgba(80,150,255,0.28)` blue    |
| Live walkers        | `rgba(100,170,255,0.32)` faint  |

## Technique

- **Diffusion-limited aggregation (DLA)** — not previously used in this gallery
- **On-lattice 8-directional Brownian motion** with adaptive steps per frame
- **Bresenham rasterisation** for mountain seed
- **Off-screen canvas compositing** for efficient aggregate rendering
- **No external libraries** — fully self-contained single HTML file
