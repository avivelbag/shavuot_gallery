# Piece 77 — Until the Dawn Rises

**Theme:** Tikkun Leil Shavuot
**Technique:** Thomas attractor / RK4 integration / orbit trail

A real-time animation of the Thomas attractor (René Thomas, 1999), integrated with
fourth-order Runge-Kutta (RK4) at dt = 0.05. The trajectory is rendered as a fading
orbit trail: the newest points glow pale gold (the color of dawn) and cool through amber
and indigo into near-black as they age out of the buffer. The attractor slowly rotates in
depth at 0.002 radians per frame, so its three-dimensional structure unfolds continuously.
The piece enacts the arc of Tikkun Leil Shavuot — the all-night Torah study vigil on the
eve of Shavuot — as a mathematical object that moves forever without settling.

## Attractor

The Thomas attractor is governed by three cyclically symmetric equations:

    dx/dt = sin(y) − b·x
    dy/dt = sin(z) − b·y
    dz/dt = sin(x) − b·z

At b = 0.208 the system is chaotic. The Lyapunov exponents are positive; the trajectory
never repeats. Initial condition: (x₀, y₀, z₀) = (0.1, 0.0, 0.0). The first 5000 steps
are discarded to eliminate the transient before the display buffer begins.

## Integration

RK4 with step dt = 0.05. Each animation frame advances the state by 200 steps, adding
200 new points to the circular buffer.

## Trail buffer

A circular buffer of 6000 3D points (three Float32Arrays). The 3D coordinates are stored
rather than canvas-space coordinates, so the projection remains valid across window resizes.
Each frame, the buffer is drawn from oldest to newest (so new points composite on top).
Age is computed from buffer position: age = (count − 1 − j) / (count − 1), where j = 0
is the oldest point.

## Projection

The (x, z) plane rotates by a cumulative angle that advances 0.002 rad/frame. y maps
directly to the vertical axis. Scale = min(W, H) / 12; the attractor lives in roughly
[−5, 5]³, so this gives comfortable margins on any aspect ratio.

## Color palette

- Newest (age 0): pale gold #F5D080, alpha 0.9
- Mid-age: warm amber #C87020 → deep indigo #1A1060
- Oldest (age 1): near-black #08060F, alpha 0.02

The blue channel uses a quadratic formula to peak the warm amber transition in the middle
of the age range, producing a luminous golden trail that cools into darkness.

## Background

Near-black #060408. The canvas is cleared and fully redrawn each frame from the circular
buffer, so no compositing tricks are needed. At 6000 × 1.5 px arc() calls per frame the
animation runs at 60 fps on modern hardware.

## Files

- `index.html` — self-contained animation with embedded essay
- `essay.md` — source essay text (~370 words)
- `thumbnail.svg` — 400×400 hand-crafted SVG of the attractor's double-lobe shape
- `README.md` — this file
