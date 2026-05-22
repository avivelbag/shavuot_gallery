# And Sinai Was Covered in Flowers — Eden Growth Bloom

**Shavuot theme: Har Sinai / Matan Torah — the flowering of the mountain**

The Midrash in Shir HaShirim Rabbah (4:12) and Pirkei DeRabbi Eliezer (ch. 41) teach that at the moment the Torah was given, Mount Sinai burst into bloom — the barren desert mountain suddenly covered with grasses and flowers. This piece renders that blooming as a stochastic Eden growth model: cells accrete outward from a single mountain-peak seed, filling the canvas with a dense, lush, petal-shaped cluster.

## Artwork

A canvas 2D Eden growth model running on a pointy-top hex grid. Growth begins from a single seed cell at the canvas centre (350, 350). At each step, a random cell from the current frontier is selected and added to the cluster. The hex grid produces more organic, rounded shapes than a square grid.

### Algorithm

- **Hex grid:** axial coordinates, pointy-top orientation; HEX_SIZE = 4px circumradius
- **Frontier:** maintained as a parallel array + Set (for O(1) membership tests); new cells are added using O(1) swap-remove from the array
- **Growth rate:** 12 cells per animation frame (~16 seconds to fill a 700×700 canvas)
- **Boundary check:** cells whose pixel centre falls outside the canvas are excluded from the frontier

### Color

Each cell is colored by its pixel distance from the seed using a 4-stop floral palette:

| Distance | Color |
|----------|-------|
| Core (0%) | `#3A1E6A` — deep mountain violet |
| Inner (33%) | `#C06080` — warm rose |
| Mid (67%) | `#D4A820` — wheat gold |
| Edge (100%) | `#FFF8F0` — pale cream |

### Phases

1. **Bloom:** the cluster grows from the centre outward, covering the canvas over ~16 seconds
2. **Hebrew text:** *וְהַר סִינַי עָשָׁן כֻּלּוֹ* (Exodus 19:18, "And Mount Sinai smoked altogether") drawn at canvas centre at start; naturally covered by the bloom as it expands
3. **Shimmer:** after bloom completion, the outermost ~7% of cells pulse their opacity (0.72–1.0) with individual random phases, suggesting the mountain breathing

## Palette

| Element | Colour |
|---------|--------|
| Background | `#100820` (very dark purple-black) |
| Core cells | `#3A1E6A` (deep violet) |
| Mid cells | `#C06080` (rose), `#D4A820` (gold) |
| Edge cells | `#FFF8F0` (pale cream) |

## Technique

- **Eden model / stochastic boundary accretion** — not previously used in this gallery
- **Pointy-top hex grid in axial coordinates** with O(1) frontier management (swap-remove)
- **4-stop distance palette interpolation** for the floral color gradient
- **Canvas shimmer animation** with per-cell random phase for organic breathing effect
- **No external libraries** — fully self-contained single HTML file
