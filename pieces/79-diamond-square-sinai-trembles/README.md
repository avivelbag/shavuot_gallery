# The Whole Mountain Quaked — וַיֶּחֱרַד כָּל-הָהָר מְאֹד

**Technique:** Diamond-square fractal terrain / isometric heightmap rendering

**Theme:** Har Sinai / thunder and fire — Exodus 19:18

A 65×65 diamond-square heightmap rendered isometrically and animated by continuously morphing between two generated terrains (linear interpolation over 120 frames at 60fps). The mountain never rests: it restructures its ridges and valleys on a two-second cycle, enacting the verse's description of the entire mountain quaking at the moment of revelation.

The diamond-square algorithm produces fractal terrain with a Hurst exponent of approximately 0.65 — dramatic peaks and valleys but not pure noise. Two heightmaps are maintained; when the current morphing cycle completes, the next heightmap becomes current and a new one is generated, creating seamless continuous motion.

Rendered as an isometric projection with per-cell top/left/right face shading, a height-based color palette ranging from deep purple-grey base rock to near-white summit cloud, a smoke particle system above the summit cells, and a red-orange fire glow strip along the mountain base.

**Shavuot connection:** Exodus 19:18 is the only place in the Torah where the verb ḥarad (חרד) — ordinarily reserved for the trembling of living creatures — describes inanimate matter. The mountain does what flesh does when it encounters the unbearable. The Mechilta de-Rabbi Ishmael interprets this as the entire created order responding to the weight of revelation. The Talmud (Shabbat 88a) adds that the Israelites themselves recoiled 12 mil backward at each commandment and were escorted back by angels. The fractal terrain's endless quaking enacts the permanent seismic condition of a world through which Torah has passed.
