# Chesed Like Water — Physarum Pathways

A Physarum polycephalum slime-mold simulation on an HTML5 canvas. Ten thousand agents
move across a 400×300 trail grid, each sensing in three forward directions (straight,
±45°) and turning toward the strongest chemical signal. Each frame, agents deposit trail
at their new position; the trail then diffuses (3×3 box blur) and decays. Three food
sources — Naomi (נ) at the apex, Ruth (ר) and Boaz (ב) at the base — anchor the
network; the slime mold grows to connect them along the most efficient paths, with no
central coordination.

Color palette: deep warm cream background (#FAF0DC), trail network in soft amber-gold
(#D4882A) fading to warm rust (#8B3A10) at maximum concentration. After approximately
1800 frames (~30 seconds at 60 fps), the simulation enters drift mode: trail decay
increases and agent step size decreases, thinning the network to its most-traveled
connections without restarting — keeping the piece alive indefinitely.

**Theme:** Chesed / Book of Ruth — Ruth, Naomi, and Boaz as the three poles of a network
of lovingkindness that finds its paths spontaneously, without obligation  
**Technique:** Physarum polycephalum slime-mold simulation, canvas 2D ImageData pixel
rendering, pre-computed color LUT, double-buffered trail diffusion
