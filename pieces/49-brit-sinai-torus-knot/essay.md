# An Everlasting Covenant — The Torus Knot of Sinai

**Exodus 24:7–8**

> *וַיִּקַּח סֵפֶר הַבְּרִית וַיִּקְרָא בְּאָזְנֵי הָעָם וַיֹּאמְרוּ כֹּל אֲשֶׁר-דִּבֶּר יְהוָה נַעֲשֶׂה וְנִשְׁמָע׃ וַיִּקַּח מֹשֶׁה אֶת-הַדָּם וַיִּזְרֹק עַל-הָעָם וַיֹּאמֶר הִנֵּה דַם-הַבְּרִית אֲשֶׁר כָּרַת יְהוָה עִמָּכֶם עַל כָּל-הַדְּבָרִים הָאֵלֶּה׃*

> *"And he took the book of the covenant and read it in the hearing of the people; and they said, 'All that the LORD has spoken we will do and we will hear.' And Moses took the blood and dashed it on the people, and said, 'See the blood of the covenant that the LORD has made with you in accordance with all these words.'"*

---

## What a Brit Is

A *brit* — a covenant — was a familiar instrument in the ancient Near East long before the Israelites arrived at Sinai. Hittite and Mesopotamian documents preserve the genre in detail: a suzerainty treaty in which a great king enumerated his past benefits, stated his present claims, imposed binding obligations on a vassal nation, and accepted obligations in return. What made the agreement legally operative was the cutting ritual. Animals were sliced down the middle; the parties walked between the pieces, calling upon themselves the fate of the animals if they violated the terms. The Hebrew idiom *karat brit*, to cut a covenant, encodes this ceremony literally. The cutting is the contract.

What makes the Sinai covenant theologically astonishing is the identity of the parties. Exodus 24 is not describing Israel's subjugation to a divine sovereign. It is describing a bilateral legal agreement. The obligations run in both directions. God accepts them as freely as Israel does — or appears to. The prophets — Isaiah, Jeremiah, Hosea — will spend centuries invoking the terms of this treaty against all parties, including against God himself. "Remember your covenant" is not a prayer; it is a legal demand. This is the radical claim of the text: the Creator of heaven and earth has entered into a binding relationship with a human nation.

---

## The Mountain Over Their Heads

But the Talmud records a disturbing detail. The Babylonian Talmud (Shabbat 88a) transmits a tradition in the name of Rav Avdimi bar Hama bar Hassa: when the Torah was offered at Sinai, the Holy One, Blessed be He, held Mount Sinai over the heads of the Israelites like an inverted barrel — a *gigit*, a cask — and declared: "If you accept the Torah, good; if not, this will be your grave."

This image inverts the covenant formula entirely. Acceptance under the threat of death is not acceptance. Talmudic law recognizes *ones* — duress — as vitiating contractual obligations. A *brit* made with a sword at your throat is not a *brit*; it is extortion. So the rabbis face a genuine legal problem: if the Sinai covenant was invalid at the moment of its making, what makes any of it binding? Does the whole edifice rest on coercion?

The answer arrives in the Book of Esther, six centuries later. Esther 9:27 records how the Jews of Persia responded to the Purim miracle: *kiym'u v'kiblu*, "they established and accepted." The rabbis (Shabbat 88a) read the doubling as temporal: the Israelites had previously accepted the Torah at Sinai under duress; in Persia, they reaffirmed it freely. The Sinai covenant, made under the shadow of the mountain, was retroactively validated by a free choice made in exile. The *brit* was not dead; it was waiting to be ratified by people who had nothing to gain and no mountain over their heads.

---

## The Geometry of Eternity

A torus knot is a closed curve on the surface of a torus — a donut shape — that winds *p* times around the central axis and *q* times through the hole, without ever crossing itself. Unlike a simple loop, which is topologically trivial and deformable to a point, a torus knot is topologically locked. No continuous deformation can convert it into an unknot without cutting the curve. It has no start and no end. It cannot be loosened, unraveled, or slipped off. The only way to change its topology is to break it.

This is the geometry of *brit olam*, an eternal covenant. A *brit olam* cannot be dissolved through negotiation, through lapse, through forgetting, or through conquest. It can only be ended by destroying the relationship itself — one of the parties, or the bond between them. The term appears throughout Tanach: with Noah (Genesis 9:16), with Abraham (Genesis 17:7), with the Levitical priesthood, with David. In each case, what "eternal" means is precisely this topological property: the knot cannot be untied from within the knot.

The piece renders a (3,2) torus knot: three winds around the torus axis, two through its hole. It is the simplest non-trivial torus knot — not a trefoil (which is a (2,3) torus knot by one convention), but closely related. As it tumbles slowly on all three axes, the gold emission ridge catches the directional light, giving the appearance of a braided cord of ancient gold. The covenant formula **נַעֲשֶׂה וְנִשְׁמָע** — we will do and we will hear — is canvas-rendered in white and mapped onto the tube surface, running along the cord's full length.

---

## The Visualization

A (3,2) torus knot is built from scratch as a WebGL tube mesh: 240 segments along the parametric curve, 10 sides per cross-section. Frenet-Serret frames are parallel-transported along the curve to avoid twist artifacts. A Phong-style fragment shader provides ambient and directional lighting from above-right, with a gold emission stripe calculated from the world-upward component of each fragment's surface normal. The covenant formula is rendered onto a 512×64 canvas and uploaded as a WebGL texture, mapped along the full length of the tube. The knot rotates meditative on all three axes — 0.003 radians per frame in X, 0.007 in Y, 0.001 in Z — a slow, weightless tumble through a field of deep midnight blue. No external libraries; raw WebGL 1 with typed arrays throughout.
