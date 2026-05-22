# Until the Morning Light — Clifford Attractor

**Theme:** Tikkun Leil Shavuot — the all-night vigil of Torah study on the eve of Shavuot

**Technique:** Clifford attractor / density histogram

Eight million points iterated through the Clifford map (*x' = sin(a·y) + c·cos(a·x), y' = sin(b·x) + d·cos(b·y)*) accumulate into a Float32Array density buffer, tone-mapped logarithmically to a five-stop navy→indigo→blue→gold→cream palette on a near-black ground (#030510). The attractor is built in batches of 40,000 points per animation frame (~200 frames total), re-rendering every 5 frames so the luminous figure-of-eight "develops" on screen like a long-exposure photograph. On completion, the Hebrew label עַד אוֹר הַבֹּקֶר ("until the morning light") fades in at the bottom.

Parameters a=−1.4, b=1.6, c=1.0, d=0.7 are validated at startup (first 1000 points must remain within ±2.5 in both axes); if the check fails, fallback parameters a=−1.7, b=1.8, c=−0.9, d=−0.4 are used.

The essay cites Song of Songs 5:2 (the "I sleep" verse applied by the Magen Avraham to Israel oversleeping at Sinai), Zohar Emor III 98a (the source of the custom), and the Pri Etz Chaim (the Ari's kabbalistic "wedding night" reason for the vigil).

**Piece ID:** 64-clifford-attractor-tikkun-leil  
**Year:** 2026
