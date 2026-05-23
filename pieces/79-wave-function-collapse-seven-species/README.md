# The Fruit of the Land

**Shavuot theme: Bikkurim / Seven Species**

Wave Function Collapse (WFC) tiles a 16×10 grid with botanical icons of the seven species of the Promised Land — wheat, barley, grapes, figs, pomegranates, olives, and dates — plus connector tiles. Each cell collapses one at a time, one per animation frame, so the visitor watches the mosaic fill itself in from entropy to order. When the grid is complete it pauses briefly and restarts with a new random seed.

## Technique

Canvas 2D, no libraries. WFC with Shannon entropy cell selection, weighted tile sampling, BFS constraint propagation, and contradiction detection with full restart.

**Tile set** — 10 tile types drawn on 64×64 offscreen canvases using Canvas 2D path commands:

| Tile | Species | Dominant color |
|------|---------|---------------|
| wheat | wheat stalk with grain head | `#D4A017` harvest gold |
| barley | barley stalk with long awns | `#D4A017` harvest gold |
| grape | cluster of filled circles | `#6B2D6B` fig purple (used for grape) |
| fig | teardrop shape | `#6B2D6B` fig deep purple |
| pomegranate | round body with crown | `#C0392B` pomegranate red |
| olive | oval with small branch | `#7D8B3A` olive drab |
| date | hanging cluster | `#8B5E3C` date brown |
| stem | plain vertical connector | `#4A7C3F` leaf green |
| ground | plain horizontal ground | `#F5EDD0` warm cream |
| open | plain background tile | `#F5EDD0` warm cream |

**Edge codes** — STEM, LEAF, GROUND, BORDER, OPEN. Two tiles are compatible as neighbors if their shared edge codes match.

**Grid** — 16 columns × 10 rows at 64 px/tile = 1024×640 canvas; scaled via CSS `object-fit: contain`.

## Palette

| Color | Hex |
|-------|-----|
| Harvest gold | `#D4A017` |
| Leaf green | `#4A7C3F` |
| Fig deep purple | `#6B2D6B` |
| Pomegranate red | `#C0392B` |
| Olive drab | `#7D8B3A` |
| Date brown | `#8B5E3C` |
| Warm cream | `#F5EDD0` |
