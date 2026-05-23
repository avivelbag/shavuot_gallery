# Letters That Give Life — Conway's Game of Life

**Shavuot theme:** Matan Torah — the giving of the Torah at Sinai on Shavuot.

The word אנכי ("Anochi", the first word of the Ten Commandments) is pixel-rendered onto a 300×200 GoL grid and released. The letterforms dissolve into oscillators, still lifes, and gliders — a living aftermath of the original inscription.

## Technique

**Grid:** 300×200 boolean cells on a toroidal (wrap-around) surface. One GoL step per animation frame (~60fps).

**Letter rendering:** Each of the 4 Hebrew letters (Yod, Kaf, Nun, Aleph — right-to-left in visual order) is stored as a 9-integer bitmask (7 bits per row, bit 6 = leftmost column). Rendered at 2× pixel scale onto the grid, centered. The full word occupies ~68×18 grid cells at seeding.

**GoL rules (B3/S23):** A dead cell with exactly 3 live neighbors becomes alive. A live cell with 2 or 3 live neighbors survives. All other transitions produce or preserve death.

**Rendering:** Each grid cell maps to an `ImageData` pixel: alive = gold `#E8C438` (232,196,56), dead = near-black `#070502` (7,5,2). An offscreen 300×200 canvas is upscaled via `drawImage` to fill the display panel.

**Text overlay:** At frame 600 (~10 seconds), the word אָנֹכִי fades in as a semi-transparent CSS text element (opacity 0.5, cream `#F5F0E0`) at the top of the art panel. It fades out after 3 seconds (frame 780). CSS `transition: opacity 1.5s ease` handles both fades.

## Palette

| Role | Hex | RGB |
|------|-----|-----|
| Alive cell (gold) | `#E8C438` | 232, 196, 56 |
| Dead cell (near-black) | `#070502` | 7, 5, 2 |
| Text overlay (cream) | `#F5F0E0` | 245, 240, 224 |
| Background | `#070502` | 7, 5, 2 |

## Letter bitmasks

The 7×9 pixel-art letters use bit 6 as the leftmost column and bit 0 as the rightmost. Reading order is right-to-left (Hebrew), so the letters are laid out on the canvas as: Yod (leftmost) → Kaf → Nun → Aleph (rightmost). The bitmasks are designed to be recognizable pixel-art approximations, not typographic replicas.
