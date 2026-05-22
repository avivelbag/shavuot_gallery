# 57 — Ten Roots: Newton's Fractal of the Commandments

**Theme:** Matan Torah / Aseret HaDibrot (the Ten Commandments at Sinai)

**Technique:** Newton fractal / complex root convergence — WebGL fragment shader

Each pixel of the canvas corresponds to a starting point in the complex plane. Newton's method is applied iteratively to find a root of `f(z) = z¹⁰ − 1`. The ten convergence basins — one per root of unity — are colored with a fire-and-stone palette keyed to the Aseret HaDibrot enumerated in Exodus 20. The fractal boundary, where convergence is ambiguous, mirrors the halakhic boundary where ethical complexity accumulates.

**Source:** Exodus 20:1–14

**Files:**
- `index.html` — WebGL fractal renderer with embedded essay and commandments legend
- `essay.md` — Essay on Aseret HaDibrot, rabbinic enumeration, and the fractal boundary as halakhic metaphor
- `thumbnail.svg` — Schematic ten-petal pie chart showing basin colors
