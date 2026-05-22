# Lightning Roots — Lichtenberg at Sinai

A canvas-based Dielectric Breakdown Model (DBM) simulation producing Lichtenberg
figures — branching electric discharge trees — rooted into the peak of Har Sinai.

The DBM maintains a 240×320 logical-pixel potential grid (rendered at 3× scale).
The top row is held at potential = 1 (source); the bottom at potential = 0 (sink).
A discharge tree seeds at the top-center and grows downward by iterating:

1. Build a frontier of all cells adjacent to the discharge but not yet discharged.
2. Weight each frontier cell by V(cell)^η (η ≈ 1.7).
3. Pick one cell by weighted random draw; mark it as discharged.
4. Run 6 Gauss-Seidel relaxation sweeps to partially re-solve the Laplace equation.

The tree grows 6 cells per animation frame until it reaches the mountain apex
(bottom 15% of the grid). It then holds for ~0.8 s, fades over ~3 s, and restarts
with a fresh random seed — seamlessly looping.

Palette: near-black background (#080810); discharge rendered electric white (#EEEEFF)
at tips fading through violet (#8855FF) toward roots; faint deep-blue glow (#1133AA)
spreads one pixel around each branch.

The mountain silhouette at the base is a filled triangle rendered directly into the
pixel grid, with the discharge tree rooting into its apex.

**Theme:** Har Sinai — Exodus 19:16–19, theophany and revelation  
**Technique:** Dielectric Breakdown Model (DBM) / Lichtenberg figure simulation, canvas 2D ImageData pixel painting
