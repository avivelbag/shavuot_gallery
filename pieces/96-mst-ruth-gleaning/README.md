# 96 — She Went and Gleaned in the Field

**Theme:** Book of Ruth / Bikkurim / harvest
**Technique:** Minimum spanning tree (Kruskal's algorithm animated)
**Year:** 2026

## Description

N=280 grain points are scattered across the canvas in slightly irregular
horizontal rows, mimicking the pattern of a real barley field. Kruskal's
algorithm then builds a minimum spanning tree across all points, advancing
three edges per animation frame. Each accepted edge grows as a smooth stroke
over 12 frames; rejected (cycle-forming) edges flash briefly in muted red.

One grain point — Ruth — is distinguished as a larger amber circle near the
centre of the field. When her point first receives an MST edge it pulses gold
and the label "רות" appears for two seconds. The four corner clusters (the
peah — the corners the law commands be left for gleaners) are deferred until
last: when their edges finally close the tree, each corner pulses in bright
gold.

After the full MST is built the field holds for three seconds, then scatters
and restarts.

## Theological focus

Ruth 2:2–3 describes Ruth gleaning in Boaz's field. The text says *va-yiker
mikreha* — "her chance happened to her" — a phrase the Talmud (Megillah 13a)
reads as concealed Providence. Kruskal's algorithm makes the same point from
the opposite direction: purely local decisions (always pick the shortest
available edge) converge on a globally optimal structure — the minimum
spanning tree. What looks like wandering turns out to be optimal.

The law of peah (Leviticus 19:9–10) commands farmers to leave field corners
unharvested for the poor, the stranger, the widow, and the orphan. The
animation enacts this by deferring the corner cluster edges until the very
end, letting the harvest-tree complete everywhere else before the corners are
finally gathered.

## Sources

- Ruth 2:2–3 (Ruth gleans in Boaz's field)
- Leviticus 19:9–10 (the law of peah and leket)
- Talmud Megillah 13a (providential reading of *mikreh*)
- Kruskal (1956): "On the Shortest Spanning Subtree of a Graph"

## Files

| File | Purpose |
|------|---------|
| `index.html` | Self-contained canvas animation + embedded essay |
| `essay.md` | Standalone essay (~350 words) |
| `thumbnail.svg` | 400×400 static preview showing partial MST |
| `README.md` | This file |
