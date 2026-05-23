# The Whole Mountain Quaked

## Fire, Smoke, and Trembling

Exodus 19:18 reads: "And Mount Sinai was entirely in smoke, because the LORD descended upon it in fire; and its smoke ascended like the smoke of a furnace, and the whole mountain quaked greatly (וַיֶּחֱרַד כָּל-הָהָר מְאֹד)." Three phenomena are layered here: fire below, smoke ascending, and then — as a third, distinct event — the mountain itself trembles. The verse is not a figure of speech. The Torah names each phenomenon separately, and the trembling of the mountain is the last and most specific.

## Ḥarad — Terror of the Living, Terror of Stone

The verb used for the mountain's shaking is חרד (ḥarad). This is a striking choice. In the Torah, ḥarad almost always describes the response of conscious beings to overwhelming experience: Isaac trembled greatly when he understood what had happened with the blessing (Genesis 27:33); the Israelites were terrified when they heard of Pharaoh's approach (Exodus 14:10); the people trembled at Sinai in Exodus 19:16, using this same root. The word belongs, in its ordinary Torah usage, to creatures with hearts that pound.

Exodus 19:18 is the only place in the entire Torah where ḥarad describes inanimate matter. The mountain does what living creatures do when they encounter the unbearable. Stone behaves like flesh. The created order, ordinarily indifferent to revelation, participates in it.

## The Mechilta: A World That Felt the Weight

The Mechilta de-Rabbi Ishmael (on Exodus 19:18) does not read the mountain's trembling as hyperbole or metaphor. It interprets it as a cosmological event: the entire created order — not Israel alone, not the mountain alone, but the physical world as such — felt the weight of the divine presence descending. The revelation at Sinai was not a private transaction between God and one nation standing at a mountain's foot. It was an event that reorganized the physical world's sense of what it was capable of experiencing. Mountains could tremble. Rock had always had the capacity for terror; Sinai was the moment that capacity was activated.

## Shabbat 88a: The Israelites Move Backward

The Talmud (Shabbat 88a) adds another layer to the theophany's physical overwhelming. At each of the Ten Commandments, the Israelites — already trembling at the foot of the mountain — recoiled backward 12 mil, approximately ten miles. They fled from the sound of the divine voice. Then the angels who attend the divine presence had to escort them back to their places before the next commandment could be given. This happened ten times: ten flights, ten angelic escorts. The act of receiving Torah was not passive reception. It was physically violent — a body thrown backward by sound, escorted back by celestial hands, thrown again.

The revelation that shook the mountain also threw the people. The mountain's ḥarad and the people's ḥarad were the same event, felt by stone and by flesh simultaneously.

## Shavuot: Receiving a Torah That Shook the World

Shavuot commemorates not just the receiving of the commandments but the receiving of a Torah that shook the world when it arrived. The mountain did not stay still and let the law land on it gently. The world reorganized itself around the event. What the festival asks us to remember, year after year, is that the Torah was not received in tranquility. It arrived like a seismic event — physically, cosmologically, in stone and in people simultaneously.

## This Piece

The animation generates a fractal terrain using the diamond-square algorithm, producing a 65×65 heightmap with natural mountain ridges and valleys. The algorithm works by recursively subdividing a grid: at each pass, diamond centers are set to the average of their four corners plus a random displacement, then square edge midpoints are set to the average of their neighbors plus a displacement. Each pass halves the displacement magnitude, controlled by a roughness parameter (0.65 here — dramatic but not chaotic). The result is a Float32Array normalized to [0,1].

Two heightmaps are held simultaneously — H_current and H_next — and the displayed terrain is a linear interpolation between them over 120 frames. When the interpolation completes, H_current becomes H_next, and a new H_next is generated. The mountain never settles. It continuously restructures itself, ridge by ridge, valley by valley, as if some invisible seismic force is always moving through its substrate. This is the quaking of Sinai: not a single event, but the permanent condition of a world that received the Torah and was never the same shape again.

The isometric projection renders each cell as a filled rhombus with top, left, and right faces shaded at different brightnesses, giving the illusion of depth. Smoke particles drift upward from the summit. A faint red glow runs along the base, suggesting the fire in which the LORD descended.
