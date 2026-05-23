# Piece 75 — Fire That Does Not Consume

**Theme:** Har Sinai  
**Technique:** Barkley excitable medium / reaction-diffusion spiral waves

A Barkley model (1991) simulation that generates self-organizing spiral waves — the mathematical equivalent of Belousov-Zhabotinsky (BZ) chemical waves — rendered in a Sinai fire palette. The piece connects Deuteronomy 4:11–12 (the mountain burning with fire at the revelation) with the paradox of Exodus 3:2 (the burning bush that is not consumed).

The BZ spiral wave is the chemical analog of "fire that does not consume": an excitation propagates through the medium, leaves recovery rather than destruction, and the medium is perpetually ready for the next wave. The Barkley model captures this with two variables: *u* (activator/flame) and *v* (recovery/aftermath), updated via forward Euler on a 200×200 grid.

Hebrew text overlay: וְהַהָר בֹּעֵר בָּאֵשׁ (Deuteronomy 4:11, "and the mountain was burning with fire").

## Files

- `index.html` — self-contained piece with embedded Barkley simulation and essay
- `essay.md` — source essay text (~380 words)
- `thumbnail.svg` — 400×400 SVG showing spiral BZ-like arcs in fire palette
- `README.md` — this file

## Parameters

Barkley model: a=0.75, b=0.06, ε=0.02, D=1.0, Δt=0.1. Grid: 200×200, double-buffered Float32Arrays. 3 simulation steps per animation frame. Seeded with 4 asymmetric 3×3 perturbations to spawn persistent spiral arms.

Color palette: u=0 → #120805 (charcoal); u=0.3 → #5C1800 (ember); u=0.6 → #E83A00 (orange); u=0.85 → #FF8C00 (flame); u=1.0 → #FFE8B0 (flame-tip). Recovering cells (u&lt;0.1, v&gt;0.3) tinted with #2A3050 (cool blue-gray).
