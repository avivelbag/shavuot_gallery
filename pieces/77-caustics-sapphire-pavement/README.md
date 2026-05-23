# Like the Very Sky for Purity

**Theme:** Har Sinai — Exodus 24:10, the sapphire pavement beneath the divine presence

**Technique:** Caustics simulation / ray refraction / height-field surface — canvas 2D animation

## Description

Moses, Aaron, Nadab, Abihu, and the seventy elders ascended Sinai and beheld the God of Israel. The Torah describes one specific thing beneath the divine presence: a pavement of sapphire, clear as the sky. This piece renders that pavement as a physically-grounded caustics simulation.

A 120×120 grid of rays (14,400 total) is cast downward through a time-varying height field that models a transparent refracting surface. Each ray bends according to its local surface normal (computed via finite differences), lands on the image plane below, and deposits energy there via bilinear splat. The accumulated energy is normalized and colorized from deep sapphire (#0D1B6B) through cornflower (#4A7BC8) to ice white (#E8F4FF) — the palette of "sapphire, clear as the sky."

The height field evolves continuously, driven by three independent sinusoidal components at slightly different frequencies, producing gently shifting caustic patterns that suggest the shimmer of a lit sapphire pool.

## Physics

```
h(x,y,t) = 0.08 · [sin(4.0·x + p₁) + sin(4.0·y + p₂) + 0.5·sin(2.8·(x+y) + p₃)]

Normal: (-∂h/∂x, -∂h/∂y)  via central finite differences with ε = 1/N
Refraction offset: eta = 0.33  (≈ n_water − n_air, scaled for visual effect)
Landing position: (gx + eta·nx, gy + eta·ny)

Phase increments per frame: Δp₁=0.012, Δp₂=0.015, Δp₃=0.009
```

## Commentary

Rashi (following Midrash Tanchuma) reads the sapphire pavement as present before God during the slavery — a reminder of the clay bricks trodden by Israel. Nahmanides insists the verse describes literal perception. Ibn Ezra suggests "sapphire" is the sky itself, making Sinai the axis mundi where heaven meets earth.

The caustics simulation enacts Ibn Ezra's reading: the refracted light that pools on the floor of a lit pool is the same quality of light the Torah calls "like the very heaven for purity."

## Sources

- Exodus 24:10 (the verse)
- Rashi on Exodus 24:10 (citing Midrash Tanchuma, Terumah 8)
- Nahmanides (Ramban) on Exodus 24:10
- Ibn Ezra on Exodus 24:10

## Files

- `index.html` — self-contained caustics animation (no external dependencies)
- `thumbnail.svg` — static preview: radial sapphire gradient with caustic curve overlays
- `essay.md` — accompanying essay on Exodus 24:10 and the commentators
