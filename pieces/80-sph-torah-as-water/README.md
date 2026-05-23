# Descend as the Rain, Distill as the Dew

**Shavuot theme: Crown of Torah / naaseh v'nishma**

Moses' final song (Deuteronomy 32:2) compares his teaching to three kinds of water — rain, dew, and mist. The Talmud (Ta'anit 7a) maps this to humility: Torah, like water, flows only downward, into the lowest vessel. This piece simulates that physics directly: 400 particles of fluid falling under gravity, compressing and pooling at the floor, then sloshing back and forth — water finding its lowest point.

## Technique

Pure canvas 2D, no libraries. SPH (Smoothed Particle Hydrodynamics) — Müller et al. 2003 kernels.

**Kernels:**
- Density: poly6 kernel `W = (315 / (64π h⁹)) * (h² − r²)³` for r < h
- Pressure gradient: spiky kernel `∇W = −(45 / (π h⁶)) * (h − r)² / r`
- Viscosity: laplacian kernel `∇²W = (45 / (π h⁶)) * (h − r)`

**Parameters:**
| Constant | Value |
|----------|-------|
| N (particles) | 400 |
| h (smoothing radius) | 30 px |
| ρ₀ (rest density) | 1000 |
| k (gas constant) | 2000 |
| μ (viscosity) | 250 |
| g (gravity) | 600 px/s² |
| Boundary damping | 0.3 (velocity reversal) |
| dt | 1/60 s |

**Spatial hashing:** Grid cells of size h. Each frame, particles are inserted into a hash table by cell; neighbor lookup checks the 9 surrounding cells. Reduces O(N²) to O(N · avg_neighbors) ≈ O(50k) per frame.

**Per-frame SPH update:**
1. Build spatial hash
2. Pass 1: compute density (poly6 sum) and pressure `p = k(ρ − ρ₀)` for each particle
3. Pass 2: compute pressure force (spiky gradient) and viscosity force (laplacian) from neighbors
4. Add gravity force `fy += g * ρ`
5. Semi-implicit Euler integration: update velocity then position
6. Enforce canvas boundaries (reflect with damping 0.3)

**Surface rendering:** A scalar field is computed on an 80×60 grid by summing Gaussian contributions `exp(−r²/σ²)` from nearby particles. Marching squares contours this field at threshold 0.5. The interior is filled with a semi-transparent indigo gradient; the contour itself is drawn in silver-white (#D8E8F0).

**Determinism:** A fixed-seed LCG PRNG initialises particle positions and perturbations, so the loop is visually identical across sessions.

## Palette

| Element | Colour |
|---------|--------|
| Background | `#0A0C14` |
| Particles | `rgba(100, 130, 220, 0.4)` (deep indigo) |
| Fluid interior | `rgba(60, 80, 180, 0.18)` |
| Surface contour | `#D8E8F0` (silver-white) |
