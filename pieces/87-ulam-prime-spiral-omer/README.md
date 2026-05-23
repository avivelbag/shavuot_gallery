# The Fifty Gates: A Prime Spiral

**Theme:** Sefirat HaOmer / 49 gates of understanding — Rosh Hashanah 21b; Leviticus 23:15–16; Zohar, Parashat Emor

**Technique:** Ulam prime spiral / Sieve of Eratosthenes / Canvas 2D animation

## Description

Numbers 1–2401 (49×49) arranged in a square Ulam spiral from the center outward, with primes highlighted. The Sieve of Eratosthenes identifies primes at startup. Non-primes are rendered in near-black; primes 1–49 in wheat gold (#D4A840); the 50th prime (229) in brilliant white with a soft glow; primes beyond 50 in muted indigo (#303060). A faint line traces the spiral path.

On load, cells are revealed one by one along the spiral path at ~40 cells per rAF frame. When a prime is encountered it flashes briefly brighter. When the 50th prime (229) is placed, the reveal pauses one second, then the cell pulses three times with a white halo before the reveal continues. After the full grid is placed, the 50th prime breathes gently at 0.3 Hz.

A counter in the upper-right displays "Day N of 49 / Gate N of 50", incrementing with each prime found, and freezes at "Day 49 of 49 / Gate 50 of 50" on completion.

## Sources

- Leviticus 23:15–16 (the Omer commandment)
- Talmud Bavli, Rosh Hashanah 21b (fifty gates of understanding)
- Psalm 8:6 (cited by the Talmud)
- Zohar, Parashat Emor (7×7 sefirot mapping of the Omer)
- Sefer HaChinuch, Mitzvah 306

## Files

- `index.html` — self-contained animation (no external dependencies)
- `essay.md` — accompanying essay
- `thumbnail.svg` — static preview: 21×21 center section with primes in gold and the 50th prime in white
- `README.md` — this file
