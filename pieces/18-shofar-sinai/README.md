# Growing Louder — The Shofar at Sinai

**Theme:** Har Sinai / The Shofar Blast — Exodus 19:19, the voice of the shofar that grew louder and louder

**Technique:** Canvas 2D additive waveform synthesis, oscilloscope animation

## Description

A looping canvas animation rendering the shofar at Sinai as an oscilloscope display of additive sine wave synthesis. Seven harmonics (f, 2f, 3f … 7f) of a base frequency matching the shofar's natural overtone series are drawn individually as faint amber overlays, then summed into a single composite waveform shown as a thick near-white line.

Over a 10-second cycle the amplitude envelope grows from near-zero to full canvas height — mimicking the Torah's description that "the voice of the shofar grew louder and louder" (Exodus 19:19). At the end of each cycle the waveform briefly decays and the cycle restarts from silence.

Hebrew text וְקוֹל הַשּׁוֹפָר הוֹלֵךְ וְחָזֵק מְאֹד appears in gold above the canvas, right-to-left.

**Palette:** Deep blue-black (`#0d0d1a`) background, near-white (`#f0ece0`) composite waveform, amber (`#d4a017`) harmonic overlays and Hebrew text.

## Animation details

- `t = performance.now() / 1000` — time in seconds
- For each pixel x: `y = centerY + amp(t) × Σ Aₖ sin(2π·k·f·x/W + φₖ + t·sₖ)`
- Envelope: `amp(t) = (H·0.45 / Σ Aₖ) × pow(t%10 / 10, 1.5)` growing phase; quadratic decay over final 0.5 s
- Harmonic amplitudes Aₖ = 1/k (natural overtone series), normalized so composite peak = H·0.45
- Animation targets 60 fps via `requestAnimationFrame`

## Sources

- Exodus 19:13 (long blast, signal to ascend)
- Exodus 19:16–19 (thunder, lightning, thick cloud, shofar)
- Leviticus 25:9 (shofar of Jubilee)
- Mekhilta de-Rabbi Ishmael, Yitro, Bachodesh 4
- Talmud Bavli Rosh Hashanah 26a
- Maimonides, Mishneh Torah, Laws of Repentance 3:4

## Files

- `index.html` — self-contained canvas animation (no external dependencies)
- `thumbnail.svg` — static SVG preview showing composite waveform with amber harmonic overlays
- `essay.md` — accompanying essay on the shofar at Sinai as sound before speech
