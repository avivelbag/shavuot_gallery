# "First of All Your Yield" — Differential Growth / Bikkurim

**Theme:** Bikkurim / First Fruits and Harvest — the first-fruits offering on Shavuot (Deuteronomy 26:1–11)

**Technique:** differential growth / spring-repulsion curve simulation

## Description

A 700×700 canvas animation that runs a differential growth simulation on a closed polygon. The curve begins as a circle of 12 nodes centered at (350, 350) and grows by continuously inserting midpoint nodes wherever an edge exceeds MAX_EDGE (ramping from 18px to 8px as the curve matures). Two opposing forces govern each node: cohesion, which pulls it toward its two immediate neighbors via a spring (Laplacian smoothing), and repulsion, which pushes it away from all non-neighboring nodes within REPULSION_RADIUS (30px), with force proportional to 1/distance². A gentle boundary force keeps the curve within the canvas.

The result is the characteristic folded, fruit-like silhouette of differential growth — the same mathematics that gives lettuce leaves and figs their ruffled, abundant borders. The curve is filled in warm harvest gold (#C8A020) transitioning to ripe amber (#D4600A) as it grows, with a 1px cream stroke. When the node count reaches ~1100, the simulation fades to the field-green background (#0A2010) and restarts from a new seed-circle.

The Hebrew text at the bottom, "רֵאשִׁית כָּל בִּכּוּרֵי אַדְמָתְךָ" (Exodus 23:19, "the first of the first fruits of your land"), appears throughout the animation in gold at 70% opacity.

## Sources

- Deuteronomy 26:1–11 (the Viduy Bikkurim — first-fruits declaration)
- Deuteronomy 8:8 (the seven species)
- Mishnah Bikkurim 3:1–4 (the festive procession to Jerusalem)
- Exodus 23:19 (the commandment text displayed on canvas)
- Numbers 28:26 (Shavuot as Yom HaBikkurim)

## Files

- `index.html` — self-contained animated differential growth simulation (no external dependencies)
- `thumbnail.svg` — static SVG preview of a mature differential growth curve, 400×400
- `essay.md` — accompanying essay on the Bikkurim ceremony and Deuteronomy 26
