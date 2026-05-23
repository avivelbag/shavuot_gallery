# A Land Flowing — Lattice Boltzmann Milk and Honey

**Shavuot theme: Bikkurim / milk and honey / the Promised Land**

The Torah's most repeated geographical description — "a land flowing with milk and honey" — appears approximately twenty-one times, first as a promise at the Burning Bush (Exodus 3:8) and last as fulfillment in the Bikkurim declaration (Deuteronomy 26:9). The Bikkurim offering, bringing first fruits to the Temple on Shavuot, was the farmer's embodied testimony that the promise had been kept.

## Artwork

A full-viewport D2Q9 Lattice Boltzmann Method (LBM) fluid simulation on a 300×150 grid. Two dye streams — cream-white (#FFF8E7) from the top half and amber-gold (#D4890A) from the bottom half — are injected at the left inlet and flow rightward around two obstacles shaped as the Hebrew letter ה (the final letter of אֶרֶץ, "land"), placed at 1/3 and 2/3 of the grid width.

### Simulation parameters

| Parameter | Value |
|-----------|-------|
| Grid | 300 × 150 (D2Q9) |
| Relaxation time τ | 0.6 |
| Viscosity ν | (τ−0.5)/3 = 1/30 |
| Inlet velocity u_x | 0.10 lattice units |
| Reynolds number Re | ≈ 108 (obstacle width 36 cells) |
| Steps per frame | 5 |

### D2Q9 velocity set

```
e = [(0,0),(1,0),(0,1),(-1,0),(0,-1),(1,1),(-1,1),(-1,-1),(1,-1)]
w = [4/9, 1/9, 1/9, 1/9, 1/9, 1/36, 1/36, 1/36, 1/36]
```

Bounce-back boundary conditions at solid cells; left-inlet enforces constant equilibrium distribution at ρ=1, u=(0.10,0); right outlet extrapolates.

### ה letterform

Each ה is 36 columns wide × 50 rows tall with 4-cell strokes. The top bar spans the full width; the right bar descends the full height; the left leg begins at row 24 of the bounding box, leaving a 24-row gap that distinguishes ה from ח.

### Dye advection

A separate passive scalar field is advected via semi-Lagrangian back-tracing using the velocity field computed during LBM collision, with bilinear interpolation.

### Rendering

Per-pixel color lerp between cream (#FFF8E7) and amber (#D4890A) based on dye concentration; solid cells rendered as dark warm stone (#1A1208); subtle vignette overlay; Hebrew inscription "אֶרֶץ זָבַת חָלָב וּדְבַשׁ" at bottom-right.

### Palette

| Element | Colour |
|---------|--------|
| Cream stream | `#FFF8E7` |
| Amber stream | `#D4890A` |
| Solid obstacles | `#1A1208` |
| Background | `#0D0802` |

## Technique

- **D2Q9 Lattice Boltzmann Method** — not previously used in this gallery
- **Semi-Lagrangian dye advection** — passive scalar transported by the velocity field
- **Bounce-back boundary conditions** — for solid ה obstacles and top/bottom walls
- **Kármán vortex shedding** — Re ≈ 108 places simulation in the vortex-street regime
- **No external libraries** — fully self-contained single HTML file
