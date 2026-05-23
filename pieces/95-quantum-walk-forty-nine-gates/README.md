# 95 — The Gate That No Creature May Enter

**Quantum Walk on 49 Gates of Understanding**

A 2D discrete-time quantum walk on a 49×49 grid, themed on the Talmudic teaching
(Rosh Hashanah 21b) that fifty gates of understanding were created in the world and
all were given to Moses except the fiftieth, which belongs to God alone. Shavuot
falls on the fiftieth day of the Omer count.

## Concept

The 49×49 grid represents the forty-nine attainable gates. The corner cell at
position (48,48) — which would be the fiftieth gate — carries an absorbing boundary
condition: amplitude arriving there is zeroed out at every step. The quantum walk
begins at the centre (24,24) in equal superposition across all four coin directions
and spreads outward by interference over 49 steps, mirroring the Sefirat HaOmer count.

The result is ballistic spreading with interference fringes: probability blooms in
gold across the grid while the 50th gate corner stays permanently dark.

## Technical

- **Algorithm:** 2D discrete-time quantum walk with Grover coin
- **State:** Float64Array of real and imaginary parts; index `(x*49+y)*4+coin`
- **Grover coin:** C(d,d) = -1/2, C(d,d') = 1/2 for d≠d'
- **Shift:** each coin component moves one step in its direction per frame
- **Absorbing boundary:** ψ[48][48][*] = 0 after each step
- **Rendering:** probability mapped indigo→violet→gold with additive blending

## Files

- `index.html` — full-viewport canvas with embedded essay
- `essay.md` — the standalone essay (~480 words)
- `thumbnail.svg` — 400×400 SVG preview (7×7 probability grid)
- `README.md` — this file

## Sources

- Talmud Bavli, Rosh Hashanah 21b — fifty gates of understanding
- Leviticus 23:15–16 — the commandment to count fifty days of the Omer
- Psalm 8:6 — "You have made him slightly less than divine"
