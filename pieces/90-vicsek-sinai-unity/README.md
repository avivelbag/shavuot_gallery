# As One Person, with One Heart

**Shavuot theme: Matan Torah / unity at Sinai**

At Exodus 19:2, the Torah uses the singular verb *va'yichan* — "he encamped" — to describe all of Israel arriving at Sinai. Rashi's comment: *ke'ish echad be'lev echad*, "as one person with one heart." The Mechilta observes that this unity preceded the revelation; it was not a gift but a precondition.

This piece makes that moment visible through the Vicsek model: a minimal active-matter simulation where self-propelled particles align only with their neighbors. Below a critical noise threshold, a disordered swarm spontaneously orders into coherent collective motion — no leader, no center, only local alignment. The phase transition is sharp and sudden: chaos snaps into unity.

## Technique

**Vicsek active-matter model** — each frame, every particle computes the mean heading of all particles within radius *r* = 40 px (using `atan2(Σ sin θ, Σ cos θ)`), then sets its new heading to that mean plus noise `η · U[-π, π]`. Position is updated at constant speed *v* = 1.5 px/frame with toroidal boundary conditions.

**Mountain collision** — the Sinai peak is a triangle at bottom-center (20% of canvas height). Particles that land inside the triangle are reflected across the nearest edge normal and nudged back outside.

**Noise schedule** — η starts at 0.85 (fully disordered), decreases linearly to 0.05 over 12 s (the phase transition occurs near η ≈ 0.3), holds for 8 s at η = 0.05 (unified flow), then spikes to 0.85 over 2 s and repeats.

**Color by alignment** — each particle's alignment score `cos(θ − mean_θ_neighbors)` maps to: gold `#D4A017` (aligned), violet `#6B3FA0` (intermediate), indigo `#1A1A4E` (disordered).

**Order parameter** — `φ = |Σ e^(iθ)| / N` displayed as "Alignment: X%" in the HUD.

## Palette

| Element | Colour |
|---------|--------|
| Background | `#0a0a18` |
| Aligned particles | `#D4A017` (wheat gold) |
| Intermediate | `#6B3FA0` (twilight violet) |
| Disordered | `#1A1A4E` (deep indigo) |
| Mountain | `#2A2A2A` (dark charcoal) |
| HUD text | `rgba(180,170,150,0.5)` |
