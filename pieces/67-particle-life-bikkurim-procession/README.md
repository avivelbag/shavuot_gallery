# 67 — The Flute Plays Before Them: Bikkurim Procession

**Theme:** Bikkurim  
**Technique:** particle life / multi-species attraction-repulsion

A canvas 2D animation of particle life — a technique in which multiple species of particles
interact through pairwise attraction and repulsion rules, producing spontaneous self-organization
into flocking clusters, rotating rings, and flowing streams without any explicit path.

Three particle species represent the Bikkurim procession (Mishnah Bikkurim 3:3–4):

- **Pilgrims** (#C8A020, 300 particles) — the main body of first-fruits bearers
- **Musicians** (#3A7040, 80 particles) — the flute players and Levitical escorts
- **Escort** (#1A3080, 40 particles) — the officials and honor guard

Interaction is governed by a 3×3 attraction matrix A[i][j] specifying the force coefficient from
species i toward species j. A gentle rightward drift (vx += 0.02 each frame) simulates the
procession's movement toward Jerusalem. Particles wrap toroidally — the procession loops forever.
Velocity is damped (v *= 0.85) and clamped to 3px/frame. Short-range repulsion (R=15) prevents
overlap. Attraction acts within R=120 with linear falloff.

The Hebrew caption at top reads: וְהֶחָלִיל מַכֶּה לִפְנֵיהֶם ("and the flute plays before them"),
the Mishnah's description of the procession's music (Bikkurim 3:3).

**Conceptual note:** The Bikkurim declaration (Deuteronomy 26:5–10, *Arami oved avi*) is the
conceptual ancestor of the Passover Haggadah — the Talmud (Pesachim 116a) and *Sifrei Devarim*
(section 301) instruct that Seder night's obligation of telling the Exodus story is fulfilled
by expounding this declaration phrase by phrase.

**Scripture:** Deuteronomy 26:5–9 (Arami oved avi / wandering Aramean declaration);
Mishnah Bikkurim 3:2–4 (procession choreography and the flute).
