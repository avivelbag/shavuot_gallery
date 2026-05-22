# Rose of Sharon — Rhodonea Curves of the Covenant

A canvas-based animation of six overlapping rhodonea (polar rose) curves on a
deep indigo background, evoking the rose of Sharon from Song of Songs 2:1 and
the kabbalistic reading of Shavuot as the *chag of deveikut* — the festival of
divine union.

Six distinct rational k = p/q values (3, 5/2, 7/3, 4/3, 8/3, 9/4) produce
petal counts of 3, 10, 7, 8, 16, and 9 respectively. Each curve rotates at an
independent speed (0.0003–0.0008 rad/frame). Every ~20 seconds, each curve's
k parameter begins drifting slowly toward a new rational target, morphing the
petal count over approximately 600 frames.

Curves are drawn with `globalCompositeOperation = 'screen'` on the dark
background so overlapping petals accumulate luminosity. Shadow blur (6–14 px)
adds a soft glow to each stroke.

The Hebrew inscription — *אֲנִי חֲבַצֶּלֶת הַשָּׁרוֹן* ("I am the rose of
Sharon", Song of Songs 2:1) — is rendered below the mandala form in a calm
serif typeface.

**Theme:** Shir HaShirim / Deveikut — Song of Songs 2:1; Shabbat 88b;
Yadayim 3:5 (Rabbi Akiva, "holy of holies")

**Technique:** canvas 2D — rhodonea polar curves, rational k = p/q parametric
form, independent rotation, slow k-drift, screen compositing, shadow glow
