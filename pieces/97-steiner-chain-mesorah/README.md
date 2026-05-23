# Links That Never Break

**Piece 97 — Shavuot Gallery**

An animated Steiner chain of 7 circles orbiting the annular gap between two fixed golden bounding circles. The seven chain circles represent the seven generations of Torah transmission in Pirkei Avot 1:1, each labeled with its Hebrew name. The chain is constructed via inversion: both bounding circles are mapped to concentric rings, the 7 equal tangent circles placed trivially in that frame, then inverted back. Animation rotates the angle in the concentric frame each tick; Steiner's porism guarantees the chain always closes.

## Connection to Shavuot

- **Pirkei Avot 1:1 and Shavuot.** Pirkei Avot is studied on the Shabbatot between Pesach and Shavuot, framing the festival as the origin of an unbroken chain of tradition: Sinai → Moshe → Yehoshua → Elders → Prophets → Men of the Great Assembly.
- **Steiner's porism as mesorah.** The porism states that a Steiner chain closes from *any* starting position — closure is structural, not conditional. This is the mathematical image of a tradition that survives exile, dispersion, and persecution by virtue of its design.
- **Inversion as adaptation.** Conformal inversion transforms a hard problem into a trivial one and maps back; the mesorah similarly adapts to each generation's language and context while preserving the essential tangency between teacher and student.

## Technical approach

- **Fixed circles:** outer circle centered at canvas center, radius R_out = min(W,H)×0.42; inner circle offset by R_out×0.15 along x, radius R_in = R_out×0.35.
- **Limit points:** solved from the Apollonius condition |P−O1|²/r1² = |P−O2|²/r2², reducing to a 1-D quadratic on the x-axis.
- **Inversion circle:** center at the limit point outside both circles, radius ρ = √(power of L w.r.t. outer circle).
- **Concentric frame:** invert both bounding circles → concentric pair with radii ρ_in, ρ_out. Place 7 equal circles of radius r_c = (ρ_out−ρ_in)/2 at distance ρ_in+r_c from center, at angles θ + 2πj/7.
- **Invert back:** apply circle inversion formula: center' = L + ρ²(C−L)/(|C−L|²−r²), radius' = ρ²r/||C−L|²−r²|.
- **Pulse:** inner circle radius oscillates ±2% at 0.5 Hz (sin wave, 2π×0.5/60 rad/frame).
- **Animation:** θ increments by ω=0.004 rad/frame; canvas redrawn each requestAnimationFrame.

## Palette

| Role | Color |
|------|-------|
| Moses (משה) | #1A3A6B deep blue |
| Joshua (יהושע) | #8B2020 crimson |
| Elders (הזקנים) | #2A5E2A forest green |
| Prophets (הנביאים) | #C87020 amber |
| Men of Great Assembly | #5A2080 violet |
| Shimon HaTzaddik | #1A6060 teal |
| Antigonus | #E8DFC0 ivory |
| Bounding circles | #BF9B30 gold |

## Files

| File | Purpose |
|------|---------|
| `index.html` | Animated piece with embedded essay |
| `essay.md` | Standalone essay (~400 words) |
| `thumbnail.svg` | 400×400 static SVG of the full Steiner 7-chain |
| `README.md` | This file |
