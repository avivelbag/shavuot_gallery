# The Fiftieth Gate — IFS Harvest Field

Three fractal plants — a wheat stalk, a barley frond, and a spreading vine leaf —
grown simultaneously by the chaos game on an HTML5 canvas. Each plant is defined
by a set of 4–6 weighted affine transforms (the Iterated Function System); the
algorithm applies a randomly-selected transform to the current point on every
iteration, and plots the resulting point. After one million iterations, the orbit
traces the fractal attractor without any explicit recursion.

The canvas is divided into three vertical columns, one per plant. Each animation
frame adds 5 000 points per plant (15 000 total); the scene fills from black to
a dense harvest field in roughly 2–3 seconds, then holds while a gentle ±2%
breathing scale (4-second cycle) animates the canvas via CSS `transform: scale()`.

Color is y-position-dependent: roots are warm earth (#8B5E3C), mid-stalk is deep
field green (#3A6B2A), upper leaves are ripe barley (#C8A035) to harvest gold
(#E8C84A), and tips reach off-white seed (#F5EDD8). Small random per-point jitter
adds shading depth.

The Hebrew letter *nun* (נ = 50) appears above the central barley plant, connecting
to both the fifty-day Omer count and the fiftieth gate of Binah.

**Theme:** Chag HaKatzir / Harvest — Exodus 23:16; Sefirat HaOmer — Leviticus 23:15–16  
**Technique:** Iterated Function Systems (IFS) via the chaos game, canvas 2D pixel painting
