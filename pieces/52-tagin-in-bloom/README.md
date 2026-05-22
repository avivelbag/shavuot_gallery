# Crowns Upon the Letters — Tagin in Bloom

**Technique:** Gray-Scott reaction-diffusion seeded by Hebrew letterforms

The tagin (תַּגִּין) are the scribal crowns drawn atop seven specific Hebrew letters in every Torah scroll: שׁ עָ טָ נָ זָ גָ יָ (sha'atnez getz). The Talmud (Menachot 29b) records that Moses saw God tying these crowns onto the letters at Sinai and was told they encode meaning beyond immediate legibility — Rabbi Akiva would one day derive mountains of halacha from each one.

This piece applies the Gray-Scott reaction-diffusion model to the Hebrew word **תּוֹרָה** (Torah). The letter bodies are rasterized onto a 300×300 simulation grid as seed concentrations. The reaction-diffusion equations then run with parameters in the coral-growth regime (F=0.055, k=0.062), causing organic tendrils to bloom outward from the letter forms — visually enacting the Talmudic story: the letters contain latent potential that, given time and the right conditions, blossoms visibly into crown-like structures.

## Color palette

Deep midnight blue `#0A0A1F` at V=0 to bright gold `#FFD700` at V=1 — dark parchment with gold ink, evoking a Torah scroll written in fire on fire.

## Loop

After ~5000 simulation steps the tendril field converges. Non-letter areas are gently reset over 200 frames (V fades exponentially), then the bloom restarts from the initial letter seeds — the cycle of latent potential perpetually re-emerging.

## Distinction from piece 07

Piece 07 (milk-honey reaction-diffusion) uses random circular seeds on a cream-to-amber palette with Du=0.16/Dv=0.08 parameters. This piece uses Hebrew letterform seeds, a midnight-blue-to-gold palette, Du=0.21/Dv=0.105, a reset loop, and a thematic focus on tagin/scribal marks rather than agricultural abundance.
