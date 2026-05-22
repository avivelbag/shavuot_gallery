# Burning to the Heart of Heaven — Sinai Contour Map

A canvas 2D piece rendering Sinai as a topographic contour map. Noise-generated
mountain terrain is divided into 14 elevation bands from deep olive-brown at the
base to bright white at the peak, evoking the moment described in Deuteronomy 4:11:
the mountain burning with fire to the heart of the sky.

The summit emits a continuous upward stream of semi-transparent warm-white smoke
particles, the only animated element — everything else is computed once and cached
to an offscreen canvas. The sky gradient runs from deep indigo (#1A0A3A) at the
top to smoky violet-orange (#7A3B2E) near the horizon.

A self-contained ~80-line simplex noise implementation (Gustavson/public-domain,
fixed permutation table) generates the mountain profile from three octaves sampled
along the x-axis. Contour bands are rendered using per-band canvas clipping, then
blit each frame behind the animated smoke particles.

**Theme:** Har Sinai / Deuteronomy 4:11 — the mountain burning to the heart of heaven  
**Technique:** canvas 2D simplex-noise terrain, topographic contour band rendering,
animated particle smoke column
