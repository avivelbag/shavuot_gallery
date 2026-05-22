# From Ruth to David — The Living Branch

**Shavuot theme: The Book of Ruth / Davidic Genealogy**

The closing genealogy of the Book of Ruth (Ruth 4:18–22) traces the lineage from Peretz to King David in ten generations. The Yerushalmi Talmud (Chagigah 2:3) holds that David was born and died on Shavuot, making the Book of Ruth the story of how one woman's *hesed* — loving-kindness — grew into a royal line over ten generations.

## Artwork

A botanical tree grows upward from the base of the canvas on a parchment field. The trunk begins at Peretz and climbs through nine sequential branches to David at the crown. Each branch is a smooth quadratic Bézier curve drawn progressively in warm sienna. The horizontal wobble of the control points alternates left and right at each generation, giving the chain a gentle botanical curve rather than a rigid spine.

**Nodes:** Ten cream circles, one per generation, appear by fading in once their incoming branch arrives. Each circle contains the Hebrew name of the ancestor in right-to-left serif text, with font size reduced automatically if the name exceeds the circle's diameter.

**Root figure:** A minimal silhouetted female form below Peretz's node represents Ruth — the starting point not listed in the genealogy but whose *hesed* made the entire chain possible.

**Crown:** A three-peaked gold crown appears above David's node once the tree reaches full growth.

**Gold pulse:** David's node emits a pulsing radial gradient glow in gold (#D4A017) after the tree completes, referencing the Yerushalmi tradition that David was born on Shavuot.

## Animation timing

- Initial delay: 0.5 seconds
- Duration per branch: 0.78 seconds
- Total growth: approximately 7.5 seconds
- Crown and glow: appear after the final branch completes

## Palette

| Element | Colour |
|---------|--------|
| Background | `#F5EDD6` (parchment) |
| Branches | `#7B3F00` (warm sienna) |
| Node circles | `#FFF5DC` (cream) |
| Node text | `#3A1A00` (dark brown) |
| Root figure | `#3A1A00` (deep brown) |
| Crown / glow | `#D4A017` (gold) |

## Technique

**Animated botanical Bézier tree** — each of the nine edges stores a draw-progress value `t` (0 → 1). Each frame advances `t` at a rate derived from total elapsed time, staggered by generation index so each branch triggers only after its parent completes. The bezier curve is sampled at `t * N` steps per frame to produce the growing-branch effect. All drawing is canvas 2D with no external libraries.
