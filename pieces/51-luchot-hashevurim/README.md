# Both the Tablets and the Fragments — Luchot HaShevurim

Piece 51 of the Shavuot gallery. Canvas animation of stone tablet shattering and reassembling, illustrating the Talmudic teaching (Bava Batra 14b) that both the whole second tablets and the broken fragments of the first were kept in the Ark of the Covenant.

## Technique

Voronoi fragment physics on the HTML canvas. Shard geometry is computed once at init via Sutherland-Hodgman polygon clipping of the tablet rectangle against perpendicular bisector half-planes for 12 seed points. All subsequent animation is rigid-body translation and rotation of the fixed polygon vertex arrays.

## Animation phases (looping ~13.5s cycle)

1. **Whole** (4s): limestone tablet with engraved Hebrew inscription, stone grain overlay
2. **Shattering** (2s): crack-glow in amber, shards fly apart with randomised velocity and angular spin
3. **Scattered** (3s): shards at rest with warm ambient glow
4. **Reassembling** (4.5s): shards lerp back to original positions; crack lines fade in and remain visible

## Color palette

| Element | Color | Hex |
|---|---|---|
| Tablet face | Warm limestone | `#D4C5A9` |
| Engravings / cracks | Dark slate | `#2A2520` |
| Background | Deep earthy charcoal | `#1A1510` |
| Crack glow | Amber | `#FF8C00` |

## Files

- `index.html` — self-contained piece (no external deps)
- `essay.md` — ~600-word essay on Exodus 32:19, Bava Batra 14b, and the Shavuot dimension of the shattering
- `thumbnail.svg` — split-tablet SVG thumbnail with crack lines
