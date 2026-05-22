# A Consuming Fire — WebGL Plasma at Sinai

A WebGL fragment shader piece rendering the divine consuming fire (אֵשׁ אֹכֶלֶת)
described in Exodus 24:17 as pure mathematical plasma erupting from a mountain
silhouette.

A fullscreen fragment shader generates animated fire using six-octave fractional
Brownian motion (fBm) built from a hash-based value-noise function, with domain
warping — the noise input coordinates are themselves offset by a second fBm
layer — to produce the characteristic churning turbulence of flame. The result
is mapped through a fire color ramp from deep black through dark red, bright
orange, pale gold, to white at the hottest core. A triangle signed-distance
function anchors a mountain silhouette at the base; fire erupts from the peak
and rises, decaying with height. The sky above transitions from deep violet to
near-black. The Hebrew phrase **אֵשׁ אֹכֶלֶת** — *consuming fire* — appears as
an HTML overlay above the canvas.

**Theme:** Har Sinai / The Theophany — Exodus 24:17  
**Technique:** WebGL fragment shader / domain-warped fBm plasma, mountain SDF
