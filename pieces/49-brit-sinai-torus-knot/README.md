# An Everlasting Covenant — The Torus Knot of Sinai

A WebGL 3D piece rendering a (3,2) torus knot as a glowing tube mesh, with the
covenant formula **נַעֲשֶׂה וְנִשְׁמָע** (we will do and we will hear) mapped
onto the surface as a canvas texture.  The knot tumbles slowly on all three axes,
its gold emission ridge catching a fixed directional light against a deep
midnight background.

## Theme

**Matan Torah** — the Sinai covenant as a mathematical object.  Exodus 24:7–8
seals the revelation with blood and the declaration "we will do and we will
hear."  The Talmud (Shabbat 88a) describes God holding the mountain over the
people like a barrel; the question of coercion and consent is resolved
centuries later by the free re-acceptance recorded in Esther 9:27.  A torus
knot — closed, non-self-intersecting, topologically indestructible — is the
geometry of *brit olam*, an eternal covenant that cannot be loosened from
within itself.

## Technique

**WebGL 3D torus knot tube mesh** — no external libraries.

- Parametric (3,2) torus knot, sampled at 240 segments
- Tube cross-section: 10 sides, radius 0.07 units
- Parallel-transport (rotation-minimizing) frames to avoid twist at the join
- Typed arrays (Float32Array / Uint16Array) for all geometry
- Phong-ish fragment shader: ambient + directional diffuse + gold emission
  stripe based on world-space surface normal dot world-up
- Canvas-rendered Hebrew text uploaded as WebGL RGBA texture
- Rotation increments: 0.003 (X), 0.007 (Y), 0.001 (Z) radians per frame

## Sinai theme
Matan Torah / The Covenant Formula — Exodus 24:7–8; Shabbat 88a
