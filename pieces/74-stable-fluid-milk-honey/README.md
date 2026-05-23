# Piece 74 — A Land Flowing

**Theme:** Milk and Honey / The Promised Land
**Technique:** WebGL stable fluids / Navier-Stokes pressure projection

A real-time GPU fluid simulation of the biblical image *eretz zavat chalav u'dvash* — a land
flowing with milk and honey (Exodus 3:8). Two fluid streams, warm cream from the left and amber
honey from the right, are injected along a Lissajous figure-eight path and kept in perpetual
swirling motion. The fluids interpenetrate without fully merging, enacting the complementary
relationship between the Written and Oral Torah.

The simulation implements Jos Stam's 1999 stable fluids algorithm on a 256×256 grid using
WebGL1 with floating-point textures. Each frame: semi-Lagrangian velocity advection,
implicit viscosity diffusion (10 Jacobi iterations, ν=0.00001), velocity divergence,
pressure projection (20 Jacobi iterations, Helmholtz-Hodge decomposition), gradient
subtraction, and dye advection.

## Files

- `index.html` — self-contained WebGL piece with embedded essay
- `essay.md` — source essay text (~400 words)
- `thumbnail.svg` — 400×400 static rendering of the swirling fluid
- `gen_thumbnail.py` — Python script to regenerate thumbnail as PNG (requires NumPy and Pillow)
- `README.md` — this file

## Parameters

- Simulation grid: 256×256 texels, scaled to full viewport
- Velocity strength: 80 texels/second
- Velocity impulse radius: 8 texels
- Dye injection strength: 0.4 per frame
- Dye injection radius: 16 texels
- Viscosity: ν = 0.00001
- Diffusion iterations: 10 Jacobi steps
- Pressure iterations: 20 Jacobi steps
- Velocity dissipation: 0.9998 per frame
- Dye dissipation: 0.999 per frame
- Injection path: Lissajous 1:2 (figure-eight), alternating direction every 3 seconds

## Color palette

- Background: #0A0804 (near-black warm)
- Cream fluid: #FFF5DC / #F0E8C8
- Mid-amber blend: #E8B030
- Honey fluid: #D4820A / #C86A00

## Browser requirements

WebGL 1.0 with `OES_texture_float` extension is required. Optional:
`OES_texture_float_linear` for smoother advection. Runs at 60 fps on any GPU from 2015+.
