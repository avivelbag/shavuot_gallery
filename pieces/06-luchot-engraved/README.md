# Engraved in Stone — Luchot HaBrit

**Shavuot theme: Matan Torah / The Two Tablets**

The forty days and forty nights that Moses spent on Sinai ended with two stone tablets inscribed by the hand of God with the Ten Commandments — the foundational covenant between the divine and Israel, sealed at Shavuot. This piece renders those tablets as they might be imagined: rough-hewn limestone, letters carved deep into the face of the stone, glowing amber with the fire that wreathed the mountain.

## Artwork

Two arched stone tablets stand side by side. The left tablet bears the first five commandments; the right carries commandments six through ten — in Hebrew, in the brief traditional heading forms used in liturgical memory. The arch at the top of each tablet mirrors the rounded shape depicted in centuries of illuminated manuscripts and synagogue art.

The commandments, left to right on the left tablet:

| # | Hebrew |
|---|--------|
| I | אָנֹכִי |
| II | לֹא יִהְיֶה |
| III | לֹא תִשָּׂא |
| IV | זָכוֹר |
| V | כַּבֵּד |

And on the right tablet:

| # | Hebrew |
|---|--------|
| VI | לֹא תִרְצָח |
| VII | לֹא תִנְאָף |
| VIII | לֹא תִגְנֹב |
| IX | לֹא-תַעֲנֶה |
| X | לֹא תַחְמֹד |

## Technique

**Stone texture** — `feTurbulence type="fractalNoise"` with `numOctaves="3"` feeds into `feDisplacementMap` at `scale="5"`, producing pixel-level roughness that reads as hewn limestone without distorting the tablet silhouette.

**Carved letterforms** — near-white (`#f0ece0`) Hebrew text using `direction="rtl"` and `unicode-bidi="bidi-override"` for correct RTL rendering. An SVG filter (`feOffset` + `feComposite`) creates a dark drop-shadow offset that simulates the shadow cast by a chiselled groove when light falls from above-left.

**Glow animation** — a warm amber (`#c87820`) overlay rect on each tablet, driven by a CSS `@keyframes glow` animation at 8 s period (`ease-in-out infinite alternate`). No JavaScript.

**Self-contained** — the entire piece is a single HTML file with inline SVG and CSS. No external resources are loaded.

## Palette

| Element | Colour |
|---------|--------|
| Background | `#0e0c08` (near-black, warm-tinted) |
| Stone (light) | `#c8c0b0` |
| Stone (shadow) | `#8a8a8a` |
| Carved letters | `#f0ece0` (near-white) |
| Chisel shadow | `#180e04` |
| Glow | `#c87820` (amber-gold) |
| Ground fire | `#b05010` |
