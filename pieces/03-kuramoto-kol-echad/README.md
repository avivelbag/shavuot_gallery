# All the People Answered with One Voice

**Piece:** `03-kuramoto-kol-echad`
**Technique:** Kuramoto model (coupled oscillator synchronization)
**Theme:** Matan Torah / collective voice at Sinai (Exodus 24:3; Shabbat 86b)

## What it shows

300 oscillators with natural frequencies drawn from a Lorentzian distribution begin spinning independently — displayed as a rainbow of colors. As the coupling constant K ramps from 0 to 3.0 over 15 seconds, they spontaneously phase-lock into a single collective rhythm and the canvas turns gold. K is held at 3.0 for 10 seconds before ramping back to 0 and looping.

## Technical notes

- Euler integration with dt = 0.016 s (one frame at 60 fps)
- Mean-field Kuramoto update: O(N) per frame
- Lorentzian (Cauchy) frequencies: ωᵢ = 1.0 + 0.5·tan(π·(Uᵢ − 0.5)), clamped to [0.1, 3.0]
- Critical coupling Kc = 2Γ = 1.0 for this distribution
- Order parameter r = |N⁻¹ Σ eⁱᵠ| displayed live
- Phase-to-color: HSL hue = (φ/2π)×360, S=80%, L=55%; blends to gold as r → 1
- Coupling lines drawn between oscillators within 80 px; opacity ∝ sin(φⱼ − φᵢ) clamped positive
