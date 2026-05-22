# Given in the Wilderness — Curl Noise Sand

A canvas-2D curl noise flow field rendered as densely packed streamlines evoking
wind-blown desert sand dunes. Theme: the Torah given in the wilderness because
the desert is *hefker* — ownerless — and therefore belongs to everyone.
Source: *Bamidbar Rabbah* 1:7.

## Technique

A 3D gradient (Perlin) noise function `N(x, y, t)` serves as a scalar potential.
Its curl is approximated by finite differences:

```
curl_x =  (N(x, y+ε, t) − N(x, y−ε, t)) / (2ε)
curl_y = −(N(x+ε, y, t) − N(x−ε, y, t)) / (2ε)
```

The resulting divergence-free vector field naturally produces elongated ridge-and-trough
patterns. Each seed point is integrated for 150 steps of length 2.5 px along the
normalised curl vector to produce a streamline.

**Seed grid:** ~1,750 points (50 cols × 35 rows) with slight random jitter.
A rolling batch of 60 streamlines is redrawn per frame so all seeds cycle in
~0.5 s at 60 fps.

**Animation:** `timeOffset` advances by 0.0003 per frame and is passed as the `z`
coordinate of the 3D noise lookup, treating the 2D field as a slowly scrolling
slice through a 3D volume. The dune pattern drifts and breathes without teleporting.

**Color:** streamlines are coloured by y-position — pale sand (#F5E6C8) near the
top, tawny amber (#C8843A) through the mid-dune field, deep ochre (#7A4A18)
near the bottom, with faint violet shadow (#3A2855) in the deepest troughs.
Background uses a matching warm gradient.

**Overlay:** a 1 px warm-grey (#A09070) horizon line at 65% canvas height divides
sky from dune field. The Hebrew word **מִדְבָּר** (midbar, wilderness) appears
above the horizon in a light, weight-200 sans-serif at low opacity.

No external dependencies; animation runs via `requestAnimationFrame`.

**Theme:** Matan Torah / Given in the Wilderness — Bamidbar Rabbah 1:7; Avot 6:6  
**Technique:** canvas 2D — curl noise divergence-free flow field, streamline integration, rolling batch animation
