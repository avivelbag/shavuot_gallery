# 67 — Na'aseh V'Nishma: The Magnetic Pendulum

**Theme:** Matan Torah  
**Technique:** magnetic pendulum fractal / basin of attraction

A canvas 2D simulation of the magnetic pendulum system: three magnets placed at the vertices
of an equilateral triangle (radius 1.0, center at origin), with a damped pendulum bob simulated
via Euler integration. For each pixel in a 600×600 grid spanning (−3, 3) × (−3, 3), the
simulation tracks the bob until it settles near one magnet (|v| < 0.001 and nearest magnet
distance < 0.2) or reaches 3000 steps. Pixels are colored by attractor (gold / blue / cream)
with brightness proportional to convergence speed — fast settlers are bright, slow settlers
(near fractal boundaries) are dark.

The simulation runs in browser-native JavaScript, processing ~2000 pixels per animation frame.
A thin gold progress line advances down the canvas as rows complete. Once rendering finishes,
"נַעֲשֶׂה וְנִשְׁמָע" appears in cream lettering at top center.

**Physics:**
- Euler integration, dt = 0.02
- Gravity restoring force: F = −0.5 · (x, y)
- Magnet attraction: F = k / (r² + ε) where k = 1.0, ε = 0.01 (singularity guard)
- Damping: F = −0.2 · (vx, vy)
- Stopping: |v| < 0.001 AND nearest magnet distance < 0.2; max 3000 steps

**Magnet colors:**
- Gold (#D4A020) — top, 12 o'clock, position (0, 1.0)
- Deep blue (#1A3080) — bottom-left, 8 o'clock, position (−0.866, −0.5)
- Warm cream (#F0E8D0) — bottom-right, 4 o'clock, position (0.866, −0.5)

**Scripture and commentary:**
- Exodus 24:7 — *naaseh v'nishma*, "we will do and we will hear"
- Talmud Bavli, Shabbat 88a — the 600,000 angels and the two crowns
- Maharal of Prague, Derush al HaTorah — commitment must precede comprehension
- Exodus 19:10–15 — shloshet yemei hagbalah, the three preparatory days before Sinai
