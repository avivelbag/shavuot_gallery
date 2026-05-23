# The Aleph That Contains Everything

**Technique:** Spectre aperiodic monotile (substitution rules), canvas 2D  
**Theme:** Matan Torah / the Aleph of Anochi  
**Source:** Exodus 20; Makkot 24a; Baal Shem Tov / Zoharic tradition

## Description

The spectre monotile (Smith, Myers, Kaplan & Goodman-Strauss, 2023) is a single 14-sided equilateral polygon that tiles the plane aperiodically without reflections — the first such shape ever discovered. This piece renders it through substitution rules: one tile inflates into eight, iterated four times to fill the canvas.

Centered behind the tiling glows a faint Hebrew Aleph (א) in flame gold — the silent first letter of *Anochi*, the opening word of the Ten Commandments. According to the Zoharic/Chasidic tradition associated with the Baal Shem Tov, all Israel heard only this letter directly from God. The Aleph makes no sound. It contains everything.

Every four seconds, one randomly chosen tile briefly brightens to full gold and fades — an ember in the divine script.

## Palette

- Aleph-ink black `#0A0A14`
- Deep lapis `#1B2A6B`
- Faded parchment `#F5EDD6`
- Flame gold `#D4A017`

## Files

- `index.html` — full-viewport canvas with embedded essay
- `essay.md` — standalone essay text (~500 words)
- `thumbnail.svg` — 400×400 static preview
- `README.md` — this file

## Mathematical note

The spectre's 14 edges all have equal length; interior angles follow the pattern that prevents any translational symmetry while requiring only rotation (no reflection). The substitution rule maps each tile to a cluster of 8 child tiles at specified offsets and orientations, producing coverage of the plane at every iteration level.
