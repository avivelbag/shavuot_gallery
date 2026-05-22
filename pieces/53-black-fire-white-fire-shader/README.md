# Black Fire on White Fire — Torah as Living Flame

**Technique:** WebGL fragment shader with Hebrew text glow texture and FBM fire distortion

The three opening words of the Aseret HaDibrot (Ten Commandments) — *אָנֹכִי יְהֹוָה אֱלֹהֶיךָ* (Exodus 20:2) — are rendered as white-hot fire using a WebGL GLSL fragment shader.

## Approach

A 1024×512 offscreen canvas pre-renders the Hebrew phrase with layered shadow-blur passes (blurs 0–48px) to produce a smooth SDF-like glow field: each pixel holds a brightness value proportional to its closeness to the nearest letter. This texture is uploaded as a WebGL sampler.

The fragment shader distorts the UV lookup by a fractional Brownian motion offset (5-octave FBM, amplitude 0.014) so the letter boundaries breathe and flicker continuously. Colors are mapped by the field value: background (#0A0D1A) → ember red (#CC2200) → flame orange (#FF7A1A) → hot yellow (#FFE566) → white core (#FFFDE8). A second FBM field adds a low-opacity warm luminescence (#F5F0E8, ~6%) over the whole background — the "white fire" ground of the Midrash.

## Distinguishing features from piece 27-black-fire-white-fire

Piece 27 uses a cellular-automaton approach (canvas 2D). This piece uses a WebGL GLSL fragment shader with a pre-rendered SDF texture and real-time FBM distortion — entirely different technique, different visuals, and different text (the opening of the Decalogue vs. a general אש motif).

## Color palette

| Role             | Hex       |
|------------------|-----------|
| Smoke background | `#0A0D1A` |
| Ember red        | `#CC2200` |
| Flame orange     | `#FF7A1A` |
| Hot yellow       | `#FFE566` |
| White core       | `#FFFDE8` |
| White-fire ground| `#F5F0E8` |

## Theme

Matan Torah — the giving of the Torah at Sinai. The Midrash (Tanhuma Bereishit 1; Devarim Rabbah 3:12) teaches the Torah was written in black fire on white fire; the artwork renders both fires simultaneously as living, animated flame.

## Animation

Runs at ~60fps via `requestAnimationFrame`. Canvas resizes to viewport on window resize with device-pixel-ratio awareness (capped at 2×). No audio. Loops seamlessly.
