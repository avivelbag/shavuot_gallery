# Piece 87 — And All the People Saw the Thunder

**Theme:** Har Sinai / Matan Torah  
**Technique:** Double pendulum chaos / RK4 numerical integration

Seven double pendulums start from nearly identical initial conditions (θ₁=2.4 rad, θ₂=1.8 rad, with a 0.002 rad perturbation per pendulum) and are integrated forward using 4th-order Runge-Kutta at dt=0.02, running 8 steps per animation frame. Only the trace of the second (lower) bob is drawn — the arms themselves are invisible. Traces accumulate on an off-screen canvas, building a dense luminous tangle in seven colors drawn from the palette of Sinai. The simulation runs for 20 seconds before resetting with fresh perturbations, fading the old traces over 60 frames.

The piece visualizes Exodus 20:15 ("all the people *saw* the thunders") and the Mekhilta deRabbi Yishmael's interpretation that each Israelite received the divine voice individually, according to their capacity — a direct analogue to chaotic sensitive dependence on initial conditions.

## Files

- `index.html` — self-contained animation with embedded essay
- `essay.md` — source essay (~350 words)
- `thumbnail.svg` — 400×400 static approximation of double-pendulum traces in the seven palette colors
- `README.md` — this file

## Parameters

- Pendulum: L=1 (normalized), m=1, g=9.8
- Initial angles: θ₁=2.4 + k×0.002, θ₂=1.8, ω₁=ω₂=0 (k = 0..6)
- Integration: RK4, dt=0.02, 8 steps/frame
- Colors: #4B8FD4, #8B5CF6, #F0EFEA, #D4A017, #C8702A, #C2547A, #7EC8D4
- Cycle: 20 simulation-seconds, then 60-frame fade and reset
