# Let My Teaching Drop as Dew — WebGL Metaballs

A WebGL fragment shader piece in which glowing pearl-white droplets fall
silently from a deep indigo sky, accumulate at an implied ground, merge
into larger pools, and gradually trace the word **תּוֹרָה** through the
patient bias of their resting positions.

The metaball surface is computed in a fragment shader by evaluating
∑ rᵢ²/|p−cᵢ|² over all ball centers; pixels crossing the threshold 1.0 are
colored in a pearl-white to pale-gold gradient. Physics (gravity, drag,
ground settling, pairwise merge) runs in JavaScript; updated ball positions
are uploaded each frame as a `vec3[60]` uniform array.

The letter emergence is subtle: after a ball settles, it is assigned the
nearest unclaimed target point from a stroke-path encoding of "תּוֹרָה" and
drifts toward it at 0.0008 units per frame. The word becomes legible only
after many drops have accumulated — roughly thirty seconds in.

**Theme:** Matan Torah / Deuteronomy 32:2 — Torah as dew  
**Technique:** WebGL fragment shader / metaball SDF threshold, JS physics
