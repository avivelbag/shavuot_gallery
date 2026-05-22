# Thunder at Sinai

**Shavuot theme: Har Sinai / Matan Torah**

At the revelation on Mount Sinai, the Torah describes thunder, lightning, dense cloud, and the sound of the shofar growing ever louder — a theophany so overwhelming that the Israelites trembled and stood at a distance. This piece attempts to hold that moment: the mountain that could not be touched, wreathed in fire and smoke, pierced by bolts from above.

## Technique

Pure canvas 2D, no libraries. Each frame is rendered with `requestAnimationFrame` targeting ≤60 fps.

**Lightning** — recursive midpoint-displacement. A trunk line from sky to peak is subdivided 3–4 levels deep; at each level the midpoint is offset randomly perpendicular to the segment. Branches fork off at midpoints with decreasing probability at deeper levels. Every bolt is drawn with a wide, low-opacity glow pass followed by a sharp bright core. Bolts are regenerated periodically (every 8–12 frames) to create a continuous flickering storm.

**Fire and smoke** — 40 particles are tracked in a pool. Fire particles spawn at the peak with an upward velocity vector plus slight random spread; they fade from `#ff6a00` through `#ffd700` to transparent as their lifetime decreases. Smoke particles spawn slightly above the fire zone, drift slowly upward with horizontal jitter, and render as soft translucent grey circles.

**Mountain** — a static polygon path drawn once and cached; it masks the lower portion of the scene so lightning appears to strike from above.

## Palette

| Element | Colour |
|---------|--------|
| Sky | `#0a0a12` (near-black with a blue cast) |
| Lightning core | `#d0e8ff` (white-blue) |
| Lightning glow | `rgba(160, 200, 255, 0.25)` |
| Fire base | `#ff6a00` (deep orange) |
| Fire tip | `#ffd700` (gold) |
| Smoke | `rgba(160, 140, 120, 0.3)` |
| Mountain | `#1a1a2e` |
