# 66 — The Stranger Who Chose In: Ruth on the Road from Moav

**Theme:** Bikkurim / harvest (Book of Ruth)
**Technique:** Voronoi stippling / Lloyd's algorithm

Three thousand stipple dots placed via thirty iterations of weighted Lloyd's algorithm (centroidal Voronoi tessellation). Each iteration assigns every canvas pixel to its nearest dot (via spatial-hash nearest-neighbor), computes the density-weighted centroid of each Voronoi cell, and moves the dot to that centroid. The density function defines a wheat field in the lower two-thirds (layered sine waves for row texture), a sparse sky above the horizon, and a near-zero-density silhouette for Ruth centered at x=220, bottom at y=520.

After convergence, dot radii are proportional to local density (r ∈ [0.8, 3.5] px). A gentle breath animation oscillates each radius ±15% with a per-dot random phase, completing a 4-second cycle; capped at 60 fps. Palette: harvest-gold (#C8900A) on aged parchment (#F5EDD8).

The essay focuses on Ruth as the stranger who chooses in — her declaration on the road from Moab as a private Sinai, the chesed arc through Boaz's field, and the way the stippling algorithm mirrors her presence: the field organizes itself around her silhouette through absence, not occupation.

**Scripture:** Ruth 1:16 (declaration on the road); Ruth 2:11 (Boaz's recognition of her choice).
