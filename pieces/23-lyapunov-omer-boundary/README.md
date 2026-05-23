# Between Slavery and Sinai

**Piece 23 — Shavuot Gallery**

The Lyapunov fractal is a 2D parameter-space image of the two-parameter logistic map. Each pixel (a, b) represents a regime of the dynamical system x → r·x(1−x) driven by alternating growth rates a and b according to the sequence AABAB. The pixel's color encodes the Lyapunov exponent λ — the measure of whether the system amplifies or damps small perturbations. Deep blue indicates stability (λ ≪ 0); fire-red indicates chaos (λ ≫ 0); white marks the fractal boundary (λ ≈ 0) of infinite complexity.

## Connection to Shavuot

Leviticus 23:15–16 commands counting forty-nine days from Pesach to Shavuot — from the chaos of slavery in Egypt (*Mitzrayim*, the narrow straits) to the order of Torah at Sinai. The Zohar (Parashat Emor) describes each day as ascending one rung of a forty-nine-rung ladder: from the forty-nine levels of impurity absorbed in Egypt to the forty-nine gates of *binah* that open at Sinai.

The Lyapunov exponent measures the same axis — chaos to order — with mathematical precision. The fractal boundary between the blue and red regions is not a smooth line but an infinitely detailed edge, which is exactly where the Omer situates the Jewish people: between slavery and revelation, traversing a boundary of infinite complexity over forty-nine days.

## Technical approach

- **Algorithm:** Markus-Lyapunov fractal with sequence "AABAB". For each pixel (a, b), iterate the logistic map x → r·x(1−x) using r alternating by sequence; discard 50 warmup steps; accumulate λ = (1/N) Σ log|r_n(1 − 2x_n)| for N=200 steps.
- **Rendering:** Off-screen Web Worker computes all 640,000 pixel λ values (Float32Array), transfers the buffer to the main thread for colorization — keeps the page responsive during the 2–4 second computation.
- **Color mapping:** 3-stop piecewise linear interpolation in RGB; blue-indigo for λ < 0 (scaled by |λ|/2), gold-red for λ > 0 (scaled by λ/2), white for |λ| < 0.02 (the boundary).
- **Animation:** Quadratic Bezier path from P0=(3.9, 2.7) [chaotic] through P1=(3.5, 3.5) [boundary] to P2=(2.8, 3.8) [stable], evaluated at t = (performance.now() % 20000) / 20000 for a 20-second loop. A growing golden trail marks the path traversed so far.

## Files

| File | Purpose |
|------|---------|
| `index.html` | Animated Lyapunov fractal with embedded essay |
| `essay.md` | Standalone essay (~380 words) |
| `thumbnail.svg` | 400×400 stylized thumbnail with fractal boundary and Hebrew text |
| `README.md` | This file |
