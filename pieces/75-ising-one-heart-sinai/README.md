# Piece 75 — As One Person, With One Heart

**Theme:** Matan Torah
**Technique:** 2D Ising model / Metropolis-Hastings phase transition

A real-time simulation of the 2D ferromagnetic Ising model on a 200×200 lattice using the
Metropolis-Hastings algorithm. The piece animates the phase transition from disorder (high
temperature, random spins) to order (low temperature, aligned spins), mapping it to Rashi's
observation that Israel encamped at Sinai "as one person with one heart" — a collective unity
that was a prerequisite for receiving the Torah, not merely a side note.

## Physics

The 2D square-lattice Ising model has an exact critical temperature T_c = 2/ln(1+√2) ≈ 2.2692
(Onsager, 1944). Each spin σ_i ∈ {±1} interacts with its four nearest neighbors (J=1, no
external field). The Hamiltonian is H = −Σ σ_i σ_j. The Metropolis algorithm proposes a single
spin flip; the energy change is ΔE = 2·σ_i·(σ_up + σ_down + σ_left + σ_right). The flip is
accepted if ΔE ≤ 0 or with probability exp(−ΔE/T).

## Temperature schedule

- T=4.5 → start (fully disordered, salt-and-pepper noise)
- Decrease by 0.001 every 60 frames
- Pause 300 frames at T=2.4 (critical fluctuations — fractal domains)
- Continue decreasing to T=1.5 (ordered state)
- Hold 300 frames at T=1.5
- Reset to T=4.5 and repeat

## Files

- `index.html` — self-contained animation with embedded essay
- `essay.md` — source essay text (~420 words)
- `thumbnail.svg` — 400×400 hand-crafted SVG of a critical-point spin configuration
- `README.md` — this file

## Color palette

- Spin +1: wheat gold #E8C438 (R=232 G=196 B=56)
- Spin -1: sapphire blue #1A3068 (R=26 G=48 B=104)
- Hebrew overlay text: cream #F5F0E0 at opacity 0.75

## Performance

40,000 Metropolis steps per animation frame (~1 full sweep of the 200×200 lattice).
The exp(−ΔE/T) lookup table is precomputed and updated only when T changes by more than 0.0005,
avoiding per-step Math.exp calls. Runs at 60 fps on any modern browser.

## Sinai connection

Rashi on Exodus 19:2 (citing Mechilta): Israel encamped at Sinai *ke-ish echad be-lev echad* —
"as one person with one heart." This is the prerequisite for revelation: the phase transition
from disorder to collective unity, which statistical physics shows cannot happen gradually but
only by crossing a sharp critical threshold.
