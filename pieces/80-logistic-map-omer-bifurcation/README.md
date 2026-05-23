# Order Hidden Within the Count — Sefirat HaOmer

**Theme:** Sefirat HaOmer — the 49-day count from Pesach to Shavuot (Leviticus 23:15–16); the Kabbalistic 7×7 sefirot grid of the Omer (Tanya; Sefat Emet)

**Technique:** Logistic map bifurcation diagram — density-estimation rendering, per-column histogram normalization, animated left-to-right scan

## Description

A full-viewport canvas renders the bifurcation diagram of the logistic map x₍ₙ₊₁₎ = r·xₙ·(1−xₙ) for r ∈ [2.5, 4.0]. For each of 800 columns, the map is iterated 300 times to discard the transient, then 200 samples are accumulated into a per-pixel density counter. After per-column normalization, the density is mapped to a harvest-gold palette: deep indigo for empty pixels, blue for sparse, wheat-gold for medium density, off-white for high density. The diagram reveals period-doubling bifurcations, the onset of chaos, and the Feigenbaum constant δ ≈ 4.669 governing the spacing.

49 faint vertical tick marks overlay the diagram — one per Omer day, barely visible at `rgba(255,255,255,0.08)`. The 50th mark at r = 4.0 is labeled with the Hebrew letter נ (nun, 50), the edge of full chaos and the uncountable gate.

The diagram animates column by column at 20 columns per frame (~0.7 s to complete). Clicking the canvas re-renders with a new random starting point x₀ ∈ (0,1), demonstrating that the long-term structure is independent of initial conditions.

## Shavuot Connection

The Omer is counted forward — not down to zero but up toward 50. The Kabbalistic tradition (Tanya, Sefat Emet) maps the 49 days onto 7×7 pairings of the sefirot, making the count combinatorially rich rather than merely linear. The bifurcation diagram enacts this: what looks like a simple parameter scan reveals fractal depth at every scale — windows of perfect order nested inside chaos, self-similarity without end, mirroring the Kabbalistic claim that each of the 49 days contains the totality of the others.

## Sources

- Leviticus 23:15–16 (the commandment to count)
- Tanya, Iggeret HaTeshuvah (Sefirot map of the Omer)
- Sefat Emet, Shavuot (combinatorial structure of the 49 days)
- Mitchell Feigenbaum, "Quantitative Universality for a Class of Nonlinear Transformations," Journal of Statistical Physics, 1978

## Files

- `index.html` — self-contained interactive canvas animation (no external dependencies)
- `thumbnail.svg` — static 400×400 stylized bifurcation tree in gold on indigo
- `essay.md` — essay connecting Sefirat HaOmer to the logistic map
