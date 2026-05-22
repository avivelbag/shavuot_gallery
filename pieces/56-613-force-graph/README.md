# 56 — 613 Paths — Force-Directed Network of the Mitzvot

**Theme:** Matan Torah / Torah and mitzvot  
**Technique:** Force-directed graph (spring simulation, spatial-grid repulsion)

## Shavuot Connection

Shavuot is the anniversary of Matan Torah — the moment 613 commandments were given at Sinai. Rabbi Simlai's teaching in Talmud Bavli Makkot 23b assigns 248 positive commandments (the number of limbs in the body) and 365 negative commandments (days of the solar year). This piece makes that number visually tangible through a force-directed graph: 613 glowing nodes, gold for positive and violet for negative, clustering by Maimonidean book through spring forces alone.

## Algorithm

### Node Data

613 nodes are hardcoded as `{id, polarity: 'pos'|'neg', book: 1..14}`, using Maimonides' 14-book structure from the *Mishneh Torah*. The distribution of 248 positive and 365 negative commandments across the fourteen books follows the Maimonidean arrangement.

### Force Simulation

A simplified spatial-grid repulsion (not full Barnes-Hut, but a 20×20 grid approximation) runs each frame:

1. **Grid phase:** nodes are bucketed into cells.
2. **Repulsion phase:** each node accumulates a repulsion force from nearby nodes in adjacent grid cells.
3. **Attraction phase:** for each intra-book edge, Hooke's law pulls the two endpoints together toward a rest length.
4. **Integration:** velocities are damped by 0.85 per frame; positions are updated and clamped to canvas bounds.

The simulation runs for 120 frames, after which stabilization is detected and the slow ambient drift begins (magnitude ~0.05 px per frame random perturbation).

### Edges

Intra-book edges only — each node connects to up to 3 nearest same-book neighbors by initial proximity. This keeps total edge count under ~1000 and rendering fast while making the cluster structure visible.

### Hover

On `mousemove`, the nearest node within 12 px is highlighted with a bright glow ring. A tooltip `<div>` overlay shows מ״ע / מ״ל (positive/negative) and the Maimonidean book number and name.

## Palette

| Role | Hex |
|---|---|
| Positive (aseh) | `#D4A820` (warm harvest gold) |
| Negative (lo ta'aseh) | `#4A1E8A` (deep violet) |
| Edge | `#FFFFFF` at 0.08 opacity |
| Background | `#080510` |
| Glow highlight | `#FFD700` |

## Source References

- Talmud Bavli, Makkot 23b (Rabbi Simlai's teaching)
- Mishnah Oholot 1:8 (248 limbs)
- Maimonides, Mishneh Torah (14-book structure)
- Sefer HaChinuch (13th c., systematic treatment of all 613)
