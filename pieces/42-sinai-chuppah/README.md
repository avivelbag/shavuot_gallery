# The Mountain as Canopy — Sinai Chuppah

A canvas-based 2D spring-mass cloth simulation rendering the chuppah of Sinai —
the mountain suspended overhead like a wedding canopy, as described in the
Talmudic midrash of Shabbat 88a and the wedding imagery of Song of Songs Rabbah.

The simulation runs a 22×22 grid of particles (484 total) connected by
structural (horizontal and vertical), shear (diagonal), and bend (two-apart)
springs. Verlet integration with 0.988 velocity damping and 8 constraint-
satisfaction iterations per frame produces stable, naturally billowing fabric
at 60 fps.

The top row is pinned — fixed in place, representing the immovable mountain
held overhead. Gravity (0.22 px/frame²) pulls the remaining 462 free particles
downward. A sinusoidal wind force with two incommensurate frequencies
(`0.09 * sin(t * 0.003) * sin(t * 0.007)`) provides non-repeating, natural
billow.

Each 2×2 quad is rendered as a filled quadrilateral. Color is mapped by the
average y-position of the quad's four corners along a three-stop gradient:
- Deep cobalt #1B2F6E at the pinned top (sky-facing, heavy with the weight of heaven)
- Cloud white #F5F0E8 through the middle billowing folds
- Pale gold #F5E6A0 at the freely swinging bottom (lit from below by the fire of Sinai)

The Hebrew ultimatum "אִם-תְּקַבְּלוּ הַתּוֹרָה" ("if you accept the Torah")
appears below the billowing canopy in a calm serif, evoking the words spoken
under the mountain.

**Theme:** Matan Torah — Shabbat 88a (mountain suspended like a barrel);
Song of Songs Rabbah 3:11 (Sinai as chuppah); Avodah Zarah 2b (Torah offered to all nations)

**Technique:** canvas 2D — Verlet-integration spring-mass cloth simulation,
filled quadrilateral patch rendering, height-mapped color gradient
