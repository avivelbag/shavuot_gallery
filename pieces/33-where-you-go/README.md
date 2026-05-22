# Where You Go — String Art Portrait of Ruth

**Piece 33** | 2026

**Technique:** canvas 2D — greedy string art / thread portrait

**Theme:** Book of Ruth / Ruth 1:16 — voluntary loyalty and covenant

256 pins are placed uniformly around a circle. A greedy algorithm selects ~4,000 lines between pin pairs, preferring pairs whose connecting line passes through the darkest regions of a target silhouette — two humanoid figures leaning toward each other, converging at a shared road. Lines are drawn at low opacity (~10%) in warm linen-white on a dark field-brown background; their overlapping density builds the figures from pure geometry.

The piece is entirely self-contained: the silhouette is defined as a signed-distance-field function in JavaScript (no external images). It animates progressively — one line added per frame — holds the completed portrait for three seconds, then fades and restarts.

The Hebrew verse "כִּי אֶל-אֲשֶׁר תֵּלְכִי אֵלֵךְ" (Ruth 1:16) is typeset below the circle. The essay in the right panel explains why Ruth's declaration of loyalty is read on Shavuot: her voluntary acceptance of Torah and the Jewish people mirrors Israel's *naaseh v'nishma* at Sinai, as the Talmud (Yevamot 47b) makes explicit.
