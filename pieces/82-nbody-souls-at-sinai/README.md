# Every Soul That Ever Was — N-Body Souls at Sinai

**Shavuot theme: Matan Torah / all souls at Sinai**

The Talmud in Shevuot (39a) and the Midrash Tanchuma (Nitzavim 3) teach that every Jewish soul — including all those not yet born — was present at the giving of the Torah on Sinai. Deuteronomy 29:14 is the textual anchor: "also with those who are not here with us today." The covenant was not made with one cohort in one desert but with every soul across all time, simultaneously.

## Artwork

A canvas 2D N-body gravitational simulation. 300 particles orbit a single fixed "Sinai" attractor using leapfrog (Verlet velocity) integration at dt=0.016s. No inter-particle gravity — particles only feel the central Sinai mass — keeping the simulation O(N) and stable at 60fps.

### Initial conditions

Particles are spawned in three "generations" of 100 each:

- **Generation 1** (r=80–120px): warm gold `#E8C060` — souls physically at Sinai; nearly circular orbits
- **Generation 2** (r=180–240px): sky blue `#6090D0` — later generations; more eccentric ellipses
- **Generation 3** (r=300–380px): violet `#9060C0` — far-future souls; highly elliptical, some nearly radial

Initial velocities are set to circular-orbit speed `v = sqrt(G*M/r)` ± 20% random perturbation.

### Integration

Leapfrog (Verlet velocity): half-kick velocity, full drift position, half-kick velocity again at new position. Symplectic, energy-conserving, stable for long orbital integrations.

### Rendering

- Background: deep black `#04030A`; each frame fills with `rgba(4,3,10,0.15)` rather than clearing, creating slow-fade afterimage trails
- Each particle: 2px filled circle at generation colour
- Orbital trail: ring buffer of last 30 positions per particle, drawn at `alpha = 0.05 * (i/30)`
- Sinai attractor: radial gradient white glow, radius 8px
- Escape prevention: velocity reflected toward center if distance exceeds 500px

### Palette

| Element          | Colour                      |
|------------------|-----------------------------|
| Background       | `#04030A` deep black        |
| Generation 1     | `#E8C060` warm gold         |
| Generation 2     | `#6090D0` sky blue          |
| Generation 3     | `#9060C0` violet            |
| Sinai glow       | `#FFFFFF` → transparent     |

## Technique

- **N-body gravitational simulation** — not previously used in this gallery (central attractor only, O(N))
- **Leapfrog (Verlet velocity) integration** — symplectic, energy-conserving
- **Softened gravitational force** `F = G*m1*m2 / (r² + ε²)` with ε=15 to prevent singularity
- **Orbital trail ring buffer** — last 30 positions per particle, fading alpha
- **Frame persistence** — partial canvas fill for accumulated afterimage effect
- **No external libraries** — fully self-contained single HTML file
