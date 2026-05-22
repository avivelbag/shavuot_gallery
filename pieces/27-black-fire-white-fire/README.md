# Black Fire on White Fire — Cellular Automaton Torah Letters

**Shavuot theme: Matan Torah / The Primordial Torah**

The Midrash (Devarim Rabbah 3:12; Yerushalmi Shekalim 6:1) teaches that the Torah was written as *eish shechorah al gabbe eish levanah* — black fire upon white fire. Bereishit Rabbah (1:1) holds that the Torah served as the blueprint (*amon*) through which the world was created: it is therefore not merely a text but a primordial structure predating physical creation.

## Artwork

A canvas 2D probabilistic cellular automaton. Each of the 22 Hebrew letters is cycled one at a time:

1. **Seed phase (0–0.6 s):** The letter is rasterized onto a hidden 200×150 canvas using `fillText`, pixel data is read via `getImageData`, and bright pixels become live cells in the CA grid.

2. **Burn phase (0.6–4 s):** The CA evolves each frame using probabilistic fire rules:
   - Live cell: survives with P_SURVIVE = 0.88; dies otherwise.
   - Dead cell: ignites if it has ≥ 1 live neighbor AND `random() < P_SPREAD × neighborCount` (P_SPREAD = 0.12).
   - The letterform spreads outward, flickers, and develops organic motion.

3. **Decay phase (4–5 s):** P_SURVIVE ramps linearly from 0.88 down to 0, causing the fire to extinguish. The next letter then seeds from the residue.

## Cellular Automaton

- **Grid:** 200 × 150 cells (two-state: 0 = dead, 1 = alive)
- **Neighborhood:** 8-connected Moore neighborhood
- **Heat system:** Each cell accumulates a float heat value (0.0–1.0). Live cells warm up (+0.15/frame), dead cells cool down (−0.04/frame). Color is derived from heat for smooth fade-in/out.
- **Rendering:** Heat values are mapped to an ImageData buffer (200×150) and blitted scaled to the full canvas via `drawImage`.

## Palette

| Element           | Colour                           |
|-------------------|----------------------------------|
| Dead / background | `#0A0A12` (near-black)           |
| Live / fire core  | `#E8E8FF` (silver-white-blue)    |
| Mid-heat          | Interpolated via gamma curve     |

The color mapping uses a γ = 1.5 curve (t = h^1.5) to produce a bright core with a smooth dark halo.

## Letters

All 22 Hebrew letters cycle in Aleph–Tav order, repeating indefinitely:
א ב ג ד ה ו ז ח ט י כ ל מ נ ס ע פ צ ק ר ש ת

## Technique

- **Probabilistic cellular automaton** — novel to this gallery
- **Letter rasterization via hidden canvas** — `fillText` + `getImageData`
- **Heat-based rendering** — smooth fade-in/out without explicit alpha
- **ImageData blit** — single `putImageData` + scaled `drawImage` per frame
- **No external libraries** — fully self-contained single HTML file
- **60 fps cap** — frame throttle via `FRAME_MIN_MS = 1000/60`
