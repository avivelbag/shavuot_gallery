# Written by the Finger of God — Apollonian Stone

A canvas-based Apollonian circle packing that fills every gap between tangent circles
recursively, using Descartes' Circle Theorem to compute each Soddy circle.

Starting from three mutually tangent seed circles inside an enclosing outer circle
(with negative curvature), the algorithm runs BFS: for every tangent triple, it
computes the two Soddy curvatures via the quadratic formula and uses complex-number
center arithmetic to place each new circle. The gasket terminates when circles fall
below 2px radius or the total reaches ~2000 circles.

The animation reveals each generation of the gasket sequentially (one generation per
0.8 seconds), looping after all generations have appeared — the viewer watches
inscription fill the stone level by level.

A Hebrew aleph (א), the first letter of *Anochi* ("I am") and of the Ten
Commandments, is centered in the largest seed circle at low opacity, evoking the
primordial letter from which all revelation flows.

**Palette:** deep slate (#1A1A2E) background; circles filled with radial gradients
from deep amber (#8B5A00) at center to pale gold (#F5D87A) at the rim; smallest
circles rendered in pure white (#FFFFFF).

**Theme:** Exodus 31:18 — tablets of stone written by the finger of God; Torah
Shebichtav and Torah Sheba'al Peh given simultaneously at Sinai  
**Technique:** Apollonian gasket / recursive Descartes circle packing, canvas 2D
