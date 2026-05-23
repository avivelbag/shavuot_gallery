# Given in the Wilderness — מִדְבָּר

**Technique:** Cellular automaton sand transport / barchan dune formation

**Theme:** Matan Torah — the Torah was given in the wilderness (midbar) so it could belong to everyone

A 300×200 discrete grain-physics simulation. Each cell stores a sand height (0–8). Each time step: saltation moves grains downwind with probability 0.3; avalanche redistributes grains where slope exceeds the angle of repose (threshold 3). After 300 frames, the Hebrew word מִדְבָּר is stamped into the field at maximum height and erodes into the dune landscape over ~200 frames.

The wind slowly rotates 15° every 600 frames (over a 60-frame transition), demonstrating the model's response to changing conditions and producing the characteristic barchan crescent shapes that migrate and merge.

**Shavuot connection:** The Mechilta de-Rabbi Ishmael (Yitro, Bachodesh §1) teaches that the Torah was given specifically in the wilderness — ownerless desert — so that it could belong to all who wish to receive it: "whoever wishes to receive it, let them come and receive it." The root of מִדְבָּר (wilderness) is ד-ב-ר, the same root as דָּבָר (word) — the wilderness is etymologically the place of the word.
