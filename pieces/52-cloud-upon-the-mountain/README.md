# The Cloud Upon the Mountain — Ananei HaKavod

A WebGL fragment shader piece rendering the Ananei HaKavod — Clouds of Glory — of
Exodus 19:9 and 24:15–18 as a volumetric, billowing cloud mass with a fiery interior
glow, hovering above a dark mountain silhouette.

A fullscreen fragment shader generates the cloud using six-octave fractional Brownian
motion (fBm) built from a hash-based value-noise function, with three levels of domain
warping — each layer's noise output offsets the input coordinates of the next — to
produce the characteristic billowing, folded-cloth shapes of a storm cloud. Cloud density
drives a five-stop color gradient: cool blue-grey at the transparent edges, warm ivory
through the cloud body, deep amber (#FF6A00) and gold (#FFD700) in the glowing interior,
and near-white at the hottest core. The fire colors pulse ±15% brightness on a ~5-second
cycle. A multi-peak mountain ridge occupies the lower third as a near-black silhouette,
its summits receiving a warm ambient glow from the cloud above. The Hebrew phrase
**וַיְכַס הֶעָנָן אֶת-הָהָר** — *and the cloud covered the mountain* (Exodus 24:15) —
appears as a ghostly overlay at the cloud's lower edge.

**Theme:** Har Sinai / Ananei HaKavod — Exodus 19:9; 24:15–18  
**Technique:** WebGL fragment shader / layered fBm domain-warped volumetric cloud
