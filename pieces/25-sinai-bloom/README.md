# The Mountain in Bloom — Sinai's Flowering at Revelation

**Shavuot theme: Har Sinai / The Flowering Mountain**

The Midrash in *Shir HaShirim Rabbah* 1:12 records that Mount Sinai burst into flower and greenery at the very moment of the Theophany. *Pirkei DeRabbi Eliezer* (ch. 41) explains why Sinai was chosen for the revelation: its humility, not its height. The Shulchan Aruch (Orach Chaim 494:3, Rama) records the custom of decorating synagogues with greenery on Shavuot as a reenactment of this image.

## Artwork

A canvas 2D animation in three phases:

1. **Growth phase (0–7 s):** 10 wildflower plants grow incrementally from the slopes of a dark mountain silhouette against an indigo sky.  Plants are seeded along the left and right slopes at evenly spaced t-values.  Each frame reveals a growing fraction of the pre-computed segment array, creating the impression of roots-to-tips organic growth.

2. **Lightning phase (7–10 s):** 2–3 jagged white-blue polylines flash from the top of the canvas to the mountain peak, regenerated every 8 frames with random opacity (0.3–1.0) for a flicker effect.  Hebrew text הַר סִינַי fades in 1.5 s into this phase.

3. **Hold phase (10–11.5 s):** Plants and Hebrew text remain; lightning dissipates.  Then the cycle resets.

## L-system

```
Axiom: F
Rule:  F → FF+[+F-F-F]-[-F+F+F]
Angle: 25° ± 5° random jitter per branch (seeded per-plant for determinism)
```

The turtle interprets F as "draw forward", + as "turn left", - as "turn right", [ as "push stack", ] as "pop stack".  Bracket nesting depth drives thickness tapering (3 px at root → 0.5 px at tips) and the stem colour interpolation.

**4 iterations** are used for all plants.  The L-system string is expanded once and the resulting segment array (position, thickness, colour, optional flower dot) is stored.  Progressive growth is achieved by drawing only the first `floor(progress × segs.length)` segments each frame.

## Palette

| Element | Colour |
|---------|--------|
| Sky top | `#0a0520` (deep indigo-black) |
| Sky horizon | `#0d2b1a` (dark blue-green, dawn) |
| Mountain silhouette | `#1a1008` (near-black, warm undertone) |
| Stem root | `#1a5c2a` (deep forest green) |
| Stem tip | `#2a8040` (lighter forest green) |
| Flower — cream | `#f5f5e8` |
| Flower — pale purple | `#c8a8e8` |
| Flower — soft gold | `#e8c850` |
| Lightning | `#e8f0ff` (bright white-blue) |
| Hebrew text | `#f5f0e0` (cream) |

## Mountain silhouette

A filled polygon at canvas coordinates (relative to 800 × 600):
```
(0, 450) → (400, 210) → (800, 450) → (800, 600) → (0, 600)
```
Drawing plants first, then painting the mountain polygon on top, naturally hides the roots inside the rock.

## Lightning

`displace(x1, y1, x2, y2, depth=4, spread=30)` recursively midpoint-displaces a vertical line from canvas top to the mountain peak.  Spread scales by 0.55 at each level.  Bolts are regenerated every 8 frames with freshly randomised opacity for the flicker effect.

## Technique

- **L-system expansion** — string rewriting rules applied iteratively
- **Pre-computed segment cache** — turtle walk runs once; growth is progressive array reveal
- **Seeded PRNG (mulberry32)** — angle jitter and flower placement are deterministic per plant
- **Canvas 2D painter's algorithm** — draw order: sky → plants → mountain → lightning → text
- **No external libraries** — fully self-contained single HTML file
