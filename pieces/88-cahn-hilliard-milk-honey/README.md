# Piece 88 — Flowing Together: The Separation That Makes Sweetness

**Theme:** Milk and Honey / Promised Land  
**Technique:** Cahn–Hilliard equation (spinodal decomposition), canvas 2D

A Cahn–Hilliard simulation of spinodal decomposition rendering the "land flowing with milk and honey" (Exodus 3:17, and more than twenty other occurrences in the Torah) as the thermodynamically inevitable separation of an immiscible binary mixture. φ = −1 maps to creamy milk (#FFF5E6); φ = +1 maps to amber honey (#C8860A). The viewer watches disordered mixture spontaneously resolve into growing, coarsening domains — the promised land fulfilling itself.

## Files

- `index.html` — self-contained piece with embedded essay and Cahn–Hilliard simulation
- `essay.md` — source essay text (~350 words)
- `thumbnail.svg` — 400×400 hand-drawn approximation of late-stage coarsening output
- `README.md` — this file

## Simulation parameters

- Grid: 300×300 Float32Array φ, periodic boundaries
- ε² = 6.25 (interface width parameter, ε = 2.5)
- dt = 0.25 (explicit time step)
- 8 sub-steps per animation frame
- Initial condition: uniform random noise in [−0.1, 0.1]
- Color ramp: φ = −1 → #FFF5E6 (milk), φ = +1 → #C8860A (honey), linear interpolation
- After ~2000 frames (~33 seconds at 60 fps), crossfade to fresh noise over 2 seconds, then repeat
