# Four Entered the Orchard — Kleinian Group Schottky Limit Set

A full-viewport canvas animation of the Schottky Kleinian group limit set, rendered
by breadth-first orbit tracing (Indra's Pearls algorithm). Two pairs of generator
Möbius transformations — g₁, g₁⁻¹, g₂, g₂⁻¹ — act on four mutually tangent
("kissing") circles arranged at (±0.6, 0) and (0, ±0.6) with radius 0.35. The
kissing configuration produces a limit set with four visible spiral arms.

Each animation frame slowly rotates all four generating circle centers by ω = 0.003
rad/frame, recomputing the Möbius matrices before rendering up to 50,000 circles per
frame. Rendering terminates per-branch when a transformed circle's screen radius
falls below 0.5 px or depth exceeds 18. Color depends on which generator sequence
produced the orbit image: deep violet (#1A0035), midnight blue (#0A0A2E), gold
(#C8A435), white-hot (#FFFDF0). Alpha fades with depth for a glowing effect at the
fractal boundary.

The four spiral arms evoke the four sages of Talmud Chagigah 14b who entered Pardes:
Ben Azzai, Ben Zoma, Acher (Elisha ben Abuyah), and Rabbi Akiva. The limit set —
always approached, never reached — renders the boundary of mystical understanding
that the text warns can only be entered safely by one who is fully prepared.

Studied on Tikkun Leil Shavuot, the all-night Torah session before the dawn of
revelation at Shavuot.

**Theme:** Tikkun Leil Shavuot / Pardes — Talmud Chagigah 14b  
**Technique:** Kleinian group Schottky limit set (iterated Möbius transformations)
