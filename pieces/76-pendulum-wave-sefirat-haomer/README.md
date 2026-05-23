# Forty-Nine Voices in Time

**Theme:** Sefirat HaOmer — the 49-day count from Passover to Shavuot (Leviticus 23:15–16)

**Technique:** Pendulum wave / simple harmonic oscillator ensemble — canvas 2D animation

## Description

49 pendulums hang from a horizontal bar. Pendulum *k* is tuned so it completes exactly *k* full oscillations in T₁ = 3.0 seconds — the period of the slowest pendulum. All begin at the same angle (θ₀ = 0.3 radians) and swing as θ_k(t) = θ₀ · cos(ω_k · t). The ensemble fans out into waves, spirals, and apparent chaos before re-synchronizing exactly at t = T₁, looping continuously.

Each pendulum's bob leaves a fading trail of its last 120 positions. Colors cycle from violet (day 1) through gold (day 49) using HSL(h, 80%, 60%) where h = (k/49)×300. A day counter and the word שָׁבוּעוֹת (Shavuot) appear as an overlay.

The 49 pendulums map to the 49 days of the Omer, grouped into 7 columns of 7 (one column per week/Sefirah). The re-synchronization at t = T₁ corresponds to the arrival of Shavuot.

## Physics

```
ω_k = k · 2π / T₁
L_k = g / ω_k²    (g = 9.8 m/s²)
```

With T₁ = 3.0 s: L₁ ≈ 2.24 m (longest), L₄₉ ≈ 0.00093 m (shortest).  
Pixel lengths are mapped linearly from physical lengths: longest → 80% canvas height, shortest → 20 px minimum.

## Sources

- Leviticus 23:15–16 (the biblical commandment)
- Arizal, *Sha'ar haKavanot*, Derush Sefirat HaOmer (canonical Kabbalistic source for the 7×7 Sefirot structure)
- Sefat Emet, *Emor* (personal obligation to count)
- Talmud Bavli, Menachot 65b (night counting, temimot)

## Files

- `index.html` — self-contained canvas animation (no external dependencies)
- `thumbnail.svg` — static preview showing 7 pendulums (one per Sefirah-week) mid-swing
- `essay.md` — accompanying essay on Sefirat HaOmer and pendulum wave physics
