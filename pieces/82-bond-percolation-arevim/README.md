# Guarantors for One Another

**Shavuot theme: Matan Torah / kol Yisrael arevim**

The Talmud (Shevuot 39a) teaches *kol Yisrael arevim zeh bazeh* — all Israel are guarantors for one another. This doctrine of mutual guarantorship (*arvut*) is derived directly from the moment at Sinai when the entire people answered the covenant together (Exodus 19:8). Because they accepted the Torah as one, the obligation of each is entangled with the obligation of every other.

Bond percolation renders this with mathematical precision: a 60×60 lattice of nodes, with bonds added one per frame in random order. Below the critical threshold (~50% of bonds), only isolated clusters exist. At the threshold, a spanning component suddenly appears — every node in it reachable from every other. That is the "Sinai moment."

## Technique

Pure canvas 2D. No libraries.

**Union-Find:** Path-compressed, union by rank (sz). Per-root boolean flags `top`, `bot`, `lft`, `rgt` track whether the component touches each grid edge. Spanning is detected the instant a union produces a root with `top && bot` or `lft && rgt`. Cost: O(α(N)) per bond.

**Bond ordering:** All horizontal and vertical bonds on the lattice are pre-generated and shuffled with Fisher-Yates (xorshift32 PRNG, fixed seed). One bond is popped per animation frame, giving a smooth, reproducible animation.

**Color logic:**
| Component state | Color |
|-----------------|-------|
| < 5 nodes | Dim grey `#444444` |
| Largest, < 10% of grid | Muted blue `#4060A0` |
| Largest, ≥ 10% of grid | Royal blue `#2060E0` |
| Spanning (Sinai moment) | Gold `#F0C040` |
| Non-spanning after Sinai | Fade to near-black `#111111` over 60 frames |

**Spanning detection:** Per-root bitflags accumulated during union. O(1) per union, no per-frame scan needed.

**Reset:** After a 3-second hold at the Sinai moment, the simulation re-initialises with a fresh shuffle, allowing the loop to show a different random percolation path each cycle.

## Palette

| Element | Colour |
|---------|--------|
| Background | `#0A0A14` |
| Small clusters | `#444444` |
| Growing giant | `#2060E0` |
| Spanning (Sinai) | `#F0C040` |
| Post-Sinai others | `#111111` |
