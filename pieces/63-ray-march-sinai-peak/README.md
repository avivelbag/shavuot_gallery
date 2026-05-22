# The Mountain That Burned With Fire — Ray March Sinai

**Theme:** Har Sinai — Deuteronomy 4:11 / Exodus 19:18

**Technique:** ray marching / GLSL SDF — WebGL fragment shader

A full-viewport WebGL canvas ray-marches a 3D scene containing:

- A **rounded cone SDF** for the mountain (smooth-min blended with a ground plane), shaded in dark basalt gray-brown (#3A2E20).
- A **volumetric fire crown** accumulated during the march via domain-warped 4-octave fBm, using emission+absorption integration. Fire palette transitions from deep orange (#C04010) at the base through bright gold (#F0C020) to near-white (#FFF8E0) at the crown.
- An **exponential fog** haze (#0A0820) thickening toward the base; sky gradient from midnight blue (#050415) at top to smoky violet (#2A1840) near the mountain.
- A **Lichtenberg bolt** generated in JS every ~4 seconds (recursive branching random walk, 3 levels deep, ~60 points) uploaded as a `uniform vec2[64]` array and rendered as a glowing white polyline in the fragment shader.
- **Camera orbit**: one full rotation every 120 seconds at fixed elevation; fire drift at ~0.15 units/sec; capped at 60fps via requestAnimationFrame.

The essay cites Deuteronomy 4:11 and Exodus 19:18 verbatim in Hebrew (with nikud) and English translation as on-page scripture blocks. It discusses the Mechilta d'Rabbi Yishmael (Yitro 9) tradition of black fire on white fire, and the Talmudic question (Shabbat 88b) of why God chose a wilderness mountain ownerless by any nation.

**Piece ID:** 63-ray-march-sinai-peak
**Year:** 2026
