# 66 — Where All Paths Converge: The Sinai Billiard

**Theme:** Har Sinai  
**Technique:** chaotic billiard / ergodic trajectory

A canvas 2D animation of the Sinai billiard: a square room (side 2.0, centered at origin)
with a circular obstacle of radius 0.4 at its center, a canonical system in mathematical
chaos theory named for Yakov Sinai's 1970 ergodicity proof.

Ten particles are launched from a tight cluster near (−0.6, −0.6) with identical 45°
initial velocity. Each particle is offset by a small ε in y₀ (from −0.018 to +0.036),
making their starting positions nearly indistinguishable. The billiard computes exact
reflections: wall collisions invert the perpendicular velocity component; circle collisions
reflect the velocity about the outward normal using v′ = v − 2(v·n)n. The simulation
advances 500 collision events per particle per animation frame at 60 fps.

Each particle's trail is drawn at alpha 0.6 in its own color (deep gold, crimson, sapphire,
warm white, copper, violet, sky, olive, rose, mint). A semi-transparent background overlay
(rgba 10,10,20 at 0.04 alpha) fades old segments each frame, keeping the canvas alive
as new trails accumulate.

After a few hundred frames the trails fill the room in a dense, divergent tangle — the
visual signature of ergodicity and sensitive dependence on initial conditions.

**Mathematical note:** The Sinai billiard is ergodic (every trajectory eventually fills all
available space with uniform density) and hyperbolic (trajectories from nearby starting
points diverge exponentially fast). The circular obstacle is the key: it acts as a focusing
lens that amplifies small initial differences at every bounce.

**Scripture and Midrash:** Exodus 19:2 (encampment at Sinai in the singular *vayichan*);
Mechilta d'Rabbi Yishmael, Yitro 1 (Torah given in ownerless wilderness, *hefker*);
Shemot Rabbah 5:9 (the voice divided into seventy languages; each person heard according
to their strength).
