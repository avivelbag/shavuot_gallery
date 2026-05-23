# Piece 84 — The Crown That Never Ceases Turning

**Theme:** Keter Torah / perpetual Torah study
**Technique:** Rössler strange attractor / particle system

A real-time particle simulation of the Rössler strange attractor (Otto Rössler, 1976).
800 particles are released near (0, 0, 0.1) with perturbations of ±0.001 and warmed up
for 500 RK4 steps to settle onto the attractor before display begins. Each frame, every
particle advances 3 RK4 steps (dt = 0.01) and leaves a 60-position trail colored by
z-value: deep sapphire (#1A1A8A) at the base, royal blue (#4040CC) at mid-height, and
brilliant gold (#F0C040) at the high fold — the crown's rim. The projection rotates slowly
(0.001 rad/frame) around the vertical axis to reveal the three-dimensional crown structure.

## Rössler system

    dx/dt = -y - z
    dy/dt = x + 0.2·y
    dz/dt = 0.2 + z·(x - 5.7)

Classic parameters a = 0.2, b = 0.2, c = 5.7. The attractor occupies approximately
x ∈ [−10, 12], y ∈ [−12, 3], z ∈ [0, 30]. The high-z fold (z > 21) is the crownlike rim
that gilds in gold. No single orbit traces the crown; it emerges from the collective
envelope of all 800 trajectories — Keter from the ensemble.

## Hebrew watermark

The letter כ (kaf, for Keter) is rendered in large faint gold at center-right as a
watermark, reinforcing the Keter Torah theme.

## Files

- `index.html` — self-contained animation with embedded essay
- `essay.md` — source essay text (~370 words)
- `thumbnail.svg` — 400×400 SVG approximation of the Rössler crown spiral
- `README.md` — this file

## Shavuot connection

The piece is keyed to Pirkei Avot 5:22 (Ben Bag Bag: "Turn it and turn it again, for
everything is in it") and Avot 4:13 (the three crowns of the Mishnah, Keter Torah as the
crown open to all). The Rössler orbit literalizes perpetual return and perpetual discovery:
deterministic, never-repeating, the crown rim always gold.
