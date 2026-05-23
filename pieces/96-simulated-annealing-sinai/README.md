# The Fire That Does Not Consume

**Shavuot theme: Matan Torah / Har Sinai**

Deuteronomy 4:11–12 describes Sinai as "burning with fire unto the heart of heaven." The Midrash (Shemot Rabbah 5:9) adds that the fire was *consuming but not consumed* — inverting ordinary physics and signalling the divine presence. This piece enacts that inversion through simulated annealing: the algorithm that uses heat to find order.

## Technique

Canvas 2D, no libraries. Full-viewport animation using `requestAnimationFrame`.

**Simulated annealing** — N=2000 particles begin in random positions at maximum temperature (T=500). Each frame, T is multiplied by 0.9995, and M=50 random perturbations are attempted via the Metropolis-Hastings criterion: accept moves that lower energy; accept energy-raising moves with probability exp(−ΔE/T). Energy is the local contribution of each particle: the sum of distances to its K=5 nearest neighbours (a proxy for disorder).

**Spatial hash grid** — a 60-pixel grid divides the canvas into cells; each particle's neighbours are found by looking only in the surrounding 9 cells, making the O(N·K) energy calculation tractable at 60 fps.

**Hexagonal close-packing** — at startup a hexagonal lattice is generated with spacing d≈√(W·H/N)≈32 px and each particle is greedily assigned to its nearest unassigned lattice point. As T falls, a spring force (stiffness ∝ (T_max−T)/T_max) draws each particle toward its assigned lattice point; the crystal lattice visually locks in as the temperature approaches zero.

**Colour** — each particle is coloured by its normalised local energy: deep indigo (#1C1864) for low energy, gold (#D4A017) at the midpoint, fire red (#FF4500) for high energy. The background transitions from fiery deep red (#2A0A00) at T_max to midnight blue (#050A1A) at T≈0. The temperature readout changes colour in step with the particles.

**Loop** — when T < 1 the crystal is held for 5 seconds, then the canvas fades to black, particles re-scatter, and T resets to T_max. The lattice assignment is kept fixed so every annealing run converges to the same crystal.

## Palette

| Element | Colour |
|---------|--------|
| Background (hot) | `#2A0A00` |
| Background (mid) | `#1A0F00` |
| Background (cool) | `#050A1A` |
| Particle (high energy) | `#FF4500` |
| Particle (mid energy) | `#D4A017` |
| Particle (low energy) | `#1C1864` |
