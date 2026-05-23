# The Essence of a Sapphire Brick — Dendritic Crystal Growth

**Technique:** Gravner-Griffeath hexagonal cellular automaton / dendritic crystal growth  
**Theme:** Har Sinai / the two tablets / sapphire pavement

Implements the Gravner-Griffeath "Snowflake" cellular automaton on a 300×300 hexagonal grid.
Each cell holds a liquid water value u ∈ [0,1] and a boolean frozen flag. Starting from a
single frozen seed at the center, a diffusion field propagates outward and crystallizes at the
boundary wherever the local water density exceeds threshold θ = 0.5. The six-fold symmetry
emerges purely from the hexagonal neighbor topology — no randomness is introduced.

The piece is thematically grounded in Exodus 24:10: when Moses and the seventy elders ascended
Sinai, they saw the God of Israel standing on a pavement of sapphire, clear as the sky itself.
The Talmud (Megillah 29a, Berachot 55a) records that the Tablets of the Law were hewn from this
sapphire beneath the Throne of Glory — pre-cosmic substance given physical form. The crystal
growing outward from a single seed images the pre-existing law crystallizing into visible form.
