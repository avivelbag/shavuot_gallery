# Spotted Fig, Striped Field

**Theme:** Bikkurim / Seven Species — Deuteronomy 8:8; Mishna Bikkurim 1:3

**Technique:** Gierer-Meinhardt reaction-diffusion (morphogenesis, spot-stripe bifurcation)

## Description

A 256×256 Gierer-Meinhardt (GM) reaction-diffusion simulation that sweeps the inhibitor diffusion
coefficient continuously from the spot regime to the stripe regime and back over forty seconds.

The GM model is a mathematical formalization of Turing's 1952 "local activation / long-range
inhibition" mechanism for biological morphogenesis. A single bifurcation parameter — the ratio of
inhibitor to activator diffusivity — determines whether the steady patterned state consists of
isolated spots (like pomegranate seeds, fig arils, or olive cross-sections) or parallel stripes
(like rows of wheat or barley seen from above). As D_h sweeps from 0.2 to 2.0, the pattern morphs
from spots through a disordered transitional zone into stripes and back again, making visible the
mathematical unity of the seven species of Deuteronomy 8:8.

The color palette maps activator concentration through deep field green → harvest gold →
pomegranate red (spot regime) or harvest gold (stripe regime), with the high-value hue shifting
based on the current D_h to reinforce the wheat-vs-pomegranate visual metaphor.

A faint text overlay at the bottom fades between species labels as D_h crosses the thresholds:
pomegranate seeds (רִמּוֹן) · fig cross-section (תְאֵנָה) · olive grove (זַיִת) · rows of wheat (חִטָּה).

## Files

- `index.html` — self-contained simulation with embedded essay (no external dependencies)
- `thumbnail.svg` — static preview: upper-left shows spot pattern, lower-right shows stripe pattern
- `essay.md` — accompanying essay connecting the GM model to the seven species of Bikkurim
- `README.md` — this file

## Sources

- Deuteronomy 8:8 (the seven species of the Promised Land)
- Mishna Bikkurim 1:3 (only the seven species qualify as bikkurim)
- Turing, A.M. — "The Chemical Basis of Morphogenesis," Philosophical Transactions of the Royal Society B, 237:641 (1952)
- Gierer, A. and Meinhardt, H. — "A theory of biological pattern formation," Kybernetik 12:30–39 (1972)
