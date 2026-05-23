# The Voice That Filled the World

**Shavuot theme: Har Sinai / the divine voice radiating to all the earth**

Shemot Rabbah 5:9 teaches that when God spoke at Sinai, the divine voice split into seventy languages and traveled simultaneously to every nation without weakening. This piece renders that voice as a deforming sphere: a WebGL triangle mesh whose 64×64 vertices are displaced each frame by a sum of 25 real spherical harmonics (Y_l^m for l = 0 to l = 4). The l = 0 (monopole) term is the voice that is uniform in all directions; the higher harmonics articulate its 70 faces, each direction hearing something different.

## Technique

WebGL triangle mesh (sphere ~64×64 segments). The vertex shader computes all 25 real spherical harmonics in closed form, using spherical coordinates (θ, φ) stored as vertex attributes. Coefficients c_lm(t) = sin(ω_lm · t + φ_lm) are animated with ω_lm = 0.3 + l · 0.2 and random initial phases, uploaded each frame as a `uniform float[25]`. Amplitude A = 0.35 (35% of sphere radius).

Color maps deformation magnitude to a three-stop palette: midnight blue (#0B1440) → electric violet (#6B22C8) → flame white (#FFF8E8). Blinn-Phong lighting from a single directional light gives the surface roundness. The sphere rotates at 0.15 rad/s around the y-axis.

## Sources

- Shemot Rabbah 5:9 — the voice split into 70 languages
- Exodus 19:18–19 — the whole mountain trembled
- Pirkei DeRabbi Eliezer 41 — the voice reached every corner without weakening
